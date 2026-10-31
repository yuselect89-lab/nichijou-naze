from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math,json,shutil,hashlib
B=Path('/workspace/work/NNZ_GIZA10_WORK_ASSETS');R=Path('/workspace/nichijou-naze')
W,H=1080,1920
S=B/'shared';(S/'backgrounds').mkdir(parents=True,exist_ok=True);(S/'characters').mkdir(exist_ok=True);(S/'fonts').mkdir(exist_ok=True)
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc';regular='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
shutil.copy2('/usr/share/doc/fonts-noto-cjk/copyright',S/'fonts/Noto_CJK_LICENSE.txt')
shutil.copy2(font,S/'fonts/NotoSansCJK-Bold.ttc');shutil.copy2(regular,S/'fonts/NotoSansCJK-Regular.ttc')
# Original procedural exhibition background; no objects/text/brand overlays.
im=Image.new('RGB',(W,H));px=im.load()
for y in range(H):
 for x in range(W):
  g=math.exp(-(((x-490)/670)**2+((y-820)/850)**2)*1.5)
  px[x,y]=(int(10+12*g),int(17+19*g),int(28+26*g))
im.save(S/'backgrounds/exhibition_clean_1080x1920.png')
# Four unchanged registered originals plus reversible upper-body crops.
pre=json.loads((B/'docs/library_preflight.json').read_text());chars={}
for d in pre['decisions']:
 role=d['key'];src=R/d['selected_file'];target=S/'characters'/f'{role}_original.png';shutil.copy2(src,target)
 img=Image.open(src).convert('RGBA');bbox=img.getbbox();crop=(max(0,bbox[0]-24),48,min(img.width,bbox[2]+24),1250)
 img.crop(crop).save(S/'characters'/f'{role}_upperbody.png')
 chars[role]={'id':'NNZ_CHAR_FEMALE_01','version':'v03_expressions','source':str(src.relative_to(R)),'original_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'crop_bbox':crop,'original':f'shared/characters/{role}_original.png','crop':f'shared/characters/{role}_upperbody.png','license':'User existing registered character; provenance preserved; no new public license asserted'}
(S/'characters/provenance.json').write_text(json.dumps(chars,ensure_ascii=False,indent=2))
labels={
 1:[('question','ギザギザ？',80,True)],
 2:[('concept','最高額の硬貨',72,True)],
 3:[('year','1951年',48,False),('discovery','硬貨の最高額＝10円',68,True)],
 4:[('fifty','50円',80,True),('fifty_year','1955',42,False),('hundred','100円',80,True),('hundred_year','1957',42,False)],
 5:[('year','1959年',72,True),('smooth','ギザなし',54,False)],
 6:[('reeded','ギザあり',64,True),('smooth','ギザなし',64,True)]}
roles=['question',None,'reaction','process',None,'payoff']
scripts=['昔の10円玉。なぜフチがギザギザ？','当時は最高額の硬貨にギザを付ける慣習がありました。','1951年に製造が始まった10円玉が、なんと最高額！','ところが50円、100円も登場。どちらもギザ付き。','見分けにくくなったことなどから、1959年に10円のギザは廃止されました。','あのギザは、10円玉が硬貨の頂点だった時代の名残なんです。']
for i in range(1,7):
 c=B/f'C{i:02d}';(c/'labels').mkdir(exist_ok=True)
 for name,txt,size,bold in labels[i]:
  f=ImageFont.truetype(font if bold else regular,size,index=0)
  box=f.getbbox(txt);ww=box[2]-box[0]+48;hh=box[3]-box[1]+40
  layer=Image.new('RGBA',(ww,hh));dr=ImageDraw.Draw(layer);dr.text((24-box[0],20-box[1]),txt,font=f,fill=(245,241,230,255) if bold else (172,191,207,255));layer.save(c/'labels'/f'{name}.png')
  svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{ww}" height="{hh}" viewBox="0 0 {ww} {hh}"><text x="24" y="{hh-22}" fill="{("#f5f1e6" if bold else "#acbfcf")}" font-family="Noto Sans CJK JP" font-weight="{700 if bold else 400}" font-size="{size}">{txt}</text></svg>'
  (c/'labels'/f'{name}.svg').write_text(svg)
 # Editable layer instructions, normalized motion anchors rather than invented VO times.
 plan={'cut':f'C{i:02d}','script_locked':scripts[i-1],'canvas':[1080,1920],'background':'shared/backgrounds/exhibition_clean_1080x1920.png','labels':[{'png':f'C{i:02d}/labels/{name}.png','svg':f'C{i:02d}/labels/{name}.svg','text':txt} for name,txt,_,_ in labels[i]],'presenter':chars[roles[i-1]]['crop'] if roles[i-1] else None,'presenter_role':roles[i-1] or 'focus_only','timing':'Unsynced editorial handles. Work aligns to existing locked audio. Audio was not accessed.','status':'PARTIAL - photography and historically verified coin faces missing','no_baked_caption_banner_progress_or_cta':True}
 (c/'layer_plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2))
# A real isolated animated guide, not a coin or a finished cut. Work repositions to actual photographed edge.
g=B/'C01/guide_sequence';g.mkdir(exist_ok=True)
for k in range(48):
 t=k/47;s=t*t*(3-2*t);im=Image.new('RGBA',(720,160));d=ImageDraw.Draw(im)
 x=90+540*s
 d.line([(70,105),(650,105)],fill=(226,187,113,110),width=3)
 d.ellipse((x-18,87,x+18,123),outline=(255,219,149,255),width=5)
 d.line([(x,36),(x,79)],fill=(255,219,149,255),width=5)
 d.polygon([(x,85),(x-9,71),(x+9,71)],fill=(255,219,149,255))
 im.save(g/f'{k+1:04d}.png')
# Independent comparison-board dividers, no fake coin art.
board=Image.new('RGBA',(1080,1920));d=ImageDraw.Draw(board)
for y in [680,1120]:
 d.line([(115,y+155),(885,y+155)],fill=(124,155,173,100),width=2)
board.save(B/'C06/comparison_dividers.png')
# Composition guide only. An unfilled photo slot is transparent, not a fake photograph.
for i in range(1,7):
 preview=Image.open(S/'backgrounds/exhibition_clean_1080x1920.png').convert('RGBA');d=ImageDraw.Draw(preview)
 d.text((80,110),f'C{i:02d} / LAYER AUDIT',font=ImageFont.truetype(regular,36),fill=(139,165,185))
 d.text((80,168),'未完成箇所を含む素材配置の確認用',font=ImageFont.truetype(regular,34),fill=(224,180,119))
 y=320
 for name,_,_,_ in labels[i]:
  l=Image.open(B/f'C{i:02d}/labels/{name}.png');preview.alpha_composite(l,(80,y));y+=l.height+10
 if roles[i-1]:
  ch=Image.open(S/'characters'/f'{roles[i-1]}_upperbody.png');ch.thumbnail((590,660),Image.Resampling.LANCZOS);preview.alpha_composite(ch,(60,1120))
 d=ImageDraw.Draw(preview)
 text='写真原本なし / C01 HOLD' if i==1 else '硬貨の図柄・刻印は未完成 / 本番利用HOLD'
 d.text((80,980),text,font=ImageFont.truetype(regular,36),fill=(255,204,145))
 preview.save(B/'stills_for_qc'/f'C{i:02d}_layer_audit_1080.png')
 preview.resize((360,640),Image.Resampling.LANCZOS).save(B/'stills_for_qc'/f'C{i:02d}_layer_audit_360.png')
print('LAYERS_DONE')
