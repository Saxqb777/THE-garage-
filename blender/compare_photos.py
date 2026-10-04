"""Render the model from cameras that roughly match the reference photos and stitch side by side images.

Run: python3 blender/compare_photos.py path/to/lc100.blend OUT_DIR [samples]
Writes OUT_DIR/compare_<name>.png with the photo on the left and the render on the right.
Camera poses were estimated from the photos (perspective of the wheels, horizon height, framing).
"""
import math
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, REPO)

import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

from blender.lib import preview as P  # noqa: E402

SHOTS = {
    # name: (photo, crop box or None, camera location, target, lens mm)
    "side_left": ("reference/photos/side_left.webp", None, (3.95, -1.55, 1.25), (0.0, -0.05, 0.85), 24),
    "front34_right": ("reference/photos/front_three_quarter_right.webp", None, (-2.75, -5.35, 1.0), (-0.25, -1.45, 0.78), 26),
    "rear": ("reference/photos/rear_browser_screenshot.webp", (310, 105, 1690, 1140), (0.04, 6.9, 1.62), (0.0, 2.6, 1.02), 31),
}


def outdoor():
    """Hard sun and sky, like the listing photos."""
    sc = bpy.context.scene
    world = bpy.data.worlds.new("outdoor")
    world.use_nodes = True
    nt = world.node_tree
    sky = nt.nodes.new("ShaderNodeTexSky")
    sky.sky_type = "NISHITA"
    sky.sun_elevation = math.radians(28)
    sky.sun_rotation = math.radians(205)
    sky.sun_disc = False
    nt.links.new(sky.outputs["Color"], nt.nodes["Background"].inputs["Color"])
    nt.nodes["Background"].inputs["Strength"].default_value = 0.35
    sc.world = world
    sun = bpy.data.objects.new("compare_sun", bpy.data.lights.new("compare_sun", "SUN"))
    sun.data.energy = 3.2
    sun.data.angle = math.radians(1.5)
    sun.rotation_euler = (math.radians(62), 0.0, math.radians(205))
    sc.collection.objects.link(sun)
    me = bpy.data.meshes.new("compare_floor")
    s = 40
    me.from_pydata([(-s, -s, 0), (s, -s, 0), (s, s, 0), (-s, s, 0)], [], [(0, 1, 2, 3)])
    mat = bpy.data.materials.new("compare_floor")
    mat.use_nodes = True
    b = mat.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (0.3, 0.3, 0.31, 1)
    b.inputs["Roughness"].default_value = 0.8
    me.materials.append(mat)
    sc.collection.objects.link(bpy.data.objects.new("compare_floor", me))


def stitch(photo_path, crop, render_path, out_path, label):
    photo = Image.open(os.path.join(REPO, photo_path)).convert("RGB")
    if crop:
        photo = photo.crop(crop)
    render = Image.open(render_path).convert("RGB")
    h = 640
    photo = photo.resize((int(photo.width * h / photo.height), h), Image.LANCZOS)
    render = render.resize((int(render.width * h / render.height), h), Image.LANCZOS)
    out = Image.new("RGB", (photo.width + render.width + 12, h + 40), (16, 17, 20))
    out.paste(photo, (0, 40))
    out.paste(render, (photo.width + 12, 40))
    d = ImageDraw.Draw(out)
    d.text((10, 12), f"reference photo: {label}", fill=(230, 230, 230))
    d.text((photo.width + 22, 12), "stand in model, matched camera (approximate)", fill=(242, 195, 107))
    out.save(out_path)


def main():
    blend, out_dir = sys.argv[1], sys.argv[2]
    samples = int(sys.argv[3]) if len(sys.argv) > 3 else 48
    os.makedirs(out_dir, exist_ok=True)
    bpy.ops.wm.open_mainfile(filepath=blend)
    outdoor()
    for name, (photo, crop, loc, tgt, lens) in SHOTS.items():
        im = Image.open(os.path.join(REPO, photo))
        w, h = (crop[2] - crop[0], crop[3] - crop[1]) if crop else im.size
        P.camera(loc, tgt, lens)
        render_path = os.path.join(out_dir, f"match_{name}.png")
        P.render(render_path, 1000, int(1000 * h / w), samples)
        stitch(photo, crop, render_path, os.path.join(out_dir, f"compare_{name}.png"), name.replace("_", " "))
        print("wrote", name, flush=True)


if __name__ == "__main__":
    main()
