"""Quick Cycles preview renders for checking parts against the reference photos."""
import math

import bpy
from mathutils import Vector


def studio(floor=True, world_strength=0.9):
    sc = bpy.context.scene
    world = bpy.data.worlds.new("preview_world")
    world.use_nodes = True
    nt = world.node_tree
    bg = nt.nodes["Background"]
    sky = nt.nodes.new("ShaderNodeTexSky")
    sky.sky_type = "NISHITA"
    sky.sun_elevation = math.radians(35)
    sky.sun_rotation = math.radians(140)
    sky.sun_intensity = 0.35
    nt.links.new(sky.outputs["Color"], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = world_strength * 0.25
    sc.world = world
    for name, loc, size, energy in (("key", (4.5, -5.0, 5.0), 4.0, 1800), ("fill", (-5.5, -2.0, 3.0), 5.0, 700),
                                    ("top", (0.0, 0.5, 6.5), 6.0, 1500), ("rim", (1.0, 7.0, 3.5), 4.0, 900)):
        light = bpy.data.lights.new(f"preview_{name}", "AREA")
        light.size = size
        light.energy = energy
        obj = bpy.data.objects.new(f"preview_{name}", light)
        obj.location = loc
        direction = Vector((0, 0, 0.8)) - Vector(loc)
        obj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
        sc.collection.objects.link(obj)
    if floor:
        me = bpy.data.meshes.new("preview_floor")
        s = 30
        me.from_pydata([(-s, -s, 0), (s, -s, 0), (s, s, 0), (-s, s, 0)], [], [(0, 1, 2, 3)])
        mat = bpy.data.materials.new("preview_floor_mat")
        mat.use_nodes = True
        b = mat.node_tree.nodes["Principled BSDF"]
        b.inputs["Base Color"].default_value = (0.32, 0.32, 0.33, 1)
        b.inputs["Roughness"].default_value = 0.55
        me.materials.append(mat)
        obj = bpy.data.objects.new("preview_floor", me)
        sc.collection.objects.link(obj)


def camera(location, target, lens=40.0):
    sc = bpy.context.scene
    cam = sc.camera
    if cam is None:
        cam = bpy.data.objects.new("preview_cam", bpy.data.cameras.new("preview_cam"))
        sc.collection.objects.link(cam)
        sc.camera = cam
    cam.data.lens = lens
    cam.location = location
    direction = Vector(target) - Vector(location)
    cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    return cam


def render(path, width=1200, height=700, samples=48):
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = samples
    sc.cycles.use_denoising = True
    try:
        sc.cycles.denoiser = "OPENIMAGEDENOISE"
    except TypeError:
        pass
    sc.render.resolution_x = width
    sc.render.resolution_y = height
    sc.render.film_transparent = False
    sc.view_settings.view_transform = "AgX"
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)


VIEWS = {
    # name: (camera location, target, lens), Blender space, car faces minus Y, left side is plus X
    "front34_left": ((5.2, -6.6, 1.55), (0.0, -0.6, 0.85), 42),
    "side_left": ((10.5, 0.12, 1.0), (0.0, 0.12, 0.95), 48),
    "rear34_left": ((5.0, 7.0, 1.9), (0.0, 0.8, 0.9), 42),
    "rear": ((0.0, 8.5, 1.45), (0.0, 1.6, 1.05), 50),
    "front": ((0.0, -8.5, 1.35), (0.0, -1.6, 0.95), 50),
    "front34_right": ((-4.6, -6.4, 1.3), (0.0, -0.9, 0.85), 42),
}
