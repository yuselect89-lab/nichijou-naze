from pathlib import Path
import json
R=Path(__file__).resolve().parents[2]
D=R/'common_assets/nichijou_naze/layouts/v1.1.0/examples';D.mkdir(parents=True,exist_ok=True)
M='common_assets/nichijou_naze/layouts/v1.1.0/test_media/'
def base(id,layout,duration=180):return dict(id=id,revision='1.1.0',layout=layout,durationFrames=duration,background={'src':M+'kitchen-ice-dummy.svg'})
char=lambda pose,side='left':dict(side=side,top=1100,height=360,entry='slide',idle=True,nodAt=[60],poses=[{'fromFrame':0,'pose':pose}])
scenes=[]
for pose in ['surprise','happy','troubled']:
 s=base('expression-'+pose,'NNZ_LAYOUT_FOOTAGE_01',120);s.update(character=dict(side='left',height=1050,top=380,entry='fade',idle=True,nodAt=[50],poses=[{'fromFrame':0,'pose':pose}]))
 # Full body test on a textured neutral background, not hiding the protected real subject.
 s['background']={'src':M+'diagram-canvas.svg'};scenes.append(s)
s=base('footage-character','NNZ_LAYOUT_FOOTAGE_01');s.update(character=char('troubled'),protectedSubjects=[dict(x=310,y=500,width=460,height=500)],labels=[dict(id='core',text='白い中心',anchor=dict(x=540,y=760),box=dict(x=610,y=405,width=270,height=92),fromFrame=25)])
s['character']['poses'] += [dict(fromFrame=60,pose='surprise'),dict(fromFrame=112,pose='happy')];scenes.append(s)
s=base('diagram-character','NNZ_LAYOUT_DIAGRAM_01');s['background']={'src':M+'diagram-canvas.svg'};s.update(character=char('point_right'),crossSection={'outside':M+'ice-outside.svg','region':dict(x=240,y=400,width=660,height=650),'parts':[dict(id='shell',image=M+'ice-shell.svg',fromFrame=0),dict(id='bubbles',image=M+'ice-bubbles.svg',fromFrame=35)]},labels=[dict(id='bubble',text='小さな気泡',anchor=dict(x=570,y=730),box=dict(x=540,y=1110,width=340,height=110),fromFrame=40)],arrows=[dict(from_=dict(x=470,y=1110),to=dict(x=540,y=810),fromFrame=45)])
s['arrows'][0]['from']=s['arrows'][0].pop('from_');scenes.append(s)
s=base('focus-crosssection-return','NNZ_LAYOUT_FOCUS_01',240);s.update(focus=dict(target=dict(x=540,y=750),zoom=1.5,zoomFromFrame=25,revealFromFrame=65,revealFrames=30,returnFromFrame=185),crossSection={'outside':M+'ice-outside.svg','region':dict(x=195,y=325,width=690,height=750),'parts':[dict(id='shell',image=M+'ice-shell.svg',fromFrame=0),dict(id='bubbles',image=M+'ice-bubbles.svg',fromFrame=80)]},character=char('point_right'),labels=[dict(id='bubble',text='内部を拡大',anchor=dict(x=540,y=700),box=dict(x=550,y=1110,width=330,height=110),fromFrame=90,toFrame=185)])
scenes.append(s)
s=base('label-parameters','NNZ_LAYOUT_DIAGRAM_01');s['background']={'src':M+'kitchen-ice-dummy.svg'};s.update(labels=[dict(id='outer',text='外側',anchor=dict(x=350,y=650),box=dict(x=90,y=385,width=240,height=94),fromFrame=5,color='#176f9c'),dict(id='inner',text='中心',anchor=dict(x=540,y=760),box=dict(x=650,y=1070,width=240,height=94),fromFrame=60,color='#c36a32')]);scenes.append(s)
s=base('step3-cause','NNZ_LAYOUT_DIAGRAM_01',240);s['background']={'src':M+'diagram-canvas.svg'};s.update(steps=[dict(text='空気が残る',fromFrame=0,shape='dots'),dict(text='中心に集まる',fromFrame=65,shape='inward'),dict(text='気泡で白く見える',fromFrame=135,shape='bubbles')]);scenes.append(s)
s=base('crosssection-carton','NNZ_LAYOUT_DIAGRAM_01');s['background']={'src':M+'diagram-canvas.svg'};s.update(crossSection=dict(outside=M+'carton-outside.svg',region=dict(x=170,y=390,width=720,height=680),parts=[dict(id='shell',image=M+'carton-shell.svg',fromFrame=0),dict(id='liquid',image=M+'carton-inner.svg',fromFrame=50,toFrame=150)]),labels=[dict(id='liquid',text='内部の液体',anchor=dict(x=540,y=900),box=dict(x=510,y=1160,width=360,height=100),fromFrame=70,toFrame=150)],character=char('think'));scenes.append(s)
s=base('motions','NNZ_LAYOUT_FOOTAGE_01',240);s.update(character=char('neutral','right'),protectedSubjects=[dict(x=310,y=500,width=460,height=500)])
s['character']['poses'] += [dict(fromFrame=65,pose='talk'),dict(fromFrame=125,pose='happy'),dict(fromFrame=175,pose='think')];s['character']['nodAt']=[90,145];scenes.append(s)
# Explicit adapters reuse unchanged legacy implementations, including image-space zoom math.
for name,id,conf in [('arrow','NNZ_TMP_ARROW_01',{'image':'common_assets/nichijou_naze/props/pet_bottle/bottle_diagram.svg','arrows':[dict(x1=290,y1=990,x2=510,y2=1020,label='底')] ,'characterPose':'point_left'}),('compare','NNZ_TMP_COMPARE_01',{'left':dict(image='common_assets/nichijou_naze/props/milk_carton/carton_notch.svg',label='切欠きあり',marker='○'),'right':dict(image='common_assets/nichijou_naze/props/milk_carton/carton_plain.svg',label='切欠きなし',marker=''),'characterPose':'point_left'}),('zoom','NNZ_TMP_ZOOM_01',{'image':'common_assets/nichijou_naze/props/pet_bottle/bottle_diagram.svg','highlight':dict(x=.5,y=.86),'zoom':2.6,'label':'底の形','characterPose':'point_right'})]:
 s=base('legacy-'+name,'NNZ_LAYOUT_DIAGRAM_01');s['background']={'src':M+'diagram-canvas.svg'};s['legacyOverlay']=dict(id=id,fromFrame=0,durationFrames=180,config=dict(title='',durationSeconds=6,**conf));scenes.append(s)
for s in scenes:(D/(s['id']+'.json')).write_text(json.dumps(s,ensure_ascii=False,indent=2))
(D/'playlist.json').write_text(json.dumps([s['id'] for s in scenes],indent=2))
print('Wrote',len(scenes),'scenes,',sum(s['durationFrames'] for s in scenes),'frames')
