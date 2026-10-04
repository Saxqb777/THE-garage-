"""Signed distance field for the LC100 stand in body (numpy only, no bpy).

All functions take arrays in body coordinates:
    u: metres behind the front axle (Blender Y = u minus WHEELBASE / 2)
    x: lateral metres (signed; the body is symmetric so most terms use abs(x))
    z: metres above the ground
and return the signed distance in metres (negative inside).
Numbers come from docs/reference-notes.md.
"""
import numpy as np

from blender.lib import conventions as C

U_FRONT = -0.815          # grille and headlamp plane; bumper reaches C.U_FRONT_END
U_REAR = 3.955            # back door skin; bumper reaches C.U_REAR_END
Z_FLOOR = 0.46            # underside of the body
HALF_W = C.BODY_HALF_WIDTH
ROOF = C.ROOF_HEIGHT

ARCH_R = 0.495            # wheel arch opening radius
ARCH_Z = C.WHEEL_CENTER_Z
ARCHES = (C.U_FRONT_AXLE, C.U_REAR_AXLE)
WELL_X = 0.52             # inner wall of the wheel wells

WS_BASE_U, WS_BASE_Z, WS_SLOPE = 0.545, 1.27, 1.20  # windshield: u = base + slope * (z minus base z)
GH_BASE_W, GH_BASE_Z, GH_TAN = 0.865, 1.25, 0.306   # greenhouse half width and tumblehome
BACK_LEAN = 0.42                                    # rear face leans forward this much per metre up, above BACK_LEAN_Z
BACK_LEAN_Z = 1.10


def smin(a, b, k):
    if k <= 0:
        return np.minimum(a, b)
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0.0, 1.0)
    return b * (1.0 - h) + a * h - k * h * (1.0 - h)


def smax(a, b, k):
    return -smin(-a, -b, k)


def softplus(t, k):
    """Smooth max(t, 0) with blend width k."""
    return 0.5 * (t + np.sqrt(t * t + k * k))


def belt_z(u):
    """Top of the lower body (the beltline ledge) along the cabin."""
    return 1.200 + 0.022 * (u - 0.6)


CREASE_Z = 0.80          # door crease; the body steps out below it
FLARE_OUT = 0.018        # how far the lower body and arch flares stand proud
FLARE_BAND = 0.085       # width of the flare band around each arch


