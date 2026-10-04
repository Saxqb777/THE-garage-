"""Wheel assembly for The Garage: 16x8 five spoke alloy plus a 275/70R16 highway tire.

Public entry point:

    build_wheel_assembly(position)  returns the assembly Empty (bpy.types.Object)

position is one of 'front_L', 'front_R', 'rear_L', 'rear_R'. The call creates, in the
current scene, an Empty named WHEEL_0000_wheel_assembly_<position> at the wheel centre
(no rotation, unit scale) with two mesh children whose origins sit at the wheel centre:

    WHEEL_0000_disc_wheel_<position>   alloy wheel, centre cap, six lug nuts
    WHEEL_0000_tire_<position>         tire with geometric tread

Local frame of every object: the spin axis is local X. The outer face of a left wheel
points +X, the outer face of a right wheel points negative X (right wheels are true mirrors of
the left ones). Front and rear wheels are identical.

Geometry approach
Tire: one closed revolve grid around X. The profile holds the ribs and circumferential
  grooves; every profile row has its own column phase pattern (three columns per pitch)
  so V shaped sipes and shoulder notches can be cut by lowering single columns.
Disc wheel cast face (hub ring, five spokes, windows, lug pockets): signed distance
  field sampled on a voxel grid, marching cubes, Blender decimate, vertices projected
  back onto the SDF and normals taken from the SDF gradient.
Lip, flange and barrel, lug nuts, centre cap and emblem: revolve geometry.

The heavy marching cubes work is done once per session and cached as numpy arrays, so
the four wheels build quickly and no temporary datablocks survive the call.
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

POSITIONS = ("front_L", "front_R", "rear_L", "rear_R")

# =================================================================================
# Dimensions (metres, left wheel frame: +X points out of the car)
# =================================================================================
TIRE_R = conventions.TIRE_OUTER_RADIUS          # 0.3955
TIRE_PITCHES = 72                               # tread pitches around the tire
TIRE_COLS_PER_PITCH = 3
TIRE_CROWN = 0.35                               # tread crown: radius drops by this factor times x squared
GROOVE_DEPTH = 0.009

RIM_SEAT_R = conventions.RIM_DIAMETER / 2.0     # 0.2032 bead seat radius
FLANGE_R = RIM_SEAT_R + 0.0175                  # 0.2207 flange outer radius
HALF_RIM_W = conventions.RIM_WIDTH / 2.0        # 0.1016 bead seat half width
LIP_X = 0.1125                                  # outer lip face
R_LIP_IN = 0.194                                # inner wall of the short outer lip
R_PLATE = 0.200                                 # cast face outer radius (buried in lip)

R_HUB = 0.089
X_HUB_FACE = 0.089
X_HUB_BACK = 0.056
X_FACE_HUB = 0.083                              # spoke face height where it meets the hub
X_FACE_RIM = 0.100                              # spoke face height at the lip
T_SPOKE = 0.024
RHO_WIN_IN = 0.097
RHO_WIN_OUT = 0.188
W_SPOKE_HUB = 0.030                             # spoke half width at R_HUB
W_SPOKE_RIM = 0.047                             # spoke half width at R_LIP_IN
R_CORNER_IN = 0.014                             # window fillet radius at the hub end
R_CORNER_OUT = 0.021                            # window fillet radius at the lip end
H_BEVEL = 0.004                                 # how far the spoke face drops at its edges
W_BEVEL = 0.011                                 # width of that slope
R_PCD = 0.1397 / 2.0
R_POCKET = 0.0165
POCKET_DEPTH = 0.005
SEAT_R = 0.0128                                 # cone seat radius at the pocket floor
SEAT_HALF_ANGLE = math.radians(30.0)
R_BORE = 0.042
R_CAP = 0.048
SPOKE_PHASE = math.radians(90.0)                # spoke 0 points to +Z
LUG_PHASE = math.radians(90.0)

MC_VOXEL = 0.00125
MC_FACE_TRIS = 17500
LATHE_SEGMENTS = 120

_CACHE = {}


# =================================================================================
# small numpy helpers
# =================================================================================
def _smin(a, b, k):
    h = np.clip(k - np.abs(a - b), 0.0, None) / k
    return np.minimum(a, b) - h * h * k * 0.25


def _smax(a, b, k):
    return -_smin(-a, -b, k)


def _smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def _sd_polygon(px, py, poly):
    """Exact signed distance from points (px, py) to a closed polygon (N, 2). Negative inside."""
    n = len(poly)
    d = np.full(px.shape, np.inf, dtype=np.float64)
    sign = np.ones(px.shape, dtype=np.float64)
    for i in range(n):
        j = (i - 1) % n
        ex, ey = poly[j][0] - poly[i][0], poly[j][1] - poly[i][1]
        wx, wy = px - poly[i][0], py - poly[i][1]
        t = np.clip((wx * ex + wy * ey) / (ex * ex + ey * ey), 0.0, 1.0)
        bx, by = wx - ex * t, wy - ey * t
        d = np.minimum(d, bx * bx + by * by)
        c1 = py >= poly[i][1]
        c2 = py < poly[j][1]
        c3 = ex * wy > ey * wx
        flip = (c1 & c2 & c3) | (~c1 & ~c2 & ~c3)
        sign = np.where(flip, -sign, sign)
    return sign * np.sqrt(d)


def _signed_volume(verts, faces):
    tot = 0.0
    for f in faces:
        for k in range(1, len(f) - 1):
            a, b, c = verts[f[0]], verts[f[k]], verts[f[k + 1]]
            tot += np.dot(a, np.cross(b, c))
    return tot / 6.0


def _flip_if_inverted(verts, faces):
    if _signed_volume(verts, faces) < 0.0:
        return [tuple(reversed(f)) for f in faces]
    return faces


def _revolve(profile, segments, axis_offset=(0.0, 0.0, 0.0), closed=True, radius_fn=None):
    """Revolve a (h, r) profile around the local X axis.

    h is the position along X, r the radius. Rows with r == 0 become poles.
    radius_fn(row_index, r, theta_array) may reshape a row (used for hex nut flats).
    Returns verts (N, 3) and faces (list of tuples) with outward orientation.
    """
    theta = np.arange(segments) * (2.0 * math.pi / segments)
    rows = []
    verts = []
    for i, (h, r) in enumerate(profile):
        if r <= 1e-9:
            rows.append(("pole", len(verts)))
            verts.append((h, 0.0, 0.0))
        else:
            rr = np.full(segments, r)
            if radius_fn is not None:
                rr = radius_fn(i, r, theta)
            start = len(verts)
            for j in range(segments):
                verts.append((h, rr[j] * math.cos(theta[j]), rr[j] * math.sin(theta[j])))
            rows.append(("ring", start))
    faces = []
    n = len(rows)
    pairs = [(i, (i + 1) % n) for i in range(n)] if closed else [(i, i + 1) for i in range(n - 1)]
    for a, b in pairs:
        ka, sa = rows[a]
        kb, sb = rows[b]
        if ka == "ring" and kb == "ring":
            for j in range(segments):
                j1 = (j + 1) % segments
                faces.append((sa + j, sa + j1, sb + j1, sb + j))
        elif ka == "ring" and kb == "pole":
            for j in range(segments):
                faces.append((sa + j, sa + (j + 1) % segments, sb))
        elif ka == "pole" and kb == "ring":
            for j in range(segments):
                faces.append((sa, sb + (j + 1) % segments, sb + j))
    verts = np.array(verts, dtype=np.float64) + np.array(axis_offset, dtype=np.float64)
    faces = _flip_if_inverted(verts, faces)
    return verts, faces


def _tube_along_curve(points, tube_r, sides=6):
    """Closed tube swept along a closed 3D polyline. Returns verts, faces."""
    pts = np.asarray(points, dtype=np.float64)
    n = len(pts)
    verts = []
    for i in range(n):
        t = pts[(i + 1) % n] - pts[i - 1]
        t /= np.linalg.norm(t)
        up = np.array([1.0, 0.0, 0.0]) if abs(t[0]) < 0.9 else np.array([0.0, 0.0, 1.0])
        b1 = np.cross(t, up)
        b1 /= np.linalg.norm(b1)
        b2 = np.cross(t, b1)
        for k in range(sides):
            a = 2.0 * math.pi * k / sides
            verts.append(pts[i] + tube_r * (math.cos(a) * b1 + math.sin(a) * b2))
    faces = []
    for i in range(n):
        i1 = (i + 1) % n
        for k in range(sides):
            k1 = (k + 1) % sides
            faces.append((i * sides + k, i * sides + k1, i1 * sides + k1, i1 * sides + k))
    verts = np.array(verts)
    faces = _flip_if_inverted(verts, faces)
    return verts, faces


# =================================================================================
# Tire
# =================================================================================
def _tread_r(x):
    return TIRE_R - TIRE_CROWN * x * x


def _tire_rows():
    """Outer half of the tire profile from the crown centre to the bead toe.

    Each row: (x, r, pattern, notch depth, circumferential slant).
    Patterns: 'u' uniform columns, 'a'/'b'/'c' sipe phases, 's'/'t' shoulder notch phases.
    """
    g = GROOVE_DEPTH
    rows = [
        (0.0000, _tread_r(0.0000), "c", 0.002, 0.0025),
        (0.0225, _tread_r(0.0225), "c", 0.002, 0.005),
        (0.0240, _tread_r(0.0240) - g, "c", 0.0, 0.005),
        (0.0310, _tread_r(0.0310) - g, "a", 0.0, 0.0),
        (0.0325, _tread_r(0.0325), "a", 0.002, 0.0),
        (0.0675, _tread_r(0.0675), "a", 0.002, 0.004),
        (0.0690, _tread_r(0.0690) - g, "a", 0.0, 0.004),
        (0.0760, _tread_r(0.0760) - g, "s", 0.0, 0.0),
        (0.0775, _tread_r(0.0775), "s", 0.0055, 0.0),
        (0.0975, _tread_r(0.0975), "s", 0.0055, 0.0),
        (0.1063, 0.3907, "s", 0.0040, 0.0),
        (0.1171, 0.3845, "s", 0.0025, 0.0),
        (0.1244, 0.3744, "s", 0.0010, 0.0),
        (0.1267, 0.3650, "s", 0.0002, 0.0),
        (0.1312, 0.3470, "u", 0.0, 0.0),
        (0.1352, 0.3270, "u", 0.0, 0.0),
        (0.1372, 0.3040, "u", 0.0, 0.0),
        (0.1360, 0.2820, "u", 0.0, 0.0),
        (0.1327, 0.2650, "u", 0.0, 0.0),
        (0.1295, 0.2560, "u", 0.0, 0.0),
        (0.1305, 0.2475, "u", 0.0, 0.0),
        (0.1282, 0.2385, "u", 0.0, 0.0),
        (0.1215, 0.2310, "u", 0.0, 0.0),
        (0.1125, 0.2240, "u", 0.0, 0.0),
        (0.1045, 0.2185, "u", 0.0, 0.0),
        (0.1000, 0.2035, "u", 0.0, 0.0),
        (0.0880, 0.2035, "u", 0.0, 0.0),
    ]
    return rows


def _tire_arrays():
    """Build the tire grid. Returns verts (N, 3) and quad faces."""
    outer = _tire_rows()
    # inner side mirrors the outer side; sipe/notch phases differ so the pattern reads staggered
    swap = {"a": "b", "s": "t", "b": "a", "t": "s", "c": "c", "u": "u"}
    inner = [(-x, r, swap[p], d, sl) for (x, r, p, d, sl) in reversed(outer[1:])]
    liner = [(0.0, 0.300, "u", 0.0, 0.0)]
    rows = outer + liner + inner
    P = len(rows)
    C = TIRE_PITCHES * TIRE_COLS_PER_PITCH
    L = 2.0 * math.pi * TIRE_R / TIRE_PITCHES
    phase = {"u": None, "a": 0.05, "b": 0.72, "c": 0.55, "s": 0.30, "t": 0.78}
    notch_w = {"a": 0.0008, "b": 0.0008, "c": 0.0008, "s": 0.0030, "t": 0.0030}

    xs = np.array([r[0] for r in rows])
    rs = np.array([r[1] for r in rows])
    # inward profile normals (2D, in the x r plane) from central differences on the closed loop
    tx = np.roll(xs, -1) - np.roll(xs, 1)
    tr = np.roll(rs, -1) - np.roll(rs, 1)
    ln = np.hypot(tx, tr)
    nx, nr = tr / ln, -tx / ln
    # orient inward: the loop interior centroid
    cx, cr = xs.mean(), rs.mean()
    flip = (nx * (cx - xs) + nr * (cr - rs)) < 0
    nx = np.where(flip, -nx, nx)
    nr = np.where(flip, -nr, nr)
    # for tread rows the notch goes straight down in radius
    for i, (x, r, p, d, sl) in enumerate(rows):
        if p in ("a", "b", "c") or (p in ("s", "t") and abs(x) <= 0.1005):
            nx[i], nr[i] = 0.0, -1.0

    verts = np.empty((P, C, 3), dtype=np.float64)
    pitch_idx = np.arange(C) // TIRE_COLS_PER_PITCH
    sub_idx = np.arange(C) % TIRE_COLS_PER_PITCH
    for i, (x, r, p, d, sl) in enumerate(rows):
        if phase[p] is None:
            off = sub_idx * (L / TIRE_COLS_PER_PITCH)
            depth = np.zeros(C)
        else:
            w = notch_w[p]
            off = phase[p] * L + sl + sub_idx * w
            depth = np.where(sub_idx == 1, d, 0.0)
        s = pitch_idx * L + off
        theta = s / TIRE_R
        rr = r - depth * (-nr[i])  # move along the inward normal
        xx = x - depth * (-nx[i])
        verts[i, :, 0] = xx
        verts[i, :, 1] = rr * np.cos(theta)
        verts[i, :, 2] = rr * np.sin(theta)
    faces = []
    for i in range(P):
        i1 = (i + 1) % P
        for j in range(C):
            j1 = (j + 1) % C
            faces.append((i * C + j, i * C + j1, i1 * C + j1, i1 * C + j))
    verts = verts.reshape(-1, 3)
    faces = _flip_if_inverted(verts, faces)
    return verts, faces


# =================================================================================
# Disc wheel: cast face as a signed distance field
# =================================================================================
def _window_outline():
    """One window (between two spokes) as a closed polygon in a frame whose +v axis is the window bisector.

    Straight spoke edges, an inner arc around the hub, an outer arc near the lip, with
    tangent fillets of radius R_CORNER_IN at the hub end and R_CORNER_OUT at the lip end.
    """
    half = math.pi / 5.0
    s0, s1 = R_HUB, R_LIP_IN
    b = (W_SPOKE_RIM - W_SPOKE_HUB) / (s1 - s0)
    a0 = W_SPOKE_HUB - b * s0
    kappa = math.sqrt(1.0 + b * b)
    ang_r = math.pi / 2.0 - half
    e = np.array([math.cos(ang_r), math.sin(ang_r)])
    nrm = np.array([-math.sin(ang_r), math.cos(ang_r)])
    m = (-b * e + nrm) / kappa  # unit normal of the spoke edge, pointing into the window

    def line_circle(a, rho):
        A, B, Cc = 1.0 + b * b, 2.0 * a * b, a * a - rho * rho
        sc = (-B + math.sqrt(B * B - 4.0 * A * Cc)) / (2.0 * A)
        return sc * e + (a + b * sc) * nrm

    def arc(c, p_from, p_to, r, n):
        a1 = math.atan2(p_from[1] - c[1], p_from[0] - c[0])
        a2 = math.atan2(p_to[1] - c[1], p_to[0] - c[0])
        da = (a2 - a1 + math.pi) % (2.0 * math.pi) - math.pi
        return [(c[0] + r * math.cos(a1 + da * t), c[1] + r * math.sin(a1 + da * t))
                for t in np.linspace(0.0, 1.0, n)[1:-1]]

    ri, ro = R_CORNER_IN, R_CORNER_OUT
    c_in = line_circle(a0 + ri * kappa, RHO_WIN_IN + ri)
    c_out = line_circle(a0 + ro * kappa, RHO_WIN_OUT - ro)
    t_in_line = c_in - ri * m
    t_in_circ = c_in * (RHO_WIN_IN / np.linalg.norm(c_in))
    t_out_line = c_out - ro * m
    t_out_circ = c_out * (RHO_WIN_OUT / np.linalg.norm(c_out))

    def mirror(p):
        return np.array([-p[0], p[1]])

    pts = [tuple(t_in_circ)]
    pts += arc(c_in, t_in_circ, t_in_line, ri, 7)
    pts += [tuple(t_in_line), tuple(t_out_line)]
    pts += arc(c_out, t_out_line, t_out_circ, ro, 8)
    pts.append(tuple(t_out_circ))
    a_out = math.atan2(t_out_circ[1], t_out_circ[0])
    for t in np.linspace(a_out, math.pi - a_out, 16)[1:-1]:
        pts.append((RHO_WIN_OUT * math.cos(t), RHO_WIN_OUT * math.sin(t)))
    pts.append(tuple(mirror(t_out_circ)))
    pts += [(-q[0], q[1]) for q in reversed(arc(c_out, t_out_line, t_out_circ, ro, 8))]
    pts += [tuple(mirror(t_out_line)), tuple(mirror(t_in_line))]
    pts += [(-q[0], q[1]) for q in reversed(arc(c_in, t_in_circ, t_in_line, ri, 7))]
    pts.append(tuple(mirror(t_in_circ)))
    a_in = math.atan2(t_in_circ[1], t_in_circ[0])
    for t in np.linspace(math.pi - a_in, a_in, 9)[1:-1]:
        pts.append((RHO_WIN_IN * math.cos(t), RHO_WIN_IN * math.sin(t)))
    return np.array(pts)


def _face_fields_2d(y, z):
    """2D fields on the wheel plane needed by the SDF."""
    rho = np.hypot(y, z)
    phi = np.arctan2(z, y)
    win0 = SPOKE_PHASE + math.pi / 5.0
    sector = 2.0 * math.pi / 5.0
    k = np.round((phi - win0) / sector)
    loc = phi - (win0 + k * sector)
    u = -rho * np.sin(loc)
    v = rho * np.cos(loc)
    d_win = _sd_polygon(u, v, _window_outline())
    return rho, d_win


def _x_face(rho):
    s = np.clip((rho - R_HUB) / (R_LIP_IN - R_HUB), 0.0, 1.0)
    return X_FACE_HUB + (X_FACE_RIM - X_FACE_HUB) * s ** 1.4


def _lug_centres():
    return [(R_PCD * math.cos(LUG_PHASE + i * math.pi / 3.0),
             R_PCD * math.sin(LUG_PHASE + i * math.pi / 3.0)) for i in range(6)]


def _face_sdf(x, y, z):
    """Signed distance like field of the cast wheel face. x, y, z broadcastable arrays."""
    rho, d_win = _face_fields_2d(y, z)
    xf = _x_face(rho)
    bevel = H_BEVEL * (1.0 - _smoothstep(0.0, W_BEVEL, d_win))
    x_front = xf - bevel
    x_back = xf - T_SPOKE
    # spoke plate
    plate = _smax(-d_win, x - x_front, 0.004)
    plate = _smax(plate, x_back - x, 0.002)
    plate = np.maximum(plate, rho - R_PLATE)
    # hub ring
    hub = _smax(rho - R_HUB, x - X_HUB_FACE, 0.003)
    hub = np.maximum(hub, X_HUB_BACK - x)
    hub = np.maximum(hub, R_BORE - rho)
    floor_x = X_HUB_FACE - POCKET_DEPTH
    apex_x = floor_x - SEAT_R / math.tan(SEAT_HALF_ANGLE)
    ca, sa = math.cos(SEAT_HALF_ANGLE), math.sin(SEAT_HALF_ANGLE)
    for (cy, cz) in _lug_centres():
        rn = np.hypot(y - cy, z - cz)
        pocket = np.maximum(rn - R_POCKET, floor_x - x)
        hub = _smax(hub, -pocket, 0.0015)
        cone = rn * ca - (x - apex_x) * sa
        hub = np.maximum(hub, -cone)
    return _smin(plate, hub, 0.004)


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
    xs = np.arange(0.050, 0.108, vx)
    X = xs[:, None, None]
    Y = ys[None, :, None]
    Z = ys[None, None, :]
    vol = np.empty((len(xs), len(ys), len(ys)), dtype=np.float32)
    # evaluate slice by slice to keep memory small, 2D fields are shared
    rho, d_win = _face_fields_2d(Y[0], Z[0])
    xf = _x_face(rho)
    bevel = H_BEVEL * (1.0 - _smoothstep(0.0, W_BEVEL, d_win))
    x_front = xf - bevel
    x_back = xf - T_SPOKE
    floor_x = X_HUB_FACE - POCKET_DEPTH
    apex_x = floor_x - SEAT_R / math.tan(SEAT_HALF_ANGLE)
    ca, sa = math.cos(SEAT_HALF_ANGLE), math.sin(SEAT_HALF_ANGLE)
    lug_rn = [np.hypot(Y[0] - cy, Z[0] - cz) for (cy, cz) in _lug_centres()]
    for i, x in enumerate(xs):
        plate = _smax(-d_win, x - x_front, 0.004)
        plate = _smax(plate, x_back - x, 0.002)
        plate = np.maximum(plate, rho - R_PLATE)
        hub = _smax(rho - R_HUB, x - X_HUB_FACE, 0.003)
        hub = np.maximum(hub, X_HUB_BACK - x)
        hub = np.maximum(hub, R_BORE - rho)
        for rn in lug_rn:
            pocket = np.maximum(rn - R_POCKET, floor_x - x)
            hub = _smax(hub, -pocket, 0.0015)
            cone = rn * ca - (x - apex_x) * sa
            hub = np.maximum(hub, -cone)
        vol[i] = _smin(plate, hub, 0.004)
    verts, faces, _, _ = measure.marching_cubes(vol, level=0.0, spacing=(vx, vx, vx))
    verts = verts.astype(np.float64)
    verts[:, 0] += xs[0]
    verts[:, 1] += ys[0]
    verts[:, 2] += ys[0]
    return verts, faces.astype(np.int64)


def _decimate_tris(verts, tris, target):
    """Decimate a triangle soup with Blender's collapse decimator. Temporary datablocks are removed."""
    me = bpy.data.meshes.new("_wheel_tmp_mc")
    n, m = len(verts), len(tris)
    me.vertices.add(n)
    me.vertices.foreach_set("co", verts.ravel())
    me.loops.add(m * 3)
    me.loops.foreach_set("vertex_index", tris.ravel())
    me.polygons.add(m)
    me.polygons.foreach_set("loop_start", np.arange(m) * 3)
    me.polygons.foreach_set("loop_total", np.full(m, 3))
    me.update(calc_edges=True)
    ob = bpy.data.objects.new("_wheel_tmp_mc", me)
    bpy.context.scene.collection.objects.link(ob)
    mod = ob.modifiers.new("dec", "DECIMATE")
    mod.decimate_type = "COLLAPSE"
    mod.ratio = min(1.0, target / float(m))
    mod.use_collapse_triangulate = True
    dg = bpy.context.evaluated_depsgraph_get()
    ev = ob.evaluated_get(dg)
    me2 = bpy.data.meshes.new_from_object(ev)
    v = np.empty(len(me2.vertices) * 3)
    me2.vertices.foreach_get("co", v)
    v = v.reshape(-1, 3)
    faces = [tuple(p.vertices) for p in me2.polygons]
    bpy.data.objects.remove(ob, do_unlink=True)
    bpy.data.meshes.remove(me)
    bpy.data.meshes.remove(me2)
    return v, faces


