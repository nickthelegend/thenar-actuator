"""Original parametric 9:1 cycloidal bench demonstrator. Units mm.
Not a rated actuator or JX1 replacement. Geometry is generated here, then
imported and saved through the installed SolidWorks API by save_solidworks.py.
"""
from pathlib import Path
import math, json, itertools
import cadquery as cq
import numpy as np
import trimesh
from shapely.geometry import Polygon, Point
from shapely import affinity

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'cad'/'demo-r1'; OUT.mkdir(parents=True,exist_ok=True)
PRINT=OUT/'print'; PRINT.mkdir(exist_ok=True)
CHECK=ROOT/'verification'; CHECK.mkdir(exist_ok=True)
P=dict(ring_pins=10,ratio=9,pin_pitch_radius=43.,pin_radius=4.,eccentricity=2.,
       profile_clearance=.20,case_diameter=110.,output_pins=5,output_pin_radius=27.,
       output_pin_diameter=5.,output_hole_diameter=9.4,motor_shaft_bore=5.20,
       motor_mount_pitch=31.,motor_pilot_pocket=22.4,disc_bearing_bore=22.2,
       output_bearing_bore=47.2,input_journal=7.9,output_journal=24.9)
parts={}; records=[]; placed={}; asm=cq.Assembly(name='THENAR-C9-DEMO-R1')
COMP=OUT/'components'; COMP.mkdir(exist_ok=True); placements=[]
blue=cq.Color(.12,.42,.75); orange=cq.Color(.95,.52,.12); grey=cq.Color(.65,.68,.72)
def circlepts(r,n,offset=0):
    return [(r*math.cos(offset+i*2*math.pi/n),r*math.sin(offset+i*2*math.pi/n)) for i in range(n)]
def cylinder(r,h,z=0,xy=(0,0)):
    return cq.Workplane('XY').workplane(offset=z).center(*xy).circle(r).extrude(h)
def ann(ro,ri,h,z=0,xy=(0,0)):
    return cq.Workplane('XY').workplane(offset=z).center(*xy).circle(ro).circle(ri).extrude(h)
def holes(s,pts,d,z,h):
    return s.cut(cq.Workplane('XY').workplane(offset=z).pushPoints(pts).circle(d/2).extrude(h))
def add(name,s,translation=(0,0,0),printable=True,qty=1,note='',color=blue):
    s=s.val() if isinstance(s,cq.Workplane) else s
    assert s.isValid() and len(s.Solids())==1,(name,'invalid solid')
    parts[name]=s
    if printable:
        cq.exporters.export(s,str(PRINT/(name+'.step')))
        cq.exporters.export(s,str(PRINT/(name+'.stl')),tolerance=.025,angularTolerance=.10)
        mesh=trimesh.load_mesh(PRINT/(name+'.stl'))
        assert mesh.is_watertight and mesh.is_volume,name
        b=s.BoundingBox()
        records.append(dict(part=name,quantity_per_set=qty,bbox_mm=[round(b.xlen,3),round(b.ylen,3),round(b.zlen,3)],
                            solid_volume_cm3=round(s.Volume()/1000,3),note=note))
    asm.add(s,name=name,loc=cq.Location(cq.Vector(*translation)),color=color)
    placed[name]=s.translate(translation)
    cq.exporters.export(s,str(COMP/(name+'.step')))
    placements.append(dict(name=name,translation_mm=translation,printable=printable))

# Fixed case: back plate, spacer ring, front bearing housing, bearing retainer.
bolts=circlepts(50,6,math.pi/6)
pins=circlepts(P['pin_pitch_radius'],10)
back=cylinder(55,8)
back=holes(back,[(x,y) for x in (-15.5,15.5) for y in (-15.5,15.5)],3.4,0,8)
back=holes(back,[(0,0)],22.4,0,2.5)
back=holes(back,[(0,0)],17,0,8)
back=holes(back,bolts,4.5,0,8)
back=holes(back,pins,8.2,6,2)
add('01-back-plate',back,note='Motor face at Z0. Four M3 motor screws. Pin pockets face up.')
ring=ann(55,48,38)
ring=holes(ring,bolts,4.5,0,38)
add('02-case-ring',ring,(0,0,8),note='Print flat; 38 mm high. No integrated rollers.')
front=cylinder(55,15)
front=holes(front,[(0,0)],30.4,0,15)
front=holes(front,[(0,0)],47.2,3,12)
front=holes(front,pins,8.2,0,2)
front=holes(front,bolts,4.5,0,15)
front=holes(front,circlepts(29,3),2.7,6,9)
add('03-front-bearing-cover',front,(0,0,46),note='6005 bearing seat starts 3 mm from underside; retainer screws form threads in pilot holes.')
ret=ann(34,15.2,3)
ret=holes(ret,circlepts(29,3),3.4,0,3)
add('04-bearing-retainer',ret,(0,0,61),note='Three M3x12 screws, bearing retention only. Bottom face retains outer bearing ring at Z61.')

