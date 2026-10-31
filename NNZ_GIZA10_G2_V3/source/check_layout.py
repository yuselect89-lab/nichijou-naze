from pathlib import Path
import json,numpy as np
from render_project import layers
B=Path(__file__).resolve().parents[1];rows=[]
for p in sorted((B/'scenes').glob('C*.json')):
 s=json.loads(p.read_text());over=0;caption=0;right=0;times=[]
 for t in np.linspace(0,s['duration'],25):
  ls=layers(s,float(t));a={g:np.array(im.getchannel('A'))for g,im in ls.items()}
  if 'presenter'in a:
   count=int(((a['presenter']>32)&(a['photos']>32)).sum());over=max(over,count)
   if count:times.append(round(float(t),3))
  for aa in a.values():caption=max(caption,int((aa[1510:1790]>32).sum()));right=max(right,int((aa[:,940:]>32).sum()))
 rows.append({'cut':s['cut'],'sampled_frames':25,'max_presenter_photo_overlap_pixels':over,'overlap_times_s':times,'max_content_pixels_in_caption_reservation':caption,'max_content_pixels_in_right_ui_reservation':right})
(B/'docs/layout_qc.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
