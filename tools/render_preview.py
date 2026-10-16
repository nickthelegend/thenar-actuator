"""Render actual CAD mesh geometry, not an AI generated illustration."""
from pathlib import Path
import json, numpy as np, cadquery as cq
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
ROOT=Path(__file__).resolve().parents[1]
placements=json.loads((ROOT/'cad/demo-r1/placements.json').read_text())
fig=plt.figure(figsize=(15,8),facecolor='#f4f6fa')
for panel,exploded in enumerate([False,True]):
    ax=fig.add_subplot(1,2,panel+1,projection='3d'); ax.set_facecolor('#f4f6fa')
    for p in placements:
        if p['name']=='08-fit-coupon': continue
        s=cq.importers.importStep(str(ROOT/'cad/demo-r1/components'/(p['name']+'.step'))).val()
        verts,faces=s.tessellate(.25,.2)
        v=np.array([x.toTuple() for x in verts]); t=np.array(p['translation_mm'],float)
        if exploded:
            # Presentation offsets only; assembly positions are in placements.json.
            z=t[2]; t[2]+=0 if z<0 else (15 if z==0 else 25+1.8*z)
        v+=t
        color='#a9b3bf' if p['name'].startswith('REF') else ('#ec9b3b' if p['name'].startswith(('05','06','07','11')) else '#3f83bb')
        mesh=Poly3DCollection(v[np.array(faces)],facecolor=color,edgecolor='none',alpha=1)
        ax.add_collection3d(mesh)
    ax.set_xlim(-60,60); ax.set_ylim(-60,60); ax.set_zlim(-50,250 if exploded else 85)
    ax.set_box_aspect((120,120,300 if exploded else 135)); ax.view_init(elev=24,azim=-62)
    ax.set_axis_off(); ax.set_title('exploded assembly' if exploded else 'assembled demo',fontsize=16,pad=8)
fig.suptitle('thenar c9 | 9:1 stepper gearbox demo',fontsize=22,fontweight='bold',y=.98)
fig.text(.5,.035,'actual CAD geometry · PLA fit/motion prototype · no torque rating · not JX1-ready',ha='center',fontsize=12,color='#425067')
plt.subplots_adjust(top=.91,bottom=.08,wspace=.02)
fig.savefig(ROOT/'verification/cad-preview.png',dpi=140)
print('Rendered CAD preview')