def _cast_face_arrays():
    verts, tris = _marching_cubes_face()
    verts, faces = _decimate_tris(verts, tris, MC_FACE_TRIS)
    # drop unreferenced vertices, project onto the SDF, normals from the gradient
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
# Disc wheel: revolve parts
# =================================================================================
def _lip_profile():
    f = FLANGE_R
    return [
        (0.0850, R_LIP_IN),
        (0.1090, R_LIP_IN),
        (0.1112, R_LIP_IN + 0.0008),
        (0.1124, R_LIP_IN + 0.0028),
        (LIP_X, R_LIP_IN + 0.0050),
        (LIP_X, f - 0.0042),
        (0.1116, f - 0.0017),
        (0.1096, f - 0.0003),
        (0.1070, f),
        (0.1046, f),
        (HALF_RIM_W, RIM_SEAT_R + 0.0004),
        (0.0870, RIM_SEAT_R),
        (0.0620, 0.1850),
        (-0.0300, 0.1850),
        (-0.0600, RIM_SEAT_R),
        (-HALF_RIM_W, RIM_SEAT_R + 0.0004),
        (-0.1046, f),
        (-0.1070, f),
        (-0.1096, f - 0.0003),
        (-0.1116, f - 0.0017),
        (-LIP_X, f - 0.0042),
        (-LIP_X, 0.2010),
        (-0.1095, 0.1968),
        (-0.0560, 0.1968),
        (-0.0400, 0.1790),
        (0.0520, 0.1790),
        (0.0680, 0.1968),
        (0.0850, 0.1968),
    ]


