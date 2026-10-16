# JX1 actuator requirements audit

Audit date: 16 October 2026. Source revision: [384de0f801f8a03af6b32420fd2efed343133eb0](https://github.com/nickthelegend/thenar-jx1/tree/384de0f801f8a03af6b32420fd2efed343133eb0).

The repository describes a 1.23 m robot with a CAD-estimated mass of 33.61 kg. Its final specification explicitly says nothing has been built or physically tested. Existing simulation and emulated-hub results must not be described as physical robot verification.

## Selected actuator classes

These are the upstream project's selected catalogue capabilities, not newly measured requirements or guaranteed simultaneous torque-speed operating points.

| Class | Locations | Quantity | Selected peak / rated N·m |
|---|---|---:|---:|
| XL | hip pitch and knee | 4 | 120 / 40 |
| L | hip roll | 2 | 60 / 20 |
| M | hip yaw, four ankle motors, waist yaw | 7 | 36 / 11 |
| S | shoulder pitch and roll | 4 | 17 / 6 |
| XS | shoulder yaw and elbow | 4 | 14 / 5 |
| neck servo | neck yaw and pitch | 2 | 1.9 stall; continuous unspecified |

Source: [actuator catalogue](https://github.com/nickthelegend/thenar-jx1/blob/384de0f801f8a03af6b32420fd2efed343133eb0/actuators/actuator_catalog.yaml).

## Conflicting load evidence must be reconciled

The old requirement file assumes 27.5 kg. The later final specification uses 33.61 kg and reports a conservative fast-walk demand of 55.5 N·m hip yaw, 64.6 hip roll, 119.9 hip pitch, 91.3 knee and 39.1 per ankle motor. Some exceed the selected actuators. The same document reports lower loads for a particular learned gait. A successful gait scenario is not evidence that the conservative load envelope can be discarded.

Use the current CAD masses and a frozen scenario set to regenerate requirements: supported stand, single-leg support, slow/nominal/fast walk, turning, squat, stopping and a specified disturbance. Retain pose-specific torque and speed pairs and RMS duty-cycle values; do not multiply independent maxima into a fictitious motor operating point.

Source: [final specification](https://github.com/nickthelegend/thenar-jx1/blob/384de0f801f8a03af6b32420fd2efed343133eb0/docs/final_robot_specification.md).

## Why the lab stepper is a demo motor

The manufacturer currently lists JK42HS48-1684 at 0.55 N·m holding torque, 1.68 A, 5 mm shaft, 24 mm shaft length. Variants differ; verify the actual label, shaft and driver current convention. A running torque-speed curve is still needed.

At 9:1 and an assumed 80% forward efficiency, 36 N·m would require 5 N·m motor torque at that operating speed. Using 0.55 N·m holding torque in the same arithmetic gives 3.96 N·m, but this is neither a measured output torque nor a plastic gearbox rating. For 36 N·m the holding-based ratio would be 81.8:1; running operation would require its own curve. At a hypothetical 6 rad/s output, that ratio requires about 4,688 motor rpm. No evidence establishes that this motor supplies the necessary torque there.

More reduction also increases reflected motor inertia approximately with the square of ratio. A large ratio is therefore not a free route to a compliant humanoid joint. Measure backdrive force in both powered and unpowered states.

Motor source: https://www.jkongmotor.com/nema-17-jk42hs48-1684-hybrid-stepper-motor.html

## Interface mismatch

The upstream M-class interface is an assumed 46 mm output PCD with six M3 positions and a 34 × 2 mm pilot, inside an 88 × 49 mm envelope. This demo borrows the output pattern for discussion only, uses clearance holes, and is substantially larger. Upstream bolt patterns are themselves marked assumed. It is not a drop-in module.

JX1 also expects 48 V CAN actuator feedback and control. A 24 V STEP/DIR driver does not implement that interface or torque control. A real replacement requires current sensing, calibrated encoders, an appropriate torque-capable motor drive, fault handling and a tested protocol adapter. The existing JX1 hardware torque limits must not be applied to this prototype.
