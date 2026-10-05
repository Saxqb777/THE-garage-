"""Give the source model's doors, barn doors and hood a real body (model v2, step 1).

The source car is one outer skin, so a cut out door is a paper thin shell: open it and you
look at the back of the paint. This module measures each panel's outer skin with ray casts
from outside, then builds behind it, as one closed solid:
  * a pressed steel body 3 mm inside the skin (never z fights it) with a 28 mm flange all
    round the edge, so the panel has thickness and a rolled edge,
  * a cavity under the belt line whose inner face is the door card (grey trim) and whose
    rim is painted steel, like the real door seen from inside,
  * a 40 mm box section around the window opening (the frame), black inside,
  * a rubber seal tube running round the outer edge on the inner face.
The side windows are merged into their doors (one part, glass material kept). Everything is
built in world space before the hinge pivots are set, so build_lc100 needs no changes there.

Geometry comes from signed distance fields sampled on a grid and meshed with marching cubes,
then decimated in MeshLab; the outer face of the solid is dropped since the skin hides it.
"""
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree
from scipy import ndimage
from skimage.measure import marching_cubes

import bmesh
import bpy

from blender.lib import meshing as M

GAP = 0.003          # solid sits this far inside the skin
FLANGE = 0.028       # thickness at the panel edge
FRAME_EXTRA = 0.012  # window frame section: FLANGE + this
SEAL_R = 0.007
INSET = 0.006        # the solid stops this far short of the cut edge, so the skin overhangs it
SEAL_INSET = 0.022   # the seal runs this far inside the outer edge, on the inner face
H = 0.008            # marching cubes cell
GRID = 0.01          # ray cast grid

AXES = {0: Vector((1, 0, 0)), 1: Vector((0, 1, 0)), 2: Vector((0, 0, 1))}


class Panel:
    """One panel to thicken. axis: outward axis index, sign: outward direction along it."""

    def __init__(self, key, axis, sign, cavity, card_key, frame_key, glass_keys=(), top_band=None, seal=True, target=9000):
        self.key, self.axis, self.sign, self.cavity = key, axis, sign, cavity
        self.card_key, self.frame_key, self.glass_keys = card_key, frame_key, glass_keys
        self.top_band, self.seal, self.target = top_band, seal, target
        self.ab = [i for i in (0, 1, 2) if i != axis]  # the two grid axes


def panels_for(objs):
    out = []
    for s, sg in (("L", 1.0), ("R", -1.0)):
        out.append(Panel(f"DOOR_6751_front_door_{s}", 0, sg, 0.085, "door_card_grey", "plastic_black_matte",
                         glass_keys=(f"GLASS_6751_front_door_glass_{s}",)))
        out.append(Panel(f"DOOR_6755_rear_door_{s}", 0, sg, 0.085, "door_card_grey", "plastic_black_matte",
                         glass_keys=(f"GLASS_6755_rear_door_glass_{s}", f"GLASS_6755_rear_door_quarter_glass_{s}")))
        # the barn door skin stops under the glass top, so a frame bar is added over the glass
        out.append(Panel(f"DOOR_6761_back_door_{s}", 1, 1.0, 0.06, "door_card_grey", "interior_plastic_grey",
                         glass_keys=(), top_band=f"GLASS_6761_back_door_glass_{s}", target=7000))
    out.append(Panel("BODY_5353_hood", 2, 1.0, 0.045, "paint_white", "paint_white", seal=False, target=6000))
    return [p for p in out if p.key in objs]


# ---------------------------------------------------------------------------
# measuring the skin

def world_polygons(obj):
    me = obj.data
    mw = obj.matrix_world
    co = [mw @ v.co for v in me.vertices]
    return co, [list(p.vertices) for p in me.polygons]


def bounds_of(obj):
    co = np.array([obj.matrix_world @ Vector(c) for c in obj.bound_box])
    return co.min(0), co.max(0)


