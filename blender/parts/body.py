"""Procedural LC100 body: skin from the SDF, sliced into named panels with real gaps.

Pipeline (see build()):
  1. marching cubes of body_sdf.body, decimated
  2. plane cuts along every panel, glass, seal and lamp outline (gaps get two cuts)
  3. classify faces into regions (gap strips and the grille opening are deleted)
  4. one object per part, custom normals from the SDF, thickness for openable panels
Outlines are in docs/reference-notes.md terms: side view (u, z), top view (u, x),
rear or front view (x, z), always for the vehicle's left side; right side is mirrored.
"""
import math

import bmesh
import bpy
import numpy as np

from blender.lib import conventions as C
from blender.lib import materials as MAT
from blender.lib import meshing as M
from blender.parts import body_sdf as S

GAP = 0.004
LAMP_GAP = 0.003
HALF_WB = C.WHEELBASE / 2.0

# ---------------------------------------------------------------------------
# Outlines (left side). Side view points are (u, z).


def belt(u):
    return S.belt_z(u)


def sill_z(u):
    return belt(u) + 0.022


A_PILLAR = lambda z: 0.668 + S.WS_SLOPE * (z - 1.27)  # noqa: E731  front door front edge above the belt
C_CUT = lambda z: 2.585 - 0.43 * (z - 1.255)  # noqa: E731  rear door rear edge above the belt
DOOR_TOP = 1.78
DOOR_BOTTOM = 0.49
WIN_TOP = 1.748  # glass top edge; seal reaches 2 cm higher

REAR_ARCH_R = S.ARCH_R + 0.03


def arc(uc, zc, r, u_start, z_end, n=14):
    """Points on a circle from its upper point at u = u_start, sweeping forward and down to height z_end."""
    ang0 = math.atan2(math.sqrt(max(r * r - (u_start - uc) ** 2, 0.0)), u_start - uc)
    dz1 = z_end - zc
    ang1 = math.atan2(dz1, -math.sqrt(max(r * r - dz1 * dz1, 0.0)))
    return [(uc + r * math.cos(a), zc + r * math.sin(a)) for a in np.linspace(ang0, ang1, n)]


def side_cuts():
    """(name, view, polyline, gap, filter key) for the left side."""
    rd_rear = [(C_CUT(1.80), 1.80), (C_CUT(1.255), 1.255), (2.66, 1.16), (2.68, 1.08), (2.68, 0.86)]
    return [
        ("fd_front", [(0.632, 0.43), (0.632, 1.232), (0.668, 1.27), (A_PILLAR(DOOR_TOP), DOOR_TOP), (A_PILLAR(1.80), 1.80)], GAP),
        ("door_top", [(A_PILLAR(DOOR_TOP) - 0.05, DOOR_TOP), (C_CUT(DOOR_TOP) + 0.05, DOOR_TOP)], GAP),
        ("b_pillar", [(1.692, 0.43), (1.692, 1.80)], GAP),
        ("door_bottom", [(0.45, DOOR_BOTTOM), (2.42, DOOR_BOTTOM)], GAP),
        ("rd_rear", rd_rear, GAP),
        ("rd_arch", arc(C.U_REAR_AXLE, S.ARCH_Z, REAR_ARCH_R, 2.68, DOOR_BOTTOM - 0.02), 0.0),
        ("fender_top_rear", None, GAP),  # handled as a top view cut
    ]


def window_outlines():
    """Seal outer outline and glass outline per window, side view, left side."""
    top_o, top_i = WIN_TOP + 0.02, WIN_TOP
    fd_out = [(A_PILLAR(sill_z(0.66)) + 0.035, sill_z(0.66)), (1.655, sill_z(1.655)), (1.655, top_o), (A_PILLAR(top_o) + 0.035, top_o)]
    fd_in = [(A_PILLAR(sill_z(0.7) + 0.02) + 0.066, sill_z(0.7) + 0.02), (1.635, sill_z(1.635) + 0.02), (1.635, top_i), (A_PILLAR(top_i) + 0.066, top_i)]
    rd_out = [(1.725, sill_z(1.725)), (2.300, sill_z(2.300)), (2.300, top_o), (1.725, top_o)]
    rd_in = [(1.745, sill_z(1.745) + 0.02), (2.285, sill_z(2.285) + 0.02), (2.285, top_i), (1.745, top_i)]
    rq_rear = lambda z, inset: 2.545 - inset - 0.43 * (z - 1.255)  # noqa: E731
    z0 = sill_z(2.30)
    rq_out = [(2.300, z0), (rq_rear(z0, 0.0), z0), (rq_rear(top_o, 0.0), top_o), (2.300, top_o)]
    rq_in = [(2.315, z0 + 0.02), (rq_rear(z0 + 0.02, 0.022), z0 + 0.02), (rq_rear(top_i, 0.022), top_i), (2.315, top_i)]
    qw_front = lambda z, inset: 2.655 + inset - 0.43 * (z - 1.255)  # noqa: E731
    q0 = sill_z(2.65)
    qw_out = [(qw_front(q0, 0), q0), (3.42, sill_z(3.42)), (3.415, top_o - 0.12), (3.39, top_o - 0.05), (3.33, top_o - 0.008),
              (3.28, top_o), (qw_front(top_o, 0), top_o)]
    qw_in = [(qw_front(q0 + 0.02, 0.022), q0 + 0.02), (3.40, sill_z(3.40) + 0.02), (3.395, top_i - 0.12), (3.372, top_i - 0.055),
             (3.318, top_i - 0.012), (3.275, top_i), (qw_front(top_i, 0.022), top_i)]
    return {
        "fd": (fd_out, fd_in),
        "rd": (rd_out, rd_in),
        "rq": (rq_out, rq_in),
        "qw": (qw_out, qw_in),
    }


