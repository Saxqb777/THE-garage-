"""Placeholder interior: enough volume and colour that the glass shows a cabin, not a hollow shell.

Real interior comes in Phase 2. Positions are in body coordinates (u behind the front axle, x left, z up).
"""
import math

import bmesh
import bpy
from mathutils import Matrix, Vector

from blender.lib import conventions as C
from blender.lib import materials as MAT

HALF_WB = C.WHEELBASE / 2.0
FLOOR_Z = 0.62


def _box(name, u0, u1, x0, x1, z0, z1, mat, bevel=0.03, tilt_deg=0.0, tilt_pivot=None, segments=3):
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x = x0 + (v.co.x + 0.5) * (x1 - x0)
        v.co.y = (u0 + (v.co.y + 0.5) * (u1 - u0)) - HALF_WB
        v.co.z = z0 + (v.co.z + 0.5) * (z1 - z0)
    if bevel > 0:
        bmesh.ops.bevel(bm, geom=list(bm.edges), offset=bevel, segments=segments, affect="EDGES", profile=0.5)
    if tilt_deg and tilt_pivot is not None:
        pu, pz = tilt_pivot
        pivot = Vector((0.0, pu - HALF_WB, pz))
        rot = Matrix.Translation(pivot) @ Matrix.Rotation(math.radians(tilt_deg), 4, "X") @ Matrix.Translation(-pivot)
        bmesh.ops.transform(bm, matrix=rot, verts=bm.verts)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(obj)
    MAT.assign(obj, mat)
    for p in me.polygons:
        p.use_smooth = True
    return obj


def _join(name, parts):
    bpy.context.view_layer.update()
    target = parts[0]
    others = parts[1:]
    if others:
        with bpy.context.temp_override(active_object=target, selected_editable_objects=parts, object=target):
            bpy.ops.object.join()
    target.name = name
    target.data.name = name
    target["partKey"] = name
    return target


def _seat(name, x_c, half_w, u_front, u_back, cushion_z, back_top):
    cushion = _box(name, u_front, u_back, x_c - half_w, x_c + half_w, cushion_z - 0.11, cushion_z, "interior_cloth_grey", 0.035)
    back = _box(name + "_b", u_back - 0.13, u_back, x_c - half_w + 0.01, x_c + half_w - 0.01, cushion_z - 0.02, back_top,
                "interior_cloth_grey", 0.04, tilt_deg=-12, tilt_pivot=(u_back - 0.06, cushion_z))
    head = _box(name + "_h", u_back - 0.09 + 0.07, u_back + 0.07, x_c - 0.13, x_c + 0.13, back_top + 0.04, back_top + 0.22,
                "interior_cloth_grey", 0.035, tilt_deg=-12, tilt_pivot=(u_back - 0.06, cushion_z))
    base = _box(name + "_r", u_front + 0.05, u_back - 0.05, x_c - half_w + 0.05, x_c + half_w - 0.05, FLOOR_Z, cushion_z - 0.1,
                "interior_plastic_grey", 0.01, segments=1)
    return _join(name, [cushion, back, head, base])


def build():
    objs = {}
    carpet = _box("INT_0000_floor_carpet", 0.62, 3.88, -0.84, 0.84, FLOOR_Z - 0.03, FLOOR_Z, "interior_carpet", 0.01, segments=1)
    tunnel = _box("_tunnel", 0.70, 1.75, -0.13, 0.13, FLOOR_Z, FLOOR_Z + 0.16, "interior_carpet", 0.04)
    objs["INT_0000_floor_carpet"] = _join("INT_0000_floor_carpet", [carpet, tunnel])
    dash = _box("INT_0000_instrument_panel", 0.62, 0.98, -0.83, 0.83, 0.86, 1.24, "interior_plastic_grey", 0.06)
    hood = _box("_binnacle", 0.86, 1.02, 0.18, 0.56, 1.18, 1.30, "interior_plastic_grey", 0.04)
    stack = _box("_stack", 0.80, 1.00, -0.13, 0.13, FLOOR_Z + 0.12, 1.12, "interior_plastic_grey", 0.03)
    objs["INT_0000_instrument_panel"] = _join("INT_0000_instrument_panel", [dash, hood, stack])
    # steering wheel: a torus on the driver side (LHD, vehicle left is +X), tilted towards the driver
    bpy.ops.mesh.primitive_torus_add(major_radius=0.19, minor_radius=0.017, major_segments=48, minor_segments=12)
    wheel = bpy.context.active_object
    wheel.name = "INT_0000_steering_wheel"
    wheel.data.name = wheel.name
    wheel.rotation_euler = (math.radians(90 - 26), 0.0, 0.0)
    wheel.location = (0.37, 1.10 - HALF_WB, 1.12)
    MAT.assign(wheel, "interior_plastic_grey")
    bpy.ops.object.shade_smooth()
    wheel["partKey"] = wheel.name
    objs[wheel.name] = wheel
    objs["INT_0000_front_seat_L"] = _seat("INT_0000_front_seat_L", 0.37, 0.25, 1.30, 1.82, 1.03, 1.62)
    objs["INT_0000_front_seat_R"] = _seat("INT_0000_front_seat_R", -0.37, 0.25, 1.30, 1.82, 1.03, 1.62)
    objs["INT_0000_rear_seat"] = _seat("INT_0000_rear_seat", 0.0, 0.74, 2.30, 2.82, 1.02, 1.56)
    return objs
