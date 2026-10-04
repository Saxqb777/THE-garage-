"""Build the LC100 stand in model and export public/models/lc100.glb.

Run: python3 blender/build_lc100.py [--no-export] [--blend out.blend] [--render view1,view2]

Steps (the M1 pipeline from the brief):
  1. shell    procedural body and bumpers (Phase 2: import the paid model here instead)
  2. parts    wheels and small parts placed on the body
  3. pivots   hinge origins and parenting from src/data/parts.m1.json
  4. names    every node checked against the contract, extras written
  5. export   Draco GLB plus a size and triangle report
"""
import json
import os
import sys
import time

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, REPO)

import bpy  # noqa: E402
import numpy as np  # noqa: E402
from mathutils import Matrix, Vector  # noqa: E402

from blender.lib import conventions as C  # noqa: E402
from blender.lib import naming  # noqa: E402
from blender.parts import body as BODY  # noqa: E402
from blender.parts import body_sdf as S  # noqa: E402

HALF_WB = C.WHEELBASE / 2.0
OUT_GLB = os.path.join(REPO, "public", "models", "lc100.glb")


def log(*a):
    print(*a, flush=True)


def skin_x(u, z):
    """Body skin half width at (u, z) on the left side, found by bisection on the SDF."""
    lo, hi = 0.3, 1.1
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        d = S.body(np.array([u]), np.array([mid]), np.array([z]))[0]
        if d > 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


# ---------------------------------------------------------------------------
# Step 1: shell


def step_shell():
    objs = BODY.build(log=log)
    objs.update(BODY.build_bumpers(log=log))
    return objs


# ---------------------------------------------------------------------------
# Step 2: parts


def step_parts(objs):
    from blender.parts import wheel
    for pos in wheel.POSITIONS:
        empty = wheel.build_wheel_assembly(pos)
        objs[empty.name] = empty
        for child in empty.children:
            objs[child.name] = child
    from blender.parts import interior
    objs.update(interior.build())
    try:
        from blender.parts import placement
    except ImportError:
        log("parts: blender/parts/placement.py not present yet, skipping small parts")
        return objs
    objs.update(placement.place_all(objs, skin_x))
    return objs


# ---------------------------------------------------------------------------
# Step 3: pivots and parenting


def hinge_pivots():
    """Blender space pivot point for every hinged part (left side, mirrored for right)."""
    z_mid = 0.95
    piv = {
        "BODY_5301_hood": (0.0, 0.45 - HALF_WB, 1.245),
    }
    for side, sgn in (("L", 1.0), ("R", -1.0)):
        piv[f"DOOR_6701_front_door_{side}"] = (sgn * (skin_x(0.632, z_mid) + 0.004), 0.632 - HALF_WB, z_mid)
        piv[f"DOOR_6702_rear_door_{side}"] = (sgn * (skin_x(1.692, z_mid) + 0.004), 1.692 - HALF_WB, z_mid)
        piv[f"DOOR_6703_back_door_{side}"] = (sgn * 0.80, S.U_REAR + 0.02 - HALF_WB, 1.2)
    return piv


def set_origin(obj, point):
    point = Vector(point)
    if obj.type == "MESH":
        obj.data.transform(Matrix.Translation(-point + obj.location))
    obj.location = point


def parent_keep_world(child, parent):
    bpy.context.view_layer.update()
    mw = child.matrix_world.copy()
    child.parent = parent
    child.matrix_parent_inverse.identity()
    child.matrix_world = mw


def step_pivots(objs, contract):
    for key, point in hinge_pivots().items():
        if key in objs:
            set_origin(objs[key], point)
    bpy.context.view_layer.update()
    for key, part in contract.items():
        parent = part.get("parent")
        if parent and key in objs and parent in objs and objs[key].parent is None:
            parent_keep_world(objs[key], objs[parent])
    return objs


# ---------------------------------------------------------------------------
# Step 4: names and extras


def step_names(contract):
    problems = naming.validate_contract(contract)
    scene_keys = set()
    for obj in bpy.context.scene.objects:
        if obj.name.startswith("preview_"):
            continue
        if obj.name not in contract:
            problems.append(f"scene object {obj.name!r} is not in the contract")
            continue
        scene_keys.add(obj.name)
        part = contract[obj.name]
        obj["partKey"] = obj.name
        if obj.type == "MESH":
            obj.data.name = obj.name
        hinge = part.get("hinge")
        if hinge:
            obj["hingeAxis"] = list(hinge["axis"])
            obj["openDeg"] = float(hinge["openDeg"])
    if problems:
        for p in problems:
            log("NAME ERROR:", p)
        raise SystemExit("naming check failed")
    missing = sorted(set(contract) - scene_keys)
    log(f"names: {len(scene_keys)} nodes match the contract, {len(missing)} contract parts not built yet")
    for k in missing:
        log("   not built:", k)
    return scene_keys, missing


# ---------------------------------------------------------------------------
# Step 5: export


def tri_count(obj):
    return sum(len(p.vertices) - 2 for p in obj.data.polygons) if obj.type == "MESH" else 0


def step_export(path=OUT_GLB):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    for obj in list(bpy.context.scene.objects):
        if obj.name.startswith("preview_"):
            bpy.data.objects.remove(obj)
    bpy.ops.export_scene.gltf(
        filepath=path,
        export_format="GLB",
        use_selection=False,
        export_apply=True,
        export_extras=True,
        export_yup=True,
        export_normals=True,
        export_tangents=False,
        export_cameras=False,
        export_lights=False,
        export_animations=False,
        export_draco_mesh_compression_enable=True,
        export_draco_mesh_compression_level=7,
        export_draco_position_quantization=14,
        export_draco_normal_quantization=10,
        export_draco_texcoord_quantization=12,
    )
    meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    tris = sum(tri_count(o) for o in meshes)
    size = os.path.getsize(path)
    report = {
        "file": os.path.relpath(path, REPO),
        "bytes": size,
        "megabytes": round(size / 1e6, 2),
        "meshes": len(meshes),
        "nodes": len(bpy.context.scene.objects),
        "triangles": tris,
        "materials": sorted({m.name for o in meshes for m in o.data.materials if m}),
        "parts": {o.name: tri_count(o) for o in sorted(meshes, key=lambda o: o.name)},
    }
    with open(os.path.join(REPO, "public", "models", "lc100.report.json"), "w") as f:
        json.dump(report, f, indent=2)
    log(f"export: {report['file']} {report['megabytes']} MB, {len(meshes)} meshes, {tris} triangles")
    return report


def main():
    args = sys.argv[1:]
    t0 = time.time()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    contract = naming.load_contract()
    objs = step_shell()
    objs = step_parts(objs)
    objs = step_pivots(objs, contract)
    step_names(contract)
    if "--blend" in args:
        bpy.ops.wm.save_as_mainfile(filepath=args[args.index("--blend") + 1])
    if "--render" in args:
        from blender.lib import preview as P
        out_dir = args[args.index("--render") + 2] if len(args) > args.index("--render") + 2 else "/tmp"
        P.studio()
        for v in args[args.index("--render") + 1].split(","):
            loc, tgt, lens = P.VIEWS[v]
            P.camera(loc, tgt, lens)
            P.render(os.path.join(out_dir, f"lc100_{v}.png"), 1400, 800, 48)
    if "--no-export" not in args:
        step_export()
    log(f"done in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