def back_outlines():
    """Rear view (x, z) outlines for the left back door."""
    door_outer = [(0.785, 0.78), (0.785, 1.30), (0.66, 1.795), (0.645, 1.83)]
    glass_out = [(0.032, 1.315), (0.765, 1.315), (0.652, 1.69), (0.615, 1.745), (0.032, 1.755)]
    glass_in = [(0.052, 1.335), (0.742, 1.335), (0.637, 1.68), (0.604, 1.725), (0.052, 1.735)]
    return door_outer, glass_out, glass_in


def windshield_outlines():
    def half(z, inset):
        return S.gh_w(z) - inset
    out = [(-half(1.285, 0.065), 1.285), (half(1.285, 0.065), 1.285), (half(1.775, 0.065), 1.775), (-half(1.775, 0.065), 1.775)]
    inn = [(-half(1.305, 0.085), 1.305), (half(1.305, 0.085), 1.305), (half(1.755, 0.085), 1.755), (-half(1.755, 0.085), 1.755)]
    return out, inn


FUEL_LID = [(3.255 + 0.02, 1.005), (3.405 - 0.02, 1.005), (3.405 - 0.006, 1.011), (3.405, 1.025), (3.405, 1.155 - 0.02),
            (3.405 - 0.006, 1.149), (3.405 - 0.02, 1.155), (3.255 + 0.02, 1.155), (3.255 + 0.006, 1.149), (3.255, 1.155 - 0.02),
            (3.255, 1.025), (3.255 + 0.006, 1.011), (3.255 + 0.02, 1.005)]

HEADLAMP = dict(z0=0.895, z1=1.090, x_in=0.4435, u_side=-0.66)
HEADLAMP_SIDE = [(-0.735, 0.86), (-0.715, 0.895), (-0.66, 0.965), (-0.66, 1.11)]  # side view outline, raked lower corner
GRILLE = dict(x=0.4435, z0=0.862, z1=1.090)
TAILLAMP = dict(z0=0.865, z1=1.235, x_in=0.795, u_side=3.775, clear=(1.018, 1.133))
HOOD = dict(x=0.80, u_rear=0.47, z_front=1.092)

# ---------------------------------------------------------------------------
# Face filters used by the cuts. Each takes (u, x, z, n) arrays for one face set.


def _mirror_pts(view, pts):
    if view == "side":
        return pts
    if view in ("front", "rear"):
        return [(-a, b) for a, b in pts]
    if view == "top":
        return [(a, -b) for a, b in pts]
    raise ValueError(view)


class Slicer:
    def __init__(self, bm):
        self.bm = bm
        self.cutter = M.Cutter(bm, lambda c: M.sdf_vertex_normals(S.body, c))

    def poly_cut(self, view, pts, gap, region_filter, margin=0.03):
        """Cut along a polyline (and its gap edges); remember gap strips for deletion."""
        offsets = [0.0] if gap <= 0 else [-gap / 2, gap / 2]
        for off in offsets:
            line = pts if off == 0 else M.offset_polyline(pts, off)
            for co, no, (a0, b0), (a1, b1) in M.segment_planes("front" if view == "rear" else view, line):
                lo, hi = self._bbox(view, (a0, b0), (a1, b1), margin)
                self.cutter.cut(co, no, lo, hi, mask_fn=region_filter)

    @staticmethod
    def _bbox(view, p0, p1, m):
        a = sorted((p0[0], p1[0]))
        b = sorted((p0[1], p1[1]))
        big = 5.0
        if view == "side":
            lo = (-big, a[0] - m - HALF_WB, b[0] - m)
            hi = (big, a[1] + m - HALF_WB, b[1] + m)
        elif view == "top":
            lo = (b[0] - m, a[0] - m - HALF_WB, -big)
            hi = (b[1] + m, a[1] + m - HALF_WB, big)
        else:  # front or rear view, (x, z)
            lo = (a[0] - m, -big, b[0] - m)
            hi = (a[1] + m, big, b[1] + m)
        return lo, hi


