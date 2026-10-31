from pathlib import Path
from PIL import Image,ImageChops
import json,math,subprocess,numpy as np
B=Path(__file__).resolve().parents[1];roles={'C01':'question','C03':'reaction','C04':'process','C06':'payoff'};rows=[];errors=[]
for cut,role in roles.items():
 seed=Image.open(B/'assets/reuse_input/shared/characters'/f'{role}_upperbody.png').convert('RGBA');asset=Image.open(B/'assets/characters'/f'{role}.png').convert('RGBA');expected=seed.resize((asset.width,round(seed.height*asset.width/seed.width)),Image.Resampling.LANCZOS)
 match=asset.size==expected.size and np.array_equal(np.array(asset),np.array(expected))
 if not match:errors.append(cut+' upper-body derivative has been cropped or changed')
 scene=json.loads((B/'scenes'/(cut+'.json')).read_text());obj=next(o for o in scene['items']if o['group']=='presenter');bbox=asset.getchannel('A').getbbox();n=math.ceil(scene['duration']*24);lost=[];visible=0
 from render_project import value
 for k in range(n):
  x,y,w,h,a=value(obj,k/24)
  if a<=.001:continue
  visible+=1
  l=x+bbox[0]*w/asset.width;r=x+bbox[2]*w/asset.width;top=y+bbox[1]*h/asset.height;bot=y+bbox[3]*h/asset.height
  if l<0 or r>940 or top<0 or bot>1510:lost.append({'frame':k,'unclipped_alpha_bounds':[l,top,r,bot]})
 if lost:errors.append(cut+' presenter loses pixels at safety/canvas bounds')
 t={'C01':3.8,'C03':4.4,'C04':.8,'C06':3.8}[cut];x,y,w,h,a=value(obj,t);x,y,w,h=map(round,[x,y,w,h])
 path=B/cut/'presenter_motion_RGBA.mov';raw=subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',str(path),'-vf','alphaextract','-frames:v','1','-pix_fmt','gray','-f','rawvideo','-'],capture_output=True,check=True).stdout
 actual=np.frombuffer(raw,dtype=np.uint8).reshape(1920,1080);want=np.array(asset.resize((w,h),Image.Resampling.LANCZOS).getchannel('A'));same=np.array_equal(actual[y:y+h,x:x+w],want)
 if not same:errors.append(cut+' encoded presenter silhouette differs from full derivative')
 rows.append({'cut':cut,'role':role,'seed_upper_body_size':seed.size,'derivative_size':asset.size,'whole_seed_resize_match':match,'timeline_frames_checked':n,'visible_frames_checked':visible,'presenter_bounds_checked_before_safety_clip':True,'clipped_frames':lost,'encoded_alpha_full_gesture_match':same,'encoded_sample_s':t})
report={'result':'PASS'if not errors else'FAIL','scope':'Full upper-body crop of the registered character and encoded alpha; no post-resize crop or safety-clip truncation','cuts':rows,'errors':errors}
(B/'docs/presenter_integrity_qc.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2));raise SystemExit(bool(errors))
