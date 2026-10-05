"""Test scene for blender/parts/details.py.

Builds every detail part (both sides), lays them out on a grey studio floor, renders
Cycles previews and exports a Draco compressed GLB. Run headless with plain python3:

    python3 blender/parts/test_details.py [overview grille mirror plate handle] [--samples N] [--no-export]

Outputs go to the scratchpad folder OUT below.
"""
import importlib
import json
import math
import os
import struct
import sys
import time

import bpy
import bmesh
from mathutils import Vector

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
if REPO not in sys.path:
    sys.path.insert(0, REPO)
RES_SCALE = float(os.environ.get("DETAILS_RES_SCALE", "1.0"))
OUT = "/tmp/claude-0/-home-user-THE-garage-/d03d873b-2b55-5f6e-84dd-76d905acf029/scratchpad/agents/details/"

from blender.parts import details  # noqa: E402

importlib.reload(details)

VIEWS = {
    # name: (camera location, look at point, focal length mm)
    "overview": ((0.35, -3.6, 2.0), (0.35, 0.75, 0.30), 28.0),
    "grille": ((0.42, -1.30, 0.86), (0.0, 0.0, 0.50), 55.0),
    "mirror": ((-1.95, -0.62, 0.78), (-1.70, 0.02, 0.55), 55.0),
    "plate": ((-1.20, 0.13, 0.57), (-1.20, 0.8, 0.50), 40.0),
    "handle": ((1.02, -0.42, 0.66), (0.85, 0.0, 0.50), 60.0),
    # extra QA views
    "mudguard": ((1.10, 0.15, 0.55), (0.90, 0.8, 0.36), 50.0),
    "marker": ((2.42, -0.22, 0.55), (2.35, 0.0, 0.50), 60.0),
    "wiper": ((0.1, 0.95, 0.55), (-0.35, 1.6, 0.02), 45.0),
    "badges": ((-0.45, 0.05, 0.62), (-0.45, 0.8, 0.50), 45.0),
}


def tri_count(ob):
    return sum(len(p.vertices) - 2 for p in ob.data.polygons)


def place(ob, x, y, z, rz_deg=0.0, rx_deg=0.0):
    ob.location = (x, y, z)
    ob.rotation_euler = (math.radians(rx_deg), 0.0, math.radians(rz_deg))


def build_layout():
    """Build every part and arrange it facing the camera (which sits at -Y)."""
    parts = {}

    def keep(ob):
        parts[ob.name] = ob
        for c in ob.children:
            parts[c.name] = c
        return ob

    zc = 0.50
    # row 1: mirrors, grille, handles, markers
    place(keep(details.build_mirror("L")), -1.70, 0.0, zc, 180)
    place(keep(details.build_mirror("R")), -1.15, 0.0, zc, 180)
    place(keep(details.build_grille()), 0.0, 0.0, zc, 0)
    place(keep(details.build_door_handle("front", "L")), 0.85, 0.0, zc, -90)
    place(keep(details.build_door_handle("rear", "L")), 1.25, 0.0, zc, -90)
    place(keep(details.build_door_handle("front", "R")), 1.65, 0.0, zc, 90)
    place(keep(details.build_door_handle("rear", "R")), 2.05, 0.0, zc, 90)
    place(keep(details.build_side_marker("L")), 2.35, 0.0, zc, -90)
    place(keep(details.build_side_marker("R")), 2.52, 0.0, zc, 90)
    # row 2: badges and mudguards
    badges = details.build_badges()
    for b in badges.values():
        keep(b)
    place(badges["TRIM_0000_back_door_name_plate"], -1.20, 0.8, zc, 180)
    place(badges["TRIM_7551_back_door_emblem"], -0.72, 0.8, zc, 180)
    place(badges["TRIM_7551_grade_badge"], -0.47, 0.8, zc, 180)
    place(badges["TRIM_7551_quarter_badge_L"], -0.10, 0.8, zc, -90)
    place(badges["TRIM_7551_quarter_badge_R"], 0.35, 0.8, zc, 90)
    place(keep(details.build_mudguard("front_L")), 0.90, 0.8, 0.52, 180)
    place(keep(details.build_mudguard("front_R")), 1.30, 0.8, 0.52, 180)
    place(keep(details.build_mudguard("rear_L")), 1.75, 0.8, 0.56, 180)
    place(keep(details.build_mudguard("rear_R")), 2.20, 0.8, 0.56, 180)
    # row 3: wipers lying on the floor (local +Z up = glass normal)
    place(keep(details.build_wiper("front", "L")), 0.0, 1.6, 0.02, 0)
    place(keep(details.build_wiper("front", "R")), -1.0, 1.6, 0.02, 0)
    place(keep(details.build_wiper("rear", "L")), 0.50, 1.6, 0.02, 0)
    place(keep(details.build_wiper("rear", "R")), 1.95, 1.6, 0.02, 0)
    return parts


