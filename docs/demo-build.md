# C9 demo assembly

Purpose: fit, motion and low-load bench experiments. No assigned output torque rating. Do not fit to a load-bearing robot joint.

## Printed parts

Print one of each file in `cad/demo-r1/print/`: back plate, case ring, front bearing cover, bearing retainer, cycloidal disc, input eccentric, output carrier, output flange, four split-spacer halves and one fit coupon. The coupon is not installed. The manifest is the authoritative quantity list.

Suggested quotation basis, not a strength qualification: PLA or PLA+, 0.2 mm layers, 0.4 mm nozzle, six perimeters and six top/bottom layers. Quote 60% infill for housings and 100% for disc, eccentric, carrier, flange and spacers. Supplier should identify support requirements and orientation, particularly the output carrier. Do not scale the models or sand the cycloidal working profile to force a fit. Print the fit coupon first. All STL coordinates are millimetres.

## Bought hardware per demonstrator

| Item | Qty | Purpose |
|---|---:|---|
| JK42HS48-1684 motor, lab stock | 1 | Motor; verify shaft and face dimensions |
| 608 bearing, 8 × 22 × 7 mm | 1 | Eccentric bearing |
| 6005 bearing, 25 × 47 × 12 mm | 1 | Output support; single bearing is not a rated moment-bearing arrangement |
| Smooth steel pins, Ø8 × 42 mm | 10 | Fixed ring; lengths include 2 mm end pockets |
| Smooth steel pins, Ø5 × 15 mm | 5 | Output extraction pins, 5 mm insertion into carrier |
| M4 × 70 through bolts, M4 nuts, two washers each | 6 sets | Clamp 61 mm case stack; verify thread protrusion |
| M3 × 12 motor screws with washers | 4 | 8 mm back plate leaves nominal 3–4 mm motor engagement; check motor drawing |
| M3 × 12 screws | 3 | Front bearing retainer; 2.7 mm printed pilot holes |
| M3 × 14 screws | 3 | Separate output flange; 8 mm flange/pilot stack, nominal 6 mm engagement |
| M3 × 8 screw and M3 nut | 1 set | Input shaft clamp; align to actual shaft flat |
| M3 × 6 screw with Ø10 × 1 washer, 3.3 mm hole | 1 set | Eccentric bearing inner-race retention |
| Polymer-compatible retaining compound | as needed | Secure output pins and disc bearing outer race after fit trials; supplier compatibility required |
| Adjustable bipolar driver, controller, regulated supply | 1 each | Reduced-current motor test; reuse lab equipment |
| Rated wiring, terminals, fuse, DC disconnect and USB cable | 1 set | Bench wiring |
| Rigid mount, guard, caliper, multimeter and temperature sensor | reuse | Test fixture and inspection |

This is an original design with **608 and 6005 bearings**. The earlier 6704 shopping list belonged to a different reference gearbox and is not the BOM for these files.

## Assembly order and access

1. Inspect printed coupon and measure bearings, pins and shaft. Nominal model clearances are trial values. Rebuild with measured fit compensation where needed; this is not a tolerance-certified print.
2. Mount motor to back plate. Measure bolt engagement and ensure screws do not bottom. Motor face is assembly Z0; body occupies Z−48 to 0.
3. Install M3 nut and radial clamp screw in the eccentric hub, then slide over the motor shaft. Its bottom is Z8. The shaft bore is blind, ending at Z25; the journal is solid above it. Tighten gently onto the measured flat.
4. Fit 608 into the disc and secure its outer race with a compatible retention method. Assemble over the eccentric journal, with bearing at Z28–35 and disc Z28.5–34.5. Install washer and M3×6 axial screw; it must retain only the inner race. Confirm free bearing rotation.
5. Place ten steel ring pins in the back-plate pockets. Install case ring. Pin top ends locate in the front cover during step 8.
6. Secure the five output pins into the blind carrier holes. Feed those pins through the disc holes; carrier plate occupies Z37–43. Check every pin clears the disc throughout manual input rotation.
7. Fit both halves of the lower inner-race spacer around the output journal (Z43–49). Slide the 6005 over the still-unflanged journal to Z49–61. Do not install the output flange yet.
8. Fit front cover over the bearing and ring-pin ends. Install case through-bolts evenly. Fit upper split spacer halves at Z61–68, then the front retainer at Z61–64. It contacts the outer race; the upper spacer contacts the inner race. Check neither spacer rubs the housing.
9. Install output flange at Z68 with three M3×14 screws. This separate flange permits bearing installation. Measure axial end float and bearing drag; adjust spacers after measurement. Do not eliminate drag by overtightening or crushing plastic.
10. Clamp assembly to a rigid test fixture, add guard and manually rotate before applying power. Begin with reduced driver current and slow acceleration. Stop for binding, pin movement, cracking, rising drag or heating.

## Open engineering items

The single cycloidal disc is unbalanced; this version is deliberately low speed. A JX1 version needs a balanced load path, bearing life and moment-load calculations, metal pin retention, validated shaft fits, thermal design and closed-loop control. Polymer retaining compound, screw pullout and journal wear have not been qualified. PLA and PLA+ material data depend on brand and print process; they are not interchangeable structural allowables.
