"""Wheel assembly for The Garage: the Toyota LC100 2003 to 2007 six spoke 16x8 alloy plus
the 275/70R16 highway tire from blender/parts/wheel.py.

Public entry point (same interface and output names as blender/parts/wheel.py):

    build_wheel_assembly(position)  returns the assembly Empty (bpy.types.Object)

position is one of 'front_L', 'front_R', 'rear_L', 'rear_R'. The call creates, in the
current scene, an Empty named WHEEL_0000_wheel_assembly_<position> at the wheel centre
(no rotation, unit scale) with two mesh children whose origins sit at the wheel centre:

    WHEEL_0000_disc_wheel_<position>   alloy wheel, centre cap, six lug nuts
    WHEEL_0000_tire_<position>         tire with geometric tread

Local frame of every object: the spin axis is local X. The outer face of a left wheel
points +X, the outer face of a right wheel points negative X (right wheels are true
mirrors of the left ones). Front and rear wheels are identical.

Design, read from the reference photos
Six wide spokes with a soft central crease. Next to every spoke, on its counter
clockwise side when seen from outside the left wheel, a narrow through slot runs from
the hub boss almost to the rim; a thin rib separates that slot from the big rounded
window. So the twelve openings alternate: big window, narrow slot. A large flat hub
boss carries six conical lug nuts in shallow pockets and a domed centre cap with a small
Toyota emblem. Moderate dish, satin silver, a thin bright lip.

Geometry approach
The cast face (hub boss, spokes, ribs, windows, slots, lug pockets) is a signed
distance field sampled on a voxel grid and extracted with marching cubes, then
decimated, projected back onto the field and shaded with the field gradient. The
openings are built as exact rounded convex polygons (inset polygon plus radius), which
gives clean fillets at every corner. Tire, lip and barrel, lug nuts and the emblem reuse
the helpers of blender/parts/wheel.py unchanged.

The heavy work runs once per session and is cached as numpy arrays, so the four wheels
build quickly and no temporary datablocks survive the call.
"""
import math
import os
import sys

import bpy
import numpy as np

_REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _REPO not in sys.path:
    sys.path.insert(0, _REPO)

from blender.lib import conventions, materials  # noqa: E402
from blender.parts import wheel as _w  # noqa: E402

POSITIONS = _w.POSITIONS

# =================================================================================
# Dimensions (metres, left wheel frame: +X points out of the car)
# =================================================================================
RIM_SEAT_R = _w.RIM_SEAT_R
FLANGE_R = _w.FLANGE_R
LIP_X = _w.LIP_X
R_LIP_IN = _w.R_LIP_IN                          # 0.194 inner wall of the outer lip
R_PLATE = _w.R_PLATE                            # 0.200 cast face outer radius (buried in lip)

R_HUB = 0.093                                   # flat hub boss radius
X_HUB_FACE = 0.082                              # hub boss face
X_HUB_BACK = 0.048
X_FACE_HUB = 0.0755                             # spoke face height where it meets the hub
X_FACE_RIM = 0.1005                             # spoke face height at the lip
FACE_POWER = 1.25                               # dish curve exponent
T_SPOKE = 0.024                                 # plate thickness

# angular layout of one 60 degree sector, counter clockwise from the spoke axis.
# All offsets are perpendicular distances from the spoke axis, linear in the axial
# position s, so every edge is a straight line in the wheel plane.
S_HUB = R_HUB                                   # where the linear widths are anchored
S_RIM = R_LIP_IN
W_SPOKE_HUB = 0.0275                            # spoke half width at S_HUB
W_SPOKE_RIM = 0.0335                            # spoke half width at S_RIM
T_SLOT_HUB = 0.0105                             # slot width
T_SLOT_RIM = 0.0125
T_RIB_HUB = 0.0150                              # rib between slot and window
T_RIB_RIM = 0.0175

RHO_WIN_IN = 0.0985                             # window inner arc
RHO_WIN_OUT = 0.1865                            # window outer arc
R_WIN_FILLET = 0.0120                           # window corner radius
RHO_SLOT_IN = 0.1035
RHO_SLOT_OUT = 0.1795

H_EDGE = 0.0045                                 # how far the face drops at an opening edge
W_EDGE = 0.016                                  # width of that rounding
K_ROOF = 0.045                                  # spoke crease: slope away from the spoke axis
R_PCD = 0.1397 / 2.0
R_POCKET = 0.0160
POCKET_DEPTH = 0.0045
SEAT_R = 0.0128
SEAT_HALF_ANGLE = math.radians(30.0)
R_BORE = 0.040
SPOKE_PHASE = math.radians(90.0)                # spoke 0 points to +Z
LUG_PHASE = math.radians(90.0)                  # a nut sits on spoke 0