# Single-disc cycloidal profile, generated from the roller-envelope equations.
t=np.linspace(0,2*np.pi,1440,endpoint=False); N=P['ring_pins']; R=P['pin_pitch_radius']; e=P['eccentricity']; r=P['pin_radius']
psi=np.arctan2(np.sin((1-N)*t),R/(e*N)-np.cos((1-N)*t))
xy=np.column_stack((R*np.cos(t)-r*np.cos(t+psi)-e*np.cos(N*t),R*np.sin(t)-r*np.sin(t+psi)-e*np.sin(N*t)))
profile=Polygon(xy).buffer(-P['profile_clearance'],quad_segs=8)
assert profile.is_valid and profile.geom_type=='Polygon'
profile_pts=list(profile.exterior.coords)[:-1]
disc=cq.Workplane('XY').polyline(profile_pts).close().extrude(6)
disc=holes(disc,[(0,0)],22.2,0,6)
outpins=circlepts(27,5)
disc=holes(disc,outpins,9.4,0,6)
add('05-cycloidal-disc',disc,(2,0,28.5),note='9 lobes; print broad face down; retain profile exactly.',color=orange)

# Motor shaft reaches 24 mm beyond its mounting face. Blind 25 mm bore leaves
# solid material before the eccentric journal, avoiding a shaft/bearing clash.
coupler=cylinder(8,20)
coupler=coupler.union(cylinder(3.95,7,20,(2,0)))
coupler=holes(coupler,[(0,0)],5.20,0,17)
coupler=holes(coupler,[(2,0)],2.7,21,6)
coupler=coupler.cut(cq.Workplane('YZ').workplane(offset=2).center(0,10).circle(1.65).extrude(8))
coupler=coupler.cut(cq.Workplane('YZ').workplane(offset=4.5).center(0,10).polygon(6,5.7/math.cos(math.pi/6)).extrude(4))
add('06-input-eccentric',coupler,(0,0,8),note='Blind shaft bore; one M3 nut and M3x8 clamp screw. Shaft flat and length must be measured.',color=orange)

# Output carrier with five retained steel extraction pins and journal on 6005.
output=cylinder(35,6).union(cylinder(12.45,25,6))
output=holes(output,outpins,5.15,0,5)
output=holes(output,circlepts(8,3),2.7,23,8)
add('07-output-carrier',output,(0,0,37),note='Separate flange allows bearing installation over journal. Pins need retaining compound suitable for PLA.',color=orange)
flange=cylinder(28,6).union(cylinder(17,2,6))
flange=holes(flange,circlepts(23,6),3.4,0,6)
flange=holes(flange,circlepts(8,3),3.4,0,8)
add('11-output-flange',flange,(0,0,68),note='Three M3x14 screws attach to carrier. 46 PCD and 34x2 pilot reference unverified JX1 M assumptions. Not a robot-ready interface.',color=orange)

# Split inner-race spacers can be assembled around the integral output journal.
# They limit axial float. Two halves per spacer, retained by the surrounding
# bore; final end float must be checked, not removed by crushing printed parts.
for num,height,z in [('09',6,43),('10',7,61)]:
    half=ann(14.8,12.55,height).intersect(cq.Workplane('XY').box(40,20,height,centered=(True,False,False)))
    add(num+'-split-inner-spacer-A',half,(0,0,z),note='Print two complementary halves as supplied. Contacts inner race only.')
    add(num+'-split-inner-spacer-B',half.rotate((0,0,0),(0,0,1),180),(0,0,z),note='Mate to matching A half; check axial end float after assembly.')

# Printable bore coupon, kept out of assembly.
coupon=cq.Workplane('XY').box(96,32,5,centered=(True,True,False))
coupon=holes(coupon,[(-33,0),(-10,0),(15,0)],22.0,0,5)
coupon=holes(coupon,[(-10,0)],22.2,0,5); coupon=holes(coupon,[(15,0)],22.4,0,5)
coupon=holes(coupon,[(37,0)],5.2,0,5)
add('08-fit-coupon',coupon,(150,0,0),note='Coupon is not an actuator part. Left-to-right bores 22.0,22.2,22.4,5.2 mm.')