def heightfield(obj, panel):
    """Outer surface coordinate along the panel axis on a grid over the other two axes.

    Returns (A, B, T, hit): grid coordinate vectors, skin coordinate (signed outward) and the
    hit mask. Rays come from outside, so inner trim never shadows the skin.
    """
    co, polys = world_polygons(obj)
    # only faces that look outward define the skin depth; lips and jamb faces would dent it
    rot = obj.matrix_world.to_3x3()
    polys = [p for p, f in zip(polys, obj.data.polygons) if abs((rot @ f.normal)[panel.axis]) >= 0.6]
    tree = BVHTree.FromPolygons(co, polys)
    lo, hi = bounds_of(obj)
    ia, ib = panel.ab
    A = np.arange(lo[ia] - 2 * GRID, hi[ia] + 2 * GRID, GRID)
    B = np.arange(lo[ib] - 2 * GRID, hi[ib] + 2 * GRID, GRID)
    far = (hi if panel.sign > 0 else lo)[panel.axis] + panel.sign * 0.3
    d = -panel.sign * AXES[panel.axis]
    T = np.full((len(A), len(B)), np.nan)
    org = [0.0, 0.0, 0.0]
    for i, a in enumerate(A):
        for j, b in enumerate(B):
            org[ia], org[ib], org[panel.axis] = a, b, far
            hit = tree.ray_cast(Vector(org), d, 1.5)
            # grazing hits (the skin wrapping round the edge) give a noisy depth: leave them out
            if hit[0] is not None and abs(hit[1].dot(d)) > 0.35:
                T[i, j] = panel.sign * hit[0][panel.axis]
    return A, B, T, ~np.isnan(T)


def skin_depth(obj, panel, A, B):
    """Outer surface depth of obj on an existing grid, same rules as heightfield (outward faces only)."""
    co, polys = world_polygons(obj)
    rot = obj.matrix_world.to_3x3()
    polys = [p for p, f in zip(polys, obj.data.polygons) if abs((rot @ f.normal)[panel.axis]) >= 0.6]
    tree = BVHTree.FromPolygons(co, polys)
    ia, ib = panel.ab
    lo, hi = bounds_of(obj)
    far = (hi if panel.sign > 0 else lo)[panel.axis] + panel.sign * 0.3
    d = -panel.sign * AXES[panel.axis]
    T = np.full((len(A), len(B)), np.nan)
    org = [0.0, 0.0, 0.0]
    for i, a in enumerate(A):
        for j, b in enumerate(B):
            org[ia], org[ib], org[panel.axis] = a, b, far
            hit = tree.ray_cast(Vector(org), d, 3.0)
            if hit[0] is not None and abs(hit[1].dot(d)) > 0.35:
                T[i, j] = panel.sign * hit[0][panel.axis]
    return T


def fill_nearest(T, mask):
    """T with every cell outside mask replaced by the value of the nearest cell inside it."""
    if mask.all():
        return T
    idx = ndimage.distance_transform_edt(~mask, return_distances=False, return_indices=True)
    return T[tuple(idx)]


# ---------------------------------------------------------------------------
# the solid

def silhouette(obj, panel, A, B):
    """Cells covered by the panel's own faces seen along the axis: exact at edges where rays graze."""
    from skimage.draw import polygon
    ia, ib = panel.ab
    co, polys = world_polygons(obj)
    # lips and jamb faces (steep) would fray the outline
    rot = obj.matrix_world.to_3x3()
    polys = [p for p, f in zip(polys, obj.data.polygons) if abs((rot @ f.normal)[panel.axis]) >= 0.3]
    co = np.array([c[:] for c in co])
    mask = np.zeros((len(A), len(B)), bool)
    ra = (co[:, ia] - A[0]) / GRID
    rb = (co[:, ib] - B[0]) / GRID
    for p in polys:
        rr, cc = polygon(ra[p], rb[p], mask.shape)
        mask[rr, cc] = True
    return mask


