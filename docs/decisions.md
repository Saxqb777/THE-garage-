# Decisions log

Newest at the bottom. Each entry: date, decision, why, how to undo.

## 2026-10-04

* Model the car as it is in the photos, not the brief's spec sheet: barn doors, no flares, no side steps, no roof rails, 4500 EFI badge on the rear quarter. Why: photos are the visual target. Undo: add the parts and update docs/reference-notes.md.
* Procedural stand in shell built in Blender from the blueprint and photos, because no free LC100 shell was supplied and the usual download sites are blocked here. Why: unblocks the whole pipeline (naming, pivots, export, app) today. The Phase 2 paid model replaces it through the same contract with zero UI changes.
* One parts contract, src/data/parts.m1.json, read by Blender and the app. Group codes are marked verified, recalled (from memory, needs checking) or unknown (0000). Keys freeze once Saaqib verifies them against the EPC, before any DB seeding or public link.
* More meshes than the brief's 20 to 30 target (about 70): fenders, handles, mirrors, mud flaps, badges and wipers are separate because each is a sellable part. Draw calls stay far below any limit that matters.
* Blender runs as the bpy 4.5 LTS Python module from PyPI, since blender.org downloads are blocked.
* Draco mesh compression (not meshopt) for the GLB, because meshopt quantisation moves node transforms and would shift hinge pivots. Decoder is self hosted in public/draco.
* Garage lighting for M1 uses drei Lightformers (no HDRI download needed). Real HDRIs for the other scenes come in M3 once Poly Haven is reachable or files are supplied.
