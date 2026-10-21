from pathlib import Path
import hashlib,shutil
r=Path(__file__).resolve().parents[2]
source=r/'common_assets/nichijou_naze/characters/female_v01'
target=r/'public/common_assets/nichijou_naze/characters/female_v01'
copied=0;skipped=0
for sub in ['poses','thumbs']:
    for p in (source/sub).glob('*.png'):
        dest=target/sub/p.name
        if dest.exists():
            if hashlib.sha256(p.read_bytes()).digest()!=hashlib.sha256(dest.read_bytes()).digest():raise RuntimeError('Different existing runtime file; refusing overwrite: '+str(dest))
            skipped+=1;continue
        dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest);copied+=1
snapshot=target/'versions/v02_highres/manifest.json';snapshot.parent.mkdir(parents=True,exist_ok=True)
if not snapshot.exists():shutil.copy2(source/'manifest.json',snapshot)
elif snapshot.read_bytes()!=(source/'manifest.json').read_bytes():raise RuntimeError('Manifest version already exists with different contents')
print(f'copied={copied} identical_skipped={skipped}')
