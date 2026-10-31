from pathlib import Path
from PIL import Image,ImageFont,ImageDraw
B=Path('/workspace/work/NNZ_GIZA10_WORK_ASSETS')
reg='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc';bold='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
for dest,parts in [('C02/labels/concept',[('最高額',bold,72),('の硬貨',reg,72)]),('C03/labels/discovery',[('硬貨の最高額＝',reg,62),('10円',bold,68)])]:
 fonts=[ImageFont.truetype(f,s,index=0) for _,f,s in parts];width=round(sum(f.getlength(p[0]) for f,p in zip(fonts,parts)))+48;height=112
 im=Image.new('RGBA',(width,height));d=ImageDraw.Draw(im);x=24;spans=[]
 for (text,file,size),f in zip(parts,fonts):
  d.text((x,16),text,font=f,fill=(245,241,230,255),anchor='lt');x+=f.getlength(text)
  spans.append(f'<tspan font-size="{size}" font-weight="{700 if file==bold else 400}">{text}</tspan>')
 im.save(B/(dest+'.png'))
 (B/(dest+'.svg')).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"><text x="24" y="82" font-family="Noto Sans CJK JP" fill="#f5f1e6">'+''.join(spans)+'</text></svg>')
