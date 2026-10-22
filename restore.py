from pathlib import Path
import hashlib,json
r=Path(__file__).resolve().parent;m=json.loads((r/'parts.json').read_text());out=r/m['output']
if out.exists():
 if hashlib.sha256(out.read_bytes()).hexdigest()==m['sha256']:print('Already restored:',out);raise SystemExit(0)
 raise SystemExit('Output already exists with different contents; refusing to overwrite.')
for p in m['parts']:
 if hashlib.sha256((r/p['name']).read_bytes()).hexdigest()!=p['sha256']:raise SystemExit('Part missing or damaged: '+p['name'])
tmp=out.with_suffix('.zip.tmp')
with tmp.open('wb') as f:
 for p in m['parts']:f.write((r/p['name']).read_bytes())
if hashlib.sha256(tmp.read_bytes()).hexdigest()!=m['sha256']:raise SystemExit('ZIP integrity check failed')
tmp.rename(out);print('Restored and SHA256 verified:',out)
