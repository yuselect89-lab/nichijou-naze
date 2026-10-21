"""Technical finishing of newly redrawn masters, never enlargement of old sprites."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib,shutil,csv
r=Path(__file__).resolve().parents[2]
root=r/'common_assets/nichijou_naze/characters/female_v01'
public=r/'public/common_assets/nichijou_naze/characters/female_v01'
names={'neutral':'b1f39a67-f891-455b-8703-162575d19a59','talk':'3cdf905c-1a2f-423a-b359-97e608209bb0','point_right':'39634aa9-4ea3-411c-b9a7-3724ddd95ad1','point_left':'1611570d-9af2-4003-a528-974951aa4d54','think':'c5192010-d7b3-425a-a9ed-0b2e7f3f55c0'}
records=[]
for sub in ['poses','thumbs','sources/v02_highres']:(root/sub).mkdir(parents=True,exist_ok=True)
for pose,uid in names.items():
    src=Path('/workspace/generated_images')/f'exec-{uid}.png'
    im=Image.open(src).convert('RGBA');native=im.size
    raw=np.array(im);a=raw[:,:,3].astype(float)
    # The generator uses 253/254 alpha for opaque pixels and leaves tiny alpha specks.
    cap=255 if pose=='think' else 253
    raw[:,:,3]=np.clip((a-6)*255/(cap-6),0,255).round().astype('uint8')
    raw[raw[:,:,3]==0,:3]=0
    clean=Image.fromarray(raw)
    bbox=clean.getchannel('A').getbbox();cropped=clean.crop(bbox)
    factor=2160/cropped.height
    sized=cropped.resize((round(cropped.width*factor),2160),Image.Resampling.LANCZOS)
    assert sized.width<=1392
    canvas=Image.new('RGBA',(1536,2304),(0,0,0,0));canvas.alpha_composite(sized,((1536-sized.width)//2,72))
    a=np.array(canvas);a[a[:,:,3]<3]=0;canvas=Image.fromarray(a)
    filename=f'NNZ_CHAR_FEMALE_01_pose_{pose}.png';dest=root/'poses'/filename
    if dest.exists():raise RuntimeError('Refusing to overwrite existing pose: '+str(dest))
    canvas.save(dest,optimize=True)
    thumb=canvas.resize((256,384),Image.Resampling.LANCZOS);thumb.save(root/'thumbs'/f'{pose}_thumb.png',optimize=True)
    shutil.copy2(src,root/'sources/v02_highres'/f'{pose}_generated.png')
    rec={'pose':pose,'filename':'poses/'+filename,'width':1536,'height':2304,'alpha_content_bbox':canvas.getchannel('A').getbbox(),'generated_source_resolution':native,'generated_content_crop':bbox,'technical_scale_factor':factor,'source':'sources/v02_highres/'+pose+'_generated.png','sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'direction':'screen right' if pose=='point_right' else 'screen left' if pose=='point_left' else 'front / slight three-quarter'}
    records.append(rec)
    for sub,fn in [('poses',filename),('thumbs',f'{pose}_thumb.png')]:
        (public/sub).mkdir(parents=True,exist_ok=True);target=public/sub/fn
        if target.exists():raise RuntimeError('Refusing to overwrite runtime asset')
        shutil.copy2(root/sub/fn,target)
manifest={'asset_id':'NNZ_CHAR_FEMALE_01','name':'日常のなぜ？ 女性解説キャラクター 本番用5ポーズ','version':'v02_highres','date':'2026-10-22','style':'既存デザインに合わせたデフォルメ・アニメ線画、柔らかな陰影','character_description':'茶系お団子ヘア、茶色の大きな目、クリーム系パーカー、紺系パンツ、グレー／クリームのスニーカー。約3頭身。','available_poses':list(names),'source_reference':{'design_authority':'vendor/common-library/1.0.0/common_assets/nichijou_naze/characters/female_v01/preview.jpg','legacy_sprites':'vendor/common-library/1.0.0/common_assets/nichijou_naze/characters/female_v01/poses/','method':'Reference-conditioned high-detail redraws; all poses anchored to the same neutral redraw.','reference_issue':'Original point_left sprite points screen-right; v02 corrects its direction without renaming other assets.'},'resolution':{'canvas':[1536,2304],'target_content_height':2160,'native_generation_note':'Generated source pixels are recorded per pose (mostly 1024x1536). Delivery size is normalized from new detailed redraws, not native 2304px generation and not an enlargement of 253px sprites.'},'background_transparency':'RGBA true alpha, no matte or floor. Alpha specks removed; nearly opaque interiors normalized.','processing':['Inspect generated pose identity, hands and silhouette','Clean alpha <=6 and normalize opaque interiors','Crop transparent border, align full-body height 2160px','Lanczos resample of new generated redraws and centered placement on 1536x2304 canvas','Retain raw generated masters and prototype files'],'usage_notes':['Use version v02_highres explicitly to preserve old episode rendering.','point_right/point_left refer to viewer/screen direction.','Static talk pose is not lip-sync or mouth animation.','For large placement use <=1200px full-body display height as validated; avoid enlarging beyond delivered pixels.','All previous short-name prototype files remain unchanged.'],'poses':records,'qc_status':'Visual review complete; see validation/highres for actual 1080x1920 render evidence.','limitations':['Small stylistic pose differences remain in expression and viewing angle, not a rigged identical-face model.','Native generation resolution is lower than delivery resolution for these newly redrawn masters.','Mouth shape layers and lip-sync are not included.']}
(root/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
shutil.copy2(root/'manifest.json',public/'manifest.json')
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',25)
sheet=Image.new('RGB',(1600,620),'#edf1ef')
for i,pose in enumerate(names):
    im=Image.open(root/'poses'/f'NNZ_CHAR_FEMALE_01_pose_{pose}.png');im.thumbnail((300,500))
    x=i*320+(320-im.width)//2;sheet.paste(im,(x,40),im)
    ImageDraw.Draw(sheet).text((i*320+22,560),pose,font=font,fill='#1d3440')
sheet.save(root/'preview_v02_highres.jpg',quality=95)
registry=json.loads((r/'library-registry.json').read_text())
registry.setdefault('legacyCharacter',registry['character'])
registry['activeCharacterVersion']='v02_highres'
registry['character']={'id':'NNZ_CHAR_FEMALE_01','revision':'v02_highres','status':'render_verification_pending','manifest':'common_assets/nichijou_naze/characters/female_v01/manifest.json','poses':[{'pose':x['pose'],'path':'common_assets/nichijou_naze/characters/female_v01/'+x['filename'],'width':1536,'height':2304,'sha256':x['sha256']} for x in records]}
(r/'library-registry.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2))
management=r/'common_assets/nichijou_naze/management';management.mkdir(parents=True,exist_ok=True)
rows=json.loads((r/'vendor/common-library/1.0.0/common_assets/nichijou_naze/management/asset_registry.json').read_text())
rows.append({'Asset ID':'NNZ_CHAR_FEMALE_01','種別':'キャラ','名前・用途':'女性解説キャラ 本番用高解像度5ポーズ','ステータス':'render_verification_pending','Version':'v02_highres','相対パス':'characters/female_v01/manifest.json','使用回':'共通素材','権利・制作元':'既存資料を参照してAI描き起こし＋透過・余白・サイズ整形','QC':'1080x1920実レンダー待ち','備考':'1536x2304 RGBA / 5 poses / native generation sizes in manifest'})
(management/'asset_registry.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
with (management/'asset_registry.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
try:
    from openpyxl import Workbook
    wb=Workbook();ws=wb.active;ws.title='Assets';ws.append(list(rows[0]));[ws.append([row[k] for k in rows[0]]) for row in rows];wb.save(management/'asset_registry.xlsx')
except ImportError:pass
print(json.dumps({'poses':len(records),'resolution':[1536,2304],'canonical':str(root)},indent=2))
