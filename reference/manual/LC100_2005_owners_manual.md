# Toyota Land Cruiser 100 (2005) Owner's Manual, text extraction for The Garage

Source: Toyota OM60B33U, 2005 Land Cruiser Owner's Manual, English, 351 pages, copyright 2004 Toyota Motor Corporation.
Purpose: reference material for Claude Code on The Garage project. Use it for official Toyota part names, control positions, warning light names, fluid specs, fuse names, dimensions and service points.

## READ THIS FIRST: spec mismatch

This manual is the US market Land Cruiser 100, not the GCC GXR that The Garage models. Same body, same dimensions, same chassis, but:

| Item | This manual (US) | The Garage car (GCC GXR 2005) |
|---|---|---|
| Engine | 2UZ-FE 4.7 V8 | 1FZ-FE 4.5 inline 6 |
| Gearbox | 5 speed automatic | 5 speed manual plus transfer lever |
| Trim | Fully loaded (leather, moonroof, nav, AHC, VGRS, heated seats, power seats) | Base: cloth, manual AC dials, single DIN radio, no moonroof, no nav, no AHC, no VGRS |
| Steering | LHD | LHD (same) |
| Fuel | Octane 87/91 | GCC 91/95 |
| Cluster | Voltmeter, oil pressure gauge | Confirm against GXR photo, GXR cluster is simpler |

Rule for Claude Code: use this manual for NAMES and POSITIONS of things, then strip anything the GXR does not have. When in doubt, check the GXR reference photos or ask Saaqib. Never add a feature to the 3D car just because it is in this manual.

## Page numbering

Headings below use the printed page number (the number at the bottom of each manual page). PDF page = printed page + 10. Front matter pages i to x are PDF pages 1 to 10.

## Key pages for The Garage

| Need | Printed page | What it gives |
|---|---|---|
| Instrument panel hotspots (Get In view) | 2 to 5 | Numbered list of every dash control, 4 views |
| Cluster gauges | 6 | Numbered cluster layout |
| Warning and indicator light names | 7 | Official names for every cluster symbol |
| Keys, doors, locks, windows, tailgate, hood | 9 to 32 | Door and tailgate behaviour, hood release |
| Steering wheel, mirrors | 97 to 106 | Mirror and tilt controls |
| Lights, turn signals, wipers, defogger | 107 to 116 | Stalk positions and functions |
| Gauges and warning lights behaviour | 117 to 132 | What each gauge and light does |
| Ignition, transmission, 4WD lever, parking brake | 133 to 150 | Ignition positions, transfer case |
| AC controls | 175 to 186 | Control names (GXR uses manual dials) |
| Engine compartment overview | 290 | Numbered engine bay components |
| Fuse locations and fuse list | 291, 329 to 330 | Every fuse name, amp and circuit |
| Engine oil, coolant, brake fluid checks | 296 to 310 | Service points |
| Bulb replacement | 311 to 322 | Every exterior and interior bulb |
| Dimensions and weights | 324 | 4890 x 1940 x 1875 mm, wheelbase 2850, tread 1620/1615 |
| Service specifications and fluids | 325 to 328 | Capacities, oil grades, tire pressure |

## How Claude Code should use this file

- Grep it, do not read it top to bottom. Search for a control name, a fuse, a fluid or a page number.
- Hotspot labels in src/data must use the exact Toyota wording from pages 2 to 7 and 290.
- Search aliases can be pulled from the Index section at the end (printed pages 333 onward).
- Diagrams are not in this file. Figure codes were stripped. Open the PDF in reference/ for the pictures when placing hotspots.

---

# Front matter

## Front matter page i

Foreword
Welcome to the growing group of value-conscious people who drive Toyotas. We are proud of the advanced engineering and
quality construction of each vehicle we build.
This Owner's Manual explains the operation of your new Toyota. Please read it thoroughly and have all the occupants
follow the instructions carefully. Doing so will help you enjoy many years of safe and trouble-free motoring. For
important information about this manual and your Toyota, read the following pages carefully.
When it comes to service, remember that your Toyota dealer knows your vehicle very well and is interested in your complete
satisfaction. Your Toyota dealer will provide quality maintenance and any other assistance you may require.
If there is not a Toyota dealer near you, or you need emergency assistance for any reason, please call the following number:

 U.S. OWNERS:

Toyota Customer Assistance Center

Toll-free:1-800-331-4331

Please leave this Owner's Manual in this vehicle at the time of resale. The next owner will need this information also.
All information and specifications in this manual are current at the time of printing. However, because of Toyota's policy of
continual product improvement, we reserve the right to make changes at any time without notice.
Please note that this manual applies to all models and explains all equipment, including options. Therefore, you may
find some explanations for equipment not installed on your vehicle.

© 2004 TOYOTA MOTOR CORPORATION
All rights reserved. This material may not be reproduced or copied, in whole or in part, without the written permission of Toyota
Motor Corporation.

## Front matter page ii

Important information about this manual
Safety and vehicle damage warnings

Safety symbol

Throughout this manual, you will see safety and vehicle damage warnings. You must follow these warnings carefully to
avoid possible injury or damage.
The types of warnings, what they look like, and how they are
used in this manual are explained as follows:

CAUTION
This is a warning against anything which may
cause injury to people if the warning is ignored.
You are informed about what you must or must not
do in order to reduce the risk of injury to yourself
and others.

When you see the safety symbol
shown above, it means: "Do not"; "Do
not do this"; or "Do not let this happen".

NOTICE
This is a warning against anything which may
cause damage to the vehicle or its equipment if the
warning is ignored. You are informed about what
you must or must not do in order to avoid or reduce the risk of damage to your vehicle and its
equipment.

## Front matter page iii

Important information about your Toyota

The purpose of all occupant restraint systems is to help
reduce the possibility of death or serious injury in the
event of a collision. None of these systems, either individually or together, can ensure that there is no injury
in the event of collision. However, the more you know
about these systems and how to use them properly, the
greater your chances become of surviving an accident
without death or serious injury.

Occupant restraint systems
Toyota encourages you and your family to take the time
to read Section 1-3 of this Owner's Manual carefully. In
terms of helping you understand how you can receive
the maximum benefit of the occupant restraint systems
this vehicle provides, Section 1-3 of this Owner's Manual is the most important section for you and your family
to read.

Seat belts provide the primary restraint to all occupants
of the vehicle, and every occupant of the vehicle should
wear seat belts properly at all times. Children should
always be secured in child restraint systems that are
appropriate for their age and size. SRS (Supplemental
Restraint System) airbags are, as their names imply,
designed to work with, and be supplemental to, seat
belts and are not substitutes for them. SRS airbags can
be very effective in reducing the risk of head and chest
injuries by preventing contact of the head and chest
with interior portions of the vehicle.

Section 1-3 describes the function and operation concerning seats, seat belts, SRS airbags and child restraint systems of this vehicle and some potential hazards you should be aware of. These systems work together along with the overall structure of this vehicle in
order to provide occupant restraint in the event of a
crash. The effect of each system is enhanced when it is
us ed p r oper l y a nd t oget her w i t h o t her s y s t ems . N o
single occupant restraint system can, by itself, provide
y ou o r y our f ami l y w i t h t he e qual l ev el o f r es t r ai nt
which these systems can provide when used together.
That is why it is important for you and your family to
understand the purpose and proper use of each of these
systems and how they relate to each other.

## Front matter page iv

In order to be effective, the SRS airbags must deploy
with tremendous speed. The rapid deployment of the
SRS airbags makes the SRS airbags themselves potential sources of serious injury if an occupant is too close
to an airbag, or if an object or some part of his or her
body has been placed between the occupant and the
airbag at the time of deployment. This is just one example of how the instructions in Section 1-3 of this Owner's Manual will help ensure proper use of the occupant
restraint systems, and increase the safety they can provide to you and your family in the event of an accident.

Event data recorder
Your vehicle has computers that monitor and control
certain aspects of your vehicle. These computers assist
in driving and maintaining optimal vehicle performance.
Besides storing data useful for troubleshooting, there is
a system to record data in a crash or a near car crash
event. This is called an Event Data Recorder (EDR).
The SRS airbag sensor assembly contains the EDR. In
a crash or a near car crash event, this device records
some or all of the following information:

Toyota recommends you to read the provisions in Section 1-3 carefully and refer to them as needed during
your time of ownership of this vehicle.

 Engine speed
 Whether the brake pedal was applied or not
 Vehicle speed
 To what extent the accelerator pedal was depressed
 Position of the transmission selector lever
 Whether the driver and front passenger wore the
seat belts or not
 Driver's seat position
 Front passenger's occupant classification

## Front matter page v

 SRS airbag deployment data

New vehicle warranty

 SRS airbag system diagnostic data

Your new vehicle is covered by the following Toyota
limited warranties:

The information above is intended to be used for the
purpose of improving vehicle safety performance. Unlike
general data recorders, the EDR does not record sound
data such as conversation between passengers.

 New vehicle warranty
 Emission control systems warranty

Toyota will not disclose the data recorded in an EDR to
a third party except when:

 Others
For further information, please refer to the "Owner 's
Warranty Information Booklet" or "Owner's Manual Supplement".

 An agreement from the vehicle's owner (or the leasing company for a leased vehicle) is obtained
 Officially requested by the police or other authorities
 Used as a defence for Toyota in a law suit
 Ordered by the court

Your responsibility for maintenance

However, if necessary Toyota will:

It is the owner's responsibility to make sure the specified maintenance is performed. Section 6 gives details
of these maintenance requirements. Also included in
Section 6 is general maintenance. For scheduled maintenance information, place refer to the "Scheduled Maintenance Guide" or "Owner's Manual Supplement".

 Use the data for research on Toyota vehicle safety
performance
 Disclose the data to a third party for research purposes without disclosing details of the vehicle owner, and only when it is deemed necessary
 Disclose summarized data cleared of vehicle identification information to a non-Toyota organization for
research purposes

## Front matter page vi

Accessories, spare parts and
modification of your Toyota

Important health and safety
information about your Toyota

A wide variety of non-genuine spare parts and accessories for Toyota vehicles are currently available in the
market. You should know that Toyota does not warrant
these products and is not responsible for their performance, repair, or replacement, or for any damage they
may c aus e t o, o r a dv er s e e ff ec t t hey m ay h av e o n,
your Toyota vehicle.

CAUTION
D WARNING: Engine exhaust, some of its constituents, and a wide variety of automobile components contain or emit chemicals known to the
State of California to cause cancer and birth defects and other reproductive harm. In addition,
oils, fuels and fluids contained in vehicles as well
as waste produced by component wear contain or
emit chemicals known to the State of California
to cause cancer and birth defects or other reproductive harm.

This vehicle should not be modified with non-genuine
Toyota products. Modification with non-genuine Toyota
products could affect its performance, safety or durability, and may even violate governmental regulations. In
addition, damage or performance problems resulting from
the modification may not be covered under warranty.

D Battery posts, terminals and related accessories
contain lead and lead compounds. Wash your
hands after handling. Used engine oil contains
chemicals that have caused cancer in laboratory
animals. Always protect your skin by washing
thoroughly with soap and water.

## Front matter page vii

Installation of a mobile
two-way radio system

Tires and loading on your Toyota
Underinflated or overinflated tire inflation pressure
and the excess load may result in the deterioration
of steering ability and braking ability, leading to
an accident. Check the tire inflation pressure periodically and be sure to keep the load limits given
in this Owner's Manual. For details about tire inflation pressure and load limits, see pages 301 and
230.

As the installation of a mobile two-way radio system in
your vehicle could affect electronic systems such as
multiport fuel injection system/sequential multiport fuel
injection system, electronic throttle control system,
cruise control system, anti-lock brake system, active
traction control system, vehicle stability control system,
SRS airbag system and seat belt pretensioner system,
be sure to check with your Toyota dealer for precautionary measures or special instructions regarding installation.

## Front matter page viii

Scrapping of your Toyota

On-pavement and off-road
driving tips

The SRS airbag and seat belt pretensioner devices in
your Toyota contain explosive chemicals. If the vehicle
is scrapped with the airbags and pretensioners left as
they are, this may cause an accident such as fire. Be
sure to have the systems of the SRS airbag and seat
belt pretensioner removed and disposed of by a qualified
service shop or by your Toyota dealer before you dispose of your vehicle.

This vehicle belongs to the utility vehicle class. Utility
vehicles have a significantly higher rollover rate than
other types of vehicles. This vehicle will handle and
maneuver differently from an ordinary passenger car because it is designed for off-road use also. In addition,
this vehicle has a higher ground clearance and center of
gravity than that of an ordinary passenger car. This
vehicle design feature causes this type of vehicle to be
more likely to rollover. Failure to operate this vehicle
correctly may result in loss of control, accidents or
vehicle rollover causing death or serious injury. Be sure
to read "Off-road vehicle precautions" on page 208 and
"Off-road driving precautions" on page 238.

## Front matter page ix

Table of contents
1 OPERATION OF INSTRUMENTS AND CONTROLS

Page

1
2
3
4
5
6
7
8
9
10

Overview of instruments and controls . . . . . . . . . . . . . . . . . . . . . . . . . . 1
Keys and Doors . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9
Occupant restraint systems . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 33
Steering wheel and Mirrors . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 97
Lights, Wipers and Defogger . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 107
Gauges, Meters and Service reminder indicators . . . . . . . . . . . . . . 117
Ignition switch, Transmission and Parking brake . . . . . . . . . . . . . . 133
Audio system . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 151
Air conditioning system . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 175
Other equipment . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 187
INFORMATION BEFORE DRIVING YOUR TOYOTA . . . . . . . . . . 207
STARTING AND DRIVING . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 235
IN CASE OF AN EMERGENCY . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 251
CORROSION PREVENTION AND APPEARANCE CARE . . . . . 275
VEHICLE MAINTENANCE AND CARE . . . . . . . . . . . . . . . . . . . . . . . 283

2
3
4
5
6
7 DO-IT-YOURSELF MAINTENANCE
1
2
3

Introduction . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 289
Engine and Chassis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 295
Electrical components . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 311
8 SPECIFICATIONS . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 323

9 REPORTING SAFETY DEFECTS FOR U.S. OWNERS AND
UNIFORM TIRE QUALITY GRADING . . . . . . . . . . . . . . . . . . . . . . . . 331
10 INDEX . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 333

## Front matter page x

# Section 1-1: Overview of instruments and controls

## p.1 SECTION

SECTION

1- 1

OPERATION OF INSTRUMENTS AND
CONTROLS
Overview of instruments and controls
Instrument panel overview . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 2
Instrument cluster overview . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 6
Indicator symbols on the instrument panel . . . . . . . . . . . . . . . . . . . . . . . 7

## p.2 Instrument panel overview

Instrument panel overview
View A
1. Side vents
2. Side defroster outlets
3. Instrument cluster
4. Center vents
5. Electric moon
personal lights

roof

switches

and/or

6. Glove box
7. Power door lock switches
8. Power window switches
9. Automatic transmission selector lever
10. Seat heater switches
11. Rear seat audio system
12. Cup holder
13. Parking brake lever
14. Second start mode selector button and
driving pattern selector button
15. Four-wheel drive control lever
16. Lower vent
17. Hood lock release lever
18. Fuel filler door opener
19. Window lock switch

## p.3 View B

View B
(Vehicles with navigation system)
1. Headlight, turn signal and front fog
light switches
2. Cruise control switch
3. Ignition switch
4. Wiper and washer switches
5. Emergency flasher switch
6. Navigation system including air conditioning controls (See the separate
"Navigation System Owner's Manual".)
7. Clock, outside temperature and trip information display
8. Front passenger's seat belt reminder
light
9. Audio system
10. Outside rear view mirror heater switch
11. Rear air conditioning switch
12. Rear window defogger switch
13. Center differential lock switch
14. Power antenna switch
15. Power tilt and telescopic steering
switch
16. Instrument panel light control dial
17. Power rear view mirror control switches
18. Power quarter window switch
(left-hand side)
19. Power quarter window switch
(right-hand side)
20. Roll sensing of curtain shield airbags
off switch

## p.4 View B

View B
(Vehicles without navigation system)
1. Headlight, turn signal and front fog
light switches
2. Cruise control switch
3. Ignition switch
4. Wiper and washer switches
5. Emergency flasher switch
6. Clock, outside temperature and trip information display
7. Audio system
8. Front passenger's seat belt reminder
light
9. Air conditioning controls
10. Outside rear view mirror heater switch
11. Rear air conditioning switch
12. Rear window defogger switch
13. Center differential lock switch
14. Power antenna switch
15. Power tilt and telescopic steering
switch
16. Instrument panel light control dial
17. Power rear view mirror control switches
18. Power quarter window switch
(left-hand side)
19. Power quarter window switch
(right-hand side)
20. Roll sensing of curtain shield airbags
off switch

## p.5 Lower part of center cluster panel

Lower part of center cluster panel

1. Ashtray
2. Cigarette lighter
3. Power outlet

## p.6 Instrument cluster overview

Instrument cluster overview

1. Voltmeter

4. Tachometer

7. Odometer and two trip meters

2. Speedometer

5. Engine oil pressure gauge

8. Trip meter reset knob

3. Service reminder indicators and
indicator lights

6. Engine coolant temperature gauge

9. Fuel gauge

## p.7 Indicator symbols on the instrument panel

Indicator symbols on the instrument panel
Brake system warning light∗1

Unengaged "Park" warning light∗1

Driver's seat belt reminder light∗1

Automatic transmission fluid temperature warning
light∗1

Discharge warning light∗1

Turn signal indicator lights

Engine oil replacement reminder light

Headlight high beam indicator light

Malfunction indicator lamp∗1

Driving pattern ("POWER" mode) indicator
light

Low fuel level warning light∗1

Automatic transmission second start indicator
light

SRS warning light∗1

Center differential lock indicator light

Anti-lock brake system warning light∗1

Cruise control indicator light∗2

Open door warning light∗1

Automatic transmission indicator lights

## p.8 Vehicle stability control system off indicator

Vehicle stability control system off indicator
light∗1
Vehicle stability control system and active traction
control system warning light∗1
Active traction control system indicator light
Slip indicator light
Roll sensing of curtain shield airbags off indicator light∗3

∗1 :

For details, see "Service reminder indicators and warning
buzzers" on page 122.

∗2 :

If this light flashes, see "Cruise control" on page 142.

∗3 :

For details, see "Roll sensing of curtain shield airbags off
switch" on page 66.

# Section 1-2: Keys and Doors

## p.9 SECTION

SECTION

1- 2

OPERATION OF INSTRUMENTS AND
CONTROLS
Keys and Doors
Keys . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 10
Engine immobilizer system . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12
Wireless remote control . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13
Side doors . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 18
Power windows . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 22
Power quarter windows . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 24
Back door . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 25
Hood . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 27
Theft deterrent system . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 28
Fuel tank cap . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 29
Electric moon roof . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 31

## p.10 Keys

Keys
A transponder chip for engine immobilizer
system has been placed in the head of
the master and sub keys. These chips are
needed to enable the system to function
correctly, so be careful not to lose these
keys. If you make your own duplicate key,
you will not be able to cancel the system
or start the engine.
To protect items locked in the glove box
when using valet parking, leave the sub
key with the attendant.

Your vehicle is supplied with two kinds
of keys.
1. Master keys (black)-These keys work
in every lock. Your Toyota dealer will
need one of them to make a new key
with a built-in transponder chip.
2. Sub key (gray)-This key does not
work in the glove box.

Since the side doors can be locked without a key, you should always carry a
spare master key in case you accidentally
lock your keys inside the vehicle.

NOTICE

For information on use of the wireless
remote control key, see "Wireless remote
control" on page 13.

When using a key containing a transponder chip, observe the following
precautions:
z When starting the engine, do not
use the key with a key ring resting
on the key grip and do not press
the key ring against the key grip.
Otherwise the engine may not start,
or may stop soon after it starts.

## p.11 z Do not use the key with electromagnetic materials.

z Do not use the key with electromagnetic materials.

z When starting the engine, do not
use the key with other transponder
keys around (including keys of other vehicles) and do not press other
key plates against the key grip.
Otherwise the engine may not start,
or may stop soon after it starts. If
this happens, remove the key once
and then insert it again after removing other transponder keys (including keys of other vehicles) from the
ring or while gripping or covering
them with your hand to start the
engine.

z Do not bend the key grip.
z Do not cover the key grip with any
material that cuts off electromagnetic waves.
z Do not knock the key hard against
other objects.
z Do not leave the key exposed to
high temperatures for a long period,
such as on the dashboard and hood
under direct sunlight.
z Do not put the key in water or
wash it in an ultrasonic washer.

## p.12 Engine immobilizer system

Engine immobilizer system

KEY NUMBER PLATE
Your key number is shown on the plate.
Keep the plate in a safe place such as
your wallet, not in the vehicle.
If you should lose your keys or if you
need additional keys, duplicates can be
made by a Toyota dealer using the key
number.
We recommend writing down the key number and storing it in a safe place.

The engine immobilizer system is a
theft prevention system. When you insert the key in the ignition switch, the
transponder chip in the key's head
transmits an electronic code to the vehicle. The engine will start only when
the electronic code in the chip corresponds to the registered ID code for
the vehicle.

The system is automatically set when the
key is removed from the ignition switch.
The indicator light will start flashing to
show the system is set.
If any of the following indicator conditions
occurs, contact your Toyota dealer.

 The indicator light stays on except

when the theft deterrent system is setting or activating. (See "Theft deterrent
system" on page 28.)

 The indicator light does not start flash-

ing when the key is removed from the
ignition switch.

 The indicator light flashes inconsistently.

## p.13 Wireless remote control*-

Wireless remote control*-
Inserting the registered key in the ignition
switch automatically cancels the system,
which enables the engine to start. The
indicator light will go off.
For your Toyota dealer to make a new key
with a built-in transponder chip, your
dealer will need your key number and
master key. However, there is a limit to
the number of additional keys your Toyota
dealer can make for you.
If you make your own duplicate key,
you will not be able to cancel the system or start the engine.

FCC ID: MOZRI-20BTY
MADE IN JAPAN
This device complies with Part 15 of the
FCC Rules. Operation is subject to the
following two conditions:
(1) This device may not cause harmful
interference, and (2) this device must
accept any interference received, including interference that may cause undesired operation.

CAUTION
Changes or modifications not expressly approved by the party responsible for compliance could void the
user's authority to operate the equipment.
1. "LOCK" switch
2. Indicator light
3. "PANIC" switch
4. "UNLOCK" switch
The wireless remote control system is
designed to lock or unlock all the side
doors and back door from a distance
within approximately 1 m (3 ft.) of the
vehicle.
NOTE: *This feature can be deactivated
as vehicle theft deterrent measure in case
of the loss of the wireless remote control
key. Ask your Toyota dealer for details.
When you operate any switch, push it
slowly and securely. At this time, the indicator light flashes once.

## p.14 -Locking and unlocking

-Locking and unlocking
doors
The wireless remote control key is an
electronic component. Observe the following instructions in order not to cause damage and trouble to the key.

 Do not leave the key in places where
the temperature becomes high such as
on the dashboard.

If you lose your wireless remote control
key, contact your Toyota dealer as soon
as possible to avoid the possibility of
theft, or an accident. (For detailed information, see "If you lose your keys" on
page 273.)

 Do not disassemble it.
 Avoid knocking it hard against other
objects or dropping it.

 Avoid putting it in water.
You can use up to 4 wireless remote control keys for the same vehicle. Contact
your Toyota dealer for detailed information.

Locking operation

If the wireless remote control key does
not actuate the doors or operate from a
normal distance, or the indicator light on
the key is dimmed or does not come on:

 Check for closeness to a radio trans-

mitter such as a radio station or an
airport which can interfere with normal
operation of the key.

 The battery may have been consumed.

Check the battery in the key. To
replace the battery, see following
"-Replacing battery" on page 17.
Unlocking operation

## p.15 -Activating panic mode

-Activating panic mode
To lock and unlock all the side doors
and back door, push the switches slowly and securely.
To lock: Push the "LOCK" switch. All the
side doors and back door are locked simultaneously. At this time, turn signal
lights flash once.*
NOTE: *The turn signal lights can be set
not to flash. Ask your Toyota dealer for
details.
Check to see that all the side doors and
back door are securely locked.
If any of the side doors or back door is
not securely closed, or if the key is in the
ignition switch, locking cannot be performed by the "LOCK" switch.
To unlock: Push the "UNLOCK" switch
once to unlock the driver's door alone.
Pushing the switch twice within 3 seconds
unlocks all the side doors and back door
simultaneously.* At this time, turn signal
lights flash twice.**
NOTE: *The 2-step unlocking function can
be changed. **The turn signal lights can
be set not to flash. Ask your Toyota dealer for details.

Together with the activation of unlocking,
the interior light comes on for 15 seconds
if the interior light switch is in "DOOR"
position.* However, this function does not
work when the ignition key is in the "ACC"
or "ON" position. (For detailed information,
see "Interior light" on page 111.)
You have 30 seconds to open a door after
using the wireless remote unlock feature.** If a door is not opened by then, all
the side doors and back door will be automatically locked again.
NOTE: *The interior light can be set not
to come on or the duration of lighting can
be changed. **The time before automatic
re-locking can be changed. Ask your
Toyota dealer for details.
If the "LOCK" or "UNLOCK" switch is kept
pressed in, the locking or unlocking operation is not repeated. Release the switch
and then push again.

Pushing the "PANIC" switch for 1 second blows the horn intermittently and
flashes the headlights, tail lights and
interior lights.*
NOTE: *This feature can be deactivated.
Ask your Toyota dealer for details.
The "PANIC" switch is used to deter vehicle theft when you witness anyone attempting to break into or damage your
vehicle.

## p.16 The alarm will last for 1 minute. To stop

The alarm will last for 1 minute. To stop
the alarm midway, push the "PANIC",
"LOCK" or "UNLOCK" switch, or unlock
any side door or back door with key. You
can also stop the alarm by turning the
ignition key from "LOCK" to the "ON" position.
The "PANIC" mode does not work when
the ignition key is in the "ON" position.
For vehicles sold in U.S.A.
This device complies with Part 15 of the
FCC Rules. Operation is subject to the
following two conditions: (1) This device
may not cause harmful interference, and
(2) this device must accept any interference received, including interference
that may cause undesired operation.

NOTICE:
This equipment has been tested and
found to comply with the limits for a
Class B digital device, pursuant to Part
15 of the FCC Rules. These limits are
designed to provide reasonable protection against harmful interference in a
residential installation. This equipment
generates, uses and can radiate radio
frequency energy and, if not installed
and used in accordance with the instructions, may cause harmful interference to
radio communications. However, there is
no guarantee that interference will not
occur in a particular installation. If this
equipment does cause harmful interference to radio or television reception,
which can be determined by turning the
equipment off and on, the user is encouraged to try to correct the interference by one or more of the following
measures:

 Reorient or relocate the receiving antenna.

 Increase the separation between the
equipment and receiver.

 Connect the equipment into an outlet

on a circuit different from that to
which the receiver is connected.

 Consult the dealer or an experienced
radio/TV technician for help.

FCC WARNING:
Changes or modifications not expressly approved by the party responsible for compliance could void the
user's authority to operate the equipment.

CAUTION
Changes or modifications not expressly approved by the party responsible for compliance could void the
user's authority to operate the equipment.

## p.17 -Replacing battery

-Replacing battery
For replacement, use a CR1616 lithium
battery or equivalent and a special screwdriver.

CAUTION
Special care should be taken to prevent small children from swallowing
the removed battery or components.

NOTICE
z When replacing the battery, be careful not to lose the components.
z Replace only with the same or
equivalent type recommended by a
Toyota dealer.

1. Remove the screw, and then the cover.

2. Remove
frame.

the

module

from

the

key

z Dispose of used battery according
to the local laws.
Replace the battery by following these
procedures:

## p.18 Side doors-

Side doors-
4. Install the lid with the 2 screws.
5. Install the module into the key frame
and secure the cover with the screw.
6. When pushing any switch on the wireless key, make sure the indicator light
comes on.

NOTICE
z Make sure the positive side and
negative side of the battery are
faced correctly.
3. Remove the 2 screws to take out the
lid of the module. Take out the discharged battery and put in a new battery with the positive side up.

NOTICE
Do not bend the terminals.

z Do not replace the battery with wet
hands. Water may cause unexpected
rust.
z Do not touch or move any components inside the transmitter, or it
may interfere with proper operation.
z Be careful not to bend the electrode
when inserting the battery and that
dust or oils do not adhere to the
case.
z Take care not to lose the screws.
z Close the cover securely.

LOCKING AND UNLOCKING WITH KEY
Insert the key into the keyhole and turn
it.
To lock: Turn the key forward.
To unlock: Turn the key backward.
All the side doors and back door lock and
unlock simultaneously with either front
side door. In the driver's door lock, turning the key once will unlock the driver's
door and twice in succession will unlock
all the side doors and back door simultaneously.*
NOTE: *The 2-step unlocking function can
be changed. Ask your Toyota dealer for
details.

## p.19 LOCKING

LOCKING
AND
UNLOCKING
POWER DOOR LOCK SWITCH

WITH

Push the switch.

l12093a

To lock: Push the switch down on the
front side.
To unlock: Push the switch down on the
rear side.
All the side doors and back door lock or
unlock simultaneously.

LOCKING
AND
UNLOCKING
INSIDE LOCK KNOB

WITH

Driver's side

When the front doors are locked from the
outside or locked with the wireless remote
control key, the power door lock switch
will not work until the either front door is
unlocked with the key, lock knob, or wireless remote control key.

Move the lock knob.
To lock: Push the knob forward.
To unlock: Pull the knob backward.
The front doors can be opened by pulling
the inside handles even if the lock knob
are in the lock position.
Closing the side door with the lock knob
in the lock position will also lock the side
door. Be careful not to lock your keys in
the vehicle.
Front side doors cannot be locked when
either front side door is open and the key
is in the ignition.

l12046a

Passenger's side

## p.20 -Automatic door locking and

-Automatic door locking and
unlocking functions
CAUTION
Before driving, be sure that the doors
are closed and locked, especially
when small children are in the vehicle. Along with the proper use of
seat belts, locking the doors helps
prevent the driver and passengers
from being thrown out from the vehicle during an accident. It also helps
prevent the doors from being opened
unintentionally.
REAR DOOR CHILD-PROTECTORS

You can select the following modes of
the automatic locking and unlocking
functions. The initial mode is mode 1.

 Mode 1-Automatic locking operation
linked to shift lever position
All doors are automatically locked when
the shift lever is moved out of "P"
position, the engine is running and all
the doors are closed.

 Mode 2-Automatic locking operation
linked to vehicle speed
All doors are automatically locked when
the vehicle speed goes above about 20
km/h (12 mph).

Move the lock lever to the "LOCK"
position as shown on the label.

 Mode 3-Automatic unlocking opera-

When the child-protector is locked, you
cannot open the rear door by the inside
door handle. We recommend using this
feature whenever small children are in the
vehicle.

All doors are automatically unlocked
when the driver's door is opened within
10 seconds after the ignition switch is
turned to the "ACC" or "LOCK" position, or the key is removed.

tion linked to the ignition switch

 Mode 4-Automatic unlocking operation linked to shift lever position
All doors are automatically unlocked
when the selector lever is moved to
"P" position.

## p.21 SETTING FUNCTIONS

SETTING FUNCTIONS
You can set the following functions by
yourself.
To set the mode 1 (the automatic locking operation linked to shift lever position):

3. Within 10 seconds of turning the ignition switch to the "ON" position, press
and hold the front of the driver's side
power door lock switch for 5 seconds
and then release it.
4. The doors will be locked and unlocked
to indicate that the function is set.

1. Set the parking brake, close all doors
and turn the ignition switch to the "ON"
position.

To cancel the function, do the above operation again.

2. Shift the selector lever into the "P"
position.

To set the mode 3 (the automatic unlocking operation linked to the ignition
switch):

3. Within 10 seconds of turning the ignition switch to the "ON" position, press
and hold the front of the driver's side
power door lock switch for 5 seconds
and then release it.
4. The doors will be locked and unlocked
to indicate that the function is set.
To cancel the function, do the above operation again.
To set the mode 2 (the automatic locking operation linked to vehicle speed):
1. Set the parking brake, close all doors
and turn the ignition switch to the "ON"
position.
2. Shift the selector lever from the "P"
into the "N" position.

1. Set the parking brake, close all doors
and turn the ignition switch to the "ON"
position.
2. Shift the selector lever into the "P"
into the "N" position.
3. Within 10 seconds of turning the ignition switch to the "ON" position, press
and hold the rear of the driver's side
power door lock switch for 5 seconds
and then release it.
4. The doors will be locked and unlocked
to indicate that the function is set.

To set the mode 4 (the automatic unlocking operation linked to shift lever
position):
1. Set the parking brake, close all doors
and turn the ignition switch to the "ON"
position.
2. Shift the selector lever into the "P"
position.
3. Within 10 seconds of turning the ignition switch to the "ON" position, press
and hold the rear of the driver's side
power door lock switch for 5 seconds
and then release it.
4. The doors will be locked and unlocked
to indicate that the function is set.
To cancel the function, do the above operation again.

CAUTION
To prevent an accident, set and cancel the function with the parking
brake set securely.

To cancel the function, do the above operation again.

## p.22 Power windows

Power windows
Window lock
switch
The windows can be operated with the
switch on each side door.
The power windows work when the ignition
switch is in the "ON" position.
Key off operation: If both front doors are
closed, they work for 45 seconds even
after the ignition switch is turned off. They
stop working when either front door is
opened.
OPERATING THE DRIVER'S WINDOW
Use the switch on the driver's door.
Normal operation: The window moves as
long as you hold the switch.
To open: Lightly push down the switch.
To close: Lightly pull up the switch.
l12088a

Automatic operation: Push the switch
completely down or pull it completely up,
and then release it. The window will fully
open or close. To stop the window partway, lightly move the switch in the opposite direction and then release it.

OPERATING
DOWS

Jam protection function: If something
gets caught between the window and window frame during automatic closing operation or key off closing operation, the window stops and opens halfway.

Normal operation: The window moves as
long as you hold the switch.

If the window receives a strong impact,
this function may work even if nothing is
caught.

THE

PASSENGERS'

WIN-

Use the switch on each passenger's
door or the switches on the driver's
door that control each passenger's window.

To open: Lightly push down the switch.
To close: Lightly pull up the switch.
If you push in the window lock switch on
the driver's door, the passengers' windows
cannot be operated.
The indicator lights on the switch tell you
which of the switches can be operated.

## p.23 CAUTION

CAUTION
To avoid serious personal injury, you
must do the following.

 Before you close the power win12C007b
Automatic operation: Push the switch
completely down or pull it completely up,
and then release it. The window will fully
open or close. To stop the window partway, lightly move the switch in the opposite direction and then release it.
Jam protection function: If something
gets caught between the window and window frame during automatic closing operation or key off closing operation, the window stops and opens halfway.
If the window receives a strong impact,
this function may work even if nothing is
caught.

dows, always make sure there is
nobody around the power windows.
You must also make sure the
heads, hands and other parts of the
bodies of all occupants are kept
completely inside the vehicle. If
someone's neck, head or hands get
caught in a closing window, it
could result in death or serious injury. When anyone closes the power
windows, make sure he or she operates the windows safely.

 When small children are in the vehicle, never let them use the power
window switches without supervision. Use the window lock switch to
prevent them from making unexpected use of the switches.

 Be sure to remove the ignition key
when you leave your vehicle.

## p.24 Power quarter windows

Power quarter windows
 Never leave anyone (particularly a

CAUTION

small child) alone in your vehicle,
especially with the ignition key still
inserted. Otherwise, he or she
could use the power window
switches and get trapped in a window. Unattended person (particularly a small child) can be involved in
a serious accident.

To avoid serious personal injury, you
must do the following.

 Before you close the power quarter

 Never try jamming any part of your
body in a window to activate the
jam protection function intentionally.

 The jam protection function may
not work if something gets caught
just before the window is fully
closed.

The rear quarter windows can be operated with the "REAR VENT" switches
on the instrument panel.
The power rear quarter windows work
when the ignition switch is in the "ON"
position.
Both left and right rear quarter windows
move as long as you hold the switch.
To open: Push the right one of
switches.
To close: Push the left one of
switches.

the
the

windows, always make sure there is
nobody around the power quarter
windows. You must also make sure
the hands and other parts of the
bodies of all occupants are kept
completely inside the vehicle. If
someone's hands get caught in a
closing window, it could result in a
serious injury. When anyone closes
the power quarter windows, make
sure he or she operates the windows safely.

 Be sure to remove the ignition key
when you leave your vehicle.

 Never leave anyone (particularly a
small child) alone in your vehicle,
especially with the ignition key still
inserted. Otherwise, he or she
could use the power quarter window switches and get trapped in a
window. Unattended person (particularly a small child) can be involved
in a serious accident.

## p.25 Back door

Back door

LOCKING AND UNLOCKING WITH KEY
Insert the key into the key hole and
turn it.
To lock: Turn the key clockwise.
To unlock: Turn the key counterclockwise.
All the doors lock and unlock simultaneously with back door.
Operating the power door lock switch simultaneously locks or unlocks all the side
doors and the back door. (See "-Locking
and unlocking doors" on page 14 and
"Side doors" on page 18.)

Pull the handle toward you and pull
down the lower side of the back door.

LOCKING AND UNLOCKING FROM INSIDE

When closing the back door, make sure
it is fully closed.

To lock: Push the knob.
To unlock: Pull the knob.

See "Cargo and luggage" on page 230 for
precautions when loading luggage.

Operating the power door lock switch simultaneously locks or unlocks all the side
doors and the back door. (See "Side
doors" on page 18.)

To open the back door, pull the lock release lever.

## p.26 CAUTION

CAUTION

 Keep the back door closed while
driving. This not only keeps the
luggage from being thrown out but
also prevents exhaust gases from
entering the vehicle.

 If the open back door hides the

Push the handle and push down the
lower side of the back door.
When closing the back door, make sure
it is fully closed.
See "Cargo and luggage" on page 230 for
precautions when loading luggage.

stop and tail lights, rear turn signal
lights or rear retro reflectors while
you are parked, other road users
must be warned of the presence of
your vehicle by a warning triangle
or other device.

BACK DOOR CHILD-PROTECTOR
Move the lock lever to the "LOCK"
position as shown on the label.
When the child-protector is locked, you
cannot open the back door by the inside
door handle. We recommend using this
feature whenever small children are in the
vehicle.

## p.27 Hood

Hood
CAUTION
Before driving, be sure that the back
door is closed and locked, especially
when small children are in the vehicle. Along with the proper use of
seat belts, locking the doors helps
prevent the driver and passengers
from being thrown out from the vehicle during an accident. It also helps
prevent the doors from being opened
unintentionally.
To open the hood:
1. Pull the hood lock release lever. The
hood will spring up slightly.

CAUTION
Before driving, be sure that the hood
is closed and securely locked. Otherwise, the hood may open unexpectedly while driving and an accident may
occur.

2. In front of the vehicle, pull up the
auxiliary catch lever and lift the
hood.
Before closing the hood, check to see that
you have not forgotten any tools, rags,
etc. Then lower the hood and make sure
it locks into place. If necessary, press
down gently on the front edge to lock it.

## p.28 Theft deterrent system

Theft deterrent system
The system will automatically be set after
30 seconds. When the system is set, the
indicator light will start flashing again.
4. After making sure the indicator light
starts flashing, you may leave the vehicle.
Never leave anyone in the vehicle when
you set the system, because unlocking
from the inside will activate the system.
WHEN THE SYSTEM IS SET
Activating the system
To deter vehicle theft, the system is
designed to sound an alarm if any of
the side doors, back door or hood is
forcibly unlocked or opened or the battery terminal is disconnected and then
reconnected when the vehicle is locked.
The alarm blows the horn intermittently
and flashes the headlights, tail lights and
other exterior lights.

SETTING THE SYSTEM
1. Turn the ignition key to the "LOCK"
position and remove it.
The indicator light will start flashing when
the key is removed from the ignition
switch. (See "Engine immobilizer system"
on page 12 for details.)
2. Have all passengers get out of the
vehicle.
3. Close and lock all the side doors, back
door and hood.
The indicator light will come on when all
the side doors, back door and hood are
closed and locked.

The system will sound the alarm under
the following conditions:

 If any of the side doors is unlocked or

opened without the key or wireless remote control key, or if the back door
or hood is forcibly opened

 If the battery terminal is disconnected
and then reconnected

The indicator light will come on when the
system is activated.

## p.29 Fuel tank cap

Fuel tank cap
If any of the side door or back door is
unlocked without the key or wireless remote control key and the key is not in the
ignition switch, all the side doors and
back door will be automatically locked
again.
After one minute, the alarm will automatically stop and the indicator light will starts
flashing again.
Reactivating the alarm
Once set, the system automatically resets
the alarm after the alarm stops.
The alarm will activate again under the
same
circumstances
described
in
"Activating the system".
Stopping the alarm
The alarm will be stopped by the following
two ways:

 Turn the ignition key from the "LOCK"
to "ON" position.

TESTING THE SYSTEM
1. Open all the windows.
2. Set the system as described above.
The side doors and back door should
be locked with the key or wireless remote control key. Be sure to wait until
the indicator light goes off or starts
flashing.

3. Unlock any side door or back door
from the inside. The system should activate the alarm.
4. Stop the alarm as described above.
5. Repeat this operation for the other
doors, back door and hood. When testing the hood, also check that the system is activated when the battery terminal
is
disconnected
and
then
reconnected.

This indicates that the fuel filler door
is on the left side of your vehicle.

If the system does not work properly,
have it checked by your Toyota dealer.

 Unlock any of the side doors or back

door with the key or wireless remote
control key.

These ways cancel the system at the
same time.

## p.30 CAUTION

CAUTION

 Make sure the cap is installed securely to prevent fuel spillage in
the event of an accident.
1. To open the fuel filler door, pull the
lever.
When refueling, turn off the engine.

CAUTION

 Do not smoke, cause sparks or allow open flames when refueling.
The fumes are flammable.

 When opening the cap, do not remove the cap quickly. In hot weather, fuel under pressure could cause
injury by spraying out of the filler
neck if the cap is suddenly removed.

2. To remove the fuel tank cap, turn
the cap slowly counterclockwise,
then pause slightly before removing
it. After removing the cap, hang it
on the cap hanger.
It is not unusual to hear a slight swoosh
when the cap is opened. When installing,
turn the cap clockwise till you hear a
click.
If the cap is not tightened securely, the
malfunction indicator lamp comes on.
Make sure the cap is tightened securely.

 Use only a genuine Toyota fuel tank
cap for replacement. It is designed
to regulate fuel tank pressure.

## p.31 Electric moon roof

Electric moon roof
To operate the moon roof, use the
switches beside the personal light.
The moon roof works when the ignition
switch is in the "ON" position. However,
if both front doors are closed, it works for
45 seconds even after the ignition switch
is turned off. It stops working when either
of the front doors is opened.
Sun shade operation-
The sun shade can be opened or closed
by hand.
Sliding operation-
Sliding operation

To open: Push the switch on the rear
side.
The roof will open and stop partway 30
mm (1.2 in.) from the fully opened position. When you push the switch again, the
moon roof will open fully. To stop the roof
partway, push the same switch or tilt
switch while the roof is moving.
As driving with the moon roof opened fully
will cause wind throbs, we recommend
you to drive with the moon roof partway
30 mm (1.2 in.) from the fully opened
position.

Tilting operation

The roof will fully close. To stop the roof
partway, push the same switch or tilt
switch.
Tilting operation-
To tilt up: Push the switch on the "UP"
side.
The roof will tilt up fully. To stop the roof
partway, push the same switch or slide
switch.
To lower: Push the switch on the opposite
side of the "UP" side.
The roof will fully close. To stop the roof
partway, push the same switch or slide
switch.
Jam protection function (closing operation only): If something gets caught between the moon roof and frame during
closing operation, the moon roof stops and
opens halfway.
If an impact is given to the moon roof,
this function may work without anything
caught.

The sun shade will be opened together
with the roof.
To close: Push the switch on the front
side.

## p.32 If the battery terminals is disconnected

If the battery terminals is disconnected
or the battery is run down, the moon
roof may not operate automatically and
the jam protection function will not operate
correctly after you reconnect, replace or
recharge the battery with the moon roof
slide-opened or tilted up. In any of these
cases, you should return the moon roof to
normal.
To normalize the moon roof, push and
hold the switch until the moon roof is
closed or tilted down completely.
Make sure the moon roof opens and
closes automatically. If the moon roof cannot be operated properly, have it checked
by your Toyota dealer.

CAUTION
To avoid serious personal injury, you
must do the following.

 While the vehicle is moving, always
keep the heads, hands and other
parts of the bodies of all occupants
away from the roof opening. Otherwise, they could be seriously injured if the vehicle stops suddenly
or if the vehicle is involved in an
accident.

 Before you close the moon roof,
always make sure there is nobody
around the moon roof. You must
also make sure nobody places his
or her head, hands and other parts
of the body in the roof opening. If
someone's neck, head or hands get
caught in the closing roof, it could
result in death or serious injury.
When anyone closes the moon roof,
first make sure it is safe to do so.

 Be sure to remove the ignition key
when you leave your vehicle.

 Never leave anyone (particularly a
small child) alone in your vehicle,
especially with the ignition key still
inserted. Otherwise, he or she
could use the moon roof switches
and get trapped in the roof opening. Unattended person (particularly
a small child) can be involved in a
serious accident.

 Never sit on top of the vehicle
around the roof opening.

 Never try jamming any part of your
body to activate the jam protection
function intentionally.

 The jam protection function may
not work when something gets
caught just before the moon roof is
fully closed.

# Section 1-3: Occupant restraint systems

## p.33 SECTION

SECTION

1- 3

OPERATION OF INSTRUMENTS AND
CONTROLS
Occupant restraint systems
Seats . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 34
Front seats . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 34
Armrest . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 37
Rear seats . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 37
Head restraints . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 46
Seat heaters . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 47
Seat belts . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 48
SRS driver airbag and front passenger airbag . . . . . . . . . . . . . . . . . . . 58
SRS side airbags and curtain shield airbags with
roll sensing function . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 65
Child restraint . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 76

## p.34 Front seats-

Front seats-
-Front seat precautions

Seats
While the vehicle is being driven, all vehicle occupants should have the seatback
upright, sit well back in the seat and properly wear the seat belts provided.

CAUTION

 Do not drive the vehicle unless the
occupants are properly seated. Do
not allow any passengers to sit on
top of a folded-down seatback, or
in the luggage compartment or cargo area. Persons not properly
seated and/or not properly restrained by seat belts can be severely injured in the event of emergency braking or a collision.

 During driving, do not allow any
passengers to stand up or move
around between seats. Otherwise,
severe injuries can occur in the
event of emergency braking or a
collision.

Driver seat

 Slightly recline the back of the
CAUTION

The SRS driver airbag deploys with
considerable force, and can cause
death or serious injury especially if
the driver is very close to the airbag.
The National Highway Traffic Safety
Administration ("NHTSA") advises:
Since the risk zone for driver airbag
is the first 50 - 75 mm (2 - 3 in.) of
inflation, placing yourself 250 mm (10
in.) from your driver airbag provides
you with a clear margin of safety.
This distance is measured from the
center of the steering wheel to your
breastbone. If you sit less than 250
mm (10 in.) away now, you can
change your driving position in several ways:

 Move your seat to the rear as far
as you can while still reaching the
pedals comfortably.

seat. Although vehicle designs vary,
many drivers can achieve the 250
mm (10 in.) distance, even with the
driver seat all the way forward, simply by reclining the back of the
seat somewhat. If reclining the back
of your seat makes it hard to see
the road, raise yourself by using a
firm, non-slippery cushion, or raise
the seat if your vehicle has that
feature.

 If your steering wheel is adjustable,
tilt it downward. This points the airbag toward your chest instead of
your head and neck.
The seat should be adjusted as recommended by NHTSA above, while
still maintaining control of the foot
pedals, steering wheel, and your view
of the instrument panel controls.

## p.35 -Seat adjustment

-Seat adjustment
precautions
Front passenger seat

Front seats (with SRS side airbags)

CAUTION

CAUTION

CAUTION

 Do not adjust the seat while the

The SRS front passenger airbag also
deploys with considerable force, and
can cause death or serious injury especially if the front passenger is very
close to the airbag. The front passenger seat should be as far from the
airbag as possible with the seatback
adjusted, so the front passenger sits
upright.

The SRS side airbags are installed in
the driver and front passenger seats.
Observe the following precautions.

vehicle is moving as the seat may
unexpectedly move and cause the
driver to lose control of the vehicle.
 Be careful that the seat does not
hit a passenger, luggage or the rear
seat.

 Do not lean against the front door
when the vehicle is in use, since
the side airbag inflates with considerable speed and force. Otherwise,
you may be killed or severely injured.

 Do not use seat accessories which
cover the area where the side airbags inflate. Such accessories may
prevent the side airbags from activating correctly, causing death or
serious injury.

NOTICE
Do not operate the control switch in
more than one dimension at a time.
It may cause electrical overload.

 Do not modify or replace the seats
or upholstery of the seats equipped
with side airbags. Such change may
prevent the side airbag system from
activating correctly, disable the system or cause the side airbags to
inflate accidentally, resulting in
death or serious injury.

## p.36 -Adjusting front seats

-Adjusting front seats
1. SEAT POSITION AND SEAT CUSHION
ANGLE ADJUSTING SWITCH
Move the control switch in the desired
direction.
Releasing the switch will stop the seat at
that position.
Do not place anything under the front
seats, as this might interfere with the seat
movement.
2. SEATBACK
SWITCH

I13380b

ANGLE

ADJUSTING

Move the control switch in the desired
direction.
Releasing the switch will stop the seatback at that position.

CAUTION
Avoid reclining the seatback any
more than needed. The seat belts provide maximum protection in a frontal
or rear collision when the driver and
the front passenger are sitting up
straight and well back in the seats. If
you are reclined, the lap belt may
slide past your hips and apply restraint forces directly to the abdomen
or your neck may contact the shoulder belt. In the event of a frontal
collision, the more the seat is reclined, the greater the risk of death
or personal injury.
3. SEAT LUMBAR SUPPORT ADJUSTING SWITCH
Push the control switch on either side.
The amount of lumbar support will change
while the switch is pushed.

## p.37 Rear seats-

Rear seats-
-Rear seat precautions

Armrest

CAUTION

 Do not adjust the seat while the
vehicle is moving.

Tumbling the seats will enlarge the luggage compartment. See "Cargo and luggage" on page 230 for precautions when
loading luggage.

 Be careful that the seat does not
hit a passenger or luggage.

 After adjusting the seatback, push
your body back against the seat to
make sure the seat is locked in
position.

 When returning seats to their origiTo use the armrest, pull it down as
shown above.

NOTICE
To prevent damage to the armrest,
avoid putting heavy loads on it.

nal position, observe the following
in order to prevent personal injury
in a collision or sudden stop:
Make sure the seat is securely
locked by pushing forward and rearward on the top of the seatback
and by trying to pull up the edge
of the bottom cushion. Failure to
do so will prevent seat belt from
operating properly.
Make sure the seat belts are not
twisted or caught under the seat
and are arranged in their proper
position and are ready to use.

## p.38 -Moving second

-Moving second
third seat entry

-Adjusting second seats

seat

for

SEATBACK ANGLE ADJUSTING LEVER
Lean forward and pull the lever toward
you. Then lean back to the desired
angle and release the lever.

CAUTION

 Avoid reclining the seatback any

I13220c

more than needed. The seat belts
provide maximum protection in a
frontal or rear collision when the
second seat passengers are sitting
up straight and well back in the
seats. If you are reclined, the lap
belt may slide past your hips and
apply restraint forces directly to the
abdomen or your neck may contact
the shoulder belt. In the event of a
frontal collision, the more the seat
is reclined, the greater the risk of
death or personal injury.

 Do not adjust the seat while the
vehicle is moving.

 After adjusting the seatback, push
your body back against the seat to
make sure the seat is locked in
position.

For easy access to the third seat:
1. Lower the head restraint to the lowest position.
2. Push the seatback angle adjusting
lever and pull the seat cushion lock
release lever or pull the strap.
After passengers are in, return the seat
until it locks.

## p.39 -Tumbling second seat

-Tumbling second seat
CAUTION
After returning the seat, make sure
the seat is securely locked by pushing forward and rearward on the top
of the seatback and by trying to pull
up the edge of the bottom cushion.

I13378b

BEFORE TUMBLING SECOND SEAT
1. Stow the second seat belt buckles
as shown in the illustration.
This prevents the seat belt buckles from
falling out when you tumble the second
seat.

I13340a

2. Make sure the shoulder belt passes
through the hanger when folding the
second seat.
This prevents the shoulder belt from being
damaged.

CAUTION

NOTICE
The seat belt buckles must be stowed
before you tumble the second seat.

The seat belt must be removed from
the hanger when the seat belt is in
use.

## p.40 TUMBLING SECOND SEAT

TUMBLING SECOND SEAT
1. Lower the outer head restraint to the
lowest position and pull up the center head restraint. Unlock the seatback and fold it down.
Tumbling the rear seats will enlarge the
luggage compartment. See "Cargo and
luggage" on page 230 for precautions
when loading luggage.

2. Unlock the seat cushion. Swing the
whole seat up and forward.

3. Hook the strap.
When returning the second seat to its
original position, put the holding strap into
the hole.

## p.41 CAUTION

CAUTION
When returning seats to their original
position, observe the following precautions in order to prevent personal
injury in a collision or sudden stop:

 Make sure the seat is securely
locked by pushing forward and rearward on the top of the seatback
and by trying to pull up the edge
of the bottom cushion. Failure to
do so will prevent seat belt from
operating properly.
4. Remove the seat hook covers from
the back of the seat cushion, and
install them over the seat hooks.

CAUTION
Be sure to apply the covers on the
seat hooks, or you may get burned
when they become hot.

WHEN RETURNING THE SECOND SEAT

 Make sure the seat belts are not

If you cannot raise the seatback because of the locked seat belt, do not
try it hard. Release the lock of the seat
belt in the following way. Push in the
lower front edge of the seatback cushion to slacken the seat belt (1) and let
the seat belt retract a little (2).

twisted or caught under the seat
and are arranged in their proper
position and are ready to use.

When returning the second seat to its
original position, remove the seat hook
covers from the floor and install them in
the back of the seat cushion.

## p.42 -Adjusting third seats

-Adjusting third seats

-Tumbling third seats
SEATBACK ANGLE ADJUSTING LEVER
Lean forward and pull the lever toward
you. Then lean back to the desired
angle and release the lever.

CAUTION

 Avoid reclining the seatback any
more than needed. The seat belts
provide maximum protection in a
frontal or rear collision when the
third seat passengers are sitting up
straight and well back in the seats.
If you are reclined, the lap belt may
slide past your hips and apply restraint forces directly to the abdomen or your neck may contact the
shoulder belt. In the event of a
frontal collision, the more the seat
is reclined, the greater the risk of
death or personal injury.

 Do not adjust the seat while the
vehicle is moving.

 After adjusting the seatback, push
your body back against the seat to
make sure the seat is locked in
position.

I13377b

BEFORE TUMBLING THIRD SEAT
1. Stow the third seat belt and buckles
as shown in the illustration.
This prevents the seat belt and buckles
from falling out when you tumble the third
seat.

NOTICE
The seat belt and buckles must be
stowed before you tumble the third
seat.

## p.43 I13262c

I13262c

2. Make sure the shoulder belt passes
through the hanger when folding the
third seat.
This prevents the shoulder belt from being
damaged.

CAUTION
The seat belt must be removed from
the hanger when the seat belt is in
use.

TUMBLING THIRD SEAT
1. Lower the head restraint to the lowest position. Unlock the seatback
and fold it down.

2. Unlock the seat cushion and slide
the whole seat to the rear-most
position while pulling up the handle.

Tumbling the third seats will enlarge the
luggage compartment. See "Cargo and
luggage" on page 230 for precautions
when loading luggage.

## p.44 13c558
3. Swing the whole seat up.

4. Hook the strap.
When returning the third seat to its original position, put the holding strap into the
hole.
5. Remove the seat hook covers from
the back of the seat cushion, and
install them over the seat hooks.

CAUTION
Be sure to apply the covers on the
seat hooks, or you may get burned
when they become hot.
When returning the third seat to its original position, remove the seat hook covers
from the floor and install them in the back
of the seat cushion.

## p.45 -Removing third seats

-Removing third seats
CAUTION
When returning seats to their original
position, observe the following precautions in order to prevent personal
injury in a collision or sudden stop:

 Make sure the seat is securely
locked by pushing forward and rearward on the top of the seatback
and by trying to pull up the edge
of the bottom cushion. Be certain
to replace head restraint. Failure to
do so will prevent seat belt from
operating properly.

 Make sure the seat belts are not
twisted or caught under the seat
and are arranged in their proper
position and are ready to use.

After tumbling the third seat, open the
cover, hold the whole seat and pull it
up while pulling the handle toward you.
Removing the third seat will enlarge the
luggage compartment. See "Cargo and
luggage" on page 230 for precautions
when loading luggage.

Remove the seat hook covers from the
back of the seat cushion, and install
them over the seat hooks.

CAUTION
Be sure to apply the covers on the
seat hooks, or you may get burned
when they become hot.
When returning the third seat to its original position, remove the seat hook covers
from the floor and install them in the back
of the seat cushion.

## p.46 Head restraints

Head restraints
CAUTION
When removing or reinstalling the
seat, observe the following precautions to prevent personal injury:

 Do not fold or remove the seat
while the vehicle is moving.

 Be careful not to get your hands or

 When reinstalling the seat, be careful not to hit the seat against you
or inside of the vehicle.

 Install each seat in the same position from which it was removed.
Failure to do so will prevent third
seat occupants from using seat
belts properly.

feet pinched in the seat.

 Be careful not to hit the removed
seat against a person or drop it on
yourself.

 After

tumbling or installing the
seat, push it forward and backward
to make sure it is locked in position.

NOTICE
Avoid putting heavy loads on the removed seat. The metallic tips of the
seat legs may be damaged and the
seat cannot be reinstalled.

Front

To prevent personal injury in a collision or sudden stop:

 Do not sit on or place anything on
the folded seatback while driving.

I13375b

 Do not leave the removed seat
loose in the vehicle.

 Do not try to sit on or place anything on the removed seat.

Rear

## p.47 Seat heaters

Seat heaters
For your safety and comfort, adjust the
head restraint before driving.

Right side
front seat

To raise: Pull it up.
To lower: Push it down while pressing the
lock release button.
Front head restraint only-You can also
move the head restraint forward or backward. If such adjustment is desired, pull
or push the head restraint.
Rear center head restraint-When an occupant sits on the rear center seat, always pull up the rear center head restraint to the lock position.
The head restraint is most effective when
it is close to your head. Therefore, using
a cushion on the seatback is not recommended.

CAUTION

 Adjust the center of the head restraint so that it is closest to the
top of your ears.

CAUTION
Occupants must use caution when operating the seat heater because it
may make them feel too hot or cause
burns at low temperatures (erythema,
varicella). Use extra caution for;

Left side
front seat

To turn on the seat heater, push the
switch to "HI" (high heating temperature) or "LO" (low heating temperature).
At this time, the indicator light on either side will illuminate to indicate the
seat heater is operating. To turn off the
seat heater, push the switch lightly on
the opposite side.

 Babies, small children, elderly persons, sick persons or persons with
physical disabilities

 Persons who have delicate skin
 Persons who are exhausted
 Persons who have taken alcohol or
drugs which induce sleep (sleeping
drug, cold remedy, etc.)
To prevent the seat from overheating,
do not use the seat heater with a
blanket, cushion, or other insulating
objects which cover the seat.

The ignition key must be in the "ON" position to operate seat heaters.

 After adjusting the head restraint,
make sure it is locked in position.

 Do not drive with the head restraints removed.

## p.48 Seat belts-

Seat belts-
-Seat belt precautions
NOTICE
z Do not put unevenly weighed objects on the seat and do not stick
sharp objects (needles, nails, etc.)
into the seat.
z When cleaning the seats, do not
use organic substances (paint thinner, benzine, alcohol, gasoline,
etc.). They may damage the heater
and seat surface.
z To prevent the battery from being
discharged, turn the switch off
when the engine is not running.

Toyota strongly urges that the driver and
passengers in the vehicle be properly restrained at all times with the seat belts
provided. Failure to do so could increase
the chance of injury and/or the severity of
injury in accidents.
The seat belts provided for your vehicle
are designed for people of adult size,
large enough to properly wear them.
Child. Use a child restraint system appropriate for the child until the child becomes large enough to properly wear the
vehicle's seat belts. (For details, see
"Child restraint" on page 76.)
If a child is too large for a child restraint
system, the child should sit in the rear
seat and must be restrained using the
vehicle's seat belt. According to accident
statistics, the child is safer when properly
restrained in the rear seat than in the
front seat.
If a child must sit in the front seat, the
seat belts should be worn properly. If an
accident occurs and the seat belts are not
worn properly, the force of the rapid inflation of the airbag may cause death or
serious injury to the child.

Do not allow any children to stand up or
kneel on either rear or front seats. An
unrestrained child could suffer serious injury or death during emergency braking or
a collision. Also, do not let the child sit
on your lap. Holding a child in your arms
does not provide sufficient restraint.
Pregnant woman. Toyota recommends the
use of a seat belt. Ask your doctor for
specific recommendations. The lap belt
should be worn securely and as low as
possible over the hips and not on the
waist.
Injured person. Toyota recommends the
use of a seat belt. Depending on the injury, first check with your doctor for specific
recommendations.

## p.49 -Fastening 3-point seat belts

-Fastening 3-point seat belts
CAUTION
Persons should ride in their seats
properly wearing their seat belts
whenever the vehicle is moving.
Otherwise, they are much more likely
to suffer serious bodily injury or
death in the event of sudden braking
or a collision.
When using the seat belts, observe
the following:

 Use the belt for only one person at
a time. Do not use a single belt for
two or more people-even children.

 Avoid reclining the seatback any
more than needed. The seat belts
provide maximum protection in a
frontal or rear collision when the
driver and the front passenger are
sitting up straight and well back in
the seats. If you are reclined, the
lap belt may slide past your hips
and apply restraint forces directly
to the abdomen or your neck may
contact the shoulder belt. In the
event of a frontal collision, the
more the seat is reclined, the greater the risk of death or personal injury.

 Be careful not to damage the belt
webbing or hardware. Take care that
they do not get caught or pinched
in the seat or doors.

 Inspect the belt system periodically.
Check for cuts, fraying, and loose
parts. Damaged parts should be replaced. Do not disassemble or
modify the system.

 Keep the belts clean and dry. If
they need cleaning, use a mild soap
solution or lukewarm water. Never
use bleach, dye, or abrasive cleaners, or allow them to come into
contact with the belt-they may severely weaken the belts. (See
"Cleaning the interior" on page
279.)

 Replace the belt assembly (including bolts) if it has been used in a
severe impact. The entire assembly
should be replaced even if damage
is not obvious.

Tab
Buckle

Adjust the seat as needed and sit up
straight and well back in the seat. To
fasten your belt, pull it out of the retractor and insert the tab into the
buckle.
You will hear a click when the tab locks
into the buckle.
The seat belt length automatically adjusts
to your size and the seat position.
The retractor will lock the belt during a
sudden stop or on impact. It also may
lock if you lean forward too quickly. A
slow easy motion will allow the belt to
extend, and you can move around freely.

## p.50 When a passenger's shoulder belt is completely extended and is then retracted

When a passenger's shoulder belt is completely extended and is then retracted
even slightly, the belt is locked in that
position and cannot be extended. This feature is used to hold the child restraint
system securely. (For details, see "Child
restraint" on page 76.) To free the belt
again, fully retract the belt and then pull
the belt out once more.
If the seat belt cannot be pulled out of the
retractor, firmly pull the belt and release
it. You will then be able to smoothly pull
the belt out of the retractor.

CAUTION

 After inserting the tab, make sure
the tab and buckle are locked and
that the lap and shoulder portions
of the belt are not twisted.

 Do not insert coins, clips, etc. in
the buckle as this may prevent you
from properly latching the tab and
buckle.

 If the seat belt does not function
normally, immediately contact your
Toyota dealer. Do not use the seat
until the seat belt is fixed, because
it cannot protect an adult occupant
or your child from injury.

CAUTION
Take up
slack

 Both high-positioned lap belts and
loose-fitting belts could cause serious injuries due to sliding under the
lap belt during a collision or other
unintended event. Keep the lap belt
positioned as low on hips as possible.

Too high

 Do not place the shoulder belt under your arm.

Keep as low on hips as possible

Adjust the position
shoulder belts.

of

the

lap and

Position the lap belt as low as possible
on your hips-not on your waist, then adjust it to a snug fit by pulling the shoulder
portion upward through the latch plate.

## p.51 CAUTION

CAUTION

l13197b

Seat belts with an adjustable shoulder
anchor-
Adjust the shoulder anchor position to
your size.
To raise: Slide the anchor up.
To lower: Push in the lock release button
and slide the anchor down.

Always make sure the shoulder belt
is positioned across the center of
your shoulder. The belt should be
kept away from your neck, but not
falling off your shoulder. Failure to
do so could reduce the amount of
protection in an accident and cause
serious injuries in a collision.

To release the belt, press the buckle
release button and allow the belt to
retract.
If the belt does not retract smoothly, pull
it out and check for kinks or twists. Then
make sure it remains untwisted as it retracts.

After adjustment, make sure the anchor is
locked in position.

## p.52 -Fastening 2-point seat belts

-Fastening 2-point seat belts
Lengthen

CAUTION

Too high

 After inserting the tab, make sure
the tab and buckle are locked and
that the lap portion of the belt is
not twisted.

 Do not insert coins, clips, etc. in
Tab
Buckle

Sit up straight and well back in the
seat. To fasten your belt, insert the tab
into the buckle.
You will hear a click when the tab locks
into the buckle.
If the belt is not long enough for you, hold
the tab at a right angle to the belt and
pull on the tab.

Adjust to a snug fit

the buckle as this may prevent you
from properly latching the tab and
buckle.

 If the seat belt does not function
normally, immediately contact your
Toyota dealer. Do not use the seat
until the seat belt is fixed, because
it cannot protect an adult occupant
or your child from injury.

Keep as low on hips as possible

Remove excess length of the belt and
adjust the belt position.
To shorten the belt, pull the free end of
the belt.
Position the lap belt as low as possible
on your hips-not on your waist, then adjust it to a snug fit.

CAUTION
Both high-positioned and loose-fitting lap belts could cause serious injuries due to sliding under the lap belt
during a collision or other unintended
event. Keep the lap belt positioned as
low on hips as possible.

## p.53 -Seat belt extender

-Seat belt extender
If your seat belts cannot be fastened securely because they are not long enough,
a personalized seat belt extender is available from your Toyota dealer free of
charge.
Please contact your local Toyota dealer so
that the dealer can order the proper required length for the extender. Bring the
heaviest coat you expect to wear for proper measurement and selection of length.
Additional ordering information is available
at your Toyota dealer.
To release the belt, press the buckle
release button.

CAUTION
When using the seat belt extender,
observe the following precautions.
Failure to follow these instructions
could reduce the effectiveness of the
seat belt restraint system in case of
an accident, increasing the chance of
personal injury.

 Remember that the extender provided for you may not be safe when
used on a different vehicle, for
another person, or at a different
seating position than the one originally intended.

 If the seat belt extender has been
connected to the driver's seat belt
buckle without the driver actually
wearing the seat belt, the SRS driver's airbag system will judge that
the driver is wearing it. In this
case, the driver's airbag may not
activate correctly, causing death or
serious injury in the event of collision. Be sure to wear the seat belt
with the seat belt extender.

## p.54  Do not use the seat belt extender

 Do not use the seat belt extender

CAUTION

if it is not absolutely necessary.

 After inserting the tab, make sure

 Do not use the seat belt extender

the tab and buckle are locked and
that the lap and shoulder portions
of the belt and the seat belt extender are not twisted.

when installing a child restraint
system on the front or rear passenger seat. If installing a child restraint system with the seat belt
extender connected to the seat belt,
the seat belt will not securely hold
the child restraint system, which
could cause death or serious injury
to the child or other passengers in
the event of collision.

 Do not insert coins, clips, etc. in
the buckle as this may prevent you
from properly latching the tab and
buckle.

 If the seat belt does not function
To connect the extender to the seat
belt, insert the tab into the seat belt
buckle so that the "PRESS" signs on
the buckle release buttons of the extender and the seat belt are both facing
outward as shown.
You will hear a click when the tab locks
into the buckle.
When releasing the seat belt, press on
the buckle release button on the extender,
not on the seat belt. This helps prevent
damage to the vehicle interior and extender itself.
When not in use, remove the extender
and store in the vehicle for future use.

normally, immediately contact your
Toyota dealer. Do not use the seat
until the seat belt is fixed, because
it cannot protect an adult occupant
or your child from injury.

## p.55 -Seat belt pretensioners

-Seat belt pretensioners
CAUTION

 Make sure the roll sensing of curtain shield airbags
light is not on.

off

indicator

 When the roll sensing of curtain

The seat belt pretensioners are designed to be activated in response to
a severe frontal impact or a vehicle
rollover.
When the sensor detects a severe frontal
impact or a vehicle rollover, the front seat
belts are quickly drawn back by the retractor so that the belts snugly restrain
the occupants.

Roll sensing of curtain shield airbags
off indicator light
The seat belt pretensioners will not operate in a vehicle rollover if the roll sensing
of curtain shield airbags off indicator light
is on. For details, see "Roll sensing of
curtain shield airbags off switch" on page
66.

shield airbags off switch is turned
on (and the roll sensing of curtain
shield airbags off indicator light is
on), the seat belt pretensioners will
not operate in a vehicle rollover
and turning off the seat belt pretensioners can reduce the occupant
protection which your vehicle safety
systems can provide to you in certain accidents and increase the likelihood of death or serious injuries.

The seat belt pretensioners are activated
even with no passenger in the front seat.
The seat belt pretensioners and SRS airbags may not operate together in all collisions.

## p.56 When the seat belt pretensioners are activated, an operating noise may be heard

When the seat belt pretensioners are activated, an operating noise may be heard
and a small amount of non-toxic gas may
be released. This does not indicate that
a fire is occurring. This gas is normally
harmless.
Once the seat belt pretensioners have
been activated, the seat belt retractors
remain locked.

CAUTION

 Do not modify, remove, strike or
The seat belt pretensioner system consists mainly of the following components,
and their locations are shown in the illustration.
1. Front airbag sensors
2. SRS warning light
3. Seat belt pretensioner assemblies
4. Airbag sensor assembly
The seat belt pretensioners are controlled
by the airbag sensor assembly. The airbag
sensor assembly consists of a safing sensor and airbag sensor.

open the seat belt pretensioner assemblies, airbag sensor or surrounding area or wiring. Failure to
follow these instructions may prevent the seat belt pretensioners
from activating correctly, cause sudden operation of the system or disable the system, resulting in death
or serious injury.

 Do not use tires or wheels other
than the manufacturer's recommended size. Such a use may cause
the curtain shield airbags and seat
belt pretensioners to inflate accidentally, resulting in death or serious injury. For details, see "Checking and replacing tires" on page
304.

 Do not place luggage heavier than
specified on the roof luggage carrier. Such luggage may cause the
curtain shield airbags and seat belt
pretensioners to inflate accidentally,
resulting in death or serious injury.
For details, see "Roof luggage carrier" on page 202.

 Do not modify or change the suspension system. Such changes may
cause the curtain shield airbags to
inflate accidentally, resulting in
death or serious injury.
Failure to follow these instructions
can result in death or serious injuries. Consult your Toyota dealer
about any repair and modification.

## p.57 If any of the following conditions occurs,

If any of the following conditions occurs,
this indicates a malfunction of the airbags
or seat belt pretensioners. Contact your
Toyota dealer as soon as possible.

NOTICE
Do not perform any of the following
changes without
consulting your
Toyota dealer. Such changes can
interfere with proper operation of the
seat belt pretensioners in some
cases.

 The light does not come on when the
ignition key is turned to the "ON" position or remains on for more than 6
seconds or flashes.

z Installation of electronic devices
such as a mobile two-way radio,
cassette tape player or compact
disc player
z Repairs on or near the front seat
belt retractor assemblies
z Modification of the front end structure
z Attachment of a grille guard (bull
bar, kangaroo bar, etc.), snowplow,
winches or any other equipment to
the front end
z Repairs made on or near the front
fenders, front end structure or console

 The light comes on or starts flashing
while driving.

 If any seat belt does not retract or can
This indicator comes on when the ignition key is turned to the "ON" position.
It goes off after about 6 seconds. This
means the seat belt pretensioners are
operating properly.

not be pulled out due to a malfunction
or activation of the relevant seat belt
pretensioner.

 The seat belt pretensioner assembly or
surrounding area has been damaged.

This warning light system monitors the
airbag sensor assembly, front airbag sensors, side and curtain shield airbag sensors, curtain shield airbag sensors, driver's seat position sensor, driver's seat belt
buckle switch, seat belt pretensioner assemblies, inflators, warning light, roll sensing of curtain shield airbags off indicator
light, interconnecting wiring and power
sources. (For details, see "Service reminder indicators and warning buzzers" on
page 122.)

## p.58 SRS driver airbag and front

SRS driver airbag and front
passenger airbag
CAUTION

 The SRS front airbag system is de13c560

In the following cases, contact your Toyota
dealer as soon as possible:

 The front of the vehicle (shaded in the
illustration) was involved in an accident
that was not severe enough to cause
the seat belt pretensioners to operate.

 The seat belt pretensioner assembly or

surrounding area is scratched, cracked,
or otherwise damaged.

The SRS (Supplemental Restraint System) front airbags are designed to provide further protection for the driver
and front passenger in addition to the
primary safety protection provided by
the seat belts.
In response to a severe frontal impact,
the SRS front airbags work together with
the seat belts to help reduce injury by
inflating. The SRS front airbags help reduce injuries mainly to the driver's or front
passenger's head or chest caused by hitting the vehicle interior.
The SRS front passenger airbag is activated even with no passenger in the front
seat.

Always wear your seat belt properly.

signed only as a supplement to the
primary protection of the driver and
front passenger seat belt systems.
The driver and front passenger can
be killed or seriously injured by the
inflating airbags if they do not wear
the available seat belts properly.
During sudden braking just before
a collision, an unrestrained driver
or front passenger can move forward into direct contact with or
close proximity to the airbag which
may then deploy during the collision. To ensure maximum protection
in an accident, the driver and all
passengers in the vehicle must
wear their seat belts properly. Wearing a seat belt properly during an
accident reduces the chances of
death or serious injury or being
thrown out of the vehicle. For
instructions and precautions concerning the seat belt system, see
"Seat belts" on page 48.

## p.59  Improperly seated and/or restrained

 Improperly seated and/or restrained
infants and children can be killed
or seriously injured by the deploying airbags. An infant or child who
is too small to use a seat belt
should be properly secured using a
child
restraint
system.
Toyota
strongly recommends that all infants and children be placed in the
rear seat of the vehicle and properly restrained. The rear seat is the
safest for infants and children. For
instructions concerning the installation of a child restraint system, see
"Child restraint" on page 76.

The SRS front airbags are designed to
deploy in severe (usually frontal) collisions where the magnitude and duration
of the forward deceleration of the vehicle exceeds the designed threshold
level.
The SRS front airbags will deploy if the
severity of the impact is above the designed threshold level, comparable to an
approximate 25 km/h (15 mph) collision
when the vehicle has the impact straight
into a fixed barrier that does not move or
deform.
However, this threshold velocity will be
considerably higher if the vehicle strikes
an object, such as a parked vehicle or
sign pole, which can move or deform on
impact, or if the vehicle is involved in an
underride collision (e.g. a collision in
which the front of the vehicle "underrides",
or goes under, the bed of a truck, etc.).
It is possible that in some collisions
where the forward deceleration of the vehicle is very close to the designed threshold level, the SRS front airbags and the
seat belt pretensioners may not activate
together.

Collision from the rear

Collision from the side
Vehicle rollover

The SRS front airbags are generally not
designed to inflate if the vehicle is involved in a side or rear collision, if it
rolls over, or if it is involved in a low-
speed frontal collision. But, whenever a
collision of any type causes sufficient
forward deceleration of the vehicle, deployment of the SRS front airbags may
occur.

Always wear your seat belts properly.

## p.60 Hitting a curb,

Hitting a curb,
edge of pavement
or hard surface

The front airbag sensors constantly monitor the forward deceleration of the vehicle.
If an impact results in a forward deceleration beyond the designed threshold level,
the system triggers the airbag inflators. At
this time a chemical reaction in the inflators very quickly fills the airbags with non-
toxic gas to help restrain the forward motion of the occupants. The front airbags
then quickly deflate, so that there is no
obstruction of the driver's vision should it
be necessary to continue driving.

Falling into or
jumping over a
deep hole

Landing hard or vehicle falling

The SRS front airbags may also deploy
if a severe impact occurs to the underside of your vehicle. Some examples
are shown in the illustration.

The SRS front airbag system consists
mainly of the following components, and
their locations are shown in the illustration.
1. Front airbag sensors
2. SRS warning light
3. Airbag module for front passenger
(airbag and inflator)
4. Airbag sensor assembly
5. Airbag module for driver
(airbag and inflator)
6. Driver's seat position sensor
7. Driver's seat belt buckle switch
The airbag sensor assembly consists of a
safing sensor and airbag sensor.

When the airbags inflate, they produce a
loud noise and release some smoke and
residue along with non-toxic gas. This
does not indicate a fire. This smoke may
remain inside the vehicle for some time,
and may cause some minor irritation to
the eyes, skin or breathing. Be sure to
wash off any residue as soon as possible
to prevent any potential skin irritation with
soap and water.
If you can safely exit from the vehicle,
you should do so immediately.

## p.61 Deployment of the airbags happens in a

Deployment of the airbags happens in a
fraction of a second, so the airbags must
inflate with considerable force. While the
system is designed to reduce serious injuries, primarily to the head and chest, it
may also cause other, less severe injuries
to the face, chest, arms and hands. These
are usually in the nature of minor burns
or abrasions and swelling, but the force of
a deploying airbag can cause more serious injuries, especially if an occupant's
hands, arms, chest or head is in close
proximity to the airbag module at the time
of deployment. This is why it is important
for the occupant to: avoid placing any
object or part of the body between the
occupant and the airbag module; sit
straight and well back into the seat; wear
the available seat belt properly; and sit as
far as possible from the airbag module,
while still maintaining control of the vehicle.

CAUTION
The driver or front passenger who is
too close to the steering wheel or
dashboard during airbag deployment
can be killed or seriously injured.
Toyota strongly recommends that:

 The driver sit as far back as possible from the steering wheel while
still maintaining control of the vehicle.

 The front passenger sit as far back
as possible from the dashboard.

 All vehicle occupants be properly
restrained using the available seat
belts.

 If the seat belt extender has been
connected to the driver's seat belt
buckle without wearing the seat belt
when using the extender in the
driver's seat, the SRS driver's airbag system will judge that the driver wears the seat belt even if not
wearing it. In this case, the driver's
airbag may not activate correctly,
causing death or serious injury in
the event of collision. Be sure to
wear the seat belt with the seat belt
extender.
For instructions and precautions concerning the seating position, see
"-Front seat precautions" on page
34.

Parts of the airbag module (steering wheel
hub, airbag cover and inflator) may be hot
for several minutes after deployment, so
do not touch! The airbags inflate only
once. The windshield may be damaged by
absorbing some of the force of the inflating airbag.

## p.62  Do not hold a child on your lap or

 Do not hold a child on your lap or
in your arms. Use a child restraint
system in the rear seat. For instructions concerning the installation of
a child restraint system, see "Child
restraint" on page 76.

 Do not sit on the edge of the seat

 Toyota strongly recommends that all

or lean against the dashboard when
the vehicle is in use, since the
front passenger airbag could inflate
with considerable speed and force.
Anyone who is up against, or very
close to, an airbag when it inflates,
can be killed or seriously injured.
Sit up straight and well back in the
seat, and always use your seat belt
properly.

infants and children be placed in
the rear seat of the vehicle and be
properly restrained.

 Do not allow a child to stand up or
kneel on the front passenger seat,
since the front passenger airbag
could inflate with considerable
speed and force. Otherwise, the
child may be killed or seriously injured.

## p.63  Do not modify or remove any wiring. Do not modify, remove, strike

 Do not modify or remove any wiring. Do not modify, remove, strike
or open any components such as
the steering wheel pad, steering
wheel, column cover, dashboard
near the front passenger airbag,
front passenger airbag or airbag
sensor assembly. Doing so may prevent the front airbag system from
activating correctly, cause sudden
activation of the system or disable
the system, resulting in death or
serious injury.

 Do not put anything or any part of
your body on or in front of the
dashboard or steering wheel pad
that houses the front airbag system. They might restrict inflation or
cause death or serious injury as
they are projected rearward by the
force of deploying airbags. Likewise, the driver and front passenger
should not hold objects in their
arms or on their knees.

Failure to follow these instructions
can result in death or serious injury.
Consult your Toyota dealer about any
repair and modification.

NOTICE
Do not perform any of the following
changes without
consulting your
Toyota dealer. Such changes can
interfere with proper operation of the
SRS front airbag system in some
cases.
z Installation of electronic devices
such as a mobile two-way radio,
cassette tape player or compact
disc player
z Modification of the suspension system
z Modification of the front end structure
z Attachment of a grille guard (bull
bar, kangaroo bar, etc.), snowplow,
winches or any other equipment to
the front end
z Repairs made on or near the front
fenders, front end structure, console, steering column, steering
wheel or dashboard near the front
passenger airbag

## p.64 If any of the following conditions occurs,

If any of the following conditions occurs,
this indicates a malfunction of the airbags
or seat belt pretensioners. Contact your
Toyota dealer as soon as possible.

 The light does not come on when the
ignition key is turned to the "ON" position or remains on for more than 6
seconds or flashes.

 The light comes on or starts flashing
while driving.

The indicator comes on when the ignition key is turned to the "ON" position.
It goes off after about 6 seconds. This
means the SRS front airbags are operating properly.

In the following cases, contact your Toyota
dealer as soon as possible:
 The SRS front airbags have been inflated.

This warning light system monitors the
airbag sensor assembly, front airbag sensors, side and curtain shield airbag sensor
assemblies, curtain shield airbag sensor
assemblies, driver's seat position sensor,
driver's seat belt buckle switch, seat belt
pretensioner assemblies, inflators, warning
light, roll sensing of curtain shield airbags
off indicator light, interconnecting wiring
and power sources. (For details, see "Service reminder indicators and warning buzzers" on page 122.)

illustration) was involved in an accident
that was not severe enough to cause
the SRS front airbags to inflate.

 The front of the vehicle (shaded in the

 The pad section of the steering wheel
or dashboard (shaded in the illustration) is scratched, cracked, or otherwise damaged.

NOTICE
Do not disconnect the battery cables
before contacting your Toyota dealer.

## p.65 SRS side airbags and curtain

SRS side airbags and curtain
shield airbags with roll sensing function
The SRS (Supplemental Restraint System) side airbags and curtain shield airbags are designed to provide further
protection for the driver, front passenger and second seat passengers in
addition to the primary safety protection provided by the seat belts.

In response to a severe side impact, the
SRS side airbags and curtain shield airbags on impacted side work with the seat
belts to help reduce injury by inflating.
The SRS side airbags help reduce injuries
mainly to the driver's or front passenger's
chest, and the SRS curtain shield airbags
help reduce injuries mainly to the driver's,
front passenger's or second seat passenger's head and can help the driver, front
passenger and second seat passengers to
retain inside the vehicle.
Roll sensing function:
In response to a vehicle rollover, the SRS
curtain shield airbags on both sides work
with the seat belts to help reduce injury
by inflating. The SRS curtain shield airbags help reduce injuries mainly to the
driver's, front passenger's or second seat
passenger's head and can help the driver,
front passenger and second seat passengers to retain inside the vehicle.

CAUTION

 The SRS side airbag and curtain
shield airbag system is designed
only as a supplement to the primary protection of the driver, front
passenger and second seat passenger seat belt systems. To ensure
maximum protection in an accident,
the driver and all passengers in the
vehicle must wear their seat belts
properly. Wearing a seat belt properly during an accident reduces the
chances of death or serious injury
or being thrown out of the vehicle.
For instructions and precautions
concerning the seat belt system,
see "Seat belts" on page 48.

The SRS side and curtain shield airbags
on the passenger side are activated even
with no passenger in the front seat.
Always wear your seat belt properly.

## p.66 When you push the roll sensing of curtain

When you push the roll sensing of curtain
shield airbags off switch for a few seconds with the ignition switch on, the roll
sensing of curtain shield airbags off indicator light comes on and the roll sensing
function is turned off. When you push the
switch again, the indicator light goes off
and the roll sensing function is turned on.

 Do not allow anyone to lean his/her
head or any part of his/her body
against the door or the area of the
seat, front pillar, rear pillar or roof
side rail from which the SRS side
airbag and curtain shield airbag
deploy even if he/she is a child
seated in the child restraint system.
It is dangerous if the SRS side airbag and curtain shield airbag inflate, and the impact of the deploying airbags could cause death or
serious injury to the occupant.

 Improperly seated and/or restrained
infants and children can be killed
or seriously injured by the deploying airbags. An infant or child who
is too small to use a seat belt
should be properly secured using a
child
restraint
system.
Toyota
strongly recommends that all infants and children be placed in the
rear seats of the vehicle and properly restrained. The rear seats are
the safest for infants and children.
For instructions concerning the
installation of a child restraint system, see "Child restraint" on page
76.

In a severe side impact, the curtain shield
airbag on impacted side will inflate even
if the roll sensing function is turned off.

Roll sensing of curtain shield airbags
off switch
The roll sensing of curtain shield airbags off switch can turn off the curtain
shield airbags in a vehicle rollover. This
switch should only be used in a situation where the inflation is not desired
(such as extreme-off road driving).

If the ignition switch is turned to "ACC" or
"LOCK" with the roll sensing function off
and then the ignition switch is turned back
to "ON", the roll sensing function will be
back on automatically.

## p.67 CAUTION

CAUTION

 Make sure the roll sensing of curtain shield airbags
light is not on.

off

indicator
Collision from the rear

 When the roll sensing of curtain
shield airbags off switch is turned
on (and the roll sensing of curtain
shield airbags off indicator light is
on), the curtain shield airbags will
not inflate in a vehicle rollover and
turning off the curtain shield airbags can reduce the occupant
protection which your vehicle safety
systems can provide to you in certain accidents and increase the likelihood of death or serious injuries.

Collision from the front
Vehicle rollover

The SRS side airbags may not inflate if
the vehicle is subjected to a collision
from the side at certain angles, or a
collision to the side of the vehicle body
other than the passenger compartment
as shown in the illustration.

The SRS side airbags are not generally
designed to inflate if the vehicle is involved in a front or rear collision, if it
rolls over, or if it is involved in a low-
speed side collision.

The SRS side airbags are designed to
inflate when the passenger compartment
area suffers a severe impact from the
side.
Always wear your seat belts properly.

## p.68 Collision from

Collision from
the front

The angle of
vehicle tip-up
is marginal

The curtain shield airbags may not inflate if the vehicle is subjected to a
collision from the side at certain
angles, or a collision to the side of the
vehicle body other than the passenger
compartment as shown in the illustration.
The curtain shield airbags are designed to
inflate when the passenger compartment
area suffers a severe impact from the
side or vehicle rollover.
Always wear your seat belts properly.

Skidding vehicle
hitting a curb
stone

The curtain shield airbags may inflate
if the angle of vehicle tip-up is marginal or if the skidding vehicle's tires hit
a curb stone laterally as shown in the
illustration.

Collision from
the rear

Pitch end over end

The curtain shield airbags are not generally designed to inflate if the vehicle
is involved in a front or rear collision,
if it pitches end over end or if it is
involved in a low-speed side collision.

## p.69 The SRS side airbag and curtain shield

The SRS side airbag and curtain shield
airbag system is controlled by the airbag
sensor assembly. The airbag sensor assembly consists of a safing sensor and
airbag sensor.
Hitting a curb, edge of
pavement or hard surface

Falling into or jumping over a deep hole
Landing hard or vehicle falling

The SRS side airbags and curtain shield
airbags may deploy if a severe impact
occurs to the underside of your vehicle.
Some examples are shown in the illustration.

The SRS side airbag and curtain shield
airbag system consists mainly of the following components, and their locations are
shown in the illustration.
1. SRS warning light
2. Curtain shield airbag modules
(airbag and inflator)

In a severe side impact, the side and
curtain shield airbag sensor and/or the
curtain shield airbag sensor trigger(s) the
side airbag inflators and/or the curtain
shield airbag inflators. At this time, a
chemical reaction in the inflators quickly
fills the airbags with non-toxic gas to help
restrain the lateral motion of the occupants.
In a vehicle rollover, the airbag sensor
assembly triggers the curtain shield airbag
inflator. At this time, a chemical reaction
in the inflators quickly fills the airbags
with non-toxic gas to help restrain the
lateral motion of front and second seat
occupants.

3. Side airbag modules
(airbag and inflator)
4. Curtain shield airbag sensors
5. Side and curtain shield airbag sensors
6. Airbag sensor assembly

## p.70 When the airbags inflate, they produce a

When the airbags inflate, they produce a
fairly loud noise and release some smoke
and residue along with non-toxic gas. This
does not indicate a fire. This smoke may
remain inside the vehicle for some time,
and may cause some minor irritation to
the eyes, skin or breathing. Be sure to
wash off any residue as soon as possible
to prevent any potential skin irritation with
soap and water.
If you can safely exit from the vehicle,
you should do so immediately.
Deployment of the airbags happens in a
fraction of a second, so the airbags must
inflate with considerable force. While the
system is designed to reduce serious injuries, it may also cause minor burns or
abrasions and swelling.
Front seats as well as parts of the front
and rear pillar, front, center and rear garnish and roof interior may be hot for several minutes, but the airbags themselves
will not be hot. The airbags are designed
to inflate only once.

CAUTION
SRS side airbags and curtain shield
airbags
inflate with considerable
force. To reduce the possibility of
death or serious injury when they inflate, the driver, front passenger and
second seat passengers must:
 Wear their seat belts properly.
 Remain properly seated with their
backs upright and against the seats
at all times.

 Do not allow anyone to lean against
the door when the vehicle is in use,
since the side airbag and curtain
shield airbag could inflate with considerable speed and force. Otherwise, he/she may be killed or seriously injured. Special care should
be taken especially when you have
a small child in the vehicle.

## p.71  Sit up straight and well back in the

 Sit up straight and well back in the
seat, distributing your weight evenly
in the seat. Do not apply excessive
weight to the outer side of the
seats with a side airbag and to the
front and rear pillar, front, center
and rear garnish and roof interior
with the curtain shield airbag.
Improper sitting and wearing of the
seat belts may not retain you inside
the vehicle.

 Make sure the roll sensing of cur-

 Do not allow anyone to get his/her

tain shield airbags off indicator is
not on. The curtain shield airbags
will not inflate in a vehicle rollover
if this indicator light is on and you
may be killed or seriously injured.

head close to the area where the
side airbag and curtain shield airbag inflate, since these airbags
could inflate with considerable
speed and force. Otherwise, he/she
may be killed or serious injured.
Special care should be taken especially when you have a small child
in the vehicle.

## p.72  Do not allow anyone to kneel on

 Do not allow anyone to kneel on
the passenger seat, facing the passenger's side door, since the side
airbag and curtain shield airbag
could inflate with considerable
speed and force. Otherwise, he/she
may be killed or seriously injured.
Special care should be taken especially when you have a small child
in the vehicle.

 Do not allow anyone to get his/her

 Do not attach a cup holder or any

head or hands out of windows,
since the curtain shield airbags
could inflate with considerable
speed and force. Otherwise, he/she
may be killed or seriously injured.
Special care should be taken especially when you have a small child
in the vehicle.

other device or object on or around
the door. When the side airbag inflates, the cup holder or any other
device or object will be thrown with
great force, or the side airbags may
not activate correctly, resulting in
death or serious injury. Likewise,
the driver and front passenger
should not hold objects in their
arms or on their knees.

## p.73 13c800b
 Do not hook a hanger, heavy or

 Do not disassemble or repair the

sharp pointed objects on the coat
hook. If the curtain shield airbags
inflate, those items will be thrown
away with great force or the curtain
shield airbags may not activate correctly, resulting in death or serious
injury. When you hang clothes,
hang them on the coat hook directly.

front and rear pillars and roof side
rails containing the curtain shield
airbags. Such changes may disable
the system or cause the curtain
shield airbags to inflate accidentally, resulting in death or serious injury.

 Do not use seat accessories which
 Do not attach a microphone or any
other device or object around the
area where the curtain shield airbag
activates such as on the windshield
glass, side door glass, front, center
and roof side garnish, roof interior
or assist grips. When the curtain
shield airbag inflates, the microphone or other device or object will
be thrown away with great force or
the curtain shield airbag may not
activate correctly, resulting in death
or serious injury.

cover the parts where the side airbags inflate. Such accessories may
prevent the side airbags from activating correctly, causing death or
serious injury.

 Do not modify or replace the seats
or upholstery of the seats with side
airbags. Such changes may prevent
the side airbag system from activating correctly, disable the system or
cause the side airbags to inflate accidentally, resulting in death or serious injury.

 Do not modify or change the suspension system. Such changes may
cause the curtain shield airbags to
inflate accidentally, resulting in
death or serious injury.

 Do not use tires or wheels other
than the manufacturer's recommended size. Such a use may cause
the curtain shield airbags to inflate
accidentally, resulting in death or
serious injury. For details, see
"Checking and replacing tires" on
page 304.

## p.74  Do not place luggage heavier than

 Do not place luggage heavier than
specified on the roof luggage carrier. Such luggage may cause the
curtain shield airbags to inflate accidentally, resulting in death or serious injury. For details, see "Roof
luggage carrier" on page 202.
Failure to follow these instructions
can result in death or serious injury.
Consult your Toyota dealer about any
repair and modification.

NOTICE
Do not perform any of the following
changes without
consulting your
Toyota dealer. Such changes can interfere with proper operation of the
SRS side airbag and curtain shield
airbag system in some cases.
z Installation of electronic devices
such as a mobile two-way radio,
cassette tape player or compact
disc player.
z Modification of the side structure of
the passenger compartment.
z Repairs made on or near the console or front seat.

The indicator comes on when the ignition key is turned to the "ON" position.
It goes off after about 6 seconds. This
means the SRS side airbags and curtain
shield airbags are operating properly.
This warning light system monitors the
airbag sensor assembly, front airbag sensors, side and curtain shield airbag sensor
assemblies, curtain shield airbag sensor
assemblies, driver's seat position sensor,
driver's seat belt buckle switch, seat belt
pretensioner assemblies, inflators, warning
light, roll sensing of curtain shield airbags
off indicator light, interconnecting wiring
and power sources. (For details, see "Service reminder indicators and warning buzzers" on page 122.)

## p.75 If any of the following conditions occurs,

If any of the following conditions occurs,
this indicates a malfunction of the airbags
or seat belt pretensioners. Contact your
Toyota dealer as soon as possible.

In the following cases, contact your Toyota
dealer as soon as possible:

 The light does not come on when the

 The portion of the doors (shaded in the

ignition key is turned to the "ON" position or remains on for more than 6
seconds or flashes.

 The light comes on or starts flashing
while driving.

 Any of the SRS side airbags and curtain shield airbags have been inflated.

illustration) was involved in an accident
that was not severe enough to cause
the SRS side airbags and curtain
shield airbags to inflate.

 The surface of the seats with the side
airbag (shaded in the illustration) is
scratched, cracked, or otherwise damaged.

 The portion of the front, center and
rear garnish, and roof interior containing the curtain shield airbags inside
(shaded in the illustration) is scratched,
cracked, or otherwise damaged.

NOTICE
Do not disconnect the battery cables
before contacting your Toyota dealer.

## p.76 Child restraint-

Child restraint-
-Child restraint precautions
Toyota strongly urges the use of appropriate child restraint systems for
children.
The laws of all 50 states in the U.S.A.
now require the use of a child restraint
system.
Your vehicle conforms to SAEJ1819.
If a child is too large for a child restraint
system, the child should sit in the rear
seat and must be restrained using the
vehicle's seat belt. See "Seat belts" on
page 48 for details.

CAUTION

 For effective protection in automobile accidents and sudden stops, a
child must be properly restrained,
using a seat belt or child restraint
system depending on age and size
of the child. Holding a child in your
arms is not a substitute for a child
restraint system. In an accident, the
child can be crushed against the
windshield, or between you and the
vehicle's interior.

 Toyota strongly urges use of a

 On vehicle with side airbags and

proper child restraint system which
conforms to the size of the child,
installed on the rear seat. According to accident statistics, the child
is safer when properly restrained in
the rear seat than in the front seat.

curtain shield airbags, do not allow
the child to lean his/her head or
any part of his/her body against the
door or the area of the seat, front
or rear pillar, front, center or rear
garnish or roof interior from which
the side airbags or curtain shield
airbags deploy even if the child is
seated in the child restraint system.
It is dangerous if the side airbag
and curtain shield airbag inflate,
and the impact could cause death
or serious injury to the child.

 Never install a rear-facing child restraint system on the front passenger seat. In the event of an accident, the force of the rapid inflation
of the front passenger airbag can
cause death or serious injury to the
child if the rear-facing child restraint system is installed on the
front passenger seat.

 A forward-facing child restraint system should be allowed to be
installed on the front passenger
seat only when it is unavoidable.
Always move the seat as far back
as possible, because the front passenger airbag could inflate with
considerable
speed
and
force.
Otherwise, the child may be killed
or seriously injured.

 Do not use the seat belt extender
when installing a child restraint
system on the front or rear passenger seat. If installing a child restraint system with the seat belt
extender connected to the seat belt,
the seat belt will not securely hold
the child restraint system, which
could cause death or serious injury
to the child or other passengers in
the event of collision.

## p.77 -Child restraint system

-Child restraint system
 Make sure you have complied with
all installation instructions provided
by the child restraint manufacturer
and that the system is properly secured. It is not secured properly, it
may cause death or serious injury
to the child in the event of a sudden stop or accident.

A child restraint system for a small
child or baby must itself be properly
restrained on the seat with the lap portion of the lap/shoulder belt. You must
carefully consult the manufacturer's
instructions which accompany the child
restraint system.
To provide proper restraint, use a child
restraint system following the manufacturer's instructions about the appropriate age
and size of the child for the child restraint
system.
Install the child restraint system correctly
following the instructions provided by its
manufacturer. General directions are also
provided under the following illustrations.
The child restraint system should be
installed on the rear seat. According to
accident statistics, the child is safer when
properly restrained in the rear seat than
in the front seat.

-Types of child restraint
system
Child restraint systems are classified into
the following 3 types depending on the
child's age and size.
(A) Infant seat
(B) Convertible seat
(C) Booster seat
Install the child restraint system following
the instructions provided by its manufacturer.
Your vehicle has anchor brackets for securing the top strap of a child restraint
system. For instructions about how to use
the anchor bracket, see "Using a top
strap" on page 92.
The child restraint lower anchorages approved for your vehicle may also be used.
See "Installation with child restraint lower
anchorages" on page 94.

When not using the child restraint system,
keep it secured with the seat belt or place
it somewhere other than the passenger
compartment. This will prevent it from injuring passengers in the event of a sudden stop or accident.

## p.78 -Installation with 2-point

-Installation with 2-point
type seat belt

(A) Infant seat

(C) Booster seat

(A) INFANT SEAT INSTALLATION
An infant seat must be used in rear-
facing position only.

(B) Convertible seat

## p.79 CAUTION

CAUTION

 After inserting the tab, make sure
the tab and buckle are locked and
that the lap portion of the belt is
not twisted.

 Do not insert coins, clips, etc. in
the buckle as this may prevent your
child from properly latching the tab
and buckle.

 If the seat belt does not function

CAUTION
Do not install a child restraint system
on the third seat if it interferes with
the lock mechanism of the second
seats. Otherwise, the child or second
seat occupant(s) may be killed or seriously injured in case of sudden
braking or a collision.

1. Run the center lap belt through or
around the infant seat following the
instructions provided by its manufacturer and insert the tab into the buckle
taking care not to twist the lap belt.

normally, it cannot protect your
child from death or serious injury.
Contact
your
Toyota
dealer
immediately. Do not install the child
restraint system on the seat until
the seat belt is fixed.

## p.80 2. While pressing the infant seat firmly

2. While pressing the infant seat firmly
against the seat cushion and seatback,
tighten the lap belt by pulling its free
end to hold the infant seat securely.

CAUTION
Push and pull the child restraint system in different directions to be sure
it is secure. Follow all the installation
instruction provided by its manufacturer.

3. To remove the infant seat, press the
buckle release button.

## p.81 (B) CONVERTIBLE SEAT INSTALLATION

(B) CONVERTIBLE SEAT INSTALLATION
A convertible seat must be used in forward-facing or rear-facing position depending on the age and size of the
child. When installing, follow the
manufacturer's instruction about the applicable age and size of the child as
well as directions for installing the
child restraint system.

CAUTION
Do not install a child restraint system
on the third seat if it interferes with
the lock mechanism of the second
seats. Otherwise, the child or second
seat occupant(s) may be killed or seriously injured in case of sudden
braking or a collision.

1. Run the center lap belt through or
around the convertible seat following
the
instructions
provided
by
its
manufacturer and insert the tab into
the buckle taking care not to twist the
lap belt.

## p.82 CAUTION

CAUTION

 After inserting the tab, make sure
the tab and buckle are locked and
that the lap portion of the belt is
not twisted.

 Do not insert coins, clips, etc. in
the buckle as this may prevent your
child from properly latching the tab
and buckle.

 If the seat belt does not function
normally, it cannot protect your
child from death or serious injury.
Contact
your
Toyota
dealer
immediately. Do not install the child
restraint seat on the seat until the
seat belt is fixed.

2. While pressing the convertible seat
firmly against the seat cushion and
seatback, tighten the lap belt by pulling
its free end to hold the convertible seat
securely.

CAUTION
Push and pull the child restraint system in different directions to be sure
it is secure. Follow all the installation
instructions provided by its manufacturer.

## p.83 -Installation with 3-point

-Installation with 3-point
type seat belt
3. To remove the convertible seat, press
the buckle release button.

(A) INFANT SEAT INSTALLATION
An infant seat must be used in rear-
facing position only.
CAUTION

 Never install a rear-facing child restraint system on the front passenger seat. In the event of an accidents, the force of the rapid inflation of the front passenger airbag
can cause death or serious injury
to the child if the rear-facing child
restraint system is installed on the
front passenger seat.

## p.84 CAUTION

CAUTION

 After inserting the tab, make sure
the tab and buckle are locked and
that the lap and shoulder portions
of the belt are not twisted.

 Do not insert coins, clips, etc. in
the buckle as this may prevent your
child from properly latching the tab
and buckle.

 If the seat belt does not function
 Do not install a child restraint system on the third seat if it interferes
with the lock mechanism of the second seats. Otherwise, the child or
second seat occupant(s) may be
killed or seriously injured in case
of sudden braking or a collision.

 If the driver's seat position does
not allow sufficient space for safe
installation, install the child restraint system on the second right
seat.

1. Run the lap and shoulder belt through
or around the infant seat following the
instructions provided by its manufacturer and insert the tab into the buckle
taking care not to twist the belt. Keep
the lap portion of the belt tight.

normally, it cannot protect your
child from death or serious injury.
Contact
your
Toyota
dealer
immediately. Do not install the child
restraint system on the seat until
the seat belt is fixed.

## p.85 2. Fully extend the shoulder belt to put it

2. Fully extend the shoulder belt to put it
in the lock mode. When the belt is
then retracted even slightly, it cannot
be extended.
To hold the infant seat securely, make
sure the belt is in the lock mode before
letting the belt retract.

3. While pressing the infant seat firmly
against the seat cushion and seatback,
let the shoulder belt retract as far as
it will go to hold the infant seat securely.

CAUTION
Push and pull the child restraint system in different directions to be sure
it is secure. Follow all the installation
instructions provided by its manufacturer.

## p.86 13c566
4. To remove the infant seat, press the
buckle release button and allow the
belt to retract completely. The belt will
move freely again and be ready to
work for an adult or older child passenger.

(B) CONVERTIBLE SEAT INSTALLATION
A convertible seat must be used in forward-facing or rear-facing position depending on the age and size of the
child. When installing, follow the
manufacturer's instructions about the
appropriate age and size of the child as
well as directions for installing the
child restraint system.
CAUTION

 Never install a rear-facing child restraint system on the front passenger seat. In the event of an accident, the force of the rapid inflation
of the front passenger airbag can
cause death or serious injury to the
child if the rear-facing child restraint system is installed on the
front passenger seat.

## p.87  On vehicle with side airbags and

 On vehicle with side airbags and
Move seat fully back

 A forward-facing child restraint system should be allowed to be
installed on the front passenger
seat only when it is unavoidable.
Always move the seat as far back
as possible, because the front passenger airbag could inflate with
considerable
speed
and
force.
Otherwise, the child may be killed
or seriously injured.

curtain shield airbags, do not allow
the child to lean his/her head or
any part of his/her body against the
door or the area of the seat, front
or rear pillar, front, center or rear
garnish or roof interior from which
the side airbags or curtain shield
airbags deploy even if the child is
seated in a child restraint system.
It is dangerous if the side airbag
and curtain shield airbag inflate,
and the impact could cause death
or serious injury to the child.
 Do not install a child restraint system on the third seat if it interferes
with the lock mechanism of the second seats. Otherwise, the child or
second seat occupant(s) may be
killed or serious injured in case of
sudden braking or a collision.

 If the driver's seat position does
not allow sufficient space for safe
installation, install the child restraint system on the second right
seat.

## p.88 CAUTION

CAUTION

 After inserting the tab, make sure
the tab and buckle are locked and
that the lap and shoulder portions
of the belt are not twisted.

 Do not insert coins, clips, etc. in
the buckle as this may prevent your
child from properly latching the tab
and buckle.

 If the seat belt does not function
1. Run the lap and shoulder belt through
or around the convertible seat following
the
instructions
provided
by
its
manufacturer and insert the tab into
the buckle taking care not to twist the
belt. Keep the lap portion of the belt
tight.

normally, it cannot protect your
child from death or serious injury.
Contact
your
Toyota
dealer
immediately. Do not install the child
restraint seat on the seat until the
seat belt is fixed.

2. Fully extend the shoulder belt to put it
in the lock mode. When the belt is
then retracted even slightly, it cannot
be extended.
To hold the convertible seat securely,
make sure the belt is in the lock mode
before letting the belt retract.

## p.89 3. While pressing the convertible seat

3. While pressing the convertible seat
firmly against the seat cushion and
seatback, let the shoulder belt retract
as far as it will go to hold the convertible seat securely.

CAUTION
Push and pull the child restraint system in different directions to be sure
it is secure. Follow all the installation
instructions provided by its manufacturer.

4. To remove the convertible seat, press
the buckle release button and allow the
belt to retract completely. The belt will
move freely again and be ready to
work for an adult or older child passenger.

## p.90  On vehicle with side airbags and

 On vehicle with side airbags and
Move seat fully back

(C) BOOSTER SEAT INSTALLATION
A booster seat must be used in forward-facing position only.

CAUTION

 A forward-facing child restraint system should be allowed to be
installed on the front passenger
seat only when it is unavoidable.
Always move the seat as far back
as possible, because the front passenger airbag could inflate with
considerable
speed
and
force.
Otherwise, the child may be killed
or seriously injured.

curtain shield airbags, do not allow
the child to lean his/her head or
any part of his/her body against the
door or the area of the seat, front
or rear pillar, front, center or rear
garnish or roof interior from which
the side airbags or curtain shield
airbags deploy even if the child is
seated in a child restraint system.
It is dangerous if the side airbag
and curtain shield airbag inflate,
and the impact could cause death
or serious injury to the child.

## p.91 CAUTION

CAUTION

 Always make sure the shoulder belt
is positioned across the center of
child's shoulder. The belt should be
kept away from child's neck, but
not falling off child's shoulder.
Otherwise, the child may be killed
or seriously injured in case of sudden braking or a collision.

 If the seat belt does not function
normally, it cannot protect your
child from death or serious injury.
Contact
your
Toyota
dealer
immediately. Do not install the child
restraint system on the seat until
the seat belt is fixed.

 Both high-positioned lap belts and
1. Sit the child on a booster seat. Run
the lap and shoulder belt through or
around the booster seat and across the
child following the instructions provided
by its manufacturer and insert the tab
into the buckle taking care not to twist
the belt.
Make sure the shoulder belt is correctly
across the child's shoulder and that the
lap belt is positioned as low as possible
on the child's hips. See "Seat belts" on
page 48 for details.

loose-fitting belts could cause
death or serious injuries due to
sliding under the lap belt during a
collision or other unintended event.
Keep the lap belt positioned as low
on child's hips as possible.

 For child's safety, do not place the
shoulder belt under child's arm.

 After inserting the tab, make sure
the tab and buckle are locked and
that the lap and shoulder portions
of the belt are not twisted.

 Do not insert coins, clips, etc. in
the buckle as this may prevent your
child from properly latching the tab
and buckle.

## p.92 -Using a top strap

-Using a top strap
Symbol

Anchor
brackets

2. To remove the child restraint system,
press the buckle release button and
allow the belt to retract.

Follow the procedure below for a child
restraint system that requires the use
of a top strap.

Use the anchor bracket located behind the
second seat on the floor to attach the top
strap.
Anchor brackets are installed for each
second seating position.
This symbol indicates the locations of the
anchor bracket.

## p.93 TO USE THE ANCHOR BRACKET:

TO USE THE ANCHOR BRACKET:
1. Remove the head restraint.

2. Fix the child restraint system with
the seat belt.
3. Take off the cover, latch the hook
onto the anchor bracket and tighten
the top strap.
For instructions to install the child restraint system, see "Child restraint-" on
page 76.

4. Replace the head restraint.

CAUTION

 Make sure the top strap is securely
latched, and check that the child restraint system is secure by pushing
and pulling it in different directions.
 Follow all installation instructions
provided by its manufacturer.

## p.94 -Installation with child

-Installation with child
restraint lower anchorages

The lower anchorages for the child restraint system interfaced with the
FMVSS225 specification are installed in
the second seat.
The anchorages are installed in the clearance between the seat cushion and seatback of left and center second seats.
Child restraint system interfaced with the
FMVSS213 specification can be fixed with
these anchorages. In this case, it is not
necessary to fix the child restraint system
with a seat belt on the vehicle.
Most upright
position

CHILD RESTRAINT SYSTEM INSTALLATION
1. Fold down the seatback and back to
the most upright position until it
locks into place.
2. Take off the cover between the seat
cushion and seatback and confirm
the position of the lower anchorages
below the symbol in the seat back.

## p.95 Type A-

Type A-
3. Latch the hooks of lower straps onto
the anchorages and tighten the lower
straps.
Type B-
3. Latch the buckles onto the anchorages
If your child restraint system has a top
strap, it should be anchored. (For the
installation of the top strap, see "-Using
a top strap" on page 92.)
For installation details, refer to the instruction manual equipped with each product.

Type A

CAUTION

 When using the lower anchorages
for the child restraint system, be
sure that there are no irregular objects around the anchorages or that
the seat belt is not caught.

 Push and pull the child restraint
system in different directions to be
sure it is secure. Follow all the
installation instructions provided by
its manufacturer.

 Do not install a child restraint system on the rear seat if it interferes
with the lock mechanism of the
front seats. Otherwise, the child or
front seat occupant(s) may be killed
or seriously injured in case of sudden braking or a collision.
Type B

## p.96 

# Section 1-4: Steering wheel and Mirrors

## p.97 SECTION

SECTION

1- 4

OPERATION OF INSTRUMENTS AND
CONTROLS
Steering wheel and Mirrors
Power tilt and telescopic steering wheel . . . . . . . . . . . . . . . . . . . . . . . . 98
Outside rear view mirrors . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 99
Anti-glare inside rear view mirror . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 100
Sun visors . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 105

## p.98 Power tilt and telescopic steering wheel

Power tilt and telescopic steering wheel
CAUTION
Do not adjust the steering column
while the vehicle is moving. Doing so
may cause the driver to mishandle
the vehicle and an accident may occur resulting in death or serious injuries.

ADJUSTMENT
TILT

OF

STEERING

WHEEL

ADJUSTMENT OF TELESCOPIC STEERING COLUMN

To adjust the tilt of the steering wheel,
push the control switch upward or
downward to set it to the desired position.

To adjust the steering column length,
push the control switch forward or
backward to set the steering wheel to
the desired position.

CAUTION
Do not adjust the steering wheel
while the vehicle is moving. Doing so
may cause the driver to mishandle
the vehicle and an accident may occur resulting in death or serious injuries.

When the ignition key is removed, the
steering column moves forward away from
the driver and also tilts up for easy exit
and entry.
When the key is inserted into the ignition
switch, the steering column returns to the
previously set position.
This feature can be set inoperative. Ask
your Toyota dealer.

## p.99 -Power rear view mirror

-Power rear view mirror
control

Outside rear view mirrors-
CAUTION

 Do not adjust the mirror while the
vehicle is moving. Doing so may
cause the driver to mishandle the
vehicle and an accident may occur
resulting in death or serious injuries.

 Since the mirror surfaces can get
hot, do not touch them when the
mirror heater switch is on.

Adjust the mirror so that you can just
see the side of your vehicle in the mirror.
Be careful when judging the size or distance of any object seen in the outside
rear view mirror on the passenger's side
because it is a convex mirror. Any object
seen in a convex mirror will look smaller
and farther away than when seen in a flat
mirror.
When you push the outside rear view mirror heater switch, the heater panels in the
outside rear view mirrors will quickly clear
the mirror surface. (See "Outside rear
view mirror heaters" on page 115.)

To adjust a mirror, use the switches.
1. Master switch-To select the mirror to
be adjusted
Place the switch at "L" (left) or "R"
(right).
2. Control switch-To move the mirror
Push the switch in the desired direction.
Mirrors can be adjusted when the key is
in the "ACC" or "ON" position.

## p.100 -Folding rear view mirrors

-Folding rear view mirrors

Anti-glare
mirror-

inside

rear

view

NOTICE
If ice should jam the mirror, do not
operate the control or scrape the mirror face. Use a spray de-icer to free
the mirror.

The rear view mirrors can be folded
backward for parking in compact areas.
To fold the rear view mirror, push backward.

CAUTION
Do not drive with the mirrors folded
backward. Both the driver and passenger side rear view mirrors must
be extended and properly adjusted
before driving.

Adjust the mirror so that you can just
see the rear of your vehicle in the mirror.
Pushing the switch changes the mode
between "AUTO" and "DAY".
The indicator comes on when the "AUTO"
mode is selected.
"DAY" mode: The mirror surface is normal.
"AUTO" mode: If the mirror detects
light from the headlights of the vehicle
behind you, the mirror surface darkens
slightly to reduce the reflected light.

## p.101 -Compass

-Compass
When the ignition key is inserted and
turned on, the inside rear view mirror always turns on in the "AUTO" mode.
When the outside air temperature is low,
it may take a little longer for the mirror
to darken in response to the detection of
headlights.
CAUTION
Do not adjust the mirror while the
vehicle is moving. Doing so may
cause the driver to mishandle the vehicle and an accident may occur resulting in death or serious injuries.

To ensure correct functioning of anti-glare
mirror sensors located on both sides of
the mirror, do not touch or cover the sensors with your finger or a piece of cloth,
etc.

The compass indicates the direction in
which the vehicle is heading. The illustration shown above indicates the vehicle is
heading north.
Displays

Directions

N
NE
E
SE
S
SW
W
NW

North
Northeast
East
Southeast
South
Southwest
West
Northwest

## p.102 Pushing the "AUTO" button for longer

Pushing the "AUTO" button for longer
3 seconds turns on or off the compass
display.
The compass may not show the correct
direction in the following conditions:

 The vehicle is stopped immediately af-

ter turning. The compass does not adjust while the vehicle is stopped.

 The ignition switch is turned off immediately after turning.

 The vehicle is on an inclined surface.
 The vehicle is in a place where the
earth's magnetic field is subject to interference by artificial magnetic fields
(underground parking, under a steel
tower, between buildings, roof parking,
near a crossing, near a large vehicle,
etc.).

 The vehicle is magnetized. (There is a
magnet or a metal object on or near
the inside rear view mirror.)

 The battery has been disconnected.
 Any door is open.
If the deviation is small, the compass
works to calibrate the direction automatically while the vehicle is in motion.
For obtaining additional precision or for
complete calibrating, see "Calibrating the
compass" below.

NOTICE
Do not put magnets or a metal object
near the inside rear view mirror. Doing this may cause malfunction of the
compass sensor.
CALIBRATING THE COMPASS
(deviation calibration)
The direction display on the compass
deviates from the true direction determined by the earth's magnetic field, The
amount of deviation varies according to
the geographic position of the vehicle.
To adjust for this deviation, stop the vehicle and push the button for longer than
about 6 seconds until the number (1-15)
appears on the display. Then push the
button again, referring to the following
map to select the number of the zone
where the vehicle is.

## p.103 If the direction is displayed several seconds after adjustment, the calibration 

If the direction is displayed several seconds after adjustment, the calibration is
finished.

CAUTION
Do not adjust the display while the
vehicle is moving. Be sure to adjust
the display only when the vehicle is
stopped.
Zone number

 Hawaii is included in zone 6.

## p.104  Do not perform circling calibration of

 Do not perform circling calibration of

the compass in a place where the
earth's magnetic field is subject to interference by artificial magnetic fields
(underground parking, under a steel
tower, between buildings, roof parking,
near a crossing, near a large vehicle,
etc.).

 During calibration, do not operate elec-

tric systems (moon roof, power windows, etc.) as they may interfere with
the calibration.

CALIBRATING THE COMPASS
(circling calibration)
"C" appears on the display in case the
circling calibration is required due to a
drastic change in the magnetic field. To
rectify this, follow the calibration procedure below.

Drive the vehicle slowly (at 8km/h (5mph)
or lower) in a circle until the direction is
displayed. If there is not enough space to
drive in a circle, drive around the block
until the direction is displayed.
After driving in 1 to 3 circles in the above
method, calibration is complete with the
direction shown on the display.
If calibration cannot be performed because
of the magnetized vehicle, etc., take your
vehicle to Toyota dealer.

CAUTION

 When doing the circling calibration,
be sure to secure a wide space,
and watch out for people and vehicles in the neighborhood. Do not
violate any local traffic rules while
performing circling calibration.

 Do not adjust the display while the
vehicle is moving. Be sure to adjust
the display only when the vehicle is
stopped.

## p.105 Sun visors-

Sun visors-

To block out glare, move the sun visor.
To block out glare from the front-Swing
down the main sun visor.
To block out glare from the side-Swing
down the main sun visor, remove it from
the hook and swing it to the lateral side.
You can adjust its position as shown.

-Vanity mirror

To block the glare from the front when the
main sun visor is swung down, swing
down the second sun visor.

CAUTION

To use the vanity mirror, swing down
the main sun visor and open the cover.
The vanity light comes on when you open
the cover.

Slide the main sun visor only when
it is swung down to the lateral side.
It can cover the anti-glare inside rear
view mirror and obstruct the rear
view.

## p.106 

# Section 1-5: Lights, Wipers and Defogger

## p.107 SECTION

SECTION

1- 5

OPERATION OF INSTRUMENTS AND
CONTROLS
Lights, Wipers and Defogger
Headlight and turn signals . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 108
Emergency flashers . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 110
Instrument panel light control . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 110
Front fog lights . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 111
Interior lights . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 111
Personal lights . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 112
Ignition switch light . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 113
Windshield wipers and washer . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 113
Rear window wiper and washer . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 114
Rear window defogger . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 115
Outside rear view mirror heaters . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 115

## p.108 Headlight and turn signals

Headlight and turn signals
Manually twist the knob to the position 2
to turn on the headlights if they are needed immediately when entering a dark tunnel, parking structure, etc.
NOTE: *The operating condition or sensitivity can be changed. Ask your Toyota
dealer for details.

HEADLIGHTS
To turn on the following lights: Twist
the headlight/turn signal lever knob.
Position 1-Parking, tail, license plate,
side marker and instrument panel lights
However, if the surroundings are bright
and if the instrument panel light control
dial is not turned fully on, the instrument
panel lights do not come on.
Position
above

2-Headlights

and

all

of

the

Position 3 ("AUTO")-Headlights and/or all
of the lights in position 1
They automatically turn on or off depending on the darkness of the surroundings.*

The automatic light control sensor is on
the top of the passenger's side instrument
panel.
Do not place anything on the instrument
panel, and/or do not affix anything on the
windshield to block this sensor.
When the headlights come on, the lights
automatically turn off about 30 seconds
after any of the doors is opened and
closed with the ignition key turned to the
"ACC" or "LOCK" position.* To turn them
on again, turn the ignition key to the "ON"
position, or turn the headlight switch off
and then twist the knob until the first or
second clickstop. If you are going to park
for over one week, make sure the headlight switch is off.

## p.109 When the headlight switch is on with all

When the headlight switch is on with all
the doors locked, pushing the "LOCK" button on the wireless remote control key
turns off the headlights.
NOTE: *The time before turning off the
lights can be changed. Ask your Toyota
dealer for details.

NOTICE
To prevent the battery from being discharged, do not leave the lights on
for a long period when the engine is
not running.
Daytime running light system
The headlights turn on at reduced intensity when the parking brake is released with
the engine started, even with the light
switch in the "OFF" position. They will not
go off until the ignition switch is turned
off.
To turn on the other exterior lights and
instrument panel lights, twist the knob to
the position 1.
Twist the knob to the position 2 to turn
the headlights to full intensity for driving
at night.

High-Low beams-For high beams, turn
the headlights on and push the lever away
from you (position 1). Pull the lever toward you (position 2) for low beams.

TURN SIGNALS

The headlight high beam indicator light
(blue light) on the instrument panel will
tell you that the high beams are on.

The key must be in the "ON" position.

Flashing the high beam headlights
(position 3)-Pull the lever all the way
back. The high beam headlights turn off
when you release the lever.
You can flash the high beam headlights
with the knob turned to "OFF".

To signal a turn, push the headlight/
turn signal lever up or down to position
1.
The lever automatically returns after you
make a turn, but you may have to return
it by hand after you change lanes.
To signal a lane change, move the lever
up or down to the pressure point (position
2) and hold it.
If the turn signal indicator lights (green
lights) on the instrument panel flash faster
than normal, a front or rear turn signal
bulb is burned out. See "Replacing light
bulbs" on page 315.

## p.110 Emergency flashers

Emergency flashers

Instrument panel light control
NOTICE
To prevent the battery from being discharged, do not leave the switch on
longer than necessary when the engine is not running.

To turn on the emergency flashers,
push the switch.
All the turn signal lights will flash. To turn
them off, push the switch once again.
Turn on the emergency flashers to warn
other drivers if your vehicle must be
stopped where it might be a traffic hazard.
Always pull your vehicle as far off the
road as possible.
The turn signal light switch will not work
when the emergency flashers are operating.

To adjust the brightness of the instrument panel lights, turn the dial.

## p.111 Front fog lights

Front fog lights

Interior lights
To turn on the interior light, slide the
switch.
The interior light switch has the following
positions:
"ON"-Keeps the light on all the time.
"OFF"-Turns the light off.
"DOOR"-
-Center: Turn the light on when any of
side doors and back door are opened.

To turn on the front fog lights, twist
the band of the headlight/turn signal
lever. They will come on only when the
headlights are on low beam.

Center

-Rear: Turn the light on when any of the
rear side doors and back door are
opened.

Rear

## p.112 Personal lights

Personal lights
ILLUMINATED ENTRY SYSTEM

INTERIOR LIGHTS CUT OFF OPERATION

Center-
With the switch in the "DOOR" position,
the light comes on when either side or
back door is opened. After all the doors
are closed, the light remains on for a
certain time and then goes out.*

When the ignition switch is "OFF" and any
interior lights in the vehicle stay lighting
on, the lights will cut off automatically
after 30 minutes.

However, in the following cases, the light
goes out immediately:

 All the doors are closed when the ignition key is in "ACC" or "ON" position.

 The ignition key is turned to "ACC",

"ON" or "START" when the light is still
on.

You can cancel the cut off operation by:

 Turning the key to the "ACC" position.
 Opening or closing any of side doors
and back door.

All the lights are cut off when any of the
doors are locked or unlocked by key or
wireless remote control key.
Front

 All the doors are locked when the light
is still on.

 One front door will be closed with the
lock knob pushed forward while the
other doors are locked.

NOTE: *The interior lights can be set not
to come on or the duration of lighting can
be changed. Ask your Toyota dealer for
details.

Center

## p.113 Ignition switch light

Ignition switch light

Windshield wipers and washer

For easy access to the ignition switch,
the ignition switch light comes on when
any door is opened.

To turn on the windshield wipers, move
the lever to the desired setting.

To turn on the personal light, push the
switch on 1 side. To turn the lights off,
push the switch on 2 side.
PERSONAL LIGHTS CUT OFF OPERATION
When the ignition switch is "OFF" and any
personal lights in the vehicle stay lighting
on, the lights will cut off automatically
after 30 minutes.
You can cancel the cut off operation by:

 Turning the key to the "ACC" position.
 Opening or closing any of side doors
and back door.

All the lights are cut off when any of the
doors are locked or unlocked by key or
wireless remote control key.

The light remains on for a certain time
after all the doors are closed.
It goes off immediately when the ignition
switch is turned to the "ACC" position or
when all the doors are locked.

The key must be in the "ON" position.
There are 3 settings:
1. "INT" position: Intermittent operation
2. "LO" position: Low speed operation
3. "HI" position: High speed operation
Twist the interval adjuster upward to increase the wiping time interval between
sweeps, and downward to decrease it.

## p.114 Rear window wiper and washer

Rear window wiper and washer
To squirt washer fluid, pull the lever
toward you.

NOTICE

If the windshield wipers are off, they will
operate a couple of times after the washer
squirts.

Do not operate the rear wiper if the
rear window is dry. It may scratch the
glass.

For instructions on adding washer fluid,
see "Adding washer fluid" on page 315.
In freezing weather, warm the windshield
with the defroster before using the washer.
This will help prevent the washer fluid
from freezing on your windshield, which
can block your vision.

NOTICE
Do not operate the wipers if the windshield is dry. It may scratch the
glass.
When waxing your vehicle, make sure that
the washer nozzles do not become
blocked. If a nozzle becomes blocked,
contact your Toyota dealer to have the
vehicle serviced.

NOTICE
If a nozzle becomes blocked, do not
try to clear it with a pin or other
object. The nozzle will be damaged.

To turn on the rear window wiper, twist
the lever knob upward.
The key must be in the "ON" position.
There are 2 settings:
1. "INT" position: Intermittent operation
2. "ON" position: Low speed operation
To squirt washer fluid on the rear window,
twist the knob upward or downward as far
as it will go (position 3 or 4). The knob
automatically returns from these positions
after you release it.
For instructions on adding washer fluid,
see "Adding washer fluid" on page 315.

## p.115 Rear window defogger

Rear window defogger

Outside rear view mirror heaters
Make sure you turn the defogger off when
the surfaces are clear. Leaving the defogger on for a long time could cause the
battery to discharge, especially during
stop-and-go driving. The defogger is not
designed for drying rain water or for melting snow.

NOTICE
z When cleaning the inside of the
rear window, be careful not to
scratch or damage the heater wires
or connectors.
To defog or defrost the rear window,
push the switch.
The key must be in the "ON" position.

z To prevent the battery from being
discharged, turn the switch off
when the engine is not running.

To defog or defrost the outside rear
view mirrors, push the switch.
The key must be in the "ON" position.

The thin heater wires on the inside of the
rear window will quickly clear the surface.
An indicator light will illuminate to indicate
the defogger is operating.

The heater panels in the outside rear view
mirrors will quickly clear the surfaces. An
indicator light will illuminate to indicate the
mirror heaters are operating.

Push the switch once again to turn the
defogger off.

Push the switch once again to turn the
defoggers off.

The system will automatically shut off after the defogger has operated about 15
minutes.

The system will automatically shut off after the mirror heaters have operated about
15 minutes.

## p.116 CAUTION

CAUTION
Since the mirror surfaces can get hot,
do not touch them when the mirror
heater switch is on.
Make sure you turn the mirror heaters off
when the surfaces are clear. Leaving the
mirror heaters on for a long time could
cause the battery to discharge, especially
during stop-and-go driving. The mirror
heaters are not designed for drying rain
water or for melting snow.
If the outside rear view mirrors are heavily coated with ice, use a spray de-icer
before operating the switch.

NOTICE
To prevent the battery from being discharged, turn the switch off when the
engine is not running.

# Section 1-6: Gauges, Meters and Service reminder indicators

## p.117 SECTION

SECTION

1- 6

OPERATION OF INSTRUMENTS AND
CONTROLS
Gauges, Meters and Service reminder indicators
Fuel gauge . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 118
Engine coolant temperature gauge . . . . . . . . . . . . . . . . . . . . . . . . . . . 118
Engine oil pressure gauge . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 119
Voltmeter . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 120
Tachometer . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 120
Odometer and two trip meters . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 121
Service reminder indicators and warning buzzers . . . . . . . . . . . . . . 122
Trip information display . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 129

## p.118 Engine coolant temperature

Engine coolant temperature
gauge

Fuel gauge
If the fuel tank is completely empty, the
malfunction indicator lamp comes on. Fill
the fuel tank immediately.

The gauge indicates the approximate
quantity of fuel remaining in the tank
when the ignition switch is on.
Nearly full-Needle at "F"
Nearly empty-Needle at "E"
It is a good idea to keep the tank over
1/4 full.
If the fuel level approaches "E" or the low
fuel level warning light comes on, fill the
fuel tank as soon as possible.
On inclines or curves, due to the movement of fuel in the tank, the fuel gauge
needle may fluctuate or the low fuel level
warning light may come on earlier than
usual.

The indicator lamp goes off after driving
several times. If the indicator lamp does
not go off, contact your Toyota dealer as
soon as possible.
It is not a malfunction even if the needle
of the fuel gauge returns to "E" when the
ignition switch is turned to the "START"
position.

The gauge indicates the engine coolant
temperature when the ignition switch is
on. The engine operating temperature
will vary with changes in weather and
engine load.
If the needle points to the red zone or
higher, stop your vehicle and allow the
engine to cool.
Your vehicle may overheat during severe
operating conditions, such as:

 Driving up a long hill on a hot day.
 Reducing speed or stopping after high
speed driving.

 Idling for a long period with the air
conditioning on in stop-and-go traffic.

 Towing a trailer.

## p.119 Engine oil pressure gauge

Engine oil pressure gauge
It is not a malfunction even if the needle
of the engine coolant temperature gauge
returns to "C" when the ignition switch is
turned to the "START" position.

Normal
driving

NOTICE
z Do not remove the thermostat in
the engine cooling system as this
may cause the engine to overheat.
The thermostat is designed to control the flow of coolant to keep the
temperature of the engine within
the specified operating range.
z Do not continue driving with an
overheated engine. See "If your vehicle overheats" on page 256.

It is not a malfunction even if the needle
of the engine oil pressure gauge returns
to "L" when the ignition switch is turned
to the "START" position.

NOTICE
Idling

Do not drive the vehicle with the engine oil pressure below the normal
range until the cause is fixed-it may
ruin the engine.

The engine oil pressure gauge indicates
engine oil pressure when the ignition
switch is on. Check it while driving to
make sure the needle is in the proper
range.
If the engine oil pressure should stay below the normal range, pull off the road to
a safe place and stop the engine immediately. Call a Toyota dealer or qualified
repair shop for assistance.
Engine oil pressure may not build up
when the engine oil level is too low. The
engine oil pressure gauge is not designed
to indicate oil level, and the engine oil
level must be checked using the level
dipstick.

## p.120 Voltmeter

Voltmeter

Tachometer
NOTICE
Do not let the indicator needle get
into the red zone. This may cause
severe engine damage.

The voltmeter tells whether the battery
is charged or discharged. Check it
while the engine is running-the needle
should always indicate as shown above.

The tachometer indicates engine speed
in thousands of rpm (revolutions per
minute). Use it while driving to prevent
engine over-revving.

If the needle reads below or above the
normal range while the engine is running,
it indicates the charging system needs immediate repair.

Driving with the engine running too fast
causes excessive engine wear and poor
fuel economy. Remember, in most cases
the slower the engine speed, the greater
the fuel economy.

However, it is normal for the needle to
drop below the normal range during engine starting.
It is not a malfunction even if the needle
of the voltmeter returns to "9" when the
ignition switch is turned to the "START"
position.

It is not a malfunction even if the needle
of the tachometer returns to "0" when the
ignition switch is turned to the "START"
position.

## p.121 Odometer and two trip meters

Odometer and two trip meters
3. Trip meter reset knob-Resets the two
trip meters to zero, and also change
the meter display.
To change the meter display, quickly
push and release the knob. The meter
display changes in the order from the
odometer to trip meter A to trip meter
B, then back to the odometer each
time you push.

This meter displays the odometer and
two trip meters.
1. Odometer-Shows the total
the vehicle has been driven.

To reset the trip meter A to zero, display the meter A reading, then push
and hold the knob until the meter is
set to zero. The same process can be
applied for resetting the trip meter B.

distance

2. Two trip meters-Show two different
distances independently driven since
the last time each trip meter was set
to zero.
You can use one trip meter to calculate
the fuel economy and the other to
measure the distance on each trip. All
trip meter data is cancelled if the electrical power source is disconnected.

## p.122 Service reminder indicators and warning buzzers

Service reminder indicators and warning buzzers
If the indicator or buzzer comes on...
(a)

(indicators and buzzer)

(b)

Do this.
If parking brake is off, stop immediately and contact Toyota dealer.

Fasten driver's seat belt.
(indicators and buzzer)

(c)

Fasten front passenger's seat belt.

(d)

Stop and check.

(e)

Replace engine oil.

(f)

Take vehicle to Toyota dealer.

(g)

Fill up tank.

## p.123 If the indicator or buzzer comes on...

If the indicator or buzzer comes on...

Do this.

(h)

Take vehicle to Toyota dealer immediately.

(i)

Take vehicle to Toyota dealer. If brake system warning light is also on, stop immediately and contact Toyota dealer.

(j)

Close all side doors and back door.

(k)

Shift four-wheel drive control out of "N".

(l)

Stop and check.

(m)

Take vehicle to Toyota dealer.

(n)

Key reminder buzzer

Remove key.

## p.124 (a) Brake System Warning Light and

(a) Brake System Warning Light and
Buzzer

Have your vehicle checked at your
Toyota dealer in the following cases:

This light comes on in the following cases
when the ignition key is in the "ON" position.

 The light does not come on even if the

 When the parking brake is applied...

 The light does not come on even if the

This light comes on for a few seconds
when the ignition key is in the "ON" position even after the parking brake is released.

A warning light turning on briefly during
operation does not indicate a problem.

Any of the following conditions may occur, but do not indicate a malfunction:

CAUTION

 The light may stay on for about 60

 When the brake fluid level is low...
CAUTION
It is dangerous to continue driving
normally when the brake fluid level is
low.

 When the hydraulic brake booster
fails...
If the hydraulic booster causes an problem
resulting in poor braking performance, the
warning light comes on and buzzer sounds
continuously.

parking brake is applied when the ignition key is in the "ON" position.
ignition key is turned on with the parking brake released.

If any of the following conditions occur, immediately stop your vehicle at
a safe place and contact your Toyota
dealer.

 The light does not turn off even
after the parking brake is released
while the engine is running.

 The warning buzzer comes on together with the warning light.
In either case, this can indicate that
the brakes may not work properly and
your stopping distance will become
longer. Depress the brake pedal firmly
and bring the vehicle to an immediate
stop.

 The brake system warning light remains on together with the "ABS"
warning light.
In this case, not only the anti-lock
brake system will fail but also the
vehicle will become extremely unstable during braking.

seconds after the ignition key is turned
to "ON" position. It is normal if it goes
out after a while.

 Depressing the brake pedal repeatedly

may turn on the warning light and
buzzer. It is normal if the light goes
out and the buzzer stops sounding after a few seconds.

 You may hear a small sound in the

engine compartment after the engine is
started or the brake pedal is depressed
repeatedly. This is a pump pulsating
sound of the brake system, and it is
not a malfunction.

## p.125 (b) Driver's Seat Belt Reminder Light

(b) Driver's Seat Belt Reminder Light
and Buzzer
The light and buzzer act as a reminder to
buckle up the driver's seat belt.
Once the ignition key is turned to "ON" or
"START", the reminder light flashes and
the buzzer sounds if the driver's seat belt
is not fastened. Unless the driver fastens
the belt, the light continues flashing and
the buzzer sounds 4 to 8 seconds.
(c) Front Passenger's
minder Light

Seat

Belt

Re-

The light acts as a reminder to have the
front passenger buckle up the seat belt.
Once the ignition key is turned to "ON" or
"START", the reminder light flashes if a
passenger sits in the front passenger seat
and does not fasten the seat belt. Unless
the front passenger fastens the belt, the
light continues flashing.
If luggage or other load is placed on the
front passenger seat, depending on its
weight and how it is placed on the seat,
built-in sensors in the seat cushion may
detect the pressure, causing the reminder
light to flash.

(d) Discharge Warning Light
This light warns that the battery is being
discharged.
If it comes on while you are driving, there
is a problem somewhere in the charging
system.
The engine ignition will continue to operate, however, until the battery is discharged. Turn off the air conditioning,
blower, radio, etc., and drive directly to
the nearest Toyota dealer or repair shop.

When you drive for about 7200 km (4500
miles) after engine oil replacement, this
light illuminates for about 3 seconds and
then flashes for about 12 seconds with
the ignition key is turned to "ON" position.
If you continue driving without engine oil
replacement, and if the driving range exceeds 8000 km (5000 miles), the light will
come on after the ignition key is turned
to "ON" position. The light will remain on
thereafter.

Do not continue driving if the engine
drive belt is broken or loose.

If the light is flashing, we recommend that
you replace the engine oil at an early
opportunity depending on the driving and
road condition. If the light comes on, replace it as soon as possible.

(e) Engine Oil Replacement Reminder
Light

You need to reset the light after the engine oil replacement. Reset the light by
following the procedure below:

NOTICE

This light acts as a reminder to replace
the engine oil.
This light will come on when the ignition
switch is turned to "ON", and will go off
after about a few seconds.

1. Turn the ignition key to the "OFF" position with the odometer reading shown.
(For details, see "Odometer and trip meter" on page 121).
2. Turn the ignition key to the "ON" position while holding down the "ODO/
TRIP" knob.
Hold down the knob until the light goes
off. Before the light goes off, it illuminates
for 3 seconds, flashes for 2 seconds, illuminates for 1 second.

## p.126 If the system fails to reset, the light will

If the system fails to reset, the light will
remain flashing.
(f) Malfunction Indicator Lamp
This lamp comes on when the ignition
key is turned to the "ON" position and
goes off after the engine starts. This
means that the warning light system is
operating properly.
If the lamp remains on, or the lamp
comes on while driving, first check the
followings.

 Empty fuel tank
If the fuel tank is empty, refuel immediately.

 Loose fuel tank cap
If the fuel tank cap is loose, securely
tighten it.
These cases are temporary malfunctions.
The malfunction indicator lamp will go off
after taking several driving trips.
If the lamp will not go off even after several trips, contact your Toyota dealer as
soon as possible.

If the lamp will not go off even after
the several trips...
or
If the fuel tank is not empty or the fuel
tank cap is not loose...

 There is a problem somewhere in the
engine, emission control system, electronic throttle control system, automatic
transmission electrical system or warning light system itself.

Contact your Toyota dealer as soon as
possible to service the vehicle.
If engine speed does not increase when
the accelerator pedal is depressed, there
may be a problem somewhere in the electronic throttle control system.
At this time, vibration may occur. However, if you depress the accelerator pedal
more firmly and slowly, you can drive your
vehicle at low speeds. Have your vehicle
checked by your Toyota dealer as soon as
possible.
Even if the abnormality of the electronic
throttle control system is corrected during
low speed driving, the system may not be
recovered until the engine is stopped and
the ignition key is turned to "ACC" or
"LOCK" position.

CAUTION
Be especially careful to prevent erroneous pedal operation.
Emissions Inspection and Maintenance
(I/M) programs
Your vehicle may not pass a state emission inspection if the malfunction indicator
lamp remains on. Contact your Toyota
dealer to check your vehicle's emission
control system and OBD (On-Board Diagnostics) system before taking your vehicle
for the inspection.
For details, see "Emissions Inspection and
Maintenance (I/M) programs" on page 288.
(g) Low Fuel Level Warning Light
This light comes on when the fuel level
in the tank becomes nearly empty. Fill up
the tank as soon as possible.

## p.127 (h) SRS Warning Light

(h) SRS Warning Light
This light will come on when the ignition key is turned to the "ON" position.
After about 6 seconds, the light will go
off. This means the system of the airbag and front seat belt pretensioners
are operating properly.
The warning light system monitors the airbag sensor assembly, front airbag sensors, side and curtain shield airbag sensors, curtain shield airbag sensors,
driver's seat position sensor, driver's seat
belt buckle switch, front seat belt pretensioner assemblies, inflators, warning light,
roll sensing of curtain shield airbags off
indicator light, interconnecting wiring and
power sources.
If either of the following conditions occurs,
this indicates a malfunction somewhere in
the components monitored by the warning
light system. Contact your Toyota dealer
as soon as possible to service the vehicle.

 The light does not come on when the
ignition key is turned to the "ON" position or remains on for more than 6
seconds or flashes.

If the light stays on, it indicates that the
driver and passenger airbags have a problem. If the light flashes, the side and curtain shield airbags and/or the seat belt
pretensioners have a problem.
(i) "ABS" Warning Light
The light comes on when the ignition
key is turned to the "ON" position. If
the anti-lock brake system and the
brake assist system work properly, the
light turns off after a few seconds.
Thereafter, if either of the systems malfunctions, the light comes on again.
When the "ABS" warning light is on (and
the brake system warning light is off), the
anti-lock brake system, the brake assist
system, the vehicle stability control system and/or active traction control system
do/does not operate, but the brake system
still operates conventionally.
When the "ABS" warning light is on (and
the brake system warning light is off), the
anti-lock brake system does not operate
so that the wheels could lock up during
a sudden braking or braking on slippery
road surfaces.

If either of the following conditions occurs, this indicates a malfunction somewhere in the components monitored by
the warning light system. Contact your
Toyota dealer as soon as possible to
service the vehicle.

 The light does not come on when the
ignition key is turned to the "ON" position, or remains on.

 The light comes on while you are driving.

A warning light turning on briefly during
operation does not indicate a problem.

CAUTION
If the "ABS" warning light remains on
together with the brake system warning light, immediately stop your vehicle at a safe place and contact your
Toyota dealer.
In this case, not only the anti-lock
brake system will fail but also the
vehicle will become extremely unstable during braking.

 The light comes on or flashes while
driving.

## p.128 Either of the following conditions may

Either of the following conditions may
occur, but do not indicate a malfunction.

 The light may stay on for about 60
seconds after the ignition key is turned
to "ON" position. It is normal if it turns
off after a while.

 Depressing the brake pedal repeatedly

may turn on the light. It is normal if it
turns off after a few seconds.

(j) Open Door Warning Light
This light remains on until all the side
doors and back door are completely
closed.
(k) Unengaged "Park" Warning Light
This light warns that the transmission
"Park" mechanism is not engaged. If the
four-wheel drive control is in the "N" position while the selector lever is in the "P"
position, the transmission will disengage
and the wheels will not lock.

CAUTION
To restore the park function, shift the
four-wheel drive control out of "N",
or the vehicle can move.

(l) Automatic Transmission Fluid Temperature Warning Light
This light warns that the automatic transmission fluid temperature is too high.
If this light comes on while you are driving, slow down and pull off the road. Stop
the vehicle at a safe place and put the
selector lever in "P" and leave the engine
idling until the light goes off. If the light
goes off, you can start the vehicle again.
If the light does not go off, call a Toyota
dealer or qualified repair shop for assistance.

(m) Vehicle Stability Control System and
Active Traction Control System
Warning Light
This light warns that there is a problem
somewhere in the vehicle stability control
system and/or active traction control system.

NOTICE

If the "VSC/TRAC" warning light and "VSC
OFF" indicator light come on, have your
vehicle checked by Toyota dealer as soon
as possible. However, it is no problem
that the "VSC/TRAC" warning light comes
on when the brake actuator temperature
becomes high. (For details, see "Active
traction control system" on page 145.)

Continued driving with the warning
light on may damage the automatic
transmission.

The lights will come on with the ignition
key turned to "ON", and will go off after
a few seconds.
The lights may come on for 60 seconds
after the ignition key is turned to "ON"
position. It is normal if they go out after
a while.
Depressing the brake pedal repeatedly
may turn on the lights. it is normal if they
go out after a few seconds.

## p.129 Trip information display

Trip information display
When the "VSC/TRAC" warning light and
"VSC OFF" indicator light come on, the
vehicle stability control system and/or active traction control system are not operating, but there is no problem if you continue to drive.
(n) Key Reminder Buzzer
This buzzer acts as a reminder to remove
the key when you open the driver's door
with the ignition key in the "ACC" or
"LOCK" position.
CHECKING SERVICE REMINDER INDICATORS (except the low fuel level warning
light)
1. Apply the parking brake.
2. Open one of the side doors or back
door.
The open door warning light should
come on.
3. Close the door.
The open door warning light should go
off.

4. Place the four-wheel drive control lever
in "N" position and the selector lever
in "P" position and turn the ignition key
to "ACC".
The "A/T P" should come on. It goes
off when you place the four-wheel
drive control lever in "H" or "L" position.
5. Turn the ignition key to "ON", but do
not start the engine.
All the service reminder indicators except the open door warning light should
come on. The "ABS", "VSC/TRAC",
"VSC OFF", "TRAC", and slip indicator
light go off after a few seconds. The
SRS warning light goes off after about
6 seconds.
There may be the case that the "ABS",
"VSC/TRAC" and "VSC OFF" stay on
for about 60 seconds after the ignition
key is turned to "ON" position. It is
normal if they go out after a while.
If any service reminder indicator or warning buzzer does not function as described
above, have it checked by your Toyota
dealer as soon as possible.

The following information is shown with
the ignition key turned on. Each time
you push the "MODE" button, the displayed information is changed.

 Average vehicle speed
 Driving distance after engine starting
 Available driving range
 Average fuel consumption after refueling

 Current fuel consumption
The displayed cruise information values
indicate the general driving condition and
may not always reflect precise and actual
conditions.

## p.130  Average vehicle speed

 Average vehicle speed

 Driving distance after engine starting

 Available driving range

The average vehicle speed is calculated
and displayed based on the total driving distance and the total driving time
with the engine running.

The driving distance after engine starting is displayed.

The available driving range is calculated and displayed depending on the
amount of remaining fuel.

The displayed value is updated every 10
seconds.
To begin recalculating, push the "RESET"
button for about 1 second.

To begin recalculating, push the "RESET"
button for about 1 second.

## p.131  Average fuel consumption after refueling

 Average fuel consumption after refueling
The average fuel consumption after refueling is calculated and displayed
based on the total driving distance and
the total fuel consumption after refueling.
The value is updated every 10 seconds.
When refueling, be sure to stop your vehicle and turn the ignition key off.

 Current fuel consumption
The current fuel consumption is calculated and displayed based on the driving distance and the fuel consumption
per 2 second interval with the engine
running.
The value is updated every 2 seconds.
If you are driving at low speeds just before stopping, the accurate figure may not
be shown.

## p.132 

# Section 1-7: Ignition switch, Transmission and Parking brake

## p.133 SECTION

SECTION

1- 7

OPERATION OF INSTRUMENTS AND
CONTROLS
Ignition switch, Transmission and Parking brake
Ignition switch with steering lock . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 134
Automatic transmission . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 135
Four-wheel drive system . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 139
Parking brake . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 142
Cruise control . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 142
Active traction control system . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 145
Vehicle stability control system . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 147

## p.134 Ignition switch with steering

Ignition switch with steering
lock
"ACC"-Accessories such as the radio
operate, but the engine is off.
If you leave the key in the "ACC" or
"LOCK" position and open the driver's
door, a buzzer will remind you to remove
the key.
"LOCK"-Engine is off and the steering
wheel is locked. The key can be removed only at this position.
To turn the key from "ACC" to the "LOCK"
position, you must put the selector lever
in the "P" position.
"START"-Starter motor on. The key
will return to the "ON" position when
released.
For starting tips, see page 236.
It is not a malfunction even if the needle
of the tachometer, fuel gauge, engine
coolant temperature gauge, engine oil
pressure gauge or voltmeter returns to
bottom position when the ignition switch is
turned to the "START" position.
"ON"-Engine on and all accessories
on.
This is the normal driving position.

Once you remove the key, the engine immobilizer system is automatically set. (See
"Engine immobilizer system" on page 12.)
When starting the engine, the key may
seem stuck at the "LOCK" position. To
free it, first be sure the key is pushed all
the way in, and then rock the steering
wheel slightly while turning the key gently.

NOTICE
Do not leave the key in the "ON"
position if the engine is not running.
The battery will discharge and the
electronic ignition system could be
damaged.

## p.135 Automatic transmission

Automatic transmission
Selector lever position
P: Parking, engine starting and key removal position
R: Reverse position
N: Neutral position
D: Normal driving position (Shifting into overdrive position)
4: Position for engine braking (Shifting into overdrive not possible)
3,2: Position for more powerful engine braking
L: Position for maximum engine braking
 The shift position is displayed on the instrument cluster
Driving pattern selector button for selecting a driving pattern suited to existing driving
conditions
"PWR" (power) mode for powerful acceleration
This indicator lights on the instrument panel
Normal mode for general driving condition
Second start mode selector button for selecting either second start mode or normal driving mode

 Shift while pressing the brake pedal.
(Ignition switch must be in the "ON" position)

Second start mode
This indicator lights on the instrument panel in the second
start mode

 When the

cruise control is being used, even if you downshift from "D" to "4", engine braking will not be enabled because the cruise control
is not cancelled. For ways to decrease the vehicle speed, see "Cruise control" on page 142.

## p.136 Your automatic transmission has a shift

Your automatic transmission has a shift
lock system to minimize the possibility of
incorrect operation. This means you can
only shift out of "P" position when the
brake pedal is depressed with the ignition
switch in "ON" position.
(a) Normal driving
1. Start the engine as instructed in "How
to start the engine" on page 236. The
transmission must be in "P" or "N".
2. With your foot holding down the brake
pedal, shift the selector lever to "D".
When the lever is in the "D" position, the
automatic transmission system will select
the most suitable gear for running conditions such as normal cruising, hill climbing, hard towing, etc.
Always use the "D" position for better fuel
economy and quieter driving. If the engine
coolant temperature is low, the transmission will not shift into the overdrive gear
even in the "D" position.

CAUTION
Never put your foot on the accelerator pedal while shifting.

3. Release the parking brake and brake
pedal. Depress the accelerator pedal
slowly for smooth starting.
(b) Using engine braking
To use engine braking, you can downshift
the transmission as follows:

 Shift into the "4" position. The trans-

mission will downshift to fourth gear
and engine braking will be enabled.

 Shift into the "3" position. The trans-

mission will downshift to third gear
when the vehicle speed drops down to
or lower than following speed for third
gear, and more powerful engine braking
will be enabled.
Four -wheel drive control lever
in "H" . . . . . . . . . . . 124 km/h (77 mph)
Four -wheel drive control lever
in "L" . . . . . . . . . . . 49 km/h (31 mph)

 Shift into the "2" position. The trans-

mission will downshift to second gear
when the vehicle speed drops down to
or lower than following speed for second gear, and more powerful engine
braking will be enabled.
Four -wheel drive control lever
in "H" . . . . . . . . . . . 83 km/h (52 mph)
Four -wheel drive control lever
in "L" . . . . . . . . . . . 33 km/h (21 mph)

 Shift into the "L" position. The trans-

mission will downshift to first gear
when the vehicle speed drops down to
or lower than following speed for "L"
position and maximum engine braking
will be enabled.
Four -wheel drive control lever
in "H" . . . . . . . . . . . 43 km/h (27 mph)
Four -wheel drive control lever
in "L" . . . . . . . . . . . 17 km/h (11 mph)

When the cruise control is being used,
even if you downshift from "D" to "4",
engine braking will not be enabled because the cruise control is not cancelled.
For ways to decrease the vehicle speed,
see "Cruise control" on page 142.

CAUTION
Be careful when downshifting on a
slippery
surface.
Abrupt
shifting
could cause the vehicle to skid or
spin.

## p.137 (c) Using "3", "2" and "L" positions

(c) Using "3", "2" and "L" positions
The "3", "2" and "L" positions are used for
strong engine braking as described previously.
With the selector lever in "3", "2" or "L",
you can start the vehicle in motion as
with the lever in "D".
With the selector lever in "3" and "2", the
vehicle will start in first gear and automatically shift to third or second gear.
With the selector lever in "L", the transmission is engaged in first gear.

(d) Backing up

NOTICE
z Be careful not to over-rev the engine. Watch the tachometer to keep
engine rpm from going into the red
zone. The approximate maximum allowable speed for each position is
given below for your reference:
Transmission
4 .......
3 .......
2 .......
L .......

L
67 (42)
48 (30)
33 (20)
19 (12)

km/h (mph)
Transfer
H
165 (102)
118 (73)
81 (50)
47 (29)

1. Bring the vehicle to a complete stop.
2. With the brake pedal held down with
your foot, shift the selector lever to the
"R" position.

NOTICE
Never shift into reverse while the vehicle is moving.

z Do not continue hill climbing or
hard towing for a long time in the
"3", "2" or "L" position. This may
cause severe automatic transmission damage from overheating. To
prevent such damage, "4" position
should be used in hill climbing or
hard towing.

## p.138 (e) Parking

(e) Parking

(f) Good driving practice

(g) Driving in "PWR" (Power) mode

1. Bring the vehicle to a complete stop.

 If the transmission repeatedly shifts up

In the "PWR" mode, the transmission is
shifted up and down at a higher vehicle
speed than in the Normal mode and a
more powerful acceleration is achieved. To
set the "PWR" mode, push in the driving
pattern selector button. The "PWR" mode
indicator light comes on.

 When towing a trailer, in order to main-

For ordinary driving, Toyota recommends
using the Normal mode to improve fuel
economy.

2. Pull the parking brake lever up fully to
securely apply the parking brake.
3. With the brake pedal pressed down,
shift the selector lever to the "P" position.
If the four-wheel drive control is in the
"N" position while the selector lever is in
the "P" position, the transmission will
damage and the wheels will not lock.

CAUTION
While the vehicle is moving, never
attempt to move the selector lever
into "P" position under any circumstances. Serious mechanical damage
and loss of vehicle control may result.

and down between fourth gear and overdrive gears when climbing a gentle
slope, shift the selector lever to the "4"
position. Be sure to shift the selector
lever to the "D" position immediately
afterward.
tain engine braking efficiency, do not
use overdrive.

CAUTION
Always keep your foot on the brake
pedal while stopped with the engine
running. This prevents the vehicle
from creeping.

NOTICE
Always use the brake pedal or the
parking brake to hold the vehicle on
an upgrade. Do not attempt to hold
the vehicle using the accelerator pedal, as this can cause the transmission
to overheat.

(h) Driving in "2nd
start) mode

STRT"

(second

In the "2nd STRT" (Second start) mode,
the transmission system shifts up from
second gear. Use this mode when starting
your vehicle in sand, mud, ice or snow.
To set the "2nd STRT" mode, push the
"2nd" button. In the "2nd STRT" mode, the
"2nd STRT" indicator light comes on.
The "PWR" mode is automatically cancelled when you push the "2nd" button.

## p.139 Four-wheel drive system-

Four-wheel drive system-
(a) Four-wheel drive contro l
Use the center differential lock system if
your wheels get stuck in a ditch, or when
you are driving on a slippery or bumpy
surface. When the center differential is
locked, the vehicle stability control system
is automatically turned off and the center
differential lock and "VSC OFF" indicator
lights come on because the function that
controls engine performance interferes
with the process of freeing your wheels.

(i) If you cannot shift the selector lever out of "P" position
If you cannot shift the selector lever from
the "P" position even though the brake
pedal is depressed, use the shift lock
override button. For instructions, see "If
you cannot shift automatic transmission
selector lever" on page 272.

NOTICE

Use the four-wheel drive control lever
and center differential lock button to
select the transfer and center differential modes.
The "H" and "L" position of the four-wheel
drive control lever provides either lock or
unlock mode of the center differential depending on the center differential lock button position.

As soon as the center differential lock
switch is turned on, the "VSC OFF"
indicator light comes on. After the
wheels are out of the ditch or off the
slippery or bumpy surface, turn the
center differential lock switch off.
Make sure the center differential lock
indicator light and vehicle stability
control system off indicator light turn
off.

## p.140 "H" (high speed position, center differential unlocked): Lever at "H", center di

"H" (high speed position, center differential unlocked): Lever at "H", center differential lock button left out
Use this for normal driving on all types of
roads, from dry hard-surfaced roads to
wet, icy or snow-covered roads. This
position gives greater economy, quietest
ride, least wear and better vehicle control.
"H" (high speed position, center differential locked): Lever at "H", center differential lock button pushed in
Use this for greater traction when you
experience a loss of power, such as
wheel slipping, in the center differential
unlock mode.
"N" (neutral position): Lever at "N"
No power is delivered to the wheels. The
vehicle must be stopped.
"L" (low speed position, center differential unlocked): Lever at "L", center differential lock button left out
Use this for maximum power and traction.
Use this for climbing or descending steep
hills, off-road driving, and hard pulling in
sand or mud.

In this mode, the braking feeling that occurs when the wheels are negotiating a
sharp corner is further reduced than in the
"L" (low position, center differential locked)
mode.
"L" (low speed position, center differential locked): Lever at "L", center differential lock button pushed in.
Use this for maximum power and traction.
Use this for hard pulling in situations the
vehicle cannot negotiate even in the "L"
(low speed position, center differential un-
locked) mode. Also, using this mode when
driving down steep off-road inclines will
help contribute to increased vehicle stability.
The indicator light tells when the differential lock is engaged. Note that the differential is not still locked as long as the
indicator light remains off.
When the operation is not completed, the
indicator blinks. If the indicator light does
not go off when you push out the center
differential lock switch, drive straight
ahead while accelerating or decelerating,
or drive in reverse.

The center differential lock system operation is not completed within 5 seconds
while the cruise control system is set,
cancel the cruise control system. To cancel the cruise control system, see "Cruise
control" on page 142.
If the indicator light does not go off when
you push out the center differential lock
button, drive straight ahead while accelerating or decelerating, or drive in reverse.
See "(b) Shifting procedure" for further instructions.
Advice for driving on slippery roads in
"L" (low speed position) mode
If you shift the four-wheel drive control
lever to "L" and the automatic transmission lever to "2" when you drive in steep
off-road areas, the output of the brake
can be controlled effectively by the active
traction control system, which assists the
driver to control the driving power of 4
wheels.

## p.141 (b) Shifting procedure

(b) Shifting procedure
Use the "L" position of the automatic
transmission lever for maximum power
and traction when your wheels get stuck
or when you drive down a steep incline.
In the following cases, the output of the
brake can be controlled by the active traction control system if the engine speed is
under 3,000 rpm (normally engine speed
is under 3,000 rpm when the wheels get
unstuck).

 The four-wheel drive control lever in
the "L" position and the automatic
transmission lever in the "L" position or
the automatic transmission lever in the
"D", "4", "3" or "2" with the transmission downshifting to the first gear

SHIFTING BETWEEN "H" (UNLOCKED)
AND "H" (LOCKED)
To shift between unlock and lock
modes in "H", push the center differential
lock button.
SHIFTING BETWEEN "L" (UNLOCKED)
AND "L" (LOCKED)
To shift between unlock and lock
modes in "L", push the center differential
lock button.
SHIFTING BETWEEN "H" AND "L"
Stop the vehicle, put the transmission into
"N" and move the four-wheel drive control
lever.

 The four-wheel drive control lever in

CAUTION

(As for the automatic transmission lever
positions, see "Automatic transmission" on
page 135.)

Never move the four -wheel drive control lever if wheels are slipping. Wait
until the wheels have stopped slipping or spinning before shifting.

the "L" position and the automatic
transmission lever in the "R" position

NOTICE
For normal driving on dry and hard
surface roads, unlock the center differential. To prevent damage to the
center differential lock system, do not
push the center differential lock button when the vehicle is cornering or
when its wheels are spinning freely
off the ground. If the indicator light
does not go off when unlocking the
center
differential,
drive
straight
ahead while accelerating or decelerating, or drive in reverse.

## p.142 Parking brake

Parking brake

Cruise control
CAUTION
Before driving, be sure the parking
brake is fully released and the parking brake reminder light is off.

When parking, firmly apply the parking
brake to avoid inadvertent creeping.
To set: Pull up the lever. For better holding power, first depress the brake pedal
and hold it while setting the parking
brake.
To release: Pull up the lever slightly (1),
press the lock release button (2), and lower (3).
To remind you that the parking brake is
set, the parking brake reminder light in
the instrument panel remains on until you
release the parking brake.

The cruise control allows you to cruise
the vehicle at a desired speed over
about 40 km/h (25 mph) even with your
foot off the accelerator pedal.
Your cruising speed can be maintained
within the limits of engine performance,
although a slight speed change may occur
when driving up or down the grades. On
steeper hills, a greater speed change will
occur so it is better to drive without the
cruise control.
When the cruise control is on, the driving
pattern of the automatic transmission is
fixed in the normal position, regardless of
the position of the driving pattern selector
switch.

## p.143 CAUTION

CAUTION

 To help maintain maximum control
of your vehicle, do not use the
cruise control when driving in
heavy or varying traffic, or on slippery (rainy, icy or snow -covered) or
winding roads.

 Avoid vehicle speed increases when
driving downhill. If the vehicle
speed is too fast in relation to the
cruise control set speed, cancel the
cruise control then downshift the
transmission to use engine braking
to slow down.

TURNING THE SYSTEM ON

SETTING AT A DESIRED SPEED

To operate the cruise control, push the
"ON·OFF" switch. This turns the system
on. The indicator light in the instrument
panel shows that you can now set the
vehicle at a desired cruising speed. Another push on the switch will turn the system
completely off.

The transmission must be in "D" or "4"
before you set the cruise control speed.

CAUTION
To avoid accidental cruise control engagement, keep the "ON·OFF" button
off when not using the cruise control.

Bring your vehicle to the desired speed,
push the lever down in the "- SET" direction and release it. This sets the vehicle
at that speed.
If the speed is not satisfactory, tap the
lever up for a faster speed, or tap it down
for a slower speed. Each tap changes the
set speed by 1.6 km/h (1.0 mph). You can
now take your foot off the accelerator
pedal.

## p.144 If you need acceleration-for example,

If you need acceleration-for example,
when passing-depress the accelerator
pedal enough for the vehicle to exceed
the set speed. When you release it, the
vehicle will return to the speed set prior
to the acceleration.

RESETTING TO A FASTER SPEED

RESUMING THE PRESET SPEED

Push the lever up in the "+ RES" direction
and hold it. Release the lever when the
desired speed is attained. While the lever
is held up, the vehicle will gradually gain
speed.

If the preset speed is cancelled by pulling
the control lever or by depressing the
brake pedal, pushing the lever up in the
"+ RES" direction will restore the speed
set prior to cancellation.

CANCELLING THE PRESET SPEED
a. Pulling the control lever in the
"CANCEL" direction and releasing it.

However, a faster way to reset is to accelerate the vehicle and then push the
control lever down in the "- SET" direction.

However, once the vehicle speed falls below about 40 km/h (25 mph), the preset
speed will not be resumed.

b. Depressing the brake pedal.

RESETTING TO A SLOWER SPEED

If the "CRUISE" indicator light in the
instrument cluster flashes when using the
cruise control, press the "ON·OFF" button
to turn the system off and then press it
again to turn it on.

You can cancel the preset speed by:

c. Pushing the "CRUISE ON-OFF" switch.
If the vehicle speed falls below about 40
km/h (25 mph), the preset speed will automatically cancel out.
If the vehicle speed drops 16 km/h (10
mph) below the preset speed, the preset
speed will also automatically cancel out.
If the preset speed automatically cancels
out for other than the above cases, have
your vehicle checked by your Toyota dealer at the earliest opportunity.

Push the lever down in the "- SET" direction and hold it. Release the lever when
the desired speed is attained. While the
lever is held down, the vehicle speed will
gradually decrease.
However, a faster way to reset is to depress the brake pedal and then push the
control lever down in the "- SET" direction.
Even if you downshift the transmission
from the "D" position to "4" with the cruise
control on, engine braking will not be applied because the cruise control is not
cancelled. To decrease the vehicle speed,
reset to a slower speed with the cruise
control lever or depress the brake pedal.
If you use the brake pedal, cruise control
is cancelled.

CRUISE CONTROL FAILURE WARNING

If any of the following conditions then occurs, there is some trouble in the cruise
control system.

 The indicator light does not come on.
 The indicator light flashes again.
 The indicator light goes out after it
comes on.

If this is the case, contact your Toyota
dealer and have your vehicle inspected.

## p.145 Active traction control system

Active traction control system
When active traction control is applied,
the active traction control system indicator light blinks.

Active traction control system indicator
light
The active traction control system automatically helps control the spinning of
4 wheels which may occur when accelerating on slippery road surfaces, by
controlling the output of the brake and
engine. Thus, the system assists driver
to control the driving power of 4
wheels. When you turn the ignition
switch on, the active traction control
system always turns on automatically,
and the active traction control indicator
light will come on. The indicator light
will go off after a few seconds.

You may hear a sound in the engine
compartment for a few seconds when the
engine is started or just after the vehicle
begins to move. This means that the active traction control system is in the self-
check mode, and does not indicate malfunction. When the active traction control
system is operating, you may feel vibration or hear noise of your vehicle, caused
by operation of the brakes. This indicates
the system is functioning properly.
When getting the vehicle out of mud or
newly fallen snow, etc., the active traction
control system will help operate to prevent
the wheels from spinning.

Active traction control system failure
warning
This light warns when there is a problem
somewhere in the active traction control
system.
If the "VSC/TRAC" warning light comes
on, have your vehicle checked by your
Toyota dealer as soon as possible.

## p.146 The brake actuator temperature increases

The brake actuator temperature increases
during the active traction control system
or vehicle stability control system operating. If the brake actuator temperature becomes too high while the active traction
control system or vehicle stability control
system is operating, a buzzer will start to
sound intermittently to indicate that the
active traction control system can no longer operate. In this case, immediately stop
your vehicle at a safe place. If the system
continues to operate, the buzzer sound
changes from intermittent to continuous.
(The continuous buzzer sounds for about
3 seconds.) At the time, the "VSC/TRAC"
warning light will come on and the active
traction control system temporarily stops
operating in order to protect the brake
actuator. (Although the active traction control system does not operate, there is no
problem to continue your driving.) The
system will be automatically restored after
a short time and "VSC/TRAC" warning
light goes off if the accelerator pedal is
released.
When the "ABS" warning light come on,
the active traction control system is not
operating.
The "VSC/TRAC" warning light will come
on when the ignition key is turned "ON",
and will go off after a few seconds.

The "VSC/TRAC" warning light may stay
on for 60 seconds after the ignition key
is turned to "ON" position. It is normal if
it goes off after a few seconds.
Depressing the brake pedal repeatedly
may turn on the "VSC/TRAC" warning
light. It is normal if it goes off after a few
seconds.
When the "VSC/TRAC" warning light
comes on the active traction control system is not operating, but there is no problem if you continue to drive.
In the following cases, contact your Toyota
dealer:

 The "VSC/TRAC" warning light does not

come on after the ignition key is turned
"ON".

 The "VSC/TRAC" remains on after the
ignition key is turned "ON".

CAUTION
Under certain slippery road conditions, full traction of the vehicles and
power to 4 wheels may not be maintained, even though the active traction control system is in operation.
Do not drive the vehicle under any
speed or maneuvering conditions
which will cause the vehicle to lose
traction. In situations where the road
surface is covered with ice or snow,
your vehicle should be fitted with
snow tires or tire chains. Always
drive at an appropriate and cautious
speed for the road conditions present.

## p.147 Vehicle stability control

Vehicle stability control
system
The vehicle stability control system
helps provide integrated control of the
systems such as anti-lock brake, traction control, engine control, etc. This
system automatically controls the output of the brakes or engine to help
prevent the vehicle from skidding under
adverse conditions.
The system activates when the vehicle
speed is about more than 15 km/h (9
mph).
You may hear a sound in the engine
compartment for a few seconds when the
engine is started or just after the vehicle
begins to move. This means that the vehicle stability control system is in the
self-check mode and does not indicate a
malfunction.

CAUTION

 Active traction control system, vehicle stability control system and
anti-lock brake system are electronic systems designed to help the
driver maintain control under adverse conditions. They are not a
substitute for safe driving practices.
Factors including speed, road conditions and driver steering input
can all affect whether active traction control system, vehicle stability
control system and anti-lock brake
system will be effective in preventing a loss of control. Always keep
safety driving in mind. If the slip
indicator light flashes, sounding an
alarm, special care should be taken
while driving.

 Only use tires of specified size. The
size, manufacturer, brand and tread
pattern for all 4 tires should be the
same. If you use the tires other
than specified, or different type or
size, the vehicle stability control
system may not function correctly.
When replacing the tires or wheels,
contact your Toyota dealer. (See
"Checking and replacing tires" on
page 304.)

## p.148 If the vehicle is going to skid during driving, the slip indicator light flashes

If the vehicle is going to skid during driving, the slip indicator light flashes and an
alarm sounds intermittently.
When you turn the ignition switch on, the
slip indicator light will come on. The slip
indicator light will go off after a few seconds.

Pushing the center differential lock button
automatically turns the vehicle stability
control system off. At this time, the "VSC
OFF" indicator comes on with the center
differential lock indicator light. (For details,
see "Four-wheel drive system-(a)Four-
wheel drive control" on page 139.)

Vehicle stability control system failure
warning
These lights warn when there is a problem somewhere in the vehicle stability
control system or active traction control
system.
If the "VSC/TRAC" warning light and "VSC
OFF" indicator light come on, have your
vehicle checked by your Toyota dealer as
soon as possible. However, there is no
problem if the "VSC/TRAC" warning light
comes on when the brake actuator temperature becomes high. (For details, see
"Active traction control system" on page
145.)

## p.149 When the "ABS" warning light comes on,

When the "ABS" warning light comes on,
the vehicle stability control system is not
operating.
The "VSC/TRAC" warning light and "VSC
OFF" indicator light will come on when the
ignition key is turned "ON", and will go off
after a few seconds.
The "VSC/TRAC" warning light and "VSC
OFF" indicator light may stay on for 60
seconds after the ignition key is turned to
"ON" position. It is normal if they go off
after a few seconds.
Depressing the brake pedal repeatedly
may turn on the lights. It is normal if they
go off after a few seconds.
When the "VSC/TRAC" warning light and
"VSC OFF" indicator light come on, the
vehicle stability control system is not operating, but there is no problem if you
continue to drive.
In the following cases, contact your Toyota
dealer:
 The "VSC/TRAC" warning light, "VSC
OFF" indicator light and slip indicator
light do not come on after the ignition
key is turned "ON".
 The "VSC/TRAC" warning light and
"VSC OFF" indicator light remain on after the ignition key is turned "ON".
 The "VSC OFF" indicator light comes
on while driving without pushing the
center differential lock switch.

## p.150 

# Section 1-8: Audio system

## p.151 SECTION

SECTION

1- 8

OPERATION OF INSTRUMENTS AND
CONTROLS
Audio system
Reference . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 152
Using your audio system . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 152
Audio system operating hints . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 165
Rear seat audio system . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 170
Audio remote controls (steering switches) . . . . . . . . . . . . . . . . . . . . . 172

For vehicle equipped with Navigation system, please refer to the
separate "Navigation System Owner's Manual".

## p.152 Reference

Reference
AM·FM radio/cassette player/compact
disc changer controller/compact disc
player with changer (with XM satellite
radio* controller)
*: Use of satellite radio requires XM tuner
and service. Contact your Toyota dealer
for details.

Using your audio system-
-some basics
This section describes some of the basic
features on Toyota audio systems. Some
information may not pertain to your system.

SWITCHING BETWEEN FUNCTIONS

Your audio system works when the ignition
key is in the "ACC" or "ON" position.
TURNING THE SYSTEM ON AND OFF

*: Use of satellite radio requires XM tuner
and service. Contact your Toyota dealer
for details.

Push "PWR·VOL" to turn the audio system
on and off.

LISTENING TO THE XM SATELLITE RADIO BROADCAST*

Push "AM·SAT", "FM", "TAPE" or "DISC"
to turn on that function without pushing
"PWR·VOL".

To listen to a satellite radio broadcast in
your vehicle, an additional genuine Toyota
satellite receiver and antenna (or equivalents) must be purchased and installed. A
subscription to the XM satellite radio service is also necessary.

You can turn on each player by inserting
a cassette tape or compact disc.
You can turn off each player by ejecting
the cassette tape or compact disc. If the
audio system was previously off, then the
entire audio system will be turned off
when you eject the cassette tape or compact disc. If the another function was previously playing, it will come on again.
*: Use of satellite radio requires XM tuner
and service. Contact your Toyota dealer
for details.

Push "AM·SAT", "FM", "TAPE" or "DISC"
if the system is already on but you want
to switch from one function to another.

How to subscribe to an XM satellite
radio
An XM satellite radio is a tuner designed
exclusively to receive broadcasts provided
under a separate subscription. Availability
is limited to the 48 contiguous states.

## p.153 How to subscribe:

How to subscribe:
You must enter into a separate service
agreement with the XM radio in order to
receive satellite broadcast programming in
the vehicle. Additional activation and service subscription fees apply that are not
included in the purchase price of the vehicle and optional digital satellite tuner.
For complete information on subscription
rates and terms, or to subscribe to the
XM radio, visit XM on the web at
www.xmradio.com or call an XM's Listener
Care at (800) 852-9696. The XM radio is
solely responsible for the quality, availability and content of the satellite radio services provided, which are subject to the
terms and conditions of the XM radio customer service agreement.
Customers should have their radio ID
ready; the radio ID can be found by tuning to "channel 000" on the radio. For
details, see "Displaying the radio ID" below.

Satellite tuner technology notice:
Toyota's satellite radio tuners are awarded
Type Approval Certificates from XM Satellite Radio Inc. on "March 10, 2003" and
"April 15, 2003" as proof of compatibility
with the services offered by the XM satellite radio.
Displaying the radio ID
Each XM tuner is identified with a unique
radio ID. You will need the radio ID when
activating XM service or when reporting a
problem.
If you select the "CH 000" using the
"AUDIO-TUNE" knob, the ID code of 8
alphanumeric characters appears. If you
select another channel, display of the ID
code is canceled. The channel (000) alternates the display between the radio ID
and the specific radio ID code.
*: Use of satellite radio requires XM tuner
and service. Contact your Toyota dealer
for details.

TONE AND BALANCE
For details about your system's tone and
balance controls, see the description of
your own system.
Tone
How good an audio program sounds to
you is largely determined by the mix of
the treble, midrange, and bass levels. In
fact, different kinds of music and vocal
programs usually sound better with different mixes of treble, midrange, and bass.
Balance
A good balance of the left and right stereo
channels and of the front and rear sound
levels is also important.
Keep in mind that if you are listening to
a stereo recording or broadcast, changing
the right/left balance will increase the volume of one group of sounds while decreasing the volume of another.

All fees and programming are the responsibility of the XM satellite radio and are
subject to change.

## p.154 YOUR RADIO ANTENNA

YOUR RADIO ANTENNA
Lowering the antenna
The antenna automatically extends when
the radio is on, and retracts when the
radio mode is off. However, even if you
turn off the radio when the radio on the
rear seat audio system is on, the antenna
does not retract. To lower a power antenna, push the "Ɲ" (down) switch. Also, the
antenna automatically goes down when the
radio mode is switched off to turn on the
cassette tape player or compact disc player, turning off the audio system by pushing "PWR·VOL" or turning the ignition key
to "LOCK" position.
Some models also have an antenna
printed on the inside of the right side
quarter window.

NOTICE
z Retract the antenna when entering
or passing through low structures,
such as a garage or an automatic
car wash. Failure to do so may
damage the antenna.
z The antenna mast has to be extended higher than 100 mm (3.94
in.) length when the audio is on.
Extend the antenna mast when the
radio signal is weak.
z Putting a window tint (especially,
conductive or metallic type) on the
right-hand rear quarter window may
affect the reception of radio or mobile telephone. For the installation
of the window tint, consult with
your Toyota dealer.

Down

Up

Adjusting the power antenna
To adjust the antenna height, push the
switch at either side, this may also be
performed during antenna extension. The
maximum extension length is 850 mm
(33.5 in.).
Every time you turn the radio on, the
antenna will extend to its previous position.
Clean the antenna mast periodically with
a clean dry cloth.

## p.155 CAUTION

CAUTION
Before extending the antenna, confirm
that no one is close enough to get
injured.
YOUR CASSETTE PLAYER
When you insert a cassette, the exposed
tape should be to the right.

NOTICE
Do not oil any part of the player and
do not insert anything other than cassette tapes into the slot, or the tape
player may be damaged.

YOUR COMPACT DISC PLAYER
When you insert a disc, gently push it in
with the label side up.
The discs set in the player are played
continuously, starting with disc number 1.
The disc number of the disc currently being played, the track number and the time
from the beginning of the program appear
on the display.
When play of one disc ends, the first
track of the following disc starts. When
play of the final disc ends, play of the
first disc starts again.
The player will skip any empty disc number.

NOTICE
z Do not stack up two discs for insertion, or it will cause damage the
compact disc player. Insert only one
compact disc into slot at a time.
z Never try to disassemble or oil any
part of the compact disc player. Do
not insert anything other than compact discs into the slot.
The player is intended for use with 12 cm
(4.7 in.) discs only.

## p.156 -Controls and features

-Controls and features
Details of specific buttons, controls, and
features are described in the alphabetical
list that follows.
## p.157 1 2 3 4 5 6 (Preset buttons)

1 2 3 4 5 6 (Preset buttons)
These buttons are used to preset and
tune in radio stations.
To preset a station to a button: Tune in
the desired station (see "AUDIO-TUNE"
knob or "SEEK TRACK" button). Push and
hold down the button until you hear a
beep-this will set the station to the button. The button number will appear on the
display.
To tune in to a preset station: Push the
button for the station you want. The button number and station frequency will appear on the display.
These systems can store one AM and two
FM stations for each button (The display
will show "AM", "FM1" or "FM2" when you
push "AM·SAT" or "FM" button).
XM satellite radio*-
These buttons are used to preset and
tune in radio channels.
To preset a channel to a button: Tune in
the desired channel. (See "AUDIO-TUNE"
or "SEEK TRACK".) Push and hold down
the button until you hear a beep-this will
set the channel to the button. The preset
button number will appear on the display.

To recall a preset channel: Push the button for the channel you want. The preset
button number and channel number will
appear on the display.
This radio can store three XM channels
for each button. (The display will show
"SAT1", "SAT2" or "SAT3" when you push
"AM·SAT" button
*: Use of satellite radio requires XM tuner
and service. Contact your Toyota dealer
for details.
(Eject button)
Cassette tape
Push the cassette tape eject button to
eject a cassette.
Compact disc
To eject one compact disc only: Push and
release the compact disc eject button. If
you hold the button too long (if the audio
system is on at this time, you hear a
beep.), the mechanism will change to the
mode for ejecting all the discs loaded in
the changer. You can also eject any specific one of the discs loaded in the player
as follows:

2. Push and release the compact disc
eject button.
To eject all the discs loaded in the player:
Push and hold the compact disc eject button (until you hear a beep when the audio
system is on). The last compact disc
played before pushing the button will be
ejected first. If a disc is left in the slot
for a long time, the function to eject all
the discs will be automatically cancelled.
(Program)
Push "
" to select the other side of a
cassette tape. The display indicates which
side is currently selected (" " indicates
top side, "

" indicates bottom side).

Auto-reverse feature: After the cassette
player reaches the end of a tape side, it
automatically reverses and begins to play
the other side. This is true whether the
cassette was playing or fast forwarding.

1. Push either side of the "ƝDISCƜ"
button until the number of the disc you
want to eject is displayed.

## p.158 (Reverse/Fast forward buttons)

(Reverse/Fast forward buttons)
Cassette Player
Push the fast forward button to fast forward a cassette tape. "FF" will appear on
the display. Push the reverse button to
rewind a tape. "REW" will appear on the
display.
To stop the tape while it is fast forwarding, push the fast forward button or
"TAPE"; to stop the tape while it is rewinding, push the reverse button or
"TAPE".
If a tape side rewinds completely, the cassette player will stop and then play that
same side. If a tape fast forwards completely, the cassette player will play the
other side of the tape, using the auto-reverse feature.
Compact Disc Player
If you want to fast forward or reverse
through a compact disc track, push and
hold in the fast forward or reverse button.
When you release the button, the compact
disc player will resume playing.

AM button

Manual tuning function-

Push "AM·SAT" to turn on the radio and
select the AM band. "AM" will appear on
the display.

Turn the knob. The radio will step up or
down to another frequency.

If the audio system is off, you can turn
on the radio by pushing "AM". Also, push
"AM" to switch from cassette or compact
disc operation to radio operation.

Turn the knob. The radio will step up or
down the channel.

AUDIO-TUNE Knob
This knob is used to adjust the tone and
balance or to tune the station manually on
the radio mode.
Tone and sound balance adjustment function-
Each time you push the "AUDIO-TUNE"
knob, the display changes as in the following. To adjust the tone and balance or
turn on or off the automatic sound levelizer, turn the knob.
BAS: Adjusts low-pitched tones.
MID: Adjusts mid-pitched tones.
TRE: Adjusts high-pitched tones.
BAL: Adjusts the sound balance between
the right and left speakers.
FAD: Adjusts the sound balance between
the front and rear speakers.

XM satellite radio*-

*: Use of satellite radio requires XM tuner
and service. Contact your Toyota dealer
for details.
DISC (Compact Disc) button
Push "DISC" to switch from radio or cassette operation to compact disc operation.
If the audio system is off, you can turn
on the compact disc player by pushing
"DISC". In both cases, a disc must already be loaded in the player.
When the audio is set into compact disc
operation, the display shows the track or,
track and disc number currently being
played.
If the player or another unit equipped with
the player malfunctions, your audio system
will display one of the four following error
messages.

## p.159 If "WAIT" appears on the display, it indicates that the inside of the player uni

If "WAIT" appears on the display, it indicates that the inside of the player unit
may be too hot due to the very high ambient temperature. Remove the disc from
the player and allow the player to cool
down.
If "ERROR 1" appears on the display,
it indicates the disc is dirty, damaged or
label face down. Clean the disc or insert
it correctly.
If "ERROR 3" or "ERROR 4" appears
on the display, it indicates there is a
trouble inside the system. Eject the disc.
Set the disc again.
If the malfunction is not rectified, take
your vehicle to your Toyota dealer.
DISC ƝƜ
By using this button, you can select a
disc you wish to listen to.
Push either side of the button until the
number of the disc you want to listen to
appears on the display.

Dolby

B NR∗

If you are listening to a tape that was
recorded with Dolby B Noise Reduction,
" will appush the " " button. The "
pear on the display. Push the button again
to turn off Dolby B NR.
The Dolby NR mode reduces tape noise
by about 10 dB. For best sound reproduction, play your tapes with this button on
or off according to the mode used for
recording the tape.
∗

: Dolby noise reduction manufactured under license from
Dolby Laboratories Licensing Corporation. "DOLBY" and the
double D symbol
are trademarks of Dolby Laboratories
Licensing Corporation.

FM button
Push "FM" to turn on the radio and select
the FM band. "FM1" or "FM2" will appear
on the display. This system allows you to
set six stations in FM1 and six stations
in FM2.
If the audio system is off, you can turn
on the radio by pushing "FM". Also, push
"FM" to switch from cassette or compact
disc operation to radio operation.

LOAD button
This button is used to load the compact
discs in the compact disc auto changer
which is integrated with the radio and cassette player. This compact disc auto
changer can store up to 6 discs.
The key must be in the "ACC" or "ON"
position.
Loading one compact disc only-
To load one compact disc only, quickly
push and release the button. If you hold
the button too long (if the audio system
is on at this time, you hear a beep.), the
mechanism will change to the mode for
loading multiple compact discs. After
pushing the button, insert a compact disc.
At this time, the indicators on both sides
of the slot are flashing. After the disc is
loaded, the shutter of the slot will close
and the indicators will stop flashing.
If no compact disc is inserted, the shutter
will close after 15 seconds.

## p.160 Loading multiple compact discs-

Loading multiple compact discs-

RAND (Random)

RDS (Radio Data System) display

To load multiple compact discs, push and
hold (until you hear a beep when the audio system is on). After pushing the button, insert the first compact disc. At this
time, the indicators on both sides of the
slot are flashing. After the disc is loaded,
the shutter of the slot will close and the
indicators will stop flashing. After a few
seconds, the shutter will automatically
open again so the next disc can be inserted. The same process can be applied
for loading the rest of the discs.

There are two random features-you can
either listen to the tracks on all the compact discs in the player in random order,
or only listen to the tracks on a specific
compact disc in random order.

The radio will automatically switch to the
RDS mode to receive an RDS station
while turned to FM broadcasts. "RDS" will
appear on the display.

If no compact disc is inserted, the shutter
will close after 15 seconds.
PWR·VOL (Power and Volume) knob
Push "PWR·VOL" to turn the audio system
on and off. Turn "PWR·VOL" to adjust the
volume.

To randomly play for the tracks on a disc:
Quickly push and release "
". "
"
will appear on the display. The disc you
are listening to will play in random order.
If you hear a beep, you held the button
too long, and the player will play all the
tracks in the player in random order. To
turn off the random feature, push this button again.
To randomly play for all the tracks in the
player:
" until you hear a
Push and hold "
" will appear on the disbeep. "
play and the player will perform all the
tracks on all the discs in the player in
random order. To turn off the random feature, push this button again.

RPT (Repeat)
Cassette Player
" while the track is playing.
Push "
"
" will appear on the display. When
the track ends, it will automatically be
rewound and replayed. This process will
be continued until you push the button
again to turn off the repeat feature.
There must be at least 3 seconds of blank
space between tracks in order for the repeat feature to work correctly.

## p.161 Compact Disc Player

Compact Disc Player

SAT* (Satellite radio)

There are two repeat features-You can
either replay a disc track or a whole compact disc.

Push the "AM·SAT" button to turn on the
radio and select the XM band. "SAT1",
"SAT2" or "SAT3" will appear on the display. This system allows you to set eighteen XM channels, three for each of the
preset button.

Repeating a track:
Quickly push and release "
" while the
track is playing. "
" will appear on the
display. If you hear a beep, you held the
button too long, and the player will repeat
the whole disc. When the track ends, it
will automatically be replayed. This process will be continued until you push the
button again to turn off the repeat feature.
Repeating a disc:
Push and hold "

" until you hear a

" will appear on the display.
beep. "
The player will repeat all the tracks on the
disc you are listening to. When the disc
ends, the player will automatically go back
to the first track on the disc and replay.
This process will be continued until you
push the button again to turn off the repeat feature.

Error messages
If the satellite radio tuner malfunction,
your audio system will display one of the
six following error messages.
"ANTENNA":

 The premium channel you selected is

not authorized. Wait for about 2 seconds until the radio returns to the previous channel or "CH001". If it does
not change automatically, select another channel. If you want to listen to the
premium channel, contact the XM satellite radio.

"NO SIGNAL": The XM signal is too
weak at the current location. Wait until
your vehicle reaches a location with a
stronger signal.

 The XM antenna is not connected.

"LOADING": The unit is acquiring audio
or program information. Wait until the unit
has received the information.

 A short-circuit occurs in the antenna or

"OFF AIR": The channel you selected is
not broadcasting any programming. Select
another channel.

Check whether the XM antenna cable
is attached securely.
the surrounding antenna cable. See a
Toyota certified dealer.

"UPDATING":

 You have not subscribed to the XM
satellite radio. The radio is being updated with the latest encryption code.
Contact the XM satellite radio for subscription information. When a contact is
canceled, you can choose the "CH000"
and all free-to-air channels.

"- - -": The channel you selected is no
longer available. Wait for about 2 seconds
until the radio returns to the previous
channel or "CH001". If it does not change
automatically, select another channel.
The XM Listener Care Center is also
available on the phone, please call (800)
852-9696 during the following hours:
Monday - Saturday: 7 a.m. - 1 a.m.
Sunday: 12 p.m. - 12 a.m.

## p.162 *: Use of satellite radio requires XM tuner

*: Use of satellite radio requires XM tuner
and service. Contact your Toyota dealer
for details.
SCAN button
Radio
You can either scan all the frequencies on
a band or scan only the preset stations
for that band.
To scan the preset stations:
Push and hold "SCAN" until you hear a
beep. The radio will tune in the next preset station up the band, stay there for 5
seconds, and then move to the next preset station. To select a station, push
"SCAN" again.
To scan all the frequencies:
Quickly push and release "SCAN". If you
hear a beep, you held the button too long,
and the radio will scan the preset stations. The radio will find the next station
up the station band, stay there for 5 seconds, and then scan again. To select a
station, push "SCAN" again.

XM satellite radio*-

Compact Disc Player

You can either scan the currently selected
channel category or scan only the preset
channels for that band.

There are two scan features-you can either scan the tracks on a specific disc or
scan the first tracks of all the discs in the
player.

To scan the preset channels:
Push and hold the "SCAN" button until
you hear a beep. "SCAN" appears on the
display. The radio will tune in the next
preset channel up the band, stay there for
5 seconds, and then move to the next
preset channel. To stop scanning, push
this button again.
To scan the currently selected channel
category:
Quickly push and release the "SCAN" button. "SCAN" appears on the display. The
radio will find the next channel in the
same channel category up the band, stay
there for 5 seconds, and then scan again.
To stop scanning, push this button again.
*: Use of satellite radio requires XM tuner
and service. Contact your Toyota dealer
for details.

Scanning the tracks on a disc:
Quickly push and release "SCAN". "SCAN"
will appear on the display and the player
will scan all the tracks on the disc you
are listening to. If you hear a beep, you
held the button too long, and the player
will scan the first track of all the discs in
the player. To select a track, push "SCAN"
again. If the player scanned all the tracks
on the disc, it will stop scanning.
Scanning the first track of all the discs in
the player:
Push "SCAN" until you hear a beep.
"
·SCAN" will appear on the display
and the player will perform the first track
of the next disc. To select a disc, push
the "SCAN" again. If the player has
scanned all the discs, it will stop scanning.

## p.163 SEEK TRACK button

SEEK TRACK button
Radio
In the seek mode, the radio finds and
plays the next station up or down the
station band.
To seek a station, quickly push and release the "Ɯ" or "Ɲ". Do this again to
find another station.
XM satellite radio*-
To select the next channel within the current channel category, push the "Ɯ" or
"Ɲ" side of the "SEEK TRACK" button.
Repeat until a desired channel is found.

When counting the number of tracks you
want to rewind, remember to count the
current track as well. For example, if you
want to rewind to a song that is two before the song you are listening to, push
on the left side of the button until "REW
3" appears on the display.
If you have pushed the track button more
than you wanted to, push the other side
of the button. The track number will be
reduced.
The track number you select is not valid
if it is higher than the number of tracks
remaining on the current cassette side.

*: Use of satellite radio requires XM tuner
and service. Contact your Toyota dealer
for details.

 After the beginning of the tape is

Cassette Player

 After the end of the tape is reached,

By using this button, you can skip up or
down to a different track.
You can skip up to nine tracks at a time.
Push the right or left side of the button.
"FF 1" or "REW 1" will appear on the
display.
Next, push either side of the "SEEK
TRACK" button until the number on the
display reaches the number of tracks you
want to skip. If you push the button ten
times, the skip feature will be turned off.

reached, the player will automatically
start playing the same side.

the player will automatically reverse
sides and start playing the other side.

There must be at least 3 seconds of blank
space between tracks for the track button
to work correctly. In addition, the feature
may not work well with some spoken
word, live, or classical recordings.

Compact Disc Player
By using this button, you can skip up or
down to a different track.
Push either side of the "SEEK TRACK"
button until the number of the track you
want to listen to appears on the display.
If you want to return to the beginning of
the current track, push the left side of the
button one time, quickly.
ST (Stereo reception) display
Your radio automatically changes to stereo
reception when a stereo broadcast is received. "ST" appears on the display. If the
signal becomes weak, the radio reduces
the amount of channel separation to prevent the weak signal from creating noise.
If the signal becomes extremely weak, the
radio switches from stereo to mono reception.
TAPE button
Push "TAPE" to switch from radio or compact disc operation to cassette operation.
If the audio system is off, you can turn
on the cassette player by pushing "TAPE".
In both cases, a cassette must already be
loaded in the player.

## p.164 TEXT button

TEXT button
Radio
This button is operational only in RDS
mode.
To display the station name and text message, push this button while "RDS" appears on the display. Each time you push
the button, indication on the display will
change from the band to the station name
to radio text in this order. After 6 seconds
passes, indication returns to the band.
If the radio receives a radio text from
RDS station, "MSG" appears on the display. Push the button, and a text message
is displayed.
If the entire the message is not displayed,
"" will appear on the display. To display
the rest of the message, push and hold
the button until you hear a beep.
After the entire message has been displayed, the message will disappear.
XM satellite radio* 1 -
When you push the "TEXT" button, the
display changes as follows:
CH NAME → TITLE (SONG/PROGRAM
TITLE) → NAME (ARTIST NAME/FEATURE) → CH NUMBER → CH NAME

Up to 10 alphanumeric characters can be
displayed. (Some information will not be
fully displayed.)
The message display will be canceled if
any button that affects the display is
pushed.

Compact disc player
This button is used to change the display
for the compact disc that contains text
data.

If there is no song/program title or artist
name/feature associated with the channel
at that time, "- - - - -" will appear on
the display.

To change the display, quickly push and
release the "TEXT" button while the compact disc is playing. The display changes
in the order from the elapsed time to disc
title to track title, then back to the
elapsed time.

This XM tuner supports "Audio Services"
(Music and Talk) of only XM satellite radio
and "Text Information"* 2 linked to the respective audio services.

If this button is pushed while a compact
disc that does not contain text data is
playing, "NO TITLE" will appear on the
display.

* 1 : Use of satellite radio requires XM tuner and service. Contact your Toyota
dealer for details.

If the entire disc or track title does not
appear on the display, push and hold the
button until you hear a beep. The rest of
the title will appear.

* 2 : Text information includes, Channel
Name, (Artist) Name, (Song) Title and
Category Name.

## p.165 Audio system operating hints

Audio system operating hints
TRAF (Traffic announcement function)
button
When you push the "TRAF" button, "TRAF
SEEK" appears on the display and the
radio will start seeking any traffic program
station.
If no traffic program station is found, "NO
TRAF INFO" appears on the display for a
few seconds and the display returns to
the previous mode.
TYPE (Program type) button
When you push this button, the current
program type receiving from RDS station
appears on the display.
If the system receives no RDS stations,
"NO PTY" appears on the display.
Each time you push the "Ɲ" or "Ɯ", the
program type changes as in the following:

 ROCK
 EASY LIS (Easy listening)
 CLS/JAZZ (Classical music and jazz)
 R&B (Rhythm and Blues)
 INFORM (Information)
 RELIGION

 MISC
 ALERT (Emergency message)

NOTICE

With the program type displayed, push the
"SEEK/TRACK" or "SCAN" button. You can
seek or scan for the station broad casting
the same type of program.

To ensure correct audio system operations:

XM satellite radio*-

z Do not put anything other than a
cassette tape or Compact Disc into
the slot.

When you push the "Ɯ" or "Ɲ" side of
the "TYPE" button while receiving a XM
channel, the current channel category appears on the display.
When the channel category appears, push
either "Ɯ" or "Ɲ" side of the "TYPE" button to switch to the next or previous category.
*: Use of satellite radio requires XM tuner
and service. Contact your Toyota dealer
for details.

z Be careful not to spill beverages
over the audio system.

z The use of a cellular phone inside
or near the vehicle may cause a
noise from the speakers of the audio system which you are listening
to. However, this does not indicate
a malfunction.
RADIO RECEPTION
Usually, a problem with radio reception
does not mean there is a problem with
your radio-it is just the normal result of
conditions outside the vehicle.
For example, nearby buildings and terrain
can interfere with FM reception. Power
lines or telephone wires can interfere with
AM signals. And of course, radio signals
have a limited range. The farther you are
from a station, the weaker its signal will
be. In addition, reception conditions
change constantly as your vehicle moves.

## p.166 Here are some common reception problems that probably do not indicate a problem 

Here are some common reception problems that probably do not indicate a problem with your radio:
FM
Fading and drifting stations-Generally, the
effective range of FM is about 40 km (25
miles). Once outside this range, you may
notice fading and drifting, which increase
with the distance from the radio transmitter. They are often accompanied by distortion.
Multi-path-FM signals are reflective,
making it possible for two signals to reach
your antenna at the same time. If this
happens, the signals will cancel each other out, causing a momentary flutter or
loss of reception.
Static and fluttering-These occur when
signals are blocked by buildings, trees, or
other large objects. Increasing the bass
level may reduce static and fluttering.
Station swapping-If the FM signal you
are listening to is interrupted or weakened, and there is another strong station
nearby on the FM band, your radio may
tune in the second station until the original signal can be picked up again.

AM
Fading-AM broadcasts are reflected by
the upper atmosphere-especially at night.
These reflected signals can interfere with
those received directly from the radio station, causing the radio station to sound
alternately strong and weak.
Station interference-When a reflected signal and a signal received directly from a
radio station are very nearly the same
frequency, they can interfere with each
other, making it difficult to hear the broadcast.
Static-AM is easily affected by external
sources of electrical noise, such as high
tension power lines, lightening, or electrical motors. This results in static.
XM*
Alternation or modification carried out
without appropriate authorization may invalidate the user's right to operate the
equipment.
*: Use of satellite radio requires XM tuner
and service. Contact your Toyota dealer
for details.

NOTICE
This equipment has been tested and
found to comply with the limits for a
class B digital device, pursuant to
Part 15 of the FCC Rules. These limits are designed to provide reasonable
protection against harmful interference in a residential installation. This
equipment generates, uses and can
radiate radio frequency energy and, if
not installed and used in accordance
with the instructions, may cause
harmful interference to radio communications. However, there is no guarantee that interference will not occur
in a particular installation.

## p.167 If this equipment does cause harmful

If this equipment does cause harmful
interference to radio or television reception, which can be determined by
turning the equipment off and on, the
user is encouraged to try to correct
the interference by one or more of
the following measures:
-Reorient or relocate the receiving
antenna.
-Increase the separation between the
equipment and receiver.
-Connect the equipment into an outlet on a circuit different from that to
which the receiver is connected.

CARING FOR YOUR CASSETTE PLAYER
AND TAPES
For the best performance for your cassette player and tapes:
Clean the tape head and other parts regularly.
decrease sound quality and tangle your
cassette tapes. The easiest way to
clean them is by using a cleaning tape.
(A wet type is recommended.)

Use high-quality cassettes.

 Low-quality cassette tapes can cause

many problems, including poor sound,
inconsistent
playing
speed,
and
constant auto-reversing. They can also
get stuck or tangled in the cassette
player.

NOTICE

 Do not use a cassette if it has been

*Text Information includes, Channel
Name, (Artist) Name, (Song) Title and
Category Name.

ing time longer than 100 minutes (50
minutes per side). The tape used in
these cassettes is thin and could get
stuck or tangled in the cassette player.

 A dirty tape head or tape path can

-Consult the dealer or an experienced radio/TV technician for help.

This XM tuner supports "Audio Services" (Music and Talk) of only XM
satellite radio and "Text Information"*
linked to the respective audio services.

 Avoid using cassettes with a total play-

damaged or tangled or if its label is
peeling off.

 Do not leave a cassette in the player
if you are not listening to it, especially
if it is hot outside.

 Store cassettes in their cases and out
of direct sunlight.

## p.168 CARING FOR YOUR

CARING FOR YOUR
PLAYER AND DISCS

COMPACT

DISC

 The player is intended for use with 12
cm (4.7 in.) discs only.

 Extremely high temperatures can keep

your compact disc player from working.
On hot days, use the air conditioning
to cool the vehicle interior before you
listen to a disc.

 Bumpy roads or other vibrations may
make your compact disc player skip.

 If moisture gets into your compact disc

player, you may not hear any sound
even though your compact disc player
appears to be working. Remove the
disc from the player and wait until it
dries.

CAUTION
Compact disc players use an invisible
laser beam which could cause hazardous radiation exposure if directed
outside the unit. Be sure to operate
the player correctly.

 Use only compact discs marked as

Special shaped discs

shown above. The following products
may not be playable on your compact
disc player.
Copy-protected CD
CD-R (CD-Recordable)
CD-RW (CD-Re-writable)
CD-ROM

Z17058

Transparent/translucent discs

## p.169 NOTICE

NOTICE
Do not use special shaped, transparent/translucent, low quality or labeled
discs such as those shown in the illustrations. The use of such discs
may damage the player or changer, or
it may be impossible to eject the
disc.
Correct

Low quality discs

Wrong

 Handle compact discs carefully, espe-

cially when you are inserting them.
Hold them on the edge and do not
bend them. Avoid getting fingerprints
on them, particularly on the shiny side.

 Dirt, scratches, warping, pin holes, or

other disc damage could cause the
player to skip or to repeat a section of
a track. (To see a pin hole, hold the
disc up to the light.)

 Remove discs from the compact disc

Labeled discs

player when you are not listening to
them. Store them in their plastic cases
away from moisture, heat, and direct
sunlight.

## p.170 Rear seat audio system

Rear seat audio system
(b) When the radio mode is selected
"
CH
" button: Push this button to
select a preset station on the preset button of the front audio system. Each push
of the button changes to the station with
higher numbered preset button.
"
TUNE
" button: Push this button
for manual tuning or seek tuning.

 Push this button briefly. Each time you
push the button, the radio will step up
or down to another frequency.

 Push this button and hold it until you
To clean a compact disc: Wipe it with a
soft, lint-free cloth that has been dampened with water. Wipe in a straight line
from the center to the edge of the disc
(not in circles). Dry it with another soft,
lint-free cloth. Do not use a conventional
record cleaner or anti-static device.

In the rear seat, you can enjoy a different mode from the one used on the
front audio system, using headphones.
(a) Turning the system on and off
"ON/SOURCE" button: Use this button to
turn system on when the system is off.
When the system is turned on, the mode
changes by pushing this button.
"OFF" button: Use this button to turn off
the system.
"Volume adjusting" knob: Use this knob
to adjust the volume.

hear a beep. The radio will begin seeking up or down for a station, and will
stop on reception. Each time you push
the button, the stations will be
searched automatically one after another.

## p.171 (c) When the "TAPE" mode is selected

(c) When the "TAPE" mode is selected

(e) Some basics

"
PROG
" button: Push this button
to select the other side of a cassette
tape.

This system cannot be used if the audio
system is not turned on.

"
TRACK
" button: Push the left or
right side to skip forward or backward to
locate the song you want to hear. For
details, see "SEEK TRACK button" on
page 163.
(d) When the "CD" or "DVD" mode is
selected
"
DISC
" button: Use this button to
search a desired disc.
"
TRACK
" button: Use this button
to search a desired track or push this
button and hold it to fast forward or reverse.

On this system, you cannot listen to XM
satellite radio*.

CAUTION
This system is not designed for a
driver. So, the driver should not use
this system while driving.

*: Use of satellite radio requires XM tuner
and service. Contact your Toyota dealer
for details.
You cannot select "AM" or "FM" mode in
the rear seat if the "FM" or "AM" mode
is used on the front seats side.
If you select the same mode as the front
seats side, operating the controller will
affect the mode on the front seats side.
Vehicles with navigation system only:

 When the XM satellite radio* is se-

lected in the front seat, the "CD" or
"DVD" mode cannot be selected in the
rear seat.

 When the "CD" or "DVD" mode is se-

lected in the rear seat, selecting the
XM satellite radio* in the front seat will
automatically change the "CD" or
"DVD" to "AM" mode in the rear seat.

## p.172 Audio remote controls

Audio remote controls
(steering switches)
(a) When the radio mode is selected

(b) When the "TAPE" mode is selected

" " or " " switch: Push this switch for
seek tuning or to select a station.

" " or " " switch: Push this switch to
fast forward or rewind the tape or for
automatic program selection.

 To select a preset station, push the
switch briefly. Do this again to select
the next preset station.

 To seek a station, push and hold the

switch until you hear a beep. Do this
again to find the next station. If you
push the switch on either side of the
"Ɲ" or "Ɯ" during the seek mode,
seeking will be canceled.

The switches are installed on the left side
of the steering wheel.
"MODE" switch: Use this switch to
change the mode. If a tape or compact
disc is not inserted, the "TAPE" or "CD"
mode is skipped. When you push the
switch with the audio system turned off,
the audio system turns on.
"
" switches: Use this switches to adjust the volume. Push "+" to increase the
volume and "-" to decrease the volume.
The volume continues to increase or decrease while the switch is being pressed.

 To step up or down the frequency,

push and hold the switch even after
you hear a beep. When you release
from the switch, the radio will begin
seeking up or down for a station. Do
this again to find the next station.

XM satellite radio*-
To select a preset channel, push the "Ɯ"
or "Ɲ" side of the switch. Repeat until a
desired channel is found.
*: Use of satellite radio requires XM tuner
and service. Contact your Toyota dealer
for details.

 Push this switch until you hear a beep

to fast forward or rewind the tape. To
stop fast forwarding or rewinding, push
the same side on the switch until you
hear a beep.

 Push this switch briefly for automatic

program selection. When automatically
selecting a program, you can skip up
to 9 programs at a time. For details,
see "SEEK TRACK button" on page
163.

## p.173 (c) When the "CD" or "DVD" mode is

(c) When the "CD" or "DVD" mode is
selected
" " or " " switch: Use this switch to
select a desired track or disc.

 Push this switch briefly to select a desired track.

 To select a desired disc, push and hold
this switch until the desired number of
the disc appears and you hear a beep.

CAUTION
Operate the switches with due care
while you are driving to avoid accidents.

## p.174 

# Section 1-9: Air conditioning system

## p.175 SECTION

SECTION

1- 9

OPERATION OF INSTRUMENTS AND
CONTROLS
Air conditioning system
Front air conditioning system:
Controls . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 176
Air flow selector settings . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 180
Operating tips . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 181
Instrument panel vents . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 183
Rear air conditioning system:
Controls . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 184
Air flow selector settings . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 186

For vehicle equipped with Navigation system, please refer to the
separate " Navigation System Owner's Manual".

## p.176 Front air conditioning system-

Front air conditioning system-
-Controls
1. Temperature selector knob
2. "AUTO" button
3. Temperature display
4. Fan speed display
5. Air flow display
6. "MODE" button
7. "A/C" button
8. Front windshield button
9. Fan speed control button
10. Air intake control button
11. "OFF" button

## p.177 "AUTO" button

"AUTO" button
For automatic operation of the air conditioning, press the "AUTO" button. An indicator light will illuminate to show that the
automatic operation mode has been selected.
In the automatic operation mode, the air
conditioning selects the most suitable fan
speed and air flow according to the temperature.

"MAX COLD" appears when you adjust to
maximum cooling, and "MAX HOT" appears when you adjust to maximum warming.
"OFF" button
Push the button to turn off the air conditioning system.

You may use manual controls if you want
to select your own settings.
To turn off the automatic operation, press
the "MODE" or fan speed control button.

"MODE" button

Fan speed control button

Push the button to select the vents used
for air flow.

Push the "Ɯ" (increase) or "Ɲ" (decrease)
button to adjust the fan speed.
In automatic operation, you do not have
to adjust the fan speed unless you desire
another fan speed mode.
Temperature selector knob
To increase the temperature, turn the knob
to right side, to decrease it, turn the knob
to left side.

In automatic operation, you do not have
to select the air flow unless you desire
another air flow mode.
1. Panel-Air flows mainly
instrument panel vents.

from

the

2. Bi-level-Air flows from both the floor
vents and the instrument panel vents.
3. Floor-Air flows mainly from the floor
vents.
It is recommended that you close the
lower vent. For details about this, see
"Instrument panel vents" described below.

## p.178 4. Floor/Windshield-Air

4. Floor/Windshield-Air
flows
mainly
from the floor vents and windshield
vents.

When the "A/C" button is not pressed in,
pressing "MODE" button turns off the air
conditioning.

It is recommended that you close the
lower vent. For details about this, see
"Instrument panel vents" described below.

For details about air flow selector setting,
see "Air flow selector settings" described
below.

For details about air flow selector settings,
see "Air flow selector settings" described
below.

Front windshield button
When this button is pressed, air flows
mainly from the windshield vents.
Pressing the button once again returns the
air flow mode to the last one used.
Pressing the front windshield button turns
on the defroster-linked air conditioning. At
this time, the "A/C" button indicator comes
on when the air intake control is in recirculate mode regardless of whether or not
the "A/C" button is pressed in. This is to
clean up the front view more quickly.
To turn off the air conditioning alone,
press the "A/C" button once again.

## p.179 "A/C" button

"A/C" button
To turn on the air conditioning, press the
"A/C" button. The "A/C" button indicator
will come on. To turn the air conditioning
off, press the button again.
If the "A/C" button indicator flashes, there
is a problem in the air conditioning system
and the air conditioning automatically
shuts off. If this happens, take your vehicle to a Toyota dealer for service.

Air intake control button
Press the button to select the air source.
An indicator light will illuminate to show
which air intake mode is being selected.
1. Recirculate-Recirculates the air inside
the vehicle.
2. Fresh-Draws outside air into the system.

## p.180 -Air flow selector settings

-Air flow selector settings
See "Instrument panel vents" described below.

## p.181 -Operating tips

-Operating tips
 To cool off your Toyota after it has

been parked in the hot sun, drive with
the windows open for a few minutes.
This vents the hot air, allowing the air
conditioning to cool the interior more
quickly.

 Make sure the air intake grilles in front
of the windshield are not blocked (by
leaves or snow, for example).

 On humid days, do not blow cold air

on the windshield. The windshield could
fog up because of the difference in air
temperature on the inside and outside
of the windshield.

 Keep the area under the front seats

clear to allow air to circulate throughout the vehicle.

 On cold days, set the fan speed to
high for a minute to help clear the
intake ducts of snow or moisture. This
can reduce the amount of fogging on
the windows.

 If following another vehicle on a dusty

road, or driving in windy and dusty
conditions, it is recommended that the
air intake control button be temporarily
set to RECIRCULATE, which will close
off the outside passage and prevent
outside air and dust from entering the
vehicle interior.

Heating
For best results, set controls to:
Fan speed-"AUTO"
Temperature- To the desired
temperature
Air intake-FRESH (outside air)
Air flow-"AUTO"
Lower vent-CLOSED
Air conditioning-OFF

 For quick heating, select recirculated

air for a few minutes. To keep the
windows from fogging, select fresh after the vehicle interior has been warmed.

 Press the "A/C" button on for dehumidified heating.

 Choose floor/windshield air flow to heat
the vehicle interior while defrosting or
defogging the windshield.

 When driving on dusty roads, close all

windows. If dust thrown up by the vehicle is still drawn into the vehicle after
closing the windows, it is recommended
that the air intake control button be set
to FRESH and the fan speed control
button to any setting except "OFF".

## p.182 Air conditioning

Air conditioning

Defogging

Defrosting

For best results, set controls to:

The inside of the windshield

The outside of the windshield

For best results, set controls to:

For best results, set controls to:

Temperature- Towards high temperature
to heat;
low temperature to cool
Air intake-FRESH (outside air)
Air flow-WINDSHIELD
Lower vent-CLOSED

Temperature-Towards high temperature
Air intake-FRESH (outside air)
Air flow-WINDSHIELD
Lower vent-CLOSED

Fan speed-"AUTO"
Temperature- To the desired
temperature
Air intake-FRESH (outside air)
Air flow-"AUTO"

 For quick cooling, select recirculated
air for a few minutes.

Ventilation
For best results, set controls to:
Fan speed-"AUTO"
Temperature- To the desired
temperature
Air intake-FRESH (outside air)
Air flow-"AUTO"
Air conditioning-OFF

When pressing the front windshield button,
the air intake selects "Fresh" automatically. This is to clean up the front view more
quickly.
Press the "A/C" button for dehumidified
heating or cooling. This setting clears the
front view more quickly.

 On humid days, do not blow cold air

on the windshield-the difference between the outside and inside temperatures could make the fogging worse.

When pressing the front windshield button,
the air intake selects "Fresh" automatically. This is to clean up the front view more
quickly.
Press the "A/C" button for dehumidified
heating or cooling. This setting clears the
front view more quickly.

 To heat the vehicle interior while defrosting
the
windshield,
floor/windshield air flow.

choose

## p.183 -Instrument panel vents

-Instrument panel vents

Center vents

Lower vent

If air flow control is not satisfactory, check
the instrument panel vents. The instrument
panel vents may be opened or closed as
shown.
For removing frost or fog, it is recommended that you close the lower vent
when you use the "Floor", the "Floor/Windshield" or the "Windshield" mode.

Side vents

## p.184 Rear air conditioning system-

Rear air conditioning system-
-Controls
1. Rear air conditioning on-off switch
2. "AUTO" button
3. Air flow selector
4. Fan speed selector
5. Temperature selector
6. "OFF" button
## p.185 Rear air conditioning on-off switch

Rear air conditioning on-off switch
To turn the rear air conditioning on, press
the "REAR" switch. To turn the rear air
conditioning off, press the switch again.
"AUTO" button
For automatic operation of the rear air
conditioning, press the "AUTO" button. An
indicator light will illuminate to show that
the automatic operation mode has been
selected.
In the automatic operation mode, the rear
air conditioning selects the most suitable
fan speed and air flow according to the
temperature.
You may use manual controls if you want
to select your own settings.
Fan speed selector
Press the buttons to adjust the fan speed.
In automatic operation, you do not have
to adjust the fan speed unless you desire
another fan speed mode.

Temperature selector
Move the lever to adjust the temperature-to the right to warm, to the left to
cool.
"OFF" button
Push the button to turn off the rear air
conditioning system.

Air flow selector
Press one of the buttons to select the
vents used for air flow. An indicator light
will illuminate to show which air flow
mode is being selected.
In automatic operation, you do not have
to select the air flow unless you desire
another air flow mode.
1. Panel-Air flows mainly from the roof
vents.
2. Bi-level-Air flows from both the floor
vents and the roof vents.
3. Floor-Air flows mainly from the floor
vents.
Air at higher than room temperature does
not flow from the roof vents.

## p.186 -Air flow selector settings

-Air flow selector settings
Warm air
Cool air

# Section 1-10: Other equipment

## p.187 SECTION

SECTION

1- 10

OPERATION OF INSTRUMENTS AND
CONTROLS
Other equipment
Clock . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 188
Outside temperature display . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 188
Rear view monitor system . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 189
Cigarette lighter and ashtray . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 192
Power outlets . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 192
Roll sensing of curtain shield airbags off switch . . . . . . . . . . . . . . . . 193
Rear console box . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 194
Glove box . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 195
Garage door opener . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 195
Auxiliary boxes . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 198
Cup holders . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 199
Card holder . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 201
Tie-down hooks . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 201
Cargo net hooks . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 202
Roof luggage carrier . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 202
Floor mat . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 204
Coat hooks . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 205

## p.188 Clock

Clock

Outside temperature display
When the instrument panel lights are
turned on, the brightness of the time indication will be reduced.

To reset the hour: Push the "H" button.
To reset the minutes: Push the "M" button.

The display indicates between the range
of -22°F and 122°F.

The key must be in the "ACC" or "ON"
position.

The key must be in the "ON" position.

If quick adjustment to a full hour is desired, push the ":00" button.
For example, if the ":00" button is depressed when the time is between
1:01 - 1:29, the time will change to 1:00.
If the time is between 1:30 - 1:59, the
time will change to 2:00.
If the electrical power source has been
disconnected from the clock, the time display will automatically be set to 1:00 (one
o'clock).

## p.189 Rear view monitor system

Rear view monitor system
The rear view monitor system assists
the driver by displaying an image of
the rear of the vehicle while backing
up. The displayed image on the screen
is a horizontally reversed mirror image
of the inside rear view mirror.

 Never depend on the rear view

To display the rear view image on the
screen, place the selector lever in the
"R" position when the ignition switch
in the "ON" position.

Use caution just as you would when
backing up any vehicle.

If you move the selector lever out of the
"R" position, the screen returns to the
previous screen. Operating another function of the navigation system will display
another screen.
The rear view monitor system is a supplement device intended to assist back up.
When backing up, be sure to check behind and all around the vehicle visually.

CAUTION
monitor system entirely when backing up. Always make sure your intended path is clear.

 Never back up while looking only at
the screen. The image on the
screen is different from actual conditions. Depicted distances between
objects and flat surfaces will differ
from actual distances. If you back
up while looking only at the screen,
you may hit a vehicle, a person or
an object. When backing up, be
sure to check behind and all around
the vehicle visually and with mirrors before proceeding.

 Do not use the system when the
back door is not completely closed.

 If the back of the vehicle is hit, the
position and mounting angle of the
camera may change. Be sure to
have the camera's position and
mounting angle checked at your
Toyota dealer.

 If the temperature changes rapidly,
such as when hot water is poured
on the vehicle in cold weather, the
system may not operate normally.

 If the camera lens becomes dirty, it
cannot transmit a clear image. If
water droplets, snow, or mud adhere to the lens, rinse with water
and wipe with a soft cloth. If the
lens is extremely dirty, wash it with
a mild cleanser and rinse.

 The displayed image may become
darker and moving images may be
slightly distorted when the system
is cold. When backing up, be sure
to check behind and all around the
vehicle visually and with mirror before proceeding.
When replacing the tires, please consult
your Toyota dealer. If you replace the
tires, the area displayed on the screen
may change.

## p.190  The area detected by the camera is

 The area detected by the camera is

AREA DISPLAYED ON SCREEN

limited. Objects which are close to
either corner of the bumper or under
the bumper cannot be seen on the
screen.

Image is displayed approximately level
on screen.

 The area displayed on the screen
may vary according to vehicle orientation or road conditions.

On screen

Check surroundings for safety.

Corners of bumper

## p.191  When water droplets are adhering to

 When water droplets are adhering to

the camera, or when humidity is high
(for example, when it rains)

 When foreign matter

(for example,
snow or mud) adheres to the camera
lens

 When the sun or the beam of head-

lights is shining directly into the camera lens

Check surroundings for safety.

THE REAR
CAMERA

VIEW

MONITOR

SYSTEM

The rear view monitor system camera is
located on the back door as shown in the
illustration. The camera uses a special
lens. The distance of the image that appears on the screen differs from the actual distance.
In the following cases, it may become
difficult to see the images on the screen,
even when the system is functioning.

If a bright light (for example, sunlight reflected off the vehicle body) is picked up
by the camera, the smear effect∗ peculiar
to the camera may occur.
∗: Smear effect-A phenomenon that occurs when a bright light (for example, sunlight reflected off the vehicle body) is
picked up by the camera; when transmitted by the camera, the light source
appears to have a vertical streak above
and below it.

 In the dark (for example, at night)
 When the temperature near the lens is
extremely high or low

## p.192 Cigarette lighter and ashtray

Cigarette lighter and ashtray

Power outlets
ASHTRAY
To use the ashtray, pull it out.
When finished with your cigarette, thoroughly extinguish it in the ashtray to prevent other cigarette butts from catching
fire. After using the ashtray, push it back
in completely.
To remove the ashtray, press down on the
lock spring plate and pull out.

CAUTION
CIGARETTE LIGHTER
To use the cigarette lighter, press it in.
After it finishes heating up, it automatically pops out ready for use.
If the engine is not running, the key must
be in the "ACC" position to use the lighter.
Do not hold the cigarette lighter pressed
in.
Use a Toyota genuine cigarette lighter or
equivalent for replacement.

To reduce the chance of injury in
case of an accident or sudden stop
while driving, always close the ashtray completely after use.

The power outlets are designed for
power supply for car accessories. To
use them, open the lids as shown in
the following illustrations.
The key must be in the "ACC" or "ON"
position to be used.

NOTICE
z To prevent the fuse from being
blown, do not use the electricity
over the total vehicle capacity of
12V/120W (all the outlets together).
z To prevent the battery from being
discharged, do not use the power
outlets longer than necessary when
the engine is not running.
z Close the power outlet lids when
the power outlets are not in use.
Inserting anything other than an appropriate plug that fits the outlet,
or allowing any liquid to get into
the outlet may cause electrical failure or short circuits.

## p.193 Roll sensing of curtain shield

Roll sensing of curtain shield
airbags off switch

Instrument panel

Rear console box
(Vehicles with navigation system)

The roll sensing of curtain shield airbags
off switch can turn off the curtain
shield airbags and front seat belt pretensioners in a vehicle rollover. This
switch should only be used in a situation where the inflation is not desired
(such as extreme off-road driving).
When you push the roll sensing of curtain
shield airbags off switch for a few seconds
with the ignition switch on, the roll sensing of curtain shield airbags off indicator
light comes on and the roll sensing function is turned off. When you push the
switch again, the indicator light goes off
and the roll sensing function is turned on.

Rear console box
(Vehicles without navigation system)

Luggage compartment

## p.194 Rear console box

Rear console box
In a severe side impact, the curtain shield
airbags on impacted side will inflate even
if the roll sensing function is turned off.
If the ignition switch is turned to "ACC" or
"LOCK" with the roll sensing function off
and then the ignition switch is turned back
to "ON", the roll sensing function will be
back on automatically.
For details, "Front seat belt pretensioners"
on page 55 or "SRS side airbags and
curtain shield airbags with roll sensing
function" on page 65.

CAUTION

 Make sure the roll sensing of curtain shield airbags off indicator light

is not on.

 When the roll sensing of curtain
shield airbags off switch is turned
on (and the roll sensing of curtain
shield airbags off indicator light is
on), the curtain shield airbags and
front seat belt pretensioners will
not inflate in a vehicle rollover and
turning off the curtain shield airbags can reduce the occupant
protection which your vehicle safety
systems can provide to you in certain accidents and increase the likelihood of death or serious injuries.

To use the rear console box, open as
shown in the illustration.
1. For upper box
2. For lower box

## p.195 Glove box

Glove box

Garage door opener
Buttons
Indicator
light

The battery side of the hand-held transmitter must be pointed away from the
HomeLink during the programming process.
For Canadian users, follow the procedure
in "Programming an entrance gate/Programming all devices in the Canadian
market".
1. Decide which of 3 HomeLink buttons
you want to program. Push and hold
down one of the buttons until the indicator corresponding to the selected
channel begins to flash.

To use the glove box, do this.
To open: Pull the lever.
With the instrument panel lights on, the
glove box light will come on when the
glove box is open.
To lock: Insert the master key and turn it
clockwise.

CAUTION
To reduce the chance of injury in
case of an accident or a sudden stop,
always keep the glove box door
closed while driving.

The garage door opener (HomeLink
Universal Transceiver) is manufactured under license from HomeLink and can be
programmed to operate garage doors,
gates, entry doors, door locks, home lighting systems, and security systems, etc.
(a) Programming the HomeLink
The HomeLink in your vehicle has 3
buttons and you can store one program
for each button.
To ensure correct programming into the
HomeLink, install a new battery in the
hand-held transmitter prior to programming.

2. Place your hand-held garage transmitter 25 to 75 mm (1 to 3 in.) away from
the surface of the HomeLink.
Keep the indicator light on the
HomeLink in view while programming.
3. Simultaneously press and hold the
hand-held garage transmitter button
along with the selected HomeLink button.
4. When the indicator light on the
HomeLink changes from a slow to a
rapid flash after 20 seconds, you can
release both buttons.

## p.196 5. Test the operation of the HomeLink by

5. Test the operation of the HomeLink by
pressing the newly programmed button.
If programming a garage door opener,
check to see if the garage door opens
and closes.
If the garage door does not operate,
identify if your garage transmitter is of
the "Rolling Code" type. Press and hold
the programmed HomeLink button.
The garage door has the rolling code
feature if the indicator light (on the
HomeLink) flashes rapidly and then
remains lit after 2 seconds.
If your
garage transmitter is the "Rolling Code"
type, proceed to the heading "Programming a rolling code system".
6. Repeat steps 2 through 5 for each remaining HomeLink button to program
another device.
Programming a rolling code system
If your device is "Rolling Code"
equipped, it is necessary to follow
steps 1 through 4 under the heading
"Programming the HomeLink" before
proceeding with the steps listed below.

1. Locate the "training" button on the ceiling mounted garage door opener motor.
The exact location and color of the
button may vary by brand of garage
door opener. Refer to the owner's
guide supplied by the garage door
opener manufacturer for the location of
this "training" button.
2. Press the "training" button on the ceiling mounted garage door opener motor.
Following this step, you have 30 seconds in which to initiate step 3 below.
3. Press and release the vehicle's programmed HomeLink button twice.
The garage door may open. If the door
does open, the programming process is
complete. If the door does not open,
press and release the button a third
time. This third press and release will
complete the programming process by
opening the garage door.

Programming an entrance gate/Programming all devices in the Canadian market
1. Decide which of the 3 HomeLink buttons you want to program.
2. Place
your
hand-held gate/device
transmitter 25 to 75 mm (1 to 3 in.)
away
from
the
surface
of
the
HomeLink.
Keep the indicator light on the
HomeLink in view while programming.
3. Press
and
hold
HomeLink button.

the

selected

4. Continuously press and release (cycle)
the hand-held gate/device transmitter
button every two seconds until step 5
is complete.
5. When the indicator light on the
HomeLink changes from a slow to a
rapid flash after 20 seconds, you can
release both buttons.

The ceiling mounted garage door opener motor should now recognize the
HomeLink unit and be able activate
the garage door up/down.

6. Test the operation of the HomeLink by
pressing the newly programmed button.
Check to see if the gate/device operates correctly.

4. Repeat steps 1 through 3 for each remaining HomeLink button to program
another rolling code system.

7. Repeat steps 1 through 6 for each remaining HomeLink button to program
another device.

## p.197 Programming other devices

Programming other devices
To program other devices such as home
security systems, home door locks or
lighting, contact your authorized Toyota
dealer for assistance.
Reprogramming a button
Individual HomeLink
buttons cannot be
erased, however, to reprogram a single
button, follow the procedure "Programming
the HomeLink".
(b) Operating the HomeLink
To operate the HomeLink, press the appropriate HomeLink button to activate the

programmed device. The HomeLink indicator
light
should
come
on.
The
HomeLink continues to send the signal
for up to 20 seconds as long as the button is pressed.
(c) Erasing
the
entire
HomeLink
memory (all three programs)
To erase all previously programmed codes
at one time, press and hold down the 2
outside buttons for 20 seconds until the
indicator light flashes.

CAUTION

 When programming the HomeLink
Universal Transceiver, you may be
operating a garage door or other
device. Make sure people and objects are out of the way of the garage door or other device to prevent potential harm or damage.

 Do not use this HomeLink Universal Transceiver with any garage
door opener that lacks the safety
stop and reverse feature as required by federal safety standards.
(This includes any garage door
opener model manufactured before
April 1, 1982.) A garage door opener which cannot detect an object
(signaling the door to stop and reverse), does not meet current federal safety standards. Using a garage
door opener without these features
increases risk of serious injury or
death.

This device complies with Part 15 of the
FCC Rules and with RSS-210 of the IC
Rules. Operation is subject to the following two conditions: (1) This device
may not cause harmful interference, and
(2) this device must accept any interference received, including interference
that may cause undesired operation.
WARNING: This transmitter has been
tested and complies with FCC and IC
Rules. Changes or modifications not
expressly approved by the party responsible for compliance could void
the user's authority to operate the
device.

If you sell your vehicle, be sure to erase
the programs stored in the HomeLink
memory.

## p.198 Auxiliary boxes-

Auxiliary boxes-
To use the auxiliary boxes, open the
lids as shown in the following illustrations.

CAUTION
To reduce the chance of injury in
case of an accident or a sudden stop,
always keep the auxiliary box closed
while driving.

NOTICE
Auxiliary boxes on the ceiling-In hot
weather, inside of the vehicle ceiling
becomes very hot. Do not leave anything flammable or deformable such
as a lighter, the glasses, etc. inside.

Type A (luggage compartment)

Type B (luggage compartment)

Type C (rear console)

## p.199 -First-aid kit holder

-First-aid kit holder

-Warning reflector holder

Cup holders
The cup holder is designed for holding
cups or drink-cans securely. To use
them, observe the following illustrations.

CAUTION

 Do not place anything else other
than cups or drink-cans in the cup
holder, as such items may be
thrown about in the compartment
and possibly injure people in the
vehicle during a sudden braking or
an accident.
An auxiliary box is equipped with a
band to hold the first-aid kit.

An auxiliary box is equipped with a
band to hold the warning reflector.

Although the first-aid kit itself is not included as an original equipment, this auxiliary box can be used to store the first-
aid kit.

Although the warning reflector itself is not
included as an original equipment, this
auxiliary box can be used to store the
warning reflector.

Hold the first-aid kit with a band.

Hold the warning reflector kit with a band.

Make sure the first-aid kit is securely
held.

Make sure the warning reflector is securely held.

 To reduce the chance of injury in
case of an accident or a sudden
stop while driving, keep the cup
holder closed when it is not in use.

## p.200 For front seats

For front seats

For front seat

The cup holder can be adjusted to the
size of cups by changing the separator
position or moving the separator arms.

To use a cup holder in the console box.

You can use it as an accessory box by
removing the separator inside.

For second seats

1. Open the console box lid. Pull down
the knob so that the cup holder swings
down.
2. While holding the console box lid with
your hand, push down the cup holder
to be secured.

NOTICE
z When you use the cup holder in the
console box, make sure it is securely locked.
z Do not rest your arm on the cup
holder in the console box.
z Wipe up spilt drink at once.

For third seats (right-hand side)

## p.201 For third seats (left-hand side)

For third seats (left-hand side)

Card holder

Tie-down hooks

You can store a card in the slot as
shown in the illustration.

To secure your luggage, use the tie-
down hooks as shown above.
See "Cargo and luggage" on page 230 for
precautions when loading luggage.

NOTICE
Do not use the seat anchors instead
of the tie-down hooks.

## p.202 Cargo net hooks

Cargo net hooks

Roof luggage carrier
Side
knobs

Cross
rails
Upper
knob

Roof rails

These hooks are designed to hang cargo net.
To hang the cargo net, use the cargo net
hooks and rear tie-down hooks.
Although the cargo net itself is not included as an original equipment, these
hooks can be used to hang the cargo net.

NOTICE
To prevent damage to the hook, avoid
hanging things other than a cargo net
on it.

The roof luggage carrier consists of
roof rails and sliding cross rails.

ADJUSTING THE POSITION OF CROSS
RAILS:
1. Turn the upper and side knobs counterclockwise to loosen the cross
rails.

## p.203 Follow the manufacture's instructions and

Follow the manufacture's instructions and
precautions when installing the attachments or their equivalent.

CAUTION
When you load cargo on the roof luggage carrier, observe the following:

 Place the cargo so that its weight
is distributed evenly between the
front and rear axles.

 If loading long or wide cargo, never
2. Slide the cross rails to the appropriate position for loading the luggages
and turn the side knobs clockwise to
tighten the cross rails securely.
There are cross rail stoppers on the roof
rails which help you prevent the cross
rails being touched with the tilted up moon
roof.

NOTICE
Do not remove the cross rail stoppers, or the moon roof may be damaged when it is tilted.

3. In order to fix the cross rails to the
appropriate length, turn the upper
knobs clockwise after tightening all
of the side knobs.

exceed the vehicle overall length or
width.
(See
"Dimensions
and
weights" on page 324 for information on your vehicle overall length
and width.)

 Before driving, make sure the cargo

CAUTION

is securely fastened on the roof
luggage carrier.

Make sure the cross rails are fixed
securely by pushing forward and rearward them. Failure to do so may
cause an unexpected accident or severe injury in the event of emergency
braking or a collision.

 Loading cargo on the roof luggage
carrier will make the center of the
vehicle gravity higher. Avoid high
speeds, sudden starts, sharp turns,
sudden braking or abrupt maneuvers, otherwise it may result in loss
of control or vehicle rollover due to
failure to operate this vehicle correctly.

## p.204 Floor mat

Floor mat
 If driving for a long distance, on
rough roads, or at high speeds,
stop the vehicle now and then during the trip to make sure the cargo
remains in its place.

 Do not exceed 70 kg (154 lb.) cargo
weight on the roof luggage carrier.

NOTICE
When loading the luggages, be careful
not to scratch the surface of the
moon roof.

Use a floor mat of the correct size.
If the floor carpet and floor mat have a
hole, then it is designed for use with a
locking clip. Fix the floor mat with locking
clip into the hole in the floor carpet.

CAUTION
Make sure the floor mat is properly
placed on the floor carpet. If the floor
mat slips and interferes with the
movement of the pedals during driving, it may cause an accident.

## p.205 Coat hooks

Coat hooks

To use the coat hook, push the hook.

CAUTION
Do not hook a hanger, heavy or sharp
pointed object on the coat hook. If
the curtain shield airbags inflate,
those items will be hurled away with
great force or the curtain shield airbags may not active correctly. When
you hang clothes, hang them on the
coat hook directly.

## p.206 

# Section 2: Information before driving your Toyota

## p.207 SECTION

SECTION

2

INFORMATION BEFORE DRIVING
YOUR TOYOTA
Off-road vehicle precautions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 208
Break-in period . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 209
Fuel . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 209
Fuel pump shut off system . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 211
Operation in foreign countries . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 211
Three-way catalytic converter . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 212
Engine exhaust cautions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 213
Facts about engine oil consumption . . . . . . . . . . . . . . . . . . . . . . . . . . 214
Iridium-tipped spark plugs . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 215
Brake system . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 215
Brake pad wear limit indicators . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 219
Rear step bumper . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 219
Limited-slip differential . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 220
Your Toyota's identification . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 220
Theft prevention labels . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 221
Suspension and chassis . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 221
Tire information . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 222
Vehicle load limits . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 230
Cargo and luggage . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 230
Types of tires . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 233

## p.208 Off-road vehicle precautions

Off-road vehicle precautions
This vehicle belongs to the utility vehicle class, which has higher ground
clearance and narrower tread in relation
to the height of its center of gravity to
make it capable of performing in a wide
variety of off-road applications. Specific design characteristics give it a higher center of gravity than ordinary passenger cars.
This vehicle design
feature causes this type of vehicle to
be more likely to rollover. And, utility
vehicles have a significantly higher rollover rate than other types of vehicles.
An advantage of the higher ground
clearance is a better view of the road
allowing you to anticipate problems. It
is not designed for cornering at the
same speeds as ordinary passenger
cars any more than low-slung sports
cars designed to perform satisfactorily
under off-road conditions.
Therefore,
sharp turns at excessive speeds may
cause rollover.

CAUTION
Always observe the following precautions to help minimize the risk of serious personal injury or damage to
your vehicle:

 In a rollover crash, an unbelted person is significantly more likely to
die than a person wearing a seat
belt. Therefore, the driver and all
passengers should fasten their seat
belts whenever the vehicle is moving.

 Avoid sharp turns or abrupt maneuvers, if at all possible. Failure to
operate this vehicle correctly may
result in loss of control or vehicle
rollover causing death or serious
injury.

 Loading cargo on the roof luggage
carrier will make the center of the
vehicle gravity higher. Avoid high
speeds, sudden starts, sharp turns,
sudden braking or abrupt maneuvers, otherwise it may result in loss
of control or vehicle rollover due to
failure to operate this vehicle correctly.

## p.209  Always slow down in gusty crosswinds. Because of its profile and

 Always slow down in gusty crosswinds. Because of its profile and
higher center of gravity, your vehicle is more sensitive to side
winds than an ordinary passenger
car. Slowing down will allow you
to have better control.

 When driving off-road or in rugged
terrain, do not drive at excessive
speeds, jump, make sharp turns,
strike objects, etc. This may cause
loss of control or vehicle rollover
causing death or serious injury.
You are also risking expensive damage to your vehicle's suspension
and chassis.

 Do not drive horizontally across
steep slopes.
Driving straight up
or straight down is preferred. Your
vehicle (or any similar off-road vehicle) can tip over sideways much
more easily than forward or backward.

Break-in period

Fuel

Drive gently and avoid high speeds.

FUEL TYPE

Your vehicle does not need an elaborate
break-in. But following a few simple tips
for the first 1600 km (1000 miles) can add
to the future economy and long life of
your vehicle:

Your new vehicle must use only unleaded gasoline.

 Avoid full-throttle acceleration when
starting and driving.

 Avoid racing the engine.
 Try to avoid hard stops during the first

To help prevent gas station mix-ups, your
Toyota has a smaller fuel tank opening.
The special nozzle on pumps with unleaded fuel will fit it, but the larger standard nozzle on pumps with leaded gas will
not.

 Do not drive for a long time at any

At a minimum, the gasoline you use
should meet the specifications of ASTM
D4814 in the U.S.A. and CGSB 3.5-M93
in Canada.

 Do not tow a trailer during the first 800

NOTICE

300 km (200 miles).

single speed, either fast or slow.
km (500 miles).

Do not use leaded gasoline. Use of
leaded gasoline will cause the three-
way catalytic converter to lose its effectiveness, the emission control system to function improperly, and damage to the engine. Also, this can increase maintenance costs.

## p.210 OCTANE RATING

OCTANE RATING
Select Octane Rating 87 (Research Octane Number 91) or higher. For improved vehicle performance, the use of
premium unleaded gasoline with an Octane Rating of 91 (Research Octane
Number 96) or higher is recommended.
Use of unleaded gasoline with an octane
rating or research octane number lower
than stated above will cause persistent
heavy knocking. If it is severe, this will
lead to engine damage.
If your engine knocks...
If you detect heavy knocking even when
using the recommended fuel, or if you
hear steady knocking while holding a
steady speed on level roads, consult your
Toyota dealer.
However, occasionally, you may notice
light knocking for a short time while accelerating or driving up hills. This is normal
and there is no need for concern.

GASOLINE CONTAINING DETERGENT
ADDITIVES
Toyota recommends the use of gasoline
that contains detergent additives to
avoid build-up of engine deposits.
However, all gasoline sold in the U.S.
contains detergent additives to keep clean
and/or clean intake systems.

QUALITY GASOLINE
Automotive manufacturers in the U.S.,
Europe and Japan have developed a
specification for quality fuel named
World-Wide Fuel Charter (WWFC) that
is expected to be applied world wide.
The WWFC consists of four categories
that depend on required emission levels. In the U.S., category 3 has been
adopted. The WWFC improves air quality by providing for better emissions in
vehicle fleets, and customer satisfaction
through better vehicle performance.

CLEANER BURNING GASOLINE
Cleaner burning gasoline, including reformulated gasoline that contains oxygenates such as ethanol or MTBE is
available in many areas.

Toyota recommends the use of cleaner
burning gasoline and appropriately blended
reformulated gasoline. These types of gasoline provide excellent vehicle performance, reduce vehicle emissions, and improve air quality.

OXYGENATES IN GASOLINE
Toyota allows the use of oxygenate
blended gasoline where the oxygenate
content is up to 10% ethanol or 15%
MTBE. If you use gasohol in your Toyota,
be sure that it has an octane rating no lower than 87.
Toyota does not recommend the use of
gasoline containing methanol.

GASOLINE CONTAINING MMT
Some gasoline contain an octane enhancing additive called MMT (Methylcyclopentadienyl Manganese Tricarbonyl).
Toyota does not recommend the use of
gasoline that contains MMT. If fuel containing MMT is used, your emission control system may be adversely affected.
The Malfunction Indicator Lamp on the instrument cluster may come on. If this happens, contact your Toyota dealer for service.

## p.211 GASOLINE QUALITY

GASOLINE QUALITY
In a very few cases, you may experience
driveability problems caused by the particular gasoline that you are using. If you
continue to have unacceptable driveability,
try changing gasoline brands. If that does
not rectify your problem, then consult your
Toyota dealer.

Fuel pump shut off system

Operation in foreign countries

The fuel pump shut off system stops supplying fuel to the engine when the engine
stalls or an airbag inflates upon collision.
To restart the engine after the fuel pump
shut off system activates, turn the ignition
switch to "ACC" or "LOCK" once and start
it.

If you plan to drive your Toyota in
another country...
First, comply with the vehicle registration
laws.
Second, confirm the availability of the
correct fuel (unleaded and minimum octane number).

CAUTION

NOTICE
z Do not use gasohol other than
stated above. It will cause fuel system damage or vehicle performance
problems.
z If drive ability problems are occur
(poor hot starting, vaporizing, engine knock, etc.), discontinue the
use.

Inspect the ground under the vehicle
before restarting the engine. If you
find that liquid has leaked onto the
ground, it is the fuel system has
been damaged and it is in need of
repair. In this case, do not restart the
engine.

z Take care not to spill gasohol during refueling. Gasohol may cause
paint damage.
FUEL TANK CAPACITY
96 L (25.4 gal., 21.1 Imp.gal.)

## p.212 Three-way catalytic converter

Three-way catalytic converter
 Do not idle or park your vehicle

The three-way catalytic converter is the
emission control devices installed in
the exhaust system.
Its purpose is to reduce pollutants in the
exhaust gas.

CAUTION

 Keep people and combustible materials away from the exhaust pipe
while the engine is running. The
exhaust gas is very hot.

z Avoid racing the engine.

over anything that might burn easily such as grass, leaves, paper or
rags.

z Do not push-start or pull-start your
vehicle.

NOTICE

z Keep your engine in good running
order. Malfunctions in the engine
electrical system, electric ignition
system or fuel system could cause
an extremely high three-way catalytic converter temperature.

A large amount of unburned gases
flowing into the three-way catalytic
converter may cause it to overheat
and create a fire hazard. To prevent
this and other damage, observe the
following precautions:
z Use only unleaded gasoline.
z Do not drive with an extremely low
fuel level; running out of fuel could
cause the engine to misfire, creating an excessive load on the three-
way catalytic converter.
z Do not allow the engine to run at
idle speed for more than 20 minutes.

z Do not turn off the ignition while
the vehicle is moving.

z If the engine becomes difficult to
start or stalls frequently, take your
vehicle in for a check-up as soon
as possible. Remember, your Toyota
dealer knows your vehicle and its
three-way catalytic converter system best.

## p.213 Engine exhaust cautions

Engine exhaust cautions
z To ensure that the three-way catalytic converter and the entire emission control system operate properly, your vehicle must receive the
periodic inspections required by the
Toyota Maintenance Schedule. For
scheduled maintenance information,
refer to the "Scheduled Maintenance
Guide" or "Owner's Manual Supplement".

CAUTION

 Avoid inhaling the engine exhaust.
It contains carbon monoxide, which
is a colorless and odorless gas. It
can cause unconsciousness or even
death.

 Make sure the exhaust system has
no holes or loose connections. The
system should be checked from
time to time. If you hit something,
or notice a change in the sound of
the exhaust, have the system
checked immediately.

 Do not run the engine in a garage

 Keep the back door and quarter
windows closed while driving. An
open or unsealed back door and
quarter windows may cause exhaust
gases to be drawn into the vehicle.

 To allow proper operation of your
vehicle's ventilation system, keep
the inlet grilles in front of the windshield clear of snow, leaves, or other obstructions.

 If you smell exhaust fumes in the
vehicle, drive with the windows
open and the back door closed.
Have the cause immediately located
and corrected.

or enclosed area except for the
time needed to drive the vehicle in
or out. The exhaust gases cannot
escape, making this a particularly
dangerous situation.

 Do not remain for a long time in a
parked vehicle with the engine running. If it is unavoidable, however,
do so only in an unconfined area
and adjust the heating or cooling
system to force outside air into the
vehicle.

## p.214 Facts about engine oil

Facts about engine oil
consumption
FUNCTIONS OF ENGINE OIL
Engine oil has the primary functions of
lubricating and cooling the inside of the
engine, and plays a major role in maintaining the engine in proper working order.
ENGINE OIL CONSUMPTION
It is normal that an engine should consume some engine oil during normal
engine operation. The causes of oil
consumption in a normal engine are as
follows.

 Oil is used to lubricate pistons, piston

rings and cylinders. A thin film of oil
is left on the cylinder wall when a piston moves downwards in the cylinder.
High negative pressure generated when
the vehicle is decelerating sucks some
of this oil into the combustion chamber.
This oil as well as some part of the oil
film left on the cylinder wall is burned
by the high temperature combustion
gases during the combustion process.

 Oil is also used to lubricate the stems

As an example, if a vehicle is used for
repeated short trips, and consumes a normal amount of oil, the dipstick may not
show any drop in the oil level at all, even
after 1000 km (600 miles) or more. This
is because the oil is gradually becoming
diluted with fuel or moisture, making it
appear that the oil level has not changed.

The amount of engine oil consumed depends on the viscosity of the oil, the
quality of the oil and the conditions the
vehicle is driven under.

The diluting ingredients evaporate out
when the vehicle is then driven at high
speeds, as on an expressway, making it
appear that oil is excessively consumed
after driving at high speeds.

of the intake valves. Some of this oil
is sucked into the combustion chamber
together with the intake air and is
burned along with the fuel. High temperature exhaust gases also burn the
oil used to lubricate the exhaust valve
stems.

More oil is consumed by high-speed driving and frequent acceleration and deceleration.
A new engine consumes more oil, since
its pistons, piston rings and cylinder walls
have not become conditioned.
Oil consumption: Max. 1.0 L per 1000
km (1.1 qt./600 miles, 0.9 Imp.qt/600
miles)
When judging the amount of oil consumption, note that the oil may become
diluted and make it difficult to judge
the true level accurately.

IMPORTANCE OF ENGINE OIL LEVEL
CHECK
One of the most important points in proper vehicle maintenance is to keep the engine oil at the optimum level so that oil
function will not be impaired. Therefore, it
is essential that the oil level be checked
regularly. Toyota recommends that the oil
level be checked every time you refuel
the vehicle.

NOTICE
Failure to check the oil level regularly
could lead to serious engine trouble
due to insufficient oil.

## p.215 Iridium-tipped spark plugs

Iridium-tipped spark plugs
For detailed information on oil level check,
see "Checking the engine oil level" on
page 296.

Brake system
BRAKE SYSTEM
This brake system has two independent
hydraulic circuits. If either circuit should
fail, the other will still work. However, the
pedal will be harder to press, and your
stopping distance will increase. Also, the
brake system warning light may come on.

CAUTION
Do not drive your vehicle with only a
single brake system. Have your
brakes fixed immediately.
Your engine is fitted with iridium-tipped
spark plugs.

NOTICE
Use only iridium-tipped spark plugs
and do not adjust gaps for your engine performance and smooth drivability.

BRAKE BOOSTER
The brake booster uses brake fluid pressurized by the pump to power-assist the
brakes. If the brake booster fails during
driving, the brake system warning light
comes on and buzzer sound continuously.
In this case, the brakes may not work
properly. If they do not work well, depress
the brake pedal firmly. If the brake system
warning light comes on, immediately stop
your vehicle and contact your Toyota dealer.

## p.216 The brake system warning light may stay

The brake system warning light may stay
on for about 60 seconds after the ignition
key is turned to "ON" position. It is normal if the light turns off after a while.
Depressing the brake pedal repeatedly
may turn on the brake system warning
light and buzzer. It is normal if the light
turns off and the buzzer stops sounding
after a few seconds.
You may hear a small sound in the engine
compartment after the engine is started or
the brake pedal is depressed repeatedly.
This is a pump pulsating sound of the
brake system, and it is not a malfunction.

CAUTION

 Do not pump the brake pedal if the
engine stalls. Each push on the
pedal uses up your brake fluid
pressure reserve.

 Even if the power assist is completely lost, the brakes will still
work. But you will have to push the
pedal hard, much harder than normal. And your braking distance will
increase.

ANTI-LOCK BRAKE SYSTEM
(with "ABS" warning light)
The anti-lock brake system is designed
to automatically help prevent lock-up of
the wheels during a sudden braking or
braking on slippery road surfaces. This
assists in providing stability and steering performance of the vehicle under
these circumstances.
Effective way to press the ABS brake
pedal: When the anti-lock brake system
function is in action, you may feel the
brake pedal pulsating and hear a noise.
In this situation, to let the anti-lock
brake system work for you, just hold the
brake pedal down more firmly. Do not
pump the brake in a panic stop. This
will result in reduced braking performance.
The anti-lock brake system becomes operative after the vehicle has accelerated
to a speed in excess of approximately 10
km/h (6 mph). It stops operating when the
vehicle decelerates to a speed below
approximately 5 km/h (3 mph).

Depressing the brake pedal on slippery
road surfaces such as on a manhole cover, a steel plate at a construction site,
joints in a bridge, etc. on a rainy day
tends to activate the anti-lock brake system.
You may hear a click or motor sound in
the engine compartment for a few seconds
when the engine is started or just after
the vehicle begins to move. This means
that the anti-lock brake system is in the
self check mode, and does not indicate a
malfunction.
When the anti-lock brake system is activated, the following conditions may
occur. They do not indicate a malfunction of the system:

 You may hear the anti-lock brake sys-

tem operating and feel the brake pedal
pulsating and the vibrations of the body
and steering wheel. You may also hear
the motor sound in the engine compartment even after the vehicle is stopped.

 At the end of the anti-lock brake system activation, the brake pedal may
move a little forward.

## p.217 CAUTION

CAUTION
Do not overestimate the anti-lock
brake system: Although the anti-lock
brake system assists in providing vehicle control, it is still important to
drive with all due care and maintain
a moderate speed and safe distance
from the vehicle in front of you, because there are limits to the vehicle
stability and effectiveness of steering
wheel operation even with the anti-
lock brake system on.
If tire grip performance exceeds its
capability, or if hydroplaning occurs
during high speed driving in the rain,
the anti-lock brake system does not
provide vehicle control.

Anti-lock brake system is not designed to shorten the stopping distance: Always drive at a moderate
speed and maintain a safe distance
from the vehicle in front of you.
Compared with vehicles without an
anti-lock brake system, your vehicle
may require a longer stopping distance in the following cases:

 Driving on rough, gravel or snow-
covered roads.

 Driving with tire chains installed.
 Driving over the steps such as the
joints on the road.

 Driving on roads where the road
surface is pitted or has other differences in surface height.
Install all 4 tires of specified size at
appropriate pressure: The anti-lock
brake system detects vehicle speeds
using the speed sensors for respective wheels' turning speeds. The use
of tires other than specified may fail
to detect the accurate turning speed,
resulting in a longer stopping distance.

"ABS" warning light
The light comes on when the ignition
key is turned to the "ON" position. If
the anti-lock brake system and the
brake assist system work properly, the
light turns off after a few seconds.
Thereafter, if either of the systems malfunctions, the light comes on.

## p.218 When the "ABS" warning light is on (and

When the "ABS" warning light is on (and
the brake system warning light is off), the
anti-lock brake system, the brake assist
system, the vehicle stability control system and/or active traction control system
do/does not operate, but the brake system
still operates conventionally.
When the "ABS" warning light is on (and
the brake system warning light is off), the
anti-lock brake system does not operate
so that the wheels could lock up during
a sudden braking or braking on slippery
road surfaces.
If either of the following conditions occurs, this indicates a malfunction somewhere in the components monitored by
the warning light system. Contact your
Toyota dealer as soon as possible to
service the vehicle.

 The light does not come on when the
ignition key is turned to the "ON" position, or remains on.

 The light comes on while you are driving.

A warning light turning on briefly during
operation does not indicate a problem.

CAUTION

DRUM-IN-DISC TYPE PARKING BRAKE
SYSTEM

If the "ABS" warning light remains on
together with the brake system warning light, immediately stop your vehicle at a safe place and contact your
Toyota dealer.

Your vehicle has a drum-in-disc type
parking brake system. This type of brake
system needs bedding-down of the brake
shoes periodically or whenever the parking
brake shoes and/or drums are replaced.

In this case, not only the anti-lock
brake system will fail but also the
vehicle will become extremely unstable during braking.
Either of the following conditions may
occur, but do not indicate a malfunction.

 The light may stay on for about 60

seconds after the ignition key is turned
to "ON" position. It is normal if it turns
off after a while.

 Depressing the brake pedal repeatedly

may turn on the light. It is normal if it
turns off after a few seconds.

Have your Toyota dealer perform the bedding-down.
BRAKE ASSIST SYSTEM
When you slam the brakes on, the
brake assist system judges as an emergency stop and provides more powerful
braking for a driver who cannot hold
down the brake pedal firmly.
When you slam the brakes on, more powerful braking will be applied. At this time,
you may hear a sound in the engine
compartment and feel the vibrations of the
brake pedal. This does not indicate a malfunction.
The brake assist system becomes operative after the vehicle has accelerated to
a speed in excess of approximately 10
km/h (6 mph). It stops operating when the
vehicle decelerates to a speed below
approximately 5 km/h (3 mph).

## p.219 Brake pad wear limit indicators

Brake pad wear limit indicators

Rear step bumper

The brake pad wear limit indicators on
your disc brakes give a warning noise
when the brake pads are worn to where
replacement is required.

The rear step bumper is for rear end
protection and easier step-up loading.

The brake assist system may not work for
about 60 seconds after the engine is
started.
For an explanation of this system's warning light, see "Service reminder indicators
and warning buzzers" on page 122.

If you hear a squealing or scraping noise
while driving, have the brake pads
checked and replaced by your Toyota
dealer as soon as possible. Expensive rotor damage can result if the pads are not
replaced when necessary.

To get on the rear step bumper, use the
shaded area between the arrows in the
illustration.

CAUTION

 Do not allow more than one person
to get on the rear step bumper at
a time. It is designed for only one
person.

 Never drive the vehicle with anyone
on the rear step bumper.

## p.220 Limited-slip differential

Limited-slip differential

Your Toyota's identification-
-Vehicle identification
number

Some Toyotas are equipped with a limited-slip differential. If one of the rear
wheels begins to spin, the limited-slip differential is designed to aid traction by
automatically transmitting driving force to
the other rear wheel. If you are not sure
whether your vehicle is equipped with one,
you can ask your Toyota dealer.
CAUTION
Do not start or run the engine while
your vehicle is supported by a jack.
The vehicle could be driven off the
jack and could pose a danger or result in serious injury.

NOTICE
Use only a spare tire of the same
size, construction and load capacity
as the original tires on your Toyota
because damage to the limited-slip
differential could possibly occur with
another tire type.

The vehicle identification number (VIN)
is the legal identifier for your vehicle.
This number is on the left top of the
instrument panel, and can be seen
through the windshield from outside.
This is the primary identification number
for your Toyota. It is used in registering
the ownership of your vehicle.

The vehicle identification number (VIN) is
also on the Certification Label.

## p.221 -Engine number

-Engine number

Theft prevention labels
Your new vehicle carries theft prevention labels which are approximately 56
mm (2.20 in.) by 16 mm (0.63 in.).
The purpose of these labels is to reduce
the incidence of vehicle thefts by facilitating the tracing and recovery of parts from
stolen vehicles. The label is designed so
that once it is applied to a surface, any
attempt to remove it will result in destroying the integrity of the label. Transferring
these labels intact from one part to another, will be impossible.

Suspension and chassis
CAUTION
Do not modify the suspension/chassis
with lift kits, spacers, springs, etc. It
can cause dangerous handling characteristics, resulting in loss of control.

NOTICE
The engine number is stamped on the
engine block as shown.

You should not attempt to remove the
theft prevention labels as it may violate certain state or federal laws.

## p.222 Tire information-

Tire information-
-Tire symbols
This illustration indicates typical tire
symbols.
1. Tire size-For details, see "Tire
size" on page 224.
2. DOT and Tire Identification
Number (TIN)-For details, see
"DOT and Tire Identification Number (TIN)" on page 223.
3. Tire ply composition and materials-Plies mean a layer of rubber-
coated parallel cords. Cords mean
the strands forming the plies in the
tire.
4. Location of tread wear indicators-For details, see "Checking
and replacing tires" on page 304.
5. Summer tire or all season tire-
An all season tire has "M+S" on
the sidewall. The tire not marked
with "M+S" is a summer tire. For
details, see "Types of tires" on
page 233.
6. Radial tires or bias-ply tires-A
radial tire has "RADIAL" on the
sidewall. A tire not marked with
"RADIAL" is a bias-ply tire.

## p.223 -DOT and Tire Identification

-DOT and Tire Identification
Number (TIN)
7. "TUBELESS" or "TUBE TYPE"
-A tubeless tire does not have a
tube inside the tire and air is directly filled in the tire. A tube type tire
has a tube inside the tire and the
tube maintains the air pressure.
8. Uniform tire quality grading-For details, see "Uniform tire
quality grading" that follows.
9. Load limit at maximum cold tire
inflation pressure-For details,
see "Checking and replacing tires"
on page 304.
10. Maximum cold tire inflation
pressure-This means the pressure to which a tire may be inflated. For recommended cold tire
inflation pressure, see "Tires" on
page 328.

The "DOT" symbol certifies that the
tire conforms to applicable Federal
Motor Vehicle Safety Standards.
This illustration indicates typical DOT
and Tire Identification Number (TIN).
1. "DOT" symbol
2. Tire Identification Number (TIN)
3. Tire manufacturer's identification
mark
4. Tire size code
5. Manufacturer's optional tire type
code
6. Manufacturing week
7. Manufacturing year

## p.224 -Tire size

-Tire size
This illustration indicates typical tire
size.
1. Tire use (P=Passenger car,
T=Temporary use)
2. Section width (in millimeters)
3. Aspect ratio (tire height to section
width)
4. Tire construction code (R=Radial,
D=Diagonal)
5. Wheel diameter (in inch)
6. Load index (2 digits or 3 digits)
7. Speed symbol (alphabet with one
letter)

-Name of each section of tire
1. Section width
2. Tire height
3. Wheel diameter
1. Bead
2. Sidewall
3. Shoulder
4. Tread
5. Belt
6. Inner liner
7. Reinforcing rubber
8. Carcass
9. Rim lines
10. Bead wires
11. Chafer

## p.225 -Uniform tire quality grading

-Uniform tire quality grading
This information has been prepared
in accordance with regulations issued
by the National Highway Traffic Safety Administration of the U.S. Department of Transportation. It provides
the purchasers and/or prospective
purchasers of Toyota vehicles with information on uniform tire quality grading.
Your Toyota dealer will help answer
any questions you may have as you
read this information.
DOT quality grades-All passenger
vehicle tires must conform to Federal Safety Requirements in addition to these grades. Quality
grades can be found where applicable on the tire sidewall between
tread shoulder and maximum section width. For example: Treadwear
200 Traction AA Temperature A.

Tread wear-The tread wear grade
is a comparative rating based on the
wear rate of the tire when tested under controlled conditions on a specified government test course. For example, a tire graded 150 would wear
one and a half (1-1/2) times as well
on the government course as a tire
graded 100. The relative performance
of tires depends upon the actual
conditions of their use, however, and
may depart significantly from the
norm due to variations in driving habits, service practices and differences
in road characteristics and climate.

Traction AA, A, B, C-The traction
grades, from highest to lowest, are
AA, A, B, and C, and they represent
the tire's ability to stop on wet pavement as measured under controlled
conditions on specified government
test surfaces of asphalt and concrete.
A tire marked C may have poor traction performance.
Warning: The traction grade assigned
to this tire is based on braking
(straight ahead) traction tests and
does not include cornering (turning)
traction.

## p.226 Temperature A, B, C-The temperature grades are A (the highest), B,

Temperature A, B, C-The temperature grades are A (the highest), B,
and C, representing the tire's resistance to the generation of heat and
its ability to dissipate heat when
tested under controlled conditions on
a specified indoor laboratory test
wheel. Sustained high temperature
can cause the material of the tire to
degenerate and reduce tire life, and
excessive temperature can lead to
sudden tire failure. The grade C corresponds to a level of performance
which all passenger car tires must
meet under the Federal Motor Vehicle
Safety Standard No. 109. Grades B
and A represent higher levels of performance on the laboratory test wheel
than the minimum required by law.
Warning: The temperature grades for
this tire are established for a tire that
is properly inflated and not overloaded. Excessive speed, underinflation, or excessive loading, either separately or in combination, can cause
heat buildup and possible tire failure.

## p.227 -Glossary of tire terminology

-Glossary of tire terminology
Tire related term

Meaning

Cold tire inflation pressure

tire inflation pressure when the vehicle has been parked for at least 3 hours
or more, or it has not been driven more than 1.5 km or 1 mile under that
condition

Maximum inflation pressure

the maximum cold inflation pressure to which a tire may be inflated and it is
shown on the sidewall of the tire

Recommended inflation pressure

cold tire inflation pressure recommended by a manufacturer

Accessory weight

the combined weight (in excess of those standard items which may be replaced)
of automatic transmission, power steering, power brakes, power windows, power seats, radio, and heater, to the extent that these items are available as
factory-installed equipment (whether installed or not)

Curb weight

the weight of a motor vehicle with standard equipment including the maximum
capacity of fuel, oil, and coolant, and, if so equipped, air conditioning and additional weight optional engine

Maximum loaded vehicle weight

the sum of-
(a) curb weight;
(b) accessory weight;
(c) vehicle capacity weight; and
(d) production options weight

Normal occupant weight

68 kg (150 lb.) times the number of occupants specified in the second column
of Table 1 that follows

## p.228 Meaning

Meaning

Tire related term
Production options weight

the combined weight of those installed regular production options weighing over
2.3 kg (5 lb.) in excess of those standard items which they replace, not previously considered in curb weight or accessory weight, including heavy duty
brakes, ride levelers, roof rack, heavy duty battery, and special trim

Vehicle capacity weight
(Total load capacity)

the rated cargo and luggage load plus 68 kg (150 lb.) times the vehicle's designated seating capacity

Intended outboard sidewall

(A) the sidewall that contains a whitewall, bears white lettering or bears
manufacturer, brand, and/or model name molding that is higher or deeper
than the same molding on the other sidewall of the tire, or
(B) the outward facing sidewall of an asymmetrical tire that has a particular
side that must always face outward when mounted on a vehicle

Occupant distribution

distribution of occupants in a vehicle as specified in the third column of Table
1 that follows

Rim

a metal support for a tire or a tire and tube assembly upon which the tire beads
are seated

Rim diameter (Wheel diameter)

nominal diameter of the bead seat

Rim size designation

rim diameter and width

Rim type designation

the industry of manufacturer's designation for a rim by style or code

Rim width

nominal distance between rim flanges

Vehicle maximum load on the tire

the load on an individual tire that is determined by distributing to each axle
its share of the maximum loaded vehicle weight and dividing by two

## p.229 Tire related term

Tire related term

Meaning

Vehicle normal load on the tire

the load on an individual tire that is determined by distributing to each axle
its share of the curb weight, accessory weight, and normal occupant weight
(distributed in accordance with Table 1 that follows) and dividing by two

Weather side

the surface area of the rim not covered by the inflated tire

Table 1- Occupant loading and distribution for vehicle normal load for various designated seating capacities
Designated seating capacity, number Vehicle normal load, number of occu- Occupant distribution in a normally
of occupants
pants
loaded vehicle
2 through 4

2

2 in front

5 through 10

3

2 in front, 1 in second seat

## p.230 Cargo and luggage-

Cargo and luggage-
-Stowage precautions

Vehicle load limits
Vehicle load limits include total load
capacity, seating capacity, towing capacity and cargo capacity. Follow the
load limits shown below.
Total load capacity:
545 kg (1200 lb.)
Total load capacity means combined
weight of occupants, cargo and luggage. Tongue load is included when
trailer towing.
Seating capacity:
Total 8 (Front 2, Rear 6)
Seating capacity means the maximum
number of occupants whose estimated average weight is 68 kg (150
lb.) per person. Depending on the
weight of each person, the seating capacity given may exceed the total
load capacity.
NOTICE
Even if the number of occupants
are within the seating capacity,
do not exceed the total load capacity.

Towing capacity:
2948 kg (6500 lb.)
Towing capacity means the maximum
gross trailer weight (trailer weight plus
its cargo weight) that your vehicle is
able to tow.
Cargo capacity
Cargo capacity may increase or decrease depending on the size (weight)
and the number of occupants. For details, see "Capacity and distribution"
that follows.
CAUTION
Do not apply the load more than
each load limit. That may cause
not only damage to the tires, but
also deterioration to the steering
ability and braking ability, which
may cause an accident.

When stowing cargo and luggage in
or on the vehicle, observe the following:
 Put cargo and luggage in the luggage compartment when at all
possible. Be sure all items are secured in place.
 Be careful to keep the vehicle balanced. Locating the weight as far
forward as possible helps maintain
the balance.
 For better fuel economy, do not
carry unneeded weight.
CAUTION
 To prevent cargo and luggage
from sliding forward during
braking, do not stack anything
in the luggage compartment
higher than the seatbacks.
 Do not place anything on the
flattened seat or it may slide
forward during braking.

## p.231 -Capacity and distribution

-Capacity and distribution
 Never allow anyone to ride in
the luggage compartment. It is
not designed for passengers.
They should ride in their seats
with their seat belts properly
fastened. Otherwise, they are
much more likely to suffer serious bodily injury, in the event
of sudden braking or a collision.
 Do not place anything on the
luggage cover. Such items may
be thrown about and possibly
injure people in the vehicle
during sudden braking or an
accident. Secure all items in a
safe place.
 Do not drive with objects left
on top of the instrument panel.
They may interfere with the
driver's field of view. Or they
may move during sharp vehicle
acceleration or turning, and impair the driver's control of the
vehicle. In an accident they
may injure the vehicle occupants.

NOTICE
Do not load the vehicle beyond
the vehicle capacity weight given in Section 8.

Cargo capacity depends on the total weight of the occupants.
(Cargo capacity) = (Total load capacity) - (Total weight of occupants)
STEPS FOR DETERMINING CORRECT LOAD LIMIT
1. Locate the statement "The combined weight of occupants and cargo should never exceed XXX
pounds" on your vehicle's placard.
2. Determine the combined weight of
the driver and passengers that will
be riding in your vehicle.
3. Subtract the combined weight of
the driver and passengers from
XXX kilograms or XXX pounds.

## p.232 4. The resulting figure equals the

4. The resulting figure equals the
available amount of cargo and luggage load capacity. For example,
if the "XXX" amount equals 1400
lbs. and there will be five 150 lb.
passengers in your vehicle, the
amount of available cargo and luggage load capacity is 650 lbs.
(1400-750 (5x150)=650 lbs).
5. Determine the combined weight of
luggage and cargo being loaded on
the vehicle. That weight may not
safely exceed the available cargo
and luggage load capacity calculated in Step 4.
6. If your vehicle will be towing a trailer, load from your trailer will be
transferred to your vehicle. Consult
this manual to determine how this
reduces the available cargo and
luggage load capacity of your vehicle.
For details about trailer towing, see
page 241.

Cargo
capacity
Total load
capacity
EXAMPLE ON YOUR VEHICLE
In case that 2 people with the combined weight of 166 kg (366 lb.) are
riding in your vehicle with the total
load capacity of 545 kg (1200 lb.), the
available amount of cargo and luggage load capacity will be as follows:
545 kg - 166 kg = 379kg.
(1200 lb. - 366 lb. = 834 lb.)
From this condition, if 3 more passengers with the combined weight of 176
kg (388 lb.) get on, the available cargo and luggage load will be reduced
as follows:

379 kg - 176 kg = 203 kg.
(834 lb. - 388 lb. = 446 lb.)
As shown in the above example, if the
number of occupants increases, the
cargo and luggage load equaling the
combined weight of occupants who
got on later must be reduced. In other
words, if the increase in the number
of occupants causes the excess of
the total load capacity (combined
weight of occupants plus cargo and
luggage load), you have to reduce the
cargo and luggage on your vehicle.
For details about total load capacity,
see "Vehicle load limits" on page 230.

## p.233 CAUTION

CAUTION
Even if the total load of occupant's weight and the cargo load
is less than the total load capacity, do not apply the load unevenly. That may cause not only damage to the tire but also deterioration to the steering ability due to
unbalance of the vehicle, causing
an accident.

Weight of removed
third seat
Cargo
capacity

SEATING CONFIGURATION VARIATION
In case of removing the third seat, it
is possible to load as much cargo as
the weight of the removed seat.
(Cargo capacity) = (Total load capacity) - (Total weight of occupants) +
(weight of the removed third seat)
Third seat weight, kg (lb.):
Right
20 (44)
Left
20 (44)

Types of tires
Determine what kind of tires your
vehicle is originally equipped with.
1. Summer tires
Summer tires are high-speed capability tires best suited to highway driving
under dry conditions.
Since summer tires do not have the
same traction performance as snow
tires, summer tires are inadequate for
driving on snow-covered or icy roads.
For driving on snow-covered or icy
roads, we recommend using snow
tires. If installing snow tires, be sure
to replace all four tires.
2. All season tires
All season tires are designed to provide better traction in snow and to be
adequate for driving in most winter
conditions, as well as for use all year
round.

## p.234 All season tires, however, do not have

All season tires, however, do not have
adequate
traction
performance
compared with snow tires in heavy or
loose snow. Also, all season tires fall
short in acceleration and handling
performance compared with summer
tires in highway driving.
The details about how to distinguish
summer tires from all season tires are
described on page 222.
CAUTION
 Do not mix summer and all season tires on your vehicle as
this can cause dangerous handling characteristics, resulting
in loss of control.
 Do not use tires other than the
manufacturer's
designated
tires, and do not mix tires or
wheels of the sizes different
from the originally equipped
tires and wheels as this could
result in loss of control and
could cause death or serious
injury.

# Section 3: Starting and driving

## p.235 SECTION

SECTION

3

STARTING AND DRIVING
Before starting the engine . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 236
How to start the engine . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 236
Tips for driving in various conditions . . . . . . . . . . . . . . . . . . . . . . . . . . 237
Off-road driving precautions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 238
Winter driving tips . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 240
Dinghy towing . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 241
Trailer towing . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 241
How to save fuel and make your vehicle last longer, too . . . . . . . . . 249

## p.236 Before starting the engine

Before starting the engine
1. Check the area around the vehicle before entering it.
2. Adjust seat position, seatback angle,
head restraint height and steering
wheel angle.
3. Adjust the inside and outside rear view
mirrors.
4. Lock all doors.
5. Fasten seat belts.

How to start the engine-
(a) Cranking hold function
Once you turn the ignition key to "START"
position and release it, the cranking hold
function continues to crank the engine in
"ON" position until it starts.
The function stops cranking the engine
after about 25 seconds maximum if the
engine has not started yet. When you
crank the engine again, wait a few seconds and restart it.
If you hold the key in "START" position,
the function will keep cranking for about
30 seconds maximum.

(b) Before cranking
1. Apply the parking brake firmly.
2. Turn off unnecessary lights and accessories.
3. Put the selector lever in "P". If you
need to restart the engine while the
vehicle is moving, put the selector lever in "N". A starter safety device will
prevent the starter from operating if the
selector lever is in any drive position.
4. Depress the brake pedal and hold it
to the floor until driving off.

## p.237 (c) Starting the engine

(c) Starting the engine
Before starting the engine, be sure to follow the instructions in "(b) Before cranking".
Normal starting procedure
The multiport fuel injection system/sequential multiport fuel injection system in your
engine automatically controls the proper
air-fuel mixture for starting.
You can start a cold or hot engine as
follows:
With your foot off the accelerator pedal,
turning the ignition key to "START" position, then release it.
Engine should be warmed up by driving,
not in idle. For warming up, drive with
smoothly turning engine until engine coolant temperature is within normal range.
If the engine stalls...
Simply restart it, using the correct procedure given in normal starting.
If the engine will not start...
See "If your vehicle will not start" on page
252.

NOTICE
z Do not race a cold engine.
z If the engine becomes difficult to
start or stalls frequently, have the
engine checked immediately.

Tips for driving in various
conditions
 Always slow down in gusty crosswinds.

This will allow you much better control.

 Drive slowly onto curbs and, if pos-

sible, at a right angle. Avoid driving
onto high, sharp-edged objects and
other road hazards. Failure to do so
can lead to severe tire damage such
as a tire burst.
Drive slowly when passing over bumps
or travelling on a bumpy road. Otherwise, the impact could cause severe
damage to the tires and/or wheels.

 When parking on a hill, turn the front

wheels until they touch the curb so
that the vehicle will not roll. Apply the
parking brake, and place the transmission in "P". If necessary, block the
wheels.

 Washing your vehicle or driving through

deep water may get the brakes wet. To
see whether they are wet, check that
there is no traffic near you, and then
press the pedal lightly. If you do not
feel a normal braking force, the brakes
are probably wet. To dry them, drive
the vehicle cautiously while lightly
pressing the brake pedal with the parking brake applied. If they still do not
work safely, pull to the side of the road
and call a Toyota dealer for assistance.

## p.238 Off-road driving precautions

Off-road driving precautions
CAUTION

 Before driving off, make sure the
parking brake is fully released and
that the parking brake reminder
light is off.

 Do not leave your vehicle unattended while the engine is running.

 Do not rest your foot on the brake
pedal while driving. It can cause
dangerous overheating, needless
wear, and poor fuel economy.

 To drive down a long or steep hill,
reduce your speed and downshift.
Remember, if you ride the brakes
excessively, they may overheat and
not work properly.

 Be careful when accelerating, upshifting, downshifting or braking on
a slippery surface. Sudden acceleration or engine braking could cause
the vehicle to spin or skid.

 Do not drive in excess of the speed
limit. Even if the legal speed limit
permits it, do not drive over 140
km/h (85 mph) unless your vehicle
has high-speed capability tires.
Driving over 140 km/h (85 mph) may
result in tire failure, loss of control
and possible injury. Be sure to consult a tire dealer to determine
whether the tires on your vehicle
are high-speed capability tires or
not before driving at such speeds.

 Do not continue normal driving
when the brakes are wet. If they are
wet, your vehicle will require a
longer stopping distance, and it
may pull to one side when the
brakes are applied. Also, the parking brake will not hold the vehicle
securely.

When driving your vehicle off-road, please
observe the following precautions to ensure your driving enjoyment and to help
prevent the closure of areas to off-road
vehicles.
a. Drive your vehicle only in areas where
off-road vehicles are permitted to travel.
b. Respect private property. Get owner's
permission before entering private property.
c. Do not enter areas that are closed.
Honor gates, barriers and signs that restrict travel.
d. Stay on established roads.
When
conditions are wet, driving techniques
should be changed or travel delayed to
prevent damage to roads.
For owners in U.S. mainland, Hawaii and
Puerto Rico:
To obtain additional information pertaining
to driving your vehicle off-road, consult
the following organizations.

 State and Local Parks and Recreation
Departments

 State Motor Vehicle Bureau
 Recreational Vehicle Clubs

## p.239  U.S. Forest Service and Bureau of

 U.S. Forest Service and Bureau of
Land Management

CAUTION
Always observe the following precautions to minimize the risk of serious
personal injury or damage to your vehicle:

 Drive carefully when off the road.
Do not take unnecessary risks by
driving in dangerous places.

 Do not grip the steering wheel
spokes when driving off-road.
A
bad bump could jerk the wheel and
injure your hands.
Keep both
hands and especially your thumbs
on the outside of the rim.

 Always check your brakes for effectiveness immediately after driving in
sand, mud, water or snow.

 After driving through tall grass,

NOTICE

mud, rock, sand, rivers, etc., check
that there is no grass, bush, paper,
rags, stone, sand, etc. adhering or
trapped on the underbody.
Clear
off any such matter from the underbody. If the vehicle is used with
these materials trapped or adhering
to the underbody, a breakdown or
fire could occur.

z If driving through water, such as
when crossing shallow streams,
first check the depth of the water
and the bottom of the river bed for
firmness.
Drive slowly and avoid
deep water.

 In a rollover crash, an unbelted person is significantly more likely to
die than a person wearing a seat
belt. Therefore, the driver and all
passengers should fasten their seat
belts whenever the vehicle is moving.

 When driving off-road or in rugged
terrain, do not drive at excessive
speeds, jump, make sharp turns,
strike objects, etc. This may cause
loss of control or vehicle rollover
causing death or serious injury.
You are also risking expensive damage to your vehicle's suspension
and chassis.

z Take all necessary safety measures
to ensure that water damage to the
engine or other components does
not occur.
z Water entering the engine air intake
will cause severe engine damage.
z Water can wash the grease from
wheel bearings, causing rusting and
premature failure, and may also enter the differentials, transmission
and transfer case, reducing the gear
oil's lubricating qualities.
z Sand and mud that has accumulated
in brake drums and around brake
discs may affect braking efficiency
and may damage brake system components.

## p.240 Winter driving tips

Winter driving tips
z Always perform a maintenance inspection after each day of off-road
driving that has taken you through
rough terrain, sand, mud, or water.
For scheduled maintenance information, refer to the "Scheduled Maintenance Guide" or "Owner's Manual
Supplement".

Make sure your coolant is properly protected against freezing.

Check the condition of the battery and
cables.

Only use "Toyota Super Long Life Coolant"
or similar high quality ethylene glycol
based non-silicate, non-amine, non-nitrite,
and non-borate coolant with long-life
hybrid organic acid technology. (Coolant
with
long-life
hybrid
organic
acid
technology is a combination of low
phosphates and organic acids.)

Cold temperatures reduce the capacity of
any battery, so it must be in top shape
to provide enough power for winter starting. It tells you how to visually inspect the
battery on page 312. Your Toyota dealer
and most service stations will be pleased
to check the level of charge.

See "Checking the engine coolant level"
on page 298 for details of coolant type
selection.
"Toyota Super Long Life Coolant" is a mixture of 50% coolant and 50% deionized
water. This coolant provides protection
down to about -35°C (-31°F).

NOTICE
Do not use plain water alone.

Make sure the engine oil viscosity is
suitable for the cold weather.
See page 297 for recommended viscosity.
Leaving a heavy summer oil in your vehicle during winter months may cause
harder starting. If you are not sure about
which oil to use, call your Toyota dealer-
they will be pleased to help.
Keep the door locks from freezing.
Squirt lock de-icer or glycerine into the
locks to keep them from freezing.
Use a washer fluid containing an antifreeze solution.
This product is available at your Toyota
dealer and most auto parts stores. Follow
the manufacturer's directions for how
much to mix with water.

## p.241 Dinghy towing

Dinghy towing
NOTICE
Do not use engine antifreeze or any
other substitute as washer fluid because it may damage your vehicle's
paint.
Do not use your parking brake when
there is a possibility it could freeze.
When parking, put the transmission into
"P" and block the front wheels. Do not
use the parking brake, or snow or water
accumulated in and around the parking
brake mechanism may freeze, making it
hard to release.
Keep ice and snow from accumulating
under the fenders.
Ice and snow built up under your fenders
can make steering difficult. During bad
winter driving, stop and check under the
fenders occasionally.
Depending on where you are driving,
we recommend you carry some emergency equipment.

Trailer towing
Your vehicle is designed primarily as a
passenger-and-load-carrying vehicle. Towing a trailer will have an adverse effect on
handling, performance, braking, durability
and driving economy (fuel consumption,
etc.). Your safety and satisfaction depend
on the proper use of correct equipment
and cautious driving habits. For your safety and the safety of others, you must not
overload your vehicle or trailer. Ask your
local Toyota dealer for further details before towing.
WEIGHT LIMITS

Your vehicle is not designed to be
dinghy towed (with four wheels on the
ground) behind a motorhome.

NOTICE
Do not tow your vehicle with four
wheels on the ground. This may
cause serious damage to your vehicle.

Before towing, make sure the total trailer weight, gross combination weight,
gross vehicle weight, gross axle weight
and trailer tongue load are all within
the limits.
The total trailer weight and tongue load
can be measured with platform scales
found at a highway weighing station, building supply company, trucking company,
junk yard, etc.

Some of the things you might put in the
vehicle are tire chains, window scraper,
bag of sand or salt, flares, small shovel,
jumper cables, etc.

## p.242 CAUTION

CAUTION

 The maximum gross trailer weight
(trailer weight plus cargo weight)
must
never
exceed
2948 kg
(6500 lb.). If towing a trailer and
cargo
weighing
over
907 kg
(2000 lb.), it is necessary to use a
sway control device with sufficient
capacity. The combination of the
gross trailer weight added to the
total weight of the vehicle, occupants and vehicle cargo must never
exceed
a
total
of
5625 kg
(12400 lb.). Exceeding the maximum
weight of the trailer, the vehicle, or
the vehicle and trailer combination,
can cause an accident resulting in
serious personal injuries.

 Trailer hitch assemblies have different weight capacities established by
the hitch manufacturer. Even though
the vehicle may be physically capable of towing a higher weight, the
operator must determine the maximum weight rating of the particular
hitch assembly and never exceed
the maximum weight rating specified for the trailer-hitch. Exceeding
the maximum weight rating set by
the trailer hitch manufacturer can
cause an accident resulting in serious personal injuries.
 The gross vehicle weight must not
exceed the Gross Vehicle Weight
Rating (GVWR) indicated on the
Certification Label. The gross vehicle weight is the sum of weights
of the unloaded vehicle, driver, passengers, luggage, hitch and trailer
tongue load. It also includes the
weight of any special equipment
installed on your vehicle.

## p.243  The load on either the front or rear

 The load on either the front or rear

Total trailer weight

Tongue load

axle resulting from distribution of
the gross vehicle weight on both
axles must not exceed the Gross
Axle Weight Rating (GAWR) listed
on the Certification Label.

Tongue load
Total trailer weight

Never load the trailer with more
weight in the back than in the
front. About 60% of the trailer load
should be in the front half of the
trailer and the remaining 40% in the
rear.

100 = 9 to 11% (∗ 1)
or 15% (∗ 2)

 The trailer cargo load should be
distributed so that the tongue load
is 9 to 11% for weight carrying
hitch (∗1) or 15% for weight distributing hitch (∗2) of the total trailer
weight, not exceeding the maximum
load of the following
Weight carrying hitch
295 kg (650 lb.)
Weight distributing hitch
442 kg (975 lb.)

## p.244 HITCHES

HITCHES

 If you wish to install a trailer hitch, you
should consult with your Toyota dealer.

 Use only a hitch recommended by the
hitch manufacturer and the one which
conforms to the total trailer weight
requirement.

 The hitch must be bolted securely to
the vehicle frame and installed according to the hitch manufacturer's instructions.

NOTICE
Do not use axle-mounted hitches as
they can cause damage to the axle
housing, wheel bearings, wheels or
tires. Also, never install a hitch which
may interfere with the normal function
of an Energy Absorbing Bumper, if so
equipped.

 The hitch ball and king pin should have
a light coat of grease.

 Toyota recommends removing the trail-

er hitch whenever you are not towing
a trailer to reduce the possibility of
additional damage caused by the hitch
if your vehicle is struck from behind.
After removing the hitch, seal any
mounting holes in the vehicle body to
prevent entry of pollutants such as exhaust fumes, dirt, water, etc.

1 Trailer ball load rating
2 Ball diameter
3 Shank length
4 Shank diameter
TRAILER BALL
Follow these easy steps to properly determine the correct trailer ball for your application:
1. Determine the correct trailer ball size
for the trailer coupler. Most couplers
are stamped with the required trailer
ball size. The sizes you will most likely
find stamped on the coupler are:

## p.245 Trailer Class Typical Trailer Ball Size

Trailer Class Typical Trailer Ball Size
III
2 in.
II
2 in.
I
1 7/8 in.

MATCHING TRAILER BALL HEIGHT TO
TRAILER COUPLER HEIGHT
No matter which class of tow hitch applies, for a safe trailer hookup, the trailer
ball setup on must be the proper height
for the coupler on the trailer.

2. Select the appropriate trailer ball to
match or exceed the gross trailer
weight rating of the trailer. The trailer
ball load rating should be printed on
the top of the ball.

BRAKES AND SAFETY CHAINS

 Toyota

recommends trailers with
brakes that conform to any applicable federal and state/provincial regulations.

3. When mounted in the ball mount, the
threaded ball shank must protrude beyond the bottom of the lock washer
and nut at least 2 threads. The trailer
ball shank must be matched to the ball
mount hole diameter size.

 A safety chain must always be used
between the towing vehicle and the
trailer. Leave sufficient slack in the
chain for turns. The chain should
cross under the trailer tongue to
prevent the tongue from dropping to
the ground in case it becomes damaged or separated. For correct safety
chain procedures, follow the hitch or
trailer manufacturer's recommendations.

1 Coupler
2 Trailer ball

## p.246 CAUTION

CAUTION

 If the total trailer weight exceeds
453 kg (1000 lb.), trailer brakes are
required.

 Never tap into your vehicle's hydraulic system as it would lower its
braking effectiveness.

 Never tow a trailer without using a
safety chain securely attached to
both the trailer and the vehicle. If
damage occurs to the coupling unit
or hitch ball, there is danger of the
trailer wandering over into another
lane.

TIRES

 Ensure that your vehicle's tires are
properly inflated. Adjust the tire inflation pressure indicated below:
tire inflation pressure, kPa (psi)
Front
220 (32)
Rear
240 (35)
See Section 7-2 and Section 8 for instructions.

 The trailer tires should be inflated to
the pressure recommended by the trailer manufacturer in respect to the total
trailer weight.

TRAILER LIGHTS

 Your vehicle is equipped with a wire

harness stored in the rear end under
body. Your vehicle is fitted with a socket for trailer lights under the rear
bumper. Use either of them to connect
and operate the trailer lights. However,
the trailer lights must comply with federal, state/provincial and local regulations. See your local recreational vehicle dealer or rental agency for the
correct type of wiring and relays for
your trailer. Check for correct operation
of the turn signals and stop lights each
time you hitch up. Direct splicing may
damage your vehicle's electrical system
and cause a malfunction of your lights.

## p.247 BREAK-IN SCHEDULE

BREAK-IN SCHEDULE

 Toyota recommends that you do not

tow a trailer with a new vehicle or a
vehicle with any new power train component (engine, transmission, differential, wheel bearing, etc.) for the first
800 km (500 miles) of driving.

MAINTENANCE

 If you tow a trailer, your vehicle will

require more frequent maintenance due
to the additional load. For this
information,
please
refer
to
the
scheduled maintenance information in
the "Scheduled Maintenance Guide" or
"Owner's Manual Supplement".

 Retighten all fixing bolts of the towing
ball and bracket after approximately
1000 km (600 miles) of trailer driving.

PRE-TOWING SAFETY CHECK

 Check that your vehicle remains level

when a loaded or unloaded trailer is
hitched. Do not drive if the vehicle has
an abnormal nose-up or nose-down
condition, and check for improper
tongue load, overload, worn suspension
or other possible causes.

 Make sure the trailer cargo is securely
loaded so that it cannot shift.

 Check that your rear view mirrors con-

form to any applicable federal, state/
provincial or local regulations. If not,
install the rear view mirrors required
for towing purpose.

TRAILER TOWING TIPS
When towing a trailer, your vehicle will
handle differently than when not towing. The three main causes of vehicle-
trailer accidents are driver error, excessive speed and improper trailer loading.
Keep these in mind when towing:

 Before starting out, check operation of

the lights and all vehicle-trailer connections. After driving a short distance,
stop and recheck the lights and connections. Before actually towing a trailer, practice turning, stopping and backing with a trailer in an area away from
traffic until you learn the feel.

 Because stopping distance may be in-

creased, vehicle-to-vehicle distance
should be increased when towing a
trailer. For each 16 km/h (10 mph) of
speed, allow at least one vehicle and
trailer length between you and the vehicle ahead. Avoid sudden braking as
you may skid, resulting in jackknifing
and loss of control. This is especially
true on wet or slippery surfaces.

 Avoid jerky starts or sudden acceleration.

 Avoid jerky steering and sharp turns.

The trailer could hit your vehicle in a
tight turn. Slow down before making a
turn to avoid the necessity of sudden
braking.

 Remember that when making a turn,

the trailer wheels will be closer than
the vehicle wheels to the inside of the
turn. Therefore, compensate for this by
making a larger than normal turning
radius with your vehicle.

 Backing with a trailer is difficult and

requires practice. Grip the bottom of
the steering wheel and move your hand
to the left to move the trailer to the
left. Move your hand to the right to
move the trailer to the right. (This procedure is generally opposite to that
when backing without a trailer). Also,
just turn the steering wheel a little at
a time, avoiding sharp or prolonged
turning. Have someone guide you when
backing to reduce the risk of an accident.

## p.248  Crosswinds and rough roads will ad-

 Crosswinds and rough roads will ad-

versely affect handling of your vehicle
and trailer, causing sway. Pay attention
to the rear from time to time to prepare yourself for being passed by large
trucks or buses, which may cause your
vehicle and trailer to sway. If swaying
happens, firmly grip the steering wheel
and reduce speed immediately but
gradually. Never increase speed. Steer
straight ahead. If you make no extreme
correction with the steering or brakes,
the vehicle and trailer will stabilize itself.

 Be careful when passing other ve-

hicles. Passing requires considerable
distance. After passing a vehicle, do
not forget the length of your trailer and
be sure you have plenty of room before changing lanes.

 In order to maintain engine braking and
electrical charging performance, do not
use the overdrive. Transmission must
be in the "4" position.

 Because of the added load of the trail-

er, your vehicle's engine may overheat
on hot days (at temperatures over
30°C [85°F]) when going up a long or
steep grade with a trailer. If the engine
coolant temperature gauge indicates
overheating, immediately turn off the air
conditioning (if in use), pull off the road
and stop in a safe spot. Refer to "If
your vehicle overheats" on page 256.

 Always place wheel blocks under both

the vehicle and trailer wheels when
parking. Apply the parking brake firmly.
Put the transmission in "P". Avoid parking on a slope with a trailer, but if it
cannot be avoided, do so only after
performing the following:
1. Apply the brakes and keep them
applied.
2. Have someone place wheel blocks
under both the vehicle and trailer
wheels.
3. When the wheel blocks are in place,
release your brakes slowly until the
blocks absorb the load.
4. Apply the parking brake firmly.
5. Shift into "P" and turn off the engine.

When restarting out after parking on a
slope:
1. With the transmission in "P" position, start the engine. Be sure to
keep the brake pedal depressed.
2. Shift into the "3", "2", "L" or "R"
position.
3. Release the parking brake and
brake pedal and slowly pull or back
away from the wheel blocks. Stop
and apply your brakes.
4. Have someone retrieve the blocks.

## p.249 How to save fuel and make

How to save fuel and make
your vehicle last longer, too
CAUTION

 Do not exceed 72 km/h (45 mph) or
the posted towing speed limit,
whichever is lower. Because instability (swaying) of a towing vehicle-
trailer
combination
usually
increases as the speed increases, exceeding 72 km/h (45 mph) may
cause loss of control.

 Slow down and downshift before
descending steep or long downhill
grades. Do not make sudden downshifts.

 Avoid holding the brake pedal down
too long or too frequently. This
could cause the brakes to overheat
and result in reduced braking efficiency.

Improving fuel economy is easy-just take
it easy. It will help make your vehicle last
longer, too. Here are some specific tips
on how to save money on both fuel and
repairs:

 Keep your tires inflated at the cor-

rect pressure. Underinflation causes
tire wear and wastes fuel. See page on
301.

 Do not carry unneeded weight in

your vehicle. Excess weight puts a
heavier load on the engine, causing
greater fuel consumption.

 Avoid lengthy warm-up idling. Once
the engine is running smoothly, begin
driving-but gently. Remember, however, that on cold winter days this may
take a little longer.

 Accelerate

 Avoid engine over-revving. Use a

gear position suitable for the road on
which you are travelling.

 Avoid continuous speeding up and
slowing down.
wastes fuel.

Stop-and-go

driving

 Avoid

unnecessary stopping and
braking. Maintain a steady pace. Try
to time the traffic signals so you only
need to stop as little as possible or
take advantage of through streets to
avoid traffic lights. Keep a proper distance from other vehicles to avoid sudden braking. This will also reduce wear
on your brakes.

 Avoid heavy traffic or traffic jams
whenever possible.

 Do not rest your foot on the brake

smoothly.

pedal. This causes premature wear,
overheating and poor fuel economy.

 Avoid long engine idling. If you have

 Maintain a moderate speed on high-

slowly and
Avoid jackrabbit starts.

a long wait and you are not in traffic,
it is better to turn off the engine and
start again later.

ways. The faster you drive, the greater
the fuel consumption. By reducing your
speed, you will cut down on fuel consumption.

## p.250  Keep the front wheels in proper

 Keep the front wheels in proper

alignment. Avoid hitting the curb and
slow down on rough roads. Improper
alignment not only causes faster tire
wear but also puts an extra load on
the engine, which, in turn, wastes fuel.

 Keep the bottom of your vehicle free
from mud, etc. This not only lessens
weight but also helps prevent corrosion.

 Keep your vehicle tuned-up and in

top shape. A dirty air cleaner, improper valve clearance, dirty plugs, dirty oil
and grease, brakes not adjusted, etc.
all lower engine performance and contribute to poor fuel economy. For longer
life of all parts and lower operating
costs, keep all maintenance work on
schedule, and if you often drive under
severe conditions, see that your vehicle
receives more frequent maintenance.
(For scheduled maintenance information, please refer to the "Scheduled
Maintenance Guide" or "Owner's Manual Supplement".)

CAUTION
Never turn off the engine to coast
down hills. Your power steering and
brake booster will not function without the engine running. Also, the
emission control system operates
properly only when the engine is running.

# Section 4: In case of an emergency

## p.251 SECTION

SECTION

4

IN CASE OF AN EMERGENCY
If your vehicle will not start . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 252
If your engine stalls while driving . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 256
If you cannot increase engine speed . . . . . . . . . . . . . . . . . . . . . . . . . . 256
If your vehicle overheats . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 256
If you have a flat tire . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 257
If your vehicle becomes stuck . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 268
If your vehicle needs to be towed . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 269
If you cannot shift automatic transmission
selector lever . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 272
If you lose your keys . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 273

## p.252 If your vehicle will not start-

If your vehicle will not start-
(a) Simple checks
Before making these checks, make sure
you have followed the correct starting
procedure given in "How to start the
engine" on page 236 and that you have
sufficient fuel. Also check whether the
other keys will start the engine. If they
work, your key may be broken. Have the
key checked at your Toyota dealer. If
none of your keys work, there may be a
malfunction in the immobilizer system. Call
your Toyota dealer. (See "Keys" on page
10.)

If the engine is not turning over or is
turning over too slowly-

If the engine turns over at its normal
speed but will not start-

1. Check that the battery terminals are
tight and clean.

1. The engine may be flooded because of
repeated cranking. See "(b) Starting a
flooded engine" for further instructions.

2. If the battery terminals are O.K., switch
on the interior light.
3. If the light is out, dim or goes out
when the starter is cranked, the battery
is discharged. You may try jump starting. See "(c) Jump starting" for further
instructions.
If the light is O.K., but the engine still will
not start, it needs adjustment or repair.
Call a Toyota dealer or qualified repair
shop.

NOTICE
Do not pull- or push-start the vehicle. It may damage the vehicle or
cause a collision when the engine
starts. Also the three-way catalytic
converter may overheat and become a
fire hazard.

2. If the engine still will not start, it needs
adjustment or repair. Call a Toyota
dealer or qualified repair shop.

## p.253 (b) Starting a flooded engine

(b) Starting a flooded engine

(c) Jump starting

If the engine will not start, your engine
may be flooded because of repeated
cranking.

To avoid serious personal injury and
damage to your vehicle which might result from battery explosion, acid burns,
electrical burns, or damaged electronic
components, these instructions must be
followed precisely.

If this happens, turn the ignition key to
"START" with the accelerator pedal fully
depressed, and hold the key at this position for about 30 seconds. Then the
cranking hold function stops cranking automatically, and you can try starting the
engine with your foot off the accelerator
pedal.
If the engine does not start, wait a few
minutes and try again.
If the engine still will not start, it needs
adjustment or repair. Call a Toyota dealer
or qualified repair shop for assistance.

If you are unsure about how to follow this
procedure, we strongly recommend that
you seek the help of a competent mechanic or towing service.

CAUTION

 Batteries

contain
sulfuric
acid
which is poisonous and corrosive.
Wear protective safety glasses when
jump starting, and avoid spilling
acid on your skin, clothing, or vehicle.

 The gas normally produced by a
battery will explode if a flame or
spark is brought near. Use only
standardized jumper cables and do
not smoke or light a match while
jump starting.

NOTICE
The battery used for boosting must
be 12 V. Do not jump start unless you
are sure that the booster battery is
correct.

 If you should accidentally get acid
on yourself or in your eyes, remove
any contaminated clothing and flush
the affected area with water immediately. Then get immediate medical attention. If possible, continue
to apply water with a sponge or
cloth while en route to the medical
office.

## p.254 JUMP STARTING PROCEDURE

JUMP STARTING PROCEDURE
1. If the booster battery is installed in
another vehicle, make sure the vehicles
are not touching. Turn off all unnecessary lights and accessories.
When boosting, use the battery of
matching or higher quality. Any other
battery may be difficult to jump start
with.
If jump starting is difficult, charge the
battery for several times.
2. If required, remove all the vent plugs
from the booster and discharged batteries. Lay a cloth over the open vents
on the batteries. (This helps reduce the
explosion hazard, personal injuries and
burns.)
3. If the engine in the vehicle with the
booster battery is not running, start it
and let it run for a few minutes. During
jump starting, run the engine at about
2000 rpm with the accelerator pedal
lightly depressed.

Discharged battery

Jumper cable

Booster
battery
Positive
terminal
("+" mark)

Jumper
cable

Positive terminal
("+" mark)

4. Make the cable connections in the order a, b, c, d.
a. Connect the clamp of the positive
(red) jumper cable to the positive
(+) terminal on the discharged battery.
b. Connect the clamp at the other end
of the positive (red) jumper cable to
the positive (+) terminal on the
booster battery.

Discharged battery
Negative
terminal ("-" mark)

Booster
battery

c. Connect the clamp of the negative
(black) jumper cable to the negative
(-) terminal on the booster battery.
d. Connect the clamp at the other end
of the negative (black) jumper cable
to a solid, stationary, unpainted, metallic point of the vehicle with the
discharged battery.
The recommended connecting point is
shown in the following illustration:

## p.255 5. Charge the discharged battery with the

5. Charge the discharged battery with the
jumper cables connected for approximately 5 minutes. At this time, run the
engine in the vehicle with the booster
battery at about 2000 rpm with the accelerator pedal lightly depressed.
6. Start your engine in the normal way.
After starting, run it at about 2000 rpm
for several minutes with the accelerator
pedal lightly depressed.
7. Carefully disconnect the cables in the
exact reverse order: the negative cable
and then the positive cable.
Connecting point

Do not connect the cable to or near
any part that moves when the engine
is cranked.

CAUTION
When making the connections, to
avoid serious injury, do not lean over
the battery or accidentally let the
jumper cables or clamps touch anything except the correct battery terminals or the ground.

If the first start attempt is not successful...
Check that the clamp on the jumper
cables are tight. Recharge the discharged
battery with the jumper cables connected
for several minutes and restart your hybrid
system in the normal way.
If the another attempt is not successful,
the battery may be depleted. Have it
checked at your Toyota dealer.

8. Carefully dispose of the battery cover
cloths-they may now contain sulfuric
acid.
9. If removed, replace all the battery vent
plugs.
If the cause of your battery discharging is
not apparent (for example, lights left on),
you should have it checked at your Toyota
dealer.

## p.256 If your engine stalls while

If your engine stalls while
driving

If you cannot increase engine
speed

If your vehicle overheats

If your engine stalls while driving...

If engine speed does not increase when
the accelerator pedal is depressed, the
electronic throttle control system may
be faulty. Move the vehicle to a safe
place by means of creeping and call a
Toyota dealer for assistance:

If your engine coolant temperature
gauge indicates overheating, if you experience a loss of power, or if you hear
a loud knocking or pinging noise, the
engine has probably overheated. You
should follow this procedure...

1. Depress the brake pedal and shift to
the "D" position.

1. Pull safely off the road, stop the vehicle and turn on your emergency
flashers. Put the transmission in "P"
and apply the parking brake. Turn off
the air conditioning if it is being used.

1. Reduce your speed gradually, keeping
a straight line. Move cautiously off the
road to a safe place.
2. Turn on your emergency flashers.
3. Try starting the engine again.
If the engine will not start, see "If your
vehicle will not start" on page 252.

CAUTION
If the engine is not running, the power assist for the brakes and steering
will not work so steering and braking
will be much harder than usual.

2. Gradually release the brake pedal, and
the vehicle starts to move by creeping.
After arriving at a safe place, stop the
vehicle and call a Toyota dealer for
assistance.

CAUTION

 The above method of moving the
vehicle is for emergency. Use it
only for moving minimum distances
to a safe place.

 Be especially careful to prevent erroneous pedal operation.

2. If coolant or steam is boiling out of the
radiator or reservoir, stop the engine.
Wait until the steam subsides before
opening the hood. If there is no coolant
boiling over or steam, leave the engine
running.

CAUTION
To help avoid personal injury, keep
the hood closed until there is no
steam. Escaping steam or coolant is
a sign of very high pressure.

## p.257 3. Visually check to see if the engine

3. Visually check to see if the engine
drive belt (fan belt) is broken or loose.
Look for obvious coolant leaks from the
radiator, hoses, and under the vehicle.
However, note that water draining from
the air conditioning is normal if it has
been used.

CAUTION
When the engine is running, keep
hands and clothing away from the
moving fan and engine drive belts.
4. If the engine drive belt is broken or the
coolant is leaking, stop the engine immediately. Call a Toyota dealer for assistance.

CAUTION
Do not attempt to remove the radiator
cap when the engine and radiator are
hot. Serious injury could result from
scalding hot fluid and steam blown
out under pressure.
7. After the engine coolant temperature
has cooled to normal, again check the
coolant level in the reservoir. If necessary, bring it up to half full again. Serious coolant loss indicates a leak in the
system. You should have it checked as
soon as possible at your Toyota dealer.

If you have a flat tire-
1. Reduce your speed gradually,
keeping a straight line. Move cautiously off the road to a safe place
well away from the traffic. Avoid
stopping on the center divider of
a highway. Park on a level spot
with firm ground.
2. Stop the engine and turn on your
emergency flashers.
3. Firmly set the parking brake and
put the transmission in "P".
4. Have everyone get out of the vehicle on the side away from traffic.
5. Read the following instructions
thoroughly.

5. If the engine drive belt is O.K. and
there are no obvious leaks, you may
help the engine cool down more quickly
by running it at about 1500 rpm for a
few minutes with the accelerator pedal
lightly depressed.
6. Check the coolant reservoir. If it is dry,
add coolant to the reservoir while the
engine is running. Fill it about half full.
For the coolant type, see "Coolant type
selection" on page 299.

## p.258 CAUTION

CAUTION
When jacking, be sure to observe
the following to reduce the possibility of personal injury:
 Follow jacking instructions.
 Do not put any part of your
body under the vehicle supported by the jack. Otherwise,
personal injury may occur.
 Do not start or run the engine
while your vehicle is supported
by the jack.
 Stop the vehicle on a level firm
ground, firmly set the parking
brake and put the transmission
in reverse. Block the wheel diagonally opposite to the one
being changed if necessary.

 Make sure to set the jack properly in the jack point. Raising
the vehicle with jack improperly positioned will damage the
vehicle or may allow the vehicle to fall off the jack and
cause personal injury.
 Never get under the vehicle
when the vehicle is supported
by the jack alone.
 Use the jack only for lifting
your vehicle during wheel
changing.
 Do not raise the vehicle with
someone in the vehicle.
 When raising the vehicle, do
not place any objects on top
of or underneath the jack.
 Raise the vehicle only high
enough to remove and change
the tire.

NOTICE
Do not continue driving with a
deflated tire. Driving even a
short distance can damage a
tire and wheel beyond repair.

## p.259 -Required tools and spare

-Required tools and spare
tire

1. Get the required tools and spare
tire.
1 Tool bag
2 Jack
3 Spare tire
To prepare yourself for an emergency,
you should familiarize yourself with
the use of the jack, each of the tools
and their storage locations.
When storing the jack, put it in place
and secure to prevent it from flying
forward during a collision or sudden
braking.

Turn the jack joint by hand.
To remove: Turn the joint in direction
1 until the jack is free.
To store: Turn the joint in direction 2
until the jack is firmly secured to prevent it flying forward during a collision
or sudden braking.

To remove the spare tire under the
luggage compartment:
1. Put a jack handle, jack handle extensions and jack handle end together as shown in the illustration.
1
Jack handle end
2
Jack handle extension
3
Jack handle
CAUTION
Make sure they are each securely
fixed with screws.

## p.260 When connecting a jack handle extension with a jack handle end, use a

When connecting a jack handle extension with a jack handle end, use a
jack handle to tighten the bolts on the
joints as shown in the illustration.
When connecting the jack handle with
extension, tighten the wing bolt on the
joint securely. Make sure the hollow
meets the bolt on every joint when
you tighten the bolts.
NOTICE
Tighten all the joints securely.
Otherwise, the extension may
come off and it may damage
the paint or vehicle body.

2. Remove the access hole cover on
the rear bumper with a flat-bladed
screwdriver.
To protect the paint, place several
sheets of paper over the paintwork.

3. Insert the jack handle end into the
lowering screw through the access
hole and turn it counterclockwise
with pushing it to the front lightly.

## p.261 -Blocking the wheel

-Blocking the wheel

4. After the tire is lowered completely
to the ground, remove the holding
bracket as shown in the illustration.

When storing the spare tire, put it in
place with the outer side of the wheel
facing up and hook the holding bracket as shown in the illustration. Then
secure the tire, taking care that the
tire goes straight up without catching
on any other part, to prevent it from
moving during a collision or sudden
braking.
Check the tire from the side to see
that the tire is stored horizontally.

2. Block the wheel diagonally opposite the flat tire to keep the
vehicle from rolling when it is
jacked up.
When blocking the wheel, place a
wheel block in front of one of the front
wheels or behind one of the rear
wheels.

## p.262 -Removing wheel ornament

-Removing wheel ornament

-Loosening wheel nuts
CAUTION
Never use oil or grease on the
bolts or nuts. The nuts may loosen and the wheels may fall off,
which could cause a serious accident.

3. Remove the wheel ornament.
Pry off the wheel ornament, using the
beveled end of the wheel ornament
remover as shown.
CAUTION
Do not try to pull off the ornament by hand. Take due care in
handling the ornament to avoid
unexpected personal injury.

4. Loosen all the wheel nuts.
Always loosen the wheel nuts before
raising the vehicle.
Turn the wheel nuts counterclockwise
to loosen. To get maximum leverage,
fit the wrench to the nut so that the
handle is on the right side, as shown
above. Grab the wrench near the end
of the handle and pull up on the handle. Be careful that the wrench does
not slip off the nut.
Do not remove the nuts yet-just unscrew them about one-half turn.

## p.263 -Positioning the jack

-Positioning the jack
JACK POINTS:
Front-Under the frame side rail
Left rear-Under the rear axle
housing
Right rear-Under the bracket on
the rear axle housing
Make sure the jack is positioned on
a level and solid place.

Put a jack handle, jack handle extensions, and jack handle end together
as shown in the illustration.
1
Jack handle end
2
Jack handle extensions
3
Jack handle
CAUTION

5. Position the jack at the correct
jack point as shown.

Make sure they are each securely
fixed with screws.

## p.264 -Raising your vehicle

-Raising your vehicle
NOTICE
Tighten all the joints securely.
Otherwise, the extension may
come off and it may damage
the paint or vehicle body.

When connecting a jack handle extension with another extension and a jack
handle end, use a jack handle to tighten the bolts on the joints as shown
in the illustration. When connecting
the jack handle with extension, tighten the wing bolt on the jack handle
securely. Make sure the hollow meets
the bolt on any joint when you tighten
the bolts.

6. After making sure no one is in
the vehicle, raise it high enough
so that the spare tire can be
installed.
Remember you will need more ground
clearance when putting on the spare
tire than when removing the flat tire.

## p.265 -Changing wheels

-Changing wheels
To raise the vehicle, insert the jack
handle end into the joint of the jack
(it is a loose fit) and turn it clockwise
with the handle, making sure the handle remains firmly fitted onto the jack
handle end. As the jack touches the
vehicle and begins to lift, double-
check that it is properly positioned.
CAUTION
Never get under the vehicle when
the vehicle is supported by the
jack alone.

7. Remove the wheel nuts and
change tires.
Lift the flat tire straight off and put it
aside.
Roll the spare wheel into position and
align the holes in the wheel with the
bolts. Then lift up the wheel and get
at least the top bolt started through
its hole. Wiggle the tire and press it
back over the other bolts.

Before putting on wheels, remove any
corrosion on the mounting surfaces
with a wire brush or such. Installation
of wheels without good metal-to-metal contact at the mounting surface can
cause wheel nuts to loosen and
eventually cause a wheel to come off
while driving.

## p.266 -Reinstalling wheel nuts

-Reinstalling wheel nuts

-Lowering your vehicle
CAUTION
Never use oil or grease on the
bolts or nuts. Doing so may lead
to overtightening the nuts and
damaging the bolts. The nuts
may loosen and the wheels may
fall off, which could cause a serious accident. If there is oil or
grease on any bolt or nut, clean
it.

8. Reinstall all the wheel nuts finger tight.
Reinstall the wheel nuts (tapered end
inward) and tighten them as much as
you can by hand. Press back on the
tire and see if you can tighten them
more.

9. Lower the vehicle completely
and tighten the wheel nuts.
Turn the jack handle extension counterclockwise with handle to lower the
vehicle, making sure the handle remains firmly fitted onto the jack handle extension.
Use only the wheel nut wrench and
turn it clockwise to tighten the nuts.
Do not use other tools or any additional leverage other than your hands,
such as a hammer, pipe or your foot.
Make sure the wrench is securely engaged over the nut.

## p.267 -Reinstalling wheel ornament

-Reinstalling wheel ornament
Tighten each nut a little at a time in
the order shown. Repeat the process
until all the nuts are tight.
CAUTION
 When lowering the vehicle,
make sure all portions of your
body and all other persons
around will not be injured as
the vehicle is lowered to the
ground.
 Have the wheel nuts tightened
with a torque wrench to 131
N·m (13.4 kgf·m, 96.6 ft·lbf), as
soon as possible after changing wheels. Otherwise, the
nuts may loosen and the
wheels may fall off, which
could cause a serious accident.

10. Reinstall the wheel ornament.
Put the wheel ornament into position.
And press hand firmly on one side of
wheel ornament and then firmly tap
the other side around the edge of
wheel ornament with the heel of your
hand to snap into place.
CAUTION
Take due care in handling the ornament to avoid unexpected personal injury.

-After changing wheels
11. Check the air pressure of the replaced tire.
Adjust the air pressure to the specification designated on page 328. If the
pressure is lower, drive slowly to the
nearest service station and fill to the
correct pressure.
Do not forget to reinstall the tire inflation valve cap as dirt and moisture
could get into the valve core and
possibly cause air leakage. If the cap
is missing, have a new one put on as
soon as possible.
12. Restow all the tools, jack and
flat tire securely.
As soon after changing wheels as
possible, tighten the wheel nuts to the
torque specified on page 328 with a
torque wrench. Have a technician repair the flat tire.
This is the same procedure for changing or rotating your tires.

## p.268 If your vehicle becomes

If your vehicle becomes
stuck
CAUTION
Before driving, make sure all the
tools, jack and flat tire are securely in place in their storage
location to reduce the possibility
of personal injury during a collision or sudden braking.

If your vehicle becomes stuck in snow,
mud, sand, etc., then you may attempt to
rock the vehicle free by moving it forward
and backward.
If your vehicle is equipped with the traction control system, turn off the system to
become unstuck to allow the tires to spin
enough to remove the vehicle from the
obstruction. (For details, see "Vehicle stability control system" on page 147.)

CAUTION
Do not attempt to rock the vehicle
free by moving it forward and backward if people or objects are anywhere near the vehicle. During the
rocking operation the vehicle may
suddenly move forward or backward
as it becomes unstuck, causing injury
or damage to nearby people or objects.

NOTICE
If you rock your vehicle, observe the
following precautions to prevent damage to the transmission and other
parts.
z Do not depress the accelerator pedal while shifting the selector lever
or before the transmission is completely shifted to forward or reverse
gear.
z Do not race the engine and avoid
spinning the wheels.
z If your vehicle remains stuck after
rocking the vehicle several times,
consider other ways such as towing.

## p.269 If your vehicle needs to be

If your vehicle needs to be
towed-
(a) Towing with wheel lift type truck-
-From front

-From rear

(b) Using flat bed truck

If towing is necessary, we recommend
you have it done by your Toyota dealer
or a commercial tow truck service. In
consultation with them, have your vehicle towed using either (a) or (b).

(a) Towing with wheel lift type truck
Use a towing dolly under the wheels not
lifted by the truck.
(b) Using flat bed truck

Only when you cannot receive a towing
service from a Toyota dealer or commercial tow truck service, tow your vehicle carefully in accordance with the
instructions given in "-Emergency towing" in this section.
Proper equipment will help ensure that
your vehicle is not damaged while being
towed. Commercial operators are generally
aware of the state/provincial and local
laws pertaining to towing.
Your vehicle can be damaged if it is
towed incorrectly. Although most operators
know the correct procedure, it is possible
to make a mistake. To avoid damage to
your vehicle, make sure the following precautions are observed. If necessary, show
this page to the tow truck driver.
TOWING PRECAUTIONS:
Use a safety chain system for all towing,
and abide by the state/provincial and local
laws. The wheels and axle on the ground
must be in good condition. If they are
damaged, use a towing dolly.

## p.270 -Emergency towing

-Emergency towing
(c) Towing with sling type
truck

CAUTION
Use extreme caution when towing vehicle. Avoid sudden starts or erratic
driving maneuvers which would place
excessive stress on the emergency
towing hook and towing cable or
chain. The hook and towing cable or
chain may break and cause serious
injury or damage.

NOTICE
(c) Towing with sling type truck

NOTICE
Do not tow with sling type truck, either from the front or rear. This may
cause body damage.

If towing is necessary, we recommend
you to have it done by your Toyota
dealer or a commercial tow truck service.
If towing service is not available in an
emergency, your vehicle may be temporarily towed by a cable or chain secured to front emergency towing hook.
Use extreme caution when towing the
vehicle.
A driver must be in the vehicle to steer it
and operate the brakes.

Towing in this manner may be done only
on hard-surfaced roads for a short distance and at low speeds. Also, the
wheels, axles, drive train, steering and
brakes must all be in good condition.

z Do not use front and rear eyelets.
It is not designed for towing.
z Use only a cable or chain specifically intended for use in towing vehicles. Securely fasten the cable or
chain to the towing hook provided.
z Never tow a vehicle from the rear
with four wheels on the ground.
This may cause serious damage to
the transmission.
Before towing, release the parking brake
and put the transmission in "N". Unlock
the center differential. The key must be in
"ACC" (engine off) or "ON" (engine running).

## p.271 CAUTION

CAUTION
If the engine is not running, the power assist for the brakes and steering
will not work so steering and braking
will be much harder than usual.

-Emergency towing hook
precautions
 Before emergency towing, check that

the hook is not broken or damage and
that the installation bolts are not loose.

 Fasten the towing cable or chain securely to the hook.

 Do not jerk the hook. Apply steady and
even force.

 To avoid damaging the hook, do not

pull from the side or at a vertical
angle. Always pull straight ahead.

CAUTION
If the emergency towing hook is used
to get out when your vehicle becomes
struck in mud, sand or other condition from which the vehicle cannot be
driven out under its own power, make
sure to observe the precautions mentioned below. Otherwise, excessive
stress will be put on the hook and
the towing cable or chain may break,
causing serious injury or damage.

 If the towing vehicle can hardly
move, do not forcibly continue the
towing. Contact your Toyota dealer
or a commercial tow truck service
for assistance.

 Tow the vehicle as straight ahead
as possible.

 Keep away from the vehicle during
towing.

## p.272 -Tips for towing a stuck vehicle

-Tips for towing a stuck vehicle

If you cannot shift automatic
transmission selector lever

The following methods are effective to
use when your vehicle is stuck in the
mud, sand or other condition from
which the vehicle cannot be driven out
under its own power. Use extreme caution when towing the vehicles. In addition, keep away from the vehicles and
towing cable or chain when towing.

 Remove the sand soil in the front and
the back of the tires.

 Place stones or wood under the tires.

If you cannot shift the selector lever
out of "P" position to other positions
even though the brake pedal is depressed, use the shift lock override button as follows:

3. Insert your finger into the hole to
push down the shift lock override
button. You can shift out of "P"
position only while pushing the button.

1. Turn the ignition key to
position. Make sure the
brake is applied.

4. Shift into "N" position.

"LOCK"
parking

2. Pry up the cover with a flat-bladed
screwdriver or equivalent.

5. Reinstall the cover.
6. Start the engine. For your safety,
keep the brake pedal depressed.
Be sure to have the system checked by
your Toyota dealer as soon as possible.

## p.273 If you lose your keys

If you lose your keys
You can purchase a new key at your
Toyota dealer if you can give them the
key number and master key.
Even if you lose only one key, contact
your Toyota dealer to make a new key. If
you lose all your master keys, you cannot
make new keys; the whole engine immobilizer system must be replaced.
See the suggestion given in "Keys" on
page 10.
You can use the wireless remote control
system with the new key. Contact your
Toyota dealer for detailed information.
If your keys are locked in the vehicle and
you cannot get a duplicate, many Toyota
dealers can still open the door for you,
using their special tools. If you must
break a window to get in, we suggest
breaking the smallest side window because it is the least expensive to replace.
Be extremely cautious to avoid cuts from
the glass.

## p.274 

# Section 5: Corrosion prevention and appearance care

## p.275 SECTION

SECTION

5

CORROSION PREVENTION AND
APPEARANCE CARE
Protecting your Toyota from corrosion . . . . . . . . . . . . . . . . . . . . . . . . . 276
Washing and waxing your Toyota . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 277
Cleaning the interior . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 279

## p.276 Protecting your Toyota from

Protecting your Toyota from
corrosion
Toyota, through its diligent research, design and use of the most advanced
technology available, helps prevent corrosion and provides you with the finest quality vehicle construction. Now, it is up to
you. Proper care of your Toyota can help
ensure long-term corrosion prevention.
The most common causes of corrosion
to your vehicle are:

 The accumulation of road salt, dirt and
moisture in hard-to-reach areas under
the vehicle.

 Chipping

of paint, or undercoating
caused by minor accidents or by
stones and gravel.

Care is especially important if you live
in particular areas or operate your vehicle under certain environmental conditions:

 Road salt or dust control chemicals will

accelerate corrosion, as will the presence of salt in the air near the sea-
coast or in areas of industrial pollution.

 High humidity accelerates corrosion es-

pecially when temperatures range just
above the freezing point.

 Wetness or dampness to certain parts

of your vehicle for an extended period
of time, may cause corrosion even
though other parts of the vehicle may
be dry.

 High ambient temperatures can cause

corrosion to those components of the
vehicle which do not dry quickly due to
lack of proper ventilation.

The above signifies the necessity to keep
your vehicle, particularly the underside, as
clean as possible and to repair any damage to paint or protective coatings as
soon as possible.
To help prevent corrosion on
Toyota, follow these guidelines:

your

Wash your vehicle frequently. It is, of
course, necessary to keep your vehicle
clean by regular washing, but to prevent
corrosion, the following points should be
observed:

 If you drive on salted roads in the
winter or if you live near the ocean,
you should hose off the undercarriage
at least once a month to minimize corrosion.

 High pressure water or steam is effec-

tive for cleaning the vehicle's underside
and wheel housings. Pay particular
attention to these areas as it is difficult
to see all the mud and dirt. It will do
more harm than good to simply wet the
mud and debris without removing. The
lower edge of doors, rocker panels and
frame members have drain holes which
should not be allowed to clog with dirt
as trapped water in these areas can
cause corrosion.

 Wash the underside of the vehicle thoroughly when winter is over.

See "Washing and waxing your Toyota" on
page 277 for more tips.
Check the condition of your vehicle's
paint and trim. If you find any chips or
scratches in the paint, touch them up immediately to prevent corrosion from starting. If the chips or scratches have gone
through the bare metal, have a qualified
body shop make the repair.

## p.277 Washing and waxing your

Washing and waxing your
Toyota
Check the interior of your vehicle. Water and dirt can accumulate under the
floor mats and could cause corrosion. Occasionally check under the mats to make
sure the area is dry. Be particularly careful when transporting chemicals, cleansers, fertilizers, salt, etc.; these should be
transported in proper containers. If a spill
or leak should occur, immediately clean
and dry the area.
Use mud shields on your wheels. If you
drive on salted or gravel roads, mud
shields help protect your vehicle. Full-size
shields, which come as near to the ground
as possible, are the best. We recommend
that the fittings and the area where the
shields are installed be treated to resist
corrosion. Your Toyota dealer will be
happy to assist in supplying and installing
the shields if they are recommended for
your area.
Keep your vehicle in a well ventilated
garage or a roofed place. Do not park
your vehicle in a damp, poorly ventilated garage. If you wash your vehicle in
the garage, or if you drive it covered with
water or snow, your garage may be so
damp as to cause corrosion. Even if your
garage is heated, a wet vehicle can corrode if the ventilation is poor.

Washing your Toyota
Keep your
washing.

vehicle

clean

by

regular

The following cases may cause weakness
to the paint or corrosion to the body and
parts. Wash your vehicle as soon as possible.

 When driving in a coastal area
 When driving on a road sprinkled with
antifreeze

1. Rinse off loose dirt with a hose. Remove any mud or road salt from the
underside of the vehicle or in the
wheel wells.
2. Wash with a mild car-wash soap,
mixed according to the manufacturer's
instructions. Use a soft cotton mitt and
keep it wet by dipping it frequently into
the wash water. Do not rub hard-let
the soap and water remove the dirt.

a lot of smoke, soot, dust, iron dust or
chemical substances

Plastic wheel ornaments: The plastic
wheel ornaments are damaged easily by
organic substances. If any organic substances splashes an ornament, be sure to
wash it off with water and check if the
ornament is damaged.

 When the vehicle becomes remarkably
dirty with dust and mud

CAUTION

Hand-washing your Toyota

Do not attach the heavily damaged
plastic wheel ornament. It may fly off
the wheel and cause accidents while
the vehicle is moving.

 When exposed to coal tar, tree sap,

bird droppings and carcass of an insect

 When driving in areas where there is

Work in the shade and wait until the
vehicle body is not hot to the touch.

CAUTION
When cleaning under floor or chassis,
be careful not to injure your hands.

Aluminum wheels: Use only a mild soap
or neutral detergent.
Plastic bumpers: Wash carefully. Do not
scrub with abrasive cleaners. The bumper
faces are soft.

## p.278 Road tar: Remove with turpentine or

Road tar: Remove with turpentine or
cleaners that are marked safe for painted
surfaces.

NOTICE
Do not use organic substances (gasoline kerosene, benzine or strong solvents) which may be toxic or cause
damage.
3. Rinse
thoroughly-dried
soap
can
cause streaking. In hot weather you
may need to rinse each section right
after you wash it.
4. To prevent water spots, dry the vehicle
using a clean soft cotton towel. Do not
rub or press hard-you might scratch
the paint.

Automatic car wash

Waxing your Toyota

Your vehicle may be washed in an automatic car wash, but remember that the
paint can be scratched by some types of
brushes, unfiltered washing water, or the
washing process itself. Scratching reduces
paint durability and gloss, especially on
darker colors. The manager of the car
wash should be able to advise you whether the process is safe for the paint on
your vehicle.

Polishing and waxing is recommended
to maintain the original beauty of your
Toyota's finish.

NOTICE
To prevent damage to the antenna,
make sure it is retracted before driving your Toyota through an automatic
car wash.

Apply wax once a month or if the vehicle
surface does not repel water well.
1. Always wash and dry the vehicle before you begin waxing, even if you are
using a combined cleaner and wax.
2. Use a good quality polish and wax. If
the finish has become extremely weathered, use a car-cleaning polish, followed by a separate wax. Carefully follow the manufacturer's instructions and
precautions. Be sure to polish and wax
the chrome trim as well as the paint.
Windshield washer nozzles: Make sure
that the nozzles do not become blocked
when waxing. If a nozzle becomes
blocked, contact your Toyota dealer to
have the vehicle serviced.

NOTICE
If a nozzle becomes blocked, do not
try to clear it with a pin or other
object. The nozzle will be damaged.

## p.279 Cleaning the interior

Cleaning the interior
3. Wax the vehicle again when water
does not bead but remains on the surface in large patches.

NOTICE
Always remove the plastic bumpers if
your vehicle is re-painted and placed
in a high heat paint waxing booth.
High temperatures could damage the
bumpers.

CAUTION

 Vehicles with side airbags and curtain shield airbags:
Be careful not to splash water or
spill liquid on the floor. This may
prevent the side and curtain shield
airbags from activating correctly, resulting in serious injury.

 Do not wash the vehicle floor with
water, or allow water to get onto
the floor when cleaning the vehicle
interior or exterior. Water may get
into audio components or other
electrical components above or under the floor carpet (or mat) and
cause a malfunction; and it may
cause body corrosion.

Vinyl interior
The vinyl upholstery may be easily
cleaned with a mild soap or detergent
and water.
First vacuum over the upholstery to remove loose dirt. Then, using a sponge or
soft cloth, apply the soap solution to the
vinyl. After allowing it to soak in for a few
minutes to loosen the dirt, remove the dirt
and wipe off the soap with a clean damp
cloth. If all the dirt do not come off, repeat the procedure. Commercial foaming-
type vinyl cleaners are also available
which work well. Follow the manufacturer's
instructions.

NOTICE
Do not use solvent, thinner, gasoline
or window cleaner on the interior.

## p.280 Carpets

Carpets
Use a good foam-type
clean the carpets.

shampoo

to

Begin by vacuuming thoroughly to remove
as much dirt as possible. Several types of
foam cleaners are available; some are in
aerosol cans and others are powders or
liquids which you mix with water to produce a foam. To shampoo the carpets,
use a sponge or brush to apply the foam.
Rub in overlapping circles.
Do not apply water-the best results are
obtained by keeping the carpet as dry as
possible. Read the shampoo instructions
and follow them closely.
Seat belts
The seat belts may be cleaned with
mild soap and water or with lukewarm
water.
Use a cloth or sponge. As you are cleaning, check the belts for excessive wear,
fraying, or cuts.

NOTICE

NOTICE

z Do not use dye or bleach on the
belts-it may weaken them.

z Do not use organic substances (solvents, kerosene, alcohol, gasoline,
etc.) or alkaline or acidic solutions.
These chemicals can cause discoloring, staining or peeling of the
surface.

z Do not use the belts until they become dry.
Windows
The windows may be cleaned with any
household window cleaner.

NOTICE
When cleaning the inside of the rear
window, be careful not to scratch or
damage the heater wires or connectors.
Air conditioning control panel, car audio, instrument panel, console panel,
and switches
Use a soft damp cloth for cleaning.
Soak a clean soft cloth in water or lukewarm water then lightly wipe off dirt.

z If you use cleaners or polishing
agents, make sure their ingredients
do not include the substances mentioned above.
z If you use a liquid car freshener, do
not spill the liquid onto the vehicle's interior surfaces. It may contain
the
ingredients mentioned
above. Immediately clean any spill
using the method mentioned above.

## p.281 Leather Interior

Leather Interior
The leather upholstery may be cleaned
with neutral detergent for wool.
Remove dirt using a soft cloth dampened
with 5% solution of neutral detergent for
wool. Then thoroughly wipe off all traces
of detergent with a clean damp cloth.
After cleaning or whenever any part of the
leather gets wet, dry with a soft clean
cloth. Allow the leather to dry in a ventilated shaded area.

NOTICE
z If a stain should fail to come out
with a neutral detergent, apply a
cleaner that does not contain an
organic solvent.
z Never use organic substances such
as benzine, alcohol or gasoline, or
alkaline or acid solutions for cleaning the leather as these could
cause discoloring.
z Use of a nylon brush or synthetic
fiber cloth, etc. may scratch the
fine grained surface of the leather.

z Mildew may develop on soiled leather upholstery. Be especially careful
to avoid oil spots. Try to keep your
upholstery always clean.
z Long exposure to direct sunlight
may cause the leather surface to
harden and shrink. Keep your vehicle in a shaded area, especially in
the summer.
z The interior of your vehicle is apt
to heat up on hot summer days, so
avoid placing on the upholstery
items made of vinyl or plastic or
containing wax as these tend to
stick to leather when warm.
z Improper cleaning of the leather upholstery could result in discoloration or staining.
If you have any questions about the
cleaning of your Toyota, your local
Toyota dealer will be pleased to answer
them.

## p.282 

# Section 6: Vehicle maintenance and care

## p.283 SECTION

SECTION

6

VEHICLE MAINTENANCE AND CARE
Maintenance requirements . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 284
General maintenance . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 285
Does your vehicle need repairing? . . . . . . . . . . . . . . . . . . . . . . . . . . . . 287
Emissions inspection and maintenance (I/M) programs . . . . . . . . . 288

For scheduled maintenance information, please refer to the
"Scheduled Maintenance Guide" or "Owner's Manual Supplement".

## p.284 Maintenance requirements

Maintenance requirements
Your Toyota vehicle has been designed for
fewer maintenance requirements with longer service intervals to save both your time
and money. However, each regular maintenance, as well as day-to-day care, is
more important than ever before to ensure
smooth, trouble-free, safe, and economical
driving.
It is the owner's responsibility to make
sure the specified maintenance, including
general maintenance service, is performed.
Note that both the new vehicle and
emission control system warranties specify
that proper maintenance and care must be
performed.
See
"Owner's
Warranty
Information Booklet" or "Owner's Manual
Supplement"
for
complete
warranty
information.
General maintenance
General maintenance items are those day-
to-day care practices that are important to
your vehicle for proper operation. It is the
owner's responsibility to ensure that the
general maintenance items are performed
regularly.
These checks or inspections can be done
either by yourself or a qualified technician,
or if you prefer, your Toyota dealer will be
pleased to do them at a nominal cost.

Scheduled maintenance

Where to go for service?

The scheduled maintenance items listed in
the "Scheduled Maintenance Guide" or
"Owner's Manual Supplement" are those
required to be serviced at regular intervals.

Toyota technicians are well-trained specialists and are kept up to date with the
latest service information through technical
bulletins, service tips, and in-dealership
training programs. They learn to work on
Toyotas before they work on your vehicle,
rather than while they are working on it.

For details of your maintenance schedule,
read the "Scheduled Maintenance Guide"
or "Owner's Manual Supplement".
It is recommended that only genuine
Toyota parts be used for maintenance
or for the repair of the emission control system.

You can be confident that your Toyota
dealer's service department performs the
best job to meet the maintenance requirements on your vehicle-reliably and economically.

The owner may elect to use non-Toyota
supplied parts for replacement purposes without invalidating the emission
control system warranty. However, use
of replacement parts which are not of
equivalent quality may impair the effectiveness of the emission control systems.

Your copy of the repair order is proof that
all required maintenance has been performed for warranty coverage. If any problems should arise with your vehicle while
under warranty, your Toyota dealer will
promptly take care of it. Again, be sure
to keep a copy of the repair order for any
service performed on your Toyota.

You may also elect to have maintenance, replacement, or repair of the
emission control devices and system
performed by any automotive repair establishment or individual without invalidating this warranty. See "Owner's Warranty Information Booklet" or "Owner's
Manual Supplement" for complete warranty information.

What about do-it-yourself maintenance?
Many of the maintenance items are easy
to do yourself if you have a little mechanical ability and a few basic automotive
tools. Simple instructions for how to perform them are presented in Section 7.

## p.285 General maintenance

General maintenance
If you are a skilled do-it-yourself
mechanic, the Toyota service manuals are
recommended. Please be aware that
do-it-yourself maintenance can affect your
warranty coverage. See "Owner's Warranty
Information Booklet" or "Owner's Manual
Supplement" for the details.

Listed below are the general maintenance
items that should be performed as frequently as specified. In addition to checking the items listed, if you notice any
unusual noise, smell or vibration, you
should investigate the cause or take your
vehicle to your Toyota dealer or a qualified service shop immediately. It is recommended that any problem you notice be
brought to the attention of your dealer or
the qualified service shop for their advice.

CAUTION
Make these checks only with adequate ventilation if you run the engine.
IN THE ENGINE COMPARTMENT
Items listed below should be checked
from time to time, e.g. each time when
refueling.
Washer fluid
Make sure there is sufficient fluid in the
tank. See page 315 for additional information.

Engine coolant level
Make sure the coolant level is between
the "FULL" and "LOW" lines on the see-
through reservoir when the engine is cold.
See page 298 for additional information.
Radiator, condenser and hoses
Check that the front of the radiator and
condenser are clean and not blocked with
leaves, dirt, or insects. See page 299 for
additional information.
Battery electrolyte level
Make sure the electrolyte level of all battery cells is between upper and lower level lines on the case. Add only distilled
water when replenishing. See page 312 for
additional information.
Brake fluid level
Make sure the brake fluid level is correct.
See page 300 for additional information.
Engine oil level
Check the level on the dipstick with the
engine turned off and the vehicle parked
on a level ground. See page 296 for additional information.
Power steering fluid level
Check the level through the reservoir. The
level should be in the "HOT" or "COLD"
range depending on the fluid temperature.
See page 301 for additional information.

## p.286 Exhaust system

Exhaust system
If you notice any change in the sound of
the exhaust or smell exhaust fumes, have
the cause located and corrected immediately. (See "Engine exhaust cautions" on
page 213.)
INSIDE THE VEHICLE
Items listed below should be checked
regularly, e.g. while performing periodic
services, cleaning the vehicle, etc.
Lights
Make sure the headlights, stop lights, tail
lights, turn signal lights, and other lights
are all working. Check headlight aim.
Service reminder indicators and warning
buzzers
Check that all service reminder indicators
and warning buzzers function properly.
Steering wheel
Be alert for changes in steering condition,
such as hard steering or strange noise.

Seats
Check that all front seat controls such as
seat adjusters, seatback recliner, etc. operate smoothly and that all latches lock
securely in any position. Check that the
head restraint move up and down smoothly and that the locks hold securely in any
latched position. For folding-down rear
seatbacks, swing-up rear seat cushions
and detachable third seats, check that the
latches lock securely.
Seat belts
Check that the seat belt system such as
buckles, retractors and anchors operate
properly and smoothly. Make sure the belt
webbing is not cut, frayed, worn or damaged.
Accelerator pedal
Check the pedal for smooth operation and
uneven pedal effort or catching.
Brake pedal
Check the pedal for smooth operation and
that the pedal has the proper clearance.
Check the brake booster function.
Brakes
In a safe place, check that the brakes do
not pull to one side when applied.

Parking brake
Check that the lever has the proper travel
and that, on a safe incline, your vehicle
is held securely with only the parking
brake applied.
Automatic transmission "Park" mechanism
Check the lock release button of the selector lever for proper and smooth operation. On a safe incline, check that your
vehicle is held securely with the selector
lever in "P" position and all brakes released.
OUTSIDE THE VEHICLE
Items listed below should be performed
from time to time, unless otherwise
specified.
Fluid leaks
Check underneath for leaking fuel, oil, water or other fluid after the vehicle has
been parked for a while. If you smell fuel
fumes or notice any leak, have the cause
found and corrected immediately.
Doors and engine hood
Check that all doors and back door operate smoothly and all latches lock securely.
Make sure the engine hood secondary
latch secures the hood from opening when
the primary latch is released.

## p.287 Does your vehicle need

Does your vehicle need
repairing?
Tire inflation pressure
Check the pressure with a gauge every two weeks, or at least once a
month. See page 301 for additional
information.
Tire surface and wheel nuts
Check the tires carefully for cuts,
damage or excessive wear. See page
304 for additional information. When
checking the tires, make sure no nuts
are missing, and check the nuts for
looseness. Tighten them if necessary.
Tire rotation
Rotate the tires according to the
maintenance schedule. (For scheduled maintenance information, please
refer to the "Scheduled Maintenance
Guide" or "Owner's Manual Supplement".) See page 306 for additional
information.

Be on the alert for changes in performance, sounds, and visual tip-offs that
indicate service is needed. Some important clues are as follows:

 Engine missing, stumbling, or pinging
 Appreciable loss of power
 Strange engine noises
 A fluid leak under the vehicle (however,

water dripping from the air conditioning
after use is normal.)

 Change in exhaust sound (This may

indicate a dangerous carbon monoxide
leak. Drive with the windows open and
have the exhaust system checked immediately.)

 Engine continually runs hot; oil pressure gauge stays low

If you notice any of these clues, take your
vehicle to your Toyota dealer as soon as
possible. It probably needs adjustment or
repair.

CAUTION
Do not continue driving with the vehicle unchecked. It could result in serious vehicle damage and possibly
personal injury.

 Flat-looking tire; excessive tire squeal
when cornering; uneven tire wear

 Vehicle pulls to one side when driving
straight on a level road

 Strange noises related to suspension
movement

 Loss of brake effectiveness; spongy

feeling brake pedal; pedal almost
touches floor; vehicle pulls to one side
when braking

 Engine coolant temperature continually
higher than normal

## p.288 Emissions

Emissions
Inspection
and
Maintenance (I/M) programs
Some states have vehicle emission inspection programs which include OBD
(On-Board Diagnostics) checks.
The OBD system monitors the operation
of the emission control system. When the
OBD system determines that a problem
exists somewhere in the emission control
system, the malfunction indicator lamp
comes on. In this case, your vehicle may
not pass the I/M test and need to be
repaired. Contact your Toyota dealer to
service the vehicle.
Even if the malfunction indicator lamp
does not come on, your vehicle may not
pass the I/M test as readiness codes
have not been set in the OBD system.
Readiness codes are automatically set
during ordinary driving. However, when the
battery is disconnected or run down, the
codes are erased. Also, depending on
your driving habits, the codes may not be
completely set.
Also, if the malfunction indicator lamp had
come on recently due to temporary malfunction such as a loose fuel tank cap,
your vehicle may not pass the I/M test.

The malfunction indicator lamp will go off
after taking several driving trips, but the
error code in the OBD system will not be
cleared unless about 40 trips or more are
taken.
If your vehicle does not pass the I/M test
even the malfunction indicator lamp does
not come on, contact your Toyota dealer
to prepare the vehicle for re-testing.

# Section 7-1: Do it yourself maintenance, Introduction

## p.289 SECTION

SECTION

7- 1

DO-IT-YOURSELF MAINTENANCE
Introduction
Engine compartment overview . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 290
Fuse locations . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 291
Do-it-yourself service precautions . . . . . . . . . . . . . . . . . . . . . . . . . . . 292
Parts and tools . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 293

## p.290 Engine compartment overview

Engine compartment overview
1. Engine oil filler cap
2. Brake fluid reservoir
3. Fuse block
4. Battery
5. Windshield and rear window washer
fluid tank
6. Engine oil level dipstick
7. Condenser
8. Radiator
9. Engine coolant reservoir
10. Power steering fluid reservoir

## p.291 Fuse locations

Fuse locations

1

Spare fuses

Spare fuses

## p.292 Do-it-yourself service

Do-it-yourself service
precautions
If you perform maintenance by yourself,
be sure to follow the correct procedure
given in this section.
You should be aware that improper or incomplete servicing may result in operating
problems.
Performing
do-it-yourself
maintenance
during the warranty period may affect your
warranty coverage. Read the separate
Toyota Warranty statement for details and
suggestions.
This part gives instructions only for those
items that are relatively easy for an owner
to perform. As explained in Section 6,
there are still a number of items that must
be done by a qualified technician with
special tools.

CAUTION

 When the engine is running, keep
hands, clothing, and tools away
from the moving fan and engine
drive
belts.
(Removing
rings,
watches, and ties is advisable.)

 Right

after driving, the engine
compartment-the engine, radiator,
exhaust manifold, power steering
fluid reservoir and spark plug
boots, etc.-will be hot. So be careful not to touch them. Oil, fluids
and spark plugs may also be hot.

 If the engine is hot, do not remove
the radiator cap or loosen the drain
plugs to prevent burning yourself.

For information on tools and parts for do-
it-yourself maintenance, see "Parts and
tools" on page 293.

 Do not leave anything that may

Utmost care should be taken when working on your vehicle to prevent accidental
injury. Here are a few precautions that
you should be especially careful to observe:

 Do not smoke, cause sparks or al-

burn easily, such as paper or rags,
in the engine compartment.
low open flames around fuel or the
battery. Their fumes are flammable.

 Be extremely cautious when working on the battery. It contains poisonous and corrosive sulfuric acid.

 Do not get under your vehicle with
just the body jack supporting it. Always use automotive jack stands or
other solid supports.
 Be sure that the ignition is off if
you work near the electric cooling
fan or radiator grille. With the ignition on, the electric cooling fan will
automatically start to run if the air
conditioning is on.
 Use eye protection whenever you
work on or under your vehicle
where you may be exposed to flying
or falling material, fluid spray, etc.
 Used engine oil contains potentially
harmful contaminants which may
cause skin disorders such as inflammation or skin cancer, so care
should be taken to avoid prolonged
and repeated contact with it. To remove used engine oil from your
skin, wash thoroughly with soap
and water.
 Do not leave used oil within the
reach of children.

## p.293 Parts and tools

Parts and tools
 Dispose of used oil and filter only
in a safe and acceptable manner.
Do not dispose of used oil and filter in household trash, in sewers or
onto the ground. Call your dealer or
a service station for information
concerning recycling or disposal.

z Do not pry the outer electrode of a
spark plug against the center electrode.
z Use only spark plugs of the specified type. Using other types will
cause engine damage, loss of performance or radio noise.

NOTICE

z Do not reuse iridium-tipped spark
plugs by cleaning or regapping.

z Remember that battery and ignition
cables carry high currents or voltages. Be careful of accidentally
causing a short circuit.

z Do not overfill automatic transmission fluid, transfer oil and power
steering fluid, or the transmission,
transfer and power steering could
be damaged.

z Add only "Toyota Super Long Life
Coolant" or similar high quality ethylene glycol based non-silicate,
non-amine, non-nitrite and non-borate coolant with long-life hybrid
organic acid technology to fill the
radiator. "Toyota Super Long Life
Coolant" is a mixture of 50% coolant and 50% deionized water.
z If you spill some of the coolant, be
sure to wash it off with water to
prevent it from damaging the parts
or paint.

z Do not drive with the air cleaner
filter removed, or excessive engine
wear could result. Also backfiring
could cause a fire in the engine
compartment.
z Be careful not to scratch the glass
surface with the wiper frame.
z When closing the engine hood,
check to see that you have not forgotten any tools, rags, etc.

Here is a list of parts and tools you will
need to perform do-it-yourself maintenance. Remember all Toyota parts are designed in metric sizes, so your tools must
be metric.
CHECKING THE ENGINE OIL LEVEL
Parts (if level is low):

 "Toyota Genuine Motor Oil" or equivalent. See "Checking the engine oil level" on page 296 for instructions.

Tools:

 Rag or paper towel
 Funnel (only for adding oil)
CHECKING THE ENGINE COOLANT LEVEL
Parts (if level is low):

 "Toyota Super Long Life Coolant" or

similar high quality ethylene glycol
based non-silicate, non-amine, non-nitrite, and non-borate coolant with long-
life hybrid organic acid technology.
"Toyota Super Long Life Coolant" is a
mixture of 50% coolant and 50% deionized water.

z Do not allow dirt or anything else
to fall through the plug holes.

## p.294 Tools:

Tools:

CHECKING AND REPLACING FUSES

 Funnel (only for adding coolant)

Parts (if replacement is necessary):

CHECKING BRAKE FLUID

 Fuse with same amperage rating as
original

Parts (if level is low):

 SAE J1703 or FMVSS No.116 DOT 3
brake fluid

Parts:

 Water
 Washer fluid containing antifreeze (for

Tools:

 Rag or paper towel
 Funnel (only for adding fluid)

winter use)

Tools:

CHECKING POWER STEERING FLUID

 Funnel

Parts (if level is low):
Automatic transmission fluid
or III

DEXRON

II

 Bulb with same number and wattage
rating as original (See charts in "Replacing light bulbs" on page 315.)

 Rag or paper towel
 Funnel (only for adding fluid)
CHECKING BATTERY CONDITION
Tools:

clamp bolts)

REPLACING LIGHT BULBS
Parts:

Tools:

 Warm water
 Baking soda
 Grease
 Conventional

ADDING WASHER FLUID

wrench

(for

terminal

Tools:

 Screwdriver

# Section 7-2: Do it yourself maintenance, Engine and Chassis

## p.295 SECTION

SECTION

7- 2

DO-IT-YOURSELF MAINTENANCE
Engine and Chassis
Checking the engine oil level . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 296
Checking the engine coolant level . . . . . . . . . . . . . . . . . . . . . . . . . . . . 298
Checking the radiator and condenser . . . . . . . . . . . . . . . . . . . . . . . . . 299
Checking brake fluid . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 300
Checking power steering fluid . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 301
Checking tire inflation pressure . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 301
Checking and replacing tires . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 304
Rotating tires . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 306
Installing snow tires and chains . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 306
Replacing wheels . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 308
Aluminum wheel precautions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 309

## p.296 Checking the engine oil level

Checking the engine oil level
Low level

NOTICE

Full level

Be careful not to drop engine oil on
the vehicle components.
If the oil level is below or only slightly
above the low level, add engine oil of
the same type as already in the engine.

Add oil

O.K.

Remove the oil filler cap and add engine
oil in small quantities at a time, checking
the dipstick. We recommend that you use
a funnel when adding the oil.

Too full

With the engine at operating temperature and turned off, check the oil level
on the dipstick.
1. To get a correct reading, the vehicle
should be on level ground. After turning
off the engine, wait a few minutes for
the oil to drain back into the bottom of
the engine.
2. Pull the dipstick out, hold a rag under
the end and wipe it clean.

3. Standing up on the left side of the
vehicle, reinsert the dipstick in the direction so that the "ENGINE OIL" on
top should be read correctly and push
it in as far as it will go, or the reading
will not be correct.
4. Pull the dipstick out and look at the oil
level while holding a rag under the
end.

CAUTION
Be careful not to touch the hot exhaust manifold.

The approximate quantity of oil needed to
raise the level between low and full on the
dipstick is indicated below for reference.
When the level reaches within the correct
range, install the filler cap hand-tight.
Oil quantity, L (qt., Imp.qt.):
1.5 (1.6, 1.3)

NOTICE
z Be careful not to spill engine oil on
the vehicle components.
z Avoid overfilling, or
could be damaged.

the

engine

z Check the oil level on the dipstick
once again after adding the oil.

## p.297 ENGINE OIL SELECTION

ENGINE OIL SELECTION
"Toyota Genuine Motor Oil" is used in
your Toyota vehicle. Use Toyota approved
"Toyota Genuine Motor Oil" or equivalent
to satisfy the following grade and viscosity.
Oil grade:

SAE 5W-30 is the best choice for good
fuel economy, and good starting in cold
weather.
If SAE 5W-30 oil is not available, SAE
10W-30 oil may be used. However, it
should be replaced with SAE 5W-30 at
the next oil change.

API grade, SL "Energy-Conserving" or
ILSAC multigrade engine oil
Recommended viscosity:
SAE 5W-30
API service symbol

Temperature range anticipated before next
oil change

ILSAC certification mark

## p.298 Checking the engine coolant

Checking the engine coolant
level
Oil identification marks

Look at the see-through coolant reservoir when the engine is cold. The coolant level is satisfactory if it is between
the "FULL" and "LOW" lines on the
reservoir. If the level is low, add the
coolant. (For the coolant type, see
"Coolant type selection" described below.)

Either or both API registered marks are
added to some oil containers to help
you select the oil you should use.
The API Service Symbol is located anywhere on the outside of the container.
The top portion of the label shows the oil
quality by API (American Petroleum Institute) designations such as SL. The center
portion of the label shows the SAE viscosity grade such as SAE 5W-30. "Energy-
Conserving" shown in the lower portion,
indicates that the oil has fuel-saving capabilities.
The ILSAC (International Lubricant Standardization and Approval Committee) Certification Mark is displayed on the front of
the container.

The coolant level in the reservoir will vary
with engine temperature. However, if the
level is on or below the "LOW" line, add
coolant. Bring the level up to the "FULL"
line.
To ensure excellent lubrication performance for your engine, "Toyota Genuine
Motor Oil" is available, which has been
specifically tested and approved for all
Toyota engines.
Please contact your Toyota dealer for further details about "Toyota Genuine Motor
Oil".

If the coolant level drops within a short
time after replenishing, there may be a
leak in the system. Visually check the
radiator, hoses, radiator cap and drain
cock and water pump.
If you can find no leak, have your Toyota
dealer test the cap pressure and check
for leaks in the cooling system.

CAUTION
To prevent burning yourself, do not
remove the radiator cap when the engine is hot.

## p.299 Checking the

Checking the
condenser

radiator

and

If any of the above parts are extremely
dirty or you are not sure of their condition, take your vehicle to a Toyota dealer.

Coolant type selection
Use of improper coolants may damage
your engine cooling system.
Only use "Toyota Super Long Life Coolant"
or similar high quality ethylene glycol
based non-silicate, non-amine, non-nitrite,
and non-borate coolant with long-life
hybrid organic acid technology. (Coolant
with
long-life
hybrid
organic
acid
technology is a combination of low
phosphates and organic acids.)

To prevent burning yourself, be careful not to touch the radiator or condenser when the engine is hot.

"Toyota Super Long Life Coolant" is a mixture of 50% coolant and 50% deionized
water. This coolant provides protection
down to about -35°C (-31°F).

To prevent damage to the radiator
and condenser, do not perform the
work by yourself.

NOTICE
Do not use plain water alone.

CAUTION

NOTICE
Toyota recommends "Toyota Super Long
Life Coolant", which has been tested to
ensure that it will not cause corrosion nor
result in malfunction of your engine coolant system with proper usage. "Toyota Super Long Life Coolant" is formulated with
long-life hybrid organic acid technology
and has been specifically designed to
avoid engine cooling system malfunction
on Toyota vehicles.
Please contact your Toyota dealer for further details.

## p.300 Checking brake fluid

Checking brake fluid
If the level is low, add SAE J1703 or
FMVSS No. 116 DOT 3 brake fluid to
the brake reservoir.
Refilling brake fluid:
1. Turn the ignition switch off.
2. Depress the brake pedal more than 40
times.
3. Remove the reservoir cap by hand.
Add brake fluid up to the "MAX" line.
If you do not follow the procedure above,
the reservoir may overflow.
To check the fluid level, simply look at
the see-through reservoir. The level
should be between the "MAX" and
"MIN" lines on the reservoir.
It is normal for the brake fluid level to go
down slightly as the brake pads wear or
when the fluid level in the accumulator is
high.
If the reservoir needs frequent refueling,
it may indicate a serious mechanical problem.

Use only newly opened brake fluid. Once
opened, brake fluid absorbs moisture from
the air, and excess moisture can cause a
dangerous loss of braking.

CAUTION
Take care when filling the brake fluid
reservoir because brake fluid can
harm your hands or eyes. If fluid gets
on your hands or in your eyes, flush
the affected area with clean water immediately. If you still feel uncomfortable with your hands or eyes, go to
the doctor.

NOTICE
If you spill the fluid, be sure to wipe
it off to prevent it from damaging the
parts or painting.

## p.301 Checking tire inflation pressure

Checking tire inflation pressure

Checking power steering fluid

If hot
O.K.

If hot
add

Close

Open

If cold
O.K.

If cold
add

Check the fluid level on the dipstick. If
necessary, add automatic transmission
fluid DEXRONII or III.
If the vehicle has been driven around 80
km/h (50 mph) for 20 minutes (a little
more in frigid temperatures), the fluid is
hot (60 C-80 C or 140 F-175 F). You
may also check the level when the fluid
is
cold
(about
room
temperature,
10 C-30 C or 50 F-85 F) if the engine
has not been run for about five hours.

Clean all dirt from outside of the reservoir
tank and look at the fluid level. If the fluid
is cold, the level should be in the "COLD"
range. Similarly, if it is hot, the fluid level
should be in the "HOT" range. If the level
is at the low side of either range, add
automatic transmission fluid DEXRONII
or III to bring the level within the range.
To remove the reservoir cap, turn it counterclockwise and lift up. To reinstall it,
turn it clockwise. After replacing the filler
cap, visually check the steering box case,
vane pump and hose connections for
leaks or damage.
CAUTION
The reservoir tank may be hot so be
careful not to burn yourself.

NOTICE
Avoid overfilling, or the power steering could be damaged.

## p.302 Keep your tire inflation pressures

Keep your tire inflation pressures
at the proper level.
The recommended cold tire inflation
pressures, tire sizes and the combined weight of occupants and cargo
(vehicle capacity weight) are described on page 328 and 324. They
are also described on the tire and
loading information label as shown.
You should check the tire inflation
pressures every two weeks, or at
least once a month. And do not forget
the spare!
The following instructions for
checking tire inflation pressure
should be observed:
 The
pressure
should
be
checked only when the tires are
cold. If your vehicle has been
parked for at least 3 hours and has
not been driven for more than 1.5
km or 1 mile since, you will get
an accurate cold tire inflation pressure reading.

 Always use a tire inflation pressure gauge. The appearance of
a tire can be misleading. Besides,
tire inflation pressures that are
even just a few pounds off can degrade ride and handling.
 Do not bleed or reduce tire
inflation pressure after driving.
It is normal for the tire inflation
pressure to be higher after driving.
 Never exceed the vehicle capacity weight. The passenger and
luggage weight should be located
so that the vehicle is balanced.

Tire inflation
pressure gauge

INSPECTION AND ADJUSTMENT
PROCEDURE
1. Remove the tire valve cap.
2. Press the tip of the tire inflation
pressure gauge to the tire valve.
3. Read the pressure using a graduation of the gauge.
4. In case that the tire inflation pressure is not within the prescribed
range, insert the compressed air
from the valve. In case of applying
too much air, press the center of
the valve and release the air to adjust.

## p.303 5. After completing the tire inflation

5. After completing the tire inflation
pressure measurement and adjustment, apply soap water to the
valve and check the leakage.
6. Install the tire valve cap.
If the gauge and the air pump are not
available, have your vehicle checked
by your Toyota dealer.
CAUTION
Be sure to reinstall the tire valve
caps. Without the valve caps, dirt
or moisture could get into the
valve core and cause air leakage.
If the caps have been lost, have
new ones put on as soon as possible.
Incorrect tire inflation pressure may
waste fuel, reduce the comfort of driving, reduce tire life and make your vehicle less safe to drive.
If a tire frequently needs refilling,
have it checked by your Toyota dealer.

CAUTION
Keep your tires properly inflated.
Otherwise, the following conditions may occur and cause an accident resulting in death or serious injuries.
Low tire pressure (underinflation)-
 Excessive wear
 Uneven wear
 Poor handling
 Possibility of blowouts from an
overheated tire
 Poor sealing of the tire bead
 Wheel deformation and/or tire
separation
 A greater possibility of tire
damage from road hazards

High tire pressure (overinflation)-
 Poor handling
 Excessive wear
 Uneven wear
 A greater possibility of tire
damage from road hazards

## p.304 Checking and replacing tires

Checking and replacing tires
Tread wear indicator

CHECKING YOUR TIRES
Check the tire's tread for tread
wear indicators. If the indicators
show, replace the tires. The location of the tread wear indicators is
shown by the "TWI" or "Δ " marks,
etc., molded on the sidewall of
each tire.

The tires on your Toyota have built-in
tread wear indicators to help you
know when the tires need replacement. When the tread depth wears to
1.6 mm (0.06 in.) or less, the indicators will appear. If you can see the
indicators in two or more adjacent
grooves, the tire should be replaced.
The lower the tread, the higher the
risk of skidding.
The effectiveness of snow tires is
lost if the tread wears down below
4 mm (0.16 in.).
If you have tire damage such as
cuts, splits, cracks deep enough to
expose the fabric, or bulges indicating internal damage, the tire
should be replaced.
If a tire often goes flat or cannot be
properly repaired due to the size or
location of a cut or other damage, it
should be replaced. If you are not
sure, consult with your Toyota dealer.

If air loss occurs while driving, do not
continue driving. Driving even a short
distance can damage a tire beyond
repair.
Any tires which are over 6 years
old must be checked by a qualified
technician even if damage is not
obvious.
Tires deteriorate with age even if they
have never or seldom been used.
This also applies to the spare tire and
tires stored for future use.
REPLACING YOUR TIRES
When replacing a tire, use a tire of
the same size and construction,
and the same or greater maximum
load as the originally installed
tires. Also, all the tires must be the
same brand and have the same
tread patterns.

## p.305 Using any other size or type of tire

Using any other size or type of tire
may seriously affect handling, ride,
speedometer/odometer calibration,
ground clearance, and clearance between the body and tires or snow
chains.
Check that the maximum load of the
replaced tire is greater than 1/2 of the
Gross Axle Weight Ratings (GAWR)
of either the front axle or the rear
axle, whichever is greater. As for the
maximum load of the tire, see the load
limit at maximum cold tire inflation
pressure mentioned on the sidewall
of the tire, and as for the Gross Axle
Weight Ratings (GAWR), see the Certification Label. For details about the
sidewall of the tire and the Certification Label, see pages 222 and 220.

CAUTION
Observe the following instructions. Otherwise, an accident
may occur resulting in death or
serious injuries.
 Do not mix radial, bias belted,
or bias-ply tires on your vehicle, as this may cause dangerous handling characteristics resulting in loss of control.
 Do not use tires other than the
manufacturer's recommended
size, as this may cause dangerous handling characteristics
resulting in loss of control.
 Do not use tires of different
brands, sizes, construction or
tread patterns, as this may
cause dangerous handling
characteristics resulting in
loss of control.

Toyota recommends all four tires,
or at least both front or rear tires
be replaced as a set.
See "If you have a flat tire" on page
257 for tire change procedure.
When a tire is replaced, the wheel
should always be balanced.
An unbalanced wheel may affect vehicle handling and tire life. Wheels
can get out of balance with regular
use and should therefore be balanced
occasionally.
When replacing a tubeless tire, the
air valve should also be replaced
with a new one.

## p.306 Installing

Installing
chains

Rotating tires
See "If you have a flat tire" on page
257 for tire change procedure.
When rotating tires, check for uneven
wear and damage. Abnormal wear is
usually caused by incorrect tire inflation pressure, improper wheel alignment, out-of-balance wheels, or severe braking.

To equalize tire wear and help extend tire life, Toyota recommends
that you rotate your tires according to the maintenance schedule.
(For scheduled maintenance information, please refer to the "Scheduled Maintenance Guide" or "Owner's
Manual
Supplement".)
However, the most appropriate timing for tire rotation may vary according to your driving habits and
road surface conditions.

WHEN TO
CHAINS

snow
USE

tires

SNOW

and

TIRES

OR

Snow tires or chains are recommended
when driving on snow or ice.
On wet or dry roads, conventional tires
provide better traction than snow tires.
SNOW TIRE SELECTION
If you need snow tires, select tires of
the same size, construction and load
capacity as the originally installed tires.
Also, all the tires must be the same
brand and have the same tread patterns.
Do not use tires other than those mentioned above. Do not install studded tires
without first checking local regulations for
possible restrictions.

## p.307 CAUTION

CAUTION
Observe the following instructions.
Otherwise, an accident may occur resulting in death or serious injuries.

 Do not use snow tires other than
the manufacturer's recommended
size, as this may cause dangerous
handling characteristics resulting in
loss of control.

 Do not use snow tires of different
brands, sizes, construction or tread
patterns, as this may cause dangerous handling characteristics resulting in loss of control.

SNOW TIRE INSTALLATION
Snow tires should be installed on all
wheels.
Installing snow tires on the rear wheels
only can lead to an excessive difference
in road grip capability between the front
and rear tires which could cause loss of
vehicle control.

Side chain

Cross chain

When storing removed tires, you should
store them in a cool dry space.
Mark the direction of rotation and be sure
to install them in the same direction when
replacing.

CAUTION

 Do not drive with the snow tires
incorrectly inflated.

 Never drive over 105 km/h (65 mph)
with any type of snow tires.

TIRE CHAIN SELECTION
Use the tire chains of correct size.
Use the following type chains.
For P275/65R17 113S and P275/60R18
111H tires
mm (in.)
A Diameter of side chain:
3.5 (0.14)
B Diameter of cross chain: 4.0 (0.16)
Regulations regarding the use of tire
chains vary according to location or
type of road, so always check local regulations before installing chains.

## p.308 Replacing wheels

Replacing wheels
NOTICE

CAUTION

If the wrong combination of tire and
chain is used, the chains could damage the vehicle body.

 Do not exceed 50 km/h (30 mph) or

CHAIN INSTALLATION

 Drive

Install the chains on the rear tires as
tightly as possible. Do not use tire
chains on the front tires. Retighten
chains after driving 0.5 - 1.0 km (1/4 -
1/2 mile).
When installing chains on your tires, carefully follow the instructions of the chain
manufacturer.
If wheel covers are used, they will be
scratched by the chain band, so remove
the covers before putting on the chains.

the chain manufacturer's recommended speed limit, whichever is
lower.
carefully avoiding bumps,
holes, and sharp turns, which may
cause the vehicle to bounce.

 Avoid sharp turns or locked-wheel
braking, as use of chains may adversely affect vehicle handling.

 When driving with chains installed,
be sure to drive carefully. Slow
down before entering curves to
avoid losing control of the vehicle.
Otherwise an accident may occur.

WHEN TO REPLACE YOUR WHEELS
If you have wheel damage such as
bending, cracks or heavy corrosion, the
wheel should be replaced.
If you fail to replace a damaged wheel,
the tire may slip off the wheel or cause
loss of handling control.
WHEEL SELECTION
When replacing wheels, care should be
taken to ensure that the wheels are replaced by ones with the same load capacity, diameter, rim width, and offset.
Correct replacement wheels are available
at your Toyota dealer.
A wheel of a different size or type may
adversely affect handling, wheel and bearing life, brake cooling, speedometer/odometer calibration, stopping ability, headlight
aim, bumper height, vehicle ground clearance, and tire or snow chain clearance to
the body and chassis.

## p.309 Replacement with used wheels is not recommended as they may have been subjected 

Replacement with used wheels is not recommended as they may have been subjected to rough treatment or high mileage
and could fail without warning. Also, bent
wheels which have been straightened may
have structural damage and therefore
should not be used. Never use an inner
tube in a leaking wheel which is designed
for a tubeless tire.

CAUTION
Observe the following instructions.
Otherwise, an accident may occur resulting in death or serious injuries.

 Do not use wheels other than the
manufacturer's recommended size,
as this may cause dangerous handling characteristics resulting in
loss of control.

 Do not use wheels of different

Aluminum wheel precautions
 When installing aluminum wheels,

check that the wheel nuts are tight
after driving your vehicle the first 1600
km (1000 miles).

 If

you have rotated, repaired, or
changed your tires, check that the
wheel nuts are still tight after driving
1600 km (1000 miles).

 When using tire chains, be careful not
to damage the aluminum wheels.

 Use

only Toyota wheel nuts and
wrench designed for your aluminum
wheels.

 When balancing your wheels, use only

Toyota balance weights or equivalent
and a plastic or rubber hammer.

 As with any wheel, periodically check

your aluminum wheels for damage. If
damaged, replace immediately.

brands, sizes and types, as this
may cause dangerous handling
characteristics resulting in loss of
control.

## p.310 

# Section 7-3: Do it yourself maintenance, Electrical components

## p.311 SECTION

SECTION

7- 3

DO-IT-YOURSELF MAINTENANCE
Electrical components
Checking battery condition . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 312
Battery recharging precautions . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 313
Checking and replacing fuses . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 314
Adding washer fluid . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 315
Replacing light bulbs . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 315

## p.312 Checking battery condition-

Checking battery condition-
-Precautions

-Checking battery exterior

CAUTION

 If electrolyte gets on your skin,

BATTERY PRECAUTIONS

thoroughly wash the contact area. If
you feel pain or burning, get medical attention immediately.

The battery produces flammable and
explosive hydrogen gas.

 Do not cause a spark from the battery with tools.

 Do not smoke or light a match near
the battery.
The electrolyte contains poisonous
and corrosive sulfuric acid.

 Avoid contact with eyes, skin or
clothes.

 Never ingest electrolyte.
 Wear protective safety glasses when
working near the battery.

 Keep children away from the battery.
EMERGENCY MEASURES

 If electrolyte gets in your eyes,
flush your eyes with clean water
immediately and get immediate
medical attention. If possible, continue to apply water with a sponge
or cloth while en route to the medical office.

Terminals

Ground cable

 If electrolyte gets on your clothes,
there is a possibility of its soaking
through to your skin, so immediately take off the exposed clothing and
follow the procedure above, if necessary.

 If you accidentally swallow electrolyte, drink a large quantity of water
or milk. Follow with milk of magnesia, beaten raw egg or vegetable
oil. Then go immediately for emergency help.

Hold-down clamp

Check the battery for corroded or loose
terminal connections, cracks, or loose
hold-down clamp.
a. If the battery is corroded, wash it off
with a solution of warm water and baking soda. Coat the outside of the terminals with grease to prevent further corrosion.
b. If the terminal connections are loose,
tighten their clamp nuts-but do not
overtighten.
c. Tighten the hold-down clamp only
enough to keep the battery firmly in
place. Overtightening may damage the
battery case.

## p.313 -Checking battery condition

-Checking battery condition
NOTICE
z Be sure the engine and all accessories are off before performing maintenance.
z When checking the battery, remove
the ground cable from the negative
terminal ("-" mark) first and reinstall it last.

Type A
Green

Dark

Clear or
light yellow

During recharging, the battery is producing hydrogen gas.
Therefore, before recharging:
1. If recharging with the battery installed
on the vehicle, be sure to disconnect
the ground cable.

Type B
Blue

White

Red

z Be careful not to cause a short circuit with tools.
z Take care no solution gets into the
battery when washing it.

2. Be sure the power switch on the recharger is off when connecting the
charger cables to the battery and when
disconnecting them.

CAUTION

 Always charge the battery in an un-

CHECKING BY INDICATOR
If the battery terminal is disconnected
or the battery is run down, the moon
roof may not operate automatically and
the jam protection function will not operate
correctly after you reconnect, replace or
recharge the battery with the moon roof
slide-opened or tilted up. In any of these
cases, you should return the moon roof to
normal. To return the moon roof to normal,
see "Electric moon roof" on page 31.

Battery recharging precautions

Check the battery condition by the indicator color.
Indicator color

Condition

Type A

Type B

Green

Blue

Good

White

Charging necessary.
Have battery
checked by your
Toyota dealer.

Dark
Clear or
light
yellow

Red

Have battery
checked by your
Toyota dealer.

confined area. Do not charge the
battery in a garage or closed room
where there is not sufficient ventilation.

 Only do a slow charge (5 A or
less). Charging at a quicker rate is
dangerous. The battery may explode, causing personal injuries.

NOTICE
Never recharge the battery while the
engine is running. Also, be sure all
accessories are turned off.

## p.314 Checking and replacing fuses

Checking and replacing fuses
Type A fuses can be pulled out by the
pull-out tool. The location of the pull-out
tool is shown in the illustration.

Type A

If you are not sure whether the fuse has
blown, try replacing the suspected fuse
with one that you know is good.
If the fuse has blown, push a new fuse
into the clip.

Good

Only install a fuse with the amperage rating designated on the fuse box lid.

Blown

Type B

Good

Blown

Type C

If the headlights or other electrical
components do not work, check the
fuses. If any of the fuses are blown,
they must be replaced.
See "Fuse locations" on page 291 for
locations of the fuses.
Turn the ignition switch and inoperative
component off. Pull the suspected fuse
straight out and check it.

Good

Blown

Determine which fuse may be causing the
problem. The lid of the fuse box shows
the name of the circuit for each fuse. See
page on 329 for the functions controlled
by each circuit.

If you do not have a spare fuse, in an
emergency you can pull out the "RADIO",
"DOME" or "RR A.C" fuse, which may be
dispensable for normal driving, and use it
if its amperage rating is the same.
If you cannot use one of the same amperage, use one that is lower, but as close
to the rating as possible. If the amperage
is lower than that specified, the fuse
might blow out again but this does not
indicate anything wrong. Be sure to get
the correct fuse as soon as possible and
return the substitute to its original clip.
It is a good idea to purchase a set of
spare fuses and keep them in your vehicle for emergencies.

## p.315 If the new fuse immediately blows out,

If the new fuse immediately blows out,
there is a problem with the electrical system. Have your Toyota dealer correct it as
soon as possible.

CAUTION
Never use a fuse with a higher amperage rating, or any other object, in
place of a fuse. This may cause extensive damage and possibly a fire.

Adding washer fluid

Replacing light bulbs-

If any washer does not work, the washer tank may be empty. Add washer
fluid.

The following illustrations show how to
gain access to the bulbs. When replacing
a bulb, make sure the ignition switch and
light switch are off. Use bulbs with the
wattage ratings given in the table.

You may use plain water as washer fluid.
However, in cold areas where temperatures range below freezing point, use
washer fluid containing antifreeze. This
product is available at your Toyota dealer
and most auto parts stores. Follow the
manufacturer's directions for how much to
mix with water.

NOTICE
z Do not use engine antifreeze or any
other substitute because it may
damage your vehicle's paint.
z Do not fill washer fluid over the
"NORMAL" level.

CAUTION

 To prevent burning yourself, do not
replace the light bulbs while they
are hot.

 Halogen bulbs have pressurized gas
inside and require special handling.
They can burst or shatter if
scratched or dropped. Hold a bulb
only by its plastic or metal case.
Do not touch the glass part of a
bulb with bare hands.

NOTICE
Only use a bulb of the listed type.

## p.316 -Headlights

-Headlights
The inside of the lens of exterior lights
such as headlights may temporarily fog up
when the lens becomes wet in the rain or
in a car wash. This is not a problem
because the fogging is caused by the
temperature difference between the outside
and inside of the lens, just like the windshield fogs up in the rain. However, if
there is a large drop of water on the
inside of the lens, or if there is water
pooled inside the light, contact your
Toyota dealer.
Bulb
No.

W

Type

Headlights
(high)

9005

60

A

Headlights
(low)

9006

51

B

Front turn signal
and
front
side 1157NA
marker lights

27/8

C

Front fog lights

9006

51

B

Parking lights

-

5

D

Rear turn signal
lights

7440

21

G

Stop/tail lights

7443

21/5

D

Light bulbs

Light bulbs

Bulb
No.

W

Type

Back-up lights

7440

21

D

License plate lights

-

5

D

Interior lights

-

8

E

Personal lights
Type A
Type B

-
-

5
8

F
E

Glove box light

-

1.4

D

Door courtesy
lights

-

3

D

Vanity lights

-

1.5

E

A : HB3 halogen bulbs
B : HB4 halogen bulbs
C : Single end bulbs (amber)
D : Wedge base bulbs
E : Double end bulbs
F : Single end bulbs
G : Wedge base bulbs (amber)

1. Open the hood.
LEFT-HAND HEADLIGHT: Remove the
washer inlet.
Be careful not to spill the washer fluid
over the "NORMAL" level.
Do not place the washer inlet on the engine or battery.

## p.317 2. Turn the bulb base counterclockwise

2. Turn the bulb base counterclockwise
to the front of the vehicle as shown.

3. Pull the bulb out of the bulb base.
If the connector is tight, wiggle it.

4. Install a new bulb base by turning it
clockwise to the front of the vehicle.
LEFT-HAND HEADLIGHT:
washer inlet securely.

Install

the

Aiming is not necessary after replacing
the bulb. When aiming adjustment is necessary, contact your Toyota dealer.

## p.318 -Front fog lights

-Front fog lights

1. Turn the bulb base counterclockwise
to the front of the vehicle as shown.

2. Pull the bulb out of the bulb base.
If the connector is tight, wiggle it.

3. Install a new bulb base by turning it
clockwise to the front of the vehicle.
Aiming is not necessary after replacing
the bulb. When aiming adjustment is necessary, contact your Toyota dealer.

## p.319 -Front turn signal and front

-Front turn signal and front
side marker lights

-Parking lights

Use a Phillips-head screwdriver.

Use a Phillips-head screwdriver.

## p.320 -Stop and tail lights

-Stop and tail lights

Use a Phillips-head screwdriver.

## p.321 -Rear turn signal, stop/tail,

-Rear turn signal, stop/tail,
and back-up lights

Use a flat-bladed screwdriver.

-License plate lights

a: Back-up light
b: Rear turn signal light
c: Stop/tail light

## p.322 

# Section 8: Specifications

## p.323 SECTION

SECTION

8

SPECIFICATIONS
Dimensions and weights . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 324
Engine . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 324
Fuel . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 324
Service specifications . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 325
Tires . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 328
Fuses . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 329

## p.324 Dimensions and weights

Dimensions and weights

Engine

Fuel

Overall length

mm (in.)

4890 (192.5)

Overall width

mm (in.)

1940 (76.4)

Model:
2UZ-FE

Overall height

mm (in.)

1875 (73.8)∗1

Wheelbase

mm (in.)

2850 (112.2)

Front tread

mm (in.)

1620 (63.8)

Rear tread

mm (in.)

1615 (63.6)

Fuel type:
Unleaded gasoline, Octane Rating 87
(Research Octane Number 91) or higher.
For improved vehicle performance, the
use of premium unleaded gasoline with
an Octane Rating of 91 (Research Octane Number 96) or higher is recommended.

Vehicle capacity weight
(occupants + luggage)
kg (lb.)

545 (1200)

Towing capacity
(trailer weight + cargo weight)
kg (lb.)
2948 (6500)
∗1 :

Unladen vehicle

Type:
8 cylinder V type, 4 cycle, gasoline
Bore and stroke, mm (in.):
94.0
84.0 (3.70
3.30)
Displacement, cm3 (cu. in.):
4664 (284.6)

Fuel tank capacity, L (gal., Imp.gal.):
96 (25.4, 21.1)

## p.325 Service specifications

Service specifications
ENGINE
Valve clearance (engine cold), mm (in.):
Intake
0.15 - 0.25 (0.006 - 0.010)
Exhaust 0.25 - 0.35 (0.010 - 0.014)

Recommended viscosity:
SAE 5W-30

Spark plug type:
DENSO SK20R11
NGK
IFR6A11

COOLING SYSTEM
Total capacity, L (qt., Imp.qt.)
Without rear heater
14.7 (15.5, 12.9)
With rear heater
15.4 (16.3, 13.6)
Coolant type:
"Toyota Super Long Life Coolant" is used
in your Toyota vehicle at factory fill. In
order to avoid technical problems, only use
"Toyota Super Long Life Coolant" or similar
high quality ethylene glycol based non-silicate, non-amine, non-nitrite, and non-borate coolant with long-life hybrid organic
acid technology. (Coolant with long-life hybrid organic acid technology is a combination of low phosphates and organic acids.)

Spark plug gap, mm (in.):
1.1 (0.043)
ENGINE LUBRICATION
Oil capacity (drain and refill),
Imp.qt.)
With filter
6.8 (7.2, 6.0)
Without filter
6.4 (6.8, 5.6)

L

(qt.,

Oil grade:
"Toyota Genuine Motor Oil" is used in
your Toyota vehicle. Use Toyota approved "Toyota Genuine Motor Oil" or
equivalent to satisfy the following grade
and viscosity.
Oil grade:
API grade, SL "Energy-Conserving" or
ILSAC multigrade engine oil

Temperature range anticipated before next
oil change

Do not use plain water alone.

Please contact your Toyota dealer for further details.

Please contact your Toyota dealer for further details.
BATTERY
Open voltage∗ at 20 C (68 F):
12.6 - 12.8 V
Fully charged
12.2 - 12.4 V
Half charged
11.8 - 12.0 V
Discharged
∗:

Voltage that is checked 20 minutes after the key is removed with all the lights
turned off
Charging rates:
5 A max.

## p.326 AUTOMATIC TRANSMISSION

AUTOMATIC TRANSMISSION
Fluid capacity (drain and refill), L (qt.,
Imp.qt.)
Up to 3.0 (3.2, 2.6)
Fluid type:
"Toyota Genuine ATF WS"
Change automatic transmission fluid
only as necessary.
Generally, it is necessary to change automatic transmission fluid only if your
vehicle is driven under one of the Special Operating Conditions listed in your
"Scheduled
Maintenance
Guide"
or
"Owner's Manual Supplement". When
changing the automatic transmission
fluid, use only "Toyota Genuine ATF
WS" (ATF JWS3324 or NWS9638) to aid
in assuring maximum transmission performance.
Notice: Using automatic transmission
fluid other than "Toyota Genuine ATF
WS" may cause deterioration in shift
quality, locking up of your transmission accompanied by vibration, and
ultimately
damage
the automatic
transmission of your vehicle.

TRANSFER

CHASSIS LUBRICATION

Oil capacity, L (qt., Imp.qt.)
1.3 (1.4, 1.1)

Wheel bearings:
Lithium base
NLGI No.2

Oil type:
Gear oil API GL-4 or GL-5
Recommended oil viscosity:
SAE 75W-90
DIFFERENTIAL
Oil capacity, L (qt., Imp.qt.):
Front
1.6 (1.7, 1.4)
Rear

3.3 (3.5, 2.9)

Oil type:
Hypoid gear oil API GL-5
Recommended oil viscosity:
Above -18 C (0 F)
SAE 90
Below -18 C (0 F)
SAE 80W or 80W-90

wheel

bearing

grease,

Front drive shaft thrust bushings:
Synthetic oil and lithium soap
chassis grease, NLGI No.1

base

Propeller shafts:
Spiders
Lithium base chassis grease, NLGI
No.2
Slide yoke
Lithium base chassis grease, NLGI
No.2 or Molybdenum-disulfide lithium
base chassis grease, NLGI No.2

## p.327 BRAKES

BRAKES
Minimum pedal clearance when depressed
with the force of 490 N (50 kgf, 110 lbf)
with the engine running, mm (in.):
116 (4.6)
Pedal free play, mm (in.):
1 - 6 (0.04 - 0.24)
Pad wear limit, mm (in.):
1.0 (0.04)
Lining wear limit, mm (in.):
1.0 (0.04)
Parking brake adjustment when pulled with
the force of 196 N (20 kgf, 44 lbf):
4 - 6 clicks
Fluid type:
SAE J1703 or FMVSS No.116 DOT 3
STEERING
Wheel free play:
Less than 40 mm (1.6 in.)
Power steering fluid type:
Automatic transmission fluid DEXRONII
or III

## p.328 Tires

Tires
Tire size and inflation pressure:
kPa (psi)
Tire size
P275/60R18 111H

Front

Rear

Normal driving

Trailer towing

Normal driving

Trailer towing

200 (29)

220 (32)

220 (32)

240 (35)

Wheel size
18

8JJ

Wheel nut torque, N·m (kgf·m, ft·lbf): 131 (13.4, 96.6)
NOTE: For a complete information on tires (e.g. replacing tires or replacing wheels), see "Checking tire inflation pressure"
on page 301 through "Aluminum wheel precautions" on page 309.

## p.329 Fuses

Fuses

Engine compartment

Left side kick panel

Right side kick panel

Fuses

8. HAZ-TRN 15 A: Emergency flashers,

18. BAT 30 A: All components in "ECU-B2"

Turn signal lights

1. ABS NO.2 40 A: Anti-lock brake system

9. ALT-S 7.5 A: Charging system

2. ABS NO.1 50 A: Anti-lock brake system

10. NV-IR 20 A: No circuit

3. AHC 50 A: No circuit

11. FR FOG 15 A: Fog lights

4. ST1 7.5 A: Mutiport fuel injection system/

12. TOWING BRK 30 A: Trailer lights

Sequential multiport fuel injection

19. TEL 7.5 A: No circuit
20. AMP 30 A: Audio system
21. EFI or ECD No.1 25 A: Multiport fuel
injection system/Sequential multiport fuel
injection system

13. HEAD CLNER 20 A: Headlight cleaner

22. AM2 15 A: All components in "IGN"

5. TOWING 30 A: Trailer lights

14. FR-IG 10 A: Charging system

23. ETCS 10 A: Multiport fuel injection sys-

6. MIR HTR 15 A: Outside rear view mirror

15. PANEL 7.5 A: Instrument panel light

defogger

7. RR HTR 10 A: Rear air conditioning system

tem/Sequential multiport fuel injection system

16. TOWING TAIL 30 A: Trailer lights

24. HORN 10 A: Horns

17. TAIL 15 A: Parking lights, Tail lights

25. HEAD

(RH-LWR)

10

A:

Right-hand

headlight (low beam)

## p.330 26. HEAD (LH-LWR) 10 A: Left-hand headlight (low beam)

26. HEAD (LH-LWR) 10 A: Left-hand headlight (low beam)

27. HEAD

(RH-UPR)

20

A:

Right-hand

headlight (high beam)

28. HEAD (LH-UPR) 20 A: Left-hand headlight (high beam)

29. PWR OUTLET 15 A: Power outlets
30. CIG 15 A: Cigarette lighter
31. ACC 7.5 A: Instrument panel light

42. DBL LOCK 15 A: Double lock system

62. GAUGE2 10 A: Back-up lights

43. A/C 15 A: Air conditioning system

63. MET 7.5 A: Gauges and meters

44. STOP 15 A: Stop lights

64. IGN 7.5 A: Multiport fuel injection system/Sequential multiport fuel injection
system

45. OBD-2 7.5 A: On-board diagnosis system

46. IDEL UP 7.5 A: Idle-up system
47. LH SEAT 30 A: Power seat system
48. DOOR 25 A: Power door lock system,
Power windows

32. AM1 7.5 A: Multiport fuel injection system/Sequential multiport fuel injection
system

49. SUN ROOF 25 A: Electronic moon roof

33. DEFOG 20 A: Rear window defogger

51. ECU-B2 10 A: Power door lock system,

34. AHC-B 15 A: Active height control suspension (AHC)

50. RR WIPER 15 A: Rear wiper system
Power window

52. DIFF 20 A: Four-wheel drive system

35. FUEL HTR 20 A: Fuel heater

53. WASHER 15 A: Windshield washer

36. POWER HTR 7.5 A: Power heater

54. RADIO 10 A: Audio system

37. AHC-IG 20 A: Active height control suspension (AHC)

38. EFI or ECD No.2 10 A: Emission control system

55. DOME 10 A: Interior lights
56. VGRS 40 A: Variable gear ratio steering system
57. P/W (FL) 20 A: Power window

39. GAUGE1 10 A: Gauges and meters

58. P/W (RL) 20 A: Power window

40. ECU-IG1 10 A: Multiport fuel injection
system/Sequential multiport fuel injection system

59. WIPER 25 A: Windshield wiper

41. ECU-B1 10 A: Navigation system

61. SEAT HTR 15 A: Seat heater

60. ECU-IG2 10 A: Rear air conditioning
system

65. SECURITY 7.5 A: Theft deterrent system
66. P/W (RR) 20 A: Power window
67. P/W (FR) 20 A: Power window
68. BATT CHARGE 30 A: Trailer charging
system
69. TIL&TEL 20
steering

A:

Tilt

and

telescopic

70. RR A/C 30 A: Rear air conditioning
system
71. RH SEAT 30 A: Power seat system

# Section 9: Reporting safety defects (US) and tire grading

## p.331 SECTION

SECTION

9

REPORTING SAFETY DEFECTS FOR U.S.
OWNERS AND UNIFORM TIRE QUALITY
GRADING
Reporting safety defects for U.S. owners . . . . . . . . . . . . . . . . . . . . . . 332

## p.332 Reporting safety defects for

Reporting safety defects for
U.S. owners
If you believe that your vehicle has
a defect which could cause a crash
or could cause injury or death, you
should immediately inform the National Highway Traffic Safety Administration (NHTSA) in addition to
notifying Toyota Motor Sales,
U.S.A.,
Inc.
(Toll-free:
1-800-331-4331).
If NHTSA receives similar complaints, it may open an investigation, and if it finds that a safety defect exists in a group of vehicles, it
may order a recall and remedy
campaign. However, NHTSA cannot
become involved in individual problems between you, your dealer, or
Toyota Motor Sales, U.S.A., Inc.

To contact NHTSA, you may either
call the Auto Safety Hotline toll-free
at 1-800-424-9393 (or 366-0123
in Washington, D.C. area) or write
to: NHTSA, U.S. Department of
Transportation, Washington, D.C.
20590. You can also obtain other
information about motor vehicle
safety from the Hotline.

# Section 10: Index

## p.333 SECTION

SECTION

10

INDEX

## p.334 A

A
Adding washer fluid . . . . . . . . . . . . . . . . . . 315
Adjustment
Front seats . . . . . . . . . . . . . . . . . . . . . . . . . 36
Seat belt . . . . . . . . . . . . . . . . . . . . . . . . . . . 48
Second seat . . . . . . . . . . . . . . . . . . . . 37 3 8
Third seat . . . . . . . . . . . . . . . . . . . . . . . . . . 42
Air conditioning system . . . . . . . . . . . . . . . 176
Airbags . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 58
Aluminum wheel precautions . . . . . . . . . . 309
Anti-theft steering column lock . . . . . . . . 134
Appearance care
Cleaning the interior . . . . . . . . . . . . . . . . 279
Protecting your Toyota
from corrosion . . . . . . . . . . . . . . . . . . . 276
Washing and waxing . . . . . . . . . . . . . . . . 277
Armrest . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 37
Automatic transmission
Driving with an automatic
transmission . . . . . . . . . . . . . . . . . . . . . 135
Shift lock override button . . . . . . . . . . . . 272
Shift pattern . . . . . . . . . . . . . . . . . . . . . . . 135
Shifting speed . . . . . . . . . . . . . . . . . . . . . 135
Auxiliary box . . . . . . . . . . . . . . . . . . . . . . . . 198
Auxiliary catch, Engine hood . . . . . . . . . . . 27

B
Back door . . . . . . . . . . . . . . . . . . . . . . . . . . . . 25
Back door lock . . . . . . . . . . . . . . . . . . . . . . . . 25

Battery
Checking battery condition . . . . . . . . . . 312
Gas caution . . . . . . . . . . . . . . . . . . . . . . . 312
Handling safety . . . . . . . . . . . . . . . . . . . . 312
Recharging precautions . . . . . . . . . . . . . 313
Winter driving tips . . . . . . . . . . . . . . . . . . 240
Before starting the engine . . . . . . . . . . . . . 236
Brake pad wear limit indicators . . . . . . . . 219
Brake system . . . . . . . . . . . . . . . . . . . . . . . . 215
Brakes
Fluid level . . . . . . . . . . . . . . . . . . . . . . . . . 300
Pad wear limit indicators . . . . . . . . . . . . 219
Parking . . . . . . . . . . . . . . . . . . . . . . . . . . . 142
Break-in tips . . . . . . . . . . . . . . . . . . . . . . . . 209
Brightness control . . . . . . . . . . . . . . . . . . . . 110

C
Car audio system . . . . . . . . . . . . . . . . . . . . 152
Carbon monoxide caution . . . . . . . . . . . . . 213
Cargo and luggage
Capacity . . . . . . . . . . . . . . . . . . . . . . . . . . 230
Distribution . . . . . . . . . . . . . . . . . . . . . . . . 231
Stowage precautions . . . . . . . . . . . . . . . 230
Cassette player . . . . . . . . . . . . . . . . . . . . . . 152
Checking and replacing fuses . . . . . . . . . 314
Checking and replacing tires . . . . . . . . . . 304
Checking brake fluid . . . . . . . . . . . . . . . . . . 300
Checking the engine oil level . . . . . . . . . . 296
Checking the radiator
and condenser . . . . . . . . . . . . . . . . . . . . . 299
Child restraint
Child restraint system . . . . . . . . . . . . . . . 77
Installation . . . . . . . . . . . . . . . . . . . . . . 78, 83

Precautions . . . . . . . . . . . . . . . . . . . . . . . . 76
Types of child restraint system . . . . . . . . 77
Using a top strap . . . . . . . . . . . . . . . . . . . . 92
Cigarette lighter and ashtray . . . . . . . . . . 192
Cleaning the interior . . . . . . . . . . . . . . . . . . 279
Clock . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 188
Coat hooks . . . . . . . . . . . . . . . . . . . . . . . . . . 205
Cold weather
Operation . . . . . . . . . . . . . . . . . . . . . . . . . 240
Compact disc auto changer
controller . . . . . . . . . . . . . . . . . . . . . . . . . . 152
Compact disc player . . . . . . . . . . . . . . . . . . 152
Controls, Instrument panel . . . . . . . . . . . . 2, 6
Cooling system
Coolant level . . . . . . . . . . . . . . . . . . . . . . 298
Radiator and reservoir . . . . . . . . . . . . . . 298
Winter driving tips . . . . . . . . . . . . . . . . . . 240
Corrosion prevention . . . . . . . . . . . . . . . . . 276
Cruise control . . . . . . . . . . . . . . . . . . . . . . . 142
Cup holder . . . . . . . . . . . . . . . . . . . . . . . . . . 199

D
Defogger, Rear window . . . . . . . . . . . . . . . 115
Differential, Limited slip . . . . . . . . . . . . . . . 220
Dimmer switch, Headlight . . . . . . . . . . . . . 108
Directional signals . . . . . . . . . . . . . . . . . . . 108

## p.335 Do-it-yourself maintenance

Do-it-yourself maintenance
Parts and tools . . . . . . . . . . . . . . . . . . . . . 293
Service precautions . . . . . . . . . . . . . . . . 292
Does your vehicle need repairing? . . . . . 287
Driving
Automatic transmission . . . . . . . . . . . . . 135
Driving tips . . . . . . . . . . . . . . . . . . . . . . . . 236
Driving tips
Driving tips in various conditions . . . . . 237
Driving with an automatic
transmission . . . . . . . . . . . . . . . . . . . . . 135
Economical driving . . . . . . . . . . . . . . . . . 249
Good driving practice . . . . . . . . . . . . . . . 135
Winter driving tips . . . . . . . . . . . . . . . . . . 240
During
Break-in . . . . . . . . . . . . . . . . . . . . . . . . . . 209

E
Economical driving
Saving money on both fuel
and repairs . . . . . . . . . . . . . . . . . . . . . . 249
Electric moon roof . . . . . . . . . . . . . . . . . . . . . 31
Electrical system
Battery . . . . . . . . . . . . . . . . . . . . . . . 312, 313
Fuse locations . . . . . . . . . . . . . . . . . . . . . 291
Fuses . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 314
Emergency flasher switch . . . . . . . . . . . . . 110

Emergency, In case of
Blown fuse . . . . . . . . . . . . . . . . . . . . . . . . 314
Emergency flasher switch . . . . . . . . . . . 110
Flat tire . . . . . . . . . . . . . . . . . . . . . . . . . . . 257
If you cannot shift automatic
transmission selector lever . . . . . . . . 272
If you lose your keys . . . . . . . . . . . . . . . . 273
If your engine stalls while driving . . . . . 256
If your vehicle needs to be towed . . . . . 269
If your vehicle will not start . . . . . . . . . . 252
Jump starting . . . . . . . . . . . . . . . . . . . . . . 253
Towing . . . . . . . . . . . . . . . . . . . . . . . . . . . . 269
Engine
Before starting the engine . . . . . . . . . . . 236
Checking the coolant level . . . . . . . . . . 298
Emission control device . . . . . . . . . . . . . 212
Engine compartment . . . . . . . . . . . . . . . 290
Exhaust gas caution . . . . . . . . . . . . . . . . 213
Hood release . . . . . . . . . . . . . . . . . . . . . . . 27
Oil consumption . . . . . . . . . . . . . . . . . . . . 214
Oil level . . . . . . . . . . . . . . . . . . . . . . . . . . . 296
Oil pressure gauge . . . . . . . . . . . . . . . . . 119
Starting procedure . . . . . . . . . . . . . . . . . 236
Three-way catalytic converter . . . . . . . 212
Engine coolant
Temperature gauge . . . . . . . . . . . . . . . . . 118
Winter driving tips . . . . . . . . . . . . . . . . . . 240
Engine coolant temperature gauge . . . . . 118
Engine immobiliser system . . . . . . . . . . . . . 12
Engine oil
Winter driving tips . . . . . . . . . . . . . . . . . . 240
Engine oil pressure gauge . . . . . . . . . . . . . 119
Exhaust gas caution . . . . . . . . . . . . . . . . . . 213

F
Facts about engine oil consumption . . . . 214
First-aid kit holder . . . . . . . . . . . . . . . . . . . 199
Flasher, Headlight . . . . . . . . . . . . . . . . . . . . 108
Flat tire
After changing wheels . . . . . . . . . . . . . . 267
Changing tire . . . . . . . . . . . . . . . . . . . . . . 265
If you have a flat tire . . . . . . . . . . . . . . . . 257
Jack point . . . . . . . . . . . . . . . . . . . . . . . . . 263
Jacking precautions . . . . . . . . . . . . . . . . 257
Jacking up . . . . . . . . . . . . . . . . . . . . . . . . 264
Loosening wheel nuts . . . . . . . . . . . . . . . 262
Lowering vehicle . . . . . . . . . . . . . . . . . . . 266
Reinstalling wheel ornament . . . . . . . . . 267
Removing wheel ornament . . . . . . . . . . 262
Wheel block . . . . . . . . . . . . . . . . . . . . . . . 261
Wheel nuts . . . . . . . . . . . . . . . . . . . . . . . . 266
Floor mat . . . . . . . . . . . . . . . . . . . . . . . . . . . . 204
Fluid level
Brake . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 300
Power steering . . . . . . . . . . . . . . . . . . . . . 301
Washer fluid . . . . . . . . . . . . . . . . . . . . . . . 315
Fog light switch, Front . . . . . . . . . . . . . . . . 111
Foreign countries, Operation in . . . . . . . . 211
Four-wheel drive
Operating the four-wheel
drive system . . . . . . . . . . . . . . . . . . . . . 139
Front fog light switch . . . . . . . . . . . . . . . . . 111
Front seats . . . . . . . . . . . . . . . . . . . . . . . . 35, 36
Fuel
Filler door opener . . . . . . . . . . . . . . . . . . . 29
Fuel economy . . . . . . . . . . . . . . . . . . . . . 249
Gauge . . . . . . . . . . . . . . . . . . . . . . . . . . . . 118
Operation in foreign countries . . . . . . . 211

## p.336 Tank cap . . . . . . . . . . . . . . . . . . . . . . . . . . . 29

Tank cap . . . . . . . . . . . . . . . . . . . . . . . . . . . 29
Fuel information . . . . . . . . . . . . . . . . . . . . . 209
Fuel pump shut off system . . . . . . . . . . . . 211
Fuse
Fuse box . . . . . . . . . . . . . . . . . . . . . . . . . . 314
Fuse locations . . . . . . . . . . . . . . . . . . . . . . . 291

G
Gauge
Engine coolant temperature . . . . . . . . . 118
Engine oil pressure . . . . . . . . . . . . . . . . . 119
Fuel . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 118
Glove box . . . . . . . . . . . . . . . . . . . . . . . . . . . 195

Indicator symbols . . . . . . . . . . . . . . . . . . . . . . 7
Installation with child restraint
lower anchorages . . . . . . . . . . . . . . . . . . . 94
Instrument panel
Brightness control . . . . . . . . . . . . . . . . . . 110
Cigarette lighter and ashtray . . . . . . . . . 192
Clock . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 188
Engine oil pressure gauge . . . . . . . . . . . 119
Fuel gauge . . . . . . . . . . . . . . . . . . . . . . . . 118
Indicator symbols . . . . . . . . . . . . . . . . . . . . 7
Odometer . . . . . . . . . . . . . . . . . . . . . . . . . 121
Tachometer . . . . . . . . . . . . . . . . . . . . . . . . 120
Trip meter . . . . . . . . . . . . . . . . . . . . . . . . . 121
Instrument panel light control . . . . . . . . . . 110
Instrument panel overview . . . . . . . . . . . . 2, 6
Interior light . . . . . . . . . . . . . . . . . . . . . . . . . 111

H
Hazard switch . . . . . . . . . . . . . . . . . . . . . . . 110
Head restraints . . . . . . . . . . . . . . . . . . . . . . . 46
Headlight switch . . . . . . . . . . . . . . . . . . . . . 108
High speed operation
During break-in . . . . . . . . . . . . . . . . . . . . 209
Hood release, Engine . . . . . . . . . . . . . . . . . . 27
How to start the engine . . . . . . . . . . . . . . . 236

J
Jack
Location . . . . . . . . . . . . . . . . . . . . . . . . . . 259
Jump starting . . . . . . . . . . . . . . . . . . . . . . . . 253

K
Keys . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 10, 273

I
Identification
Engine . . . . . . . . . . . . . . . . . . . . . . . . . . . . 221
Vehicle . . . . . . . . . . . . . . . . . . . . . . . . . . . . 220
If your vehicle becomes stuck . . . . . . . . . 268
Ignition switch . . . . . . . . . . . . . . . . . . . . . . . 134
Ignition switch light . . . . . . . . . . . . . . . . . . . 113

L
Light bulbs
Back-up lights . . . . . . . . . . . . . . . . . . . . . 321
Front fog lights . . . . . . . . . . . . . . . . . . . . . 318
Front side marker lights . . . . . . . . . . . . . 319

Front turn signal lights . . . . . . . . . . . . . . 319
Headlights . . . . . . . . . . . . . . . . . . . . . . . . 316
License plate lights . . . . . . . . . . . . . . . . . 321
Parking lights . . . . . . . . . . . . . . . . . . . . . . 319
Rear turn signal lights . . . . . . . . . . . . . . 321
Stop and tail lights . . . . . . . . . . . . . 320, 321
Light bulbs, Replacing . . . . . . . . . . . . . . . . 315
Limited slip differential . . . . . . . . . . . . . . . . 220
Load limits . . . . . . . . . . . . . . . . . . . . . . . . . . 230
Lock
Back door . . . . . . . . . . . . . . . . . . . . . . . . . . 25
Side doors . . . . . . . . . . . . . . . . . . . . . . . . . 18
Steering column . . . . . . . . . . . . . . . . . . . 134

M
Maintenance
Do-it-yourself maintenance . . . . . . . . . 292
Does your vehicle need repairing? . . . 287
General maintenance . . . . . . . . . . . . . . . 285
Maintenance requirements . . . . . . . . . . 284
Parts and tools . . . . . . . . . . . . . . . . . . . . . 293
Where to go for service . . . . . . . . . . . . . 284
Maximum allowable speed
Automatic transmission . . . . . . . . . . . . . 135
Mirrors
Folding rear view . . . . . . . . . . . . . . . . . . . 100
Outside rear view . . . . . . . . . . . . . . . . . . . 99
Power rear view . . . . . . . . . . . . . . . . . . . . . 99
Vanity . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 105
Moon roof . . . . . . . . . . . . . . . . . . . . . . . . . . . . 31

## p.337 N

N
New vehicle break-in . . . . . . . . . . . . . . . . . 209

Pretensioners
(seat belt pretensioners) . . . . . . . . . . . . . 55
Protecting your Toyota
from corrosion . . . . . . . . . . . . . . . . . . . . . 276

O
Odometer . . . . . . . . . . . . . . . . . . . . . . . . . . . 121
Off road vehicle precautions . . . . . . . . . . . 208
Oil
Consumption . . . . . . . . . . . . . . . . . . . . . . 214
Power steering . . . . . . . . . . . . . . . . . . . . . 301
Pressure gauge . . . . . . . . . . . . . . . . . . . . 119
Viscosity and grade . . . . . . . . . . . . . . . . 296
Oil consumption . . . . . . . . . . . . . . . . . . . . . 214
Operation in foreign countries . . . . . . . . . 211
Outside rear view mirror heaters . . . . . . . 115
Outside temperature display . . . . . . . . . . . 188
Overheating, Engine coolant . . . . . . . . . . 118
Overview
Engine compartment . . . . . . . . . . . . . . . 290

P
Parking brake
Operation . . . . . . . . . . . . . . . . . . . . . . . . . 142
Reminder light . . . . . . . . . . . . . . . . . . . . . 142
Personal light . . . . . . . . . . . . . . . . . . . . . . . . 112
Polishing . . . . . . . . . . . . . . . . . . . . . . . . . . . . 277
Power outlet . . . . . . . . . . . . . . . . . . . . . . . . . 192
Power quarter windows . . . . . . . . . . . . . . . . 24
Power rear view mirror control . . . . . . . . . . 99
Power steering
Fluid level . . . . . . . . . . . . . . . . . . . . . . . . . 301
Power window switches . . . . . . . . . . . . . . . . 22
Preloaders (seat belt pretensioners) . . . . . 55

Q
Quarter windows . . . . . . . . . . . . . . . . . . . . . . 24

R
Radiator
Coolant, Engine . . . . . . . . . . . . . . . . . . . . 298
Radio . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 152
Rear air conditioning system . . . . . . . . . . 184
Rear seat
Third seat entry . . . . . . . . . . . . . . . . . . . . . 38
Rear seat audio system . . . . . . . . . . . . . . . 170
Rear step bumper . . . . . . . . . . . . . . . . . . . . 219
Rear view mirrors
Folding . . . . . . . . . . . . . . . . . . . . . . . . . . . 100
Outside . . . . . . . . . . . . . . . . . . . . . . . . . . . . 99
Power . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 99
Rear view monitor system . . . . . . . . . . . . . 189
Rear window defogger switch . . . . . . . . . . 115
Rear window wiper and washer switch . . 114
Reporting safety defects
for U.S. owners . . . . . . . . . . . . . . . . . . . . 332
Rollover sensing of curtain shield
airbag off switch . . . . . . . . . . . . . . . . . . . 193
Roof luggage carrier . . . . . . . . . . . . . . . . . . 202

S
Seat adjustment precautions
Front seats . . . . . . . . . . . . . . . . . . . . . . . . . 35
Seat belt extender . . . . . . . . . . . . . . . . . . . . . 53
Seat belts
Cleaning . . . . . . . . . . . . . . . . . . . . . . . . . . 279
Fastening . . . . . . . . . . . . . . . . . . . . . . . . . . 48
Seat belt precautions . . . . . . . . . . . . . . . . 48
Seat belt pretensioners . . . . . . . . . . . . . . 55
Seat heater switches . . . . . . . . . . . . . . . . . . 47
Seating capacity . . . . . . . . . . . . . . . . . . . . . 230
Seats . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 34
Second seat . . . . . . . . . . . . . . . . . . . . . . . 37, 38
Service and maintenance . . . . . . . . . . . . . 284
Side door locks . . . . . . . . . . . . . . . . . . . . . . . 18
Skyhook TEMS . . . . . . . . . . . . . . . . . 145, 147
Spare fuse . . . . . . . . . . . . . . . . . . . . . . . . . . 314
Spare tire . . . . . . . . . . . . . . . . . . . . . . . . . . . 259
Spark plugs
Iridium-tipped spark plugs . . . . . . . . . . 215
Specifications . . . . . . . . . . . . . . . . . . . . . . . 324
SRS driver and
front passenger airbags . . . . . . . . . . . . . . 58
SRS side and curtain shield airbags
with rollover sensing function . . . . . . . . . 65
Starting
Cold weather . . . . . . . . . . . . . . . . . . . . . . 236
Engine . . . . . . . . . . . . . . . . . . . . . . . . . . . . 236
Jump starting . . . . . . . . . . . . . . . . . . . . . . 253
Steering
Power tilt steering wheel . . . . . . . . . . . . . 98
Steering column
Column lock . . . . . . . . . . . . . . . . . . . . . . . 134
Steering pad switches . . . . . . . . . . . . . . . . 172
Sun visors . . . . . . . . . . . . . . . . . . . . . . . . . . . 105

## p.338 Suspension and chassis . . . . . . . . . . . . . . 221

Suspension and chassis . . . . . . . . . . . . . . 221
Switch
Emergency flasher . . . . . . . . . . . . . . . . . 110
Headlight, dimmer and turn signal . . . . 108
Ignition . . . . . . . . . . . . . . . . . . . . . . . . . . . 134
Outside rear view mirror heaters . . . . . 115
Overdrive . . . . . . . . . . . . . . . . . . . . . . . . . 135
Rear window defogger . . . . . . . . . . . . . . 115
Rear window wiper and washer . . . . . . 114
Windshield wiper and washer . . . . . . . . 113

T
Tachometer . . . . . . . . . . . . . . . . . . . . . . . . . 120
Telescopic steering column . . . . . . . . . . . . . 98
Theft deterrent system . . . . . . . . . . . . . . . . . 28
Theft prevention labels . . . . . . . . . . . . . . . 221
Third seat . . . . . . . . . . . . . . . . . . . . . . . . . . . . 42
Three-way catalytic converter . . . . . . . . . 212
Tie-down hooks . . . . . . . . . . . . . . . . . . . . . 201
Tilt steering wheel . . . . . . . . . . . . . . . . . . . . . 98
Tires
Changing . . . . . . . . . . . . . . . . . . . . . . . . . . 257
Flat tire . . . . . . . . . . . . . . . . . . . . . . . . . . . 257
Glossary . . . . . . . . . . . . . . . . . . . . . . . . . . 227
Inflation pressure . . . . . . . . . . . . . . . . . . 301
Replacing . . . . . . . . . . . . . . . . . . . . . . . . . 304
Rotation . . . . . . . . . . . . . . . . . . . . . . . . . . . 306
Size . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 224
Snow tires and chains . . . . . . . . . . . . . . 306
Spare . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 259
Symbols . . . . . . . . . . . . . . . . . . . . . . . . . . 222
Tire Identification Number (TIN) . . . . . . 223
Tools . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 259
Total load capacity . . . . . . . . . . . . . . . . . . . 230
Towing
Capacity . . . . . . . . . . . . . . . . . . . . . . . . . . 230
Emergency towing . . . . . . . . . . . . . . . . . 270
Emergency towing hook
precautions . . . . . . . . . . . . . . . . . . . . . . 271
If your vehicle needs to be towed . . . . . 269
Tips for towing a stuck vehicle . . . . . . . 272
Trailer . . . . . . . . . . . . . . . . . . . . . . . . . . . . 241
Trailer towing . . . . . . . . . . . . . . . . . . . . . . . . 241
Trip information display . . . . . . . . . . . . . . . 129
Trip meter . . . . . . . . . . . . . . . . . . . . . . . . . . . 121

Turn signals . . . . . . . . . . . . . . . . . . . . . . . . . 108

U
Uniform tire quality grading . . . . . . . . . . . . 225

V
Vanity mirrors . . . . . . . . . . . . . . . . . . . . . . . . 105
Voltmeter . . . . . . . . . . . . . . . . . . . . . . . . . . . 120

W
Warning reflector holder . . . . . . . . . . . . . . 199
Washer fluid
Adding washer fluid . . . . . . . . . . . . . . . . 315
Washing and waxing . . . . . . . . . . . . . . . . . . 277
Wheels
Aluminum wheel . . . . . . . . . . . . . . . . . . . 309
Replacing . . . . . . . . . . . . . . . . . . . . . . . . . 308
Windshield wiper and washer switch . . . . 113
Winter driving tips . . . . . . . . . . . . . . . . . . . . 240
Wireless remote control . . . . . . . . . . . . . . . . 13

## p.339 WE REALLY CARE ABOUT YOU  PLEASE BUCKLE UP

WE REALLY CARE ABOUT YOU  PLEASE BUCKLE UP
Toyota has made a special effort to encourage use of seat belts.
Toyota belts are:

 Comfortable
 Easy to use
 Convenient
We encourage you to use your belts every time you drive.

U

## p.340 You should know as much about the quality and

You should know as much about the quality and
importance of proper maintenance of your new
vehicle as the people who built it.
The Toyota authorized Repair Manual
tells you how to maintain your vehicle and
enables you to correctly perform your own
maintenance.
The best way to keep your new vehicle in top
running order is to maintain it properly from
the moment you drive it off the showroom
floor.
The Toyota authorized Repair Manual is
packed with literally everything you need to
know to perform your own maintenance in
virtually every area of your new vehicle.

## p.341 Maintenance procedures for the engine,

Maintenance procedures for the engine,
chassis, body, electrical system, and more,
are clearly explained and illustrated.
Periodic maintenance and tune-up
Periodic maintenance and tune-up helps to prevent small problems from growing into larger ones later on. The repair manual outlines exactly what maintenance is required and clearly explains how to do the
work yourself step-by-step.
Areas covered include such things as spark plug replacement, valve clearance adjustment and engine oil
and filter replacement.

Where to obtain the
Repair Manual
The repair manual for LAND CRUISER may be
purchased from any Toyota dealer or the Material Distribution Center. To purchase the repair
manual, please contact your Toyota dealer or
call the Material Distribution Center toll-free
at 1-800-622-2033.
