"""Mesh helpers shared by part builders: SDF to mesh, plane cuts, custom normals, thickening.

Body coordinates (u, x, z) are used by the SDF modules; Blender coordinates are
X = x, Y = u minus WHEELBASE / 2, Z = z.
"""
import bmesh
import bpy
import numpy as np
from skimage.measure import marching_cubes

from blender.lib import conventions as C

HALF_WB = C.WHEELBASE / 2.0


def to_blender(u, x, z):
    return np.stack([x, u - HALF_WB, z], axis=-1)


def to_body(co):
    co = np.asarray(co)
    return co[..., 1] + HALF_WB, co[..., 0], co[..., 2]


def sample_volume(fn, bounds, h):
    (u0, u1), (x0, x1), (z0, z1) = bounds
    us = np.arange(u0, u1 + h * 0.5, h)
    xs = np.arange(x0, x1 + h * 0.5, h)
    zs = np.arange(z0, z1 + h * 0.5, h)
    X, Z = np.meshgrid(xs, zs, indexing="ij")
    vol = np.empty((len(us), len(xs), len(zs)), np.float32)
    for i, u in enumerate(us):
        vol[i] = fn(np.full_like(X, u), X, Z)
    return vol, (us[0], xs[0], zs[0])


def decimate_arrays(co, faces, target_faces):
    """Quadric edge collapse in MeshLab with normal preservation, so no face ever flips.

    Blender's collapse decimation folds triangles in flat areas; through glass those folds
    show as shards. pymeshlab needs libopengl0 on Linux (apt) for its filter plugins.
    """
    import pymeshlab
    ms = pymeshlab.MeshSet()
    ms.add_mesh(pymeshlab.Mesh(vertex_matrix=np.asarray(co, np.float64), face_matrix=np.asarray(faces, np.int32)))
    ms.meshing_decimation_quadric_edge_collapse(
        targetfacenum=int(target_faces), qualitythr=0.4, preserveboundary=True, boundaryweight=2.0,
        preservenormal=True, preservetopology=True, optimalplacement=True, planarquadric=True,
        planarweight=0.001, autoclean=True)
    m = ms.current_mesh()
    return m.vertex_matrix(), m.face_matrix()


def sdf_to_bmesh(fn, bounds, h, target_faces=None):
    """Marching cubes of fn's zero level set (optionally decimated); returns a bmesh in Blender space."""
    vol, origin = sample_volume(fn, bounds, h)
    verts, faces, _, _ = marching_cubes(vol, 0.0, spacing=(h, h, h))
    verts = verts + np.array(origin)
    co = to_blender(verts[:, 0], verts[:, 1], verts[:, 2])
    if target_faces:
        co, faces = decimate_arrays(co, faces, target_faces)
    bm = bmesh.new()
    bverts = [bm.verts.new(v) for v in co]
    for f in faces:
        try:
            bm.faces.new((bverts[f[0]], bverts[f[1]], bverts[f[2]]))
        except ValueError:
            pass  # duplicate face
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=h * 0.05)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    return bm


def bmesh_to_object(bm, name):
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    obj = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(obj)
    return obj


def decimate(obj, ratio, symmetric=True):
    mod = obj.modifiers.new("decimate", "DECIMATE")
    mod.decimate_type = "COLLAPSE"
    mod.ratio = ratio
    mod.use_symmetry = symmetric
    mod.symmetry_axis = "X"
    mod.use_collapse_triangulate = True
    depsgraph = bpy.context.evaluated_depsgraph_get()
    eval_obj = obj.evaluated_get(depsgraph)
    me = bpy.data.meshes.new_from_object(eval_obj)
    old = obj.data
    obj.modifiers.clear()
    obj.data = me
    bpy.data.meshes.remove(old)


def face_arrays(bm):
    """Centroids (Blender space) and face list for a bmesh."""
    bm.faces.ensure_lookup_table()
    faces = list(bm.faces)
    cents = np.array([f.calc_center_median() for f in faces]) if faces else np.zeros((0, 3))
    return faces, cents


def face_bounds(faces):
    lo = np.array([[min(v.co[i] for v in f.verts) for i in range(3)] for f in faces]) if faces else np.zeros((0, 3))
    hi = np.array([[max(v.co[i] for v in f.verts) for i in range(3)] for f in faces]) if faces else np.zeros((0, 3))
    return lo, hi