def add_studio(scene):
    # floor
    me = bpy.data.meshes.new("test_floor")
    bm = bmesh.new()
    bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=20.0)
    bm.to_mesh(me)
    bm.free()
    floor = bpy.data.objects.new("test_floor", me)
    scene.collection.objects.link(floor)
    mat = bpy.data.materials.new("test_floor")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.30, 0.30, 0.31, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.55
    me.materials.append(mat)
    # gradient world: warm grey ground to pale sky
    world = bpy.data.worlds.new("test_world")
    world.use_nodes = True
    nt = world.node_tree
    bg = nt.nodes["Background"]
    texco = nt.nodes.new("ShaderNodeTexCoord")
    mapping = nt.nodes.new("ShaderNodeMapping")
    mapping.inputs["Rotation"].default_value = (0.0, math.radians(-90.0), 0.0)
    grad = nt.nodes.new("ShaderNodeTexGradient")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    ramp.color_ramp.elements[0].position = 0.45
    ramp.color_ramp.elements[0].color = (0.18, 0.18, 0.19, 1.0)
    ramp.color_ramp.elements[1].position = 0.75
    ramp.color_ramp.elements[1].color = (0.75, 0.80, 0.90, 1.0)
    nt.links.new(texco.outputs["Generated"], mapping.inputs["Vector"])
    nt.links.new(mapping.outputs["Vector"], grad.inputs["Vector"])
    nt.links.new(grad.outputs["Fac"], ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = 0.55
    scene.world = world
    # large soft area lights
    for name, loc, energy, size in (
        ("key", (-2.5, -4.0, 4.5), 320.0, 4.0),
        ("fill", (4.0, -3.5, 2.5), 110.0, 4.0),
        ("rim", (0.5, 4.5, 3.5), 160.0, 3.0),
        ("top", (0.5, 0.5, 5.0), 90.0, 6.0),
    ):
        light = bpy.data.lights.new(name, "AREA")
        light.energy = energy
        light.size = size
        ob = bpy.data.objects.new(name, light)
        scene.collection.objects.link(ob)
        ob.location = loc
        direction = Vector((0.4, 0.8, 0.3)) - Vector(loc)
        ob.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def setup_render(scene, samples, width=900, height=600):
    width = int(width * RES_SCALE)
    height = int(height * RES_SCALE)
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = samples
    scene.cycles.use_denoising = False
    scene.cycles.max_bounces = 6
    scene.cycles.glossy_bounces = 4
    scene.cycles.caustics_reflective = False
    scene.cycles.caustics_refractive = False
    scene.cycles.blur_glossy = 1.0
    scene.cycles.sample_clamp_indirect = 4.0
    scene.render.resolution_x = width
    scene.render.resolution_y = height
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Base Contrast"


def render_view(scene, name, samples):
    loc, target, lens = VIEWS[name]
    cam = bpy.data.cameras.get("test_cam") or bpy.data.cameras.new("test_cam")
    cam.lens = lens
    cam.clip_start = 0.02
    co = bpy.data.objects.get("test_cam")
    if co is None:
        co = bpy.data.objects.new("test_cam", cam)
        scene.collection.objects.link(co)
    co.location = loc
    direction = Vector(target) - Vector(loc)
    co.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    scene.camera = co
    scene.cycles.samples = samples
    scene.render.filepath = os.path.join(OUT, f"preview_{name}.png")
    t = time.time()
    bpy.ops.render.render(write_still=True)
    print(f"rendered {name} in {time.time() - t:.1f}s -> {scene.render.filepath}")


def export_glb(parts, path):
    for ob in bpy.data.objects:
        ob.select_set(False)
    for ob in parts.values():
        ob.select_set(True)
    bpy.ops.export_scene.gltf(
        filepath=path,
        export_format="GLB",
        use_selection=True,
        export_apply=True,
        export_yup=True,
        export_extras=True,
        export_draco_mesh_compression_enable=True,
        export_draco_mesh_compression_level=6,
        export_materials="EXPORT",
        export_normals=True,
        export_texcoords=False,
        export_animations=False,
        export_skins=False,
        export_cameras=False,
        export_lights=False,
    )
    size = os.path.getsize(path)
    # verify the file by importing it back into a scratch scene
    verify_glb(path)
    # verify extras survived
    with open(path, "rb") as f:
        magic, version, length = struct.unpack("<III", f.read(12))
        chunk_len, chunk_type = struct.unpack("<II", f.read(8))
        gltf = json.loads(f.read(chunk_len))
    keys = sorted(n.get("extras", {}).get("partKey", "") for n in gltf["nodes"])
    missing = [n["name"] for n in gltf["nodes"] if n.get("extras", {}).get("partKey") != n["name"]]
    print(f"GLB {path}: {size / 1024:.1f} KiB, {len(gltf['nodes'])} nodes, {len(gltf['meshes'])} meshes, "
          f"{len(gltf['materials'])} materials, nodes without matching partKey: {missing}")
    return size


def verify_glb(path):
    """Import the GLB back into a throwaway scene and report what came back."""
    scene_before = bpy.context.window.scene if bpy.context.window else bpy.context.scene
    scratch = bpy.data.scenes.new("glb_verify")
    bpy.context.window.scene = scratch
    try:
        bpy.ops.import_scene.gltf(filepath=path)
        objs = [o for o in scratch.objects if o.type == "MESH"]
        tris = sum(tri_count(o) for o in objs)
        bad = [o.name for o in objs if o.get("partKey") != o.name.split(".")[0]]
        print(f"reimport check: {len(objs)} meshes, {tris} triangles, partKey mismatches: {bad}")
    finally:
        bpy.context.window.scene = scene_before
        for o in list(scratch.objects):
            bpy.data.objects.remove(o)
        bpy.data.scenes.remove(scratch)


def main(argv):
    samples = 64
    do_export = True
    views = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--samples":
            samples = int(argv[i + 1])
            i += 1
        elif a == "--no-export":
            do_export = False
        else:
            views.append(a)
        i += 1
    if not views:
        views = ["overview", "grille", "mirror", "plate", "handle"]
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    t = time.time()
    parts = build_layout()
    print(f"built {len(parts)} objects in {time.time() - t:.1f}s")
    total = 0
    for name in sorted(parts):
        ob = parts[name]
        n = tri_count(ob)
        total += n
        dims = ob.dimensions
        print(f"  {name:45s} {n:6d} tris  dims {dims.x:.3f} x {dims.y:.3f} x {dims.z:.3f}  mats {[m.name for m in ob.data.materials]}")
    print(f"total {total} triangles")
    stray = [o.name for o in bpy.data.objects if o.name not in parts]
    print("other objects in scene:", stray, "| curves:", len(bpy.data.curves), "fonts:", [f.name for f in bpy.data.fonts])
    add_studio(scene)
    setup_render(scene, samples)
    for v in views:
        render_view(scene, v, samples)
    if do_export:
        export_glb(parts, os.path.join(OUT, "details_test.glb"))


if __name__ == "__main__":
    main(sys.argv[1:])
