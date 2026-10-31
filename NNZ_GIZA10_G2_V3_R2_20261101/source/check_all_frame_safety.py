from pathlib import Path
from PIL import Image
import json,itertools,numpy as np
from render_project import value,load
B=Path(__file__).resolve().parents[1];rows=[];errors=[];cache={}
banner=Image.open(B/'shared/approved_opening_banner.png').convert('RGBA').resize((920,920),Image.Resampling.LANCZOS)
bm=np.zeros((1920,1080),dtype=bool);bm[88:1008,80:1000]=np.array(banner.getchannel('A'))>32
def shape(o,t):
 x,y,w,h,a=value(o,t);x,y,w,h=map(round,[x,y,w,h])
 if a<.13:return None
 key=(o['asset'],w,h)
 if key not in cache:cache[key]=np.array(load(o['asset']).resize((w,h),Image.Resampling.LANCZOS).getchannel('A'))>32
 return x,y,w,h,cache[key]
def intersect(a,b):
 if a is None or b is None:return 0
 x,y,w,h,m=a;xx,yy,ww,hh,mm=b;l=max(x,xx,0);r=min(x+w,xx+ww,1080);top=max(y,yy,0);bot=min(y+h,yy+hh,1920)
 if l>=r or top>=bot:return 0
 return int((m[top-y:bot-y,l-x:r-x]&mm[top-yy:bot-yy,l-xx:r-xx]).sum())
def maskshape(mask):return (0,0,1080,1920,mask)
caption=np.zeros_like(bm);caption[1510:1790,:]=True
right=np.zeros_like(bm);right[:,940:]=True
progress=np.zeros_like(bm);progress[78:92,96:930]=True
for p in sorted((B/'scenes').glob('C*.json')):
 s=json.loads(p.read_text());bad=[];peak={k:0 for k in ['banner','caption','right_ui','progress','text_text','presenter_text','diagram_text']}
 for f in range(s['frames']):
  shapes={id(o):shape(o,f/24)for o in s['items']}
  for o in s['items']:
   sh=shapes[id(o)]
   for name,mask in [('banner',bm),('caption',caption),('right_ui',right),('progress',progress)]:
    n=intersect(sh,maskshape(mask));peak[name]=max(peak[name],n)
    if n:bad.append(dict(frame=f,kind=name,id=o['id'],pixels=n))
  for a,b in itertools.combinations(s['items'],2):
   groups={a['group'],b['group']}
   kind='text_text'if a['group']==b['group']=='labels'else'presenter_text'if groups=={'presenter','labels'}else'diagram_text'if groups=={'diagram','labels'}else None
   if not kind:continue
   n=intersect(shapes[id(a)],shapes[id(b)]);peak[kind]=max(peak[kind],n)
   if n:bad.append(dict(frame=f,kind=kind,pair=[a['id'],b['id']],pixels=n))
 rows.append(dict(cut=s['cut'],frames=s['frames'],max_overlap_pixels=peak,violations=bad));cache.clear()
 if bad:errors.append(s['cut'])
report=dict(result='FAIL'if errors else'PASS',scope='Every output-frame time, native alpha before clipping; actual approved banner alpha + original R1 caption reservation + UI + progress; text/leader/character collisions',cuts=rows,errors=errors)
(B/'docs/all_frame_safety_qc.json').write_text(json.dumps(report,indent=2));print(json.dumps([{k:v for k,v in r.items()if k!='violations'}for r in rows],indent=2));raise SystemExit(bool(errors))