def face_filter(kind, side="L"):
    """Vectorised predicate on (centroids, normals) arrays in Blender space, for choosing which faces a cut touches.

    Deliberately loose: an extra cut only adds edges, but a missed cut leaves a big triangle
    straddling an outline, which then shows up as a jagged sliver after classification.
    Only side view cuts need the side test (their bounding box spans the full width); every
    other view is already limited in x by its bounding box, and a centroid side test there
    skips wide triangles that cross the centre line.
    """
    sgn = 1.0 if side == "L" else -1.0

    def f(c, n):
        u, x, z = c[:, 1] + HALF_WB, c[:, 0], c[:, 2]
        if kind == "side":
            return x * sgn > 0.3
        if kind == "top":
            return z > 0.95
        if kind == "top_any":
            return z > 0.95
        if kind == "front":
            return u < -0.3
        if kind == "rear":
            return u > 3.3
        if kind == "rear_any":
            return u > 3.3
        if kind == "ws":
            return (z > 1.15) & (u < 1.7)
        if kind == "lamp_front":
            return u < -0.3
        if kind == "lamp_rear":
            return u > 3.5
        if kind == "hood_side":
            return (u < 0.6) & (z > 0.98)
        raise ValueError(kind)

    return f


def apply_cuts(sl):
    for side in ("L", "R"):
        mir = (lambda v, p: p) if side == "L" else _mirror_pts
        fs = face_filter("side", side)
        for name, pts, gap in [(n, p, g) for n, p, g in side_cuts() if p is not None]:
            sl.poly_cut("side", pts, gap, fs)
        for key, (out, inn) in window_outlines().items():
            sl.poly_cut("side", out + [out[0]], 0.0, fs, margin=0.02)
            sl.poly_cut("side", inn + [inn[0]], 0.0, fs, margin=0.02)
        if side == "L":
            sl.poly_cut("side", FUEL_LID, LAMP_GAP, fs, margin=0.01)
        # hood sides and fender top rear edge
        x = HOOD["x"]
        sl.poly_cut("top", mir("top", [(-0.95, x), (HOOD["u_rear"] + 0.03, x)]), GAP, face_filter("hood_side", side))
        sl.poly_cut("top", mir("top", [(0.50, x - 0.02), (0.50, 0.99)]), GAP, face_filter("top", side))
        # headlamp box
        lf = face_filter("lamp_front", side)
        hx = HEADLAMP["x_in"]
        sl.poly_cut("front", mir("front", [(hx - 0.1, HEADLAMP["z0"]), (1.0, HEADLAMP["z0"])]), LAMP_GAP, lf)
        sl.poly_cut("front", mir("front", [(hx, 0.84), (hx, HEADLAMP["z1"] + 0.02)]), LAMP_GAP, lf)
        sl.poly_cut("side", HEADLAMP_SIDE, LAMP_GAP, fs)
        # grille bottom
        sl.poly_cut("front", mir("front", [(0.0, GRILLE["z0"]), (GRILLE["x"] + 0.01, GRILLE["z0"])]), 0.0, face_filter("front", side))
        # tail lamp box
        rf = face_filter("lamp_rear", side)
        for zz in (TAILLAMP["z0"], TAILLAMP["z1"]):
            sl.poly_cut("rear", mir("rear", [(TAILLAMP["x_in"] - 0.05, zz), (1.0, zz)]), LAMP_GAP, rf)
        for zz in TAILLAMP["clear"]:
            sl.poly_cut("rear", mir("rear", [(TAILLAMP["x_in"], zz), (1.0, zz)]), 0.0, rf)
        sl.poly_cut("rear", mir("rear", [(TAILLAMP["x_in"], TAILLAMP["z0"] - 0.02), (TAILLAMP["x_in"], TAILLAMP["z1"] + 0.02)]), LAMP_GAP, face_filter("rear", side))
        sl.poly_cut("side", [(TAILLAMP["u_side"], TAILLAMP["z0"] - 0.02), (TAILLAMP["u_side"], TAILLAMP["z1"] + 0.02)], LAMP_GAP, fs)
        # back door outer edge and glass
        door_outer, g_out, g_in = back_outlines()
        rr = face_filter("rear", side)
        sl.poly_cut("rear", mir("rear", door_outer), GAP, rr)
        sl.poly_cut("rear", mir("rear", g_out + [g_out[0]]), 0.0, rr, margin=0.02)
        sl.poly_cut("rear", mir("rear", g_in + [g_in[0]]), 0.0, rr, margin=0.02)
    # shared lines across the car
    rr_any = face_filter("rear_any")
    sl.poly_cut("rear", [(0.0, 0.78), (0.0, 1.83)], GAP, rr_any)
    sl.poly_cut("rear", [(-0.80, 0.80), (0.80, 0.80)], GAP, rr_any)
    sl.poly_cut("rear", [(-0.70, 1.795), (0.70, 1.795)], GAP, rr_any)
    top_any = face_filter("top_any")
    sl.poly_cut("top", [(HOOD["u_rear"], -HOOD["x"] - 0.01), (HOOD["u_rear"], HOOD["x"] + 0.01)], GAP, top_any)
    front_any = face_filter("front")
    sl.poly_cut("front", [(-0.95, HOOD["z_front"]), (0.95, HOOD["z_front"])], GAP, front_any)
    ws_out, ws_in = windshield_outlines()
    wsf = face_filter("ws")
    sl.poly_cut("front", ws_out + [ws_out[0]], 0.0, wsf, margin=0.02)
    sl.poly_cut("front", ws_in + [ws_in[0]], 0.0, wsf, margin=0.02)


