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
* Network: full internet access since 2026-10-05 (Saaqib opened the policy). Some sites still refuse scripts with their own bot walls (TurboSquid, Free3D, GrabCAD, Printables answer curl with 403): use headless Chromium through the proxy, which needs `--ignore-certificate-errors-spki-list` with the proxy CA pins (compute them from /root/.ccr/ca-bundle.crt), or web search. Respect robots.txt: Megazip disallows its diagram pages.
* Blender: installed as a Python module, `pip install --break-system-packages bpy==4.5.14 pillow numpy scipy scikit-image pymeshlab` and `apt-get install -y libopengl0` (pymeshlab's filters need it). Run Blender scripts with `python3 blender/<script>.py`. Cycles CPU renders work headless; EEVEE does not.
* Build the car: `python3 blender/build_lc100.py` writes public/models/lc100.glb and lc100.report.json (about 5 minutes).
* Parked ground shadow: after a build saved with `--blend <file>`, run `python3 blender/bake_ground_shadow.py <file>` (about 2 minutes). It writes public/textures/lc100_ground_shadow.png and src/data/groundShadow.json. Rebake whenever the body shape changes.
* Screenshots: `node scripts/screenshot.mjs "<url>" out.png 1400x800`. URL params: scene (garage, dunes, corniche_night, highway, desert_road), tod (0 to 1), lights (on, off), part (a part key), xray (1), x (all, a system or an assembly key), hinges (open), cam, look, fov, debug (exposes window.__r3f). Set SHOT_LOAD_MS for slow loads. Photo comparisons: `python3 blender/compare_photos.py <blend> <out dir>`.
* Decimation goes through MeshLab (quadric, normals preserved). Blender's own collapse decimation folds triangles in flat areas, which shows as shards through glass.
* Sending a message while a long command runs cancels that command; long builds run in the background.
* Chromium for screenshots lives in /opt/pw-browsers.
* Parts database: Neon project the-garage (id shy-breeze-90128053, Singapore). The connection string lives only in .env.local as DATABASE_URL (gitignored, so it is gone after a wipe: get it again through the Neon connector, get_connection_string with the pooled endpoint). Rebuild the dataset: `python3 scripts/parts/merge_workflow.py <workflow result json>` then `python3 scripts/parts/build_seed.py data/parts.full.json` (validates, writes src/data/parts.seed.json and data/parts_oem_sheet.csv, upserts Neon; `--no-db` skips the upsert). OEM numbers: Saaqib fills the sheet, then `python3 scripts/parts/import_oem.py data/parts_oem_sheet.csv`.
* WhatsApp: the shop number goes in NEXT_PUBLIC_WHATSAPP_NUMBER (.env.local here, Vercel environment later), digits with country code (a plus or spaces are fine). It is baked in at build time, so redeploy after changing it. Empty means the Get price button is disabled.

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

* Live: https://the-garage-sigma.vercel.app (Vercel project the-garage, team saxqb777s-projects, production branch claude/loving-brown-8dzpi5, so every push redeploys the live site). DATABASE_URL is set in Vercel (sensitive). NEXT_PUBLIC_WHATSAPP_NUMBER is not set yet. Launched 2026-10-05.
* Model v2 (Saaqib: "make the model so much better", exterior and interior only) steps 1 to 5 done pending review: solid doors, barn doors and hood with cards, frames and seals; body frames round every opening, engine bay tub, wheel arch liners (all in blender/parts/panels.py); side windows merged into the doors (68 contract parts); hinge pivots and angles corrected; door animation with check bounce and closing thud; plain paint on the headlamp lips, lower doors and fenders; no mechanical markers; additive X Ray. Screens docs/screens/m8_*.jpg. Known leftovers: small white shards on the roof rails and the A pillar from the source geometry, the grille still as in the source, black torn trim bits inside the A pillar seen from the cabin. HUD redesigned the same day as a job card and instrument cluster (src/app/globals.css shared panel, key, stamp and btn classes; fonts in src/app/layout.tsx), screens docs/screens/m8_hud_*.jpg.
* Build time is about 70 s for the full car now.
* Mechanical 3D parts on hold (Saaqib), they stay as marked locations; focus is exterior and interior.
* M7 (parts and search) done pending Saaqib's review: 313 parts in Neon (74 on the model, 239 marked locations, 40 with a service interval, 13 flagged not on the GXR), all with Arabic names and UAE slang aliases, groups verified against the variant's Toyota catalogue (reference/epc), contract rekeyed (data/rekey_m7.json). Source dataset data/parts.full.json (from data/parts.workflow.json), committed seed fallback src/data/parts.seed.json, API src/app/api/parts/route.ts, types and search in src/data/catalog.ts. Search box at the top (slash focuses it; English, Arabic, slang, OEM digits), flying to a part (src/scene/goTo.ts), distance scaled markers for parts that are not modelled (src/scene/PartHotspots.tsx), catalogue driven part card with Get price on WhatsApp, service interval chips (5k, 10k, 40k, 80k). Screens docs/screens/m7_*.jpg. OEM numbers all pending until Saaqib fills data/parts_oem_sheet.csv; no prices by design. Open for Saaqib: barn doors or lift up tailgate (both door sets are marked as fitting), WhatsApp number, low confidence rows listed in decisions.md.
* M6 (explode and assemble) done pending Saaqib's review: three stages (systems, one system's assemblies, one assembly's parts) in src/scene/explode (rig.ts geometry, Explode.tsx tweens and camera framing), breadcrumb bar src/ui/ExplodeBar.tsx, Explode and Assemble buttons, Esc goes back a stage. State in the URL: ?x=all, ?x=DOOR, ?x=DOOR_6751_front_door_L, plus part=KEY zooms to the part. The address bar always holds the current deep link (scene, x, part, xray).
* M5 (rev and HUD) done pending Saaqib's review: engine model src/engine/sim.ts (cold start fast idle, limiter bounce, torque roll, idle rock, first gear on the lift spins the wheels), Web Audio sound src/engine/audio.ts (engine loops crossfaded by rpm, throttle filter, synthesized starter crank), instrument cluster src/ui/Dash.tsx (spring needles, gear, speed, fuel, coolant, odometer, scene). Keys: E start or stop, Space rev. window.__engine exposes the engine state for scripted checks.
* M4 (interaction) done pending Saaqib's review: hover outline and label, part card (src/ui/PartCard.tsx), click to open each hinged part, X Ray (X), Get In and Get Out through the driver's door with 21 cabin hotspots numbered as in the owner's manual (src/data/hotspots.interior.json, G key or click the driver's seat), camera presets Hero, Front, Rear, Side, Engine (opens the hood), Interior (rear seat), Under (on the lift in the Garage, ground level elsewhere), two post lift in the Garage (src/scene/Lift.tsx). Camera choreography in src/scene/camera.
* M3 (environments) done pending Saaqib's review: the four scenes from the brief plus a spare (Garage, Liwa Dunes, Corniche Night, Sheikh Zayed Road, Desert Road), all data in src/scene/scenes.ts. Own ground projected sky dome (src/scene/SkyDome.tsx) with per scene yaw and floor offset, sun placed from each HDRI's measured sun, baked parked shadow plus live sun shadow, time of day slider, night mode (headlamps, red tail lamps, dash, headlight beams, wet road), HUD switcher with keys 1 to 5, H and L. Screens in docs/screens/m3_*.jpg.
* M2 (look pass) done pending Saaqib's review: set 2 geometry (stripes, lip spoiler, steps, chrome garnish, chrome handles), physical materials with dust and orange peel (src/scene/car/look.ts), post FX (bloom, ACES, vignette, SMAA), six spoke 16 inch alloys (blender/parts/wheel6.py), matched photo comparisons in docs/screens/cmp_m2_*.png. 74 parts, 7.2 MB GLB.
* Open polish items (deferred by Saaqib, "define later"): GXR mismatches in the source model (automatic gear selector instead of the 5 speed manual stick, V8 engine cover in the bay instead of the 1FZ-FE inline 6, "LAND CRUISER VX.R" text in the lower door decal), a cream box on the dash visible in X Ray, dark eyebrow strip over the headlamps (dark faces at the top of the lamp recess, not a separate part), a textured plate remnant behind the chrome door handles, the car reads as floating in the HDRI garage (floor perspective of the ground projected dome plus a faint contact shadow), dome edge, sunroof is a recessed paint patch, model artist credit still a placeholder.
* M1 history: The car is Saaqib's CC BY 4.0 LC100 2006 model (reference/model/lc100_2006_cc_by, licence note there, artist name still to come), converted to GXR spec by blender/parts/source_convert.py: VXR steps, spoiler, stripes and mod junk removed, tailgate split into barn doors, our wheels, black grille and mirrors, grey cloth interior. The procedural stand in (blender/parts/body*.py) stays as a fallback: `python3 blender/build_lc100.py --source procedural`.
* Source model facts: wheelbase 2.902 scaled to 2.85, 345k triangles, body is one triangle soup so parts are cut along measured gap lines (blender/parts/source_regions.py). Inventory and scan tools: blender/inspect_source.py, blender/lib/scan.py.
