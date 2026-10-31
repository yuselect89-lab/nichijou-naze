from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import subprocess,json,argparse
B=Path(__file__).resolve().parents[1];O=B/'qc/MAJOR_R1';O.mkdir(exist_ok=True)
ap=argparse.ArgumentParser();ap.add_argument('--legacy',type=Path);args=ap.parse_args();legacy=args.legacy or B.parent/'NNZ_GIZA10_G2_V3_R0'
rows=[]
for c,times in {'C01':[3.30,3.8,4.125],'C03':[3.78,4.4,5.0],'C04':[.45,.8,1.05],'C06':[2.74,3.8,4.5]}.items():
 folder=O/c;folder.mkdir(exist_ok=True)
 for label,t in zip(['entry','full_gesture','ending'],times):
  f=folder/(label+'_1080.png');subprocess.run(['ffmpeg','-v','error','-y','-ss',str(t),'-i',str(B/'previews_1080'/(c+'_G2_V3_silent.mp4')),'-frames:v','1','-threads','1',str(f)],check=True)
  with Image.open(f)as im:im.resize((360,640),Image.Resampling.LANCZOS).save(folder/(label+'_360.png'))
 if (legacy/'previews_1080'/(c+'_G2_V3_silent.mp4')).exists():
  f=folder/'R0_before_1080.png';subprocess.run(['ffmpeg','-v','error','-y','-ss',str(times[1]),'-i',str(legacy/'previews_1080'/(c+'_G2_V3_silent.mp4')),'-frames:v','1','-threads','1',str(f)],check=True)
  with Image.open(f)as im:im.resize((360,640),Image.Resampling.LANCZOS).save(folder/'R0_before_360.png')
  pair=Image.new('RGB',(720,680),(20,27,35));pair.paste(Image.open(folder/'R0_before_360.png').convert('RGB'),(0,40));pair.paste(Image.open(folder/'full_gesture_360.png').convert('RGB'),(360,40));d=ImageDraw.Draw(pair);font=ImageFont.truetype(str(B/'assets/fonts/NotoSansCJK-Regular.ttc'),20,index=0);d.text((10,6),'R0 / MAJOR',font=font,fill='white');d.text((370,6),'R1 / 修正候補',font=font,fill='white');pair.save(O/(c+'_before_after_360.png'))
 rows.append({'cut':c,'encoded_source':f'previews_1080/{c}_G2_V3_silent.mp4','sample_times_seconds':dict(zip(['entry','full_gesture','ending'],times))})
(B/'docs/MAJOR_R1_EVIDENCE_INDEX.json').write_text(json.dumps(rows,indent=2));print('R1_EVIDENCE_EXTRACTED')
