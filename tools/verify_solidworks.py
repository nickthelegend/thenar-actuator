from pathlib import Path
import json, pythoncom, win32com.client as com
ROOT=Path(__file__).resolve().parents[1]
a=pythoncom.LoadTypeLib(r'C:\Program Files\SOLIDWORKS Corp\SOLIDWORKS\sldworks.tlb').GetLibAttr()
SW=com.gencache.EnsureModule(a[0],a[1],a[3],a[4])
s=SW.ISldWorks(com.GetActiveObject('SldWorks.Application')._oleobj_)
d=SW.IModelDoc2(s.ActiveDoc._oleobj_)
assert Path(d.GetPathName()).name=='THENAR-C9-DEMO-R1-NATIVE.SLDASM'
expected={p['name']:p for p in json.loads((ROOT/'cad/demo-r1/placements.json').read_text())}
rows=[]
for raw in SW.IAssemblyDoc(d._oleobj_).GetComponents(False):
    c=SW.IComponent2(raw._oleobj_); p=Path(c.GetPathName()); name=p.stem
    vals=list(SW.IMathTransform(c.Transform2._oleobj_).ArrayData)
    target=[v/1000 for v in expected[name]['translation_mm']]
    error=max(abs(x-y) for x,y in zip(vals[9:12],target))
    assert error<1e-8,(name,error)
    cd=SW.IModelDoc2(c.GetModelDoc2()._oleobj_)
    count=len(SW.IPartDoc(cd._oleobj_).GetBodies2(0,False) or [])
    assert count==1,(name,count)
    rows.append(dict(part=name,translation_error_m=error,solid_count=count))
assert len(rows)==len(expected)
(ROOT/'verification/solidworks-placement.json').write_text(json.dumps(dict(status='PASS',components=rows),indent=2))
print('PASS:',len(rows),'native solid parts; all assembly translations match CAD data')