# ---------------------------------------------------------------------------
# Classification


def classify(bm):
    """Return (faces, region names array) after cuts; region 'delete' is removed."""
    faces, cents = M.face_arrays(bm)
    n = M.sdf_vertex_normals(S.body, cents)
    u, x, z = M.to_body(cents)
    ax = np.abs(x)
    nx, nu, nz = n[:, 0], n[:, 1], n[:, 2]
    region = np.array(["BODY_0000_body_shell"] * len(faces), dtype=object)
    done = np.zeros(len(faces), bool)

    def put(mask, name):
        nonlocal done
        m = mask & ~done
        region[m] = name
        done |= m

    # gap strips
    gap = np.zeros(len(faces), bool)
    for side in ("L", "R"):
        sgn = 1 if side == "L" else -1
        on_side = (x * sgn > 0.5) & (nx * sgn > 0.3)
        for name, pts, g in [(nm, p, gg) for nm, p, gg in side_cuts() if p is not None and gg > 0]:
            gap |= on_side & (M.dist_to_polyline(u, z, pts) < g / 2)
        if side == "L":
            gap |= on_side & (M.dist_to_polyline(u, z, FUEL_LID) < LAMP_GAP / 2)
        hood_side = (u < 0.52) & (z > 1.04) & ((nz > 0.3) | (nu < -0.3)) & (x * sgn > 0)
        gap |= hood_side & (np.abs(ax - HOOD["x"]) < GAP / 2) & (u < HOOD["u_rear"] + 0.03)
        topf = (nz > 0.3) & (z > 1.0) & (x * sgn > 0)
        gap |= topf & (np.abs(u - 0.50) < GAP / 2) & (ax > HOOD["x"] - 0.02)
        lampf = (x * sgn > 0.3) & (u < -0.4) & (np.abs(nz) < 0.75)
        gap |= lampf & (np.abs(z - HEADLAMP["z0"]) < LAMP_GAP / 2) & (ax > HEADLAMP["x_in"] - 0.1)
        gap |= lampf & (np.abs(ax - HEADLAMP["x_in"]) < LAMP_GAP / 2) & (z > 0.84) & (z < HEADLAMP["z1"] + 0.02)
        gap |= on_side & (M.dist_to_polyline(u, z, HEADLAMP_SIDE) < LAMP_GAP / 2)
        rlamp = (x * sgn > 0.6) & (u > 3.6) & (np.abs(nz) < 0.8)
        for zz in (TAILLAMP["z0"], TAILLAMP["z1"]):
            gap |= rlamp & (np.abs(z - zz) < LAMP_GAP / 2) & (ax > TAILLAMP["x_in"] - 0.05)
        rear = (nu > 0.25) & (u > 3.4)
        gap |= rear & (x * sgn > 0) & (np.abs(ax - TAILLAMP["x_in"]) < LAMP_GAP / 2) & (z > TAILLAMP["z0"] - 0.02) & (z < TAILLAMP["z1"] + 0.02)
        gap |= on_side & (np.abs(u - TAILLAMP["u_side"]) < LAMP_GAP / 2) & (z > TAILLAMP["z0"] - 0.02) & (z < TAILLAMP["z1"] + 0.02)
        door_outer, _, _ = back_outlines()
        gap |= rear & (x * sgn > 0) & (M.dist_to_polyline(ax, z, door_outer) < GAP / 2)
    rear = (nu > 0.25) & (u > 3.4)
    gap |= rear & (np.abs(x) < GAP / 2) & (z > 0.78) & (z < 1.83)
    gap |= rear & (np.abs(z - 0.80) < GAP / 2) & (ax < 0.80)
    gap |= rear & (np.abs(z - 1.795) < GAP / 2) & (ax < 0.70)
    topf = (nz > 0.3) & (z > 1.0)
    gap |= topf & (np.abs(u - HOOD["u_rear"]) < GAP / 2) & (ax < HOOD["x"] + 0.01)
    gap |= (nu < -0.3) & (np.abs(z - HOOD["z_front"]) < GAP / 2) & (u < -0.4)
    put(gap, "delete")

    # grille opening
    put((nu < -0.3) & (u < -0.6) & (ax < GRILLE["x"]) & (z > GRILLE["z0"]) & (z < GRILLE["z1"]), "delete")

    # windshield
    ws_out, ws_in = windshield_outlines()
    wsf = (nu < -0.3) & (nz > 0.4) & (z > 1.2)
    put(wsf & M.in_polygon(x, z, ws_in), "GLASS_5553_windshield_glass")
    put(wsf & M.in_polygon(x, z, ws_out), "seal:BODY_0000_body_shell")

    for side in ("L", "R"):
        sgn = 1 if side == "L" else -1
        on_side = (x * sgn > 0.5) & (nx * sgn > 0.3)
        upper = on_side & (z > 1.15)
        w = window_outlines()
        put(upper & M.in_polygon(u, z, w["fd"][1]), f"GLASS_6751_front_door_glass_{side}")
        put(upper & M.in_polygon(u, z, w["rd"][1]), f"GLASS_6755_rear_door_glass_{side}")
        put(upper & M.in_polygon(u, z, w["rq"][1]), f"GLASS_6755_rear_door_quarter_glass_{side}")
        put(upper & M.in_polygon(u, z, w["qw"][1]), f"GLASS_6152_quarter_window_glass_{side}")
        put(upper & M.in_polygon(u, z, w["fd"][0]), f"seal:DOOR_6751_front_door_{side}")
        put(upper & M.in_polygon(u, z, w["rd"][0]), f"seal:DOOR_6755_rear_door_{side}")
        put(upper & M.in_polygon(u, z, w["rq"][0]), f"seal:DOOR_6755_rear_door_{side}")
        put(upper & M.in_polygon(u, z, w["qw"][0]), "seal:BODY_0000_body_shell")
        door_outer, g_out, g_in = back_outlines()
        rear = (nu > 0.25) & (u > 3.4) & (x * sgn > 0)
        put(rear & M.in_polygon(ax, z, g_in), f"GLASS_6761_back_door_glass_{side}")
        put(rear & M.in_polygon(ax, z, g_out), f"seal:DOOR_6761_back_door_{side}")
        # lamps
        lamp = (x * sgn > 0.3) & (u < -0.4) & (np.abs(nz) < 0.75)
        u_side = np.interp(z, [p[1] for p in HEADLAMP_SIDE], [p[0] for p in HEADLAMP_SIDE])
        put(lamp & (z > HEADLAMP["z0"]) & (z < HEADLAMP["z1"]) & (ax > HEADLAMP["x_in"]) & (u < u_side),
            f"LIGHT_8101_headlamp_{side}")
        rl = (x * sgn > 0.6) & (u > 3.6) & (np.abs(nz) < 0.8)
        put(rl & (z > TAILLAMP["z0"]) & (z < TAILLAMP["z1"]) & (ax > TAILLAMP["x_in"]) & (u > TAILLAMP["u_side"]),
            f"LIGHT_8111_rear_combination_lamp_{side}")
        if side == "L":
            put(on_side & M.in_polygon(u, z, FUEL_LID), "BODY_0000_fuel_filler_lid")

    # hood
    hood = (ax < HOOD["x"]) & (((nz > 0.3) & (u < HOOD["u_rear"]) & (z > 1.0)) | ((nu < -0.3) & (z > HOOD["z_front"]) & (u < -0.4)))
    put(hood, "BODY_5353_hood")

    # doors and back doors
    for side in ("L", "R"):
        sgn = 1 if side == "L" else -1
        outer = (x * sgn > 0.66) & (nx * sgn > -0.2)
        fd_poly = [(0.632, DOOR_BOTTOM), (1.692, DOOR_BOTTOM), (1.692, DOOR_TOP), (A_PILLAR(DOOR_TOP), DOOR_TOP), (0.668, 1.27), (0.632, 1.232)]
        rd_poly = [(1.692, DOOR_BOTTOM), (2.42, DOOR_BOTTOM), (2.68, 0.86), (2.68, 1.08), (2.66, 1.16), (C_CUT(1.255), 1.255),
                   (C_CUT(DOOR_TOP), DOOR_TOP), (1.692, DOOR_TOP)]
        not_arch = np.hypot(u - C.U_REAR_AXLE, z - S.ARCH_Z) > REAR_ARCH_R
        put(outer & M.in_polygon(u, z, fd_poly), f"DOOR_6751_front_door_{side}")
        put(outer & not_arch & M.in_polygon(u, z, rd_poly), f"DOOR_6755_rear_door_{side}")
        bd_poly = [(0.0, 0.80), (0.785, 0.80), (0.785, 1.30), (0.66, 1.795), (0.0, 1.795)]
        rear = (nu > 0.25) & (u > 3.4) & (x * sgn > 0)
        put(rear & M.in_polygon(ax, z, bd_poly), f"DOOR_6761_back_door_{side}")
        # fenders
        fender = (x * sgn > 0) & (u < 0.632) & (z > 0.47) & (((nx * sgn > 0.3) & (ax > 0.6)) | ((nz > 0.3) & (ax > HOOD["x"]) & (u < 0.50)) |
                                                          ((nu < -0.3) & (ax > HEADLAMP["x_in"]) & (u < -0.4)))
        fender &= ~((u > 0.45) & (z < DOOR_BOTTOM))
        put(fender, f"BODY_5353_front_fender_{side}")
    return faces, region


