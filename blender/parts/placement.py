"""Places the small parts from blender/parts/details.py onto the procedural body.

Positions come from docs/reference-notes.md (side view u, z and rear view x, z). Each part is
oriented from the body SDF normal at its mounting point so badges and handles sit flush.
"""
import numpy as np
from mathutils import Matrix, Vector

from blender.lib import conventions as C
from blender.lib import meshing as M
from blender.parts import body_sdf as S
from blender.parts import details as D

HALF_WB = C.WHEELBASE / 2.0


def skin_u_rear(x, z):
    """Rear skin position u at (x, z), by bisection on the body field."""
    lo, hi = 3.4, 4.2
    for _ in range(40):
        mid = 0.5 * (lo + hi)
        d = S.body(np.array([mid]), np.array([x]), np.array([z]))[0]
        if d > 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def normal_at(co):
    return Vector(M.sdf_vertex_normals(S.body, np.array([co]))[0])


def basis(facing, normal, up=Vector((0, 0, 1))):
    """Rotation matrix taking the part's local `facing` axis onto `normal`, local Z towards `up`."""
    n = normal.normalized()
    zv = (up - up.dot(n) * n).normalized()
    if facing in ("+Y", "-Y"):
        y = n if facing == "+Y" else -n
        x = y.cross(zv)
        cols = (x, y, zv)
    else:
        xv = n if facing == "+X" else -n
        y = zv.cross(xv)
        cols = (xv, y, zv)
    m = Matrix((cols[0], cols[1], cols[2])).transposed()
    return m.to_4x4()


def place(obj, co, rot):
    obj.matrix_world = Matrix.Translation(Vector(co)) @ rot


def blender_co(u, x, z):
    return (x, u - HALF_WB, z)


def place_all(objs, skin_x):
    out = {}

    # grille sits in the front opening, scaled to the opening height
    grille = D.build_grille()
    emblem = next((c for c in grille.children if c.name == "TRIM_0000_front_emblem"), None)
    k = 0.228 / 0.25
    grille.data.transform(Matrix.Diagonal((1.0, 1.0, k, 1.0)))
    if emblem is not None:
        emblem.location.z *= k
    grille.location = blender_co(S.U_FRONT + 0.04, 0.0, 0.976)
    out[grille.name] = grille
    if emblem is not None:
        out[emblem.name] = emblem

    # badges
    badges = D.build_badges()
    for key, (x, z) in {"TRIM_0000_back_door_name_plate": (0.41, 1.165),
                        "TRIM_0000_back_door_emblem": (-0.125, 1.272),
                        "TRIM_0000_grade_badge": (-0.62, 1.0)}.items():
        u = skin_u_rear(x, z)
        co = blender_co(u, x, z)
        place(badges[key], co, basis("+Y", normal_at(co)))
        out[key] = badges[key]
    for side, sgn in (("L", 1.0), ("R", -1.0)):
        key = f"TRIM_0000_quarter_badge_{side}"
        u, z = 3.52, 1.29
        co = blender_co(u, sgn * skin_x(u, z), z)
        place(badges[key], co, basis("+X" if side == "L" else "-X", normal_at(co)))
        out[key] = badges[key]

    for side, sgn in (("L", 1.0), ("R", -1.0)):
        facing = "+X" if side == "L" else "-X"
        # mirror on the door's front upper corner, kept level
        m = D.build_mirror(side)
        u, z = 0.76, 1.27
        place(m, blender_co(u, sgn * skin_x(u, z), z), Matrix.Identity(4))
        out[m.name] = m
        # door handles, same height on both doors
        for which, u in (("front", 1.51), ("rear", 2.475)):
            h = D.build_door_handle(which, side)
            z = 1.11
            co = blender_co(u, sgn * skin_x(u, z), z)
            place(h, co, basis(facing, normal_at(co)))
            out[h.name] = h
        # amber side repeater on the front fender
        mk = D.build_side_marker(side)
        u, z = 0.545, 1.07
        co = blender_co(u, sgn * skin_x(u, z), z)
        place(mk, co, basis(facing, normal_at(co)))
        out[mk.name] = mk
        # mudguards hang behind each wheel
        for pos, u, z in (("front", 0.50, 0.50), ("rear", 3.31, 0.70)):
            g = D.build_mudguard(f"{pos}_{side}")
            place(g, blender_co(u, sgn * 0.80, z), Matrix.Identity(4))
            out[g.name] = g

    # front wipers park along the bottom of the windshield, lying on the glass
    n_ws = Vector((0.0, -1.0, S.WS_SLOPE)).normalized()
    x_axis = Vector((1.0, 0.0, 0.0))
    y_axis = n_ws.cross(x_axis)
    rot_ws = Matrix((x_axis, y_axis, n_ws)).transposed().to_4x4()
    for side, x in (("L", 0.55), ("R", -0.05)):
        arm = D.build_wiper("front", side)
        z = 1.29
        u = S.windshield_u(np.array([z]), np.array([abs(x)]))[0] - 0.004
        place(arm, blender_co(u, x, z), rot_ws)
        out[arm.name] = arm
        for c in arm.children:
            out[c.name] = c

    # rear wipers on each back door glass, angled up and outwards
    for side, sgn in (("L", 1.0), ("R", -1.0)):
        arm = D.build_wiper("rear", side)
        x, z = sgn * 0.09, 1.345
        u = skin_u_rear(abs(x), z) - 0.008
        co = blender_co(u, x, z)
        n = normal_at(co)
        zv = n.normalized()
        xv = Vector((sgn, 0.0, 0.0))
        down = zv.cross(xv) if sgn > 0 else xv.cross(zv)
        tilt = np.radians(16.0)
        xv = (xv * np.cos(tilt) - down * np.sin(tilt) * 1.0).normalized()
        yv = zv.cross(xv)
        rot = Matrix((xv, yv, zv)).transposed().to_4x4()
        place(arm, co, rot)
        out[arm.name] = arm
        for c in arm.children:
            out[c.name] = c
    return out