def footprints(panel, objs, A, B, hit, sil):
    """S: the steel (silhouette plus hits, pinholes closed, barn door top bar), outer: S with the window filled."""
    S = hit | sil
    S = ndimage.binary_closing(S, iterations=2) | S
    S = ndimage.binary_opening(S, iterations=1)  # one cell spikes along the cut lines go
    # pinholes and texture cracks close; the window opening (thousands of cells) stays open
    lab, n = ndimage.label(~S)
    sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
    for k, size in enumerate(sizes, 1):
        if size < 600:
            S |= lab == k
    if panel.top_band and panel.top_band in objs:
        glo, ghi = bounds_of(objs[panel.top_band])
        ia, ib = panel.ab
        band = (A[:, None] >= glo[ia] - 0.02) & (A[:, None] <= ghi[ia] + 0.02) & (B[None, :] >= ghi[ib] - 0.005) & (B[None, :] <= ghi[ib] + 0.04)
        S |= band
    outer = ndimage.binary_fill_holes(S)
    # the hood and the doors' lower skins are solid, so outer == S there; keep the biggest blob only
    lab, n = ndimage.label(outer)
    if n > 1:
        sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
        outer = lab == (1 + int(np.argmax(sizes)))
        S &= outer
    return S, outer


def sdf2d(mask):
    """Signed distance in metres, positive inside the mask."""
    inside = ndimage.distance_transform_edt(mask) * GRID
    outside = ndimage.distance_transform_edt(~mask) * GRID
    return np.where(mask, inside - 0.5 * GRID, -outside + 0.5 * GRID)


def smoothstep(x):
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3 - 2 * x)


def depth_field(panel, S, outer, B, belt):
    """Thickness behind the skin per grid cell."""
    sd = sdf2d(S)
    below = smoothstep((belt - B[None, :]) / 0.03) if belt is not None else np.ones_like(sd)
    extra = below * panel.cavity + (1 - below) * FRAME_EXTRA
    return FLANGE + extra * smoothstep(sd / 0.07), sd


def sample2(F, A, B, a, b):
    """Bilinear lookup of grid F at coordinates a, b (arrays), clamped at the edges."""
    ia = (a - A[0]) / GRID
    ib = (b - B[0]) / GRID
    return ndimage.map_coordinates(F, [ia.ravel(), ib.ravel()], order=1, mode="nearest").reshape(a.shape)


def mesh_field(fn, lo, hi, h):
    """Marching cubes of fn (Blender space, negative inside) over the box lo..hi."""
    xs = np.arange(lo[0], hi[0] + h, h)
    ys = np.arange(lo[1], hi[1] + h, h)
    zs = np.arange(lo[2], hi[2] + h, h)
    X, Y, Z = np.meshgrid(xs, ys, zs, indexing="ij")
    vol = fn(X, Y, Z).astype(np.float32)
    if vol.min() >= 0 or vol.max() <= 0:
        return np.zeros((0, 3)), np.zeros((0, 3), int)
    verts, faces, _, _ = marching_cubes(vol, 0.0, spacing=(h, h, h))
    verts = verts + np.array([xs[0], ys[0], zs[0]])
    # orient outward: closed mesh, so bmesh can do it
    bm = bmesh.new()
    bv = [bm.verts.new(v) for v in verts]
    for f in faces:
        try:
            bm.faces.new((bv[f[0]], bv[f[1]], bv[f[2]]))
        except ValueError:
            pass
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=h * 0.05)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.verts.ensure_lookup_table()
    co = np.array([v.co[:] for v in bm.verts])
    tri = np.array([[v.index for v in f.verts] for f in bm.faces])
    bm.free()
    return co, tri


def gradient_normals(fn, co, eps=2e-3):
    g = np.stack([
        fn(co[:, 0] + eps, co[:, 1], co[:, 2]) - fn(co[:, 0] - eps, co[:, 1], co[:, 2]),
        fn(co[:, 0], co[:, 1] + eps, co[:, 2]) - fn(co[:, 0], co[:, 1] - eps, co[:, 2]),
        fn(co[:, 0], co[:, 1], co[:, 2] + eps) - fn(co[:, 0], co[:, 1], co[:, 2] - eps)], axis=-1)
    return g / np.maximum(np.linalg.norm(g, axis=-1, keepdims=True), 1e-9)


def face_normals(co, tri):
    a, b, c = co[tri[:, 0]], co[tri[:, 1]], co[tri[:, 2]]
    n = np.cross(b - a, c - a)
    return n / np.maximum(np.linalg.norm(n, axis=-1, keepdims=True), 1e-12)


