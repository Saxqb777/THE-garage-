"""Exterior detail parts for The Garage: a 2005 Toyota Land Cruiser 100 (GCC base trim).

Every builder creates its objects in the current scene and returns the main
object. All parts are standalone meshes in a documented local frame so they
can be placed onto the body later. Units are metres, Z up.

Builders
    build_grille()                 BODY_0000_radiator_grille (+ child TRIM_0000_front_emblem)
    build_badges()                 dict of the five rear and quarter badges
    build_mirror(side)             BODY_0000_outer_mirror_L / _R
    build_door_handle(which, side) DOOR_0000_<which>_door_outside_handle_L / _R
    build_side_marker(side)        LIGHT_0000_side_turn_signal_lamp_L / _R
    build_mudguard(position)       BODY_0000_mudguard_<position>
    build_wiper(which, side)       ELEC_0000_<which>_wiper_arm_<side> (+ child blade)

Local frames (see each builder's docstring for the exact extents)
    grille          origin at the centre of the mounting plane, faces -Y
    rear badges     origin at the centre of the back face, face +Y
    quarter badges  origin at the centre of the back face, L faces +X, R faces -X
    mirror          origin at the centre of the sail base on the door skin,
                    housing along +X (L) or -X (R), glass faces +Y
    handles/markers origin at the centre of the mounting face, face +X (L) / -X (R),
                    forward is -Y
    mudguards       origin at the top centre (bolt line), flap in the XZ plane hanging -Z
    wipers          origin at the arm pivot, local +Z is the glass normal, nothing below z=0

Every object carries a custom property ``partKey`` equal to its name. Builders can
be called repeatedly in one session; they clean up every temporary datablock.
Materials come only from blender.lib.materials.
"""
import math
import os
import sys

import numpy as np
import bpy
import bmesh
from mathutils import Vector
from mathutils.geometry import tessellate_polygon

_REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
if _REPO not in sys.path:
    sys.path.insert(0, _REPO)
if "/home/user/THE-garage-" not in sys.path:
    sys.path.insert(0, "/home/user/THE-garage-")
from blender.lib import materials  # noqa: E402

try:
    from skimage import measure as _sk_measure
    from scipy import ndimage as _ndimage
except ImportError:  # pragma: no cover
    _sk_measure = None
    _ndimage = None

_FONT_CANDIDATES = (
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
)

# ---------------------------------------------------------------------------
# small geometry helpers
# ---------------------------------------------------------------------------


def _frame_map(facing):
    """Map build space (u right, v up, w out of the mounting face) to the local frame.

    Each map is a proper rotation (det +1) so text reads correctly from outside and
    normals stay valid. u is the reading direction seen from outside the car.
    """
    if facing == "-Y":
        return lambda u, v, w: (u, -w, v)
    if facing == "+Y":
        return lambda u, v, w: (-u, w, v)
    if facing == "+X":
        return lambda u, v, w: (w, u, v)
    if facing == "-X":
        return lambda u, v, w: (-w, -u, v)
    raise ValueError(facing)


def _apply_map(bm, fn):
    for v in bm.verts:
        v.co = Vector(fn(v.co.x, v.co.y, v.co.z))


def _superellipse(a, b, n, npts):
    """Closed CCW outline of a superellipse, resampled evenly by arc length."""
    t = np.linspace(0.0, 2.0 * math.pi, 1440, endpoint=False)
    c, s = np.cos(t), np.sin(t)
    x = a * np.sign(c) * np.abs(c) ** (2.0 / n)
    y = b * np.sign(s) * np.abs(s) ** (2.0 / n)
    pts = np.column_stack([x, y])
    seg = np.linalg.norm(np.roll(pts, -1, axis=0) - pts, axis=1)
    cum = np.concatenate([[0.0], np.cumsum(seg)])
    total = cum[-1]
    want = np.linspace(0.0, total, npts, endpoint=False)
    xi = np.interp(want, cum, np.append(pts[:, 0], pts[0, 0]))
    yi = np.interp(want, cum, np.append(pts[:, 1], pts[0, 1]))
    return np.column_stack([xi, yi])


def _round_polygon(pts, radii, n_arc, n_edge=1):
    """Round the corners of a convex CCW polygon.

    radii: per corner radius (0 keeps the corner sharp). Every corner contributes
    n_arc + 1 points (a sharp corner repeats its point), every edge is split into
    n_edge segments, so two polygons built with the same counts correspond 1:1.
    """
    pts = [np.asarray(p, dtype=float) for p in pts]
    n = len(pts)
    corner_pts = []
    for i in range(n):
        p = pts[i]
        p0 = pts[i - 1]
        p1 = pts[(i + 1) % n]
        r = radii[i]
        d0 = p0 - p
        d1 = p1 - p
        l0 = np.linalg.norm(d0)
        l1 = np.linalg.norm(d1)
        d0 /= l0
        d1 /= l1
        if r <= 1e-9:
            corner_pts.append([p.copy() for _ in range(n_arc + 1)])
            continue
        cosang = np.clip(np.dot(d0, d1), -1.0, 1.0)
        ang = math.acos(cosang)
        tlen = r / math.tan(ang / 2.0)
        tlen = min(tlen, 0.49 * l0, 0.49 * l1)
        r_eff = tlen * math.tan(ang / 2.0)
        t0 = p + d0 * tlen
        t1 = p + d1 * tlen
        bis = d0 + d1
        bis /= np.linalg.norm(bis)
        centre = p + bis * (r_eff / math.sin(ang / 2.0))
        a0 = math.atan2(t0[1] - centre[1], t0[0] - centre[0])
        a1 = math.atan2(t1[1] - centre[1], t1[0] - centre[0])
        # go the short way round
        da = a1 - a0
        while da > math.pi:
            da -= 2 * math.pi
        while da < -math.pi:
            da += 2 * math.pi
        arc = [centre + r_eff * np.array([math.cos(a0 + da * k / n_arc), math.sin(a0 + da * k / n_arc)])
               for k in range(n_arc + 1)]
        corner_pts.append(arc)
    out = []
    for i in range(n):
        arc = corner_pts[i]
        out.extend(arc)
        nxt = corner_pts[(i + 1) % n][0]
        last = arc[-1]
        for k in range(1, n_edge):
            out.append(last + (nxt - last) * (k / n_edge))
    return np.array(out)


def _loft(bm, sections, close=True, cap_start=None, cap_end=None):
    """Skin consecutive rings of 3D points with quads. Returns the new faces.

    cap_start / cap_end: None, 'ngon' or 'pole'.
    """
    rings = [[bm.verts.new(Vector(p)) for p in sec] for sec in sections]
    faces = []
    n = len(rings[0])
    for ra, rb in zip(rings[:-1], rings[1:]):
        count = n if close else n - 1
        for k in range(count):
            k1 = (k + 1) % n
            try:
                faces.append(bm.faces.new((ra[k], ra[k1], rb[k1], rb[k])))
            except ValueError:
                pass
    for ring, mode, flip in ((rings[0], cap_start, True), (rings[-1], cap_end, False)):
        if mode is None:
            continue
        if mode == "ngon":
            vs = ring[::-1] if flip else ring
            try:
                faces.append(bm.faces.new(vs))
            except ValueError:
                pass
        elif mode == "pole":
            centre = Vector((0.0, 0.0, 0.0))
            for v in ring:
                centre += v.co
            centre /= len(ring)
            cv = bm.verts.new(centre)
            for k in range(n):
                k1 = (k + 1) % n
                tri = (ring[k1], ring[k], cv) if flip else (ring[k], ring[k1], cv)
                try:
                    faces.append(bm.faces.new(tri))
                except ValueError:
                    pass
    return faces


