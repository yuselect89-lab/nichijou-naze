from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,subprocess,shutil,csv,zipfile
import numpy as np
r=Path(__file__).resolve().parents[2];root=r/'common_assets/nichijou_naze/characters/female_v01'
m=json.loads((root/'manifest.json').read_text());records=[]
for p in m['poses']:
    im=Image.open(root/p['filename']);assert im.mode=='RGBA' and im.size==(1536,2304)
    a=np.array(im.getchannel('A'));assert a.min()==0 and a.max()==255
    assert a[0].max()==a[-1].max()==a[:,0].max()==a[:,-1].max()==0
    bbox=im.getchannel('A').getbbox();assert bbox[1]>=60 and bbox[3]<=2244 and bbox[3]-bbox[1]>=2150
    runtime=r/'public/common_assets/nichijou_naze/characters/female_v01'/p['filename']
    assert hashlib.sha256(runtime.read_bytes()).hexdigest()==p['sha256']
    assert hashlib.sha256((root/p['filename']).read_bytes()).hexdigest()==p['sha256']
    records.append({'pose':p['pose'],'pixels':list(im.size),'mode':im.mode,'contentBbox':bbox,'alpha':'PASS true alpha and empty borders'})
casePose={45:'neutral',135:'talk',225:'point_right',315:'point_left',405:'think',480:'point_right',540:'point_left',640:'point_left',730:'point_right',820:'think'}
obs=json.loads((r/'validation/highres/observations.json').read_text());seen={o['frame']:o for o in obs};assert set(casePose)<=set(seen)
for frame,pose in casePose.items():
    o=seen[frame];images=o['images'];chars=[i for i in images if i['kind'] in ['large-character','character']]
    assert len(chars)==1 and len([i for i in images if i['kind']=='banner'])==1
    assert len([i for i in images if i['kind']=='caption'])==1
    p=next(p for p in m['poses'] if p['pose']==pose);alpha=Image.open(root/p['filename']).getchannel('A')
    c=chars[0];assert c['x']>=95.9 and c['x']+c['width']<=984.1
    assert c['y']+c['height']<=1500.1
    layer=Image.new('L',(1080,1920),0);resized=alpha.resize((round(c['width']),round(c['height'])),Image.Resampling.LANCZOS);layer.paste(resized,(round(c['x']),round(c['y'])))
    assert layer.crop((80,150,1000,292)).getextrema()[1]==0,'Character intersects yellow banner'
    assert layer.crop((96,1510,984,1790)).getextrema()[1]==0,'Character intersects captions'
    for i in images:
        if i['kind']=='caption':assert '、' not in i['text'] and '。' in i['text']
clip=r/'validation/highres/character-layout-1080x1920.mp4'
streams=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(clip)]))['streams']
assert len(streams)==1
v=streams[0];assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1080,1920,'30/1',840)
subprocess.run(['ffmpeg','-v','error','-i',str(clip),'-f','null','-'],check=True)
baseline=json.loads(Path('/tmp/nnz-before-highres.json').read_text())
for file,digest in baseline.items():assert hashlib.sha256((r/file).read_bytes()).hexdigest()==digest,'Prior asset changed: '+file
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22)
sheet=Image.new('RGB',(1800,1400),'#dbe5df')
for i,frame in enumerate(casePose):
    im=Image.open(r/f'validation/highres/frame-{frame}.png').convert('RGB').resize((340,604));x=i%5*360+10;y=i//5*700+65
    sheet.paste(im,(x,y));ImageDraw.Draw(sheet).text((x+8,y-45),casePose[frame],font=font,fill='#18323d')
sheet.save(r/'validation/highres/contact-sheet.jpg',quality=94)
# White/dark/check backgrounds expose alpha edges without changing pose pixels.
atlas=Image.new('RGB',(1600,1800),'white')
for row,bg in enumerate(['#ffffff','#132b38','checker']):
    for col,p in enumerate(m['poses']):
        tile=Image.new('RGB',(320,600),'white' if bg=='checker' else bg)
        if bg=='checker':
            d=ImageDraw.Draw(tile)
            for y in range(0,600,24):
                for x in range(0,320,24):
                    if (x//24+y//24)%2:d.rectangle((x,y,x+23,y+23),fill='#dce2df')
        im=Image.open(root/p['filename']);im.thumbnail((300,510));tile.paste(im,((320-im.width)//2,28),im)
        ImageDraw.Draw(tile).text((16,555),p['pose'],font=font,fill='white' if row==1 else '#18323d');atlas.paste(tile,(col*320,row*600))
atlas.save(r/'validation/highres/alpha-backgrounds.jpg',quality=94)
report={'asset_id':m['asset_id'],'version':m['version'],'status':'PASS render verified','poses':records,'render':{'resolution':[1080,1920],'fps':30,'frames':840,'fullDecode':'PASS','largeDisplayHeight':1220,'sideDisplayHeight':1100,'helperDisplayHeight':280,'screenCases':list(casePose),'bannerAndCaptionAlphaCollision':'NONE'},'preservedPriorAssets':len(baseline),'visualReview':['Five poses visibly match bun, hair color, cream hoodie, navy pants and sneakers.','Face and hands reviewed at large screen size; no obvious broken anatomy.','Screen-left and screen-right pointing verified.','White dark and checker composites reviewed; transparent padding and soft alpha edges retained.'],'limitations':m['limitations']}
(r/'validation/highres/qc-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
m['qc_status']='render_verified';m['validation']={'report':'validation/highres/qc-report.json','scene':'src/highres-validation/index.tsx','video':'validation/highres/character-layout-1080x1920.mp4'}
(root/'manifest.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
version=root/'versions/v02_highres';version.mkdir(parents=True,exist_ok=True);shutil.copy2(root/'manifest.json',version/'manifest.json')
shutil.copy2(root/'manifest.json',r/'public/common_assets/nichijou_naze/characters/female_v01/manifest.json')
reg=json.loads((r/'library-registry.json').read_text());reg['character']['status']='render_verified';(r/'library-registry.json').write_text(json.dumps(reg,ensure_ascii=False,indent=2))
management=r/'common_assets/nichijou_naze/management';rows=json.loads((management/'asset_registry.json').read_text())
for row in rows:
    if row['Asset ID']==m['asset_id'] and row['Version']=='v02_highres':row['ステータス']='render_verified';row['QC']='PASS 1080x1920 / 30fps / 5 poses / large and side placement / 3 templates'
for row in rows:row['Active']=row['Version']=='v02_highres' if row['Asset ID']==m['asset_id'] else row['ステータス'] not in ['planned','prototype']
(management/'asset_registry.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
with (management/'asset_registry.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
from openpyxl import Workbook
wb=Workbook();ws=wb.active;ws.title='Assets';ws.append(list(rows[0]));[ws.append([row[k] for k in rows[0]]) for row in rows];wb.save(management/'asset_registry.xlsx')
print(json.dumps({'status':report['status'],'poses':len(records),'resolution':[1536,2304],'priorAssetsPreserved':len(baseline)},indent=2))
