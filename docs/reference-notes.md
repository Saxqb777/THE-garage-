# Reference notes

What the reference material says, measured, and where the real car differs from the brief.

## Files

| File | What | Notes |
| --- | --- | --- |
| reference/photos/front_three_quarter_right.webp | Front right 3/4, 2000 px | Best view of grille, headlamp, bumper, wheel |
| reference/photos/side_left.webp | Left side, 2000 px | Rectified to an orthographic side view (below) |
| reference/photos/rear_browser_screenshot.webp | Rear, browser screenshot | Barn doors, tail lamps, rear bumper |
| reference/photos/listing_collage_9.webp | All 9 listing photos, small tiles | Interior and engine bay tiles are too small to model from |
| reference/blueprint/lc100_blueprint_sheet.jpg | 3 tops, 3 sides, 3 fronts, 1024 px | Drawn from a VX: flares, roof rails, side steps. No rear view |
| reference/manual/manual_page_dash_overview_view_b.pdf | One manual page, 2 pages total | Dash overview, navigation version (US market, VX level) |
| reference/manual/LC100_2005_owners_manual.md | Full owner's manual as text, 351 pages | US market 2UZ-FE; grep it for names, positions, fuses, specs |

Still wanted: full size originals of all 9 photos, the VIN or chassis code, a larger blueprint with a rear view. The owner's manual text is now in reference/manual/LC100_2005_owners_manual.md.

## Where the real car differs from the brief

| Brief says | Photos show | What we model |
| --- | --- | --- |
| Tailgate hinged at the top | Twin side hinged rear barn doors, split down the middle, each with its own wiper | Barn doors, hinged at the outer edges |
| Grey wheel arch flares | No flares, plain body colour arches with a small lip | No flares |
| Grey side steps | None visible | None |
| Roof rails | None | None |
| "4500 EFI" fender badge | Badge sits on the rear quarter panel, behind the rear door, under a louvred vent | Badge on the rear quarter |
| GXR trim | Rear door carries a "G" badge | Confirmed GXR, the G badge is normal on GCC GXR |
| Battery right side | Engine bay photo looks like the car's left side | Confirmed: vehicle left, per the photo |

Chassis: assume FZJ100 (independent front suspension) until Saaqib confirms the chassis code. FZJ105 would be a solid front axle. Barn doors, no flares and a manual box exist on both; the chassis code on the registration card settles it and changes the suspension part list.

## Key dimensions (metres)

`u` is the distance behind the front axle. Blender Y = u minus 1.425.

| Item | Value | Source |
| --- | --- | --- |
| Wheelbase | 2.85 | Brief, blueprint agrees (136 px at 20.96 mm per px) |
| Front overhang | 0.905 | Blueprint ratio, scaled to the 4.89 length |
| Rear overhang | 1.135 | Blueprint ratio, scaled to the 4.89 length |
| Roof height | 1.835 | Blueprint variants without rails measure 1.83 to 1.84 |
| Body width at doors | 1.88 | Blueprint 1.94 with flares, minus the flares |
| Tire | 275/70R16, 0.791 diameter, wheel centre 0.385 | Spec |
| Track | 1.62 front, 1.60 rear | Spec |

Side profile (rectified photo plus blueprint):

