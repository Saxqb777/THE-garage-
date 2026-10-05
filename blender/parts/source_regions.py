"""Where every part of the LC100 2006 source model lives, in our frame (metres, Z up, car faces -Y,
left is +X, origin on the ground midway between the axles).

All numbers were read off orthographic depth scans of the normalised model (blender/lib/scan.py),
not off photos. Side view polylines are (y, z) for the left side; the right side is mirrored.
"""

# Panel gap lines, left side, (y, z)
A_LINE = [(-0.830, 0.30), (-0.830, 1.00), (-0.816, 1.05), (-0.800, 1.12), (-0.780, 1.18), (-0.730, 1.25),
          (-0.685, 1.30), (-0.490, 1.50), (-0.372, 1.60), (-0.170, 1.80), (-0.100, 1.95)]
B_LINE = [(0.252, 0.30), (0.252, 1.95)]
REAR_DOOR_LINE = [(0.920, 0.30), (0.930, 0.60), (0.956, 0.75), (1.020, 0.85), (1.170, 0.95), (1.216, 1.05),
                  (1.190, 1.25), (1.120, 1.80), (1.100, 1.95)]
DOOR_BOTTOM = 0.36          # doors reach the sill on the GXR; the model's cladding band becomes door skin
DOOR_SIDE_X = 0.62          # outboard of the roof drip rail counts as door, inboard is roof
REAR_DOOR_GLASS_SPLIT_Y = 1.0   # division bar between the drop glass and the fixed quarter glass

HOOD_REAR_Y = -0.975
HOOD_SIDE_X = 0.845
HOOD_FRONT_Z = 1.06

# Boxes: (x0, x1, y0, y1, z0, z1), left side where it matters; mirrored for the right
HEADLAMP = (0.45, 0.98, -2.60, -1.94, 0.85, 1.075)
TAILLAMP = (0.60, 1.00, 2.24, 2.65, 0.77, 1.225)
GRILLE = (-0.62, 0.62, -2.60, -2.05, 0.84, 1.16)
FRONT_BUMPER_Y1 = -1.84
REAR_BUMPER_Y0 = 2.20
BUMPER_Z1 = 0.80
MIRROR = (0.86, 1.25, -0.90, -0.52, 1.18, 1.46)
HANDLE_FRONT = (0.94, 1.10, -0.13, 0.19, 1.060, 1.165)
HANDLE_REAR = (0.94, 1.10, 0.80, 1.12, 1.110, 1.215)
FUEL_LID = (0.90, 1.10, 1.905, 2.065, 1.025, 1.195)
QUARTER_BADGE = (0.90, 1.10, 1.88, 2.22, 1.285, 1.335)
SIDE_REPEATER = (0.90, 1.10, -1.00, -0.80, 1.00, 1.10)
WINDSHIELD = (-0.95, 0.95, -0.95, -0.28, 1.18, 1.78)
SUNROOF = (-0.52, 0.52, -0.06, 0.44, 1.78, 1.95)
REAR_GLASS = (-0.90, 0.90, 2.20, 2.65, 1.20, 1.87)
REAR_WIPER = (-0.62, 0.62, 2.30, 2.65, 1.20, 1.90)
FRONT_WIPERS = (-0.98, 0.98, -1.22, -0.88, 1.10, 1.34)
REAR_EMBLEM = (-0.16, 0.16, 2.35, 2.65, 1.235, 1.295)
REAR_GARNISH = (-0.43, 0.43, 2.35, 2.65, 1.165, 1.245)
GRADE_BADGE = (0.50, 0.70, 2.30, 2.65, 0.82, 0.92)
# rear face outline of the tailgate skin, (|x|, z); the barn doors split it at x = 0
BACK_DOOR_OUTLINE = [(0.0, 0.775), (0.62, 0.775), (0.62, 1.215), (0.80, 1.30), (0.80, 1.86), (0.0, 1.86)]
BACK_DOOR_Y0 = 2.26
MUDGUARD_FRONT_Y = (-1.50, -1.25)
MUDGUARD_REAR_Y = (1.42, 1.70)

# seats: front row ahead of this y, rear bench behind
SEAT_SPLIT_Y = 0.70

# Side cladding and steps: faces further out than this are the running board and go
CLADDING_STEP_X = 0.985
