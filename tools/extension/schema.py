from pathlib import Path
import json
R=Path(__file__).resolve().parents[2]
string={'type':'string','minLength':1}
frame={'type':'integer','minimum':0,'maximum':3600}
def arr(item):return {'type':'array','items':item}
def ref(name):return {'$ref':'#/$defs/'+name}
def obj(props,required=()):return {'type':'object','properties':props,'required':list(required),'additionalProperties':False}
rect=obj({k:{'type':'number','minimum':0,'maximum':1920 if k in ['y','height'] else 1080} for k in ['x','y','width','height']},['x','y','width','height'])
point=obj({'x':{'type':'number','minimum':0,'maximum':1080},'y':{'type':'number','minimum':0,'maximum':1920}},['x','y'])
defs={'rect':rect,'point':point,
 'media':obj({'src':string,'kind':{'enum':['image','video']},'objectPosition':string},['src']),
 'poseCue':obj({'fromFrame':frame,'pose':{'enum':['neutral','talk','point_right','point_left','think','surprise','happy','troubled']}},['fromFrame','pose']),
 'character':obj({'side':{'enum':['left','right']},'height':{'type':'number','minimum':260,'maximum':1150},'top':{'type':'number','minimum':320,'maximum':1480},'enterFrame':frame,'exitFrame':frame,'transitionFrames':{'type':'integer','minimum':8,'maximum':30},'entry':{'enum':['fade','slide']},'idle':{'type':'boolean'},'nodAt':arr(frame),'poses':{'type':'array','minItems':1,'items':ref('poseCue')}},['poses']),
 'label':obj({'id':string,'text':{'type':'string','minLength':1,'maxLength':14},'anchor':ref('point'),'box':ref('rect'),'fromFrame':frame,'toFrame':frame,'color':string},['id','text','anchor','box','fromFrame']),
 'arrow':obj({'from':ref('point'),'to':ref('point'),'fromFrame':frame,'color':string},['from','to','fromFrame']),
 'step':obj({'text':{'type':'string','minLength':1,'maxLength':18},'fromFrame':frame,'image':string,'shape':{'enum':['dots','inward','bubbles']},'color':string},['text','fromFrame']),
 'part':obj({'id':string,'image':string,'fromFrame':frame,'toFrame':frame,'opacity':{'type':'number','minimum':0,'maximum':1}},['id','image','fromFrame']),
 'crossSection':obj({'outside':string,'parts':{'type':'array','minItems':1,'items':ref('part')},'region':ref('rect'),'cutLine':string},['outside','parts','region']),
 'focus':obj({'target':ref('point'),'zoom':{'type':'number','minimum':1.2,'maximum':3},'zoomFromFrame':frame,'revealFromFrame':frame,'revealFrames':{'type':'integer','minimum':8,'maximum':90},'returnFromFrame':frame},['target','zoom','zoomFromFrame','revealFromFrame','revealFrames']),
 'legacyOverlay':obj({'id':{'enum':['NNZ_TMP_ARROW_01','NNZ_TMP_COMPARE_01','NNZ_TMP_ZOOM_01']},'fromFrame':frame,'durationFrames':frame,'config':{'type':'object'}},['id','fromFrame','durationFrames','config'])}
s=obj({'id':string,'revision':{'const':'1.1.0'},'layout':{'enum':['NNZ_LAYOUT_FOOTAGE_01','NNZ_LAYOUT_DIAGRAM_01','NNZ_LAYOUT_FOCUS_01']},'durationFrames':{'type':'integer','minimum':60,'maximum':3600},'background':ref('media'),'title':{'type':'string','maxLength':20},'character':ref('character'),'labels':arr(ref('label')),'arrows':arr(ref('arrow')),'steps':{'type':'array','minItems':3,'maxItems':3,'items':ref('step')},'crossSection':ref('crossSection'),'focus':ref('focus'),'legacyOverlay':ref('legacyOverlay'),'protectedSubjects':arr(ref('rect'))},['id','revision','layout','durationFrames','background'])
s.update({'$schema':'https://json-schema.org/draft/2020-12/schema','$id':'urn:nnz:scene:1.1.0','$defs':defs,'description':'Shape schema. validateScene additionally checks cross-field timing, safe zones, pose availability and protected-subject overlap.'})
(R/'common_assets/nichijou_naze/runtime/v1.1.0/schema.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
print('Wrote full scene JSON schema')