_NUT_PROFILE = [
    (-0.0020, 0.0000, False),
    (-0.0020, 0.0064, False),
    (0.0000, 0.0070, False),
    (0.0090, 0.0122, False),
    (0.0103, 0.0124, False),
    (0.0110, 0.0110, True),
    (0.0195, 0.0110, True),
    (0.0208, 0.0100, False),
    (0.0230, 0.0088, False),
    (0.0252, 0.0065, False),
    (0.0268, 0.0036, False),
    (0.0274, 0.0000, False),
]

_CAP_PROFILE = [
    (-0.0050, 0.0000),
    (-0.0050, 0.0410),
    (0.0000, 0.0415),
    (0.0000, 0.0475),
    (0.0062, 0.0480),
    (0.0088, 0.0460),
    (0.0094, 0.0418),
    (0.0076, 0.0390),
    (0.0076, 0.0335),
    (0.0095, 0.0250),
    (0.0112, 0.0145),
    (0.0120, 0.0000),
]


def _nut_arrays(cy, cz):
    hex_rows = {i for i, row in enumerate(_NUT_PROFILE) if row[2]}

    def radius_fn(i, r, theta):
        if i in hex_rows:
            a = np.mod(theta + math.pi / 6.0, math.pi / 3.0) - math.pi / 6.0
            return r / np.cos(a)
        return np.full(len(theta), r)

    prof = [(h, r) for (h, r, _) in _NUT_PROFILE]
    x0 = X_HUB_FACE - POCKET_DEPTH
    return _revolve(prof, 24, axis_offset=(x0, cy, cz), radius_fn=radius_fn)