# ---------------------------------------------------------------------------
# Object building

THICKNESS = {
    "BODY_5353_hood": (0.03, "paint_white"),
    "DOOR_6751_front_door": (0.07, "interior_plastic_grey"),
    "DOOR_6755_rear_door": (0.07, "interior_plastic_grey"),
    "DOOR_6761_back_door": (0.07, "interior_plastic_grey"),
    "BODY_5353_front_fender": (0.008, "underbody_black"),
    "BODY_0000_fuel_filler_lid": (0.006, "paint_white"),
    "BODY_0000_body_shell": (0.012, "interior_plastic_grey"),
    "LIGHT_8111_rear_combination_lamp": (0.05, "lamp_reflector"),
}

INSET = {"glass": 0.008, "seal": 0.003, "lamp": 0.002}


def thickness_for(key):
    for k, v in THICKNESS.items():
        if key == k or key.startswith(k + "_"):
            return v
    return None


def build_objects(bm, faces, region):
    """Create one object per part key from the classified faces."""
    bm.verts.ensure_lookup_table()
    vidx = {v: i for i, v in enumerate(bm.verts)}
    vco = np.array([v.co for v in bm.verts])
    groups = {}
    for f, r in zip(faces, region):
        if r == "delete":
            continue
        seal = r.startswith("seal:")
        key = r[5:] if seal else r
        groups.setdefault(key, []).append((f, seal))
    objs = {}
    for key, items in groups.items():
        objs[key] = make_part(key, items, vidx, vco)
    return objs


