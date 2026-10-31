from pathlib import Path
from PIL import Image
import math,json
B=Path('/workspace/work/NNZ_GIZA10_WORK_ASSETS')
for cut,role in [('C01','question'),('C03','reaction'),('C04','process'),('C06','payoff')]:
 src=Image.open(B/f'shared/characters/{role}_upperbody.png').convert('RGBA');src.thumbnail((600,760),Image.Resampling.LANCZOS)
 out=B/cut/'presenter_entrance_sequence';out.mkdir(exist_ok=True)
 for f in range(36):
  t=min(f/15,1);s=t*t*(3-2*t)
  tile=src.copy();tile.putalpha(tile.getchannel('A').point(lambda a:round(a*s)))
  im=Image.new('RGBA',(640,820));im.alpha_composite(tile,((640-src.width)//2,round(40+(1-s)*40)));im.save(out/f'{f+1:04d}.png')
 (B/cut/'presenter_motion.json').write_text(json.dumps({'sequence':'presenter_entrance_sequence/%04d.png','start':1,'frames':36,'fps':24,'duration_editorial_seconds':1.5,'alpha':'straight RGBA','role':role,'motion':'short slide and ease-in alpha, then hold; no lip-sync','placement':'Work places sprite after coin reveal; do not cover rims, labels or subtitle area','audio':'not accessed'},indent=2))
print('CHARACTER_SEQUENCES_DONE')