def _cap_arrays():
    return _revolve(_CAP_PROFILE, 40, axis_offset=(X_HUB_FACE, 0.0, 0.0))


def _emblem_arrays():
    """Toyota style three ellipse emblem embossed on the cap dome."""
    dome = [(r, h) for (h, r) in _CAP_PROFILE[7:]]
    dome_r = np.array([d[0] for d in dome])[::-1]
    dome_h = np.array([d[1] for d in dome])[::-1]

    def height(r):
        return X_HUB_FACE + np.interp(r, dome_r, dome_h) + 0.0008

    def ellipse(ay, az, cz, n=36):
        pts = []
        for k in range(n):
            t = 2.0 * math.pi * k / n
            y, z = ay * math.cos(t), cz + az * math.sin(t)
            pts.append((height(math.hypot(y, z)), y, z))
        return pts

    parts = [
        _tube_along_curve(ellipse(0.0200, 0.0128, 0.0), 0.0013),
        _tube_along_curve(ellipse(0.0056, 0.0122, 0.0), 0.0012),
        _tube_along_curve(ellipse(0.0120, 0.0048, 0.0055), 0.0012),
    ]
    return parts


def _disc_wheel_arrays():
    """All disc wheel geometry for a left wheel, plus per face material index and cast face normals."""
    face_v, face_f, face_n = _cast_face_arrays()
    parts = [(face_v, face_f, 0)]
    parts.append((*_revolve(_lip_profile(), LATHE_SEGMENTS), 0))
    for (cy, cz) in _lug_centres():
        parts.append((*_nut_arrays(cy, cz), 1))
    parts.append((*_cap_arrays(), 0))
    for v, f in _emblem_arrays():
        parts.append((v, f, 1))
    verts, faces, mats = [], [], []
    base = 0
    for v, f, m in parts:
        verts.append(v)
        faces.extend(tuple(i + base for i in fc) for fc in f)
        mats.extend([m] * len(f))
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
# Blender mesh assembly
# =================================================================================
def _mesh_from_faces(name, verts, faces):
    me = bpy.data.meshes.new(name)
    sizes = np.fromiter((len(f) for f in faces), dtype=np.int64, count=len(faces))
    loops = np.fromiter((i for f in faces for i in f), dtype=np.int64, count=int(sizes.sum()))
    starts = np.concatenate(([0], np.cumsum(sizes)[:-1]))
    me.vertices.add(len(verts))
    me.vertices.foreach_set("co", np.asarray(verts, dtype=np.float64).ravel())
    me.loops.add(len(loops))
    me.loops.foreach_set("vertex_index", loops)
    me.polygons.add(len(faces))
    me.polygons.foreach_set("loop_start", starts)
    me.polygons.foreach_set("loop_total", sizes)
    me.update(calc_edges=True)
    return me