def fix_winding(co, tri, fn):
    """Faces wound against the field gradient get flipped, so culling sees the outside."""
    cent = co[tri].mean(1)
    agree = np.einsum("ij,ij->i", face_normals(co, tri), gradient_normals(fn, cent)) < 0
    tri = tri.copy()
    tri[agree] = tri[agree][:, ::-1]
    return tri


def build_solid(panel, A, B, T, S, outer, belt, obj=None):
    """Returns (pieces, keep): the new geometry and which source faces survive. Source faces that
    lie inside the new solid (groove lips, inner flanges) are dropped: hidden, and they poke through."""
    ia, ib = panel.ab
    ax = panel.axis
    Tf = fill_nearest(T, ~np.isnan(T))
    # the deepest depth nearby: where the source skin edge is jagged (the A pillar corner) the
    # solid retreats behind it instead of following the teeth, and never pokes through the skin
    Tf = ndimage.gaussian_filter(ndimage.grey_erosion(Tf, size=5), 1.0)
    D, sd = depth_field(panel, S, outer, B, belt)

    def pick(X, Y, Z):
        P = (X, Y, Z)
        return P[ia], P[ib], panel.sign * P[ax]

    def solid(X, Y, Z):
        a, b, t = pick(X, Y, Z)
        ts = sample2(Tf, A, B, a, b) - GAP
        d = sample2(D, A, B, a, b)
        s2 = sample2(sd, A, B, a, b)
        slab = np.maximum(t - ts, (ts - d) - t)
        return np.maximum(slab, -(s2 - INSET))

    sd_outer = sdf2d(outer)
    Ts = ndimage.gaussian_filter(Tf, 3.0)  # the seal path ignores small steps in the skin

    def seal(X, Y, Z):
        a, b, t = pick(X, Y, Z)
        # a tube glued to the inner face of the flange, a little inside the edge
        tseal = sample2(Ts, A, B, a, b) - GAP - sample2(D, A, B, a, b) + SEAL_R * 0.5
        s2 = sample2(sd_outer, A, B, a, b) - SEAL_INSET
        return np.sqrt(s2 * s2 + (t - tseal) ** 2) - SEAL_R

    lo = np.zeros(3)
    hi = np.zeros(3)
    inside = np.argwhere(outer)
    a0, a1 = A[inside[:, 0].min()], A[inside[:, 0].max()]
    b0, b1 = B[inside[:, 1].min()], B[inside[:, 1].max()]
    tmin, tmax = np.nanmin(T[outer]), np.nanmax(T[outer])
    lo[ia], hi[ia] = a0 - 3 * H, a1 + 3 * H
    lo[ib], hi[ib] = b0 - 3 * H, b1 + 3 * H
    t_lo, t_hi = tmin - GAP - FLANGE - panel.cavity - 3 * H, tmax + 3 * H
    if panel.sign > 0:
        lo[ax], hi[ax] = t_lo, t_hi
    else:
        lo[ax], hi[ax] = -t_hi, -t_lo

    keep = None
    if obj is not None:
        me = obj.data
        mw = obj.matrix_world
        cent = np.array([(mw @ p.center)[:] for p in me.polygons])
        a, b, t = pick(cent[:, 0], cent[:, 1], cent[:, 2])
        ts = sample2(Tf, A, B, a, b) - GAP
        d = sample2(D, A, B, a, b)
        s2 = sample2(sd, A, B, a, b)
        # only steep faces go (groove lips and inner flanges); the skin itself always stays
        nrm = np.array([(mw.to_3x3() @ p.normal)[:] for p in me.polygons])
        steep = np.abs(nrm[:, ax]) < 0.75
        inside = steep & (t < ts - 0.004) & (t > ts - d - 0.02) & (s2 > -0.01)
        keep = ~inside

    co, tri = mesh_field(solid, lo, hi, H)
    if len(tri) == 0:
        return [], keep
    # the outer face sits behind the skin: drop it (keeps the rim within 2 cm of any edge)
    cent = co[tri].mean(1)
    a, b, _ = pick(cent[:, 0], cent[:, 1], cent[:, 2])
    nrm = face_normals(co, tri)
    outward = nrm[:, ax] * panel.sign
    s2c = sample2(sd, A, B, a, b)
    tri = tri[~((outward > 0.55) & (s2c > 0.02))]
    co, tri = M.decimate_arrays(co, tri, panel.target)
    tri = fix_winding(co, tri, solid)
    vn = gradient_normals(solid, co)
    # materials by where a face looks: cavity face = card, frame inside = frame key, rest paint
    cent = co[tri].mean(1)
    a, b, _ = pick(cent[:, 0], cent[:, 1], cent[:, 2])
    nrm = face_normals(co, tri)
    inward = -nrm[:, ax] * panel.sign
    s2c = sample2(sd, A, B, a, b)
    bb = b
    below = (bb < belt) if belt is not None else np.ones(len(tri), bool)
    is_card = (inward > 0.5) & (s2c > 0.035) & below
    # the window frame is dark all round except the face that looks outward (the skin covers it)
    is_frame = ~below & (inward > -0.5)
    pieces = []
    for mask, key in ((is_card, panel.card_key), (is_frame, panel.frame_key), (~is_card & ~is_frame, "paint_white")):
        if mask.any():
            pieces.append((co, tri[mask], key, vn))
    if panel.seal:
        sco, stri = mesh_field(seal, lo, hi, H * 0.75)
        if len(stri):
            sco, stri = M.decimate_arrays(sco, stri, 2500)
            stri = fix_winding(sco, stri, seal)
            pieces.append((sco, stri, "rubber_seal", gradient_normals(seal, sco)))
    return pieces, keep