| Feature | u | z |
| --- | --- | --- |
| Hood front edge | about 0.85 ahead of the front axle | 1.13 to 1.15 |
| Cowl, windshield base | 0.48 to 0.52 | 1.26 to 1.28 |
| Windshield top at the centre line | about 1.32 | 1.80 |
| A pillar top at the side | about 1.12 | 1.76 |
| Front door front edge | 0.63 | sill to belt |
| B pillar, front door rear edge | 1.60 to 1.69 | |
| Rear door rear edge above the arch | 2.65 to 2.71 | |
| C pillar (slanted forward at the top) | 2.37 at top, 2.57 at belt | |
| Quarter window | 2.6 to 3.4 | 1.29 to 1.79 |
| Rear end of body | about 3.95, bumper 3.985 | |
| Beltline | 1.22 at the front door, rising to 1.30 at the rear | |
| Door bottoms and sill | | 0.47 to 0.49 |
| Front bumper | | 0.43 to 0.86 |
| Rear bumper | 3.27 to 3.98 | 0.49 to 0.79 |
| Front wheel arch | centre 0, radius about 0.50 | |
| Rear wheel arch | centre 2.85, radius about 0.50 | |
| Front door handle | 1.38 to 1.64 | 1.07 to 1.13 |
| Rear door handle | 2.34 to 2.61 | 1.11 to 1.17 |
| Side turn signal (amber) | 0.51 to 0.58 | 1.05 to 1.09 |
| Fuel filler lid (left side only) | 3.25 to 3.41 | 1.00 to 1.16 |
| 4500 EFI badge | 3.31 to 3.61 | 1.25 to 1.30 |
| Quarter vent louvre | 3.43 to 3.61 | 1.33 to 1.41 |
| Tail lamp side view | 3.71 to 3.81 | 0.87 to 1.21 |
| Front mudguard | 0.45 to 0.53 | 0.17 to 0.51 |
| Rear mudguard | 3.23 to 3.35 | 0.27 to 0.73 |

Front view (blueprint): greenhouse narrows from 1.63 wide at z 1.42 to 1.47 at z 1.68 (about 17 degrees of tumblehome), mirrors span about 2.2 at z 1.24 to 1.36.

Rear view (photo, lateral positions from the centre line, positive is the vehicle's left):

* Barn door split exactly on the centre line, doors equal width, hinges on the outer edges.
* Rear glass opening: about 0.80 half width at the bottom, 0.70 at the top.
* Tail lamps: outer 0.16 of each side, wrapping round the corners, red with a clear reverse band in the middle.
* LAND CRUISER plate on the left door, 0.16 to 0.66 to the left; plate recess below it.
* Toyota emblem on the right door near the split, about minus 0.05 to minus 0.20; "G" badge low on the right door near its outer edge.
* Rear bumper full width with a step top, red reflectors at the ends, tow hitch in the middle.

## How the side photo was rectified

scripts/reference/rectify_side.py maps the photo onto the car's side plane with a homography from the two rims (rim flange 0.44 m, hub 0.38 m up, axles 2.85 m apart). Rectified image: 4 mm per pixel, u from minus 1.25 to 4.25, z from minus 0.05 to 2.05.

## Parts data sources (for M7)

* toyotapartsdeal.com, 2005 Land Cruiser parts catalogue (shared by Saaqib): https://www.toyotapartsdeal.com/2005-toyota-land_cruiser-parts.html. Reachable since Saaqib allowed the domain. Plain requests get a 403 from the site's own server; a normal browser user agent gets the page.
* Structure: about 150 diagram groups under Body, Electrical, Engine/Fuel/Tool and Power Train/Chassis, each at /parts-list/2005-toyota-land_cruiser/<category>/<group>.html. Every group page embeds its data as JSON (window.__INITIAL_STORE__, a JavaScript literal with undefined values) with, per part: part number, PNC (Toyota part name code, e.g. 81110 headlamp), description, required quantity, notes, USD price and retail, photo URLs.
* Example, Headlamp group: Unit Assy Headlamp LH 81170-60B10 ($267.95) and 81059-60071 ($227.35), RH 81130-60B20 and 81019-60071, Headlamp Assy W/Clearance 81010-60071 (RH) and 81050-60071 (LH), plus bulbs and sockets.
* Caveats: it is the US market catalogue for the year, with no trim or market filter, so several numbers per part appear without saying which fits a GCC GXR. Engine groups will be the 2UZ-FE V8, not the 1FZ-FE. Prices are US dealer prices. GCC fitment and UAE prices still need Saaqib or a GCC source (VIN lookup).
* Partsouq (shared by Saaqib as a Google share link): https://partsouq.com/en/catalog/genuine/pick?c=Toyota&model=LAND+CRUISER with a session code in the URL. The site sits behind a Cloudflare browser challenge, so scripts cannot read it; it is a manual reference. Use it by VIN in a normal browser and copy OEM numbers into the seed sheet.
* Pricing decision (Saaqib, M7): no prices on the site. The part card has a Get price button that opens WhatsApp with the exact part prefilled; the shop replies with the price. The WhatsApp number comes later (environment variable).
