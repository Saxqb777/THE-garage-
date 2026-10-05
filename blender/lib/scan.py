"""Orthographic depth scans of a set of meshes, for finding panel gaps and placing cuts.

Rays are cast along a view axis over a regular grid; the result is a depth image (metres from
the near plane), a hit mask and the hit normals. Panel gaps show as thin lines of extra depth.
"""
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

import bmesh

VIEWS = {
    # name: (ray direction, u axis, v axis) in Blender space; u is the image x, v the image y (up)
    "left": ((-1, 0, 0), (0, 1, 0), (0, 0, 1)),
    "right": ((1, 0, 0), (0, -1, 0), (0, 0, 1)),
    "top": ((0, 0, -1), (0, 1, 0), (1, 0, 0)),
    "front": ((0, 1, 0), (-1, 0, 0), (0, 0, 1)),
    "rear": ((0, -1, 0), (1, 0, 0), (0, 0, 1)),
}


def bvh_from_objects(objs):
    bm = bmesh.new()
    for o in objs:
        tmp = bmesh.new()
        tmp.from_mesh(o.data)
        tmp.transform(o.matrix_world)
        me = o.data.copy()
        tmp.to_mesh(me)
        tmp.free()
        bm.from_mesh(me)
        import bpy
        bpy.data.meshes.remove(me)
    tree = BVHTree.FromBMesh(bm)
    return tree, bm


def depth_scan(objs, view, u_range, v_range, step, start_dist=6.0):
    """Return (depth, normals, hit, us, vs). depth is distance from the start plane in metres."""
    d, ua, va = (Vector(v) for v in VIEWS[view])
    us = np.arange(u_range[0], u_range[1] + step * 0.5, step)
    vs = np.arange(v_range[0], v_range[1] + step * 0.5, step)
    tree, bm = bvh_from_objects(objs)
    depth = np.full((len(vs), len(us)), np.nan, np.float32)
    normals = np.zeros((len(vs), len(us), 3), np.float32)
    origin_base = -d * start_dist
    for j, v in enumerate(vs):
        for i, u in enumerate(us):
            origin = origin_base + ua * u + va * v
            hit = tree.ray_cast(origin, d, start_dist * 2)
            if hit[0] is not None:
                depth[j, i] = hit[3]
                normals[j, i] = hit[1][:]
    bm.free()
    return depth, normals, ~np.isnan(depth), us, vs


def gap_mask(depth, step_mm=2.0, window=9):
    """Pixels noticeably deeper than their neighbourhood median: panel gaps and seams."""
    from scipy.ndimage import median_filter
    filled = np.where(np.isnan(depth), np.nanmax(depth), depth)
    med = median_filter(filled, size=window)
    return (filled - med) > step_mm / 1000.0


def save_depth_image(depth, hit, us, vs, path, grid=0.1, label_every=0.5, gaps=None):
    from PIL import Image, ImageDraw
    d = depth.copy()
    d[~hit] = np.nan
    lo, hi = np.nanpercentile(d, 1), np.nanpercentile(d, 99)
    img = np.clip((d - lo) / max(hi - lo, 1e-6), 0, 1)
    img = (255 * (1 - img)).astype(np.uint8)
    img[~hit] = 20
    rgb = np.stack([img, img, img], axis=-1)
    if gaps is not None:
        rgb[gaps & hit] = (255, 60, 60)
    im = Image.fromarray(rgb[::-1])  # v up
    draw = ImageDraw.Draw(im)
    step = us[1] - us[0]
    for u in np.arange(np.ceil(us[0] / grid) * grid, us[-1], grid):
        x = (u - us[0]) / step
        major = abs(u / label_every - round(u / label_every)) < 1e-6
        draw.line([(x, 0), (x, im.height)], fill=(0, 120, 255) if major else (150, 180, 255), width=1)
        if major:
            draw.text((x + 2, 2), f"{u:.1f}", fill=(0, 90, 255))
    for v in np.arange(np.ceil(vs[0] / grid) * grid, vs[-1], grid):
        y = im.height - 1 - (v - vs[0]) / step
        major = abs(v / label_every - round(v / label_every)) < 1e-6
        draw.line([(0, y), (im.width, y)], fill=(255, 120, 0) if major else (255, 200, 150), width=1)
        if major:
            draw.text((2, y + 2), f"{v:.1f}", fill=(255, 90, 0))
    im.save(path)
    return im