def _rounded_box(bm, centre, size, radius, segments=3, exclude_normal=None, radius2=0.0, segments2=2):
    """Axis aligned box with bevelled edges. Returns the faces of the box.

    exclude_normal: axis letter with sign ('+Y') whose face edges get radius2 instead.
    """
    sub = bmesh.new()
    bmesh.ops.create_cube(sub, size=1.0)
    for v in sub.verts:
        v.co = Vector((v.co.x * size[0], v.co.y * size[1], v.co.z * size[2]))
    excl_axis = None
    if exclude_normal is not None:
        excl_axis = ("XYZ".index(exclude_normal[1]), 1.0 if exclude_normal[0] == "+" else -1.0)
    main_edges = []
    excl_edges = []
    for e in sub.edges:
        if excl_axis is not None:
            ax, sg = excl_axis
            if all(abs(v.co[ax] - sg * size[ax] / 2.0) < 1e-9 for v in e.verts):
                excl_edges.append(e)
                continue
        main_edges.append(e)
    if radius > 0:
        bmesh.ops.bevel(sub, geom=main_edges, offset=radius, offset_type="OFFSET", segments=segments,
                        profile=0.5, affect="EDGES", clamp_overlap=True)
    if excl_axis is not None and radius2 > 0:
        ax, sg = excl_axis
        edges2 = [e for e in sub.edges
                  if all(abs(v.co[ax] - sg * size[ax] / 2.0) < 1e-9 for v in e.verts)]
        bmesh.ops.bevel(sub, geom=edges2, offset=radius2, offset_type="OFFSET", segments=segments2,
                        profile=0.5, affect="EDGES", clamp_overlap=True)
    for v in sub.verts:
        v.co += Vector(centre)
    return _merge(bm, sub)


def _cylinder(bm, centre, radius, height, segments=16, axis="Z", top_round=0.0, radius_top=None):
    sub = bmesh.new()
    rt = radius if radius_top is None else radius_top
    bmesh.ops.create_cone(sub, cap_ends=True, cap_tris=False, segments=segments,
                          radius1=radius, radius2=rt, depth=height)
    if top_round > 0:
        top_edges = [e for e in sub.edges if all(v.co.z > height / 2.0 - 1e-9 for v in e.verts)]
        bmesh.ops.bevel(sub, geom=top_edges, offset=top_round, offset_type="OFFSET", segments=2,
                        profile=0.5, affect="EDGES", clamp_overlap=True)
    for v in sub.verts:
        v.co.z += height / 2.0
        if axis == "X":
            v.co = Vector((v.co.z, v.co.y, -v.co.x))
        elif axis == "Y":
            v.co = Vector((v.co.x, v.co.z, -v.co.y))
        v.co += Vector(centre)
    return _merge(bm, sub)


def _merge(dst, src, mat_index=0, fn=None):
    """Copy a bmesh into another and free the source.

    mat_index: material index for the copied faces, None keeps the source indices.
    fn: optional (x, y, z) -> (x, y, z) coordinate map applied while copying.
    """
    vmap = {}
    for v in src.verts:
        co = v.co if fn is None else Vector(fn(v.co.x, v.co.y, v.co.z))
        vmap[v] = dst.verts.new(co)
    faces = []
    for f in src.faces:
        try:
            nf = dst.faces.new([vmap[v] for v in f.verts])
        except ValueError:
            continue
        nf.material_index = f.material_index if mat_index is None else mat_index
        faces.append(nf)
    src.free()
    return faces


def _set_material(faces, index):
    for f in faces:
        f.material_index = index


def _signed_area(pts):
    x = pts[:, 0]
    y = pts[:, 1]
    return 0.5 * float(np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y))


def _loop_normals(pts, inward):
    """Per vertex miter normals pointing into the solid plus the miter length scale."""
    prev = np.roll(pts, 1, axis=0)
    nxt = np.roll(pts, -1, axis=0)
    e0 = pts - prev
    e1 = nxt - pts
    l0 = np.linalg.norm(e0, axis=1)
    l1 = np.linalg.norm(e1, axis=1)
    l0[l0 < 1e-12] = 1e-12
    l1[l1 < 1e-12] = 1e-12
    e0 /= l0[:, None]
    e1 /= l1[:, None]
    n0 = np.column_stack([-e0[:, 1], e0[:, 0]])
    n1 = np.column_stack([-e1[:, 1], e1[:, 0]])
    m = n0 + n1
    ml = np.linalg.norm(m, axis=1)
    ml[ml < 1e-9] = 1e-9
    m /= ml[:, None]
    cosh = np.clip(np.sum(m * n0, axis=1), 0.35, 1.0)
    if not inward:
        m = -m
    return m, 1.0 / cosh


def _extrude_loops(bm, groups, h_wall, profile, dome=None, edt=None, base=0.0, mat_index=0,
                   bottom_cap=True):
    """Extrude 2D regions (outer loop + holes) along +Z with a rounded top edge.

    groups: list of [outer, hole, ...] arrays of shape (N, 2).
    profile: list of (inset, z) rings above the vertical wall, last one is the cap.
    dome: optional f(x, y) added to the top (weighted by height) for a domed face.
    edt: optional (x0, y0, dx, dy, array) distance field used to keep insets safe.
    Returns the created faces.
    """
    if edt is not None:
        ex0, ey0, edx, edy, earr = edt

        def edt_at(p):
            i = int(min(max((p[1] - ey0) / edy, 0), earr.shape[0] - 1))
            j = int(min(max((p[0] - ex0) / edx, 0), earr.shape[1] - 1))
            return earr[i, j]
    else:
        def edt_at(p):
            return 1e9

    faces = []
    for loops in groups:
        rings_per_loop = []
        for li, pts in enumerate(loops):
            ccw = _signed_area(pts) > 0
            inward = ccw if li == 0 else (not ccw)
            nrm, sc = _loop_normals(pts, inward)
            levels = [[bm.verts.new((p[0], p[1], base)) for p in pts],
                      [bm.verts.new((p[0], p[1], base + h_wall)) for p in pts]]
            for inset, z in profile:
                vs = []
                for k, p in enumerate(pts):
                    d = inset * sc[k]
                    q = p + nrm[k] * d
                    tries = 0
                    while tries < 6 and edt_at(q) < 0.7 * d:
                        d *= 0.6
                        q = p + nrm[k] * d
                        tries += 1
                    vs.append(bm.verts.new((q[0], q[1], base + z)))
                levels.append(vs)
            rings_per_loop.append(levels)
            n = len(pts)
            for ra, rb in zip(levels[:-1], levels[1:]):
                for k in range(n):
                    k1 = (k + 1) % n
                    try:
                        faces.append(bm.faces.new((ra[k], ra[k1], rb[k1], rb[k])))
                    except ValueError:
                        pass
        caps = [(-1, True)]
        if bottom_cap:
            caps.append((0, False))
        for level_index, _top in caps:
            polys = [[Vector((v.co.x, v.co.y)) for v in rl[level_index]] for rl in rings_per_loop]
            flat = []
            for rl in rings_per_loop:
                flat.extend(rl[level_index])
            try:
                tris = tessellate_polygon(polys)
            except Exception:
                tris = []
            for t in tris:
                try:
                    faces.append(bm.faces.new((flat[t[0]], flat[t[1]], flat[t[2]])))
                except ValueError:
                    pass
        if dome is not None:
            ztop = max(v.co.z for rl in rings_per_loop for v in rl[-1]) - base
            if ztop > 1e-9:
                for rl in rings_per_loop:
                    for lvl in rl:
                        for v in lvl:
                            w = (v.co.z - base) / ztop
                            v.co.z += dome(v.co.x, v.co.y) * w
    for f in faces:
        f.material_index = mat_index
    return faces


