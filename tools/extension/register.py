"""Register versioned extension metadata without changing V02 manifests or pixels."""
from pathlib import Path
import json,csv
from openpyxl import Workbook
R=Path(__file__).resolve().parents[2];A=R/'common_assets/nichijou_naze'
def write(path,data):
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
status='render_verification_pending'
if (R/'validation/extension/qc-report.json').exists():
 qc=json.loads((R/'validation/extension/qc-report.json').read_text())
 if qc.get('result')=='PASS':status='render_verified'
runtime='common_assets/nichijou_naze/runtime/v1.1.0/'
definitions=[
 ('NNZ_LAYOUT_FOOTAGE_01','全画面映像＋キャラクター','layouts/v1.1.0','footage-character','background.src / kind / objectPosition, character, protectedSubjects, labels'),
 ('NNZ_LAYOUT_DIAGRAM_01','全画面図解＋任意キャラクター','layouts/v1.1.0','diagram-character','background, optional character, crossSection, labels, arrows, steps'),
 ('NNZ_LAYOUT_FOCUS_01','実物→注目箇所拡大→断面→実物','layouts/v1.1.0','focus-crosssection-return','background, focus.target/zoom/zoomFromFrame/revealFromFrame/revealFrames/returnFromFrame, crossSection'),
 ('NNZ_TMP_LABEL_01','部分ラベルの順次表示','diagram_templates/label_01/1.1.0','label-parameters','labels[].id/text/anchor/box/fromFrame/toFrame/color'),
 ('NNZ_TMP_STEP3_01','3段階の因果説明','diagram_templates/step3_01/1.1.0','step3-cause','steps[3].text/fromFrame/image/shape/color'),
 ('NNZ_TMP_CROSSSECTION_01','物体に依存しない断面レイヤー','diagram_templates/crosssection_01/1.1.0','crosssection-carton','crossSection.outside/region/parts[].id/image/fromFrame/toFrame/opacity/cutLine'),
 ('NNZ_MOTION_BASIC_01','登場・退場・待機・うなずき・ポーズ切替','animation/basic_01/1.1.0','motions','character.side/height/top/enterFrame/exitFrame/transitionFrames/entry/idle/nodAt/poses[]')]
assets=[]
for id,name,folder,example,params in definitions:
 item=dict(asset_id=id,name=name,version='1.1.0',status=status,
  implementation=runtime+'components.tsx',
  companion_files=[runtime+'config.ts',runtime+'Chrome.tsx'],
  usage='Import the named React layer or render an example JSON via node tools/extension/render.mjs <config.json>. One EpisodeChrome outside episode Sequences.',
  required_parameters=params,
  example='common_assets/nichijou_naze/layouts/v1.1.0/examples/'+example+'.json',
  preview='validation/extension/'+example+'-'+('95' if example=='motions' else '110' if example=='focus-crosssection-return' else '75' if example=='crosssection-carton' else '170' if example=='step3-cause' else '85')+'.png',
  qc='validation/extension/qc-report.json')
 assets.append(item)
 if not id.startswith('NNZ_LAYOUT_'):write(A/folder/'manifest.json',item)
write(A/'layouts/v1.1.0/manifest.json',{'version':'1.1.0','assets':[i for i in assets if i['asset_id'].startswith('NNZ_LAYOUT_')],'test_media':'Original hand-authored SVG dummy artwork; not footage, licensed brand imagery or production EP assets.'})
write(A/'runtime/v1.1.0/manifest.json',{'library':'nichijou-naze','version':'1.1.0','assets':assets,
 'canvas':[1080,1920],'fps':30,'frame_clock':'Sequence-local scene timing; episode-global SeriesFrame progress and caption cues.',
 'overlay_rule':'Character and diagram layers never include band, captions or progress. EpisodeChrome wraps once at episode level.',
 'safe_zones':{'foreground':{'left':72,'right':920,'top':320,'bottom':1480},'captions':{'left':96,'top':1500,'width':824,'height':240},'shorts_reserved':{'right_from':920,'bottom_from':1740}},
 'character_version':'v03_expressions','inherited_character_version':'v02_highres','qc':status,
 'drive':{'url':'https://drive.google.com/drive/folders/1YmGCqmzf_XndpvS62sMKFr4wdTrI-CK7','status':'not_updated','reason':'No Google Drive connector/authenticated identity available; drive.google.com is not an allowed destination in this environment.'}})
registry=json.loads((R/'library-registry.json').read_text());registry['extensions']={'version':'1.1.0','manifest':'common_assets/nichijou_naze/runtime/v1.1.0/manifest.json','status':status,'assets':[x['asset_id'] for x in assets]}
registry['characterVersions']={'v02_highres':{'manifest':'common_assets/nichijou_naze/characters/female_v01/manifest.json','unchanged':True},'v03_expressions':{'manifest':'common_assets/nichijou_naze/characters/female_v01/versions/v03_expressions/manifest.json','addedPoses':['surprise','happy','troubled'],'inherits':'v02_highres','status':status}}
registry['plannedOnly']=[x for x in registry['plannedOnly'] if x not in [a['asset_id'] for a in assets]]
for a in assets:
 if a['asset_id'].startswith('NNZ_TMP_'):
  registry['activeTemplates']=[t for t in registry['activeTemplates'] if not(t['id']==a['asset_id'] and t['revision']=='1.1.0')]
  registry['activeTemplates'].append({'id':a['asset_id'],'revision':'1.1.0','implementation':a['implementation'],'manifest':'common_assets/nichijou_naze/'+next(folder for id,_,folder,_,_ in definitions if id==a['asset_id'])+'/manifest.json'})
write(R/'library-registry.json',registry)
ledger=A/'management/asset_registry.json';rows=json.loads(ledger.read_text())
new=[('NNZ_CHAR_FEMALE_01','追加表情3種＋V02参照8ポーズ','characters/female_v01/versions/v03_expressions/manifest.json','v03_expressions','キャラ')]+[(id,name,folder+'/manifest.json','1.1.0','動作' if id.startswith('NNZ_MOTION') else 'レイアウト' if id.startswith('NNZ_LAYOUT') else 'テンプレ') for id,name,folder,_,_ in definitions]
for id,name,path,version,kind in new:
 rows=[row for row in rows if not(row['Asset ID']==id and row['Version']==version)]
 rows.append({'Asset ID':id,'種別':kind,'名前・用途':name,'ステータス':status,'Version':version,'相対パス':path,'使用回':'共通素材','権利・制作元':'既存V02参照AI描き起こし＋整形' if kind=='キャラ' else '独自実装／既存共通演出再利用','QC':'validation/extension/qc-report.json','備考':'既存V02・旧EP・過去レンダーは不変','Active':True})
keys=list(rows[0]);write(ledger,rows)
with ledger.with_suffix('.csv').open('w',encoding='utf-8-sig',newline='') as f:
 writer=csv.DictWriter(f,fieldnames=keys,lineterminator='\n');writer.writeheader();writer.writerows(rows)
wb=Workbook();ws=wb.active;ws.title='Assets';ws.append(keys)
for row in rows:ws.append([row.get(k,'') for k in keys])
ws.freeze_panes='A2';ws.auto_filter.ref=ws.dimensions
wb.save(ledger.with_suffix('.xlsx'))
print('Registered',len(assets),'functions and3expressions; status=',status)
