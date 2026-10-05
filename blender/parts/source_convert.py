"""Convert the CC BY LC100 2006 source model (VXR, as downloaded) into our named GXR parts.

convert() returns {part key: object}. Steps:
  1. import and normalise (blender/source_lc100.py), drop junk objects and the VXR extras
  2. plane cuts along the measured panel gaps so no triangle straddles a part boundary
  3. classify every face of every kept source object into a part key and a material key
  4. rebuild one object per part key (UVs kept), remap materials, barn door frames
Regions and lines live in blender/parts/source_regions.py.
"""
import os
import sys

import bpy
import bmesh
import numpy as np
from mathutils import Vector

from blender import source_lc100 as SRC
from blender.lib import materials as MAT
from blender.lib import meshing as M
from blender.parts import source_regions as R

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

PAINT = "flakka.2006.12"
CLADDING = ("flakka.2006.13", "flakka_12")
GREY = "flakka.2006.2"
BLACK = "flakka.2006.3"
TRIMS = "flakka.2006.4"
CHROME = "flakka.2006.5"
LAMPS = "flakka.2006.17"
GLASS_OUT = "boz7fa_land2004.028"   # windshield and lamp lenses
GLASS_TINT = "flakka.2006.14"       # side glass, rear glass, sunroof
CLADDING_PAINT = "vehicle_generic_smallspecmap__PAINT_3_"

DELETE_OBJECTS = {
    "TextPlus001",  # the modder's signature under the GXR badge
    "gnh", "Phoneee", "sticker", "Plane.0012", "asciii", "asciidd", "Box001", "flashcube", "TASK_FLASH",
    "flakka.2006.25", "flakka_sh3artoyota", "Plane001", "GEO_Mirror",
}
DELETE_PREFIXES = ("Tube", "wheel", "WHEEL_", "TASK_", "STEER_", "Object026", "Object027", "steeringwheel")
# wheel and steering empties go; the steering wheel meshes themselves are kept by name below
KEEP_EVEN_IF_PREFIXED = {"steeringwheel_SUB0_SUB0", "steeringwheel_SUB0_SUB1", "steeringwheel_SUB0_SUB2",
                         "Object026_SUB0_SUB0", "Object026_SUB0_SUB1", "Object027_SUB0_SUB0", "Object027_SUB0_SUB1"}

INTERIOR_DASH = {"flakka.2006.9", "flakka.2006.7", "flakka_mkyfat", "flakka.2006.24", "flakka.2006.26", "Object02844",
                 "stationrace.024", "Object026_SUB0_SUB0", "Object026_SUB0_SUB1", "Object027_SUB0_SUB0", "Object027_SUB0_SUB1"}
STEERING = {"steeringwheel_SUB0_SUB0", "steeringwheel_SUB0_SUB1", "steeringwheel_SUB0_SUB2"}
SEATS = "flakka.2006.11"
CARPET = "flakka.2006.8"
SIDE_CUT_OBJECTS = {PAINT, GREY, BLACK, TRIMS, CHROME, "flakka.2006.9", *CLADDING}
INTERIOR = {SEATS, CARPET, *INTERIOR_DASH, *STEERING}
BACK_DOOR_GAP = 0.003

