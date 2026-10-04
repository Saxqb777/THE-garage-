"""Rectify the left side reference photo into an orthographic side view.

Uses the two alloy rims as known references: rim flange diameter 0.44 m,
wheel centre 0.38 m above ground, axles 2.85 m apart. Output: a side view in
car coordinates (u = metres behind the front axle, z = metres above ground)
with a metric grid, for reading door lines, pillars, badges and lamps.
"""
import sys
import numpy as np
from PIL import Image, ImageDraw

SRC = "reference/photos/side_left.webp"
OUT = sys.argv[1] if len(sys.argv) > 1 else "side_rectified.png"

WB = 2.85
HUB_Z = 0.38
RIM_R = 0.22
# pixel coordinates read off zoomed crops (see reference notes)
pts_img = np.array([[550, 949], [550, 1158], [1641, 859], [1641, 1017]], float)
pts_car = np.array([[0, HUB_Z + RIM_R], [0, HUB_Z - RIM_R], [WB, HUB_Z + RIM_R], [WB, HUB_Z - RIM_R]], float)


def homography(src, dst):
    rows = []
    for (x, y), (X, Y) in zip(src, dst):
        rows.append([x, y, 1, 0, 0, 0, -X * x, -X * y, -X])
        rows.append([0, 0, 0, x, y, 1, -Y * x, -Y * y, -Y])
    _, _, vt = np.linalg.svd(np.array(rows))
    h = vt[-1].reshape(3, 3)
    return h / h[2, 2]


H_car2img = homography(pts_car, pts_img)
H_img2car = np.linalg.inv(H_car2img)


def img2car(x, y):
    p = H_img2car @ np.array([x, y, 1.0])
    return p[0] / p[2], p[1] / p[2]


if __name__ == "__main__":
    S = 0.004  # metres per output pixel
    U0, U1, Z0, Z1 = -1.25, 4.25, -0.05, 2.05
    W, Hh = int((U1 - U0) / S), int((Z1 - Z0) / S)
    # output pixel -> car coords -> image pixel
    A = np.array([[S, 0, U0], [0, -S, Z1], [0, 0, 1]])
    M = H_car2img @ A
    M = M / M[2, 2]
    coeffs = (M[0, 0], M[0, 1], M[0, 2], M[1, 0], M[1, 1], M[1, 2], M[2, 0], M[2, 1])
    src = Image.open(SRC).convert("RGB")
    out = src.transform((W, Hh), Image.PERSPECTIVE, coeffs, Image.BICUBIC)
    d = ImageDraw.Draw(out)
    for i in range(int(U0 * 10), int(U1 * 10) + 1):
        u = i / 10
        x = (u - U0) / S
        major = i % 5 == 0
        d.line([(x, 0), (x, Hh)], fill=(255, 0, 0) if major else (255, 190, 190), width=1)
        if major:
            d.text((x + 2, 2), f"{u:.1f}", fill=(255, 0, 0))
    for i in range(int(Z0 * 10), int(Z1 * 10) + 1):
        z = i / 10
        y = (Z1 - z) / S
        major = i % 5 == 0
        d.line([(0, y), (W, y)], fill=(0, 0, 255) if major else (190, 190, 255), width=1)
        if major:
            d.text((2, y + 2), f"{z:.1f}", fill=(0, 0, 255))
    out.save(OUT)
    # sanity checks: beltline should map to one height front and rear
    for label, (x, y) in {"belt_front": (872, 652), "belt_rear": (1785, 606), "bumper_tip": (112, 900), "rear_end": (1918, 790)}.items():
        u, z = img2car(x, y)
        print(f"{label}: u={u:.3f} z={z:.3f}")
