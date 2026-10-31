from pathlib import Path
from PIL import Image
import json,numpy as np,math,itertools
from render_project import value
B=Path(__file__).resolve().parents[1];cache={};rows=[]
def shape(o,t):
 x,y,w,h,a=value(o,t);x,y,w,h=map(round,[x,y,w,h])
 if a<.13 or w<1 or h<1:return None
 key=(o['asset'],w,h)
 if key not in cache:
  im=Image.open(B/o['asset']).convert('RGBA').resize((w,h),Image.Resampling.LANCZOS);cache[key]=np.array(im.getchannel('A'))>32
 return x,y,w,h,cache[key]
def intersection(a,b):
 if a is None or b is None:return 0
 x,y,w,h,m=a;xx,yy,ww,hh,mm=b
 l=max(x,xx,0);r=min(x+w,xx+ww,940);top=max(y,yy,0);bot=min(y+h,yy+hh,1510)
 if l>=r or top>=bot:return 0
 return int((m[top-y:bot-y,l-x:r-x]&mm[top-yy:bot-yy,l-xx:r-xx]).sum())
for p in sorted((B/'scenes').glob('C*.json')):
 s=json.loads(p.read_text());objs=[o for o in s['items'] if o['group']in['photos','presenter','labels']];bad=[];peak=0;n=math.ceil(s['duration']*24)
 for k in range(n):
  sh={id(o):shape(o,k/24) for o in objs}
  for a,b in itertools.combinations(objs,2):
   if a['group']!='photos' and b['group']!='photos':continue
   count=intersection(sh[id(a)],sh[id(b)]);peak=max(peak,count)
   if count:bad.append({'frame':k,'pair':[a['group']+'/'+a['id'],b['group']+'/'+b['id']],'pixels':count})
 rows.append({'cut':s['cut'],'frames_checked':n,'photo_photo_presenter_and_label_max_overlap_pixels':peak,'overlaps':bad})
 cache.clear()
(B/'docs/photo_collision_qc.json').write_text(json.dumps(rows,indent=2));print(json.dumps([{k:v for k,v in r.items() if k!='overlaps'}for r in rows],indent=2));raise SystemExit(any(r['overlaps']for r in rows))