# ---------------------------------------------------------------------------
# outlines: Toyota emblem and text
# ---------------------------------------------------------------------------


def _emblem_loops(width, height, px=1100):
    """Outline loops of the Toyota emblem (three overlapping elliptical rings).

    Built from a smooth field so the union comes out as one outer loop plus holes.
    Returns (loops, edt_info) with loops sorted by area (outer first), in metres.
    """
    a = width / 2.0
    b = height / 2.0
    ba = b / a
    tO, tV, tH = 0.090, 0.080, 0.080
    aV = 0.245
    bV = ba - tO + 0.30 * tO
    aH = 0.55
    bH = 0.37 * ba
    yH = bV - bH
    margin = 0.05
    nx = px
    ny = int(px * (ba + margin) / (1 + margin))
    xs = np.linspace(-(1 + margin), (1 + margin), nx)
    ys = np.linspace(-(ba + margin), (ba + margin), ny)
    X, Y = np.meshgrid(xs, ys)

    def ell(cx, cy, ea, eb):
        return np.sqrt(((X - cx) / ea) ** 2 + ((Y - cy) / eb) ** 2) - 1.0

    def ring(cx, cy, ea, eb, t):
        return np.maximum(ell(cx, cy, ea, eb), -ell(cx, cy, ea - t, eb - t))

    f = np.minimum.reduce([ring(0, 0, 1.0, ba, tO), ring(0, 0, aV, bV, tV), ring(0, yH, aH, bH, tH)])
    dx = xs[1] - xs[0]
    dy = ys[1] - ys[0]
    loops = []
    if _sk_measure is not None:
        for c in _sk_measure.find_contours(f, 0.0):
            c = _sk_measure.approximate_polygon(c, tolerance=0.5)
            pts = np.column_stack([xs[0] + c[:, 1] * dx, ys[0] + c[:, 0] * dy]) * a
            if np.allclose(pts[0], pts[-1]):
                pts = pts[:-1]
            if len(pts) >= 3:
                loops.append(pts)
        edt = _ndimage.distance_transform_edt(f < 0) * dx * a
        info = (xs[0] * a, ys[0] * a, dx * a, dy * a, edt)
    else:  # pragma: no cover
        # fallback without scikit image: plain rings without a union
        th = np.linspace(0, 2 * math.pi, 96, endpoint=False)
        for (cx, cy, ea, eb, t) in ((0, 0, 1.0, ba, tO),):
            loops.append(np.column_stack([cx + ea * np.cos(th), cy + eb * np.sin(th)]) * a)
            loops.append(np.column_stack([cx + (ea - t) * np.cos(th), cy + (eb - t) * np.sin(th)]) * a)
        info = None
    loops.sort(key=lambda l: -abs(_signed_area(l)))
    return loops, info


def _load_font():
    """Load a private copy of the badge font; the caller removes it after use so no
    datablock is left behind and no font shared with other text objects is touched."""
    for path in _FONT_CANDIDATES:
        if os.path.exists(path):
            return bpy.data.fonts.load(path, check_existing=False)
    return None


def _text_groups(body, cap_height, stretch=1.0, shear=0.0, spacing=1.0, resolution=3, tol=0.00004):
    """Glyph outlines of `body` as groups [outer, holes...] in metres, centred on the
    text bounding box, scaled so the glyph box height equals cap_height.

    Uses a temporary Blender text curve and removes it afterwards.
    """
    cu = bpy.data.curves.new("_tmp_details_text", "FONT")
    cu.body = body
    cu.size = 1.0
    cu.resolution_u = resolution
    cu.fill_mode = "FRONT"
    cu.extrude = 0.0
    cu.bevel_depth = 0.0
    cu.shear = shear
    cu.space_character = spacing
    font = _load_font()
    if font is not None:
        cu.font = font
    ob = bpy.data.objects.new("_tmp_details_text", cu)
    bpy.context.scene.collection.objects.link(ob)
    dg = bpy.context.evaluated_depsgraph_get()
    me = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-7)
    bm.edges.ensure_lookup_table()
    bedges = [e for e in bm.edges if len(e.link_faces) == 1]
    adj = {}
    for e in bedges:
        for v in e.verts:
            adj.setdefault(v, []).append(e)
    used = set()
    loops = []
    for e in bedges:
        if e in used:
            continue
        loop = []
        v = e.verts[0]
        start = v
        cur = e
        while True:
            used.add(cur)
            loop.append((v.co.x, v.co.y))
            v = cur.other_vert(v)
            if v == start:
                break
            nxt = None
            for e2 in adj.get(v, ()):
                if e2 not in used:
                    nxt = e2
                    break
            if nxt is None:
                break
            cur = nxt
        if len(loop) >= 3:
            loops.append(np.array(loop))
    bm.free()
    bpy.data.objects.remove(ob)
    bpy.data.meshes.remove(me)
    bpy.data.curves.remove(cu)
    if font is not None:
        bpy.data.fonts.remove(font)
    if not loops:
        return []
    allpts = np.vstack(loops)
    zmin, zmax = allpts[:, 1].min(), allpts[:, 1].max()
    scale = cap_height / max(zmax - zmin, 1e-9)
    loops = [l * scale * np.array([stretch, 1.0]) for l in loops]
    simp = []
    for l in loops:
        if _sk_measure is not None:
            c = _sk_measure.approximate_polygon(np.vstack([l, l[:1]]), tolerance=tol)
            c = c[:-1] if np.allclose(c[0], c[-1]) else c
        else:
            c = l
        if len(c) >= 3:
            simp.append(c)
    loops = simp
    allpts = np.vstack(loops)
    centre = (allpts.min(axis=0) + allpts.max(axis=0)) / 2.0
    loops = [l - centre for l in loops]

    def inside(pt, poly):
        x, y = pt
        px, py = poly[:, 0], poly[:, 1]
        qx, qy = np.roll(px, -1), np.roll(py, -1)
        cond = (py > y) != (qy > y)
        with np.errstate(divide="ignore", invalid="ignore"):
            xint = px + (y - py) * (qx - px) / (qy - py)
        return int(np.count_nonzero(cond & (x < xint))) % 2 == 1

    n = len(loops)
    parents = [[j for j in range(n) if j != i and inside(loops[i][0], loops[j])] for i in range(n)]
    groups = []
    for i in range(n):
        if len(parents[i]) % 2 == 0:
            holes = [j for j in range(n)
                     if len(parents[j]) == len(parents[i]) + 1 and i in parents[j]]
            groups.append([loops[i]] + [loops[j] for j in holes])
    return groups