# source material name -> our material key (region rules below can override)
MATERIAL_MAP = {
    "Material #32": "tex_paint_white", "Material #41": "tex_paint_white", "SABA_2179": "tex_side_step",
    CLADDING_PAINT: "plastic_trim_grey", "grey": "plastic_trim_grey", "cromo": "plastic_trim_grey",
    "black.001": "plastic_black_matte", "Material.001": "plastic_black_matte", "Material.002": "plastic_black_matte",
    "tire69": "plastic_black_matte", "rimmidle": "plastic_black_matte", "Material.006": "plastic_black_matte",
    "Material #38": "plastic_black_matte",
    "bl_lt.001": "interior_plastic_grey", "Material #34": "interior_plastic_grey", "Material #42": "interior_plastic_grey",
    "Material #43": "interior_plastic_grey", "Material #35": "interior_plastic_grey", "Material #37": "interior_plastic_grey",
    "rim": "chrome", "1245": "chrome", "EXT_Mirror": "chrome", "Material #39": "chrome", "Material #40": "chrome",
    "Material #25": "chrome", "Material #73": "chrome",
    "Material": "glass_clear", "glass": "glass_privacy", "glass_tail_light": "lamp_lens_red", "Orange_Glass": "lamp_lens_amber",
    "flsh": "lamp_lens_amber", "Material.003": "lamp_lens_red",
    "vehicle_generic_tyrewallblack.001": "rubber_seal", "WINTER_TIRE_LC100": "rubber_tire",
    "vehicle_generic_detail2": "underbody_black",
    # textured keepers (built from the source materials in textured_materials())
    "ligh": "tex_lamp_front", "vehiclelights128": "tex_lamp_rear", "LCX100LeatherSeats": "tex_seat_cloth",
    "LCX100DOLMATKOZHAZ.001": "tex_dash", "LCX100DOLMATTXT.001": "tex_interior_detail",
    "vehicle_generic_smallspecmap.001": "tex_cluster",
}
TEXTURED = {"tex_paint_white": ("Material #32", None), "tex_side_step": ("SABA_2179", None), "tex_lamp_front": ("ligh", None), "tex_lamp_rear": ("vehiclelights128", None),
            "tex_seat_cloth": ("LCX100LeatherSeats", "grey_cloth"), "tex_dash": ("LCX100DOLMATKOZHAZ.001", None),
            "tex_interior_detail": ("LCX100DOLMATTXT.001", None), "tex_cluster": ("vehicle_generic_smallspecmap.001", None)}


# ---------------------------------------------------------------------------
# geometry helpers

def line_y(line, z):
    zs = [p[1] for p in line]
    ys = [p[0] for p in line]
    return float(np.interp(z, zs, ys))


def inbox(c, box, side=1.0):
    x0, x1, y0, y1, z0, z1 = box
    x = c[0] * side
    return x0 <= x <= x1 and y0 <= c[1] <= y1 and z0 <= c[2] <= z1


def side_of(c):
    return "L" if c[0] >= 0 else "R"


def sgn(c):
    return 1.0 if c[0] >= 0 else -1.0


def in_outline(ax, z, outline):
    return bool(M.in_polygon(np.array([ax]), np.array([z]), outline)[0])


# ---------------------------------------------------------------------------
# materials

_tex_cache = {}


def grey_cloth_image(img):
    """Desaturated, darker copy of the leather texture: reads as grey cloth but keeps the seams."""
    from PIL import Image, ImageOps
    src = bpy.path.abspath(img.filepath)
    out = os.path.join(REPO, "reference", "model", "lc100_2006_cc_by", "derived_seat_grey_cloth.png")
    if not os.path.exists(out):
        im = Image.open(src).convert("RGB")
        g = ImageOps.grayscale(im)
        g = g.point(lambda v: int(40 + v * 0.42))
        g.convert("RGB").save(out)
    new = bpy.data.images.load(out)
    return new


