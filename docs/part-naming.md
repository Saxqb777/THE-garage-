# Part naming spec

Every mesh and every assembly node in every GLB is named with a part key. The same key is the primary key in the parts table, the search result id and the deep link slug. One key everywhere.

## Pattern

`SYSTEM_GROUPCODE_part_name_side`

| Token | Rule |
| --- | --- |
| SYSTEM | One of BODY, DOOR, GLASS, WHEEL, SUSP, BRAKE, ENG, COOL, EXH, TRANS, DRIVE, ELEC, INT, AC, LIGHT, TRIM |
| GROUPCODE | Four digit Toyota EPC illustration group. `0000` when unknown, and the part is flagged |
| part_name | Lower case words joined by underscores, following the Toyota part name where one exists. Position words like front, rear, outside belong here |
| side | Optional last token in capitals: `L` (vehicle left, the driver side on this LHD car), `R` (vehicle right), `F` (front), `RR` (rear) |

Regular expression used by the validators:

```
^(BODY|DOOR|GLASS|WHEEL|SUSP|BRAKE|ENG|COOL|EXH|TRANS|DRIVE|ELEC|INT|AC|LIGHT|TRIM)_(\d{4})_([a-z0-9]+(?:_[a-z0-9]+)*?)(?:_(L|R|F|RR))?$
```

Examples: `DOOR_6751_front_door_L`, `ENG_1903_alternator`, `BRAKE_4705_front_disc_brake_pad`, `WHEEL_0000_tire_rear_R`.

## Rules

* Left and right are the vehicle's own sides, as if sitting in the driver seat.
* Prefer front and rear as words in part_name (as Toyota does: "front door", "rear door"). Use the `F` and `RR` side tokens only for a front and rear pair whose Toyota name has no position word. No M1 part needs them.
* Corner parts combine both: `WHEEL_0000_tire_front_L`.
* Assemblies are nodes that group parts that move together (a wheel assembly spins and steers as one). They use the same pattern with `assembly` in part_name, for example `WHEEL_0000_wheel_assembly_front_L`.
* A part that moves with another part is its child in the GLB: the mirror, glass and handles are children of their door, wiper blades are children of their arms.
* Every part node carries glTF extras: `partKey` (same as its name). Hinged parts also carry `hingeAxis` and `openDeg` and have their origin on the hinge line.
* Material names are not part keys. They are shared material keys (paint_white, glass_clear, chrome and so on), listed in blender/lib/materials.py.

## Group code status

Each part in src/data/parts.m1.json has a `groupStatus`:

* `verified`: the group appears in the Toyota EPC group index for this exact variant (FZJ100, 1FZ-FE, GX, 5 speed manual, LHD, GCC), saved in reference/epc/fzj100_gcc_gx_mtm_groups.json. Checked at variant level, not per VIN.
* `recalled`: from memory of the Toyota EPC structure, must be checked. None left in the contract.
* `unknown`: code is `0000`, because the variant's catalogue has no single group for the part (body shell, tires, wheel assemblies) or the GX does not list it (mudguards, side steps, fuel filler lid).

On 2026-10-05 the keys were re-keyed from recalled to verified codes (for example front door 6701 became 6751, rear combination lamp 8105 became 8111, front bumper 5201 became 5252) before the database was seeded. Keys are now frozen: they are the database primary keys and the deep link slugs. A later change needs a migration of the parts table and redirects for old links.

## M1 part list

The authoritative list is src/data/parts.m1.json (75 entries). Summary:

| System | Parts |
| --- | --- |
| BODY | body shell, hood, front fenders L R, front bumper, rear bumper, radiator grille, outer mirrors L R, fuel filler lid, mudguards front and rear L R, side steps L R |
| DOOR | front doors L R, rear doors L R, back (barn) doors L R, outside handles front and rear L R |
| GLASS | windshield, front door glass L R, rear door glass L R, rear door quarter glass L R, quarter window glass L R, back door glass L R |
| LIGHT | headlamps L R, rear combination lamps L R, side turn signal lamps L R |
| WHEEL | 4 wheel assemblies, each with a disc wheel and a tire |
| TRIM | front emblem, back door emblem, LAND CRUISER name plate, G badge, 4500 EFI badges L R |
| ELEC | front wiper arms and blades L R, rear wiper arms and blades L R |
| INT | placeholders: instrument panel, steering wheel, front seats L R, rear seat, floor carpet |

## Hinges (three.js space, positive angle opens)

| Part | Hinge line | Axis | Open |
| --- | --- | --- | --- |
| Hood | rear edge, across the car | `[-1, 0, 0]` | 55 degrees |
| Front and rear doors, left | front edge, vertical | `[0, -1, 0]` | 68 degrees |
| Front and rear doors, right | front edge, vertical | `[0, 1, 0]` | 68 degrees |
| Back door left | outer left edge, vertical | `[0, -1, 0]` | 88 degrees |
| Back door right | outer right edge, vertical | `[0, 1, 0]` | 88 degrees |

## Validation

`python3 blender/lib/naming.py` checks the contract. The export step checks every node in the scene against it and fails loudly on any name that is not in the contract.
