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
* Blender: installed as a Python module, `pip install --break-system-packages bpy==4.5.14` (plus numpy, scipy, scikit-image, pillow). Run Blender scripts with `python3 blender/<script>.py`. Cycles CPU renders work headless; EEVEE does not.
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

* M1 (pipeline) in progress: no free LC100 shell was supplied and download sites are blocked, so the shell is a procedural stand in built in Blender from the blueprint and photos. Phase 2 swaps in a paid model through the same contract.