def textured_material(key):
    """Our named copy of a source material that keeps its texture."""
    if key in _tex_cache:
        return _tex_cache[key]
    src_name, variant = TEXTURED[key]
    src = bpy.data.materials.get(src_name)
    mat = src.copy()
    mat.name = key
    nt = mat.node_tree
    bsdf = next((n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"), None)
    if bsdf is not None:
        bsdf.inputs["Metallic"].default_value = 0.0
        bsdf.inputs["Roughness"].default_value = 0.9 if key in ("tex_seat_cloth", "tex_interior_detail") else 0.45
        if key == "tex_paint_white":
            bsdf.inputs["Roughness"].default_value = 0.3
            bsdf.inputs["Coat Weight"].default_value = 1.0
            bsdf.inputs["Coat Roughness"].default_value = 0.04
        bsdf.inputs["Specular IOR Level"].default_value = 0.3
        for inp in ("Emission Strength",):
            if inp in bsdf.inputs:
                bsdf.inputs[inp].default_value = 0.0
    if variant == "grey_cloth":
        for n in nt.nodes:
            if n.type == "TEX_IMAGE" and n.image:
                n.image = grey_cloth_image(n.image)
    # drop any alpha / transparency links the FBX importer wired up
    for n in nt.nodes:
        if n.type == "BSDF_PRINCIPLED":
            for l in list(n.inputs["Alpha"].links):
                nt.links.remove(l)
            n.inputs["Alpha"].default_value = 1.0
    mat.blend_method = "OPAQUE"
    _tex_cache[key] = mat
    return mat


def material_for(key):
    if key in TEXTURED:
        return textured_material(key)
    return MAT.get(key)


# ---------------------------------------------------------------------------
# classification: returns (part key, material key) or None to delete the face

def classify(src, smat, c, n, island=10**9):
    """island: triangle count of the connected island this face belongs to (paint body only)."""
    x, y, z = c
    ax = abs(x)
    s = side_of(c)
    sg = sgn(c)
    base = MATERIAL_MAP.get(smat, "plastic_black_matte")

    # VXR extras and mod leftovers
    if src in CLADDING:
        # the running board stays (set 2 reference car has it); the two tone door band above it goes
        if ax > R.CLADDING_STEP_X or z < 0.52:
            return f"BODY_0000_side_step_{s}", "tex_side_step"
        return None
    if src == TRIMS and (inbox(c, R.REAR_WIPER) or inbox(c, R.FRONT_WIPERS)):
        return None
    exterior = src not in INTERIOR
    if y < -1.9 and 0.40 < ax < 0.97 and 1.0 < z < 1.14:
        if src == BLACK:
            return None  # aftermarket black headlamp eyebrows glued on the hood lip
        if src == PAINT:
            base = "paint_white"  # hood lip over the lamps: the source texture is dark there, the real car is white
    if src == "gnh":
        return "BODY_0000_body_shell", "tex_paint_white"  # rear lip spoiler, as on the set 2 reference car
    if src == PAINT and 0.28 < z < 0.52 and ax > 0.80 and -1.0 < y < 0.98:
        return None  # thick painted board under the doors; the slimmer step from the cladding object stays
    if src == GREY and ax > 0.95 and 0.64 < z < 0.74 and -1.0 < y < 1.3:
        return None  # VXR lower door mouldings
    if src == CHROME and inbox(c, R.REAR_GARNISH):
        base = "chrome"  # the tailgate garnish with its LAND CRUISER lettering stays, as on the set 2 car
    if exterior and src != PAINT and ax > 0.95 and 0.73 < z < 0.79 and -1.05 < y < 1.1:
        return None  # top strip of the VXR lower mouldings

    # lamps
    if exterior and inbox(c, R.HEADLAMP, sg):
        if src == GLASS_OUT:
            mk = "lamp_lens_clear"
        elif src == PAINT or src == BLACK:
            mk = "lamp_housing"
        elif src == "lightfront":
            mk = "lamp_reflector"
        else:
            mk = base
        return f"LIGHT_8101_headlamp_{s}", mk
    if src in ("left1", "right1"):
        return f"LIGHT_8101_headlamp_{s}", "lamp_lens_amber"
    if exterior and inbox(c, R.TAILLAMP, sg):
        if src == GLASS_OUT:
            mk = "lamp_lens_clear"
        elif src == PAINT or src == BLACK:
            mk = "lamp_housing"
        elif src == "flakka.2006.18":
            mk = "lamp_lens_red"
        else:
            mk = base
        return f"LIGHT_8105_rear_combination_lamp_{s}", mk
    if src in ("left2", "right2", "lightback", "rear", "boz7fa_land2004.021"):
        return f"LIGHT_8105_rear_combination_lamp_{s}", base
    if src == "flakka.2006.21":
        return f"LIGHT_0000_side_turn_signal_lamp_{s}", "lamp_lens_amber"

    # front end
    if src == "flakka_sh3artoyota1":
        return "TRIM_0000_front_emblem", "chrome"
    if src in (GREY, CHROME, BLACK) and inbox(c, R.GRILLE):
        return "BODY_0000_radiator_grille", "plastic_black_gloss"
    if exterior and src != PAINT and y < R.FRONT_BUMPER_Y1 and z < R.BUMPER_Z1:
        mk = {GLASS_OUT: "lamp_lens_clear", BLACK: "plastic_black_matte", CHROME: "plastic_trim_grey"}.get(src, "plastic_trim_grey")
        if src == LAMPS:
            mk = base
        return "BODY_5201_front_bumper", mk
    if exterior and src != PAINT and y > R.REAR_BUMPER_Y0 and z < R.BUMPER_Z1:
        if src == "flakka.2006.10":
            return "BODY_0000_body_shell", "rubber_tire"
        mk = {"flakka.2006.18": "lamp_lens_red", BLACK: "plastic_black_matte"}.get(src, "plastic_trim_grey")
        return "BODY_5202_rear_bumper", mk

    # small parts on the sides
    if exterior and inbox(c, R.MIRROR, sg) and src in (PAINT, BLACK, "mirror2", "mirror3", GREY):
        # set 2 car: body colour housings; the sail base stays black
        mk = "chrome" if src in ("mirror2", "mirror3") else ("plastic_black_matte" if (src == BLACK or ax < 0.93) else "paint_white")
        return f"BODY_0000_outer_mirror_{s}", mk
    small = island < 3000  # the door skin is one big island, handles and badges are small ones
    if (src == CHROME or (src == PAINT and small)) and (inbox(c, R.HANDLE_FRONT, sg) or inbox(c, R.HANDLE_REAR, sg)):
        if src == CHROME and ax < 0.992:
            return None  # flat chrome backing plate behind the grip; the door skin is intact underneath
        which = "front" if inbox(c, R.HANDLE_FRONT, sg) else "rear"
        return f"DOOR_0000_{which}_door_outside_handle_{s}", "chrome"
    if src == PAINT and inbox(c, R.FUEL_LID):
        return "BODY_0000_fuel_filler_lid", "tex_paint_white"
    if src == PAINT and inbox(c, R.QUARTER_BADGE, sg):
        return f"TRIM_0000_quarter_badge_{s}", "chrome"
    if src in ("logogxr1", "TextPlus001"):
        return "TRIM_0000_grade_badge", "chrome"
    if src == PAINT and inbox(c, R.REAR_EMBLEM):
        return "TRIM_0000_back_door_emblem", "chrome"
    if src == "flakka.2006.23":
        if R.MUDGUARD_FRONT_Y[0] <= y <= R.MUDGUARD_FRONT_Y[1]:
            return f"BODY_0000_mudguard_front_{s}", "rubber_seal"
        if R.MUDGUARD_REAR_Y[0] <= y <= R.MUDGUARD_REAR_Y[1]:
            return f"BODY_0000_mudguard_rear_{s}", "rubber_seal"
        return "BODY_0000_body_shell", "underbody_black"

    # glass
    if src == GLASS_TINT:
        if inbox(c, R.SUNROOF):
            return "BODY_0000_body_shell", "paint_white"
        if inbox(c, R.REAR_GLASS):
            if ax < BACK_DOOR_GAP:
                return None
            return f"GLASS_6703_back_door_glass_{s}", "glass_privacy"
        if src == GLASS_TINT and z > 1.85 and y > 2.0:
            return "LIGHT_8105_rear_combination_lamp_L" if x >= 0 else "LIGHT_8105_rear_combination_lamp_R", "lamp_lens_red"
        if ax > R.DOOR_SIDE_X and z > 1.15:
            if y < line_y(R.B_LINE, z):
                return f"GLASS_6701_front_door_glass_{s}", "glass_clear"
            if y < R.REAR_DOOR_GLASS_SPLIT_Y:
                return f"GLASS_6702_rear_door_glass_{s}", "glass_privacy"
            if y < line_y(R.REAR_DOOR_LINE, z):
                return f"GLASS_6702_rear_door_quarter_glass_{s}", "glass_privacy"
            return f"GLASS_0000_quarter_window_glass_{s}", "glass_privacy"
        return "BODY_0000_body_shell", "glass_privacy"
    if src == GLASS_OUT and inbox(c, R.WINDSHIELD):
        return "GLASS_5601_windshield_glass", "glass_clear"

    # interior
    if src == SEATS:
        if y > R.SEAT_SPLIT_Y:
            return "INT_0000_rear_seat", base
        return f"INT_0000_front_seat_{s}", base
    if src in STEERING:
        return "INT_0000_steering_wheel", "interior_plastic_grey" if smat.startswith("Material #37") else base
    if src == CARPET:
        return "INT_0000_floor_carpet", base
    if src in INTERIOR_DASH and not (ax > 0.84 and z < 1.25):
        return "INT_0000_instrument_panel", base

    # back doors (barn doors): the tailgate skin and its frames, split by side with a real gap
    if y > R.BACK_DOOR_Y0 and in_outline(ax, z, R.BACK_DOOR_OUTLINE) and src in (PAINT, GREY, BLACK, TRIMS, CHROME):
        if ax < BACK_DOOR_GAP:
            return None
        return f"DOOR_6703_back_door_{s}", base

    # hood
    if src == PAINT and y < R.HOOD_REAR_Y and ax < R.HOOD_SIDE_X and z > R.HOOD_FRONT_Z:
        return "BODY_5301_hood", base

    # side doors: anything outboard of the drip rail between the gap lines
    if ax > R.DOOR_SIDE_X and R.DOOR_BOTTOM < z < 1.95 and src not in (SEATS, CARPET):
        if src in INTERIOR_DASH and ax < 0.84:
            return "INT_0000_instrument_panel", base
        a = line_y(R.A_LINE, z)
        b = line_y(R.B_LINE, z)
        r = line_y(R.REAR_DOOR_LINE, z)
        if a <= y < b:
            return f"DOOR_6701_front_door_{s}", base
        if b <= y < r:
            return f"DOOR_6702_rear_door_{s}", base
        if src == PAINT and y < a and z > 0.70 and ax > 0.44 and y > -2.6:
            return f"BODY_5301_front_fender_{s}", "tex_paint_white"
    if src in INTERIOR_DASH:
        return "INT_0000_instrument_panel", base
    if src == "flakka.2006.22":
        return "BODY_0000_body_shell", "underbody_black"
    if src == "flakka.2006.10":
        return "BODY_0000_body_shell", "rubber_tire"
    return "BODY_0000_body_shell", base


def island_sizes(bm):
    """Triangle count of the connected island of every face, indexed by face index."""
    bm.faces.ensure_lookup_table()
    n = len(bm.faces)
    parent = list(range(n))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for e in bm.edges:
        lf = e.link_faces
        if len(lf) > 1:
            r0 = find(lf[0].index)
            for f in lf[1:]:
                r = find(f.index)
                if r != r0:
                    parent[r] = r0
    counts = {}
    roots = [find(i) for i in range(n)]
    for i, r in enumerate(roots):
        counts[r] = counts.get(r, 0) + len(bm.faces[i].verts) - 2
    return [counts[r] for r in roots]


# ---------------------------------------------------------------------------
# cuts

def plane_cuts(bm):
    """Bisect faces along every part boundary. Only faces whose box crosses a boundary are touched."""
    cutter = M.Cutter(bm, lambda c: np.zeros((len(c), 3)))
    big = 9.0

    def line(view, pts, lo, hi):
        for co, no, _, _ in M.segment_planes(view, pts):
            cutter.cut(co, no, lo, hi)

    for side in (1.0, -1.0):
        def mirror(pts):
            return pts
        xlo, xhi = (0.45, big) if side > 0 else (-big, -0.45)
        for pts in (R.A_LINE, R.B_LINE, R.REAR_DOOR_LINE):
            for co, no, (a0, b0), (a1, b1) in M.segment_planes("side", [(y + 1.425, z) for y, z in pts]):
                lo = (xlo, min(a0, a1) - 1.425 - 0.02, min(b0, b1) - 0.02)
                hi = (xhi, max(a0, a1) - 1.425 + 0.02, max(b0, b1) + 0.02)
                cutter.cut(co, no, lo, hi)
        # hood side gaps and the drip rail
        cutter.cut((side * R.HOOD_SIDE_X, 0, 0), (1, 0, 0), (side * R.HOOD_SIDE_X - 0.01, -2.6, 0.9), (side * R.HOOD_SIDE_X + 0.01, R.HOOD_REAR_Y + 0.05, 1.5))
        cutter.cut((side * R.DOOR_SIDE_X, 0, 0), (1, 0, 0), (side * R.DOOR_SIDE_X - 0.01, -1.0, 1.55), (side * R.DOOR_SIDE_X + 0.01, 2.3, 2.0))
        # lamp boxes, mirror, handles, fuel lid, badges: axis aligned box edges
        for box in (R.HEADLAMP, R.TAILLAMP, R.MIRROR, R.HANDLE_FRONT, R.HANDLE_REAR, R.QUARTER_BADGE):
            box_cuts(cutter, box, side)
    box_cuts(cutter, R.FUEL_LID, 1.0)
    for box in (R.GRILLE, R.SUNROOF, R.REAR_EMBLEM, R.REAR_GARNISH):
        box_cuts(cutter, box, 1.0, mirrored=False)
    # hood rear and front edges
    cutter.cut((0, R.HOOD_REAR_Y, 0), (0, 1, 0), (-0.9, R.HOOD_REAR_Y - 0.01, 0.9), (0.9, R.HOOD_REAR_Y + 0.01, 1.6))
    cutter.cut((0, 0, R.HOOD_FRONT_Z), (0, 0, 1), (-0.9, -2.6, R.HOOD_FRONT_Z - 0.01), (0.9, -1.9, R.HOOD_FRONT_Z + 0.01))
    # barn door split (two planes leave a gap strip to delete) and the tailgate outline (rear view)
    for xv in (-BACK_DOOR_GAP, BACK_DOOR_GAP):
        cutter.cut((xv, 0, 0), (1, 0, 0), (xv - 0.01, R.BACK_DOOR_Y0, 0.7), (xv + 0.01, 2.7, 2.0))
    for side in (1.0, -1.0):
        pts = [(side * ax, z) for ax, z in R.BACK_DOOR_OUTLINE]
        for co, no, (a0, b0), (a1, b1) in M.segment_planes("front", pts):
            lo = (min(a0, a1) - 0.02, R.BACK_DOOR_Y0, min(b0, b1) - 0.02)
            hi = (max(a0, a1) + 0.02, 2.7, max(b0, b1) + 0.02)
            cutter.cut(co, no, lo, hi)
    # bumper top edges and the rear door glass split
    cutter.cut((0, 0, R.BUMPER_Z1), (0, 0, 1), (-1.1, -2.7, R.BUMPER_Z1 - 0.01), (1.1, R.FRONT_BUMPER_Y1, R.BUMPER_Z1 + 0.01))
    cutter.cut((0, 0, R.BUMPER_Z1), (0, 0, 1), (-1.1, R.REAR_BUMPER_Y0, R.BUMPER_Z1 - 0.01), (1.1, 2.7, R.BUMPER_Z1 + 0.01))
    cutter.cut((0, R.REAR_DOOR_GLASS_SPLIT_Y, 0), (0, 1, 0), (-1.1, R.REAR_DOOR_GLASS_SPLIT_Y - 0.01, 1.1), (1.1, R.REAR_DOOR_GLASS_SPLIT_Y + 0.01, 2.0))
    cutter.cut((0, 0, R.DOOR_BOTTOM), (0, 0, 1), (-1.1, -1.0, R.DOOR_BOTTOM - 0.01), (1.1, 1.3, R.DOOR_BOTTOM + 0.01))


def box_cuts(cutter, box, side, mirrored=True):
    x0, x1, y0, y1, z0, z1 = box
    if side < 0:
        x0, x1 = -x1, -x0
    pad = 0.03
    for xv in (x0, x1):
        cutter.cut((xv, 0, 0), (1, 0, 0), (xv - 0.01, y0 - pad, z0 - pad), (xv + 0.01, y1 + pad, z1 + pad))
    for yv in (y0, y1):
        cutter.cut((0, yv, 0), (0, 1, 0), (x0 - pad, yv - 0.01, z0 - pad), (x1 + pad, yv + 0.01, z1 + pad))
    for zv in (z0, z1):
        cutter.cut((0, 0, zv), (0, 0, 1), (x0 - pad, y0 - pad, zv - 0.01), (x1 + pad, y1 + pad, zv + 0.01))


# ---------------------------------------------------------------------------
# building

def sharpen(bm, angle_deg=38.0):
    import math
    thr = math.radians(angle_deg)
    for f in bm.faces:
        f.smooth = True
    for e in bm.edges:
        if len(e.link_faces) == 2 and e.calc_face_angle(0.0) > thr:
            e.smooth = False


def build_part_object(key, pieces):
    """pieces: list of (bmesh, faces, material keys per face). Returns one object named key."""
    out = bmesh.new()
    uv_out = out.loops.layers.uv.new("UVMap")
    mat_keys = []
    for bm, faces, mkeys in pieces:
        uv_in = bm.loops.layers.uv.active
        vmap = {}
        for f, mk in zip(faces, mkeys):
            if mk not in mat_keys:
                mat_keys.append(mk)
            mi = mat_keys.index(mk)
            vs = []
            for v in f.verts:
                nv = vmap.get(v)
                if nv is None:
                    nv = out.verts.new(v.co)
                    vmap[v] = nv
                vs.append(nv)
            try:
                nf = out.faces.new(vs)
            except ValueError:
                continue
            nf.material_index = mi
            nf.smooth = f.smooth
            if uv_in is not None:
                for lo, li in zip(nf.loops, f.loops):
                    lo[uv_out].uv = li[uv_in].uv
    bmesh.ops.remove_doubles(out, verts=out.verts, dist=1e-5)
    sharpen(out)
    me = bpy.data.meshes.new(key)
    out.to_mesh(me)
    out.free()
    for mk in mat_keys:
        me.materials.append(material_for(mk))
    obj = bpy.data.objects.new(key, me)
    bpy.context.scene.collection.objects.link(obj)
    obj["partKey"] = key
    return obj


def convert(log=lambda *a: print(*a, flush=True)):
    objs = SRC.import_normalised(log=log)
    SRC.bake_transforms(objs)
    kept = []
    for o in objs:
        name = o.name
        drop = name in DELETE_OBJECTS or (name.startswith(DELETE_PREFIXES) and name not in KEEP_EVEN_IF_PREFIXED) or o.type != "MESH"
        if drop:
            bpy.data.objects.remove(o)
        else:
            kept.append(o)
    log(f"source: kept {len(kept)} meshes")
    parts = {}
    total = 0
    for o in kept:
        bm = bmesh.new()
        bm.from_mesh(o.data)
        bm.faces.ensure_lookup_table()
        if o.name in SIDE_CUT_OBJECTS or o.name in (GLASS_TINT, GLASS_OUT, "flakka.2006.18", "flakka.2006.19", "boz7fa_land2004.017"):
            plane_cuts(bm)
        bm.normal_update()
        islands = island_sizes(bm) if o.name == PAINT else None
        groups = {}
        for f in bm.faces:
            smat = o.data.materials[f.material_index].name if o.data.materials and f.material_index < len(o.data.materials) and o.data.materials[f.material_index] else ""
            res = classify(o.name, smat, f.calc_center_median(), f.normal, islands[f.index] if islands else 10**9)
            if res is None:
                continue
            key, mk = res
            groups.setdefault(key, ([], []))
            groups[key][0].append(f)
            groups[key][1].append(mk)
        for key, (faces, mks) in groups.items():
            parts.setdefault(key, []).append((bm, faces, mks))
            total += len(faces)
        o["_bm"] = 1
    out = {}
    for key, pieces in parts.items():
        out[key] = build_part_object(key, pieces)
    for o in kept:
        me = o.data
        bpy.data.objects.remove(o)
        bpy.data.meshes.remove(me)
    for key, pieces in parts.items():
        for bm, _, _ in pieces:
            try:
                bm.free()
            except Exception:
                pass
    gxr_additions(out, log)
    log(f"converted: {len(out)} parts from {total} faces")
    return out


# ---------------------------------------------------------------------------
# geometry the GXR needs that the VXR source does not have

def append_mesh(obj, co, polys, mat_key):
    """Add polygons (world space) to an object under the given material key."""
    me = obj.data
    names = [m.name for m in me.materials]
    if mat_key not in names:
        me.materials.append(material_for(mat_key))
        names.append(mat_key)
    mi = names.index(mat_key)
    bm = bmesh.new()
    bm.from_mesh(me)
    uv = bm.loops.layers.uv.active or bm.loops.layers.uv.new("UVMap")
    vs = [bm.verts.new(Vector(c)) for c in co]
    for poly in polys:
        try:
            f = bm.faces.new([vs[i] for i in poly])
        except ValueError:
            continue
        f.material_index = mi
        f.smooth = True
    bm.normal_update()
    bm.to_mesh(me)
    bm.free()


def strip_surface(rows):
    """rows: list of rows, each a list of (x, y, z) points with equal length; returns (co, quads)."""
    co, polys = [], []
    n = len(rows[0])
    for r in rows:
        co.extend(r)
    for i in range(len(rows) - 1):
        for j in range(n - 1):
            a = i * n + j
            polys.append([a, a + 1, a + n + 1, a + n])
    return co, polys


LOWER_SKIN_PROFILE = [(0.742, 1.004), (0.68, 1.000), (0.60, 0.990), (0.52, 0.980), (0.42, 0.955), (0.40, 0.900)]  # (z, |x|)
ROCKER = (0.86, 0.905, 0.29, 0.43)  # |x| range and z range


def lower_door_skin(door_key, side, y_from, y_to):
    """Smooth white panel from the source skin's bottom edge down to the sill, per door."""
    sg = 1.0 if side == "L" else -1.0
    rows = []
    for z, ax in LOWER_SKIN_PROFILE:
        y0, y1 = y_from(z), y_to(z)
        ys = np.linspace(y0, y1, 12)
        row = [(sg * ax, float(y), z) for y in ys]
        if sg < 0:
            row = row[::-1]
        rows.append(row)
    return strip_surface(rows)


def gxr_additions(out, log):
    gap = 0.004
    for side in ("L", "R"):
        fd = out.get(f"DOOR_6701_front_door_{side}")
        rd = out.get(f"DOOR_6702_rear_door_{side}")
        if fd is not None:
            co, polys = lower_door_skin(fd.name, side, lambda z: line_y(R.A_LINE, max(z, 0.42)) + gap, lambda z: R.B_LINE[0][0] - gap)
            append_mesh(fd, co, polys, "paint_white")
        if rd is not None:
            co, polys = lower_door_skin(rd.name, side, lambda z: R.B_LINE[0][0] + gap, lambda z: line_y(R.REAR_DOOR_LINE, max(z, 0.42)) - gap)
            append_mesh(rd, co, polys, "paint_white")
        shell = out.get("BODY_0000_body_shell")
        if shell is not None:
            sg = 1.0 if side == "L" else -1.0
            x0, x1, z0, z1 = ROCKER
            co, polys = M.box_arrays((sg * 0.5 * (x0 + x1), 0.0, 0.5 * (z0 + z1)), (x1 - x0, 2.05, z1 - z0), bevel=0.008)
            append_mesh(shell, co, polys, "plastic_black_matte")
    log("gxr additions: lower door skins and rocker strips")