def handle_cups(panel):
    """A painted cup behind each outside handle opening, so the hole in the skin shows a recess
    and not the inside of the door."""
    from blender.parts import source_regions as R
    if panel.axis != 0:
        return []
    box = R.HANDLE_FRONT if "front_door" in panel.key else R.HANDLE_REAR if "rear_door" in panel.key else None
    if box is None:
        return []
    x0, x1, y0, y1, z0, z1 = box
    sg = panel.sign
    co, polys = M.box_arrays((sg * 0.95, 0.5 * (y0 + y1), 0.5 * (z0 + z1)), (0.03, (y1 - y0) + 0.03, (z1 - z0) + 0.025), bevel=0.004)
    return [(co, polys, "paint_white")]


def glass_pieces(objs, keys):
    pieces = []
    for k in keys:
        g = objs.get(k)
        if g is None:
            continue
        me = g.data
        mw = g.matrix_world
        co = np.array([(mw @ v.co)[:] for v in me.vertices])
        by_mat = {}
        for p in me.polygons:
            name = me.materials[p.material_index].name if me.materials else "glass_clear"
            by_mat.setdefault(name, []).append(list(p.vertices))
        for name, polys in by_mat.items():
            pieces.append((co, polys, name))
    return pieces


def to_local(obj, pieces):
    """World space pieces into the object's local space (identity before the pivots are set)."""
    inv = obj.matrix_world.inverted()
    if inv == inv.Identity(4):
        return pieces
    rot = np.array(inv.to_3x3())
    m = np.array(inv)
    out = []
    for piece in pieces:
        co = np.asarray(piece[0], float)
        co_l = co @ m[:3, :3].T + m[:3, 3]
        if len(piece) > 3 and piece[3] is not None:
            vn = np.asarray(piece[3], float) @ rot.T
            out.append((co_l, piece[1], piece[2], vn))
        else:
            out.append((co_l, piece[1], piece[2]))
    return out


def belt_of(objs, keys, panel):
    """Bottom of the lowest window, less 3 cm: where the door card ends and the frame starts."""
    ib = panel.ab[1]
    lows = [bounds_of(objs[k])[0][ib] for k in keys if k in objs]
    return min(lows) - 0.03 if lows else None