def _text_extent(groups):
    allpts = np.vstack([l for g in groups for l in g])
    return allpts.min(axis=0), allpts.max(axis=0)


# ---------------------------------------------------------------------------
# object creation
# ---------------------------------------------------------------------------


def _make_object(name, bm, material_keys, sharp_deg=38.0, recalc=True, merge_dist=2e-6, parent=None,
                 location=(0.0, 0.0, 0.0)):
    """Turn a bmesh into a scene object with the given material slots and partKey."""
    if merge_dist > 0:
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=merge_dist)
    bmesh.ops.dissolve_degenerate(bm, dist=1e-7, edges=bm.edges)
    if recalc:
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.normal_update()
    sharp = math.radians(sharp_deg)
    for f in bm.faces:
        f.smooth = True
    for e in bm.edges:
        if len(e.link_faces) == 2:
            e.smooth = e.calc_face_angle(0.0) < sharp
        else:
            e.smooth = True
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for key in material_keys:
        me.materials.append(materials.get(key))
    me.update()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    ob["partKey"] = name
    if parent is not None:
        ob.parent = parent
        ob.matrix_parent_inverse.identity()
    ob.location = location
    return ob


def _mirror_x(ob):
    """Mirror the mesh of `ob` through the YZ plane and fix normals."""
    me = ob.data
    bm = bmesh.new()
    bm.from_mesh(me)
    for v in bm.verts:
        v.co.x = -v.co.x
    bmesh.ops.reverse_faces(bm, faces=bm.faces)
    bm.normal_update()
    bm.to_mesh(me)
    bm.free()
    me.update()


def _tri_count(ob):
    return sum(len(p.vertices) - 2 for p in ob.data.polygons)


# ---------------------------------------------------------------------------
# emblem
# ---------------------------------------------------------------------------


def _emblem_bm(width, height, facing):
    """Chrome Toyota emblem built in (u, v, w) then mapped to `facing`."""
    loops, info = _emblem_loops(width, height)
    s = width / 0.15
    a, b = width / 2.0, height / 2.0
    bm = bmesh.new()
    _extrude_loops(bm, [loops], h_wall=0.0016 * s,
                   profile=[(0.0006 * s, 0.0026 * s), (0.0015 * s, 0.0033 * s)],
                   dome=lambda x, y: 0.0028 * s * max(0.0, 1.0 - ((x / a) ** 2 + (y / b) ** 2)),
                   edt=info)
    _apply_map(bm, _frame_map(facing))
    return bm


def _build_emblem(name, width, height, facing, parent=None, location=(0, 0, 0)):
    bm = _emblem_bm(width, height, facing)
    return _make_object(name, bm, ["chrome"], sharp_deg=50.0, parent=parent, location=location)


# ---------------------------------------------------------------------------
# 1. radiator grille
# ---------------------------------------------------------------------------

GRILLE_WIDTH = 0.86
GRILLE_HEIGHT = 0.25
GRILLE_BOW = 0.015


def build_grille():
    """BODY_0000_radiator_grille with child TRIM_0000_front_emblem.

    Local frame: origin at the centre of the mounting plane (y = 0), the grille faces
    -Y, Z up. The whole part lives at y <= 0: the back of the surround touches y = 0
    at the ends and bows forward to y = -0.015 at the centre (plan view curvature).
    Extents: x +-0.43, z +-0.125, front face at y = -0.035 (ends) to -0.050 (centre).
    The emblem child sits at (0, -0.0464, +0.012) facing -Y, its back sunk 0.6 mm into a
    black oval pad that bridges the bars.
    Materials: 0 plastic_trim_grey (surround), 1 plastic_black_gloss (bars, emblem pad),
    2 plastic_black_matte (backing panel and vertical stays).
    """
    W_TOP, W_BOT, H = GRILLE_WIDTH, 0.82, GRILLE_HEIGHT
    front = 0.035
    lip_top, lip_side, lip_bot = 0.036, 0.022, 0.024
    n_arc, n_edge = 5, 9

    def trapezoid(wt, wb, zt, zb, rt, rb):
        pts = [(-wb / 2, zb), (wb / 2, zb), (wt / 2, zt), (-wt / 2, zt)]
        return _round_polygon(pts, [rb, rb, rt, rt], n_arc, n_edge)

    outer = trapezoid(W_TOP, W_BOT, H / 2, -H / 2, 0.028, 0.048)
    inner = trapezoid(W_TOP - 2 * lip_side, W_BOT - 2 * lip_side, H / 2 - lip_top, -H / 2 + lip_bot, 0.018, 0.034)

    bm = bmesh.new()

    # surround: closed ring solid, the section rings interpolate from inner to outer
    def ring(t, y):
        return [(inner[k][0] * (1 - t) + outer[k][0] * t, y, inner[k][1] * (1 - t) + outer[k][1] * t)
                for k in range(len(inner))]

    sections = [ring(0.0, 0.0), ring(0.0, -front), ring(0.55, -front)]
    for i in range(1, 5):
        th = math.radians(90.0 * i / 4)
        sections.append(ring(0.55 + 0.45 * math.sin(th), -front + front * (1 - math.cos(th))))
    sections.append(ring(0.0, 0.0))  # back ring closes the tube
    frame_faces = _loft(bm, sections, close=True)
    _set_material(frame_faces, 0)

    # horizontal bars
    z_top_open = H / 2 - lip_top
    z_bot_open = -H / 2 + lip_bot
    n_bars = 5
    bar_h = 0.024
    margin = 0.009
    gap = (z_top_open - z_bot_open - 2 * margin - n_bars * bar_h) / (n_bars - 1)
    bar_front, bar_back = -0.0285, -0.008

    def inner_half_width(z):
        # half width of the inner opening at height z, from the polygon
        best = 0.0
        xs = inner[:, 0]
        zs = inner[:, 1]
        n = len(inner)
        for k in range(n):
            z0, z1 = zs[k], zs[(k + 1) % n]
            if (z0 - z) * (z1 - z) <= 0 and abs(z1 - z0) > 1e-9:
                x = xs[k] + (xs[(k + 1) % n] - xs[k]) * (z - z0) / (z1 - z0)
                best = max(best, abs(x))
        return best

    prof = _round_polygon([(bar_back, -bar_h / 2), (bar_back, bar_h / 2), (bar_front, bar_h / 2), (bar_front, -bar_h / 2)],
                          [0.0, 0.0, 0.0075, 0.0075], 3, 1)
    n_st = 15
    for i in range(n_bars):
        zc = z_top_open - margin - bar_h / 2 - i * (bar_h + gap)
        hw = min(inner_half_width(zc + bar_h / 2), inner_half_width(zc - bar_h / 2)) + 0.010
        xs = np.linspace(-hw, hw, n_st)
        secs = [[(x, p[0], zc + p[1]) for p in prof] for x in xs]
        faces = _loft(bm, secs, close=True, cap_start="ngon", cap_end="ngon")
        _set_material(faces, 1)

    # backing slab behind the bars
    sub = bmesh.new()
    hw_top = inner_half_width(z_top_open - 0.002)
    hw_bot = inner_half_width(z_bot_open + 0.002)
    hw = max(hw_top, hw_bot) + 0.004
    bmesh.ops.create_grid(sub, x_segments=16, y_segments=4, size=0.5)
    gx = [v.co.x for v in sub.verts]
    gy = [v.co.y for v in sub.verts]
    gx0, gx1, gy0, gy1 = min(gx), max(gx), min(gy), max(gy)
    for v in sub.verts:
        fx = (v.co.x - gx0) / (gx1 - gx0)
        fy = (v.co.y - gy0) / (gy1 - gy0)
        v.co = Vector(((fx - 0.5) * 2 * hw, -0.0035, z_bot_open + 0.001 + fy * (z_top_open - z_bot_open - 0.002)))
    res = bmesh.ops.extrude_face_region(sub, geom=sub.faces[:])
    new_verts = [g for g in res["geom"] if isinstance(g, bmesh.types.BMVert)]
    bmesh.ops.translate(sub, verts=new_verts, vec=(0, 0.002, 0))
    _set_material(_merge(bm, sub), 2)

    # vertical stays behind the bars
    for x in (-0.31, -0.135, 0.135, 0.31):
        zc = (z_top_open + z_bot_open) / 2
        hz = (z_top_open - z_bot_open) / 2 - 0.004
        f = _rounded_box(bm, (x, -0.0105, zc), (0.007, 0.011, 2 * hz), 0.0)
        _set_material(f, 2)

    # emblem pad
    pad_a, pad_b = 0.088, 0.062
    z_e = 0.012
    pad = _superellipse(pad_a, pad_b, 2.0, 40)
    pad_secs = [[(p[0], -0.026, z_e + p[1]) for p in pad], [(p[0], -0.032, z_e + p[1]) for p in pad]]
    pf = _loft(bm, pad_secs, close=True, cap_start="ngon", cap_end="ngon")
    _set_material(pf, 1)

    # plan view bow: centre 15 mm further forward than the ends
    half = W_TOP / 2
    for v in bm.verts:
        v.co.y -= GRILLE_BOW * max(0.0, 1.0 - (v.co.x / half) ** 2)

    grille = _make_object("BODY_0000_radiator_grille", bm, ["plastic_trim_grey", "plastic_black_gloss", "plastic_black_matte"],
                          sharp_deg=40.0)
    _build_emblem("TRIM_0000_front_emblem", 0.15, 0.10, "-Y", parent=grille,
                  location=(0.0, -0.032 - GRILLE_BOW + 0.0006, z_e))
    return grille


