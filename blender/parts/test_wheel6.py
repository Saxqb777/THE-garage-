"""Preview harness for blender/parts/wheel6.py.

Builds the four wheel assemblies in a fresh scene, renders three Cycles previews into
the scratchpad folder (3/4 close up of front_L, side view of front_L, all four wheels
from above front) and exports the assemblies to wheels6_test.glb (prefix wheel6_).

Run with plain python3 (Blender as a module):
    python3 blender/parts/test_wheel6.py [out_dir]
"""
import math
import os
import sys
import time

import bpy
from mathutils import Vector

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO not in sys.path:
    sys.path.insert(0, REPO)

OUT_DIR = sys.argv[1] if len(sys.argv) > 1 else (
    "/tmp/claude-0/-home-user-THE-garage-/d03d873b-2b55-5f6e-84dd-76d905acf029/scratchpad/agents/wheel")
SAMPLES = int(os.environ.get("WHEEL_SAMPLES", "48"))
WIDTH = int(os.environ.get("WHEEL_WIDTH", "900"))
VIEWS = os.environ.get("WHEEL_VIEWS", "3q,side,all,3q_R").split(",")


def look_at(cam, target):
    direction = Vector(target) - cam.location
    cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def add_camera(name, location, target, lens):
    cam_data = bpy.data.cameras.new(name)
    cam_data.lens = lens
    cam_data.sensor_width = 36.0
    cam = bpy.data.objects.new(name, cam_data)
    bpy.context.scene.collection.objects.link(cam)
    cam.location = location
    look_at(cam, target)
    return cam


def add_area(name, location, target, size, power, size_y=None):
    ld = bpy.data.lights.new(name, "AREA")
    ld.energy = power
    ld.shape = "RECTANGLE" if size_y else "SQUARE"
    ld.size = size
    if size_y:
        ld.size_y = size_y
    light = bpy.data.objects.new(name, ld)
    bpy.context.scene.collection.objects.link(light)
    light.location = location
    look_at(light, target)
    return light


