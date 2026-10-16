# From printed demonstrator to JX1 actuator

## Stage 1: one demo

Obtain quotes for one complete C9 print set and one fit coupon. Request the price for 20 sets separately as a scale comparison. No batch order before the first assembly is measured. Collect exact motor label, shaft geometry, available driver and printer/material details. Assemble using `demo-build.md`.

Record fit dimensions, free rotation, input/output direction and ratio. Nine input turns should produce one opposite output turn, allowing for backlash. Compare measured result with the model's prescribed kinematics.

## Stage 2: physical bench characterisation

Physical testing is pending; no robot or motor has been driven by this release. A lab operator must perform these tests with a guarded, clamped rig and a reachable power disconnect. Keep persons and robot loads out of the load path.

1. Measure the bare motor torque-speed curve at the actual driver current and supply voltage; record winding/case temperature and driver current convention. Separate stall/holding tests from rotating operation.
2. Measure gearbox output torque and speed simultaneously. Use a calibrated torque transducer or a scale acting perpendicular to a measured lever, `T = force_N × lever_m`. If the scale reports kg, convert with 9.80665 N/kg. Tare friction and fixture weight. A static lever test alone does not establish running capability.
3. Start unloaded and increase load in small steps within a separately reviewed fixture limit. Proposed initial learning objective is 1 N·m, not a certified safe limit. Stop on damage, pin migration, lost steps, abnormal temperature or drag. Do not attempt a 36 N·m load on this PLA demo.
4. Log backlash under reversing torque; output-angle error and missed steps; unpowered and powered backdrive torque in both directions; axial/radial play; noise; input power and output power; temperature versus time. Efficiency is output mechanical power / input mechanical power for gearbox-only measurements, not simply electrical efficiency.
5. Define the peak duration and repetition interval before claiming any peak rating. Define a thermal steady-state criterion, ambient temperature and cooling setup before claiming a continuous rating.

Store raw timestamped observations, sensor calibration, video, CAD revision, filament lot, print settings and failure photographs in a test record. Leave unmeasured fields empty. `verification/physical-tests.json` is explicitly pending.

## Stage 3: JX1 sizing and simulated integration

Freeze JX1 source revision and mass model. Reconcile its old 27.5 kg assumptions with the later 33.61 kg model and the differing gait results. Select the required joint class, not a uniform 36 N·m target for every joint.

For each candidate ratio, evaluate measured motor torque-speed, gearbox efficiency map, RMS duty, peak duration, regenerative power, backlash, reflected inertia, mass and envelope. Use `motor torque = joint torque / (ratio × efficiency)` only at paired operating points. Do not substitute holding torque for a running curve.

Update JX1's simulation with measured actuator saturation, velocity limits, rotor/gear inertia, friction, backlash, latency, current/thermal limits and realistic control mode. Re-run the frozen standing, walking, turn, squat and disturbance suite. A STEP/DIR stepper must not be represented as an ideal RobStride torque source. The passive planar C9 clearance check in this repo is not a JX1 dynamics simulation.

## Stage 4: engineering actuator

Develop a balanced reducer and motor/drive combination for one selected class. Prefer moderate reduction compatible with torque-speed and backdrivability; derive the ratio from measured motor data. Design metal shafts, bearing seats, pin retention and high-stress members as required by load and life calculations. Specify gearbox lubrication and sealing, output moment capacity, fastener preload, fatigue and housing heat removal. Do not send the PLA geometry unchanged as a production metal drawing.

Validate on a dynamometer and on an unloaded or counterbalanced single-joint fixture before a tethered robot test. Use encoder plausibility checks, current/temperature limits, bus and host watchdogs, hard travel stops and a power disconnect. Match JX1's CAN protocol, signs, zeros, units and command semantics. Review its existing torque caps before enabling any custom drive.

## Stage 5: pilot batch

Only after first-article acceptance, freeze drawings, BOM, inspection plan and firmware. Choose the actual allocation among XL/L/M/S/XS classes; JX1 requires 21 main units plus two neck servos, while the proposed 20 units are a development batch. Define acceptance limits for each class from robot requirements and test evidence. Inspect every unit for torque calibration, backlash, runout, thermal behaviour, electrical isolation, communication fault handling and serialised traceability.

## Release gates

| Gate | Current status | Evidence required |
|---|---|---|
| CAD geometry | sampled clearance and solid/mesh checks | `geometry.json`, SolidWorks export/reopen report |
| First printed assembly | pending | dimensions, photographs, fit and hand-turn record |
| Physical torque and durability | pending | measured curves and duty-cycle/temperature evidence |
| JX1 simulation with custom actuator | pending | measured model, scenario logs and comparison |
| Tethered real JX1 drive | pending | bench-qualified hardware, integration review and supervised test |
| Twenty-unit production release | not authorised | first article approval and frozen class-specific drawings |