def _shade(me, sharp_angle_deg, protect_vertex_below=None):
    """Smooth shading with edges marked sharp by dihedral angle.

    Edges whose both vertices are below protect_vertex_below are never marked sharp (the
    cast face gets custom normals instead).
    """
    npoly = len(me.polygons)
    me.polygons.foreach_set("use_smooth", np.ones(npoly, dtype=bool))
    pn = np.empty(npoly * 3)
    me.polygons.foreach_get("normal", pn)
    pn = pn.reshape(-1, 3)
    nloops = len(me.loops)
    le = np.empty(nloops, dtype=np.int64)
    me.loops.foreach_get("edge_index", le)
    sizes = np.empty(npoly, dtype=np.int64)
    me.polygons.foreach_get("loop_total", sizes)
    lp = np.repeat(np.arange(npoly), sizes)
    order = np.argsort(le, kind="stable")
    le_s, lp_s = le[order], lp[order]
    nedges = len(me.edges)
    first = np.searchsorted(le_s, np.arange(nedges), side="left")
    last = np.searchsorted(le_s, np.arange(nedges), side="right")
    two = (last - first) == 2
    fa = lp_s[first[two]]
    fb = lp_s[np.minimum(first[two] + 1, nloops - 1)]
    cosang = np.sum(pn[fa] * pn[fb], axis=1)
    sharp = np.zeros(nedges, dtype=bool)
    sharp[two] = cosang < math.cos(math.radians(sharp_angle_deg))
    if protect_vertex_below is not None:
        ev = np.empty(nedges * 2, dtype=np.int64)
        me.edges.foreach_get("vertices", ev)
        ev = ev.reshape(-1, 2)
        protected = (ev[:, 0] < protect_vertex_below) & (ev[:, 1] < protect_vertex_below)
        sharp &= ~protected
    attr = me.attributes.get("sharp_edge")
    if attr is None:
        attr = me.attributes.new("sharp_edge", "BOOLEAN", "EDGE")
    attr.data.foreach_set("value", sharp)
    me.update()


