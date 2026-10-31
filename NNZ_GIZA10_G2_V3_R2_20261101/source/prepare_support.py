from pathlib import Path
from PIL import Image
import json,copy
from build_repair_r2 import diagram,CYAN,static,txt
from render_project import svg_scene,composite
B=Path(__file__).resolve().parents[1]
(B/'assets/masks').mkdir(exist_ok=True)
for folder in ['photos','characters']:
 for p in (B/'assets'/folder).glob('*.png'):
  im=Image.open(p).convert('RGBA')
  if im.getchannel('A').getextrema()!=(255,255):im.getchannel('A').save(B/'assets/masks'/(p.stem+'_alpha.png'))
# Optional alternate source. It is deliberately outside scenes/C*.json so it
# cannot silently replace the adopted real edge comparison during batch render.
s=json.loads((B/'scenes/C06.json').read_text());s=copy.deepcopy(s);s['cut']='C06_M04_FALLBACK';s['adopted']=False
keep=[]
for o in s['items']:
 if o['id'].startswith('edge_'):
  y=680 if o['id']=='edge_old'else 1150;o['keys']=[[0,30,y,360,138,1]];keep.append(o)
 elif o['id'].startswith('whole_'):
  y=680 if o['id']=='whole_old'else 1150;o['keys']=[[0,420,y,180,130 if o['id']=='whole_old'else 126,1]];keep.append(o)
 elif o['id'].startswith('crop_trace_') or o['id'].startswith('memory'):continue
 else:keep.append(o)
for id,y,thumb,box,crop in [('old',870,680,(1080,800,1840,1350),(1135,1090,1785,1340)),('new',1350,1150,(1990,800,2760,1340),(2050,1080,2700,1330))]:
 keep.append(static('M04_'+id,'diagram',f'assets/diagrams/M04_{"reeded"if id=="old"else"smooth"}_large.png',30,y,600,135))
 keep.append(txt('M04_label_'+id,'縁の模式図',390,y-55,38,CYAN))
 scale=180/(box[2]-box[0]);r=[420+(crop[0]-box[0])*scale,thumb+(crop[1]-box[1])*scale,420+(crop[2]-box[0])*scale,thumb+(crop[3]-box[1])*scale]
 a=diagram('M04_trace_'+id,1080,1920,[('rect',r,CYAN,4),('line',[r[0],r[3],370,r[3],370,thumb+145,200,thumb+145,200,y],CYAN,4)])
 keep.append(static('M04_trace_'+id,'diagram',a,0,0,1080,1920))
keep.append(txt('M04_memory','かつて硬貨の最高額 10円',30,1020,34,'#FFD47D',fade=(2,2.25)))
s['items']=keep
(B/'shared/C06_M04_FALLBACK.json').write_text(json.dumps(s,ensure_ascii=False,indent=2));svg_scene(s)
(B/'scenes/C06_M04_FALLBACK.svg').replace(B/'shared/C06_M04_FALLBACK.svg')
composite(s,3.8).resize((360,640),Image.Resampling.LANCZOS).save(B/'candidate_tests/M04_fallback_not_adopted_360.png')
timeline=[];start=0
for i in range(1,7):
 c=f'C{i:02d}';ss=json.loads((B/'scenes'/f'{c}.json').read_text());n=ss['frames'];timeline.append(dict(cut=c,global_start_frame=start,frames=n,local_to_edit_time='identity',layer_groups=['photos','diagram','labels','presenter']));start+=n
(B/'shared/R2_TIMELINE.json').write_text(json.dumps(dict(fps=24,total_frames=start,duration_seconds=start/24,cuts=timeline,note='R2 scenes already use current edit durations; do not reapply the R1 remapping in the supplied reference JSON. Any final retiming must use the same map for all four layers. Audio is unchanged.'),ensure_ascii=False,indent=2))
guide='''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920"><g fill="none" stroke-width="4"><rect x="940" y="0" width="140" height="1920" stroke="#FF6589"/><rect x="0" y="1510" width="1080" height="280" stroke="#FF6589"/><rect x="140" y="1510" width="798" height="240" stroke="#FFD47D"/><rect x="96" y="78" width="834" height="14" stroke="#8DDFEC"/><rect x="116" y="332" width="856" height="248" stroke="#FFD47D"/></g></svg>'''
(B/'shared/SAFE_AREAS_GUIDE_ONLY.svg').write_text(guide)
print('SUPPORT_READY')
