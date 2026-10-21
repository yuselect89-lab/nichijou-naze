"""QC and human-review packet for V3 stage1 only. Never approve or create other cuts."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,subprocess,numpy as np,shutil,zipfile
R=Path(__file__).resolve().parents[1];repo=R.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
font_path=repo/'public/series/v1/NotoSansCJKjp-Bold.otf'
font=ImageFont.truetype(str(font_path),30);small=ImageFont.truetype(str(font_path),23)
baseline=json.loads((R/'qc/protected_before.json').read_text());changed=[p for p,v in baseline.items() if not(repo/p).exists() or sha(repo/p)!=v]
assert not changed,changed
videos=[]
for file,frames,alpha in [('cut01/animation.mp4',105,False),('cut09/base_animation.mp4',165,False),('cut09/animation.mp4',165,False),('cut09/character_overlay.webm',165,True),('cut09/labels_overlay.webm',165,True)]:
 p=R/file;info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(p)]));streams=info['streams'];v=next(s for s in streams if s['codec_type']=='video')
 assert (v['width'],v['height'],v['r_frame_rate'])==(1080,1920,'30/1');assert not any(s['codec_type']=='audio' for s in streams)
 # Full decode/frame count, including explicit alpha-aware VP9 decode for WebM.
 cmd=['ffmpeg','-v','error']+(['-c:v','libvpx-vp9'] if alpha else [])+['-i',str(p),'-f','null','-'];subprocess.run(cmd,check=True)
 count=int(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-count_frames','-show_entries','stream=nb_read_frames','-of','default=nw=1:nk=1',str(p)]));assert count==frames
 a=None
 if alpha:
  raw=subprocess.check_output(['ffmpeg','-v','error','-c:v','libvpx-vp9','-i',str(p),'-vf','select=eq(n\\,85),alphaextract','-frames:v','1','-pix_fmt','gray','-f','rawvideo','-'])
  a=np.frombuffer(raw,dtype='uint8');assert len(a)==1080*1920 and a.min()==0 and a.max()>240 and (a==0).mean()>.65
 videos.append({'file':file,'frames':count,'resolution':[1080,1920],'fps':30,'audio':False,'alpha':alpha,'alpha_zero_fraction':float((a==0).mean()) if a is not None else None,'sha256':sha(p)})
stills=[]
for folder in ['cut01','cut09','preview']:
 for p in (R/folder).glob('*.png'):
  im=Image.open(p);im.load()
  if p.name=='character_point_right.png':assert im.size==(1536,2304)
  else:assert im.size==(1080,1920)
  stills.append({'file':str(p.relative_to(R)),'size':im.size,'mode':im.mode})
observations=json.loads((R/'qc/render_observations.json').read_text());assert {x['frame'] for x in observations}=={0,15,30,45,60,85,110,135,150,164}
assert len({x['solidSignature'] for x in observations})==1
assert all(x['webgl'] for x in observations)
for x in observations:
 assert abs(x['sourceVolume']+x['receiverVolume']-4.50892)<1e-9
 b=x['importantBounds'];assert b['left']>=72 and b['right']<=920 and b['top']>=320 and b['bottom']<=1480
# Actual PNG of model has true transparent corners and opaque drawn pixels.
model=Image.open(R/'cut09/model.png');assert model.mode=='RGBA';a=np.array(model)[:,:,3];assert a.min()==0 and a.max()>240
# Export the prescribed state timeline for Work and numeric review.
js="import {drainageState,parameters} from './EP004_ICE_V3/source/physics.mjs';console.log(JSON.stringify({parameters,states:Array.from({length:165},(_,i)=>drainageState(i))}));"
states=json.loads(subprocess.check_output(['node','--input-type=module','-e',js],cwd=repo))
(R/'qc/volume_timeline.json').write_text(json.dumps(states,indent=2)+'\n')
subprocess.run(['node','--test',str(R/'source/physics.test.mjs')],cwd=repo,check=True)
# Extract final encoded composite frames for preview parity, not just source renders.
for f in [0,30,60,85,110,135,164]:
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(R/'cut09/animation.mp4'),'-vf',f'select=eq(n\\,{f})','-frames:v','1',str(R/f'preview/cut09-encoded-{f}.png')],check=True)
 shutil.copy2(R/f'preview/cut09-encoded-{f}.png',R/f'preview/cut09-{f}.png')
shutil.copy2(R/'preview/cut09-encoded-85.png',R/'cut09/main.png')
def pastefit(sheet,p,x,y,w,h):
 im=Image.open(p).convert('RGB');im.thumbnail((w,h),Image.Resampling.LANCZOS);sheet.paste(im,(x+(w-im.width)//2,y+(h-im.height)//2))
sheet=Image.new('RGB',(1800,1360),'#eaf1ef');d=ImageDraw.Draw(sheet)
items=[('Cut01 実写風再現','cut01/main.png'),('Cut09 吸水前','preview/cut09-encoded-0.png'),('Cut09 排水中','preview/cut09-encoded-85.png'),('Cut09 排水後','preview/cut09-encoded-164.png')]
for i,(title,file) in enumerate(items):
 pastefit(sheet,R/file,i*450+18,70,414,736);d.text((i*450+22,20),title,font=font,fill='#204650')
for i,f in enumerate([0,30,60,85,110,135,164]):
 pastefit(sheet,R/f'preview/cut09-encoded-{f}.png',i*255+10,880,235,418);d.text((i*255+14,1320),f'{f/30:.2f}秒',font=small,fill='#204650')
sheet.save(R/'preview/contact_sheet.jpg',quality=94)
# A before/after comparison uses only previous own-series stills, never official source imagery.
sheet=Image.new('RGB',(1480,1510),'#edf3f1');d=ImageDraw.Draw(sheet)
for row,cut in enumerate(['cut01','cut09']):
 for col,(label,p) in enumerate([('旧V1',Path('/workspace/EP004_ICE')/cut/'main.png'),('V3 品質試作',R/cut/'main.png')]):
  x=col*740;y=row*755;pastefit(sheet,p,x+170,y+55,360,640);d.text((x+170,y+10),cut+' '+label,font=font,fill='#204650')
sheet.save(R/'preview/before_after.jpg',quality=94)
# Guides are separate QC artefacts and never enter delivered cut MP4s.
guides=[]
for cut in ['cut01','cut09']:
 im=Image.open(R/cut/'main.png').convert('RGBA');overlay=Image.new('RGBA',im.size);d=ImageDraw.Draw(overlay)
 for box,color,text in [((80,150,1000,292),(255,210,0,100),'冒頭帯の予約範囲'),((96,78,984,92),(230,168,20,180),''),((96,1500,920,1740),(27,52,64,145),'字幕の予約範囲'),((920,320,1080,1920),(210,70,70,65),'UI'),((0,1740,1080,1920),(210,70,70,65),'下部UI')]:
  d.rectangle(box,fill=color,outline=(255,255,255,180),width=3)
  if text:d.text((box[0]+8,box[1]+10),text,font=font,fill=(255,255,255,255))
 checked=Image.alpha_composite(im,overlay).convert('RGB');checked.save(R/f'preview/{cut}_safezone.jpg',quality=94);guides.append(checked)
sheet=Image.new('RGB',(720,700),'#edf3f1')
for i,im in enumerate(guides):im.thumbnail((360,640));sheet.paste(im,(i*360,35))
ImageDraw.Draw(sheet).text((15,5),'360px幅・ガイドはQC専用',font=small,fill='#204650');sheet.save(R/'preview/safezone_checks.jpg',quality=94)
report={'stage':1,'technical_result':'PASS','visual_quality':'Self-reviewed; user approval pending','G3':'not performed','remaining_cuts':'Cut02-08+Cut10 not started; await user approval',
 'videos':videos,'stills':stills,'preserved_existing_files':len(baseline),'existing_files_changed':changed,
 'physics':{'tests_passed':3,'core_volume_decreases_continuously':True,'receiver_gain_matches_core_loss':True,'ice_geometry':'Fixed U-shaped solid, constant canonical mesh signature and static transforms; checked in sampled images','receiver_capacity':'actual width1.04 × depth3.72 × usable height1.40, enough for4.46223 normalized-volume units','initial_volume':4.50892,'final_residual_volume':.04669,'model':'Prescribed geometric schematic, not CFD; ignores small pipe hold-up.'},
 'safe_zone':'Important3D geometry withinx72..920,y320..1480. Short labels40px; existing character fullbody320px. Checked encoded frames and360px guide images.',
 'visual_review':{'cut01':'Recognizable cloudy household cube from firstframe, clear outer rim, natural kitchen reflections, fullbleed; AI reconstruction declared.','cut09':'Large real3D extruded/beveled ice mesh, metal frame, visible depth; cyan liquid distinguished from translucent ice; stable water surface without z-fighting; upward suction and visible discharge into receiver; final cavity remains.','character':'Unchanged verified V02 point_right; whole-sprite motion only; no rig/lip-sync.','series_overlays':'No banner, captions, progress, audio or music in production MP4s. Guide images separate.'},
 'limitations':['Quality approval by user and independent G3 are pending.','No old rough MP4 or independent original formal banner PNG found.','Official manufacturing reference text was not independently retrieved under network restrictions.','3D is a stylized explanatory reconstruction, not photoreal factory footage or measured CFD.','Cut01 generated source941x1672 normalized to1080x1920.','VO timing remains provisional; Work edits and supplies formal common overlays.'],
 'implementation_issues_resolved':['Initial CPU Cycles draft rejected for visible noise and slow animation cost.','Chromium legacy swiftshader context failed; supported swangle rendered WebGL2 successfully.','A near-coplanar liquid surface caused grid artefacts; separated surface by0.008worldunits and reduced ripples.','Receiver depth matches liquid volume; no undersized receiver pretending to hold all outflow.','Alpha-WebM timestamp rounding initially added1frame; final composite constrained to165frames.','Callout leaders fade together with their labels.'],
 'scientific_reference_status':'Checked against user V8+V3 brief and geometric continuity; independent official-site verification pending.'}
(R/'qc/stage1_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
manifest=json.loads((R/'manifest.json').read_text());manifest['technical_qc']='PASS';manifest['quality_approval']='pending';(R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'technical_qc':'PASS','existing_files_unchanged':len(baseline),'videos':len(videos),'stage':1,'quality_approval':'PENDING'},indent=2))