def thicken(objs, log=print):
    shell = objs.get("BODY_0000_body_shell")
    shell_pieces = []
    shell_keep = np.ones(len(shell.data.polygons), bool) if shell is not None else None
    for panel in panels_for(objs):
        obj = objs[panel.key]
        A, B, T, hit = heightfield(obj, panel)
        S, outer = footprints(panel, objs, A, B, hit, silhouette(obj, panel, A, B))
        belt_keys = panel.glass_keys or ((panel.top_band,) if panel.top_band else ())
        belt = belt_of(objs, belt_keys, panel)
        if shell is not None:
            Tf = ndimage.gaussian_filter(ndimage.grey_erosion(fill_nearest(T, ~np.isnan(T)), size=5), 1.0)
            op, keep_s = opening_pieces(panel, A, B, Tf, outer, shell, log)
            shell_pieces += op
            shell_keep &= keep_s
        pieces, keep = build_solid(panel, A, B, T, S, outer, belt, obj)
        pieces += handle_cups(panel)
        glass = glass_pieces(objs, panel.glass_keys)
        if not pieces:
            log(f"panels: {panel.key}: no solid built")
            continue
        keep = None if keep is None else np.asarray(keep, bool)
        dropped = int((~keep).sum()) if keep is not None else 0
        M.append_geometry(obj, to_local(obj, pieces + glass), keep)
        for k in panel.glass_keys:
            g = objs.pop(k, None)
            if g is not None:
                me = g.data
                bpy.data.objects.remove(g)
                bpy.data.meshes.remove(me)
        n = sum(len(p[1]) for p in pieces)
        log(f"panels: {panel.key}: {int(S.sum() * GRID * GRID * 1e4)} dm2 of skin, {n} faces added, {dropped} lip faces dropped, belt {belt}, glass merged {len(panel.glass_keys)}")
    if shell is not None:
        shell_pieces += arch_liner_pieces()
        M.append_geometry(shell, to_local(shell, shell_pieces), shell_keep)
        log(f"body: {len(shell_pieces)} opening and liner pieces added, {int((~shell_keep).sum())} lip faces dropped")
    return objs

# ---------------------------------------------------------------------------
# the body side: door frames, sills, engine bay tub, wheel arch liners (step 2)

JAMB_DEPTH = {"DOOR": 0.12, "BACK": 0.14, "HOOD": 0.30}
JAMB_GAP = 0.008     # between the door skin edge and the frame wall
JAMB_WALL = 0.022


