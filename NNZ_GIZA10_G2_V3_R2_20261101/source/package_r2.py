"""Validate current reports, hash every delivered file, and create one ZIP."""
from pathlib import Path
import json,hashlib,zipfile,shutil,argparse
B=Path(__file__).resolve().parents[1]
def sha(p):
 h=hashlib.sha256()
 with p.open('rb')as f:
  for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk)
 return h.hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,default=B.parent/(B.name+'_ALL_ASSETS.zip'));args=ap.parse_args()
 tech=json.loads((B/'docs/technical_qc.json').read_text());assert tech['technical_result']=='PASS' and len(tech['records'])==48
 assert len(list(B.glob('C*/*_RGBA.mov')))==24
 for f,key in [('presenter_integrity_qc.json','result'),('all_frame_safety_qc.json','result'),('input_manifest_verification.json','result')]:assert json.loads((B/'docs'/f).read_text())[key]=='PASS'
 assert all(r['exit_code']==0 for r in json.loads((B/'docs/repository_checks.json').read_text()))
 assert len(json.loads((B/'docs/alpha_qc.json').read_text()))==24
 assert all(not r['overlaps'] for r in json.loads((B/'docs/photo_collision_qc.json').read_text()))
 assert sha(B/'shared/approved_opening_banner.png')=='e6b63c322c996f543930a027db8981c2388e88441656655822c34bb4e2e2fd37'
 assert sha(B/'docs/reference_locks/02_G2_V2_VISUAL_DESIGN_LOCK_UNCHANGED.md')==sha(B/'docs/r1_history/reference_locks/02_G2_V2_VISUAL_DESIGN_LOCK_UNCHANGED.md')
 total=0
 for i in range(1,7):
  c=f'C{i:02d}';n=json.loads((B/'scenes'/f'{c}.json').read_text())['frames'];total+=n
  for g in ['photos','diagram','labels','presenter']:
   r=next(r for r in tech['records']if r['file']==f'{c}/{g}_motion_RGBA.mov');assert r['frame_count']==n and r['audio_streams']==0
 assert total==731
 for p in B.rglob('__pycache__'):shutil.rmtree(p)
 files=[p for p in sorted(B.rglob('*'))if p.is_file()and p.name!='ASSET_MANIFEST.json']
 rows=[dict(path=p.relative_to(B).as_posix(),bytes=p.stat().st_size,sha256=sha(p))for p in files]
 (B/'ASSET_MANIFEST.json').write_text(json.dumps(dict(revision='G2_V3_R2_20261101',files=rows),ensure_ascii=False,indent=2))
 with zipfile.ZipFile(args.out,'w',zipfile.ZIP_DEFLATED,compresslevel=2)as z:
  for p in sorted(B.rglob('*')):
   if p.is_file():z.write(p,p.relative_to(B.parent))
 with zipfile.ZipFile(args.out)as z:assert z.testzip()is None
 print(json.dumps(dict(zip=str(args.out),bytes=args.out.stat().st_size,manifest_files=len(rows),zip_crc='PASS',alpha_movies=24,fully_decoded_videos=48,total_frames=731),indent=2))
if __name__=='__main__':main()
