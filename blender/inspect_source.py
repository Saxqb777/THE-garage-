"""Inventory of a source car model: what each object is, how big, what material, how many loose parts.

Run: python3 blender/inspect_source.py path/to/model.fbx OUT_DIR
Writes OUT_DIR/inventory.json, OUT_DIR/inventory.md and colour coded ID renders (one colour per
object, and one per material) with legends, so a model from a shop or a mod can be mapped onto
the part contract before any cutting.
"""
import colorsys
import json
import os
import sys

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, REPO)

import bpy  # noqa: E402
import bmesh  # noqa: E402,I100  bpy must load first
from mathutils import Vector  # noqa: E402

from blender.lib import preview as P  # noqa: E402


def tri_count(obj):
    return sum(len(p.vertices) - 2 for p in obj.data.polygons)


def loose_parts(obj, limit=400):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bm.verts.ensure_lookup_table()
    seen = set()
    parts = []
    for v in bm.verts:
        if v.index in seen:
            continue
        stack = [v]
        seen.add(v.index)
        n = 0
        while stack:
            cur = stack.pop()
            n += 1
            for e in cur.link_edges:
                o = e.other_vert(cur)
                if o.index not in seen:
                    seen.add(o.index)
                    stack.append(o)
        parts.append(n)
        if len(parts) > limit:
            break
    bm.free()
    return len(parts), sorted(parts, reverse=True)[:6]


def world_bounds(obj):
    pts = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    lo = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    hi = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    return lo, hi


def material_textures(mat):
    out = []
    if mat and mat.use_nodes:
        for n in mat.node_tree.nodes:
            if n.type == "TEX_IMAGE" and n.image:
                out.append(os.path.basename(n.image.filepath))
    return out


def id_colour(i, n):
    h = (i * 0.61803398875) % 1.0
    r, g, b = colorsys.hsv_to_rgb(h, 0.75, 0.95)
    return r, g, b


def id_render(objs, key_fn, out_path, legend_path, views):
    """Flat colour render, one colour per key_fn(obj) value."""
    keys = sorted({key_fn(o) for o in objs})
    colours = {k: id_colour(i, len(keys)) for i, k in enumerate(keys)}
    mats = {}
    for k, c in colours.items():
        m = bpy.data.materials.new(f"_id_{k}")
        m.use_nodes = True
        nt = m.node_tree
        for n in list(nt.nodes):
            nt.nodes.remove(n)
        em = nt.nodes.new("ShaderNodeEmission")
        em.inputs["Color"].default_value = (*c, 1.0)
        em.inputs["Strength"].default_value = 1.0
        outn = nt.nodes.new("ShaderNodeOutputMaterial")
        nt.links.new(em.outputs[0], outn.inputs[0])
        mats[k] = m
    saved = {}
    for o in objs:
        saved[o] = [s.material for s in o.material_slots]
        k = key_fn(o)
        for s in o.material_slots:
            s.material = mats[k]
        if not o.material_slots:
            o.data.materials.append(mats[k])
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.samples = 1
    sc.cycles.use_denoising = False
    sc.view_settings.view_transform = "Standard"
    world = bpy.data.worlds.new("_id_world")
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.08, 0.08, 0.08, 1)
    sc.world = world
    for name, (loc, tgt, lens) in views.items():
        P.camera(loc, tgt, lens)
        sc.render.resolution_x, sc.render.resolution_y = 1400, 800
        sc.render.filepath = out_path.replace(".png", f"_{name}.png")
        bpy.ops.render.render(write_still=True)
    for o, ms in saved.items():
        for s, m in zip(o.material_slots, ms):
            s.material = m
    from PIL import Image, ImageDraw
    rows = len(keys)
    img = Image.new("RGB", (520, 18 * rows + 10), (20, 20, 20))
    d = ImageDraw.Draw(img)
    for i, k in enumerate(keys):
        c = tuple(int(255 * v ** (1 / 2.2)) for v in colours[k])
        d.rectangle([8, 6 + 18 * i, 28, 20 + 18 * i], fill=c)
        d.text((36, 5 + 18 * i), str(k)[:70], fill=(235, 235, 235))
    img.save(legend_path)


def main():
    src, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=src)
    objs = [o for o in bpy.context.scene.objects]
    meshes = [o for o in objs if o.type == "MESH"]
    inv = []
    for o in objs:
        row = {"name": o.name, "type": o.type, "parent": o.parent.name if o.parent else None,
               "location": [round(v, 3) for v in o.matrix_world.translation]}
        if o.type == "MESH":
            lo, hi = world_bounds(o)
            n_loose, biggest = loose_parts(o)
            row.update({
                "tris": tri_count(o),
                "verts": len(o.data.vertices),
                "size": [round(v, 3) for v in (hi - lo)],
                "centre": [round(v, 3) for v in (lo + hi) / 2],
                "materials": [{"name": m.name, "textures": material_textures(m)} if m else None for m in o.data.materials],
                "loose_parts": n_loose,
                "largest_loose_parts": biggest,
                "uv_layers": len(o.data.uv_layers),
            })
        inv.append(row)
    with open(os.path.join(out, "inventory.json"), "w") as f:
        json.dump(inv, f, indent=1)
    lines = ["| object | parent | tris | size x y z | centre x y z | loose | materials |", "|---|---|---|---|---|---|---|"]
    for r in sorted(inv, key=lambda r: -r.get("tris", -1)):
        if r["type"] != "MESH":
            continue
        mats = ", ".join(f"{m['name']}[{' '.join(m['textures'])}]" if m else "none" for m in r["materials"])
        lines.append(f"| {r['name']} | {r['parent'] or ''} | {r['tris']} | {' '.join(str(v) for v in r['size'])} | "
                     f"{' '.join(str(v) for v in r['centre'])} | {r['loose_parts']} | {mats} |")
    lines.append("")
    lines.append("Empties: " + ", ".join(f"{r['name']} at {r['location']}" for r in inv if r["type"] == "EMPTY"))
    with open(os.path.join(out, "inventory.md"), "w") as f:
        f.write("\n".join(lines))
    views = {"front34": ((5.2, -6.6, 1.9), (0.0, 0.0, 0.9), 40), "rear34": ((-5.2, 6.6, 1.9), (0.0, 0.0, 0.9), 40),
             "side": ((10.5, 0.0, 1.0), (0.0, 0.0, 0.95), 48), "top": ((0.0, 0.01, 12.0), (0.0, 0.0, 0.0), 40)}
    id_render(meshes, lambda o: o.name, os.path.join(out, "id_object.png"), os.path.join(out, "legend_object.png"), views)
    id_render(meshes, lambda o: (o.data.materials[0].name if o.data.materials and o.data.materials[0] else "none"),
              os.path.join(out, "id_material.png"), os.path.join(out, "legend_material.png"), views)
    print(f"{len(meshes)} meshes, {sum(tri_count(o) for o in meshes)} triangles, inventory written to {out}", flush=True)


if __name__ == "__main__":
    main()
