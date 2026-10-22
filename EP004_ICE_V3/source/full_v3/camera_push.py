"""Orthographic-style finishing push on the 3D base only; labels remain in safe zones."""
from pathlib import Path
import subprocess,json,shutil
R=Path(__file__).resolve().parents[2]
d=Path(__import__('sys').argv[1]) if len(__import__('sys').argv)>1 else R/'cut07'
raw=d/'base_render.mp4';out=d/'base_animation.mp4'
if not raw.exists():shutil.move(out,raw)
t='min(1,max(0,(on-95)/99))';z=f'1+0.8*({t})*({t})*(3-2*({t}))'
f=f"zoompan=z='{z}':x='500-500/zoom':y='790-790/zoom':d=1:s=1080x1920:fps=30"
subprocess.run(['ffmpeg','-v','error','-y','-i',str(raw),'-vf',f,'-frames:v','195','-an','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-preset','medium',str(out)],check=True)
(d/'camera_motion.json').write_text(json.dumps({'source':'base_render.mp4','output':'base_animation.mp4','kind':'continuous orthographic-style finishing push on rendered 3D base','from_frame':95,'to_frame':194,'zoom_from':1,'zoom_to':1.8,'anchor_px':[500,790],'ease':'smoothstep','labels_affected':False,'resolution':[1080,1920],'fps':30},indent=2)+'\n')