# ---------------------------------------------------------------------------
# 2. badges
# ---------------------------------------------------------------------------


def _text_bm(body, cap_height, width_target=None, stretch=1.0, shear=0.0, spacing=1.0,
             thickness=0.0025, chamfer=0.0004, facing="+Y", offset=(0.0, 0.0), base=0.0, bm=None,
             mat_index=0, spacing_tol=0.00004):
    """Raised chrome lettering as a bmesh in the given facing frame."""
    groups = _text_groups(body, cap_height, stretch=stretch, shear=shear, spacing=spacing, tol=spacing_tol)
    if width_target is not None and groups:
        mn, mx = _text_extent(groups)
        w = mx[0] - mn[0]
        if w > 1e-9:
            f = width_target / w
            groups = [[l * np.array([f, 1.0]) for l in g] for g in groups]
    groups = [[l + np.array(offset) for l in g] for g in groups]
    own = bm is None
    if own:
        bm = bmesh.new()
    _extrude_loops(bm, groups, h_wall=thickness - chamfer, profile=[(chamfer, thickness)], base=base,
                   mat_index=mat_index)
    if own:
        _apply_map(bm, _frame_map(facing))
    return bm


def build_badges():
    """Return a dict of the rear and quarter badges keyed by object name.

    TRIM_0000_back_door_name_plate  black plate 0.50 x 0.065 x 0.012 with raised chrome
                                    "LAND CRUISER"; origin at the centre of its back face,
                                    faces +Y. Materials: 0 plastic_black_gloss, 1 chrome.
    TRIM_0000_back_door_emblem      chrome Toyota emblem 0.13 x 0.085, back face centre, +Y.
    TRIM_0000_grade_badge           chrome "G" 0.035 tall, back face centre, faces +Y.
    TRIM_0000_quarter_badge_L / _R  chrome "4500 EFI" 0.18 x 0.03, back face centre,
                                    L faces +X, R faces -X, text reads left to right from outside.
    """
    out = {}

    # name plate
    bm = bmesh.new()
    PW, PH, PT = 0.50, 0.065, 0.012
    plate = _round_polygon([(-PW / 2, -PH / 2), (PW / 2, -PH / 2), (PW / 2, PH / 2), (-PW / 2, PH / 2)],
                           [0.018] * 4, 6, 6)
    _extrude_loops(bm, [[plate]], h_wall=PT - 0.005, profile=[(0.0025, PT - 0.0015), (0.005, PT)], mat_index=0)
    _text_bm("LAND CRUISER", 0.030, width_target=0.405, stretch=1.3, spacing=1.08, thickness=0.0028,
             chamfer=0.0005, offset=(-0.012, 0.0), base=PT - 0.0004, bm=bm, mat_index=1)
    _apply_map(bm, _frame_map("+Y"))
    name = "TRIM_0000_back_door_name_plate"
    out[name] = _make_object(name, bm, ["plastic_black_gloss", "chrome"], sharp_deg=45.0)

    # rear emblem
    name = "TRIM_0000_back_door_emblem"
    out[name] = _build_emblem(name, 0.13, 0.085, "+Y")

    # grade badge G
    name = "TRIM_0000_grade_badge"
    bm = _text_bm("G", 0.035, stretch=1.3, thickness=0.003, chamfer=0.0006, facing="+Y")
    out[name] = _make_object(name, bm, ["chrome"], sharp_deg=50.0)

    # quarter badges
    for side, facing in (("L", "+X"), ("R", "-X")):
        name = f"TRIM_0000_quarter_badge_{side}"
        bm = _text_bm("4500 EFI", 0.028, width_target=0.18, shear=0.22, spacing=1.0, thickness=0.0025,
                      chamfer=0.0005, facing=facing)
        out[name] = _make_object(name, bm, ["chrome"], sharp_deg=50.0)
    return out


# ---------------------------------------------------------------------------
# 3. outer mirror
# ---------------------------------------------------------------------------


