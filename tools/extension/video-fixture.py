"""Create a small original video background and its render test config."""
from pathlib import Path
import subprocess,json,shutil
R=Path(__file__).resolve().parents[2];D=R/'common_assets/nichijou_naze/layouts/v1.1.0/test_media'
subprocess.run(['ffmpeg','-v','error','-y','-i',str(D/'kitchen-ice-dummy.svg'),'-frames:v','1','/tmp/nnz-kitchen-test.png'],check=True)
dest=D/'kitchen-pan-dummy.mp4'
subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-i','/tmp/nnz-kitchen-test.png','-vf',"zoompan=z='1+0.0003*on':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=120:s=1080x1920:fps=30",'-frames:v','120','-c:v','libx264','-preset','fast','-crf','23','-pix_fmt','yuv420p','-threads','2',str(dest)],check=True)
public=R/'public'/dest.relative_to(R);shutil.copy2(dest,public)
config={'id':'video-background','revision':'1.1.0','layout':'NNZ_LAYOUT_FOOTAGE_01','durationFrames':120,'background':{'src':str(dest.relative_to(R)),'kind':'video'},'character':{'side':'right','top':1100,'height':360,'poses':[{'fromFrame':0,'pose':'happy'}],'entry':'fade','nodAt':[40]}}
(R/'common_assets/nichijou_naze/layouts/v1.1.0/examples/video-background.json').write_text(json.dumps(config,ensure_ascii=False,indent=2))
print('Created original4second dummy video background')
