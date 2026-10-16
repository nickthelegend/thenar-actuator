"""Import solids and build a fixed native SolidWorks assembly.
Imported-body parts, no reconstructed sketch history or motion mates.
Temporarily disable 3D Interconnect for standalone import, then restore it.
"""
from pathlib import Path
import json, pythoncom, win32com.client as com, sys
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'cad/demo-r1/solidworks'; OUT.mkdir(exist_ok=True)
def library(name):
    a=pythoncom.LoadTypeLib(str(Path(r'C:\Program Files\SOLIDWORKS Corp\SOLIDWORKS')/(name+'.tlb'))).GetLibAttr()
    return com.gencache.EnsureModule(a[0],a[1],a[3],a[4])
SW=library('sldworks'); C=library('swconst').constants
try: rawapp=com.GetActiveObject('SldWorks.Application')
except Exception: rawapp=com.Dispatch('SldWorks.Application')
s=SW.ISldWorks(rawapp._oleobj_); s.Visible=True
placements=json.loads((ROOT/'cad/demo-r1/placements.json').read_text())
previous=s.GetUserPreferenceToggle(C.swMultiCAD_Enable3DInterconnect)
log=[]
def save(d,p):
    r=d.Extension.SaveAs3(str(p),0,1,None,None,0,0)
    assert r[0] and r[1]==0,(p,r)
    return dict(file=p.name,errors=r[1],warnings=r[2])
try:
    s.SetUserPreferenceToggle(C.swMultiCAD_Enable3DInterconnect,False)
    for p in placements:
        native=OUT/(p['name']+'.SLDPRT')
        if '--resume' in sys.argv and native.exists():
            raw,err,warn=s.OpenDoc6(str(native),1,1,'',0,0)
            assert raw is not None and err==0,(p['name'],err)
            log.append(dict(file=native.name,errors=err,warnings=warn))
            continue
        src=str(ROOT/'cad/demo-r1/components'/(p['name']+'.step'))
        raw,err=s.LoadFile4(src,'r',s.GetImportFileData(src),0)
        assert raw is not None and err==0,(src,err)
        d=SW.IModelDoc2(raw._oleobj_)
        assert d.GetType()==1,(p['name'],d.GetType())
        assert len(SW.IPartDoc(d._oleobj_).GetBodies2(0,False))==1
        log.append(save(d,OUT/(p['name']+'.SLDPRT')))
        print('saved',p['name'],flush=True)
    s.CloseDoc(str(OUT/'THENAR-C9-DEMO-R1-NATIVE.SLDASM'))
    template=s.GetUserPreferenceStringValue(C.swDefaultTemplateAssembly)
    raw=s.NewDocument(template,0,0.,0.); assert raw is not None,template
    doc=SW.IModelDoc2(raw._oleobj_); a=SW.IAssemblyDoc(raw._oleobj_)
    mu=SW.IMathUtility(s.GetMathUtility()._oleobj_)
    rows=[]
    for p in placements:
        path=OUT/(p['name']+'.SLDPRT')
        rawc=a.AddComponent5(str(path),0,'',False,'',0.,0.,0.)
        assert rawc is not None,p['name']
        c=SW.IComponent2(rawc._oleobj_)
        x,y,z=[v/1000 for v in p['translation_mm']]
        values=[1.,0.,0.,0.,1.,0.,0.,0.,1.,x,y,z,1.,0.,0.,0.]
        transform=mu.CreateTransform(com.VARIANT(pythoncom.VT_ARRAY|pythoncom.VT_R8,values))
        c.Transform2=transform
        c.Name2=p['name']
        doc.ClearSelection2(True); c.Select4(False,None,False); a.FixComponent()
        rows.append(dict(name=p['name'],file=path.name,translation_mm=p['translation_mm'],solid_count=1))
    doc.ClearSelection2(True); doc.ForceRebuild3(False)
    doc.ShowNamedView2('*Isometric',7); doc.ViewZoomtofit2(); doc.GraphicsRedraw2()
    dest=OUT/'THENAR-C9-DEMO-R1-NATIVE.SLDASM'; log.append(save(doc,dest))
    s.CloseDoc(str(dest))
    raw,err,warn=s.OpenDoc6(str(dest),2,1,'',0,0)
    assert raw is not None and err==0,(err,warn)
    doc=SW.IModelDoc2(raw._oleobj_); a=SW.IAssemblyDoc(raw._oleobj_)
    actual=list(a.GetComponents(False) or [])
    assert len(actual)==len(placements),(len(actual),len(placements))
    for rawc in actual:
        c=SW.IComponent2(rawc._oleobj_); path=Path(c.GetPathName())
        assert path.exists() and path.is_relative_to(OUT),path
        assert c.GetModelDoc2() is not None,c.Name2
    doc.ShowNamedView2('*Isometric',7); doc.ViewZoomtofit2(); doc.GraphicsRedraw2()
    preview=doc.SaveAs3(str(ROOT/'verification/solidworks-preview.png'),0,2)
    report=dict(version=s.RevisionNumber(),saved=log,components=rows,reopen_errors=err,reopen_warnings=warn,
       native_components=len(actual),preview_save_result=preview,
       notes=['Imported solid-body parts; fixed placement assembly; no dynamic mates, FEA or physical validation.'])
    (ROOT/'verification/solidworks.json').write_text(json.dumps(report,indent=2))
    print('DONE',dest,flush=True)
finally:
    s.SetUserPreferenceToggle(C.swMultiCAD_Enable3DInterconnect,previous)