class Cutter:
    """Bisects only the faces near each cut, keeping centroid and normal caches up to date.

    normal_fn maps (N, 3) Blender space points to (N, 3) unit normals (usually the SDF gradient),
    which is far more stable than triangle normals of a marching cubes mesh.
    """

    def __init__(self, bm, normal_fn):
        self.bm = bm
        self.normal_fn = normal_fn
        self.faces, self.cents = face_arrays(bm)
        self.fmin, self.fmax = face_bounds(self.faces)
        self.nrms = normal_fn(self.cents)
        self.alive = np.ones(len(self.faces), bool)
        self.index = {f: i for i, f in enumerate(self.faces)}

    def cut(self, plane_co, plane_no, lo, hi, mask_fn=None):
        m = self.alive & np.all(self.fmax >= lo, axis=1) & np.all(self.fmin <= hi, axis=1)
        idx = np.nonzero(m)[0]
        if len(idx) and mask_fn is not None:
            idx = idx[mask_fn(self.cents[idx], self.nrms[idx])]
        faces = []
        for i in idx:
            f = self.faces[i]
            if f.is_valid:
                faces.append(f)
            else:
                self.alive[i] = False
        if not faces:
            return 0
        edges = {e for f in faces for e in f.edges}
        verts = {v for f in faces for v in f.verts}
        res = bmesh.ops.bisect_plane(self.bm, geom=list(verts) + list(edges) + faces, dist=1e-7,
                                     plane_co=plane_co, plane_no=plane_no)
        touched = {g for g in res["geom"] if isinstance(g, bmesh.types.BMFace) and g.is_valid}
        touched.update(f for f in faces if f.is_valid)
        touched = list(touched)
        if not touched:
            return len(faces)
        cents = np.array([f.calc_center_median() for f in touched])
        fmin, fmax = face_bounds(touched)
        nrms = self.normal_fn(cents)
        new_rows = []
        for k, f in enumerate(touched):
            i = self.index.get(f)
            if i is None:
                self.index[f] = len(self.faces)
                self.faces.append(f)
                new_rows.append(k)
            else:
                self.cents[i] = cents[k]
                self.nrms[i] = nrms[k]
                self.fmin[i] = fmin[k]
                self.fmax[i] = fmax[k]
        if new_rows:
            self.fmin = np.vstack([self.fmin, fmin[new_rows]])
            self.fmax = np.vstack([self.fmax, fmax[new_rows]])
            self.cents = np.vstack([self.cents, cents[new_rows]])
            self.nrms = np.vstack([self.nrms, nrms[new_rows]])
            self.alive = np.concatenate([self.alive, np.ones(len(new_rows), bool)])
        return len(faces)


def segment_planes(view, pts):
    """Yield (plane_co, plane_no, a, b) in Blender space for each polyline segment.

    view: 'side' (pts are (u, z)), 'top' ((u, x)), 'front' ((x, z), extruded along u).
    """
    for (a0, b0), (a1, b1) in zip(pts[:-1], pts[1:]):
        if view == "side":
            co = (0.0, a0 - HALF_WB, b0)
            no = (0.0, -(b1 - b0), a1 - a0)
        elif view == "top":
            co = (b0, a0 - HALF_WB, 0.0)
            no = (a1 - a0, -(b1 - b0), 0.0)
        elif view == "front":
            co = (a0, 0.0, b0)
            no = (-(b1 - b0), 0.0, a1 - a0)
        else:
            raise ValueError(view)
        n = np.array(no, float)
        n /= np.linalg.norm(n)
        yield co, tuple(n), (a0, b0), (a1, b1)


def view_coords(view, u, x, z):
    if view == "side":
        return u, z
    if view == "top":
        return u, x
    if view == "front":
        return x, z
    raise ValueError(view)


def offset_polyline(pts, d):
    """Offset a 2D polyline sideways by d (left normal of travel direction)."""
    pts = np.asarray(pts, float)
    out = []
    for i in range(len(pts)):
        if i == 0:
            t = pts[1] - pts[0]
        elif i == len(pts) - 1:
            t = pts[-1] - pts[-2]
        else:
            t1 = pts[i] - pts[i - 1]
            t2 = pts[i + 1] - pts[i]
            t = t1 / np.linalg.norm(t1) + t2 / np.linalg.norm(t2)
        t = t / np.linalg.norm(t)
        nrm = np.array([-t[1], t[0]])
        out.append(pts[i] + nrm * d)
    return out


def dist_to_polyline(pa, pb, pts):
    """Distance of points (pa, pb arrays) to a 2D polyline, plus the along parameter validity."""
    best = np.full(pa.shape, np.inf)
    for (a0, b0), (a1, b1) in zip(pts[:-1], pts[1:]):
        da, db = a1 - a0, b1 - b0
        L2 = da * da + db * db
        t = np.clip(((pa - a0) * da + (pb - b0) * db) / L2, 0.0, 1.0)
        d = np.hypot(pa - (a0 + t * da), pb - (b0 + t * db))
        best = np.minimum(best, d)
    return best