def _apply_face_normals(me, n_face, face_normals):
    """Custom split normals: SDF gradient on the cast face, Blender's own normals elsewhere."""
    nloops = len(me.loops)
    cn = np.empty(nloops * 3)
    me.corner_normals.foreach_get("vector", cn)
    cn = cn.reshape(-1, 3)
    lv = np.empty(nloops, dtype=np.int64)
    me.loops.foreach_get("vertex_index", lv)
    mask = lv < n_face
    cn[mask] = face_normals[lv[mask]]
    me.normals_split_custom_set([tuple(v) for v in cn])
    me.update()


def _mirror_arrays(verts, faces, normals=None):
    v = verts.copy()
    v[:, 0] *= -1.0
    f = [tuple(reversed(fc)) for fc in faces]
    n = None
    if normals is not None:
        n = normals.copy()
        n[:, 0] *= -1.0
    return v, f, n


def _remove_existing(name):
    ob = bpy.data.objects.get(name)
    if ob is not None:
        data = ob.data
        bpy.data.objects.remove(ob, do_unlink=True)
        if data is not None and data.users == 0:
            bpy.data.meshes.remove(data)
    me = bpy.data.meshes.get(name)
    if me is not None and me.users == 0:
        bpy.data.meshes.remove(me)


def _target_collection():
    coll = getattr(bpy.context, "collection", None)
    if coll is None:
        coll = bpy.context.scene.collection
    return coll