def build_mirror(side="L"):
    """BODY_0000_outer_mirror_L / _R, the base trim black mirror.

    Local frame (L): origin at the centre of the triangular sail base where it meets
    the door skin (x = 0 plane), housing out along +X, glass faces +Y, Z up.
    Sail plate: triangle y -0.07..0.09 (bottom edge at z = -0.057), apex at z = +0.114,
    12 mm thick. Housing: x 0.040..0.150, y -0.105..0.145, z -0.045..0.135; glass face
    recessed in the +Y face at y = 0.139. R is a true mirror (housing along -X).
    Materials: 0 plastic_black_gloss (housing, arm), 1 chrome (mirror glass),
    2 plastic_black_matte (sail base).
    """
    assert side in ("L", "R")
    bm = bmesh.new()

    # housing: soft box, rear face edges only lightly rounded, glass recessed
    sub = bmesh.new()
    size = (0.11, 0.25, 0.18)
    centre = (0.095, 0.02, 0.045)
    _rounded_box(sub, (0, 0, 0), size, 0.034, segments=7, exclude_normal="+Y", radius2=0.006, segments2=2)

    def rear_face():
        sub.normal_update()
        return max((f for f in sub.faces if f.normal.y > 0.99), key=lambda f: f.calc_area())

    bmesh.ops.inset_region(sub, faces=[rear_face()], thickness=0.0085, depth=0.0, use_even_offset=True)
    bmesh.ops.inset_region(sub, faces=[rear_face()], thickness=0.0015, depth=0.0, use_even_offset=True)
    glass = rear_face()
    bmesh.ops.translate(sub, verts=list(glass.verts), vec=(0, -0.0065, 0))
    for f in sub.faces:
        f.material_index = 0
    glass.material_index = 1
    for v in sub.verts:
        v.co += Vector(centre)
    _merge(bm, sub, None)

    # arm / neck between sail and housing
    _set_material(_rounded_box(bm, (0.027, 0.005, -0.028), (0.062, 0.09, 0.040), 0.013, segments=4), 0)

    # triangular sail base, built in (u = y, v = z, w = x)
    tri = _round_polygon([(-0.07, -0.057), (0.09, -0.057), (-0.02, 0.114)], [0.012, 0.012, 0.012], 5, 4)
    sail = bmesh.new()
    _extrude_loops(sail, [[tri]], h_wall=0.008, profile=[(0.0025, 0.011), (0.0045, 0.012)], mat_index=2)
    _set_material(_merge(bm, sail, fn=_frame_map("+X")), 2)

    name = f"BODY_0000_outer_mirror_{side}"
    ob = _make_object(name, bm, ["plastic_black_gloss", "chrome", "plastic_black_matte"], sharp_deg=40.0)
    if side == "R":
        _mirror_x(ob)
    return ob


# ---------------------------------------------------------------------------
# 4. door handles
# ---------------------------------------------------------------------------


def build_door_handle(which="front", side="L"):
    """DOOR_0000_<which>_door_outside_handle_<side>: chrome pull handle in a black cup.

    Local frame: origin at the centre of the cup's mounting face on the door skin,
    faces +X (L) or -X (R), Z up, forward is -Y. Cup outline 0.27 x 0.064 with a 1.2 mm
    rim; the recess goes 16 mm into the door (x < 0, hidden shell to x = -0.020).
    Chrome handle 0.24 long, 0.033 tall,
    outer face 24 mm proud of the skin; front handles carry a key cylinder at the rear end.
    Materials: 0 chrome, 1 plastic_black_matte (cup and lock face).
    """
    assert which in ("front", "rear") and side in ("L", "R")
    bm = bmesh.new()
    fm = _frame_map("+X")
    A, B = 0.135, 0.032
    n = 56
    cup = _superellipse(A, B, 2.6, n)
    flange = _superellipse(A + 0.004, B + 0.004, 2.6, n)
    floor = _superellipse(A - 0.014, B - 0.013, 2.6, n)
    depth = 0.016
    secs = [
        [fm(p[0], p[1], -depth - 0.004) for p in flange],   # hidden back of the dish
        [fm(p[0], p[1], 0.0) for p in flange],
        [fm(p[0], p[1], 0.0012) for p in flange],
        [fm(p[0], p[1], 0.0012) for p in cup],
        [fm(p[0], p[1], -depth) for p in floor],
    ]
    faces = _loft(bm, secs, close=True, cap_start="ngon", cap_end="ngon")
    _set_material(faces, 1)

    # grip: lofted pill along u with a floating middle and ends dipping into the cup
    u0, u1 = -0.118, 0.085
    n_st = 26
    secs = []
    for i in range(n_st):
        t = i / (n_st - 1)
        e = 0.11
        r = 1.0
        if t < e:
            r = math.sqrt(max(0.0, 1 - ((e - t) / e) ** 2))
        elif t > 1 - e:
            r = math.sqrt(max(0.0, 1 - ((t - (1 - e)) / e) ** 2))
        r = max(r, 0.03)
        bump = math.sin(math.pi * t) ** 0.45
        wc = -0.004 + 0.016 * bump
        bv = 0.0165 * r
        bw = 0.0110 * r
        u = u0 + (u1 - u0) * t
        ring = []
        for k in range(20):
            th = 2 * math.pi * k / 20
            ring.append(fm(u, bv * math.cos(th), wc + bw * math.sin(th)))
        secs.append(ring)
    faces = _loft(bm, secs, close=True, cap_start="pole", cap_end="pole")
    _set_material(faces, 0)

    # rear escutcheon block
    blk = bmesh.new()
    _rounded_box(blk, (0.0, 0.0, 0.0), (0.046, 0.030, 0.020), 0.006, segments=3)
    _set_material(_merge(bm, blk, fn=lambda u, v, w: fm(u + 0.097, v, w - 0.002)), 0)

    if which == "front":
        cyl = bmesh.new()
        bmesh.ops.create_cone(cyl, cap_ends=True, cap_tris=False, segments=20, radius1=0.0082, radius2=0.0074, depth=0.004)
        for v in cyl.verts:
            v.co.z += 0.002 + 0.008
        faces = _merge(bm, cyl, fn=lambda u, v, w: fm(u + 0.097, v, w))
        for f in faces:
            # dark lock face on the outer disc, chrome bezel around it
            f.material_index = 1 if abs(f.calc_center_median().x - 0.012) < 1e-4 else 0

    name = f"DOOR_0000_{which}_door_outside_handle_{side}"
    ob = _make_object(name, bm, ["chrome", "plastic_black_matte"], sharp_deg=42.0)
    if side == "R":
        _mirror_x(ob)
    return ob


# ---------------------------------------------------------------------------
# 5. side turn signal lamp
# ---------------------------------------------------------------------------


