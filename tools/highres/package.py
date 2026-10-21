from pathlib import Path
import hashlib,zipfile
r=Path(__file__).resolve().parents[2]
folders=['common_assets/nichijou_naze/characters/female_v01','common_assets/nichijou_naze/management','validation/highres','src/highres-validation']
files=[p for d in folders for p in (r/d).rglob('*') if p.is_file() and '__pycache__' not in str(p)]
files += [r/'src/integration/character.ts',r/'tools/highres/install.py',r/'docs/HIGHRES_DELIVERY.md']
files=sorted(set(files))
checksum=r/'validation/highres/SHA256SUMS.txt'
checksum.write_text('\n'.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(r)) for p in files if p!=checksum)+'\n')
files=sorted(set(files+[checksum]))
out=r/'releases/NNZ_CHAR_FEMALE_01_v02_highres.zip'
if out.exists():raise RuntimeError('Refusing to overwrite a published archive')
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
    for p in files:z.write(p,str(p.relative_to(r)))
with zipfile.ZipFile(out) as z:assert z.testzip() is None
print(out,out.stat().st_size,'bytes',len(files),'files')
