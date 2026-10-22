"""Versioned local backup. Never claims Drive success. Parts stay below GitHub's hard file limit."""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import json,hashlib,zipfile,subprocess,os,atexit
R=Path(__file__).resolve().parents[2];M=R/'common_assets/nichijou_naze/management';cat=json.loads((M/'catalog.v1.json').read_text());stamp=datetime.now(ZoneInfo('Asia/Tokyo')).strftime('%Y%m%d_%H%M%S');D=R/f'releases/NNZ_LIBRARY_OPERATIONS_V1_{stamp}';D.mkdir(exist_ok=False)
lock=R/'common_assets/nichijou_naze/management/operations/v1/.register.lock'
lock_fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY)
def release_lock():
 os.close(lock_fd);lock.unlink(missing_ok=True)
atexit.register(release_lock)
files=set()
for directory in ['common_assets/nichijou_naze','public/common_assets/nichijou_naze','tools/library','src/library-reuse','episodes/LIBRARY_REUSE_TEST','validation/library-ops','vendor/common-library/1.0.0/common_assets/nichijou_naze']:
 for p in (R/directory).rglob('*'):
  if p.is_file() and '__pycache__' not in p.parts and p.name not in ['backup-status.json','final-report.json','.register.lock']:files.add(str(p.relative_to(R)))
for a in cat['assets']:files.update(a['files']);files.add(a['qc']['report'])
files.update(['library-registry.json','tools/library.mjs','tools/ice-assets.mjs','docs/LIBRARY_OPERATIONS.md','docs/WORK_HANDOFF.md','docs/PRESENTER_DIRECTION.md','docs/library-manifest.schema.json','AGENTS.md','package.json','package-lock.json','tsconfig.json','README.md'])
for p in (R/'tests').glob('library-*.test.mjs'):files.add(str(p.relative_to(R)))
files=sorted(files);assert all((R/p).is_file() for p in files)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
records=[{'path':p,'bytes':(R/p).stat().st_size,'sha256':sha(R/p)} for p in files];groups=[];current=[];size=0
for r in records:
 if current and size+r['bytes']>75_000_000:groups.append(current);current=[];size=0
 assert r['bytes']<90_000_000
 current.append(r);size+=r['bytes']
if current:groups.append(current)
parts=[]
for i,group in enumerate(groups,1):
 dest=D/f'NNZ_LIBRARY_OPS_V1_part{i:02}.zip'
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for r in group:z.write(R/r['path'],r['path'])
 with zipfile.ZipFile(dest) as z:
  assert z.testzip() is None
  for r in group:assert hashlib.sha256(z.read(r['path'])).hexdigest()==r['sha256'],'Concurrent file change detected'
 assert dest.stat().st_size<100_000_000
 parts.append({'file':dest.name,'bytes':dest.stat().st_size,'sha256':sha(dest)})
index={'schema_version':1,'backup_id':stamp,'timezone':'Asia/Tokyo','scope':'common library, versioned registrations, dependency closure, tooling, reuse project and QC. Full EP movies are separately retained in original GitHub delivery.','git_base_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'working_tree_snapshot':True,'parts':parts,'files':records,'drive':{'url':'https://drive.google.com/drive/folders/1YmGCqmzf_XndpvS62sMKFr4wdTrI-CK7','status':'not_saved','reason':'CONNECT returned HTTP403; no Drive connector/ready Google identity.'},'restore':'python tools/library/restore.py <backup-index.json> <new_destination>'}
(D/'backup-index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2)+'\n')
(D/'README.md').write_text('# 共通素材ライブラリ 運用V1バックアップ\n\n全part ZIPとbackup-index.jsonを同じ場所へ保存してください。各ZIPを同じ新規フォルダへ展開すると復元できます。restore.pyはZIPと全ファイルのSHA256を検証して復元します。\n\nGoogle Driveには保存できていません。ローカルとGitHubでの保管です。EP004本編素材の全体は以前の納品ZIPで別途保管してください。\n')
(R/'validation/library-ops/backup-status.json').write_text(json.dumps({'local_status':'verified_archive_created','index':str((D/'backup-index.json').relative_to(R)),'drive':index['drive']},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'index':str((D/'backup-index.json').relative_to(R)),'parts':parts,'files':len(records),'drive_saved':False},ensure_ascii=False,indent=2))
