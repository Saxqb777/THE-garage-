"""Overlay the body SDF silhouette on the rectified side photo and the blueprint.

Usage: python3 scripts/reference/check_silhouette.py OUT_DIR
Writes side_overlay.png (rectified photo with the SDF outline in red),
plus top_view.png and front_view.png silhouettes of the SDF.
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from blender.parts import body_sdf as S  # noqa: E402
from scripts.reference import rectify_side as R  # noqa: E402

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
h = 0.01


def occupancy(fn, a_range, b_range, c_range, axes):
    A = np.arange(*a_range, h)
    B = np.arange(*b_range, h)
    Cc = np.arange(*c_range, 0.02)
    occ = np.zeros((len(B), len(A)), bool)
    for c in Cc:
        aa, bb = np.meshgrid(A, B)
        cc = np.full_like(aa, c)
        coords = {axes[0]: aa, axes[1]: bb, axes[2]: cc}
        occ |= fn(coords["u"], coords["x"], coords["z"]) < 0
    return A, B, occ


def combined(u, x, z):
    return np.minimum(np.minimum(S.body(u, x, z), S.front_bumper(u, x, z)), S.rear_bumper(u, x, z))


# side view over the rectified photo (4 mm per px, u from minus 1.25, z top 2.05)
U, Z, occ = occupancy(combined, (-1.25, 4.25), (-0.05, 2.05), (-1.0, 1.0), ("u", "z", "x"))
photo = Image.open(os.path.join(out, "side_rect.png")).convert("RGB") if os.path.exists(os.path.join(out, "side_rect.png")) else None
if photo is not None:
    d = ImageDraw.Draw(photo)
    edge = occ ^ np.roll(occ, 1, 0) | occ ^ np.roll(occ, 1, 1)
    ys, xs = np.nonzero(edge)
    for y, x in zip(ys, xs):
        px = (U[x] - (-1.25)) / 0.004
        py = (2.05 - Z[y]) / 0.004
        d.rectangle([px - 1, py - 1, px + 1, py + 1], fill=(255, 0, 0))
    # wheels for reference
    for uc in (0.0, 2.85):
        cx, cy = (uc + 1.25) / 0.004, (2.05 - 0.385) / 0.004
        r = 0.3955 / 0.004
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(0, 200, 255), width=2)
    photo.save(os.path.join(out, "side_overlay.png"))
Image.fromarray((~occ[::-1] * 255).astype(np.uint8)).save(os.path.join(out, "side_view.png"))

U, X, occ = occupancy(combined, (-1.0, 4.1), (-1.1, 1.1), (0.0, 1.9), ("u", "x", "z"))
Image.fromarray((~occ * 255).astype(np.uint8)).save(os.path.join(out, "top_view.png"))
X, Z, occ = occupancy(combined, (-1.1, 1.1), (0.0, 1.95), (-1.0, 4.1), ("x", "z", "u"))
Image.fromarray((~occ[::-1] * 255).astype(np.uint8)).save(os.path.join(out, "front_view.png"))
print("done")