def opening_pieces(panel, A, B, Tf, outer, shell, log):
    """A frame wall round the opening, going inward from the body skin, plus the engine bay
    floor under the hood. Returns (pieces, keep) for the body shell: its own ragged lips round
    the opening (steep faces) are dropped."""
    ia, ib = panel.ab
    ax = panel.axis
    kind = "HOOD" if panel.key.startswith("BODY_5353") else ("BACK" if "back_door" in panel.key else "DOOR")
    depth = JAMB_DEPTH[kind]
    sd_o = sdf2d(outer)
    mat = "underbody_black" if kind == "HOOD" else "paint_white"
    # the frame starts at the body skin round the opening (roof, pillars, fenders), which curves
    # away from the door skin: following the door depth would poke the frame out of the roof
    Tb = skin_depth(shell, panel, A, B)
    seen = ~np.isnan(Tb)
    Tb = ndimage.gaussian_filter(ndimage.median_filter(fill_nearest(Tb, seen), size=3), 0.7)
    Top = np.minimum(Tb, Tf)
    # no frame where the body skin could not be measured from outside (the roof curving away,
    # the cowl under the windshield): a frame there would stand proud of the body
    sd_seen = sdf2d(ndimage.binary_dilation(seen, iterations=2))

    def pick(X, Y, Z):
        P = (X, Y, Z)
        return P[ia], P[ib], panel.sign * P[ax]

    def wall(X, Y, Z):
        a, b, t = pick(X, Y, Z)
        ts = sample2(Top, A, B, a, b) - GAP
        s2 = sample2(sd_o, A, B, a, b)
        ring = np.abs(s2 + JAMB_GAP + 0.5 * JAMB_WALL) - 0.5 * JAMB_WALL
        f = np.maximum(ring, np.maximum(t - (ts - 0.004), (ts - depth) - t))
        f = np.maximum(f, -sample2(sd_seen, A, B, a, b))
        if kind == "BACK":
            # the two barn doors meet in the middle: no wall there
            f = np.maximum(f, 0.045 - np.abs(X))
        return f

    def floor(X, Y, Z):
        a, b, t = pick(X, Y, Z)
        ts = sample2(Tf, A, B, a, b) - GAP
        s2 = sample2(sd_o, A, B, a, b)
        return np.maximum(0.02 - s2, np.maximum(t - (ts - 0.44), (ts - 0.46) - t))

    inside = np.argwhere(outer)
    lo = np.zeros(3)
    hi = np.zeros(3)
    a0, a1 = A[inside[:, 0].min()], A[inside[:, 0].max()]
    b0, b1 = B[inside[:, 1].min()], B[inside[:, 1].max()]
    tmin, tmax = float(np.nanmin(Tf[outer])), float(np.nanmax(Tf[outer]))
    pad = JAMB_GAP + JAMB_WALL + 3 * H
    lo[ia], hi[ia] = a0 - pad, a1 + pad
    lo[ib], hi[ib] = b0 - pad, b1 + pad
    t_lo, t_hi = tmin - (0.47 if kind == "HOOD" else depth) - 3 * H, tmax + 3 * H
    if panel.sign > 0:
        lo[ax], hi[ax] = t_lo, t_hi
    else:
        lo[ax], hi[ax] = -t_hi, -t_lo
    pieces = []
    for fn, target in ((wall, 7000), (floor, 1500)) if kind == "HOOD" else ((wall, 6000),):
        co, tri = mesh_field(fn, lo, hi, H)
        if len(tri) == 0:
            continue
        co, tri = M.decimate_arrays(co, tri, target)
        tri = fix_winding(co, tri, fn)
        pieces.append((co, tri, mat, gradient_normals(fn, co)))
    # the shell's own lips round the opening
    me = shell.data
    mw = shell.matrix_world
    cent = np.array([(mw @ p.center)[:] for p in me.polygons])
    nrm = np.array([(mw.to_3x3() @ p.normal)[:] for p in me.polygons])
    a, b, t = pick(cent[:, 0], cent[:, 1], cent[:, 2])
    tb = sample2(Tb, A, B, a, b)
    s2 = sample2(sd_o, A, B, a, b)
    seen_here = sample2(sd_seen, A, B, a, b) > 0
    # never above the opening: the roof beside a door top is deeper than the drip rail and would go
    near = (s2 > -0.05) & (s2 < 0.02) & (a > a0 - 0.05) & (a < a1 + 0.05) & (b > b0 - 0.05) & (b < b1 - 0.02)
    steep = np.abs(nrm[:, ax]) < 0.75
    # a lip turns inward from the skin: steep and deeper than the body skin measured here. The
    # pillars and sills are the skin itself (same depth) and stay.
    drop = near & steep & seen_here & (t < tb - 0.012) & (t > tb - 0.10)
    log(f"opening: {panel.key}: {kind} frame {depth} m deep, {int(drop.sum())} shell lip faces dropped")
    return pieces, ~drop


WHEEL_CENTRES = [(0.81, -1.425, 0.385), (-0.81, -1.425, 0.385), (0.81, 1.425, 0.385), (-0.81, 1.425, 0.385)]


def arch_liner_pieces():
    """Black wheel arch liners: a half cylinder round each wheel plus an inner wall, so the arch
    never shows the floor or the cabin behind the tyre."""
    pieces = []
    for cx, cy, cz in WHEEL_CENTRES:
        sg = 1.0 if cx > 0 else -1.0

        def fn(X, Y, Z, cx=cx, cy=cy, cz=cz, sg=sg):
            rho = np.hypot(Y - cy, Z - cz)
            xs = sg * X
            shell = np.maximum(np.abs(rho - 0.50) - 0.010, np.maximum(0.62 - xs, xs - 0.90))
            inner = np.maximum(np.abs(xs - 0.62) - 0.010, rho - 0.51)
            f = np.minimum(shell, inner)
            return np.maximum(f, (cz + 0.03) - Z)

        lo = (min(sg * 0.60, sg * 0.92), cy - 0.54, cz)
        hi = (max(sg * 0.60, sg * 0.92), cy + 0.54, cz + 0.54)
        co, tri = mesh_field(fn, np.array(lo), np.array(hi), H)
        if len(tri) == 0:
            continue
        co, tri = M.decimate_arrays(co, tri, 1200)
        tri = fix_winding(co, tri, fn)
        pieces.append((co, tri, "underbody_black", gradient_normals(fn, co)))
    return pieces
