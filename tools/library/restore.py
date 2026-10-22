from pathlib import Path,PurePosixPath
import json,hashlib,zipfile,sys,shutil
index=Path(sys.argv[1]).resolve();D=Path(sys.argv[2]).resolve();m=json.loads(index.read_text());assert not D.exists(),'Restore destination must not exist'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for part in m['parts']:assert sha(index.parent/part['file'])==part['sha256'],'ZIP hash mismatch'
expected={r['path']:r for r in m['files']}
# Pre-validate the complete member list before creating the destination.
seen=set()
for part in m['parts']:
 with zipfile.ZipFile(index.parent/part['file']) as z:
  for info in z.infolist():
   p=PurePosixPath(info.filename);assert not p.is_absolute() and '..' not in p.parts and '\\' not in info.filename
   assert info.filename in expected and info.filename not in seen
   assert (info.external_attr>>16)&0o170000 !=0o120000,'No symlinks allowed'
   seen.add(info.filename)
assert seen==set(expected)
D.mkdir(parents=True)
try:
 for part in m['parts']:
  with zipfile.ZipFile(index.parent/part['file']) as z:z.extractall(D)
 for p,r in expected.items():assert sha(D/p)==r['sha256'],p
except BaseException:shutil.rmtree(D);raise
print(json.dumps({'restored':str(D),'files':len(expected),'sha256':'PASS'},indent=2))