def build_side_marker(side="L"):
    """LIGHT_0000_side_turn_signal_lamp_<side>: amber side repeater 0.069 x 0.032.

    Local frame: origin at the centre of the mounting face on the wing, faces +X (L)
    or -X (R), Z up, forward -Y. Housing 4 mm thick, domed lens to 11.5 mm proud.
    Materials: 0 lamp_housing, 1 lamp_lens_amber, 2 chrome (reflector under the lens).
    """
    assert side in ("L", "R")
    bm = bmesh.new()
    fm = _frame_map("+X")
    n = 44
    house = _superellipse(0.0345, 0.016, 3.4, n)
    lens = _superellipse(0.0315, 0.0132, 3.4, n)
    hd = 0.004
    secs = [[fm(p[0], p[1], 0.0) for p in house], [fm(p[0], p[1], hd) for p in house], [fm(p[0], p[1], hd) for p in lens]]
    faces = _loft(bm, secs, close=True, cap_start="ngon", cap_end="ngon")
    for f in faces:
        f.material_index = 0
    # reflector disc (the end cap of the last ring) in chrome
    last_cap = max(faces, key=lambda f: len(f.verts) if abs(f.calc_center_median().x - hd) < 1e-6 else 0)
    last_cap.material_index = 2

    lb = bmesh.new()
    _extrude_loops(lb, [[lens]], h_wall=0.0040, profile=[(0.0008, 0.0056), (0.0020, 0.0066)],
                   dome=lambda x, y: 0.0015 * max(0.0, 1 - ((x / 0.0315) ** 2 + (y / 0.0132) ** 2)),
                   base=hd + 0.0005, mat_index=1)
    _set_material(_merge(bm, lb, fn=fm), 1)

    name = f"LIGHT_0000_side_turn_signal_lamp_{side}"
    ob = _make_object(name, bm, ["lamp_housing", "lamp_lens_amber", "chrome"], sharp_deg=45.0)
    if side == "R":
        _mirror_x(ob)
    return ob


# ---------------------------------------------------------------------------
# 6. mudguards
# ---------------------------------------------------------------------------


def build_mudguard(position="front_L"):
    """BODY_0000_mudguard_<position>: black rubber flap behind a wheel.

    Local frame: origin at the top centre of the flap (bolt line), the flap lies in the
    XZ plane and hangs down along -Z; its faces point along Y. The wheel side is -Y, the
    rear (visible, ribbed) face is +Y: back face at y = 0, body 6 mm thick, rim and ribs
    raised to 8.5 mm. Front flaps 0.26 wide x 0.33 tall, rear 0.30 x 0.38; the outboard
    bottom corner hangs 10 mm lower. A slight plan bow pulls the edges 12 mm rearward
    and the bottom flares 18 mm rearward. R flaps are true mirrors of L flaps.
    Materials: 0 rubber_seal (flap), 1 plastic_black_matte (bolt heads).
    """
    assert position in ("front_L", "front_R", "rear_L", "rear_R")
    front = position.startswith("front")
    side = position[-1]
    W, H = (0.26, 0.33) if front else (0.30, 0.38)
    T = 0.006
    raise_h = 0.0025
    r_corner = 0.035
    rim = 0.016
    n_ribs = 3 if front else 4
    rib_w = 0.014
    bow, flare = 0.012, 0.018
    half = W / 2
    taper = 0.94  # bottom width over top width

    rib_centres = [(-0.5 + (i + 0.5) / n_ribs) * (W - 2 * rim - 0.02) for i in range(n_ribs)]
    rib_u = [(c / half, rib_w / 2 / half) for c in rib_centres]

    # column positions (normalised u in -1..1) including rib and rim walls
    us = set(np.linspace(-1, 1, 9).tolist())
    eps_u = 0.0012 / half
    rim_u = rim / half
    us.update([-1 + rim_u, -1 + rim_u + eps_u, 1 - rim_u - eps_u, 1 - rim_u])
    for uc, hw in rib_u:
        us.update([uc - hw - eps_u, uc - hw, uc + hw, uc + hw + eps_u])
    us = np.array(sorted(u for u in us if -1 <= u <= 1))

    # row positions (v in 0..1 from top to bottom) including feature walls
    vs = set(np.linspace(0, 1, 9).tolist())
    eps_v = 0.0012 / H
    top_strip = 0.03 / H
    rib_top, rib_bot = 0.055 / H, 1 - 0.05 / H
    rim_v = rim / H
    vs.update([top_strip, top_strip + eps_v, rib_top - eps_v, rib_top, rib_bot, rib_bot + eps_v,
               1 - rim_v - eps_v, 1 - rim_v])
    for k in range(1, 5):
        vs.add(1 - (r_corner / H) * (1 - math.cos(math.pi / 2 * k / 5)))
    vs = np.array(sorted(v for v in vs if 0 <= v <= 1))

    def height_at(u):
        # outboard (u = +1) bottom corner 10 mm lower
        return H + 0.010 * (u + 1) / 2

    def half_width(v, h):
        w = half * (1 - (1 - taper) * v)
        d = (1 - v) * h
        if d < r_corner:
            w -= r_corner - math.sqrt(max(0.0, r_corner ** 2 - (r_corner - d) ** 2))
        return w

    def raised(u, v):
        if v <= top_strip + 1e-9 or abs(u) >= 1 - rim_u - 1e-9 or v >= 1 - rim_v - 1e-9:
            return raise_h
        if rib_top - 1e-9 <= v <= rib_bot + 1e-9:
            for uc, hw in rib_u:
                if abs(u - uc) <= hw + 1e-9:
                    return raise_h
        return 0.0

    nu, nv = len(us), len(vs)
    back = [[None] * nu for _ in range(nv)]
    frontv = [[None] * nu for _ in range(nv)]
    bm = bmesh.new()
    for j, v in enumerate(vs):
        for i, u in enumerate(us):
            h = height_at(u)
            w = half_width(v, h)
            x = u * w
            z = -v * h
            y_curve = bow * (x / half) ** 2 + flare * v ** 2
            back[j][i] = bm.verts.new((x, y_curve, z))
            frontv[j][i] = bm.verts.new((x, y_curve + T + raised(u, v), z))
    faces = []
    for j in range(nv - 1):
        for i in range(nu - 1):
            faces.append(bm.faces.new((back[j][i], back[j][i + 1], back[j + 1][i + 1], back[j + 1][i])))
            faces.append(bm.faces.new((frontv[j][i], frontv[j + 1][i], frontv[j + 1][i + 1], frontv[j][i + 1])))
    # side walls
    for j in range(nv - 1):
        faces.append(bm.faces.new((back[j][0], back[j + 1][0], frontv[j + 1][0], frontv[j][0])))
        faces.append(bm.faces.new((back[j][nu - 1], frontv[j][nu - 1], frontv[j + 1][nu - 1], back[j + 1][nu - 1])))
    for i in range(nu - 1):
        faces.append(bm.faces.new((back[0][i], frontv[0][i], frontv[0][i + 1], back[0][i + 1])))
        faces.append(bm.faces.new((back[nv - 1][i], back[nv - 1][i + 1], frontv[nv - 1][i + 1], frontv[nv - 1][i])))
    _set_material(faces, 0)
    # bolt heads along the top strip
    for xb in (-0.62 * half, 0.0, 0.62 * half):
        yb = bow * (xb / half) ** 2 + T + raise_h
        f = _cylinder(bm, (xb, yb, -0.015), 0.0065, 0.003, segments=12, axis="Y", top_round=0.001)
        _set_material(f, 1)

    name = f"BODY_0000_mudguard_{position}"
    ob = _make_object(name, bm, ["rubber_seal", "plastic_black_matte"], sharp_deg=40.0)
    if side == "R":
        _mirror_x(ob)
    return ob


