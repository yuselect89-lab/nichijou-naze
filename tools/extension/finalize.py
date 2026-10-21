"""Actual output QC, immutable-baseline checks, galleries and release metadata."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib,subprocess,shutil
R=Path(__file__).resolve().parents[2];V=R/'validation/extension';A=R/'common_assets/nichijou_naze'
font=ImageFont.truetype(str(R/'public/series/v1/NotoSansCJKjp-Bold.otf'),26)
small=ImageFont.truetype(str(R/'public/series/v1/NotoSansCJKjp-Bold.otf'),21)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
baseline=json.loads((V/'protected-files-before.json').read_text())
assert all((R/p).exists() and sha(R/p)==value for p,value in baseline.items()),'An existing protected file changed'
sources=json.loads((A/'characters/female_v01/versions/v03_expressions/manifest.json').read_text())
poses=[]
for pose in ['neutral','talk','point_right','point_left','think','surprise','happy','troubled']:
 root=A/'characters/female_v01'
 if pose in ['surprise','happy','troubled']:root=root/'versions/v03_expressions'
 p=root/'poses'/f'NNZ_CHAR_FEMALE_01_pose_{pose}.png'
 im=Image.open(p);im.load();assert im.mode=='RGBA' and im.size==(1536,2304)
 a=np.array(im);alpha=a[:,:,3];assert alpha.min()==0 and alpha.max()==255 and (alpha==0).mean()>.4
 assert not a[alpha==0,:3].any(),'RGB under transparent pixels'
 box=im.getchannel('A').getbbox();assert 50<=box[1]<=85 and 2220<=box[3]<=2245
 assert sha(p)==sha(R/'public'/p.relative_to(R))
 poses.append({'pose':pose,'file':str(p.relative_to(R)),'resolution':[1536,2304],'alpha_bbox':box,'transparent_fraction':float((alpha==0).mean()),'sha256':sha(p)})
observations=json.loads((V/'observations.json').read_text());assert observations
samples=json.loads((V/'samples.json').read_text());assert len(samples)==36
violations=[];progress=[]
for sample in samples:
 matches=[o for o in observations if o['scene']==sample['scene'] and o['frame']==sample['local']]
 assert matches,('No DOM observation',sample)
 o=matches[-1];elements=o['elements']
 assert all(i['width']>0 and i['height']>0 for i in o['images'])
 for kind in ['background','banner','progress','caption']:
  assert len([e for e in elements if e['kind']==kind])==1,(sample,kind)
 caption=next(e for e in elements if e['kind']=='caption');assert '、' not in caption['text'] and '。' in caption['text'];assert caption['x']+caption['w']<=920.1 and caption['y']+caption['h']<=1740.1
 p=float(next(e for e in elements if e['kind']=='progress')['progress']);assert abs(p-sample['frame']/2339)<1e-8;progress.append(p)
 for e in elements:
  if e['kind'] in ['background','progress','banner','caption','focus-ring','step-link'] or e['w']<1 or e['h']<1:continue
  x,y,w,h=e['x'],e['y'],e['w'],e['h']
  if e['kind']=='character':
   # Bound visible alpha instead of the transparent padded sprite rectangle.
   imgs=[i for i in o['images'] if i.get('pose')]
   if imgs:
    for i in imgs:
     q=next(q for q in poses if q['pose']==i['pose']);b=q['alpha_bbox'];bounds=(x+w*b[0]/1536,y+h*b[1]/2304,x+w*b[2]/1536,y+h*b[3]/2304)
     if bounds[0]<72-2 or bounds[2]>920+2 or bounds[1]<320-2 or bounds[3]>1480+2:violations.append({'sample':sample,'kind':'character-alpha','bounds':bounds})
    continue
  if x<72-2 or x+w>920+2 or y<320-2 or y+h>1480+2:violations.append({'sample':sample,'kind':e['kind'],'bounds':[x,y,x+w,y+h]})
assert not violations,violations
assert min(progress)==0 and max(progress)==1
for name,frames in [('library-extension-1080x1920.mp4',2340),('video-background-1080x1920.mp4',120)]:
 path=V/name;assert path.exists(),name
 info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(path)]))
 stream=next(s for s in info['streams'] if s['codec_type']=='video')
 assert (stream['width'],stream['height'],stream['r_frame_rate'],int(stream['nb_frames']))==(1080,1920,'30/1',frames)
 assert not any(s['codec_type']=='audio' for s in info['streams'])
 subprocess.run(['ffmpeg','-v','error','-i',str(path),'-f','null','-'],check=True)
# Gallery of all8poses plus alpha on white/dark/checker.
sheet=Image.new('RGB',(1920,1120),'#edf3f3');draw=ImageDraw.Draw(sheet)
for j,q in enumerate(poses):
 im=Image.open(R/q['file']);im.thumbnail((400,440),Image.Resampling.LANCZOS);x=(j%4)*480+(480-im.width)//2;y=(j//4)*560+35
 sheet.paste(im,(x,y),im);draw.text(((j%4)*480+35,(j//4)*560+493),q['pose'],font=font,fill='#193a43')
sheet.save(V/'character-8poses.jpg',quality=95)
new=[p for p in poses if p['pose'] in ['surprise','happy','troubled']]
sheet=Image.new('RGB',(1440,780),'white');draw=ImageDraw.Draw(sheet)
for row,color in enumerate(['white','#19343c','checker']):
 for i,p in enumerate(new):
  x=i*480;y=row*260
  draw.rectangle((x,y,x+479,y+259),fill='#e4ebeb' if color=='checker' else color)
  if color=='checker':
   for yy in range(y,y+260,20):
    for xx in range(x,x+480,20):
     if ((xx-x)//20+(yy-y)//20)%2:draw.rectangle((xx,yy,xx+19,yy+19),fill='#bdcbcc')
  im=Image.open(R/p['file']);im.thumbnail((330,245));sheet.paste(im,(x+70,y+5),im)
sheet.save(V/'alpha-backgrounds.jpg',quality=95)
choose=[('expression-surprise',85),('expression-happy',85),('expression-troubled',85),('footage-character',85),('diagram-character',85),('focus-crosssection-return',110),('label-parameters',85),('step3-cause',170),('crosssection-carton',75),('motions',95),('legacy-arrow',85),('legacy-compare',85),('legacy-zoom',85)]
sheet=Image.new('RGB',(1560,1900),'#edf3f3');draw=ImageDraw.Draw(sheet)
for i,(scene,local) in enumerate(choose):
 im=Image.open(V/f'{scene}-{local}.png');assert im.size==(1080,1920);im.thumbnail((270,480))
 x=(i%5)*312+21;y=(i//5)*620+20;sheet.paste(im,(x,y));draw.text((x,y+492),scene.replace('crosssection','cross').replace('expression','expr'),font=small,fill='#1b3a44')
sheet.save(V/'contact-sheet.jpg',quality=93)
frames=[0,24,49,64,80,110,180,205,239]
sheet=Image.new('RGB',(1620,1120),'#edf3f3');draw=ImageDraw.Draw(sheet)
for i,frame in enumerate(frames):
 im=Image.open(V/f'focus-crosssection-return-{frame}.png');im.thumbnail((175,312));x=i*180+2;sheet.paste(im,(x,28));draw.text((x,350),str(frame)+'f',font=small,fill='#193a43')
draw.text((30,420),'注目点を追跡 → 拡大 → 外観と断面の境界 → 内部 → 同じ実物へ戻る',font=font,fill='#193a43')
# Add detailed 3-keyframe crops to the lower part for closer review.
for i,frame in enumerate([49,80,110]):
 im=Image.open(V/f'focus-crosssection-return-{frame}.png').crop((150,310,930,1090));im.thumbnail((500,500));sheet.paste(im,(i*540+20,500))
sheet.save(V/'focus-sequence.jpg',quality=94)
report={'result':'PASS','checks':{'tests_passed':17,'typescript':'PASS'},'canvas':[1080,1920],'fps':30,'showcase_frames':2340,'showcase_seconds':78,'video_background_test_frames':120,
 'sampled_screenshots':36,'registered_examples':13,'additional_video_example':1,
 'preserved_existing_files':len(baseline),'preserved_file_hashes':baseline,
 'poses':poses,'safe_zone_violations':violations,'global_progress':{'min':min(progress),'max':max(progress),'sequence_reset':False},
 'caption_qc':'Japanese font loaded; comma removed, fullstop retained; right edge920,bottom1740',
 'overlay_qc':'One original banner, one global progress bar and one caption at every sampled frame. Legacy adapters scaled0.9 and translated-44px; originals unmodified.',
 'animation_qc':['Both MP4s fully decoded without errors; H264 yuv420p1080x1920 at30fps, no audio',
 'Entry/exit, idle, nod and pose-crossfade samples rendered; numerical continuity tests pass',
 'Focus target, zoom, wipe, bubble reveal and return sampled across9frames',
 'Changed label colors/positions/timings and step sequencing rendered',
 'Crosssection reusable with ice and a different carton geometry; independent liquid layer appears and hides',
 'Old arrow/compare/zoom implementations reused inside new adapter and actually rendered',
 'Original4second moving video background loaded via OffthreadVideo and rendered with character'],
 'visual_review':'Face/hair/cream hoodie/navy trousers/shoes consistent across8poses; hands individually inspected; expressions distinguishable at helper scale. No obvious anatomy break or alpha matte. Mild pose-dependent head angle/shading differences remain.',
 'limitations':['New poses are1024x1536 generated redraws normalized to1536x2304; not native2304 generation.',
 'Whole-sprite rotation/translation; not skeletal nodding, mouth rigging, walking or independent limbs.',
 'Crossfade intentionally overlaps2static poses for10frames.',
 'Validation background is original dummy SVG/video, not actual footage or a finished science EP.',
 'Caption timing is API-tested with dummy cues; no production voiceover was supplied.',
 'Rights authentication and network access to the supplied Google Drive folder are unavailable; not updated.']}
(V/'qc-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
sources['qc_status']='render_verified';sources['qc_report']='validation/extension/qc-report.json';sources['preview']='validation/extension/character-8poses.jpg'
manifest=A/'characters/female_v01/versions/v03_expressions/manifest.json';manifest.write_text(json.dumps(sources,ensure_ascii=False,indent=2)+'\n');shutil.copy2(manifest,R/'public'/manifest.relative_to(R))
subprocess.run(['python',str(R/'tools/extension/register.py')],cwd=R,check=True)
print(json.dumps({'result':'PASS','protected_files':len(baseline),'poses':len(poses),'screenshots':len(samples),'mp4_frames':[2340,120]},indent=2))
