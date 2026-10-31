from pathlib import Path
from PIL import Image
import subprocess,json,math,hashlib,xml.etree.ElementTree as ET
B=Path(__file__).resolve().parents[1];errors=[];records=[]
def run(c):
 p=subprocess.run(c,capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stderr[-1000:])
 return p.stdout
for i in range(1,7):
 c=f'C{i:02d}';s=json.loads((B/'scenes'/(c+'.json')).read_text());f=B/'previews_1080'/(c+'_G2_V3_silent.mp4')
 run(['ffmpeg','-v','error','-y','-i',str(f),'-vf','scale=360:640','-an','-c:v','libx264','-crf','18','-preset','veryfast','-threads','2',str(B/'previews_360'/f.name)])
 anchors={'C01':.52,'C02':.9,'C03':.72,'C04':.9,'C05':.82,'C06':.85};n=s.get('frames',round(s['duration']*24));frame=round((n-1)*anchors[c])
 run(['ffmpeg','-v','error','-y','-i',str(f),'-vf',f'select=eq(n\\,{frame})','-frames:v','1','-threads','1',str(B/'qc'/(c+'_1080.png'))])
 with Image.open(B/'qc'/(c+'_1080.png')) as im:im.resize((360,640),Image.Resampling.LANCZOS).save(B/'qc'/(c+'_360.png'))
 for o in s['items']:
  if not (B/o['asset']).is_file():errors.append(c+' missing '+o['asset'])
  if o['group']=='labels':
   im=Image.open(B/o['asset'])
   if any(abs(k[3]/k[4]-im.width/im.height)>.01 for k in o['keys']):errors.append(c+' distorted label '+o['id'])
  if o['group']=='photos':
   im=Image.open(B/o['asset'])
   if any(k[3]>im.width+.01 or k[4]>im.height+.01 for k in o['keys']):errors.append(c+' photo upscale '+o['id'])
 ET.parse(B/'scenes'/(c+'.svg'))
 print('SCALED_AND_EXTRACTED',c,flush=True)
for suffix in ['1080','360']:
 for block,cuts in [('A',[1,2,3]),('B',[4,5,6]),('C02_C04',[2,3,4]),('C05_C06',[5,6]),('ALL',[1,2,3,4,5,6])]:
  listing=B/'source'/f'concat_{suffix}_{block}.txt';listing.write_text('\n'.join("file '"+'../'+f'previews_{suffix}/C{i:02d}_G2_V3_silent.mp4'+"'" for i in cuts))
  run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(listing),'-c','copy','-an','-movflags','+faststart',str(B/f'previews_{suffix}'/f'PREVIEW_{block}_G2_V3_silent.mp4')])
for f in sorted([*B.glob('C*/*.mov'),*B.glob('previews_*/*.mp4'),*B.glob('candidate_tests/*.mp4')]):
 try:
  d=json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(f)]));streams=d['streams'];vs=[x for x in streams if x['codec_type']=='video'];assert len(vs)==1 and not any(x['codec_type']=='audio'for x in streams)
  expected=(360,640) if f.parent.name=='previews_360' or '_360' in f.stem else (1080,1920);v=vs[0];assert (v['width'],v['height'])==expected
  assert v['r_frame_rate']=='24/1'
  if f.suffix=='.mov':assert v['codec_name']=='qtrle' and v['pix_fmt']=='argb'
  if f.name[:3] in ['C01','C02','C03','C04','C05','C06']:
   expected_n=json.loads((B/'scenes'/(f.name[:3]+'.json')).read_text())['frames'];assert int(v['nb_frames'])==expected_n
  run(['ffmpeg','-v','error','-xerror','-threads','1','-i',str(f),'-an','-f','null','-'])
  records.append({'file':str(f.relative_to(B)),'resolution':expected,'duration_s':float(d['format']['duration']),'frame_count':int(v.get('nb_frames',0)),'codec':v['codec_name'],'pixel_format':v['pix_fmt'],'audio_streams':0,'full_decode':'PASS','bytes':f.stat().st_size})
 except Exception as e:errors.append(str(f.relative_to(B))+': '+str(e))
 print('CHECKED',str(f.relative_to(B)),flush=True)
for f in B.rglob('*.png'):
 try:
  with Image.open(f)as im:im.verify()
 except Exception as e:errors.append(str(f)+str(e))
report={'technical_result':'PASS'if not errors else'FAIL','records':records,'errors':errors,'v3_external_visual_approval':False,'r1_upstream_photo_original_match':False,'new_original_matches_supplied_manifest':True,'audio_year_issue_resolved':False}
(B/'docs/technical_qc.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print('TECHNICAL_RESULT',report['technical_result'],flush=True)
raise SystemExit(bool(errors))
