from pathlib import Path
import json,csv,hashlib
from openpyxl import Workbook
R=Path(__file__).resolve().parents[2];repo=R.parent
assert json.loads((R/'qc/full_v3/report.json').read_text())['technical_result']=='PASS'
D=repo/'common_assets/nichijou_naze/props/ice_v3/v1.0.0';D.mkdir(parents=True,exist_ok=True)
# Registration descriptors point to immutable, versioned episode resources: one source, no divergent copies.
def entry(id,name,kind,source,cuts,api,parameters,notes):return {'asset_id':id,'name':name,'version':'1.0.0','kind':kind,'status':'self_qc_render_verified','source':source,'cuts':cuts,'api':api,'parameters':parameters,'usage_notes':notes,'preview':f'EP004_ICE_V3/cut{cuts[0]:02}/main.png','qc':'EP004_ICE_V3/qc/full_v3/report.json','rights':'Original AI reenactment / original Three.js geometry. See EP004_ICE_V3/licenses/. No official artwork reused.'}
assets=[
 entry('NNZ_PROP_ICE_CLOUDY_PHOTO_01','家庭の白い氷 実写風','photograph','public/ep004-v3/cut01/background.png',[1],None,{},'AI再現。中心の白濁。実験映像ではない。'),
 entry('NNZ_PROP_ICE_PROCESS_PHOTO_01','沸騰・冷却・注水の実写風セット','photo_set','public/ep004-v3/full/',[2,6],None,{'files':['boil.png','cool.png','pour.png']},'液体の工程。完成した透明氷は含まない。'),
 entry('NNZ_PROP_ICE_CONDITION_PHOTO_01','条件による白濁量の例 実写風','photograph','public/ep004-v3/full/moderate.png',[3],None,{},'沸騰後も白濁が残る一例。必ず白くなる意味ではない。'),
 entry('NNZ_PROP_ICE_COMPARE_PHOTO_01','同条件の氷比較 実写風','photograph','public/ep004-v3/full/compare.png',[10],None,{},'左右同照明・同程度サイズ。白濁量は条件依存。'),
 entry('NNZ_PROP_ICE_FACTORY_PHOTO_01','製氷工場 実写風','photograph','public/ep004-v3/full/factory.png',[8],None,{},'AI再現。公式工場写真ではない。'),
 entry('NNZ_MODEL_ICE_MICRO_01','氷内部の気泡と光散乱','Three.js scene','EP004_ICE_V3/source/full_v3/science3d.mjs',[4,5],'createScienceScene(canvas,cut) -> {draw(frame,mode),dispose}',{'cut':[4,5],'mode':['all','background','model'],'canvas':[1080,1920],'fps':30},'光線の分岐・泡の寸法は拡大模式。キャラクターと文字は別レイヤー。'),
 entry('NNZ_MODEL_FREEZING_CELL_01','家庭の製氷皿 連続凍結断面','Three.js scene','EP004_ICE_V3/source/full_v3/science3d.mjs',[7],'createScienceScene(canvas,7) -> {draw(frame,mode),dispose}',{'frames':195,'mode':['all','background','model']},'凍結形は模式。外側凍結→中心の気体集積→微細空洞。'),
 entry('NNZ_MODEL_ICECAN_AIR_01','製氷缶 送気と遅い凍結','Three.js scene','EP004_ICE_V3/source/full_v3/industrial.mjs',[8],'createAerationScene(canvas) -> {draw(frame,mode),dispose}',{'frames':165,'mode':['all','background','model']},'橙色管は送気。吸引ではない。中心の水を保持。'),
 entry('NNZ_MODEL_ICECAN_DRAIN_01','製氷缶 中心液体の吸引','Three.js scene','EP004_ICE_V3/source/scene3d.mjs',[9],'createIceScene(canvas) -> {draw(frame,mode),dispose}',{'frames':165,'mode':['all','background','model'],'physics':'EP004_ICE_V3/source/physics.mjs'},'青色管は吸水。固体を削らない。中心液体と受器の体積保存。')]
for a in assets:
 p=repo/a['source']
 if p.is_file():a['sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
manifest={'library':'nichijou-naze','version':'1.0.0','resource_set':'EP004_ICE_V3','assets':assets,'dependencies':['EP004_ICE_V3/source/vendor/three/','EP004_ICE_V3/source/physics.mjs','EP004_ICE_V3/source/full_v3/states.mjs'],'reuse':'Read descriptor by asset_id. Photographs use source/staticFile; 3D scenes expose draw(frame,mode), allowing background/model alpha separation. Version changes require a new version directory; do not mutate old resources.'}
(D/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
(D/'README.md').write_text('''# 氷の共通プロップ V1.0.0

9件のIDを登録。画像とThree.jsシーンの資源セットであり、既存テンプレを置き換えません。

```bash
node tools/ice-assets.mjs NNZ_MODEL_ICECAN_DRAIN_01
node tools/ice-assets.mjs NNZ_PROP_ICE_COMPARE_PHOTO_01
```

`manifest.json` のsourceはリポジトリルート基準。ソースを二重管理せず、版を固定したEP004_ICE_V3へ参照しています。EP004_ICE_V3/sourceとpublic/ep004-v3を一緒に維持してください。

3D APIはcanvasを渡して生成し、draw(frame,mode)で更新、終了時dispose()。mode=background/modelで背景と透過モデルを分離可能。frameは30fpsのローカル時刻。型・配色等を変更する場合は新バージョンを作成。サイズと形の基準は各ソースに明記。

キャラクターは既存v02/v03、ラベルと図解を重ねる場合は既存runtime/v1.1.0を使用。帯・字幕・進行バーは本編側へ一度だけ配置。

写真はAI再現。模式図は気泡寸法や凍結速度を実測として使わない。公式参考ページの再取得とG3は別途必要。
''')
reg=json.loads((repo/'library-registry.json').read_text());reg['iceProps']={'version':'1.0.0','manifest':str((D/'manifest.json').relative_to(repo)),'assets':[a['asset_id'] for a in assets],'status':'self_qc_render_verified'};(repo/'library-registry.json').write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n')
M=repo/'common_assets/nichijou_naze/management';rows=json.loads((M/'asset_registry.json').read_text());ids={r['Asset ID'] for r in rows}
for a in assets:
 if a['asset_id'] not in ids:rows.append({'Asset ID':a['asset_id'],'種別':a['kind'],'名前・用途':a['name'],'ステータス':'self_qc_render_verified','Version':'1.0.0','相対パス':'props/ice_v3/v1.0.0/manifest.json','使用回':'EP004 V3','権利・制作元':a['rights'],'QC':'EP004_ICE_V3/qc/full_v3/report.json','備考':a['usage_notes'],'Active':True})
(M/'asset_registry.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
with (M/'asset_registry.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator="\n");w.writeheader();w.writerows(rows)
wb=Workbook();ws=wb.active;ws.title='Assets';ws.append(list(rows[0]));[ws.append([r.get(k) for k in rows[0]]) for r in rows];wb.save(M/'asset_registry.xlsx')
ep=json.loads((R/'manifest.json').read_text())
for c in ep['cuts']:
 for a in assets:
  if int(c['cut'][3:]) in a['cuts'] and not any(x['id']==a['asset_id'] for x in c['shared_assets']):c['shared_assets'].append({'id':a['asset_id'],'version':'1.0.0','kind':a['kind']})
(R/'manifest.json').write_text(json.dumps(ep,ensure_ascii=False,indent=2)+'\n')
print('Registered',len(assets),'new resources; prior ledger rows preserved.')
