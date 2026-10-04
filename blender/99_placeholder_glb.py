"""Crude LC100 blockout so the web app has a model to load before the real one exists.

Builds every part key in src/data/parts.m1.json from boxes, extruded side profiles
and lathed wheels, roughly where the real parts sit. Assemblies become Empties,
parenting follows the contract, hinged parts get their origin on the hinge line,
and each object carries partKey (plus hingeAxis and openDeg when hinged) as custom
properties. Exports a Draco compressed GLB to public/models/lc100_placeholder.glb.

Run from anywhere:  python3 blender/99_placeholder_glb.py

Blender space: metres, Z up, the car faces -Y, the vehicle's left side is +X.
Dimensions are written in car coordinates (x, u, z) where u is metres behind the
front axle; door and pillar stations were read off the rectified side photo.
"""
import math
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, REPO)

import bpy  # noqa: E402  (import bpy first, it sets up bmesh and mathutils)
import bmesh  # noqa: E402
from mathutils import Matrix, Vector  # noqa: E402

from blender.lib import conventions as C, materials, naming  # noqa: E402

OUT = os.path.join(REPO, "public", "models", "lc100_placeholder.glb")

HW = C.BODY_HALF_WIDTH
WZ = C.WHEEL_CENTER_Z
SILL = 0.46  # bottom edge of the doors and body sides
BELT = 1.24  # bottom edge of the side glass
GLASS_TOP = 1.775
TUMBLE = 0.16  # the glasshouse narrows by this much per metre above the belt
ARCH_F, ARCH_R = 0.47, 0.50  # wheel arch radii
U_FD = (0.64, 1.69)  # front door
U_RD = (1.71, 2.66)  # rear door
U_QW = (2.74, 3.40)  # quarter window
U_END = 3.93  # back of the body; the back doors sit on it
HEX = [(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]


def P(x, u, z):
    return Vector((x, C.y_from_u(u), z))


def glass_z(u):
    """Height of the windshield surface at station u."""
    return BELT + 0.01 + (u - 0.64) * (GLASS_TOP - BELT - 0.01) / (1.07 - 0.64)


class Geo:
    """World space geometry for one object; each primitive picks a material key."""

    def __init__(self):
        self.bm = bmesh.new()
        self.mats = []

    def faces(self, verts, faces, mat, smooth=False):
        if mat not in self.mats:
            self.mats.append(mat)
        vs = [self.bm.verts.new(v) for v in verts]
        for f in faces:
            face = self.bm.faces.new([vs[i] for i in f])
            face.material_index = self.mats.index(mat)
            face.smooth = smooth
        return self

    def box(self, x0, x1, u0, u1, z0, z1, mat):
        pts = [(x0, u0), (x1, u0), (x1, u1), (x0, u1)]
        return self.faces([P(x, u, z0) for x, u in pts] + [P(x, u, z1) for x, u in pts], HEX, mat)

    def hexa(self, bottom, top, mat):
        """Bottom and top quads as car points, same winding."""
        return self.faces([P(*p) for p in bottom + top], HEX, mat)

    def prism(self, profile, x0, x1, mat):
        """Extrude a (u, z) side profile across x."""
        n = len(profile)
        verts = [P(x0, u, z) for u, z in profile] + [P(x1, u, z) for u, z in profile]
        sides = [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
        return self.faces(verts, [tuple(range(n)), tuple(range(n, 2 * n))] + sides, mat)

    def bar(self, a, b, w, h, mat):
        """Box from Blender point a to b, w wide and h thick."""
        d = (b - a).normalized()
        side = d.cross(Vector((0, 0, 1)) if abs(d.z) < 0.9 else Vector((1, 0, 0))).normalized() * (w / 2)
        top = side.cross(d).normalized() * (h / 2)
        corners = [a - side - top, a + side - top, b + side - top, b - side - top,
                   a - side + top, a + side + top, b + side + top, b - side + top]
        return self.faces(corners, HEX, mat)

    def lathe(self, profile, matrix, mat, segments=40, smooth=True):
        """Revolve a closed (radius, axial) profile around local Z, placed by matrix."""
        n = len(profile)
        verts = [matrix @ Vector((r * math.cos(a), r * math.sin(a), h))
                 for a in (2 * math.pi * k / segments for k in range(segments)) for r, h in profile]
        faces = [(k * n + i, k * n + (i + 1) % n, (k + 1) % segments * n + (i + 1) % n, (k + 1) % segments * n + i)
                 for k in range(segments) for i in range(n)]
        return self.faces(verts, faces, mat, smooth)

    def oval(self, centre, facing, rx, rz, depth, mat):
        """Flat elliptic badge facing along a Blender axis."""
        rot = Vector((0, 0, 1)).rotation_difference(Vector(facing)).to_matrix().to_4x4()
        m = Matrix.Translation(centre) @ Matrix.Diagonal((rx, 1, rz, 1)) @ rot
        return self.lathe([(0.001, 0), (1, 0), (1, depth), (0.001, depth)], m, mat, 24, smooth=False)


def arch_profile(u0, u1, z0, z1a, z1b, wheel_u, r, n=18):
    """(u, z) outline of a side panel from z0 up to a top edge z1a..z1b, minus a wheel arch."""
    a0 = math.asin((z0 - WZ) / r)
    arc = [(wheel_u + r * math.cos(a), WZ + r * math.sin(a))
           for a in (math.pi - a0 + (2 * a0 - math.pi) * i / (n - 1) for i in range(n))]

    def on_arch(u):
        return u, WZ + math.sqrt(max(r * r - (u - wheel_u) ** 2, 0.0))

    pts = [(u0, z1a), on_arch(u0) if arc[0][0] <= u0 else (u0, z0)]
    pts += [p for p in arc if u0 < p[0] < u1]
    return pts + [on_arch(u1) if arc[-1][0] >= u1 else (u1, z0), (u1, z1b)]


# ---------------------------------------------------------------- part builders
# Each takes the side sign s (+1 left, -1 right) and returns (Geo, origin in Blender space).

def body_shell(_s):
    g = Geo()
    g.box(-0.62, 0.62, -0.80, 0.56, 0.50, 1.08, "body_cavity")  # engine bay
    g.box(-0.80, 0.80, -0.84, -0.78, 0.70, 1.10, "paint_white")  # front panel
    g.box(-0.82, 0.82, 0.56, 0.68, 1.14, BELT, "paint_white")  # cowl
    g.box(-0.86, 0.86, 0.62, U_END, 0.40, SILL, "underbody_black")  # floor pan
    g.box(-0.88, 0.88, U_END - 0.07, U_END, SILL, 0.64, "paint_white")  # rear panel
    g.box(-0.93, 0.93, 1.04, U_END, 1.785, C.ROOF_HEIGHT, "paint_white")  # roof
    for s in (1, -1):
        g.box(s * 0.84, s * 0.93, U_FD[0], 2.34, 0.36, 0.47, "underbody_black")  # sill
        g.prism(arch_profile(U_RD[1], U_END, SILL, BELT + 0.04, BELT + 0.06, C.WHEELBASE, ARCH_R),
                s * 0.88, s * HW, "paint_white")  # quarter panel
        g.prism(arch_profile(2.30, 3.40, SILL, 1.0, 1.0, C.WHEELBASE, ARCH_R + 0.02),
                s * 0.70, s * 0.88, "body_cavity")  # rear wheelhouse
        g.hexa([(s * 0.84, 0.60, BELT), (s * 0.93, 0.60, BELT), (s * 0.93, 0.68, BELT), (s * 0.84, 0.68, BELT)],
               [(s * 0.84, 1.06, 1.79), (s * 0.93, 1.06, 1.79), (s * 0.93, 1.14, 1.79), (s * 0.84, 1.14, 1.79)],
               "paint_white")  # A pillar
        g.box(s * 0.84, s * 0.93, 1.66, 1.74, BELT, 1.79, "paint_white")  # B pillar
        g.box(s * 0.84, s * 0.93, 2.62, U_QW[0], BELT, 1.79, "paint_white")  # C pillar
        g.box(s * 0.84, s * HW, U_QW[1], U_END, BELT, 1.79, "paint_white")  # D pillar
    return g, P(0, C.WHEELBASE / 2, 0.9)


def hood(_s):
    g = Geo().hexa([(-0.80, -0.80, 1.085), (0.80, -0.80, 1.085), (0.80, 0.56, 1.175), (-0.80, 0.56, 1.175)],
                   [(-0.80, -0.80, 1.12), (0.80, -0.80, 1.12), (0.80, 0.56, 1.21), (-0.80, 0.56, 1.21)],
                   "paint_white")
    return g, P(0, 0.56, 1.21)  # hinge along the rear edge


def front_bumper(_s):
    g = Geo().box(-0.95, 0.95, C.U_FRONT_END, -0.70, 0.48, 0.76, "paint_white")
    g.box(-0.86, 0.86, -0.88, -0.70, 0.40, 0.48, "plastic_trim_grey")
    for s in (1, -1):
        g.box(s * 0.86, s * 0.95, -0.70, -0.50, 0.48, 0.74, "paint_white")
    return g, P(0, -0.80, 0.6)


def rear_bumper(_s):
    g = Geo().box(-0.95, 0.95, 3.76, C.U_REAR_END, 0.44, 0.76, "plastic_trim_grey")
    for s in (1, -1):
        g.box(s * 0.86, s * 0.95, 3.40, 3.76, 0.46, 0.72, "plastic_trim_grey")
    return g, P(0, 3.87, 0.6)


def grille(_s):
    g = Geo().box(-0.46, 0.46, -0.86, -0.82, 0.78, 1.06, "plastic_black_gloss")
    for z in (0.80, 0.86, 0.92, 0.98):
        g.box(-0.46, 0.46, -0.875, -0.86, z, z + 0.018, "chrome")
    g.box(-0.48, 0.48, -0.875, -0.86, 1.045, 1.07, "chrome")
    return g, P(0, -0.86, 0.92)


def outer_mirror(s):
    g = Geo().box(s * 0.90, s * 0.95, 0.74, 0.80, 1.22, 1.28, "plastic_black_matte")
    g.box(s * 0.93, s * 1.15, 0.72, 0.86, 1.24, 1.40, "paint_white")
    g.box(s * 0.96, s * 1.14, 0.86, 0.865, 1.26, 1.38, "chrome")
    return g, P(s * 0.92, 0.76, 1.25)


def rear_door(s):
    g = Geo().prism(arch_profile(*U_RD, SILL, BELT, BELT, C.WHEELBASE, ARCH_R), s * 0.885, s * HW, "paint_white")
    g.box(s * 0.885, s * 0.91, 2.30, 2.34, BELT, GLASS_TOP, "plastic_black_gloss")  # glass divider
    return g, P(s * 0.91, U_RD[0], 0.85)  # hinge on the front vertical edge


def back_door(s):
    u0, u1 = U_END - 0.03, U_END + 0.015
    g = Geo().box(s * 0.004, s * 0.86, u0, u1, 0.64, BELT, "paint_white")
    g.box(s * 0.004, s * 0.86, u0, u1, 1.72, 1.78, "paint_white")
    g.box(s * 0.78, s * 0.86, u0, u1, BELT, 1.72, "paint_white")
    g.box(s * 0.004, s * 0.06, u0, u1, BELT, 1.72, "paint_white")
    return g, P(s * 0.86, U_END - 0.01, 1.1)  # hinge on the outer vertical edge


def side_glass(profile, mat):
    def build(s):
        u = sum(p[0] for p in profile) / len(profile)
        return Geo().prism(profile, s * 0.895, s * 0.905, mat), P(s * 0.9, u, 1.5)
    return build


def windshield(_s):
    g = Geo().hexa([(-0.84, 0.64, BELT + 0.01), (0.84, 0.64, BELT + 0.01), (0.84, 1.07, GLASS_TOP),
                    (-0.84, 1.07, GLASS_TOP)],
                   [(-0.84, 0.634, BELT + 0.016), (0.84, 0.634, BELT + 0.016), (0.84, 1.064, GLASS_TOP + 0.006),
                    (-0.84, 1.064, GLASS_TOP + 0.006)], "glass_clear")
    return g, P(0, 0.85, 1.5)


def headlamp(s):
    g = Geo().box(s * 0.48, s * 0.88, -0.82, -0.62, 0.84, 1.06, "lamp_housing")
    g.box(s * 0.52, s * 0.84, -0.835, -0.82, 0.87, 1.03, "lamp_reflector")
    g.box(s * 0.48, s * 0.88, -0.865, -0.835, 0.845, 1.055, "lamp_lens_clear")
    return g, P(s * 0.68, -0.80, 0.95)


def rear_lamp(s):
    g = Geo().box(s * 0.865, s * 0.955, U_END - 0.03, U_END + 0.02, 0.92, 1.22, "lamp_lens_red")
    g.box(s * 0.865, s * 0.955, U_END - 0.03, U_END + 0.02, 0.84, 0.92, "lamp_lens_amber")
    g.box(s * HW, s * 0.955, 3.75, U_END - 0.03, 0.92, 1.22, "lamp_lens_red")
    return g, P(s * 0.91, U_END, 1.03)


TIRE = [(0.205, -0.100), (0.214, -0.122), (0.262, -0.134), (0.330, -0.139), (0.372, -0.134), (0.390, -0.118),
        (C.TIRE_OUTER_RADIUS, -0.085), (C.TIRE_OUTER_RADIUS, 0.085), (0.390, 0.118), (0.372, 0.134),
        (0.330, 0.139), (0.262, 0.134), (0.214, 0.122), (0.205, 0.100)]
RIM = [(0.002, 0.050), (0.055, 0.052), (0.065, 0.040), (0.150, 0.048), (0.185, 0.060), (0.200, 0.092),
       (0.222, 0.100), (0.222, 0.108), (0.205, 0.108), (0.196, 0.098), (0.192, -0.095), (0.215, -0.100),
       (0.215, -0.108), (0.185, -0.108), (0.180, -0.090), (0.070, 0.020), (0.002, 0.020)]


def wheel(axle, profile, mat):
    def build(s):
        centre = Vector(C.wheel_centres()[f"{axle}_{'L' if s > 0 else 'R'}"])
        m = Matrix.Translation(centre) @ Matrix.Rotation(s * math.pi / 2, 4, "Y")  # local +Z points outboard
        return Geo().lathe(profile, m, mat, 48), centre
    return build


def front_wiper(blade):
    def build(s):
        x0 = 0.30 if s > 0 else -0.25
        if blade:
            z = glass_z(0.70) + 0.01
            a, b = P(x0 - 0.02, 0.70, z), P(x0 - 0.56, 0.70, z)
            return Geo().bar(a, b, 0.012, 0.012, "rubber_seal"), (a + b) / 2
        a = P(x0, 0.60, 1.24)
        return Geo().bar(a, P(x0 - 0.45, 0.69, glass_z(0.69) + 0.025), 0.018, 0.012, "plastic_black_matte"), a
    return build


def rear_wiper(blade):
    def build(s):
        if blade:
            a, b = P(s * 0.72, U_END + 0.012, 1.30), P(s * 0.24, U_END + 0.012, 1.30)
            return Geo().bar(a, b, 0.012, 0.012, "rubber_seal"), (a + b) / 2
        a = P(s * 0.70, U_END + 0.02, 1.27)
        return Geo().bar(a, P(s * 0.30, U_END + 0.02, 1.31), 0.016, 0.012, "plastic_black_matte"), a
    return build


def instrument_panel(_s):
    g = Geo().box(-0.84, 0.84, 0.70, 1.08, 0.86, 1.18, "interior_plastic_grey")
    g.box(-0.14, 0.14, 1.08, 1.25, 0.70, 1.10, "interior_plastic_grey")
    g.box(0.22, 0.52, 1.08, 1.09, 1.06, 1.15, "emissive_dial")  # LHD cluster
    return g, P(0, 0.9, 1.0)


def steering_wheel(_s):
    centre = P(0.37, 1.22, 1.06)  # LHD
    axis = Vector((0, math.cos(math.radians(25)), math.sin(math.radians(25))))  # towards the driver
    m = Matrix.Translation(centre) @ Vector((0, 0, 1)).rotation_difference(axis).to_matrix().to_4x4()
    ring = [(0.19 + 0.016 * math.cos(t), 0.016 * math.sin(t)) for t in (2 * math.pi * i / 10 for i in range(10))]
    g = Geo().lathe(ring, m, "plastic_black_matte")
    g.lathe([(0.001, -0.03), (0.06, -0.03), (0.06, 0.02), (0.001, 0.02)], m, "plastic_black_matte", 20)
    for tip in ((0.18, 0, 0), (-0.18, 0, 0), (0, 0.18, 0)):  # local +Y is down the wheel
        g.bar(centre, m @ Vector(tip), 0.04, 0.015, "plastic_black_matte")
    g.bar(centre - axis * 0.04, centre - axis * 0.32, 0.06, 0.06, "plastic_black_matte")  # column
    return g, centre


def front_seat(s):
    g = Geo().box(s * 0.20, s * 0.60, 1.60, 2.00, SILL, 0.56, "interior_cloth_grey")
    g.box(s * 0.14, s * 0.66, 1.55, 2.05, 0.56, 0.70, "interior_cloth_grey")
    g.hexa([(s * 0.14, 2.02, 0.70), (s * 0.66, 2.02, 0.70), (s * 0.66, 2.14, 0.70), (s * 0.14, 2.14, 0.70)],
           [(s * 0.14, 2.12, 1.38), (s * 0.66, 2.12, 1.38), (s * 0.66, 2.22, 1.38), (s * 0.14, 2.22, 1.38)],
           "interior_cloth_grey")
    g.box(s * 0.28, s * 0.52, 2.13, 2.21, 1.40, 1.60, "interior_cloth_grey")
    return g, P(s * 0.40, 1.85, 0.6)


def rear_seat(_s):
    g = Geo().box(-0.68, 0.68, 2.35, 2.80, SILL, 0.58, "interior_cloth_grey")
    g.box(-0.68, 0.68, 2.30, 2.80, 0.58, 0.74, "interior_cloth_grey")
    g.hexa([(-0.68, 2.78, 0.74), (0.68, 2.78, 0.74), (0.68, 2.92, 0.74), (-0.68, 2.92, 0.74)],
           [(-0.68, 2.90, 1.34), (0.68, 2.90, 1.34), (0.68, 3.02, 1.34), (-0.68, 3.02, 1.34)],
           "interior_cloth_grey")
    return g, P(0, 2.6, 0.7)


def simple_box(x0, x1, u0, u1, z0, z1, mat):
    """Small single box parts; the origin sits on the box centre, mirrored for right side parts."""
    def build(s):
        g = Geo().box(s * x0, s * x1, u0, u1, z0, z1, mat)
        return g, P(s * (x0 + x1) / 2, (u0 + u1) / 2, (z0 + z1) / 2)
    return build


# keyed by the part name from naming.parse (key without system, group code and side)
BUILDERS = {
    "body_shell": body_shell,
    "hood": hood,
    "front_fender": lambda s: (Geo().prism(arch_profile(-0.84, U_FD[0], SILL, 1.10, 1.22, 0.0, ARCH_F),
                                           s * 0.80, s * HW, "paint_white"), P(s * 0.87, -0.1, 0.9)),
    "front_bumper": front_bumper,
    "rear_bumper": rear_bumper,
    "radiator_grille": grille,
    "outer_mirror": outer_mirror,
    "fuel_filler_lid": simple_box(HW, HW + 0.006, 3.22, 3.42, 1.03, 1.20, "paint_white"),
    "mudguard_front": simple_box(0.74, 0.93, 0.48, 0.50, 0.20, SILL + 0.01, "plastic_black_matte"),
    "mudguard_rear": simple_box(0.74, 0.93, 3.36, 3.38, 0.22, SILL + 0.01, "plastic_black_matte"),
    "front_door": lambda s: (Geo().box(s * 0.885, s * HW, *U_FD, SILL, BELT, "paint_white"),
                             P(s * 0.91, U_FD[0], 0.85)),  # hinge on the front vertical edge
    "rear_door": rear_door,
    "back_door": back_door,
    "front_door_outside_handle": simple_box(HW, HW + 0.018, 1.40, 1.58, 1.07, 1.11, "chrome"),
    "rear_door_outside_handle": simple_box(HW, HW + 0.018, 2.36, 2.54, 1.07, 1.11, "chrome"),
    "windshield_glass": windshield,
    "front_door_glass": side_glass([(0.70, BELT + 0.01), (1.64, BELT + 0.01), (1.64, GLASS_TOP), (1.14, GLASS_TOP)],
                                   "glass_clear"),
    "rear_door_glass": side_glass([(1.76, BELT + 0.01), (2.30, BELT + 0.01), (2.30, GLASS_TOP), (1.76, GLASS_TOP)],
                                  "glass_privacy"),
    "rear_door_quarter_glass": side_glass([(2.34, BELT + 0.01), (2.60, BELT + 0.01), (2.60, GLASS_TOP),
                                           (2.34, GLASS_TOP)], "glass_privacy"),
    "quarter_window_glass": side_glass([(U_QW[0], BELT + 0.05), (U_QW[1], BELT + 0.06), (U_QW[1], 1.66),
                                        (3.30, GLASS_TOP), (U_QW[0], GLASS_TOP)], "glass_privacy"),
    "back_door_glass": simple_box(0.06, 0.78, U_END - 0.015, U_END - 0.005, BELT, 1.72, "glass_privacy"),
    "headlamp": headlamp,
    "rear_combination_lamp": rear_lamp,
    "side_turn_signal_lamp": simple_box(HW, HW + 0.012, 0.50, 0.56, 1.07, 1.10, "lamp_lens_amber"),
    "disc_wheel_front": wheel("front", RIM, "alloy_wheel"),
    "disc_wheel_rear": wheel("rear", RIM, "alloy_wheel"),
    "tire_front": wheel("front", TIRE, "rubber_tire"),
    "tire_rear": wheel("rear", TIRE, "rubber_tire"),
    "front_emblem": lambda s: (Geo().oval(P(0, -0.885, 0.93), (0, -1, 0), 0.07, 0.045, 0.012, "chrome"),
                               P(0, -0.885, 0.93)),
    "back_door_emblem": lambda s: (Geo().oval(P(-0.18, U_END + 0.015, 1.06), (0, 1, 0), 0.06, 0.04, 0.01, "chrome"),
                                   P(-0.18, U_END + 0.015, 1.06)),
    "back_door_name_plate": simple_box(0.25, 0.60, U_END + 0.015, U_END + 0.022, 1.10, 1.13, "chrome"),
    "grade_badge": simple_box(-0.70, -0.55, U_END + 0.015, U_END + 0.022, 0.95, 0.98, "chrome"),
    "quarter_badge": simple_box(HW, HW + 0.006, 3.46, 3.72, 1.21, 1.24, "chrome"),
    "front_wiper_arm": front_wiper(blade=False),
    "front_wiper_blade": front_wiper(blade=True),
    "rear_wiper_arm": rear_wiper(blade=False),
    "rear_wiper_blade": rear_wiper(blade=True),
    "instrument_panel": instrument_panel,
    "steering_wheel": steering_wheel,
    "front_seat": front_seat,
    "rear_seat": rear_seat,
    "floor_carpet": simple_box(-0.84, 0.84, 0.66, 3.90, SILL, 0.48, "interior_carpet"),
}


def make_object(key, geo, origin, tumble):
    if tumble:  # lean the glasshouse inwards above the belt
        for v in geo.bm.verts:
            v.co.x *= 1 - max(v.co.z - BELT, 0) * TUMBLE / HW
    bmesh.ops.recalc_face_normals(geo.bm, faces=geo.bm.faces)
    for v in geo.bm.verts:
        v.co -= origin
    mesh = bpy.data.meshes.new(key)
    geo.bm.to_mesh(mesh)
    geo.bm.free()
    for m in geo.mats:
        mesh.materials.append(materials.get(m))
    obj = bpy.data.objects.new(key, mesh)
    obj.location = origin
    return obj


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    contract = naming.load_contract()
    problems = naming.validate_contract(contract)
    if problems:
        raise SystemExit("contract problems:\n  " + "\n  ".join(problems))

    objs = {}
    for key, part in contract.items():
        parsed = naming.parse(key)
        s = -1 if parsed["side"] == "R" else 1
        if part["kind"] == "assembly":
            obj = bpy.data.objects.new(key, None)
            obj.empty_display_size = 0.3
            obj.location = C.wheel_centres()["_".join(key.split("_")[-2:])]
        else:
            geo, origin = BUILDERS[parsed["name"]](s)
            obj = make_object(key, geo, origin, tumble=parsed["name"] != "outer_mirror")
        obj["partKey"] = key
        if part.get("hinge"):
            obj["hingeAxis"] = [float(v) for v in part["hinge"]["axis"]]
            obj["openDeg"] = float(part["hinge"]["openDeg"])
        bpy.context.scene.collection.objects.link(obj)
        objs[key] = obj

    world = {k: o.location.copy() for k, o in objs.items()}
    for key, part in contract.items():
        if part["parent"]:
            objs[key].parent = objs[part["parent"]]
            objs[key].location = world[key] - world[part["parent"]]

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    bpy.ops.export_scene.gltf(
        filepath=OUT,
        export_format="GLB",
        export_yup=True,
        export_extras=True,
        export_apply=True,
        export_texcoords=False,
        export_draco_mesh_compression_enable=True,
        export_draco_mesh_compression_level=6,
    )
    meshes = [o.data for o in objs.values() if o.type == "MESH"]
    for m in meshes:
        m.calc_loop_triangles()
    tris = sum(len(m.loop_triangles) for m in meshes)
    print(f"wrote {OUT}: {len(objs)} objects, {len(meshes)} meshes, {tris} triangles, "
          f"{os.path.getsize(OUT) / 1024:.0f} KB")


if __name__ == "__main__":
    main()