# Purchased parts are simplified envelopes, not bearing internals.
add('REF-608-bearing',ann(11,4,7), (2,0,28),False,color=grey)
add('REF-input-retaining-washer',ann(5,1.65,1), (2,0,35),False,color=grey)
add('REF-6005-bearing',ann(23.5,12.5,12),(0,0,49),False,color=grey)
motor=cq.Workplane('XY').box(42,42,48,centered=(True,True,False))
add('REF-JK42HS48-body',motor,(0,0,-48),False,color=grey)
add('REF-motor-shaft',cylinder(2.5,24),(0,0,0),False,color=grey)
for i,(x,y) in enumerate(pins): add(f'REF-ring-pin-{i+1:02}',cylinder(4,42),(x,y,6),False,color=grey)
for i,(x,y) in enumerate(outpins): add(f'REF-output-pin-{i+1:02}',cylinder(2.5,15),(x,y,27),False,color=grey)

asm.save(str(OUT/'THENAR-C9-DEMO-R1.step'))
(OUT/'parameters.json').write_text(json.dumps(P,indent=2))
(OUT/'print-manifest.json').write_text(json.dumps(records,indent=2))
(OUT/'placements.json').write_text(json.dumps(placements,indent=2))

# Numerical planar envelope check over one complete output revolution.
# 9 input turns, 721 samples; prescribed kinematics, not dynamic/contact solver.
min_pin_gap=1e9; min_output_gap=1e9; min_case_gap=1e9
for a in np.linspace(0,18*math.pi,721):
    b=-a/9
    poly=affinity.translate(affinity.rotate(profile,b,origin=(0,0),use_radians=True),e*math.cos(a),e*math.sin(a))
    for x,y in pins:
        q=Point(x,y)
        d=poly.exterior.distance(q)-4
        if poly.contains(q): d=-poly.exterior.distance(q)-4
        min_pin_gap=min(min_pin_gap,d)
    bounds=np.asarray(poly.exterior.coords)
    min_case_gap=min(min_case_gap,48-np.sqrt((bounds**2).sum(axis=1)).max())
    # hole centres follow disc; pin centres follow carrier at b.
    for x,y in outpins:
        hx=x*math.cos(b)-y*math.sin(b)+e*math.cos(a)
        hy=x*math.sin(b)+y*math.cos(b)+e*math.sin(a)
        px=x*math.cos(b)-y*math.sin(b); py=x*math.sin(b)+y*math.cos(b)
        min_output_gap=min(min_output_gap,4.7-2.5-math.hypot(hx-px,hy-py))
report=dict(status='CAD_ONLY_NOT_PHYSICALLY_TESTED',samples=721,input_turns=9,output_turns=-1,
    min_ring_pin_clearance_mm=min_pin_gap,min_output_pin_clearance_mm=min_output_gap,min_case_clearance_mm=min_case_gap,
    printed_parts=len(records),all_solids_valid=True,all_stls_watertight=True,
    limitations=['Prescribed kinematics; no dynamic simulation, strength, wear, thermal or torque validation.',
                 'Single disc is unbalanced. Low-speed bench use only. Not robot hardware.',
                 'Fits need coupon measurement. Steel pins need positive retention or validated retaining method.',
                 'No motor torque-speed curve or measured shaft flat available.'])
overlaps=[]; tested=0
for (na,sa),(nb,sb) in itertools.combinations(placed.items(),2):
    ba,bb=sa.BoundingBox(),sb.BoundingBox()
    if any(min(getattr(ba,k+'max'),getattr(bb,k+'max'))-max(getattr(ba,k+'min'),getattr(bb,k+'min'))<1e-6 for k in 'xyz'): continue
    tested+=1
    vol=sa.intersect(sb).Volume()
    if vol>1e-4: overlaps.append(dict(a=na,b=nb,volume_mm3=vol))
report['zero_pose_3d_intersection_candidates']=tested
report['zero_pose_3d_interferences']=overlaps
(CHECK/'geometry.json').write_text(json.dumps(report,indent=2))
assert min_pin_gap>0 and min_output_gap>0 and min_case_gap>0,report
assert not overlaps,overlaps
print(json.dumps(report,indent=2),flush=True)
