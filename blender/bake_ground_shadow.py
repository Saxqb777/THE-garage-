"""Bake the car's soft ground shadow (ambient occlusion on the floor) into a texture.

Run after a build that saved its blend file:
    python3 blender/build_lc100.py --blend /path/lc100_model.blend
    python3 blender/bake_ground_shadow.py /path/lc100_model.blend [samples]

Writes public/textures/lc100_ground_shadow.png (grey, white = full shadow) and
src/data/groundShadow.json (the floor rectangle it covers, in three.js metres).

How: Cycles renders the floor from straight above as a shadow catcher with the car invisible
to the camera, lit by a uniform sky plus one large overhead softbox. The catcher's alpha is
how much light the car blocks at each floor point, which is exactly the soft parked shadow.
The app lays it on a plane under the car in every scene; the sun's hard shadow is separate
and live (three.js shadow map), so it follows the time of day slider.
"""
import json
import math
import os
import sys

import bpy
import numpy as np
from mathutils import Vector

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT_PNG = os.path.join(REPO, "public", "textures", "lc100_ground_shadow.png")
OUT_JSON = os.path.join(REPO, "src", "data", "groundShadow.json")

MARGIN = 1.1          # metres of floor around the car's footprint
PX_PER_M = 120        # about 8 mm per pixel; the shadow is soft, the tire contact still reads


def main():
    blend = sys.argv[1]
    samples = int(sys.argv[2]) if len(sys.argv) > 2 else 256
    bpy.ops.wm.open_mainfile(filepath=blend)
    sc = bpy.context.scene

    for o in list(sc.objects):
        if o.type in {"CAMERA", "LIGHT"}:
            bpy.data.objects.remove(o, do_unlink=True)

    meshes = [o for o in sc.objects if o.type == "MESH"]
    lo = Vector((1e9, 1e9, 1e9))
    hi = Vector((-1e9, -1e9, -1e9))
    for o in meshes:
        o.visible_camera = False      # casts shadows, never seen
        o.visible_glossy = False
        o.visible_transmission = False
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            lo = Vector(map(min, lo, w))
            hi = Vector(map(max, hi, w))
    cx, cy = (lo.x + hi.x) / 2, (lo.y + hi.y) / 2
    width = (hi.x - lo.x) + 2 * MARGIN      # along x (left/right)
    depth = (hi.y - lo.y) + 2 * MARGIN      # along y (front/back)
    print(f"car footprint x {lo.x:.3f}..{hi.x:.3f}, y {lo.y:.3f}..{hi.y:.3f}; floor {width:.2f} x {depth:.2f} m")

    # shadow catcher floor
    me = bpy.data.meshes.new("shadow_floor")
    hw, hd = width, depth
    me.from_pydata([(cx - hw, cy - hd, 0), (cx + hw, cy - hd, 0), (cx + hw, cy + hd, 0), (cx - hw, cy + hd, 0)], [], [(0, 1, 2, 3)])
    floor = bpy.data.objects.new("shadow_floor", me)
    sc.collection.objects.link(floor)
    floor.is_shadow_catcher = True

    # uniform sky: the occlusion part
    world = bpy.data.worlds.new("bake_world")
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (1, 1, 1, 1)
    world.node_tree.nodes["Background"].inputs["Strength"].default_value = 1.0
    sc.world = world

    # one big overhead softbox: darkens the footprint like workshop ceiling lights do
    light = bpy.data.lights.new("bake_top", "AREA")
    light.shape = "RECTANGLE"
    light.size, light.size_y = 3.0, 6.0
    light.energy = 900
    top = bpy.data.objects.new("bake_top", light)
    top.location = (cx, cy, 5.0)
    sc.collection.objects.link(top)

    cam_data = bpy.data.cameras.new("bake_cam")
    cam_data.type = "ORTHO"
    cam_data.ortho_scale = max(width, depth)
    cam = bpy.data.objects.new("bake_cam", cam_data)
    cam.location = (cx, cy, 20.0)
    cam.rotation_euler = (0, 0, 0)       # looking down -Z, image up = +Y (the car's rear)
    sc.collection.objects.link(cam)
    sc.camera = cam

    r = sc.render
    r.engine = "CYCLES"
    r.film_transparent = True
    r.resolution_x = int(round(width * PX_PER_M))
    r.resolution_y = int(round(depth * PX_PER_M))
    r.resolution_percentage = 100
    r.image_settings.file_format = "PNG"
    r.image_settings.color_mode = "RGBA"
    r.image_settings.color_depth = "16"
    sc.cycles.device = "CPU"
    sc.cycles.samples = samples
    sc.cycles.use_denoising = True
    sc.view_settings.view_transform = "Standard"
    tmp = os.path.join(os.path.dirname(blend), "ground_shadow_raw.png")
    r.filepath = tmp
    bpy.ops.render.render(write_still=True)

    from PIL import Image
    a = np.asarray(Image.open(tmp)).astype(np.float32)
    alpha = a[..., 3] / (65535.0 if a.max() > 255 else 255.0)
    # fade to zero at the border so the plane edge never shows
    h, w = alpha.shape
    yy, xx = np.mgrid[0:h, 0:w]
    edge = np.minimum.reduce([xx, yy, w - 1 - xx, h - 1 - yy]).astype(np.float32)
    alpha *= np.clip(edge / (0.35 * PX_PER_M), 0, 1)
    img = Image.fromarray((np.clip(alpha, 0, 1) * 255 + 0.5).astype(np.uint8), "L")
    os.makedirs(os.path.dirname(OUT_PNG), exist_ok=True)
    img.save(OUT_PNG, optimize=True)

    # Blender (x, y) on the ground is three.js (x, -z): image up (+y) is three.js -z
    meta = {
        "texture": "/textures/lc100_ground_shadow.png",
        "center": [round(cx, 4), 0, round(-cy, 4)],
        "size": [round(width, 4), round(depth, 4)],
        "note": "Generated by blender/bake_ground_shadow.py. Plane in the XZ ground plane, texture up = -Z.",
    }
    with open(OUT_JSON, "w") as f:
        json.dump(meta, f, indent=2)
        f.write("\n")
    print(f"wrote {OUT_PNG} ({w}x{h}, peak {alpha.max():.2f}) and {OUT_JSON}")


main()