def in_polygon(pa, pb, poly):
    """Vectorised even odd rule point in polygon test."""
    poly = np.asarray(poly, float)
    inside = np.zeros(pa.shape, bool)
    n = len(poly)
    for i in range(n):
        a0, b0 = poly[i]
        a1, b1 = poly[(i + 1) % n]
        cond = (b0 > pb) != (b1 > pb)
        with np.errstate(divide="ignore", invalid="ignore"):
            cross = (a1 - a0) * (pb - b0) / (b1 - b0) + a0
        inside ^= cond & (pa < cross)
    return inside


def mesh_from_faces(name, verts_co, polys, mat_indices, materials_list):
    """Build a mesh object from numpy vertex coordinates and polygon index lists."""
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(v) for v in verts_co], [], polys)
    for m in materials_list:
        me.materials.append(m)
    if mat_indices is not None and len(polys):
        me.polygons.foreach_set("material_index", np.asarray(mat_indices, np.int32))
    me.update()
    obj = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(obj)
    return obj


def set_custom_normals(obj, loop_normals):
    me = obj.data
    me.normals_split_custom_set([tuple(n) for n in loop_normals])


def sdf_vertex_normals(fn, co):
    """Outward unit normals of the field fn at Blender space points co."""
    u, x, z = to_body(co)
    eps = 1.5e-3
    gu = fn(u + eps, x, z) - fn(u - eps, x, z)
    gx = fn(u, x + eps, z) - fn(u, x - eps, z)
    gz = fn(u, x, z + eps) - fn(u, x, z - eps)
    g = np.stack([gx, gu, gz], axis=-1)  # Blender order X, Y, Z
    return g / np.maximum(np.linalg.norm(g, axis=-1, keepdims=True), 1e-12)


def box_arrays(center, size, bevel=0.0, segments=2):
    """Vertices (Blender space) and polygons of an axis aligned, optionally bevelled box."""
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x = center[0] + v.co.x * size[0]
        v.co.y = center[1] + v.co.y * size[1]
        v.co.z = center[2] + v.co.z * size[2]
    if bevel > 0:
        bmesh.ops.bevel(bm, geom=list(bm.edges), offset=bevel, segments=segments, affect="EDGES", profile=0.5)
    bm.verts.ensure_lookup_table()
    co = np.array([v.co[:] for v in bm.verts])
    polys = [[v.index for v in f.verts] for f in bm.faces]
    bm.free()
    return co, polys


def bowl_arrays(center, axis, radius, depth, rings=8, segments=32):
    """Parabolic reflector bowl opening along `axis` (unit vector), rim centred at `center`."""
    axis = np.asarray(axis, float)
    axis /= np.linalg.norm(axis)
    helper = np.array([0.0, 0.0, 1.0]) if abs(axis[2]) < 0.9 else np.array([1.0, 0.0, 0.0])
    e1 = np.cross(axis, helper)
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(axis, e1)
    co = []
    for i in range(rings + 1):
        r = radius * max(i / rings, 0.12)
        back = depth * (1.0 - (r / radius) ** 2)
        for j in range(segments):
            a = 2 * np.pi * j / segments
            co.append(np.asarray(center) + e1 * r * np.cos(a) + e2 * r * np.sin(a) - axis * back)
    polys = []
    for i in range(rings):
        for j in range(segments):
            a = i * segments + j
            b = i * segments + (j + 1) % segments
            polys.append([a, b, b + segments, a + segments])
    polys.append(list(range(segments))[::-1])
    return np.array(co), polys


def sphere_arrays(center, radius, rings=8, segments=12):
    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=segments, v_segments=rings, radius=radius)
    bm.verts.ensure_lookup_table()
    co = np.array([v.co[:] for v in bm.verts]) + np.asarray(center)
    polys = [[v.index for v in f.verts] for f in bm.faces]
    bm.free()
    return co, polys


