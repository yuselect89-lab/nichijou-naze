"""Rebuild R2 labels, diagrams and six frame-accurate editable scenes.
Uses preserved R1 photographs/whole upper-body derivatives; no generation API.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, html, shutil
B=Path(__file__).resolve().parents[1]
FONT=B/'assets/fonts/NotoSansCJK-Bold.ttc'
WHITE='#F4F7FC'; GOLD='#FFD47D'; CYAN='#8DDFEC'
def label(id,text,size=48,color=WHITE):
 f=ImageFont.truetype(str(FONT),size);bb=f.getbbox(text);w=bb[2]-bb[0]+12;h=bb[3]-bb[1]+14
 im=Image.new('RGBA',(w,h));ImageDraw.Draw(im).text((6-bb[0],7-bb[1]),text,font=f,fill=color)
 im.save(B/'assets/labels'/f'{id}.png')
 (B/'assets/labels'/f'{id}.svg').write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><text x="{6-bb[0]}" y="{7+f.getmetrics()[0]-bb[1]}" font-family="Noto Sans CJK JP" font-weight="700" font-size="{size}" fill="{color}">{html.escape(text)}</text></svg>')
 return f'assets/labels/{id}.png'
def diagram(id,w,h,paths):
 im=Image.new('RGBA',(w,h));d=ImageDraw.Draw(im)
 for kind,coords,color,width in paths:
  if kind=='line':d.line(coords,fill=color,width=width,joint='curve')
  elif kind=='rect':d.rectangle(coords,outline=color,width=width)
 im.save(B/'assets/diagrams'/f'{id}.png')
 svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">']
 for kind,xy,color,width in paths:
  if kind=='line':svg.append(f'<polyline points="'+ ' '.join(f'{xy[i]},{xy[i+1]}' for i in range(0,len(xy),2))+f'" fill="none" stroke="{color}" stroke-width="{width}"/>')
  else:svg.append(f'<rect x="{xy[0]}" y="{xy[1]}" width="{xy[2]-xy[0]}" height="{xy[3]-xy[1]}" fill="none" stroke="{color}" stroke-width="{width}"/>')
 (B/'assets/diagrams'/f'{id}.svg').write_text(''.join(svg)+'</svg>')
 return f'assets/diagrams/{id}.png'
def strip(id,w=600,h=135,reeded=True):
 im=Image.new('RGBA',(w,h));d=ImageDraw.Draw(im);d.rectangle((3,3,w-4,h-4),fill='#AFBBC8',outline=WHITE,width=5)
 if reeded:
  for x in range(15,w-12,18):d.rectangle((x,10,x+7,h-11),fill='#293C50')
 im.save(B/'assets/diagrams'/f'{id}.png')
 parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"><rect x="3" y="3" width="{w-7}" height="{h-7}" fill="#AFBBC8" stroke="{WHITE}" stroke-width="5"/>']
 if reeded:
  parts += [f'<rect x="{x}" y="10" width="8" height="{h-20}" fill="#293C50"/>' for x in range(15,w-12,18)]
 (B/'assets/diagrams'/f'{id}.svg').write_text(''.join(parts)+'</svg>')
 return f'assets/diagrams/{id}.png'
def item(id,group,asset,keys):return dict(id=id,group=group,asset=asset,keys=keys)
def static(id,group,asset,x,y,w=None,h=None,fade=None):
 im=Image.open(B/asset);w=w or im.width;h=h or round(im.height*w/im.width)
 ks=[[0,x,y,w,h,1]]
 if fade:ks=[[0,x,y,w,h,0],[fade[0],x,y,w,h,0],[fade[1],x,y,w,h,1]]
 return item(id,group,asset,ks)
def txt(id,text,x,y,size=48,color=WHITE,fade=None):return static(id,'labels',label(id,text,size,color),x,y,fade=fade)
def fadeout(o,a,b):
 k=o['keys'][-1];o['keys'] += [[a,*k[1:5],1],[b,*k[1:5],0]];return o
def scene(c,n,items):
 s=dict(cut=c,width=1080,height=1920,fps=24,frames=n,duration=n/24,timing_status='Frame boundaries from supplied CURRENT_EDIT_REFERENCE_NOT_APPROVED.json; audio not accessed',background='assets/background.png',items=items,layer_order=['photos','diagram','labels','presenter'])
 (B/'scenes'/f'{c}.json').write_text(json.dumps(s,ensure_ascii=False,indent=2));return s
def main():
 # Preserve C01 behavior and whole upper-body gesture; exact current-edit frame count.
 s=json.loads((B/'references/C01_R1_scene.json').read_text());s.update(frames=100,duration=100/24)
 for o in s['items']:
  for k in o['keys']:k[0]=min(k[0],100/24)
 # This photo is fully within the UI boundary, not silently shaved by safety clip.
 s['items'][0]['keys'][0][1]=65;s['items'][0]['keys'][1][1]=80
 for k in s['items'][2]['keys'][:3]:k[1]-=30
 (B/'scenes/C01.json').write_text(json.dumps(s,ensure_ascii=False,indent=2))
 old='assets/photos/C01_photo_crop.png';photo='assets/photos/ten_old_1.png'
 # C02: actual oblique old ten, guide stays on its photographed front edge.
 items=[txt('custom','高額の硬貨には',90,610,50),txt('reeded_custom','ギザ',90,680,76,GOLD),
 static('old10','photos',old,120,820,700),
 item('actual_edge_guide','diagram','assets/diagrams/guide.png',[[0,640,1160,76,80,1],[2.2,675,1144,76,80,1],[113/24,640,1160,76,80,1]])]
 scene('C02',113,items)
 # C03: identical photograph rises; headline and value belong to occupied photo.
 p=item('old10','photos',old,[[0,120,820,700,499,1],[2.7,390,620,540,385,1]])
 guide=item('actual_edge_guide','diagram','assets/diagrams/guide.png',[[0,640,1160,76,80,1],[2.7,791,882,62,65,1]])
 items=[p,guide,txt('manufacture1951','1951年 製造開始',400,1380,44),
 txt('highest10','硬貨の最高額',400,1040,58,GOLD,(3.15,3.4)),txt('value10','10円',400,1120,98,WHITE,(3.15,3.4)),
 item('presenter','presenter','assets/characters/reaction.png',[[0,20,985,340,463,0],[3.55,20,985,340,463,0],[3.87,20,960,340,463,1],[5.1,20,960,340,463,1]])]
 # Connector below the photo; never through a year or denomination.
 link=diagram('highest_attachment',500,35,[('line',[80,0,80,30,300,30],GOLD,5)])
 items.append(static('attached','diagram',link,400,1007,500,35,fade=(3.15,3.4)))
 scene('C03',133,items)
 # C04: all physical diameters remain 12 px/mm; denomination emphasis changes.
 # Old photo retreats first, then fifty enters same focus position, then hundred.
 items=[item('ten','photos',photo,[[0,209,659,282,282,1],[.35,209,659,282,282,1],[.72,40,1180,282,282,1]]),
 item('fifty','photos','assets/photos/fifty_0.png',[[0,200,650,300,300,0],[.72,200,650,300,300,0],[.9,200,650,300,300,1],[1.38,200,650,300,300,1],[1.62,350,1180,300,300,1]]),
 item('hundred','photos','assets/photos/hundred_0.png',[[0,215,665,271,271,0],[1.62,215,665,271,271,0],[1.84,215,665,271,271,1]])]
 items += [txt('highest','硬貨の最高額',70,980,58,GOLD),txt('c4_ten','10円',180,1060,88),txt('c4_fifty','50円',180,1060,88,fade=(.72,.9)),txt('c4_hundred','100円',180,1060,88,fade=(1.62,1.84)),
 txt('retired10','10円',90,1125,42,fade=(.74,.9)),txt('retired50','50円',680,1310,42,fade=(1.64,1.8)),
 txt('date50','1955年 50円',90,590,42,fade=(.72,.9)),txt('date100','1957年 100円',90,590,42,fade=(1.62,1.84))]
 # Highest title is attached only to the currently occupied focus photo.
 title=next(o for o in items if o['id']=='highest');fadeout(title,.34,.4)
 items += [fadeout(txt('highest50','硬貨の最高額',70,980,58,GOLD,fade=(.72,.9)),1.38,1.42),txt('highest100','硬貨の最高額',70,980,58,GOLD,fade=(1.62,1.84))]
 # Nonoverlapping outgoing/incoming values: no illegible numeral crossfade.
 for o in items:
  if o['id']=='c4_ten':o['keys']=[[0,180,1060,*Image.open(B/o['asset']).size,1],[.34,180,1060,*Image.open(B/o['asset']).size,1],[.4,180,1060,*Image.open(B/o['asset']).size,0]]
  if o['id'] in ['c4_fifty','date50']:fadeout(o,1.38,1.42)
 items += [item('presenter','presenter','assets/characters/process.png',[[0,540,625,400,366,0],[.18,540,625,400,366,0],[.5,540,600,400,366,1],[1,540,600,400,366,1],[1.2,540,600,400,366,0]])]
 for id,bottom,fade in [('ten',941,None),('fifty',950,(.72,.9)),('hundred',936,(1.62,1.84))]:
  a=diagram('highest_link_'+id,1080,1920,[('line',[350,bottom,350,970,200,970],GOLD,4)])
  o=static('highest_link_'+id,'diagram',a,0,0,1080,1920,fade=fade)
  if id=='ten':fadeout(o,.34,.4)
  elif id=='fifty':fadeout(o,1.38,1.42)
  items.append(o)
 scene('C04',122,items)
 # C05: three independently linked examples, then a genuinely separate 1959 photo.
 items=[]
 for id,asset,x,d in [('10','ten_old_1',80,212),('50','fifty_0',360,225),('100','hundred_0',660,203)]:
  cx=x+d/2
  objects=[txt('c5value'+id,id+'円',x,610,48),static('coin'+id,'photos',f'assets/photos/{asset}.png',x,700,d),
    static('schema'+id,'diagram',strip('schema'+id,230,110),x-10,1000),
    txt('reeded'+id,'ギザあり',x-10,1125,40),txt('schema_label'+id,'模式図',x,1182,36,CYAN)]
  line=diagram('link'+id,1080,1920,[('line',[cx,700+d,cx,980,cx,1000],CYAN,5)])
  objects.append(static('link'+id,'diagram',line,0,0,1080,1920))
  items.extend(fadeout(o,2.4,2.72)for o in objects)
 items += [static('separate1959','photos','assets/photos/ten_new_1.png',320,900,300,fade=(2.82,3.12)),
 txt('change1959','1959年 ギザなしへ',110,670,56,GOLD,fade=(2.82,3.12)),
 static('separate1959_edge_schema','diagram',strip('c5_smooth',480,120,False),230,1260,480,120,fade=(3.12,3.32)),
 txt('new_schema_label','模式図',390,1400,38,CYAN,fade=(3.12,3.32))]
 newlink=diagram('new1959link',1080,1920,[('line',[470,1200,470,1260],CYAN,5)])
 items.append(static('new1959link','diagram',newlink,0,0,1080,1920,fade=(3.12,3.32)))
 scene('C05',153,items)
 # C06: matched 600/650 downsample of actual front edges. Whole source coins
 # remain small, with crop rectangle + leader to make the enlargement traceable.
 orig=Image.open(B/'references/repair_order_20261101/references/COMMONS_COMPARISON_ORIGINAL.jpg')
 specs=[('old',(1080,800,1840,1350),(1135,1090,1785,1340),690,950,180),('new',(1990,800,2760,1340),(2050,1080,2700,1330),1150,1390,160)]
 cropdata=[r for r in json.loads((B/'docs/CROP_COORDINATES.json').read_text()) if not r['id'].endswith('_source_thumbnail')];items=[]
 for id,box,crop,y,thumb_y,tw in specs:
  orig.crop(box).save(B/'assets/photos'/f'whole_{id}.png');th=round((box[3]-box[1])*tw/(box[2]-box[0]));scale=tw/(box[2]-box[0]);tx=30
  items += [static('edge_'+id,'photos',f'assets/photos/edge_{id}.png',30,y,600,231),static('whole_'+id,'photos',f'assets/photos/whole_{id}.png',tx,thumb_y,tw,th)]
  rect=[tx+(crop[0]-box[0])*scale,thumb_y+(crop[1]-box[1])*scale,tx+(crop[2]-box[0])*scale,thumb_y+(crop[3]-box[1])*scale]
  line=diagram('crop_trace_'+id,1080,1920,[('rect',rect,CYAN,4),('line',[rect[0],(rect[1]+rect[3])/2,14,(rect[1]+rect[3])/2,14,y+110,30,y+110],CYAN,4)])
  items.append(static('crop_trace_'+id,'diagram',line,0,0,1080,1920))
  cropdata.append(dict(id=id+'_source_thumbnail',source_box=box,display_xywh=[tx,thumb_y,tw,th],crop_frame_display_xyxy=rect,actual_enlargement_xywh=[30,y,600,231]))
 items += [txt('old_type','旧型：ギザあり',30,620,44),txt('new_type','1959年以降の型：ギザなし',30,1092,38),
 txt('memory','かつて硬貨の最高額',240,960,34,GOLD,fade=(2,2.25)),txt('memory_value','10円',240,1010,62,WHITE,fade=(2,2.25)),
 item('presenter','presenter','assets/characters/payoff.png',[[0,630,635,300,367,0],[2.5,630,635,300,367,0],[2.82,630,610,300,367,1]])]
 memorylink=diagram('memory_attachment',180,35,[('line',[0,0,0,30,120,30],GOLD,4)])
 items.append(static('memory_attachment','diagram',memorylink,300,922,180,35,fade=(2,2.25)))
 scene('C06',110,items)
 (B/'docs/CROP_COORDINATES.json').write_text(json.dumps(cropdata,ensure_ascii=False,indent=2))
 # Large editable fallback, same shape, color, scale; only grooves differ.
 strip('M04_reeded_large',600,135,True);strip('M04_smooth_large',600,135,False);label('M04_explicit_schema','縁の模式図',42,CYAN)
 print('BUILT_R2_SCENES',flush=True)
if __name__=='__main__':main()
