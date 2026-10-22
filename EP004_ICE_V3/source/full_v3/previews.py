from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,html
R=Path(__file__).resolve().parents[2];P=R/'preview/full_v3';font=ImageFont.truetype(str(R.parent/'public/series/v1/NotoSansCJKjp-Bold.otf'),25)
font2=ImageFont.truetype(str(R.parent/'public/series/v1/NotoSansCJKjp-Bold.otf'),17)
cs=Image.new('RGB',(1500,1250),'#f1f5f3');d=ImageDraw.Draw(cs)
for i in range(1,11):
 p=R/f'cut{i:02}/main.png';im=Image.open(p).convert('RGB');im.thumbnail((270,480));x=(i-1)%5*300+15;y=(i-1)//5*605+55;cs.paste(im,(x,y));d.text((x,y-37),f'Cut{i:02}',font=font,fill='#173f4b')
 small=Image.open(p).convert('RGB');small.thumbnail((360,640));g=ImageDraw.Draw(small)
 for xy,label,col in [((24,107,307,493),'FOREGROUND','#1ca48c'),((32,500,307,580),'CAPTION','#e87074'),((27,50,333,97),'BAND','#d3a423')]:
  g.rectangle(xy,outline=col,width=2);g.text((xy[0]+3,xy[1]+2),label,fill=col)
 small.save(P/f'cut{i:02}-safezone-360.png')
cs.save(P/'contact_sheet.jpg',quality=94)
seq=[(2,[20,95,170]),(4,[0,65,120]),(7,[0,75,135,194]),(8,[0,80,164]),(9,[0,60,110,164])]
for cut,fs in seq:
 out=Image.new('RGB',(270*len(fs),520),'#f1f5f3');dr=ImageDraw.Draw(out)
 for i,f in enumerate(fs):
  p=(R/'preview'/f'cut09-{f}.png') if cut==9 else P/f'encoded/cut{cut:02}-{f}.png'
  im=Image.open(p).convert('RGB');im.thumbnail((270,480));out.paste(im,(270*i,30));dr.text((270*i+5,5),f'Cut{cut:02} / {f/30:.2f}s',font=font2,fill='#234b58')
 out.save(P/f'cut{cut:02}-sequence.jpg',quality=94)
sections=[]
for c in json.loads((R/'manifest.json').read_text())['cuts']:
 cut=c['cut'];sections.append(f'<section><h2>{cut} / {c["start_seconds"]:g}s / {c["duration_seconds"]:g}s</h2><video controls muted playsinline preload="none" poster="{cut}/main.png" src="{cut}/animation.mp4"></video><p>{html.escape(c["animation"])}</p><a href="{cut}/animation.mp4" download>無音MP4</a> | <a href="{cut}/main.png">PNG</a></section>')
(R/'index.html').write_text('<!doctype html><html lang="ja"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>EP004 白い氷 V3</title><style>body{background:#f1f5f3;color:#234b58;font-family:sans-serif;margin:24px auto;max-width:1100px;padding:10px}main{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px}video{width:100%;max-width:360px;border-radius:16px}section{background:white;padding:18px;border-radius:24px}h2{font-size:19px}a{color:#087f9b}</style><h1>EP004「白い氷」V3</h1><p>10カット / 1080×1920 / 30fps / 無音素材。字幕・帯・進行バーは編集時に追加。全編動画なし。</p><p><a href="README.md">引き渡し手順</a> / <a href="manifest.json">manifest</a> / <a href="preview/full_v3/contact_sheet.jpg">一覧</a></p><main>'+''.join(sections)+'</main></html>')
print('Previews generated')