MC_VOXEL = 0.00125
MC_FACE_TRIS = 16500
LATHE_SEGMENTS = 96
NUT_SEGMENTS = 24

_CACHE = {}

_smin = _w._smin
_smax = _w._smax
_smoothstep = _w._smoothstep
_sd_polygon = _w._sd_polygon
_revolve = _w._revolve
_tube_along_curve = _w._tube_along_curve
_flip_if_inverted = _w._flip_if_inverted


# =================================================================================
# Opening outlines: convex polygons clipped by half planes, rounded by an inset radius
# =================================================================================
def _clip_half_plane(poly, nx, ny, c):
    """Keep the part of polygon (list of (x, y)) where nx*x + ny*y >= c (Sutherland Hodgman)."""
    out = []
    n = len(poly)
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]
        dp = nx * p[0] + ny * p[1] - c
        dq = nx * q[0] + ny * q[1] - c
        if dp >= 0.0:
            out.append(p)
        if (dp >= 0.0) != (dq >= 0.0):
            t = dp / (dp - dq)
            out.append((p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t))
    return out


def _annulus_sector(r_in, r_out, a0, a1, n=48):
    """Polygon of the annulus sector between angles a0 and a1 (radians, from +v towards +u)."""
    pts = []
    for t in np.linspace(a0, a1, n):
        pts.append((r_out * math.sin(t), r_out * math.cos(t)))
    for t in np.linspace(a1, a0, max(8, n // 3)):
        pts.append((r_in * math.sin(t), r_in * math.cos(t)))
    return pts


def _offset_line(w0, w1, sign, inward):
    """Half plane for the line u = sign * (a + b s) in the (u, v) frame.

    (u, v): u perpendicular to the spoke axis (counter clockwise positive), v along it.
    `inward` is +1 when the kept side is towards larger u, else -1. Returns (nx, ny, c)
    for nx*u + ny*v >= c, with the normal normalised so c can be shifted by a distance.
    """
    b = (w1 - w0) / (S_RIM - S_HUB)
    a = w0 - b * S_HUB
    # line: u - sign*(a + b v) = 0  ->  normal (1, -sign*b)
    nx, ny = 1.0, -sign * b
    ln = math.hypot(nx, ny)
    nx, ny, c = nx / ln, ny / ln, sign * a / ln
    if inward < 0:
        nx, ny, c = -nx, -ny, -c
    return nx, ny, c


def _window_polygon(inset):
    """Window between spoke 0 (rib side) and spoke 1 (its clockwise edge), inset by `inset`."""
    sector = math.pi / 3.0
    poly = _annulus_sector(RHO_WIN_IN + inset, RHO_WIN_OUT - inset, 0.0, sector)
    # rib outer edge: u >= w_spoke + t_slot + t_rib  (kept side towards larger u)
    nx, ny, c = _offset_line(W_SPOKE_HUB + T_SLOT_HUB + T_RIB_HUB,
                             W_SPOKE_RIM + T_SLOT_RIM + T_RIB_RIM, +1.0, +1)
    poly = _clip_half_plane(poly, nx, ny, c + inset)
    # clockwise edge of spoke 1: in spoke 1's frame u' <= -w_spoke. Rotate that line back.
    nx1, ny1, c1 = _offset_line(W_SPOKE_HUB, W_SPOKE_RIM, -1.0, -1)
    # a point (u, v) in spoke 0 frame has spoke 1 coordinates (u cos - v sin, u sin + v cos)
    # with angle -sector (spoke 1 axis is rotated by +sector)
    ca, sa = math.cos(-sector), math.sin(-sector)
    nx, ny = nx1 * ca - ny1 * sa, nx1 * sa + ny1 * ca
    poly = _clip_half_plane(poly, nx, ny, c1 + inset)
    return np.array(poly)


def _slot_polygon(inset):
    sector = math.pi / 3.0
    poly = _annulus_sector(RHO_SLOT_IN + inset, RHO_SLOT_OUT - inset, 0.0, sector * 0.6, n=36)
    nx, ny, c = _offset_line(W_SPOKE_HUB, W_SPOKE_RIM, +1.0, +1)
    poly = _clip_half_plane(poly, nx, ny, c + inset)
    nx, ny, c = _offset_line(W_SPOKE_HUB + T_SLOT_HUB, W_SPOKE_RIM + T_SLOT_RIM, +1.0, -1)
    poly = _clip_half_plane(poly, nx, ny, c + inset)
    return np.array(poly)


def _slot_fillet():
    return 0.46 * min(T_SLOT_HUB, T_SLOT_RIM)


# =================================================================================
# 2D fields on the wheel plane
# =================================================================================
def _face_fields_2d(y, z):
    """Returns a dict of 2D fields: rho, d_open (signed distance to the nearest opening,
    negative inside an opening), u_abs (perpendicular distance from the nearest spoke axis),
    s_axis (position along that axis)."""
    rho = np.hypot(y, z)
    phi = np.arctan2(z, y)
    sector = math.pi / 3.0
    k = np.floor((phi - SPOKE_PHASE) / sector)
    loc = phi - (SPOKE_PHASE + k * sector)          # 0 .. 60 degrees from spoke k axis
    win = _window_polygon(R_WIN_FILLET)
    slot = _slot_polygon(_slot_fillet())
    rs = _slot_fillet()
    d_open = np.full(rho.shape, np.inf)
    for shift in (-1, 0, 1):
        a = loc - shift * sector
        u = rho * np.sin(a)
        v = rho * np.cos(a)
        d_open = np.minimum(d_open, _sd_polygon(u, v, win) - R_WIN_FILLET)
        d_open = np.minimum(d_open, _sd_polygon(u, v, slot) - rs)
    kn = np.round((phi - SPOKE_PHASE) / sector)
    locn = phi - (SPOKE_PHASE + kn * sector)
    u_abs = np.abs(rho * np.sin(locn))
    s_axis = rho * np.cos(locn)
    return {"rho": rho, "d_open": d_open, "u_abs": u_abs, "s_axis": s_axis}


def _x_face(rho):
    s = np.clip((rho - R_HUB) / (R_LIP_IN - R_HUB), 0.0, 1.0)
    return X_FACE_HUB + (X_FACE_RIM - X_FACE_HUB) * s ** FACE_POWER


def _spoke_half_width(s):
    b = (W_SPOKE_RIM - W_SPOKE_HUB) / (S_RIM - S_HUB)
    return W_SPOKE_HUB + b * (s - S_HUB)


def _front_back(F):
    rho = F["rho"]
    xf = _x_face(rho)
    edge = H_EDGE * (1.0 - _smoothstep(0.0, W_EDGE, F["d_open"]))
    roof = K_ROOF * np.minimum(F["u_abs"], _spoke_half_width(F["s_axis"]))
    # the crease fades out on the hub boss and under the lip
    fade = _smoothstep(R_HUB - 0.01, R_HUB + 0.012, rho)
    x_front = xf - edge - roof * fade
    x_back = xf - T_SPOKE
    return x_front, x_back


def _lug_centres():
    return [(R_PCD * math.cos(LUG_PHASE + i * math.pi / 3.0),
             R_PCD * math.sin(LUG_PHASE + i * math.pi / 3.0)) for i in range(6)]


def _sdf_from_fields(x, F, x_front, x_back, lug_rn):
    rho, d_open = F["rho"], F["d_open"]
    plate = _smax(-d_open, x - x_front, 0.004)
    plate = _smax(plate, x_back - x, 0.002)
    plate = np.maximum(plate, rho - R_PLATE)
    hub = _smax(rho - R_HUB, x - X_HUB_FACE, 0.0025)
    hub = np.maximum(hub, X_HUB_BACK - x)
    hub = np.maximum(hub, R_BORE - rho)
    floor_x = X_HUB_FACE - POCKET_DEPTH
    apex_x = floor_x - SEAT_R / math.tan(SEAT_HALF_ANGLE)
    ca, sa = math.cos(SEAT_HALF_ANGLE), math.sin(SEAT_HALF_ANGLE)
    for rn in lug_rn:
        pocket = np.maximum(rn - R_POCKET, floor_x - x)
        hub = _smax(hub, -pocket, 0.0015)
        cone = rn * ca - (x - apex_x) * sa
        hub = np.maximum(hub, -cone)
    return _smin(plate, hub, 0.0035)


def _face_sdf(x, y, z):
    """Signed distance like field of the cast wheel face at scattered points."""
    F = _face_fields_2d(y, z)
    x_front, x_back = _front_back(F)
    lug_rn = [np.hypot(y - cy, z - cz) for (cy, cz) in _lug_centres()]
    return _sdf_from_fields(x, F, x_front, x_back, lug_rn)


def _face_normals(p):
    h = 0.0003
    n = np.empty_like(p)
    for k in range(3):
        dp = np.zeros(3)
        dp[k] = h
        q1 = p + dp
        q2 = p - dp
        n[:, k] = _face_sdf(q1[:, 0], q1[:, 1], q1[:, 2]) - _face_sdf(q2[:, 0], q2[:, 1], q2[:, 2])
    n /= np.linalg.norm(n, axis=1, keepdims=True)
    return n


def _marching_cubes_face():
    from skimage import measure

    half = R_PLATE + 0.0035
    vx = MC_VOXEL
    ys = np.arange(-half, half + vx * 0.5, vx)
    xs = np.arange(X_HUB_BACK - 0.006, 0.108, vx)
    Y = ys[:, None]
    Z = ys[None, :]
    F = _face_fields_2d(Y, Z)
    x_front, x_back = _front_back(F)
    lug_rn = [np.hypot(Y - cy, Z - cz) for (cy, cz) in _lug_centres()]
    vol = np.empty((len(xs), len(ys), len(ys)), dtype=np.float32)
    for i, x in enumerate(xs):
        vol[i] = _sdf_from_fields(x, F, x_front, x_back, lug_rn)
    verts, faces, _, _ = measure.marching_cubes(vol, level=0.0, spacing=(vx, vx, vx))
    verts = verts.astype(np.float64)
    verts[:, 0] += xs[0]
    verts[:, 1] += ys[0]
    verts[:, 2] += ys[0]
    return verts, faces.astype(np.int64)


def _cast_face_arrays():
    verts, tris = _marching_cubes_face()
    verts, faces = _w._decimate_tris(verts, tris, MC_FACE_TRIS)
    used = np.zeros(len(verts), dtype=bool)
    for f in faces:
        for i in f:
            used[i] = True
    remap = np.cumsum(used) - 1
    verts = verts[used]
    faces = [tuple(int(remap[i]) for i in f) for f in faces]
    for _ in range(2):
        d = _face_sdf(verts[:, 0], verts[:, 1], verts[:, 2])
        nrm = _face_normals(verts)
        verts = verts - d[:, None] * nrm
    nrm = _face_normals(verts)
    faces = _flip_if_inverted(verts, faces)
    return verts, faces, nrm


# =================================================================================
# Revolve parts: lug nuts, centre cap, emblem (lip and barrel come from wheel.py)
# =================================================================================
_CAP_PROFILE = [
    (-0.0050, 0.0000),
    (-0.0050, 0.0400),
    (0.0000, 0.0405),
    (0.0000, 0.0470),       # outer flat ring
    (0.0030, 0.0472),
    (0.0040, 0.0455),
    (0.0040, 0.0400),       # groove between ring and dome
    (0.0025, 0.0380),
    (0.0025, 0.0360),
    (0.0050, 0.0355),
    (0.0085, 0.0320),
    (0.0118, 0.0250),
    (0.0140, 0.0160),
    (0.0150, 0.0080),
    (0.0153, 0.0000),
]


def _nut_arrays(cy, cz):
    hex_rows = {i for i, row in enumerate(_w._NUT_PROFILE) if row[2]}

    def radius_fn(i, r, theta):
        if i in hex_rows:
            a = np.mod(theta + math.pi / 6.0, math.pi / 3.0) - math.pi / 6.0
            return r / np.cos(a)
        return np.full(len(theta), r)

    prof = [(h, r) for (h, r, _) in _w._NUT_PROFILE]
    x0 = X_HUB_FACE - POCKET_DEPTH
    return _revolve(prof, NUT_SEGMENTS, axis_offset=(x0, cy, cz), radius_fn=radius_fn)


def _cap_arrays():
    return _revolve(_CAP_PROFILE, 48, axis_offset=(X_HUB_FACE, 0.0, 0.0))


def _emblem_arrays():
    """Small Toyota style three ellipse emblem embossed on the cap dome."""
    dome = _CAP_PROFILE[9:]
    dome_r = np.array([r for (_, r) in dome])[::-1]
    dome_h = np.array([h for (h, _) in dome])[::-1]

    def height(r):
        return X_HUB_FACE + np.interp(r, dome_r, dome_h) + 0.0006

    def ellipse(ay, az, cz, n=28):
        pts = []
        for k in range(n):
            t = 2.0 * math.pi * k / n
            y, z = ay * math.cos(t), cz + az * math.sin(t)
            pts.append((height(math.hypot(y, z)), y, z))
        return pts

    return [
        _tube_along_curve(ellipse(0.0120, 0.0077, 0.0), 0.0010),
        _tube_along_curve(ellipse(0.0034, 0.0073, 0.0), 0.0009),
        _tube_along_curve(ellipse(0.0072, 0.0029, 0.0033), 0.0009),
    ]


def _lip_arrays():
    """Lip and barrel revolve from wheel.py, with the thin front face of the lip polished."""
    verts, faces = _revolve(_w._lip_profile(), LATHE_SEGMENTS)
    mats = []
    for f in faces:
        xm = float(np.mean([verts[i][0] for i in f]))
        rm = float(np.mean([math.hypot(verts[i][1], verts[i][2]) for i in f]))
        polished = xm > 0.1105 and R_LIP_IN + 0.001 < rm < FLANGE_R - 0.0005
        mats.append(1 if polished else 0)
    return verts, faces, mats


def _disc_wheel_arrays():
    """All disc wheel geometry for a left wheel, plus per face material index and cast face normals."""
    face_v, face_f, face_n = _cast_face_arrays()
    parts = [(face_v, face_f, [0] * len(face_f))]
    lv, lf, lm = _lip_arrays()
    parts.append((lv, lf, lm))
    for (cy, cz) in _lug_centres():
        v, f = _nut_arrays(cy, cz)
        parts.append((v, f, [1] * len(f)))
    v, f = _cap_arrays()
    parts.append((v, f, [0] * len(f)))
    for v, f in _emblem_arrays():
        parts.append((v, f, [1] * len(f)))
    verts, faces, mats = [], [], []
    base = 0
    for v, f, m in parts:
        verts.append(v)
        faces.extend(tuple(i + base for i in fc) for fc in f)
        mats.extend(m)
        base += len(v)
    verts = np.vstack(verts)
    return {
        "verts": verts,
        "faces": faces,
        "mats": np.array(mats, dtype=np.int32),
        "n_face": len(face_v),
        "face_normals": face_n,
    }


# =================================================================================
# Blender mesh assembly (helpers shared with wheel.py)
# =================================================================================
def _get_cached():
    if "disc" not in _CACHE:
        _CACHE["disc"] = _disc_wheel_arrays()
    if "tire" not in _CACHE:
        _CACHE["tire"] = _w._tire_arrays()
    return _CACHE["disc"], _CACHE["tire"]


def _make_disc_wheel(name, mirror):
    disc, _ = _get_cached()
    verts, faces, nrm = disc["verts"], disc["faces"], disc["face_normals"]
    if mirror:
        verts, faces, nrm = _w._mirror_arrays(verts, faces, nrm)
    me = _w._mesh_from_faces(name, verts, faces)
    me.materials.append(materials.get("alloy_wheel"))
    me.materials.append(materials.get("chrome"))
    me.polygons.foreach_set("material_index", disc["mats"])
    _w._shade(me, 45.0, protect_vertex_below=disc["n_face"])
    _w._apply_face_normals(me, disc["n_face"], nrm)
    return bpy.data.objects.new(name, me)


def _make_tire(name, mirror):
    _, tire = _get_cached()
    verts, faces = tire
    if mirror:
        verts, faces, _ = _w._mirror_arrays(verts, faces)
    me = _w._mesh_from_faces(name, verts, faces)
    _w._shade(me, 40.0)
    ob = bpy.data.objects.new(name, me)
    materials.assign(ob, "rubber_tire")
    return ob


triangle_count = _w.triangle_count


def build_wheel_assembly(position):
    """Create the wheel assembly for `position` and return its Empty."""
    if position not in POSITIONS:
        raise ValueError(f"position must be one of {POSITIONS}, got {position!r}")
    mirror = position.endswith("_R")
    names = {
        "assembly": f"WHEEL_0000_wheel_assembly_{position}",
        "disc": f"WHEEL_0000_disc_wheel_{position}",
        "tire": f"WHEEL_0000_tire_{position}",
    }
    for n in names.values():
        _w._remove_existing(n)
    coll = _w._target_collection()

    empty = bpy.data.objects.new(names["assembly"], None)
    empty.empty_display_type = "PLAIN_AXES"
    empty.empty_display_size = 0.15
    empty.location = conventions.wheel_centres()[position]
    empty.rotation_euler = (0.0, 0.0, 0.0)
    empty.scale = (1.0, 1.0, 1.0)
    empty["partKey"] = names["assembly"]
    coll.objects.link(empty)

    disc = _make_disc_wheel(names["disc"], mirror)
    tire = _make_tire(names["tire"], mirror)
    for ob, key in ((disc, "disc"), (tire, "tire")):
        ob["partKey"] = names[key]
        coll.objects.link(ob)
        ob.parent = empty
        ob.matrix_parent_inverse.identity()
        ob.location = (0.0, 0.0, 0.0)
    return empty
