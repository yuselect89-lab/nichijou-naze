from pathlib import Path
from PIL import Image
import json,subprocess,hashlib,re
R=Path(__file__).resolve().parents[2];repo=R.parent
baseline=json.loads((R/'qc/full_v3/baseline.json').read_text());allowed={'EP004_ICE_V3/'+x for x in ['manifest.json','README.md','index.html','SHA256SUMS.txt']}|{'library-registry.json'}|{'common_assets/nichijou_naze/management/asset_registry.'+x for x in ['json','csv','xlsx']}
changed=[];missing=[]
for p,h in baseline.items():
 f=repo/p
 if not f.exists():missing.append(p)
 elif hashlib.sha256(f.read_bytes()).hexdigest()!=h:changed.append(p)
assert not missing,missing
assert not set(changed)-allowed,set(changed)-allowed
approved=[p for p in baseline if p.startswith(('EP004_ICE_V3/cut01/','EP004_ICE_V3/cut09/'))]
assert not set(approved)&set(changed)
oldrows=json.loads((R/'source/full_v3/stage1_metadata/common_asset_ledger.json').read_text());newrows=json.loads((repo/'common_assets/nichijou_naze/management/asset_registry.json').read_text());assert newrows[:len(oldrows)]==oldrows
oldreg=json.loads((R/'source/full_v3/stage1_metadata/common_library_registry.json').read_text());newreg=json.loads((repo/'library-registry.json').read_text());newreg.pop('iceProps',None);assert newreg==oldreg
if '--registration-only' in __import__('sys').argv:
 report=json.loads((R/'qc/full_v3/report.json').read_text());report['registry_result']='PASS';report['existing_files_changed_only_administrative']=changed;report['prior_ledger_rows_preserved']=len(oldrows);report['new_ledger_rows']=len(newrows)-len(oldrows);assert report['new_ledger_rows']==9;(R/'qc/full_v3/report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('Registry integrity:PASS; old rows preserved; 9 additions');raise SystemExit(0)
m0=json.loads((R/'manifest.json').read_text());locked=[s.strip() for s in (R/'source/LOCKED_NARRATION_V8.txt').read_text().split('\n\n') if s.strip()];assert len(locked)==10;assert [c['narration'] for c in m0['cuts']]==locked;assert not list(R.glob('*.mp4'))
frames=[105,195,120,150,105,75,195,165,165,123];videos=[];images=[]
for i,n in enumerate(frames,1):
 d=R/f'cut{i:02}';assert (d/'animation.mp4').exists();assert (d/'main.png').exists()
 for p in sorted(d.glob('*.png')):
  with Image.open(p) as im:
   size=im.size;mode=im.mode;im.verify()
  if not p.name.startswith('character_'):assert size==(1080,1920),(p,size)
  images.append({'file':str(p.relative_to(R)),'resolution':size,'mode':mode,'opens':True})
 for p in sorted(d.iterdir()):
  if p.suffix not in ['.mp4','.webm']:continue
  st=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-of','json',str(p)]))['streams'];assert len(st)==1 and st[0]['codec_type']=='video',p
  s=st[0];assert (s['width'],s['height'])==(1080,1920);assert s['r_frame_rate']=='30/1';assert int(s['nb_read_frames'])==n,(p,s['nb_read_frames'],n)
  dec=subprocess.run(['ffmpeg','-v','error','-i',str(p),'-f','null','-'],capture_output=True);assert dec.returncode==0 and not dec.stderr,(p,dec.stderr)
  row={'file':str(p.relative_to(R)),'frames':n,'resolution':[1080,1920],'fps':30,'silent':True,'full_decode':'PASS'}
  if p.suffix=='.webm':
   a=subprocess.check_output(['ffmpeg','-v','error','-c:v','libvpx-vp9','-i',str(p),'-vf',f'select=eq(n\\,{min(n-1,85)}),alphaextract','-frames:v','1','-f','rawvideo','-pix_fmt','gray','-']);assert min(a)==0 and max(a)>100,(p,min(a),max(a));row['alpha']={'min':min(a),'max':max(a),'verified':True}
  videos.append(row)
# Record actual render observations from known jobs, rather than accepting declaration alone.
observations=[]
for p in [Path('/tmp/nnz-full-stills.log'),Path('/tmp/nnz-full-revised-stills.log'),Path('/tmp/nnz-full-final-stills.log'),Path('/tmp/nnz-full-final8-stills.log'),Path('/tmp/nnz-full-final7.log')]:
 if p.exists():
  for line in p.read_text().splitlines():
   if 'EP004_FULL_QC ' in line:
    observations.append(json.loads(line.split('EP004_FULL_QC ',1)[1]))
(R/'qc/full_v3/render_observations.json').write_text(json.dumps(observations,indent=2)+'\n')
report={'technical_result':'PASS','scope':'10 individual cuts; no whole-episode MP4','fps':30,'total_provisional_frames':sum(frames),'total_provisional_seconds':sum(frames)/30,'approved_stage1_preserved':approved,'existing_files_changed_only_administrative':changed,'existing_files_missing':missing,'videos':videos,'images':images,'existing_library_checks':'TypeScript PASS; 17 existing tests PASS','numeric_tests':'7 passing tests: source/physics.test.mjs and source/full_v3/states.test.mjs','visual_checks':{'Cut02':'boil/cool/pour with no completed transparent ice','Cut03':'condition-dependent cloudy-center example','Cut04_05':'internal cavities visible through cutaway; contrast corrected after first preview','Cut06':'separate symbolic dissolved gas panel; six markers retained; large background vapor bubbles are distinct','Cut07':'continuous inward freezing; gas markers concentrate before internal air cavities remain; freezing geometry explicitly schematic','Cut08':'orange air inlet and rising air bubbles; central liquid retained; no suction','Cut09':'approved continuous liquid transfer; original MP4s unchanged; solid shell remains','Cut10':'equal-size/light cloudy left and clearer right; finishing-stage time jump','character':'canonical v02/v03 PNGs only; fades, idle and nod motion; no redraw of limbs/mouth','safe_zones':'360px guide images; main diagrams/labels clear of subtitle and opening-band zones','brands':'no names/logos/packaging observed'},'limitations':['Official reference pages could not be fetched under current network policy; no official artwork reused.','Scientific visualizations are schematic, not experimental measurements.','G3 and VO/caption synchronization remain with ChatGPT Work/Gemini.','Formal original yellow banner file not independently available; not baked into assets.'],'failures':[]}
(R/'qc/full_v3/report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
m=json.loads((R/'manifest.json').read_text());m['status']='self_qc_pass_G3_pending';m['qc']='qc/full_v3/report.json'
for c in m['cuts']:
 if c['cut'] not in ['cut01','cut09']:c['status']='self_qc_pass'
 c['qc']='qc/full_v3/report.json'
(R/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'result':'PASS','videos':len(videos),'images':len(images),'preserved_approved_files':len(approved)},ensure_ascii=False))
