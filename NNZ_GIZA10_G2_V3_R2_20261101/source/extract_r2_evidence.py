from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,subprocess
B=Path(__file__).resolve().parents[1];out=B/'qc/ENCODED_R2';out.mkdir(exist_ok=True)
times={'C01':[0,1,2.6,3.2,3.8,4.1],'C02':[0,1.1,2.2,3.3,4.65],'C03':[0,1.2,2.7,3.4,3.7,4.2,5.48],'C04':[0,.4,.65,.85,1.05,1.45,1.75,2.15,5.0],'C05':[0,1.2,2.4,2.65,2.95,3.2,3.5,6.25],'C06':[0,1,2.1,2.65,3,4.5]}
index=[]
for c,ts in times.items():
 rows=[];strip=Image.new('RGB',(len(ts)*360,665),'#152133')
 for i,t in enumerate(ts):
  frame=round(t*24)
  for size in [1080,360]:
   src=B/f'previews_{size}'/f'{c}_G2_V3_silent.mp4';dest=out/f'{c}_f{frame:03d}_{size}.png'
   subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-vf',f'select=eq(n\\,{frame})','-frames:v','1','-threads','1',str(dest)],check=True)
   rows.append(dict(cut=c,frame=frame,local_seconds=frame/24,size=size,source=str(src.relative_to(B)),image=str(dest.relative_to(B))))
  strip.paste(Image.open(out/f'{c}_f{frame:03d}_360.png'),(i*360,25));ImageDraw.Draw(strip).text((i*360+8,5),f'{c} frame {frame} / {frame/24:.3f}s',fill='white')
 strip.save(out/f'{c}_TIMELINE_360.png');index.extend(rows)
 # Representative is encoded video, not an SVG/Pillow-only composition.
 chosen={'C01':3.8,'C02':2.2,'C03':4.2,'C04':2.15,'C05':1.2,'C06':3.0}[c];f=round(chosen*24)
 for size in [1080,360]:
  with Image.open(out/f'{c}_f{f:03d}_{size}.png')as im:im.save(B/'stills_for_qc'/f'{c}_{size}.png')
(B/'docs/ENCODED_EVIDENCE_INDEX.json').write_text(json.dumps(index,indent=2));print('EXTRACTED_ACTUAL_VIDEO_FRAMES',len(index))
