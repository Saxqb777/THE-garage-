"""Load the CC BY LC100 2006 source model into our frame: metres, Z up, car faces -Y, left is +X,
origin on the ground midway between the axles, wheelbase exactly 2.85.

import_normalised() returns the imported objects; nothing is deleted or renamed here.
"""
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, REPO)

import bpy  # noqa: E402
from mathutils import Matrix, Vector  # noqa: E402

from blender.lib import conventions as C  # noqa: E402

SOURCE = os.path.join(REPO, "reference", "model", "lc100_2006_cc_by", "lc100_2006.fbx")
WHEEL_EMPTIES = {"front_L": "WHEEL_LF", "front_R": "WHEEL_RF", "rear_L": "WHEEL_LR", "rear_R": "WHEEL_RR"}


def import_normalised(log=print):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.fbx(filepath=SOURCE)
    objs = [o for o in bpy.data.objects if o not in before]
    wheels = {k: bpy.data.objects[v].matrix_world.translation.copy() for k, v in WHEEL_EMPTIES.items()}
    wb = ((wheels["rear_L"] + wheels["rear_R"]) / 2 - (wheels["front_L"] + wheels["front_R"]) / 2).length
    scale = C.WHEELBASE / wb
    mid = (wheels["front_L"] + wheels["front_R"] + wheels["rear_L"] + wheels["rear_R"]) / 4
    ground = min((o.matrix_world @ Vector(c)).z for o in objs if o.type == "MESH" for c in o.bound_box)
    shift = Vector((-mid.x, -mid.y, -ground)) * scale
    M = Matrix.Translation(shift) @ Matrix.Scale(scale, 4)
    roots = [o for o in objs if o.parent is None or o.parent not in objs]
    for o in roots:
        o.matrix_world = M @ o.matrix_world
    bpy.context.view_layer.update()
    log(f"source: {len(objs)} objects, wheelbase {wb:.3f} scaled by {scale:.4f}, shifted {tuple(round(v, 3) for v in shift)}")
    return objs


def bake_transforms(objs):
    """Apply every object's world matrix into its mesh so all parts live in world space (origin at 0)."""
    for o in objs:
        if o.type != "MESH":
            continue
        if o.data.users > 1:
            o.data = o.data.copy()
        o.data.transform(o.matrix_world)
        o.matrix_world = Matrix.Identity(4)
    for o in objs:
        if o.type == "MESH" and o.parent is not None:
            o.parent = None
            o.matrix_world = Matrix.Identity(4)
    bpy.context.view_layer.update()