def material_plan(key):
    """Outer material for a part key and whether it is glass or lamp."""
    if key.startswith("GLASS_5553") or key.startswith("GLASS_6751"):
        return "glass_clear", "glass"
    if key.startswith("GLASS_"):
        return "glass_privacy", "glass"
    if key.startswith("LIGHT_8101"):
        return "lamp_lens_clear", "lamp"
    if key.startswith("LIGHT_8111"):
        return "lamp_lens_red", "lamp"
    return "paint_white", "panel"


def make_part(key, items, vidx, vco):
    outer_key, kind = material_plan(key)
    used = sorted({vidx[v] for f, _ in items for v in f.verts})
    remap = {old: new for new, old in enumerate(used)}
    co = vco[used].copy()
    nrm = M.sdf_vertex_normals(S.body, co)
    polys, mats = [], []
    seal_verts = set()
    mat_keys = [outer_key, "rubber_seal"]
    for f, seal in items:
        polys.append([remap[vidx[v]] for v in f.verts])
        if seal:
            mats.append(1)
            seal_verts.update(remap[vidx[v]] for v in f.verts)
        else:
            mats.append(0)
    # per face material refinements
    cents = np.array([co[p].mean(axis=0) for p in polys])
    u, x, z = M.to_body(cents)
    if key.startswith("LIGHT_8111"):
        mat_keys.append("lamp_lens_clear")
        clear = (z > TAILLAMP["clear"][0]) & (z < TAILLAMP["clear"][1])
        mats = [2 if c else m for m, c in zip(mats, clear)]
    if key == "BODY_0000_body_shell":
        mat_keys.append("underbody_black")
        ax = np.abs(x)
        fn = M.sdf_vertex_normals(S.body, cents)
        in_well = np.zeros(len(polys), bool)
        for uc in S.ARCHES:
            in_well |= (np.hypot(u - uc, z - S.ARCH_Z) < S.ARCH_R + 0.02) & (ax < S.side_w(z) - 0.02)
        floor = fn[:, 2] < -0.6
        mats = [2 if (w or fl) else m for m, w, fl in zip(mats, in_well, floor)]
    # insets: glass sinks into the frame, seals sit a little below paint
    if kind == "glass":
        co -= nrm * INSET["glass"]
    elif kind == "lamp":
        co -= nrm * INSET["lamp"]
    elif seal_verts:
        sv = np.array(sorted(seal_verts))
        co[sv] -= nrm[sv] * INSET["seal"]
    polys, _ = M.orient_polys(co, polys, lambda c: M.sdf_vertex_normals(S.body, c))
    thick = thickness_for(key)
    obj = M.mesh_from_faces(key, co, polys, mats, [MAT.get(k) for k in mat_keys])
    if thick is not None:
        thicken(obj, nrm, thick[0], thick[1], rim_key="lamp_housing" if kind == "lamp" else None)
    else:
        loops = []
        for p in obj.data.polygons:
            for li in p.loop_indices:
                loops.append(nrm[obj.data.loops[li].vertex_index])
        M.set_custom_normals(obj, loops)
    obj["partKey"] = key
    return obj


