from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,shutil,math,hashlib
B=Path(__file__).resolve().parents[1];R=B/'assets/reference_input';O=B/'assets/reuse_input';A=B/'assets'
# Noto font files are supplied in assets/fonts; retain those unchanged.
shutil.copy2(O/'shared/backgrounds/exhibition_clean_1080x1920.png',A/'background.png')
fb=str(A/'fonts/NotoSansCJK-Bold.ttc');fr=str(A/'fonts/NotoSansCJK-Regular.ttc')
def save(im,p):im.save(A/p);return str(Path('assets')/p)
def text(key,word,size=64,bold=True,color='#F4EFE4'):
 f=ImageFont.truetype(fb if bold else fr,size,index=0);box=f.getbbox(word);w=box[2]-box[0]+8;h=box[3]-box[1]+12;im=Image.new('RGBA',(w,h));ImageDraw.Draw(im).text((4-box[0],6-box[1]),word,font=f,fill=color)
 path=save(im,Path('labels')/(key+'.png'))
 (A/'labels'/(key+'.svg')).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"><text x="4" y="{h-8}" font-family="Noto Sans CJK JP" font-size="{size}" font-weight="{700 if bold else 400}" fill="{color}">{word}</text></svg>')
 return path
T={k:text(k,s,sz,bo,col) for k,s,sz,bo,col in [
 ('question','ギザギザ？',74,True,'#F4EFE4'),('concept','最高額の硬貨',72,True,'#F4EFE4'),('era','当時',42,False,'#AEBEC9'),('discover','硬貨の最高額＝10円',68,True,'#FFE0A0'),('succession','硬貨の最高額が交代',62,True,'#F4EFE4'),('common','3枚ともギザ付き',68,True,'#F4EFE4'),('compare','フチの違い',68,True,'#F4EFE4'),('y1951','1951年',44,False,'#AEBEC9'),('y1955','1955年',42,False,'#AEBEC9'),('y1957','1957年',42,False,'#AEBEC9'),('y1959','1959年',62,True,'#FFE0A0'),('y1959small','1959年',44,False,'#AEBEC9'),('ten','10円',66,True,'#F4EFE4'),('fifty','50円',66,True,'#F4EFE4'),('hundred','100円',66,True,'#F4EFE4'),('reeded','ギザあり',60,True,'#F4EFE4'),('smooth','ギザなし',60,True,'#F4EFE4'),('schema','模式図',38,False,'#AEBEC9'),('photo','実物写真',32,False,'#AEBEC9'),('memory','最高額だった時代の名残',40,False,'#FFE0A0')]}
T['summit']=text('summit','頂点',44,False,'#FFD68B')
# Reference copies retained unchanged. Circle crops preserve the photograph; no synthesized relief or lighting.
manifest=json.loads((R/'REFERENCE_MANIFEST.json').read_text());rights=[]
photo_specs=[('ten_old','TEN_YEN_1951_REFERENCE_COPY.jpg',[(200,200,188),(600,200,188)]),('fifty','FIFTY_YEN_1955_REFERENCE_COPY.jpg',[(240,240,196),(720,240,196)]),('hundred','HUNDRED_YEN_1957_REFERENCE_COPY.jpg',[(195,200,184),(602,200,184)]),('ten_new','TEN_YEN_1959_REFERENCE_COPY.jpg',[(200,200,188),(600,200,188)])]
for key,fn,faces in photo_specs:
 src=R/'photos_TRANSFER_COPIES_NOT_VERIFIED_ORIGINALS'/fn;shutil.copy2(src,A/'photos'/fn);im=Image.open(src).convert('RGBA')
 for j,(x,y,r) in enumerate(faces):
  out=im.crop((x-r,y-r,x+r,y+r));mask=Image.new('L',out.size);ImageDraw.Draw(mask).ellipse((0,0,2*r-1,2*r-1),fill=255);out.putalpha(mask);save(out,Path('photos')/f'{key}_{j}.png')
 entry=next(x for x in manifest['photos'] if x['file'].endswith(fn)).copy();entry['changes_in_this_package']='Circular crop of each face; downsample only; flat positional animation. No retouch, relighting, invented edge or 3D conversion.';entry['crop_centers_radii']=faces;rights.append(entry)
src=R/'photos_TRANSFER_COPIES_NOT_VERIFIED_ORIGINALS/C01_giza10_S29_REFERENCE_COPY.jpg';shutil.copy2(src,A/'photos'/src.name);im=Image.open(src).convert('RGBA').crop((150,100,1020,720));save(im,Path('photos/C01_photo_crop.png'));entry=manifest['photos'][0].copy();entry['changes_in_this_package']='Crop [150,100,1020,720], downsample to width 860; slow translation and separate guide; no retouch or generated detail';rights.append(entry)
(B/'docs/PHOTO_RIGHTS.json').write_text(json.dumps(rights,ensure_ascii=False,indent=2))
for role,w,h in [('question',480,450),('reaction',440,420),('process',400,300),('payoff',360,340)]:
 im=Image.open(O/'shared/characters'/f'{role}_upperbody.png').convert('RGBA');im=im.resize((w,round(im.height*w/im.width)),Image.Resampling.LANCZOS);im=im.crop((0,0,w,h));save(im,Path('characters')/(role+'.png'))
shutil.copy2(O/'shared/characters/provenance.json',B/'docs/CHARACTER_PROVENANCE.json')
# Isometric explanatory podium, deliberately separate from actual coin photographs.
im=Image.new('RGBA',(440,360));d=ImageDraw.Draw(im);d.polygon([(0,30),(390,30),(440,0),(50,0)],fill='#627E90');d.polygon([(0,30),(390,30),(390,360),(0,360)],fill='#304E60');d.polygon([(390,30),(440,0),(440,330),(390,360)],fill='#1C3647');d.line([(0,30),(390,30),(440,0)],fill='#D5B77A',width=5);save(im,Path('diagrams/podium.png'))
im=Image.new('RGBA',(440,120));d=ImageDraw.Draw(im);d.ellipse((0,10,439,110),fill=(255,207,120,65),outline=(255,207,120,180),width=4);save(im,Path('diagrams/top_light.png'))
for kind in ['reeded','smooth']:
 im=Image.new('RGBA',(340,78));d=ImageDraw.Draw(im);d.rounded_rectangle((1,1,338,76),radius=12,fill='#A2784C',outline='#D9BD8D',width=2)
 if kind=='reeded':
  for x in range(15,330,19):d.line((x,12,x,65),fill='#F1D8A9',width=5)
 else:d.line((15,27,325,27),fill='#F1D8A9',width=3)
 save(im,Path('diagrams')/(kind+'.png'))
im=Image.new('RGBA',(80,84));d=ImageDraw.Draw(im);d.line((40,80,40,18),fill='#FFD68B',width=5);d.polygon([(40,0),(28,24),(52,24)],fill='#FFD68B');save(im,Path('diagrams/guide.png'))
im=Image.new('RGBA',(120,180));d=ImageDraw.Draw(im);d.line((10,165,100,25),fill='#FFD68B',width=9);d.polygon([(110,5),(73,24),(108,49)],fill='#FFD68B');save(im,Path('diagrams/up_arrow.png'))
