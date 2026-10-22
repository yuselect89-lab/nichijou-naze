"""Run after render.mjs. Derive review media from the actual native-resolution render."""
from pathlib import Path
import subprocess, json, hashlib
from PIL import Image, ImageDraw
EP=Path(__file__).resolve().parents[2]
PRE=EP/'preview/v1'; ASSET=EP/'assets/v1'; EVID=EP/'evidence/v1'
full=PRE/'EP006-material-preview-1080.mp4'
def run(args):
    r=subprocess.run(args,capture_output=True,text=True)
    if r.returncode: raise RuntimeError(f'{args}: {r.stderr}')
    return r.stdout
def encode(source,dest,filters):
    if dest.exists(): raise RuntimeError(f'Refusing overwrite: {dest}')
    run(['ffmpeg','-nostdin','-v','error','-i',str(source),'-vf',filters,'-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p',str(dest)])
encode(full,PRE/'CUT04-06-continuous-1080.mp4','trim=start_frame=420:end_frame=870,setpts=PTS-STARTPTS')
encode(full,PRE/'EP006-material-preview-360.mp4','scale=360:640')
encode(PRE/'CUT04-06-continuous-1080.mp4',PRE/'CUT04-06-continuous-360.mp4','scale=360:640')
cuts=[('CUT01',0,180),('CUT02',180,300),('CUT03',300,420),('CUT04',420,570),('CUT05',570,690),('CUT06',690,870),('CUT07',870,1050)]
for cut,a,b in cuts: encode(full,ASSET/f'{cut}-review-1080.mp4',f'trim=start_frame={a}:end_frame={b},setpts=PTS-STARTPTS')
# Every video must decode completely and report the expected frame count. These are silent review files.
reports=[]
for video in [*PRE.glob('*.mp4'),*ASSET.glob('*.mp4')]:
    report=json.loads(run(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(video)]))
    streams=report['streams']; assert len(streams)==1 and streams[0]['codec_type']=='video',video
    v=streams[0]; expected=450 if 'continuous' in video.name else 1050 if 'material-preview' in video.name else next(b-a for c,a,b in cuts if c in video.name)
    assert int(v['nb_read_frames'])==expected and v['r_frame_rate']=='30/1',video
    assert int(v['width'])==(360 if '360' in video.name else 1080) and int(v['height'])==(640 if '360' in video.name else 1920),video
    run(['ffmpeg','-nostdin','-v','error','-i',str(video),'-f','null','-'])
    reports.append({'file':str(video.relative_to(EP)),'frames':expected,'width':v['width'],'height':v['height'],'fps':'30/1','audio_streams':0,'full_decode':'PASS'})
(EVID/'media-qc.json').write_text(json.dumps(reports,ensure_ascii=False,indent=2))
# Contact sheets are QC indexes only, never episode footage or comparison scenes.
sheet=Image.new('RGB',(1440,1340),'#dfe9e6'); d=ImageDraw.Draw(sheet)
for n in range(1,8):
    im=Image.open(PRE/f'CUT{n:02}-1080.png').convert('RGB').resize((360,640),Image.Resampling.LANCZOS)
    im.save(PRE/f'CUT{n:02}-360.png');x=((n-1)%4)*360;y=((n-1)//4)*670
    sheet.paste(im,(x,y+30));d.text((x+15,y+8),f'CUT{n:02} / provisional - silent',fill='#213c42')
sheet.save(PRE/'contact-sheet-7cuts.jpg',quality=95)
stages=['01-start','02-vasoconstriction','03-volume','04-folds-hold']
sheet=Image.new('RGB',(1440,675),'#dfe9e6');d=ImageDraw.Draw(sheet)
for n,name in enumerate(stages):
    im=Image.open(PRE/f'science-{name}.png').convert('RGB').resize((360,640),Image.Resampling.LANCZOS)
    im.save(PRE/f'science-{name}-360.png');sheet.paste(im,(n*360,35));d.text((n*360+15,10),name,fill='#213c42')
sheet.save(PRE/'science-four-stage-QC-index.jpg',quality=95)
# Verify transparent exports really have alpha and no opaque full-frame background.
alpha=[]
for imfile in ASSET.glob('*.png'):
    if imfile.name.startswith('character-'):continue
    im=Image.open(imfile);assert im.mode=='RGBA',imfile;ext=im.getchannel('A').getextrema();assert ext[0]==0 and ext[1]>=250,imfile
    alpha.append({'file':str(imfile.relative_to(EP)),'alpha_range':ext,'bbox':im.getbbox()})
(EVID/'alpha-qc.json').write_text(json.dumps(alpha,indent=2))
# Actual decoded CUT boundaries must retain the same image of the model.
boundary=[]
for a,b in [(149,150),(269,270)]:
    images=[]
    for f in [a,b]:
        dest=PRE/f'decoded-science-{f}.png'
        run(['ffmpeg','-nostdin','-v','error','-i',str(PRE/'CUT04-06-continuous-1080.mp4'),'-vf',f'select=eq(n\\,{f})','-frames:v','1',str(dest)])
        images.append(Image.open(dest).convert('RGB').crop((175,850,860,1280)))
    from PIL import ImageChops,ImageStat
    diff=ImageStat.Stat(ImageChops.difference(*images));mean=sum(diff.mean)/3
    assert mean<1.5,(a,b,mean)
    boundary.append({'frames':[a,b],'model_roi_mean_absolute_error':mean,'status':'PASS','note':'Compression tolerance; no camera/subject reset'})
(EVID/'boundary-qc.json').write_text(json.dumps(boundary,indent=2))
print(f'Media PASS: {len(reports)} videos; {len(alpha)} alpha exports; two decoded cut boundaries')