# ---------------------------------------------------------------------------
# 7. wipers
# ---------------------------------------------------------------------------


def _rect_section(x, yc, zc, w, t, ch):
    """Rectangle with chamfered corners in the YZ plane at station x."""
    pts = _round_polygon([(yc - w / 2, zc - t / 2), (yc + w / 2, zc - t / 2), (yc + w / 2, zc + t / 2), (yc - w / 2, zc + t / 2)],
                         [ch] * 4, 1, 1)
    return [(x, p[0], p[1]) for p in pts]


def _wiper_arm_bm(length, scale):
    """Arm along +X from the pivot at the origin, glass plane z = 0."""
    bm = bmesh.new()
    s = scale
    # pivot cap and shaft
    _cylinder(bm, (0, 0, 0.0), 0.0075 * s, 0.013 * s, segments=14)
    _cylinder(bm, (0, 0, 0.012 * s), 0.0125 * s, 0.028 * s, segments=20, top_round=0.004 * s)
    # head + main arm as one loft; (x, width, thickness, z centre)
    head_len = 0.10 * s
    stations = [
        (-0.012 * s, 0.026 * s, 0.012 * s, 0.031 * s),
        (0.055 * s, 0.024 * s, 0.012 * s, 0.031 * s),
        (head_len, 0.016 * s, 0.010 * s, 0.030 * s),
        (head_len + 0.02 * s, 0.012 * s, 0.009 * s, 0.028 * s),
    ]
    rest = length - (head_len + 0.02 * s)
    for k in range(1, 6):
        t = k / 5
        x = head_len + 0.02 * s + rest * t
        stations.append((x, (0.012 - 0.004 * t) * s, (0.009 - 0.003 * t) * s, (0.028 - 0.009 * t) * s))
    secs = [_rect_section(x, 0, zc, w, th, min(w, th) * 0.22) for (x, w, th, zc) in stations]
    _loft(bm, secs, close=True, cap_start="ngon", cap_end="ngon")
    # hook / adapter dropping to the blade
    zc_end = stations[-1][3]
    _rounded_box(bm, (length + 0.004 * s, 0, (zc_end + 0.011 * s) / 2), (0.028 * s, 0.011 * s, zc_end - 0.011 * s + 0.004 * s), 0.002 * s, segments=2)
    return bm


def _wiper_blade_bm(length, scale):
    """Blade centred on the origin along X, rubber lip on z = 0."""
    bm = bmesh.new()
    s = scale
    L = length
    # centre clip
    f = _rounded_box(bm, (0, 0, 0.016 * s), (0.026 * s, 0.013 * s, 0.014 * s), 0.002 * s, segments=2)
    _set_material(f, 0)
    # primary yoke
    f = _rounded_box(bm, (0, 0, 0.0145 * s), (0.52 * L, 0.011 * s, 0.006 * s), 0.0015 * s, segments=2)
    _set_material(f, 0)
    # secondary yokes
    for sx in (-1, 1):
        f = _rounded_box(bm, (sx * 0.26 * L, 0, 0.0095 * s), (0.36 * L, 0.009 * s, 0.005 * s), 0.0012 * s, segments=2)
        _set_material(f, 0)
        for cx in (0.44, 0.09):
            f = _rounded_box(bm, (sx * cx * L, 0, 0.0065 * s), (0.016 * s, 0.010 * s, 0.006 * s), 0.0, segments=1)
            _set_material(f, 0)
    # rubber element with a flat spine
    f = _rounded_box(bm, (0, 0, 0.0035 * s), (L, 0.0045 * s, 0.007 * s), 0.0, segments=1)
    _set_material(f, 1)
    f = _rounded_box(bm, (0, 0, 0.0065 * s), (0.98 * L, 0.008 * s, 0.002 * s), 0.0, segments=1)
    _set_material(f, 1)
    return bm


def build_wiper(which="front", side="L"):
    """ELEC_0000_<which>_wiper_arm_<side> with child ELEC_0000_<which>_wiper_blade_<side>.

    Local frame: origin at the arm pivot on the glass plane, local +Z is the glass normal
    (pointing away from the glass) and everything sits at z >= 0. Front arms are 0.55 m
    and extend along -X (parked towards the vehicle's right); blades 0.60 (L) / 0.50 (R).
    Rear arms are 0.32 m with 0.30 m blades, the rear L extends along +X, the rear R along
    -X (true mirror). The blade is a child parented with an identity parent inverse, its
    origin at the blade centre on the glass plane, directly under the arm tip:
    blade.location = (+-arm_length, 0, 0). The arm rides 20 to 37 mm above the glass.
    Materials: arm plastic_black_matte; blade 0 plastic_black_matte, 1 rubber_seal.
    """
    assert which in ("front", "rear") and side in ("L", "R")
    if which == "front":
        arm_len = 0.55
        blade_len = 0.60 if side == "L" else 0.50
        direction = -1.0
        scale = 1.0
    else:
        arm_len = 0.32
        blade_len = 0.30
        direction = 1.0 if side == "L" else -1.0
        scale = 0.85
    arm_bm = _wiper_arm_bm(arm_len, scale)
    blade_bm = _wiper_blade_bm(blade_len, scale)
    if direction < 0:
        for b in (arm_bm, blade_bm):
            for v in b.verts:
                v.co.x = -v.co.x
            bmesh.ops.reverse_faces(b, faces=b.faces)
    arm_name = f"ELEC_0000_{which}_wiper_arm_{side}"
    blade_name = f"ELEC_0000_{which}_wiper_blade_{side}"
    arm = _make_object(arm_name, arm_bm, ["plastic_black_matte"], sharp_deg=40.0)
    _make_object(blade_name, blade_bm, ["plastic_black_matte", "rubber_seal"], sharp_deg=40.0,
                 parent=arm, location=(direction * arm_len, 0.0, 0.0))
    return arm


# ---------------------------------------------------------------------------
# convenience
# ---------------------------------------------------------------------------


def build_all():
    """Build every part once (at the origin) and return {name: object}."""
    out = {}
    g = build_grille()
    out[g.name] = g
    for c in g.children:
        out[c.name] = c
    out.update(build_badges())
    for side in ("L", "R"):
        m = build_mirror(side)
        out[m.name] = m
        for which in ("front", "rear"):
            h = build_door_handle(which, side)
            out[h.name] = h
            w = build_wiper(which, side)
            out[w.name] = w
            for c in w.children:
                out[c.name] = c
        s = build_side_marker(side)
        out[s.name] = s
    for pos in ("front_L", "front_R", "rear_L", "rear_R"):
        m = build_mudguard(pos)
        out[m.name] = m
    return out


if __name__ == "__main__":
    bpy.ops.wm.read_factory_settings(use_empty=True)
    parts = build_all()
    for n, o in parts.items():
        print(f"{n:45s} tris {_tri_count(o):6d}  partKey={o['partKey']}")