def smoothstep(e0, e1, t):
    t = np.clip((t - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def flare(u, z):
    """Outward offset of the lower body: below the door crease and in a band round each arch."""
    s = smoothstep(CREASE_Z + 0.009, CREASE_Z - 0.009, z)
    for uc in ARCHES:
        r = np.sqrt((u - uc) ** 2 + (z - ARCH_Z) ** 2)
        s = np.maximum(s, smoothstep(ARCH_R + FLARE_BAND + 0.009, ARCH_R + FLARE_BAND - 0.009, r))
    return FLARE_OUT * s


def hood_z(u, ax):
    """Hood and fender tops: nearly flat, dipping down over the last 0.4 m to the grille."""
    crown = 0.012 * (1.0 - (ax / 0.82) ** 2)
    drop = 0.13 * np.clip((-0.40 - u) / 0.415, 0.0, 1.0) ** 2
    return 1.235 + 0.025 * (u + 0.5) + crown - drop


def top_z(u, ax):
    t = np.clip((u - 0.50) / 0.12, 0.0, 1.0)
    t = t * t * (3 - 2 * t)
    return hood_z(u, ax) * (1 - t) + belt_z(u) * t


def side_w(z):
    """Lower body half width: gently convex doors."""
    return HALF_W - 0.10 * (z - 0.78) ** 2


def gh_w(z):
    """Greenhouse half width at height z (tumblehome)."""
    return GH_BASE_W - GH_TAN * (z - GH_BASE_Z)


def windshield_u(z, ax):
    return WS_BASE_U + WS_SLOPE * (z - WS_BASE_Z) + 0.045 * (ax / 0.75) ** 2


def back_u(z):
    return U_REAR - BACK_LEAN * softplus(z - BACK_LEAN_Z, 0.06)


def roof_z(u, ax):
    front_drop = 0.03 * np.clip((1.6 - u) / 0.4, 0.0, 1.0)
    return ROOF - 0.035 * (ax / 0.72) ** 2 - front_drop


def rounded_rect_plan(u, ax, half_w, u_front, u_rear, r_front, r_rear):
    """2D rounded rectangle in plan; u_rear may vary with height (leaning rear face)."""
    cu = 0.5 * (U_FRONT + U_REAR)
    front = u < cu
    r = np.where(front, r_front, r_rear)
    qx = np.where(front, (u_front + r) - u, u - (u_rear - r))
    qy = ax - (half_w - r)
    outside = np.sqrt(np.maximum(qx, 0.0) ** 2 + np.maximum(qy, 0.0) ** 2)
    inside = np.minimum(np.maximum(qx, qy), 0.0)
    return outside + inside - r


def lower_body(u, ax, z):
    plan = rounded_rect_plan(u, ax, side_w(z) + flare(u, z), U_FRONT, back_u(z), 0.24, 0.14)
    d = smax(plan, Z_FLOOR - z, 0.045)
    return smax(d, z - top_z(u, ax), 0.028)


def greenhouse(u, ax, z):
    d_side = ax - gh_w(z)
    d_ws = (windshield_u(z, ax) - u) / np.sqrt(1 + WS_SLOPE ** 2)
    d_back = (u - back_u(z)) / np.sqrt(1 + BACK_LEAN ** 2)
    d_roof = z - roof_z(u, ax)
    d_prof = smax(smax(d_roof, d_ws, 0.08), d_back, 0.12)  # side profile with rounded roof ends
    d_plan = smax(smax(d_side, d_ws, 0.05), d_back, 0.16)  # plan with rounded A and D pillars
    d = smax(d_plan, d_prof, 0.08)
    return smax(d, 1.10 - z, 0.0)


def arch_lip(u, ax, z):
    """Small rolled lip around each arch opening."""
    d = np.full_like(u, 1e3)
    for uc in ARCHES:
        rad = np.sqrt((u - uc) ** 2 + (z - ARCH_Z) ** 2)
        lip = np.sqrt((rad - (ARCH_R + 0.014)) ** 2 + (ax - (side_w(z) + FLARE_OUT - 0.012)) ** 2) - 0.016
        lip = np.where(z > Z_FLOOR + 0.04, lip, 1e3)  # only where there is body behind it
        d = np.minimum(d, lip)
    return d


def wheel_wells(u, ax, z):
    d = np.full_like(u, 1e3)
    for uc in ARCHES:
        cyl = np.sqrt((u - uc) ** 2 + (z - ARCH_Z) ** 2) - ARCH_R
        d = np.minimum(d, smax(cyl, WELL_X - ax, 0.02))
    return d


def body(u, x, z):
    ax = np.abs(x)
    d = smin(lower_body(u, ax, z), greenhouse(u, ax, z), 0.012)
    d = smin(d, arch_lip(u, ax, z), 0.01)
    return smax(d, -wheel_wells(u, ax, z), 0.012)


def normals(fn, u, x, z, eps=1.5e-3):
    """Unit gradient of `fn` at the given points (outward surface normal)."""
    gu = fn(u + eps, x, z) - fn(u - eps, x, z)
    gx = fn(u, x + eps, z) - fn(u, x - eps, z)
    gz = fn(u, x, z + eps) - fn(u, x, z - eps)
    g = np.stack([gu, gx, gz], axis=-1)
    return g / np.maximum(np.linalg.norm(g, axis=-1, keepdims=True), 1e-12)


# Bumpers are separate parts with their own fields.

def front_bumper(u, x, z):
    ax = np.abs(x)
    # plan: rounded rectangle from U_FRONT_END back to u = -0.355 (hidden inside the body)
    half_len = 0.5 * (-0.355 - C.U_FRONT_END)
    centre = 0.5 * (-0.355 + C.U_FRONT_END)
    bulge = 0.012 * (1.0 - (ax / 0.95) ** 2)  # front face slightly convex
    rc = 0.30
    qx = np.abs(u - centre) - (half_len - rc) - np.where(u < centre, bulge - 0.012, 0.0)
    half_w = 0.972 - 0.06 * np.clip((0.62 - z) / 0.2, 0, 1) ** 2  # tucks in at the bottom
    qy = ax - (half_w - rc)
    plan = np.sqrt(np.maximum(qx, 0) ** 2 + np.maximum(qy, 0) ** 2) + np.minimum(np.maximum(qx, qy), 0) - rc
    d = smax(plan, z - 0.86, 0.035)
    d = smax(d, 0.43 - z, 0.06)
    # horizontal crease across the face
    crease = np.sqrt((z - 0.705) ** 2 + (u - (C.U_FRONT_END - 0.004)) ** 2) - 0.006
    d = smax(d, -crease, 0.004)
    # outer vents and centre intake recessed 35 mm
    for x0, x1, z0, z1 in ((0.47, 0.79, 0.555, 0.668), (-0.79, -0.47, 0.555, 0.668), (-0.40, 0.40, 0.57, 0.655)):
        bx = np.maximum(np.abs(x - 0.5 * (x0 + x1)) - 0.5 * (x1 - x0), np.abs(z - 0.5 * (z0 + z1)) - 0.5 * (z1 - z0))
        recess = smax(bx, u - (C.U_FRONT_END + 0.035), 0.0)
        d = smax(d, -recess, 0.006)
    d = smax(d, -wheel_wells(u, ax, z) - 0.008, 0.01)
    return smax(d, -(d + 0.03), 0.0)  # 30 mm shell


def rear_bumper(u, x, z):
    ax = np.abs(x)
    front_u = 3.30
    half_len = 0.5 * (C.U_REAR_END - front_u)
    centre = 0.5 * (C.U_REAR_END + front_u)
    rc = 0.17  # tight enough to wrap the body's rear corner with a 1 cm margin
    qx = np.abs(u - centre) - (half_len - rc)
    qy = ax - (0.972 - rc)
    plan = np.sqrt(np.maximum(qx, 0) ** 2 + np.maximum(qy, 0) ** 2) + np.minimum(np.maximum(qx, qy), 0) - rc
    d = smax(plan, z - 0.79, 0.02)
    d = smax(d, 0.49 - z, 0.05)
    # step pad grooves on top
    groove = np.abs(((u - 3.80) % 0.03) - 0.015) - 0.004
    pad = smax(groove, z - 0.788, 0.0)
    pad = smax(pad, ax - 0.55, 0.0)
    pad = smax(pad, 3.84 - u, 0.0)
    d = smax(d, -pad, 0.002)
    d = smax(d, -wheel_wells(u, ax, z) - 0.008, 0.01)
    return smax(d, -(d + 0.03), 0.0)
