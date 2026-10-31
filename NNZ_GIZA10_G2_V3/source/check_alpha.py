from pathlib import Path
import subprocess,json,numpy as np
B=Path(__file__).resolve().parents[1];out=[]
for p in sorted(B.glob('C*/*_RGBA.mov')):
 cut=p.parent.name;s=json.loads((B/'scenes'/(cut+'.json')).read_text());t=.9 if cut=='C04' and 'presenter'in p.name else s['duration']*.8
 r=subprocess.run(['ffmpeg','-v','error','-ss',str(t),'-i',str(p),'-vf','alphaextract','-frames:v','1','-pix_fmt','gray','-f','rawvideo','-'],capture_output=True,check=True)
 a=np.frombuffer(r.stdout,dtype=np.uint8).reshape(1920,1080);assert a.min()==0 and a.max()>0;assert (a[:,940:]==0).all()
 out.append({'file':str(p.relative_to(B)),'sample_s':t,'alpha_min':int(a.min()),'alpha_max':int(a.max()),'transparent_background':True,'right_ui_transparent':True})
(B/'docs/alpha_qc.json').write_text(json.dumps(out,indent=2));print('ALPHA_VERIFIED',len(out))
