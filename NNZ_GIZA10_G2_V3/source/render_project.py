from pathlib import Path
from PIL import Image
import json,math,subprocess,sys,base64,html,argparse
B=Path(__file__).resolve().parents[1];CACHE={}
def load(p):
 if p not in CACHE:CACHE[p]=Image.open(B/p).convert('RGBA')
 return CACHE[p]
def value(o,t):
 ks=o['keys']
 if t<=ks[0][0]:return ks[0][1:]
 for a,b in zip(ks,ks[1:]):
  if t<=b[0]:
   f=(t-a[0])/(b[0]-a[0]);f=f*f*(3-2*f);return [x+(y-x)*f for x,y in zip(a[1:],b[1:])]
 return ks[-1][1:]
def layers(s,t):
 out={g:Image.new('RGBA',(1080,1920)) for g in s.get('layer_order',['photos','diagram','labels','presenter']) if any(o['group']==g for o in s['items'])}
 for o in s['items']:
  x,y,w,h,a=value(o,t);x,y,w,h=round(x),round(y),round(w),round(h)
  if a<.005 or w<1 or h<1 or x>1080 or y>1920 or x+w<0 or y+h<0:continue
  if o['group']=='presenter':
   native=load(o['asset'])
   if abs(h-native.height*w/native.width)>1:raise ValueError('Presenter aspect ratio changed: '+s['cut'])
  key=(o['asset'],w,h)
  if key not in CACHE:CACHE[key]=load(o['asset']).resize((w,h),Image.Resampling.LANCZOS)
  im=CACHE[key]
  if o['group']=='presenter':
   bb=im.getchannel('A').getbbox()
   if bb and (x+bb[0]<0 or y+bb[1]<0 or x+bb[2]>940 or y+bb[3]>1510):raise ValueError('Presenter would be truncated before safety clip: '+s['cut'])
  if a<.999:
   im=im.copy();im.putalpha(im.getchannel('A').point(lambda z:round(z*a)))
  out[o['group']].alpha_composite(im,(x,y))
 for im in out.values():im.paste((0,0,0,0),(940,0,1080,1920))
 return out
def composite(s,t):
 ls=layers(s,t);im=load(s['background']).copy()
 for g in s.get('layer_order',['photos','diagram','labels','presenter']):
  if g in ls:im.alpha_composite(ls[g])
 return im

def svg_scene(s):
 def uri(path):return 'data:image/png;base64,'+base64.b64encode((B/path).read_bytes()).decode()
 dur=s['duration'];parts=[f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1080" height="1920" viewBox="0 0 1080 1920"><title>{s["cut"]} G2 V3 candidate — editable independent layers</title>',f'<g id="background"><image width="1080" height="1920" href="{uri(s["background"])}"/></g>']
 parts.append('<defs><clipPath id="content_safe"><rect width="940" height="1510"/></clipPath></defs>')
 for g in s.get('layer_order',['photos','diagram','labels','presenter']):
  parts.append(f'<g id="{g}" clip-path="url(#content_safe)">')
  for i,o in enumerate(s['items']):
   if o['group']!=g:continue
   ks=[k.copy() for k in o['keys']]
   if ks[-1][0]<dur:ks.append([dur,*ks[-1][1:]])
   attrs=['x','y','width','height','opacity'];a=ks[0][1:]
   parts.append('<image id="'+html.escape(o['id'])+'_'+str(i)+'" href="'+uri(o['asset'])+'" '+ ' '.join(f'{n}="{v}"' for n,v in zip(attrs,a))+' preserveAspectRatio="none">')
   if len(ks)>1:
    for col,att in enumerate(attrs,1):
     vals=[k[col] for k in ks]
     if len(set(vals))==1:continue
     parts.append(f'<animate attributeName="{att}" values="'+ ';'.join(str(v) for v in vals)+'" keyTimes="'+';'.join(str(k[0]/dur) for k in ks)+f'" dur="{dur}s" calcMode="spline" keySplines="'+';'.join('.333333 0 .666667 1' for _ in ks[1:])+'" fill="freeze"/>')
   parts.append('</image>')
  parts.append('</g>')
 parts.append('</svg>');(B/'scenes'/(s['cut']+'.svg')).write_text(''.join(parts))
def encoder(path,alpha=False):
 cmd=['ffmpeg','-v','error','-y','-f','rawvideo','-pixel_format','rgba' if alpha else 'rgb24','-video_size','1080x1920','-framerate','24','-i','pipe:0','-an']
 if alpha:cmd+=['-c:v','qtrle','-pix_fmt','argb','-threads','1']
 else:cmd+=['-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-threads','2','-movflags','+faststart']
 return subprocess.Popen(cmd+[str(path)],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
def render(s,preview_only=False):
 cut=s['cut'];folder=B/cut;folder.mkdir(exist_ok=True);svg_scene(s);sh=(folder/'LAYER_PLAN.json');sh.write_text(json.dumps(s,ensure_ascii=False,indent=2))
 preview=encoder(B/'previews_1080'/(cut+'_G2_V3_silent.mp4'))
 groups=[g for g in s.get('layer_order',['photos','diagram','labels','presenter']) if any(o['group']==g for o in s['items'])]
 procs={} if preview_only else {g:encoder(folder/(g+'_motion_RGBA.mov'),True) for g in groups}
 n=math.ceil(s['duration']*24);bg=load(s['background'])
 # Review anchor is an actual output frame. C04 final hierarchy, C05 distinct old/new change.
 anchors={'C01':.52,'C02':.9,'C03':.72,'C04':.9,'C05':.82,'C06':.85};anchor=round((n-1)*anchors[cut]);samples={0,n//4,n//2,3*n//4,n-1,anchor}
 for k in range(n):
  t=k/24;ls=layers(s,t);im=bg.copy()
  for g in s.get('layer_order',['photos','diagram','labels','presenter']):
   if g in ls:
    im.alpha_composite(ls[g])
    if g in procs:procs[g].stdin.write(ls[g].tobytes())
  preview.stdin.write(im.convert('RGB').tobytes())
  if k in samples:
   q=B/'qc'/cut;q.mkdir(exist_ok=True);im.save(q/f'frame_{k:04d}_1080.png');im.resize((360,640),Image.Resampling.LANCZOS).save(q/f'frame_{k:04d}_360.png')
  if k==anchor:im.save(B/'qc'/(cut+'_1080.png'));im.resize((360,640),Image.Resampling.LANCZOS).save(B/'qc'/(cut+'_360.png'))
 for name,p in [('preview',preview),*procs.items()]:
  p.stdin.close();err=p.stderr.read().decode();ret=p.wait()
  if ret:raise RuntimeError(cut+' '+name+' '+err)
 print('RENDER_DONE',cut,n,flush=True)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--cut');ap.add_argument('--preview-only',action='store_true');args=ap.parse_args()
 for f in sorted((B/'scenes').glob('C*.json')):
  s=json.loads(f.read_text())
  if not args.cut or args.cut==s['cut']:render(s,args.preview_only)