def build_studio():
    scene = bpy.context.scene
    # floor
    me = bpy.data.meshes.new("_test_floor")
    s = 30.0
    me.from_pydata([(-s, -s, 0), (s, -s, 0), (s, s, 0), (-s, s, 0)], [], [(0, 1, 2, 3)])
    floor = bpy.data.objects.new("_test_floor", me)
    scene.collection.objects.link(floor)
    mat = bpy.data.materials.new("_test_floor")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.30, 0.30, 0.31, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.55
    me.materials.append(mat)
    # world: soft vertical gradient
    world = bpy.data.worlds.new("_test_world")
    world.use_nodes = True
    nt = world.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputWorld")
    bg = nt.nodes.new("ShaderNodeBackground")
    ramp = nt.nodes.new("ShaderNodeValToRGB")
    maprange = nt.nodes.new("ShaderNodeMapRange")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    tex = nt.nodes.new("ShaderNodeTexCoord")
    nt.links.new(tex.outputs["Generated"], sep.inputs["Vector"])
    nt.links.new(sep.outputs["Z"], maprange.inputs["Value"])
    maprange.inputs["From Min"].default_value = -1.0
    maprange.inputs["From Max"].default_value = 1.0
    nt.links.new(maprange.outputs["Result"], ramp.inputs["Fac"])
    ramp.color_ramp.elements[0].position = 0.0
    ramp.color_ramp.elements[0].color = (0.10, 0.10, 0.11, 1.0)
    ramp.color_ramp.elements[1].position = 1.0
    ramp.color_ramp.elements[1].color = (0.62, 0.64, 0.68, 1.0)
    mid = ramp.color_ramp.elements.new(0.5)
    mid.color = (0.30, 0.31, 0.33, 1.0)
    nt.links.new(ramp.outputs["Color"], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = 1.0
    nt.links.new(bg.outputs["Background"], out.inputs["Surface"])
    scene.world = world
    # lights aimed at the front left wheel region
    target = (0.81, -1.425, 0.385)
    add_area("_key", (3.2, -4.2, 3.4), target, 3.0, 260.0)
    add_area("_fill", (-2.5, -5.5, 1.8), target, 4.0, 90.0)
    add_area("_top", (0.5, -1.0, 4.2), target, 6.0, 160.0, size_y=1.5)
    add_area("_rim", (2.5, 2.5, 1.5), target, 2.0, 70.0)
    # softboxes facing the wheel faces so the satin alloy picks up a broad highlight
    add_area("_side_L", (4.5, -1.6, 1.4), target, 3.0, 220.0, size_y=2.0)
    add_area("_side_R", (-4.5, -1.6, 1.4), (-0.81, -1.425, 0.385), 3.0, 220.0, size_y=2.0)


def setup_render(scene):
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = SAMPLES
    scene.cycles.use_adaptive_sampling = True
    try:
        scene.cycles.use_denoising = True
        scene.cycles.denoiser = "OPENIMAGEDENOISE"
        scene.cycles.denoising_use_gpu = False
    except Exception:
        scene.cycles.use_denoising = False
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"


def render(scene, cam, path, width, height):
    scene.camera = cam
    scene.render.resolution_x = width
    scene.render.resolution_y = height
    scene.render.resolution_percentage = 100
    scene.render.filepath = path
    t = time.time()
    bpy.ops.render.render(write_still=True)
    print(f"rendered {path} in {time.time() - t:.1f}s")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    from blender.parts import wheel6 as wheel

    t = time.time()
    assemblies = [wheel.build_wheel_assembly(p) for p in wheel.POSITIONS]
    print(f"built 4 assemblies in {time.time() - t:.1f}s")
    wheel_objects = []
    for a in assemblies:
        wheel_objects.append(a)
        wheel_objects.extend(a.children)
    for ob in wheel_objects:
        if ob.type == "MESH":
            print(f"  {ob.name}: {wheel.triangle_count(ob)} tris, {len(ob.data.vertices)} verts, "
                  f"materials {[m.name for m in ob.data.materials]}")

    build_studio()
    scene = bpy.context.scene
    setup_render(scene)
    bpy.context.view_layer.update()
    for a in assemblies:
        for ch in a.children:
            print(f"  {ch.name} world centre {[round(v, 3) for v in ch.matrix_world.translation]}")
    c = wheel.conventions.wheel_centres()["front_L"]
    cr = wheel.conventions.wheel_centres()["front_R"]
    cams = {
        "3q": (add_camera("_cam_3q", (c[0] + 1.30, c[1] - 1.05, c[2] + 0.30), (c[0], c[1], c[2] - 0.03), 50.0),
               "wheel6_3q_front_L.png", WIDTH, int(WIDTH * 0.72)),
        "side": (add_camera("_cam_side", (c[0] + 2.6, c[1], c[2]), c, 85.0),
                 "wheel6_side_front_L.png", WIDTH, int(WIDTH * 0.72)),
        "all": (add_camera("_cam_all", (0.0, -4.6, 2.4), (0.0, 0.25, 0.3), 42.0),
                "wheel6_all_four.png", WIDTH, int(WIDTH * 0.62)),
        "3q_R": (add_camera("_cam_3q_R", (cr[0] - 1.30, cr[1] - 1.05, cr[2] + 0.30), (cr[0], cr[1], cr[2] - 0.03), 50.0),
                 "wheel6_3q_front_R.png", WIDTH, int(WIDTH * 0.72)),
    }
    for key in VIEWS:
        cam, fname, w, h = cams[key]
        render(scene, cam, os.path.join(OUT_DIR, fname), w, h)

    # glTF export of the four assemblies only
    for ob in bpy.data.objects:
        ob.select_set(False)
    for ob in wheel_objects:
        ob.select_set(True)
    glb = os.path.join(OUT_DIR, "wheels6_test.glb")
    bpy.ops.export_scene.gltf(
        filepath=glb,
        export_format="GLB",
        use_selection=True,
        export_draco_mesh_compression_enable=True,
        export_extras=True,
        export_yup=True,
        export_apply=True,
    )
    print(f"GLB {glb}: {os.path.getsize(glb) / 1024:.0f} KiB")
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT_DIR, "wheels6_test.blend"))


if __name__ == "__main__":
    main()