def thicken(obj, nrm, t, inner_key, rim_key=None):
    """Give a skin panel thickness t inward, with an inner surface and a rim, and custom normals."""
    me = obj.data
    nv = len(me.vertices)
    co = np.empty(nv * 3)
    me.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)
    polys = [list(p.vertices) for p in me.polygons]
    mats = [p.material_index for p in me.polygons]
    # boundary edges with orientation from their face
    edge_count = {}
    for p in polys:
        for a, b in zip(p, p[1:] + p[:1]):
            k = (min(a, b), max(a, b))
            edge_count[k] = edge_count.get(k, 0) + 1
    boundary = []
    for p, m in zip(polys, mats):
        for a, b in zip(p, p[1:] + p[:1]):
            if edge_count[(min(a, b), max(a, b))] == 1:
                boundary.append((a, b, m))
    inner_co = co - nrm * t
    all_co = np.vstack([co, inner_co])
    new_polys = list(polys)
    new_mats = list(mats)
    mat_list = [m.name for m in me.materials]
    if inner_key not in mat_list:
        mat_list.append(inner_key)
    inner_idx = mat_list.index(inner_key)
    rim_name = rim_key or mat_list[0]
    if rim_name not in mat_list:
        mat_list.append(rim_name)
    rim_idx = mat_list.index(rim_name)
    for p in polys:
        new_polys.append([i + nv for i in reversed(p)])
        new_mats.append(inner_idx)
    seal_idx = mat_list.index("rubber_seal") if "rubber_seal" in mat_list else None
    for a, b, m in boundary:
        new_polys.append([b, a, a + nv, b + nv])
        new_mats.append(seal_idx if (seal_idx is not None and m == seal_idx) else rim_idx)
    name = obj.name
    old_me = obj.data
    new_me = bpy.data.meshes.new(name)
    new_me.from_pydata([tuple(v) for v in all_co], [], new_polys)
    for k in mat_list:
        new_me.materials.append(MAT.get(k))
    new_me.polygons.foreach_set("material_index", np.asarray(new_mats, np.int32))
    new_me.update()
    obj.data = new_me
    bpy.data.meshes.remove(old_me)
    # custom normals: outer = field normal, inner = flipped, rim = flat
    loops = []
    n_outer = len(polys)
    for pi, p in enumerate(new_me.polygons):
        for li in p.loop_indices:
            vi = new_me.loops[li].vertex_index
            if pi < n_outer:
                loops.append(nrm[vi])
            elif pi < 2 * n_outer:
                loops.append(-nrm[vi - nv])
            else:
                loops.append(tuple(p.normal))
    M.set_custom_normals(obj, loops)


# ---------------------------------------------------------------------------


def headlamp_cavity_field(u, x, z):
    """Air pocket behind a left headlamp lens: 2 mm to 70 mm under the skin, inside the lamp outline."""
    b = S.body(u, x, z)
    d = np.maximum(b + 0.002, -(b + 0.07))
    u_side = np.interp(z, [p[1] for p in HEADLAMP_SIDE], [p[0] for p in HEADLAMP_SIDE])
    d = np.maximum(d, (HEADLAMP["x_in"] + 0.003) - x)
    d = np.maximum(d, (HEADLAMP["z0"] + 0.003) - z)
    d = np.maximum(d, z - (HEADLAMP["z1"] - 0.003))
    return np.maximum(d, u - (u_side - 0.003))


_CAVITY = {}


def headlamp_cavity(side):
    """Open bucket (back and side walls, facing into the lamp) as (co, polys) in Blender space."""
    if "L" not in _CAVITY:
        bm = M.sdf_to_bmesh(headlamp_cavity_field, ((-0.84, -0.55), (0.40, 1.0), (0.87, 1.11)), 0.004)
        bm.verts.ensure_lookup_table()
        co = np.array([v.co[:] for v in bm.verts])
        polys = [[v.index for v in f.verts] for f in bm.faces]
        bm.free()
        cents = np.array([co[p].mean(axis=0) for p in polys])
        u, x, z = M.to_body(cents)
        keep = S.body(u, x, z) < -0.0045  # drop the face that sits right behind the lens
        polys = [p[::-1] for p, k in zip(polys, keep) if k]  # flip so walls face into the pocket
        _CAVITY["L"] = (co, polys)
    co, polys = _CAVITY["L"]
    if side == "L":
        return co, polys
    co = co.copy()
    co[:, 0] *= -1.0
    return co, [p[::-1] for p in polys]


def headlamp_internals(obj, side):
    """Housing pocket, chrome reflector bowls and bulbs inside a headlamp (main beam plus the clear corner lamp)."""
    sgn = 1.0 if side == "L" else -1.0
    y_face = S.U_FRONT - HALF_WB
    pieces = [(*headlamp_cavity(side), "lamp_housing")]
    main_c = (sgn * 0.60, y_face + 0.018, 0.99)
    co, pl = M.bowl_arrays(main_c, (0.0, -1.0, 0.0), 0.078, 0.040)
    pieces.append((co, pl, "lamp_reflector"))
    co, pl = M.sphere_arrays((sgn * 0.60, y_face + 0.030, 0.99), 0.011)
    pieces.append((co, pl, "lamp_lens_clear"))
    ring_c = (sgn * 0.495, y_face + 0.016, 0.99)
    co, pl = M.bowl_arrays(ring_c, (0.0, -1.0, 0.0), 0.038, 0.022)
    pieces.append((co, pl, "lamp_reflector"))
    corner_axis = (sgn * 0.75, -0.66, 0.0)
    corner_c = (sgn * 0.835, -0.715 - HALF_WB, 0.99)
    co, pl = M.bowl_arrays(corner_c, corner_axis, 0.050, 0.030)
    pieces.append((co, pl, "lamp_reflector"))
    co, pl = M.sphere_arrays((sgn * 0.828, -0.708 - HALF_WB, 0.99), 0.009)
    pieces.append((co, pl, "lamp_lens_amber"))
    M.append_geometry(obj, pieces)


