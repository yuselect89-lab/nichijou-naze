from pathlib import Path
import subprocess,json
R=Path(__file__).resolve().parents[2];P=R/'preview/full_v3/encoded';P.mkdir(exist_ok=True)
frames={2:[20,95,170],3:[60],4:[0,65,120],5:[0,52,104],6:[0,37,74],7:[0,75,135,194],8:[0,80,164],10:[20,61,122]}
for cut,fs in frames.items():
 for f in fs:
  dest=P/f'cut{cut:02}-{f}.png'
  subprocess.run(['ffmpeg','-v','error','-y','-i',str(R/f'cut{cut:02}/animation.mp4'),'-vf',f'select=eq(n\\,{f})','-frames:v','1',str(dest)],check=True)
import shutil
for p in P.glob('*.png'):shutil.copy2(p,P.parent/p.name)
for cut,f in {2:170,3:60,4:120,5:52,6:37,7:194,8:80,10:61}.items():shutil.copy2(P/f'cut{cut:02}-{f}.png',R/f'cut{cut:02}/main.png')
print('Decoded representative frames:',sum(map(len,frames.values())))
