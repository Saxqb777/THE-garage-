# The Garage: project memory

Read this first in every session. Keep it current: when a decision is made, log it in docs/decisions.md and update the state section below.

## What this is

* Interactive, game like, photoreal 3D car experience in the browser. Every visible part is clickable, searchable, explodable, and links to an OEM part card with a WhatsApp order button.
* For Land Cruiser spare parts shops in the UAE. Owner: Saaqib. Personal project, built like a product.
* First car: 2005 Toyota Land Cruiser 100, GCC, 1FZ-FE 4.5 inline 6 petrol, 5 speed manual, LHD, white.

## Working rules (from Saaqib, no exceptions)

* Never implement, delete, refactor or install anything without presenting the plan and getting an explicit "go".
* Small steps. Each step: what, the exact change, how to know it worked. Then stop and wait (unless Saaqib said "go for all").
* Ask for files, credentials, decisions directly and specifically. No silent placeholders.
* Casual tone, short messages, bullets. Long explanations only when asked.
* Markdown and docs for this project: no hyphens and no em dashes in prose. Colons are fine. Package names and file paths are exempt.
* Say plainly when something is impossible or a bad idea, before doing it.
* Model switching: Blender geometry, shader tuning against photos, explode logic, camera choreography and performance debugging are better on Fable. Say "This step is better on Fable. Switch me, then say go." and wait. Routine work: just continue. Never assume which model you are; check.

## Environment notes

* Cloud container, wiped between sessions. Commit and push everything worth keeping to branch `claude/loving-brown-8dzpi5`.
* Network: npm and PyPI work. Blender's site, Poly Haven, Partsouq, Amayama, Megazip, Sketchfab and usermanuals.au are blocked by the environment network policy (Saaqib can allow domains in the environment settings).
* Blender: installed as a Python module, `pip install --break-system-packages bpy==4.5.14 pillow numpy scipy scikit-image pymeshlab` and `apt-get install -y libopengl0` (pymeshlab's filters need it). Run Blender scripts with `python3 blender/<script>.py`. Cycles CPU renders work headless; EEVEE does not.
* Build the car: `python3 blender/build_lc100.py` writes public/models/lc100.glb and lc100.report.json (about 5 minutes).
* Parked ground shadow: after a build saved with `--blend <file>`, run `python3 blender/bake_ground_shadow.py <file>` (about 2 minutes). It writes public/textures/lc100_ground_shadow.png and src/data/groundShadow.json. Rebake whenever the body shape changes.
* Screenshots: `node scripts/screenshot.mjs "<url>" out.png 1400x800`. URL params: scene (garage, dunes, corniche_night, highway, desert_road), tod (0 to 1), lights (on, off), part (a part key), xray (1), hinges (open), cam, look, fov, debug (exposes window.__r3f). Set SHOT_LOAD_MS for slow loads. Photo comparisons: `python3 blender/compare_photos.py <blend> <out dir>`.
* Decimation goes through MeshLab (quadric, normals preserved). Blender's own collapse decimation folds triangles in flat areas, which shows as shards through glass.
* Sending a message while a long command runs cancels that command; long builds run in the background.
* Chromium for screenshots lives in /opt/pw-browsers.

## Conventions (the backbone)

* Part keys: `SYSTEM_GROUPCODE_part_name_side`, spec in docs/part-naming.md. One key everywhere: mesh name = DB primary key = search result = deep link slug.
* Contract: src/data/parts.m1.json lists every part key, its parent, and hinge data. Blender scripts and the app both read it.
* Blender space: metres, Z up, car faces `-Y`, vehicle left = `+X`, origin on the ground midway between the axles. glTF/three.js: Y up, car faces `+Z`, left = `+X`.
* Shared Blender code: blender/lib (conventions, materials, naming). Material names are stable keys the app can override.
* Hinged parts have their origin on the hinge line and carry glTF extras `partKey`, `hingeAxis` (three.js space), `openDeg`.

## Where things are

* reference/: photos, blueprint, manual page (small, committed).
* docs/reference-notes.md: measurements and differences between the brief and the real car.
* docs/decisions.md: decisions log.
* blender/: build pipeline scripts; blender/parts: part builders.
* public/models: compressed GLBs. src/scene: R3F. src/ui: HUD. src/data: contract and seed data.

## Current state

* M4 (interaction) first half done: hover outline and name label, click opens the part card (src/ui/PartCard.tsx), hinged parts open and close one by one on click, X Ray mode (X key), deep link ?part=KEY, Escape or a click on empty space closes the card. Picking uses drei Bvh (three-mesh-bvh ships with drei). Second half waits for Fable: Get In, camera presets, Lift Mode (camera choreography).
* M3 (environments) done pending Saaqib's review: the four scenes from the brief plus a spare (Garage, Liwa Dunes, Corniche Night, Sheikh Zayed Road, Desert Road), all data in src/scene/scenes.ts. Own ground projected sky dome (src/scene/SkyDome.tsx) with per scene yaw and floor offset, sun placed from each HDRI's measured sun, baked parked shadow plus live sun shadow, time of day slider, night mode (headlamps, red tail lamps, dash, headlight beams, wet road), HUD switcher with keys 1 to 5, H and L. Screens in docs/screens/m3_*.jpg.
* M2 (look pass) done pending Saaqib's review: set 2 geometry (stripes, lip spoiler, steps, chrome garnish, chrome handles), physical materials with dust and orange peel (src/scene/car/look.ts), post FX (bloom, ACES, vignette, SMAA), six spoke 16 inch alloys (blender/parts/wheel6.py), matched photo comparisons in docs/screens/cmp_m2_*.png. 74 parts, 7.2 MB GLB.
* Open polish items (deferred by Saaqib, "define later"): dark eyebrow strip over the headlamps (dark faces at the top of the lamp recess, not a separate part), a textured plate remnant behind the chrome door handles, the car reads as floating in the HDRI garage (floor perspective of the ground projected dome plus a faint contact shadow), dome edge, sunroof is a recessed paint patch, model artist credit still a placeholder.
* M1 history: The car is Saaqib's CC BY 4.0 LC100 2006 model (reference/model/lc100_2006_cc_by, licence note there, artist name still to come), converted to GXR spec by blender/parts/source_convert.py: VXR steps, spoiler, stripes and mod junk removed, tailgate split into barn doors, our wheels, black grille and mirrors, grey cloth interior. The procedural stand in (blender/parts/body*.py) stays as a fallback: `python3 blender/build_lc100.py --source procedural`.
* Source model facts: wheelbase 2.902 scaled to 2.85, 345k triangles, body is one triangle soup so parts are cut along measured gap lines (blender/parts/source_regions.py). Inventory and scan tools: blender/inspect_source.py, blender/lib/scan.py.