def bumper_inserts(obj, key):
    pieces = []
    if key.endswith("front_bumper"):
        face = C.U_FRONT_END - HALF_WB
        for x0, x1, z0, z1 in ((0.47, 0.79, 0.555, 0.668), (-0.79, -0.47, 0.555, 0.668), (-0.40, 0.40, 0.57, 0.655)):
            cx, cz, w, h = 0.5 * (x0 + x1), 0.5 * (z0 + z1), x1 - x0, z1 - z0
            co, pl = M.box_arrays((cx, face + 0.034, cz), (w, 0.006, h))
            pieces.append((co, pl, "plastic_black_matte"))
            for t in (1 / 3, 2 / 3):
                co, pl = M.box_arrays((cx, face + 0.020, z0 + t * h), (w - 0.004, 0.022, 0.009), bevel=0.002)
                pieces.append((co, pl, "plastic_black_matte"))
    else:
        face = C.U_REAR_END - HALF_WB
        for sgn in (1, -1):
            co, pl = M.box_arrays((sgn * 0.78, face - 0.001, 0.622), (0.16, 0.008, 0.038), bevel=0.003)
            pieces.append((co, pl, "lamp_lens_red"))
        co, pl = M.box_arrays((0.0, face + 0.02, 0.475), (0.075, 0.20, 0.07), bevel=0.006)
        pieces.append((co, pl, "underbody_black"))
        co, pl = M.box_arrays((0.0, face + 0.13, 0.49), (0.05, 0.10, 0.03), bevel=0.004)
        pieces.append((co, pl, "underbody_black"))
        co, pl = M.box_arrays((0.0, face + 0.165, 0.515), (0.022, 0.022, 0.03))
        pieces.append((co, pl, "chrome"))
        co, pl = M.sphere_arrays((0.0, face + 0.165, 0.548), 0.024, rings=10, segments=16)
        pieces.append((co, pl, "chrome"))
    M.append_geometry(obj, pieces)


def build(h=0.008, target_faces=130000, log=lambda *a: print(*a, flush=True)):
    """Build every body part. Returns {part key: object}."""
    import time
    t0 = time.time()
    bm = M.sdf_to_bmesh(S.body, ((-0.86, 4.0), (-1.0, 1.0), (0.40, 1.89)), h, target_faces=target_faces)
    log(f"body skin: marching cubes and decimation to {len(bm.faces)} faces in {time.time() - t0:.1f}s")
    M.untangle(bm, S.body, log=log)
    sl = Slicer(bm)
    apply_cuts(sl)
    log(f"body skin: cuts done, {len(bm.faces)} faces ({time.time() - t0:.1f}s)")
    faces, region = classify(bm)
    objs = build_objects(bm, faces, region)
    bm.free()
    for side in ("L", "R"):
        key = f"LIGHT_8101_headlamp_{side}"
        if key in objs:
            headlamp_internals(objs[key], side)
    log(f"body parts: {len(objs)} objects ({time.time() - t0:.1f}s)")
    return objs


def build_bumpers(h=0.007, target_faces=24000, log=lambda *a: print(*a, flush=True)):
    out = {}
    specs = {
        "BODY_5252_front_bumper": (S.front_bumper, ((-0.93, -0.30), (-1.0, 1.0), (0.40, 0.90))),
        "BODY_5253_rear_bumper": (S.rear_bumper, ((3.25, 4.01), (-1.0, 1.0), (0.45, 0.82))),
    }
    for key, (fn, bounds) in specs.items():
        bm = M.sdf_to_bmesh(fn, bounds, h, target_faces=target_faces)
        obj = M.bmesh_to_object(bm, key)
        bm.free()
        me = obj.data
        co = np.empty(len(me.vertices) * 3)
        me.vertices.foreach_get("co", co)
        co = co.reshape(-1, 3)
        polys, flipped = M.orient_polys(co, [list(p.vertices) for p in me.polygons], lambda c, f=fn: M.sdf_vertex_normals(f, c))
        obj.data = M.mesh_from_faces("_tmp", co, polys, None, []).data
        bpy.data.objects.remove(bpy.data.objects["_tmp"])
        bpy.data.meshes.remove(me)
        me = obj.data
        me.name = key
        nrm = M.sdf_vertex_normals(fn, co)
        me.materials.append(MAT.get("plastic_trim_grey"))
        loops = []
        for p in me.polygons:
            for li in p.loop_indices:
                loops.append(nrm[me.loops[li].vertex_index])
        M.set_custom_normals(obj, loops)
        bumper_inserts(obj, key)
        obj["partKey"] = key
        out[key] = obj
        log(f"{key}: {len(obj.data.polygons)} faces")
    return out