def _get_cached():
    if "disc" not in _CACHE:
        _CACHE["disc"] = _disc_wheel_arrays()
    if "tire" not in _CACHE:
        _CACHE["tire"] = _tire_arrays()
    return _CACHE["disc"], _CACHE["tire"]


def _make_disc_wheel(name, mirror):
    disc, _ = _get_cached()
    verts, faces, nrm = disc["verts"], disc["faces"], disc["face_normals"]
    if mirror:
        verts, faces, nrm = _mirror_arrays(verts, faces, nrm)
    me = _mesh_from_faces(name, verts, faces)
    me.materials.append(materials.get("alloy_wheel"))
    me.materials.append(materials.get("chrome"))
    me.polygons.foreach_set("material_index", disc["mats"])
    _shade(me, 45.0, protect_vertex_below=disc["n_face"])
    _apply_face_normals(me, disc["n_face"], nrm)
    ob = bpy.data.objects.new(name, me)
    return ob


def _make_tire(name, mirror):
    _, tire = _get_cached()
    verts, faces = tire
    if mirror:
        verts, faces, _ = _mirror_arrays(verts, faces)
    me = _mesh_from_faces(name, verts, faces)
    _shade(me, 40.0)
    ob = bpy.data.objects.new(name, me)
    materials.assign(ob, "rubber_tire")
    return ob


def triangle_count(ob):
    return sum(len(p.vertices) - 2 for p in ob.data.polygons)


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
        _remove_existing(n)
    coll = _target_collection()

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
