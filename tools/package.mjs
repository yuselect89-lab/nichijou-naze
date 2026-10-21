import {execFileSync} from 'node:child_process';
execFileSync('python',['-c',String.raw`from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
import hashlib
r=Path.cwd();files=[p for p in r.rglob('*') if p.is_file() and not any(x in p.relative_to(r).parts for x in ['node_modules','.git','.cache','__pycache__']) and p.suffix not in ['.pyc','.log']]
(r/'HANDOFF_SHA256SUMS.txt').write_text('\n'.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(r)) for p in sorted(files) if p.name!='HANDOFF_SHA256SUMS.txt')+'\n')
files=list(set(files+[r/'HANDOFF_SHA256SUMS.txt']))
out=r.parent/'nichijou-naze-common-library-integrated-v1.0.1.zip'
with ZipFile(out,'w',ZIP_DEFLATED) as z:
 for p in sorted(files):z.write(p,'nichijou-naze/'+str(p.relative_to(r)))
with ZipFile(out) as z:assert z.testzip() is None
print(str(out),out.stat().st_size,'bytes',len(files),'files')`],{stdio:'inherit'});