def append_geometry(obj, pieces, keep=None):
    """Append (co, polys, material_key[, vertex_normals]) pieces to a mesh object, keeping its custom normals.

    Existing loops keep their custom normals; new faces get flat face normals unless the piece
    brings per vertex normals. keep: optional bool mask over the existing polygons.
    """
    me = obj.data
    old_loop_normals = [tuple(cn.vector) for cn in me.corner_normals]
    co = np.empty(len(me.vertices) * 3)
    me.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)
    if keep is None:
        keep = np.ones(len(me.polygons), bool)
    kept = [p for p, k in zip(me.polygons, keep) if k]
    polys = [list(p.vertices) for p in kept]
    mats = [p.material_index for p in kept]
    old_loop_normals = [old_loop_normals[li] for p in kept for li in p.loop_indices]
    mat_keys = [m.name for m in me.materials]
    n_old_polys = len(polys)
    new_vn = {}  # new vertex index -> smooth normal, for pieces that bring their own
    for piece in pieces:
        pco, ppolys, key = piece[:3]
        vn = piece[3] if len(piece) > 3 else None
        if key not in mat_keys:
            mat_keys.append(key)
        mi = mat_keys.index(key)
        base = len(co)
        co = np.vstack([co, pco])
        polys.extend([[base + int(i) for i in p] for p in ppolys])
        mats.extend([mi] * len(ppolys))
        if vn is not None:
            for i, n in enumerate(vn):
                new_vn[base + i] = tuple(n)
    from blender.lib import materials as MAT
    existing = {m.name: m for m in me.materials if m is not None}
    new_me = bpy.data.meshes.new(me.name)
    new_me.from_pydata([tuple(v) for v in co], [], polys)
    for k in mat_keys:
        new_me.materials.append(existing.get(k) or MAT.get(k))
    new_me.polygons.foreach_set("material_index", np.asarray(mats, np.int32))
    new_me.update()
    loops = []
    li = 0
    for pi, p in enumerate(new_me.polygons):
        for _ in p.loop_indices:
            if pi < n_old_polys:
                loops.append(old_loop_normals[li])
                li += 1
            else:
                loops.append(None)
    vi = 0
    for pi, p in enumerate(new_me.polygons):
        for l in p.loop_indices:
            if loops[l] is None:
                v = new_me.loops[l].vertex_index
                loops[l] = new_vn.get(v, tuple(p.normal))
    obj.data = new_me
    bpy.data.meshes.remove(me)
    set_custom_normals(obj, loops)


def orient_polys(co, polys, ref_normals_fn):
    """Reverse any polygon whose geometric normal opposes the reference field normal at its centre.

    Decimation can fold a few triangles; on glass or double sided materials they render as dark
    shards, so winding must always agree with the smooth custom normals.
    """
    co = np.asarray(co)
    cents = np.array([co[p].mean(axis=0) for p in polys])
    ref = ref_normals_fn(cents)
    out = []
    flipped = 0
    for p, r in zip(polys, ref):
        pts = co[p]
        n = np.zeros(3)
        for i in range(len(p)):  # Newell's method, robust for n-gons
            a, b = pts[i], pts[(i + 1) % len(p)]
            n += np.array([(a[1] - b[1]) * (a[2] + b[2]), (a[2] - b[2]) * (a[0] + b[0]), (a[0] - b[0]) * (a[1] + b[1])])
        if np.dot(n, r) < 0:
            out.append(list(p)[::-1])
            flipped += 1
        else:
            out.append(list(p))
    return out, flipped


def untangle(bm, fn, threshold=0.5, iters=12, log=None):
    """Relax vertices around folded or badly tilted faces and snap them back onto fn's surface.

    Collapse decimation can fold triangles over their neighbours in flat areas, which shows as
    shards through glass. A face is bad when its geometric normal and the field normal at its
    centre disagree (dot below threshold). Its vertices and their neighbours get damped
    Laplacian steps, each followed by Newton projection onto the zero level set.
    """
    def bad_faces():
        bm.normal_update()
        faces = list(bm.faces)
        cents = np.array([f.calc_center_median() for f in faces])
        ref = sdf_vertex_normals(fn, cents)
        geo = np.array([f.normal[:] for f in faces])
        dots = (geo * ref).sum(axis=1)
        return [f for f, d in zip(faces, dots) if d < threshold]

    def project(points):
        for _ in range(3):
            u, x, z = to_body(points)
            d = fn(u, x, z)
            n = sdf_vertex_normals(fn, points)
            points = points - n * d[:, None]
        return points

    first = None
    for it in range(iters):
        bad = bad_faces()
        if first is None:
            first = len(bad)
        if not bad:
            break
        verts = {v for f in bad for v in f.verts}
        ring = {n for v in verts for e in v.link_edges for n in e.verts}
        verts = list(verts | ring)
        co = np.array([v.co[:] for v in verts])
        avg = np.array([np.mean([e.other_vert(v).co[:] for e in v.link_edges], axis=0) for v in verts])
        new = project(0.5 * co + 0.5 * avg)
        for v, c in zip(verts, new):
            v.co = c
    remaining = len(bad_faces())
    if log:
        log(f"untangle: {first} bad faces before, {remaining} after")
    return remaining
