# 3D parts sourcing (2026-10-05)

Search across Sketchfab, CGTrader, TurboSquid, Hum3D, Squir, Fab, RenderHub, 3DExport, GrabCAD, Printables, Thingiverse and game mod sites for the mechanical parts the model lacks. Each candidate was opened and checked for licence (commercial use in a public site serving GLB), price, content and LC100 fit. Raw results: data/sourcing.workflow.json (82 kept, 68 dropped with reasons).

## Plan per part

| Part | Route | Pick | Licence |
|---|---|---|---|
| Engine 1FZ-FE (block, head, cam cover, intake, exhaust manifold) | build | Procedural Blender build to 1FZ-FE dimensions (inline 6, 4477 cc, cast iron block, DOHC head with the two piece cam cover and TOYOTA/24 VALVE/EFI style top, long runner intake on the left, cast exhaust manifold on the ri | Own work (build); kitbash source is CC Attribution |
| Gearbox H151F | build | Procedural build: bellhousing, main case, extension housing and shift tower to the H151F outline | Own work. The linked GrabCAD scan is non commercial and is listed only as the exact part that would need the author's pe |
| Transfer case HF2A | build | Procedural build: twin cast halves, front and rear output flanges, centre diff lock actuator | Own work. The GrabCAD scan is non commercial and named only for a permission request |
| Ladder frame | build | Procedural build to the FZJ100 frame (2850 wheelbase, boxed rails, kick ups, crossmembers, body mounts). vr.designer_09 'LADDER FRAME CHASSIS WITH MOUNTING' (CC BY) is a fallback reference for crossmember and mount detai | Own work; fallback CC Attribution (credit: 'LADDER FRAME CHASSIS WITH MOUNTING' by vr.designer_09, CC BY 4.0) |
| Front IFS (upper and lower arms, knuckles, torsion bars, shocks) | build | Procedural build: double wishbone arms, knuckle, longitudinal torsion bars anchored at a frame crossmember, monotube shocks. Generic CC BY 'TORSION BAR' by vr.designer_09 (38,324 faces) only as a detail reference | Own work; reference is CC Attribution |
| Steering rack and linkage | build | Procedural build: rack housing with boots, tie rods, power steering lines, intermediate shaft | Own work. The Printables model (CC BY) is toy geometry and is not recommended |
| Rear axle with differential, 4 links, lateral rod, coil springs, shocks | build | Procedural build: banjo housing with the 9.5 inch style diff cover, 2 upper and 2 lower links, lateral rod, coils, shocks. Rysky '4-Link Suspension' (CC BY) as the topology and explode reference. vr.designer_09 'COIL SPR | Own work; references are CC Attribution |
| Front differential and CV axles | build | Procedural build: frame mounted front diff housing, two CV shafts with boots | Own work. The CGTrader 'Half Axle' ($29.99, RF) is the paid alternative but carries the 21A.3 extraction clause |
| Propeller shafts (front and rear) | free | PolyPhantom 'Driveshaft' (CC BY, 17,330 faces, 5 objects, U joints and slip joint), rescaled to LC100 lengths with the texture cleaned. A procedural build is equally fine | CC Attribution. Credit: 'Driveshaft' by PolyPhantom, CC BY 4.0, modified |
| Front brakes (vented rotor, 4 piston caliper) | build | Rotor: pao1011 'Vented Disk Brake Rotor' (CC BY, 6 hub holes, decimate and convert from inches). Caliper: procedural build of the Toyota cast 4 piston fixed caliper | Rotor CC Attribution (credit: 'Vented Disk Brake Rotor' by pao1011, CC BY 4.0, modified); caliper own work |
| Rear brakes | build | Rotor: the same pao1011 rotor scaled down, or procedural. Caliper: procedural single piston floating caliper with the drum in hat parking brake | CC Attribution for the rotor; own work for the caliper |
| Exhaust system (downpipes, catalytic converters, mid pipe, muffler, tailpipe) | build | Procedural pipe routing along the real path (curve sweeps). Catalytic converter body from the Science Museum Group 'Catalytic converter, 1982-1983' (CC0) if it looks right, otherwise procedural | Own work; the cat body is CC0 Public Domain (no attribution required, credit optional) |
| Fuel tank | build | Procedural build: steel tank with straps and a filler neck to the LC100 dimensions (96 L class main tank, located ahead of the rear axle on the right) | Own work. The CGTrader tank ($40, RF, 21A.3) is not recommended |
| Radiator and fan | free | Core: LadyLionStudios / ACBRadio 'Car Radiator Clean & Rusted' (CC BY, about 6.9k triangles once the backdrop is removed), resized to the LC100 core. Fan clutch, blade and shroud: procedural, since the 1FZ-FE uses an eng | CC Attribution. Credit: 'Car Radiator Clean & Rusted' by ACBRadio (uploaded by LadyLionStudios), CC BY 4.0, modified |
| Alternator | free | B0bik 'Alternator' (CC BY, 147k faces, Hitachi photogrammetry scan): decimate and repaint it clean | CC Attribution. Credit: 'Alternator' by B0bik, CC BY 4.0, modified |
| Starter | free | menarzuw 'ELECTRIC STARTER MOTOR + ANIMATED' (CC BY, named separate parts): keep the outer shell, solenoid and drive end, and drop the internals | CC Attribution. Credit: 'Electric Starter Motor' by menarzuw, CC BY 4.0, modified |
| AC compressor | build | Procedural build: Denso 10PA style body with a clutch pulley | Own work. The scanology scan (CC BY) is only one housing component and is not usable |
| Battery | build | Procedural box with terminals, hold down and an unbranded label | Own work. The CC BY battery models carry brand labels |
| Air filter box | build | Procedural build of the LC100 airbox and intake duct, left front of the bay | Own work. The only CC BY airbox is a 1M face Mercedes scan |
| Spare wheel carrier | build | Procedural underfloor winch carrier with cradle (the LC100 carries its spare under the rear), reusing our own wheel6 wheel | Own work (the URL is a placeholder reference only; no carrier model exists) |

## Recommendation

Build almost all of the mechanicals procedurally in Blender to real FZJ100 dimensions. Use CC BY or CC0 models only where the part shape is generic and the licence is clean: propeller shafts (PolyPhantom), the rotor (pao1011), the radiator core (ACBRadio), the alternator (B0bik), the starter (menarzuw) and optionally the catalytic converter (Science Museum, CC0). Total cost is $0.

Why not buy:
- No complete LC100 or LX470 model with a real underbody and engine is licensable. The candidates are either body only (Squir, HighRock), game mods or rips, or come with the wrong engine (the Alqhtani 2JZ).
- Every paid mechanical model is generic or the wrong part: 2JZ or BMW style engines, a GM transfer case, pickup or Prado chassis with coilovers, performance calipers. On a parts shop site, those would show customers parts that are not on their car.
- Almost every marketplace licence (CGTrader RF 21A.3, Fab Standard 4(c), TurboSquid Standard, 3DExport Basic, Unity EULA) requires stopping end users from extracting the model, and a plain GLB served to a browser fails that.
- RenderHub's Extended Use licence is the one exception that suits the web, but its only relevant items are generic (a 3D Horse gearbox at $69, a BMW style I6 at $199).

The exact parts exist only as GrabCAD scans:
- 4AM_Engineering's 1FZ-FE, intake manifold, H151F and HF2AV scans, plus Daniel Klyuev's 37110-6A060 rear prop shaft STEP.
- GrabCAD's terms limit these to non commercial internal use. The single highest value move is to ask those authors for written commercial permission. With it, the 1FZ-FE, H151F and HF2A could be decimated scans instead of builds.

Build order, by visibility:
1. Engine with its manifolds and cam cover.
2. Frame.
3. Front IFS with the torsion bars.
4. Rear axle with the links.
5. Gearbox and transfer case.
6. Exhaust and fuel tank.
7. Brakes and ancillaries.

Build every assembly as separate named parts so explode works.

These are geometry, explode and shader heavy Blender steps, so per the project rules they are better on Fable.

Attribution goes in the credits for each CC BY model used.

Separate risk: the car's own body (reference/model/lc100_2006_cc_by) appears to be DR1KING100K's Sketchfab upload, and its texture names suggest a game mod origin. Verify its CC BY claim before going public, because it affects the whole site, not just these parts.

## Questions for Saaqib

* Are you OK with building most mechanical parts ourselves (accurate shape and dimensions, but procedural rather than scanned) instead of paying for generic models that look like the wrong car?
* Should I draft a polite message to 4AM_Engineering on GrabCAD (the 1FZ-FE, intake, H151F and HF2AV scans) and Daniel Klyuev (the 37110-6A060 LC100 rear prop shaft) asking for written permission to use their models commercially on the site? If they agree, the engine, gearbox and transfer case become real scans.
* Is a paid licence acceptable at all? If so, the only web compatible one found is RenderHub's Extended Use licence. CGTrader, Fab, TurboSquid and 3DExport would need the GLB encrypted or the seller's written OK. Would you accept obfuscating the GLB, or asking sellers by message?
* How detailed should the underbody be? Visible from the lift and Under camera only (moderate detail, lighter GLB), or full explode quality for every bolt on part?
* Do you have photos of a real LC100 underside and engine bay (or access to one in the shop) that I can measure from? They would make the procedural builds much more accurate than catalogue diagrams alone.
* The source body model (lc100_2006_cc_by, likely DR1KING100K on Sketchfab) has texture names that suggest it came from a game mod. Can you confirm where you got it and who made it, so we know its CC BY claim holds before the site goes public?
* Is it fine to show credits for CC BY parts (radiator, alternator, starter, prop shaft, rotor) in a credits panel in the app?
