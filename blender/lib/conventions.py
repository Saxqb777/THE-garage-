"""Shared vehicle constants and coordinate helpers for every Blender script.

Blender space: metres, Z up, the car faces -Y, the vehicle's left side is +X.
Origin: on the ground, midway between the front and rear axles.

Most body measurements are easier to think about as `u`: metres behind the
front axle (front axle u = 0, rear axle u = WHEELBASE). Use `y_from_u` to
convert.
"""

WHEELBASE = 2.85
FRONT_OVERHANG = 0.905
REAR_OVERHANG = 1.135
LENGTH = FRONT_OVERHANG + WHEELBASE + REAR_OVERHANG  # 4.89
BODY_HALF_WIDTH = 0.94  # door skin, widest point (no wheel arch flares on this car)
ROOF_HEIGHT = 1.835  # no roof rails on this car

TRACK_FRONT = 1.62  # owner's manual p.324
TRACK_REAR = 1.615  # owner's manual p.324
TIRE_OUTER_RADIUS = 0.3955  # 275/70R16
TIRE_LOADED_RADIUS = 0.385
WHEEL_CENTER_Z = TIRE_LOADED_RADIUS
TIRE_WIDTH = 0.275
RIM_DIAMETER = 16 * 0.0254
RIM_WIDTH = 8 * 0.0254

U_FRONT_AXLE = 0.0
U_REAR_AXLE = WHEELBASE
U_FRONT_END = -FRONT_OVERHANG
U_REAR_END = WHEELBASE + REAR_OVERHANG


def y_from_u(u):
    return u - WHEELBASE / 2.0


def u_from_y(y):
    return y + WHEELBASE / 2.0


def wheel_centres():
    """Blender space centres of the four wheels, keyed by position token."""
    return {
        "front_L": (TRACK_FRONT / 2, y_from_u(U_FRONT_AXLE), WHEEL_CENTER_Z),
        "front_R": (-TRACK_FRONT / 2, y_from_u(U_FRONT_AXLE), WHEEL_CENTER_Z),
        "rear_L": (TRACK_REAR / 2, y_from_u(U_REAR_AXLE), WHEEL_CENTER_Z),
        "rear_R": (-TRACK_REAR / 2, y_from_u(U_REAR_AXLE), WHEEL_CENTER_Z),
    }
