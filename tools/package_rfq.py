from pathlib import Path
import zipfile,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
dest=ROOT/'releases'; dest.mkdir(exist_ok=True)
files=list((ROOT/'cad/demo-r1/print').glob('*'))
files += [ROOT/p for p in ['cad/demo-r1/print-manifest.json','cad/demo-r1/parameters.json','cad/demo-r1/THENAR-C9-DEMO-R1.step','rfq/PRINT-REQUEST.txt','docs/demo-build.md','verification/geometry.json']]
assert len(list((ROOT/'cad/demo-r1/print').glob('*.stl')))==13
with zipfile.ZipFile(dest/'THENAR-C9-DEMO-R1-RFQ.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in files: z.write(p,p.relative_to(ROOT).as_posix())
index=[dict(path=str(p.relative_to(ROOT)).replace('\\','/'),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in files]
(dest/'rfq-manifest.json').write_text(json.dumps(index,indent=2))
print('Packaged',len(files),'files, bytes:',(dest/'THENAR-C9-DEMO-R1-RFQ.zip').stat().st_size)
