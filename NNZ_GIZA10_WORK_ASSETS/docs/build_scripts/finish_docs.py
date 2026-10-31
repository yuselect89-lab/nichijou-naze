from pathlib import Path
import json,shutil,hashlib
B=Path('/workspace/work/NNZ_GIZA10_WORK_ASSETS');I=Path('/workspace/work/giza10_asset_input');D=B/'docs'
(D/'reference_locks').mkdir(exist_ok=True)
for name in ['01_START_HERE.md','02_G2_V2_VISUAL_DESIGN_LOCK.md','03_C01_RIGHTS_AUDIT.md','05_WORK_HANDOFF_REQUIREMENTS.md']:
 shutil.copy2(I/name,D/'reference_locks'/name)
(D/'build_scripts').mkdir(exist_ok=True)
for f in Path('/workspace/work/giza10_asset_build').glob('*.py'):shutil.copy2(f,D/'build_scripts'/f.name)
(B/'3d_models/original_input').mkdir(exist_ok=True)
for f in (I/'04_GEOMETRY_INPUT').iterdir():
 if f.suffix in ['.glb','.obj'] or f.name=='GEOMETRY_MANIFEST.json':shutil.copy2(f,B/'3d_models/original_input'/f.name)
# Remove Blender automatic backups from deliverable, preserve only intended editable files.
for p in B.rglob('*.blend1'):p.unlink()
manifest=json.loads((B/'3d_models/model_manifest.json').read_text())
for entry in manifest:entry['files']=[f for f in entry['files'] if not f.endswith('.blend1')]
(B/'3d_models/model_manifest.json').write_text(json.dumps(manifest,indent=2))
rights=[{'asset_group':'shared/characters','origin':'NNZ_CHAR_FEMALE_01 v03_expressions; five inherited poses resolve unchanged v02 originals','license':'Existing user project asset; public sublicense not asserted','changes':'Unchanged original files plus separate upper-body crop and entrance sequence; provenance.json records source hashes','use':'C01 question / C03 reaction / C04 process_intro / C06 payoff; no mouth or limb rig'}, {'asset_group':'shared/fonts','origin':'System-installed Noto Sans CJK Regular/Bold','license':'SIL Open Font License 1.1; full system package copyright included','changes':'Unmodified font files; text rasterized to transparent PNG, editable SVG also included'}, {'asset_group':'3d_models/original_input','origin':'User supplied 04_GEOMETRY_INPUT','license':'User provided; no new external license asserted','changes':'Original files preserved; working copies converted mm to metres and assigned separate source objects and materials; rim parameters not altered without evidence','use':'UNFINISHED; faces absent, reed dimensions unverified'}, {'asset_group':'shared/backgrounds, shared/podium, C01/guide_sequence, labels, C06/comparison_dividers.png','origin':'Procedural assets created for this request','license':'Created for user project; no third-party photograph included','changes':'Original vector/raster/mesh creation','use':'Editable isolated supporting assets'}, {'asset_group':'C01 photography','origin':'Not obtained','license':'NOT INCLUDED / HOLD','changes':'None','use':'Do not replace with render or generated photograph'}]
(D/'rights_manifest.json').write_text(json.dumps(rights,ensure_ascii=False,indent=2))
(D/'RIGHTS_LOG.md').write_text('''# 素材の権利記録

実際に同梱した素材の根拠は rights_manifest.json と shared/characters/provenance.json。新たな有料生成・購入・外部アップロードは行っていない。

## C01 実写：HOLD
写真原本は未取得・未同梱。S29-10yen.jpg のCommons個別ページでは、作者ぽん56、1200×900、CC BY-SA 3.0を確認した。原本取得は環境プロキシが403で拒否。有効なギザ範囲の画素数・縦構図・360pxの見えは未検証。写真の使用許可・画質PASSとは報告しない。

- ページ: https://commons.wikimedia.org/wiki/File:S29-10yen.jpg
- ライセンス: https://creativecommons.org/licenses/by-sa/3.0/
- 未採用時の表示文案: 「S29-10yen.jpg — ぽん56 / Wikimedia Commons / CC BY-SA 3.0。変更：〔実際に行ったクロップ・動き付け等を編集時に記入〕」。本パックで写真を加工した事実はない。
- 第二候補「昭和27年製 ギザ十.JPG」は閲覧ツールでも取得できず、原本未確認。

## 硬貨の図柄資料
以下のCommons個別ページではAs6673 / CC BY-SA 3.0の表示を確認。原本バイナリは取得できておらず、本パックの硬貨面に転写・テクスチャ化していない。

- https://commons.wikimedia.org/wiki/File:10yen-S26.jpg
- https://commons.wikimedia.org/wiki/File:10yen-S34.jpg
- https://commons.wikimedia.org/wiki/File:50yen-S30.jpg
- https://commons.wikimedia.org/wiki/File:100yen-S32.jpg

実画像が未照合のため図柄・刻印・ギザ本数・厚みの史実準拠は未検証。販売サイトの画像は使っていない。将来CC BY-SA写真を改変利用する場合は、ファイルごとの帰属・変更表示・継承対象を整理し、本編全体が無条件で利用できるとは扱わない。

## 共通キャラクターとフォント
キャラは既存登録原本をハッシュ照合して再利用。原本と別の上半身クロップを分離し、元ファイルを上書きしていない。既存プロジェクト内での利用根拠を引き継ぐもので、公開再配布ライセンスを新設しない。Noto Sans CJKのライセンス全文は shared/fonts/Noto_CJK_LICENSE.txt。
''')
status={'scope':'Editable assets only; no finished movie or cut shorts','overall':'PARTIAL_NOT_PRODUCTION_COMPLETE','C01':'HOLD_PHOTO_MISSING; background/labels/guide/character layers exist','C02':'supporting layers and continuous animation source exist; coin face missing','C03':'supporting layers and continuous animation source exist; coin face missing','C04':'labels/character/succession rig exist; historic faces missing','C05':'labels/separate old and new model rig exist; historic faces missing','C06':'comparison labels/dividers/same-scale tilt rig exist; faces and historical edge verification missing','models':'4 editable but unfinished working models; face relief absent','audio':'Not accessed; no audio/BGM/SE created','distribution':'Specified /codex output root does not exist and cannot be created; writable /workspace copy is not user delivery','external_visual_qc':'Not performed / not claimed'}
(D/'DELIVERY_STATUS.json').write_text(json.dumps(status,ensure_ascii=False,indent=2))
(D/'WORK_HANDOFF.md').write_text('''# Work向け引継ぎ

## 状態と入口
これは編集用の分離素材パック。全素材の完成版ではない。C01写真と4硬貨の実物準拠の面・刻印が欠けているため本番組立はHOLD。DELIVERY_STATUS.jsonを先に読む。台本・構成・カット順は reference_locks/02_G2_V2_VISUAL_DESIGN_LOCK.md を原文のまま保持した。

## 編集方法
1. 1080×1920の編集コンポジションを用意し、shared/backgrounds/exhibition_clean_1080x1920.pngをベースに置く。
2. 各Cxx/layer_plan.jsonのラベル・キャラ・参照先を読み込む。SVGは文字編集用でNoto Sans CJK JPを指定。PNGは透過を維持した確定ラスタ。ラベル・キャラ・背景は別レイヤーのまま保持する。
3. PNG連番はstart=0001、motion.jsonに記録したfpsで読み込む。RGBA straight alpha。人物連番は640×820の独立スプライトで、フルフレーム映像ではない。原本PNGと上半身クロップも残してあるので再配置・再タイミング可能。
4. shared/podium/podium_rise.blendはコインを含まない本物の立体台座。静止PNGと上昇PNG連番は独立合成用。3Dソースを開けばカメラ・素材・上昇キーフレームを修正できる。
5. 3d_models配下の4モデルはmodel_UNFINISHED.blend/GLB/OBJ。単位はmに正規化、入力原本はoriginal_inputに保持。顔の図柄を完成させる前に本番硬貨として使用しない。GLBには回転アクションを含む。未検証のギザ本数・深さ・厚みを正確な実測値と扱わない。
6. C02/C02_C03_continuous_motion_UNFINISHED.blendは同じ旧10円オブジェクトの連続回転・上昇と台座、C04/C04_C05_succession_motion_UNFINISHED.blendは10→50→100の移動と別の1959モデルの導入。C06/C06_matched_tilt_UNFINISHED.blendは同角度・同縮尺で同時に傾く別2モデル。全て未完成コインの作業用rigで、本番検証済み映像ではない。
7. Blenderのカット範囲はscene custom property cut_ranges_unsyncedに記載。C02:1–72、C03:73–144、C04:1–120、C05:121–192、C06:1–72。これは24fpsの編集用の任意ハンドル。発話尺を測定した数値ではない。C03/C05のcomposition_source.jsonは継続元への相対参照。
8. 音声は一切アクセスしていない。Workで既存の確定音声に合わせてアンカー・ホールド・速度を調整する。素材の秒数をVO実測と呼ばない。
9. 字幕・正式黄色帯・進行バー・CTAは本編側で一度だけ。素材に焼き込んでいない。正式帯原本はこのパックに重複せず既存production-lock.jsonのSHA一致品を使う。字幕は読点「、」除去・句点「。」保持。

## カット別対応と残作業
- C01「昔の10円玉。なぜフチがギザギザ？」：question。写真原本とギザ画素監査なし。guide_sequenceは写真とは無関係の独立ガイドなので、写真確定後に実際の縁へ位置・角度を合わせる。推測した縁座標は入れていない。
- C02「当時は最高額の硬貨にギザを付ける慣習がありました。」：focus_only。旧10円と台座のモーション元・概念ラベル。実写とのマッチ位置は写真確定後。
- C03「1951年に製造が始まった10円玉が、なんと最高額！」：reaction。C02の同一モデルを継続。最上段への移動後にsurpriseを配置。硬貨・最高額ラベルを隠さない。
- C04「ところが50円、100円も登場。どちらもギザ付き。」：process_intro。菊花・穴なし50円と鳳凰100円の面は未制作。指差しは実際に50円を示す位置へWorkで調整し、縁実演前に退場させる。
- C05「見分けにくくなったことなどから、1959年に10円のギザは廃止されました。」：focus_only。別メッシュの平滑10円を横から導入。旧コインの変身・溶解をしていない。
- C06「あのギザは、10円玉が硬貨の頂点だった時代の名残なんです。」：payoff。上下の同縮尺比較と共通傾き。独立ラベルと区切り線。顔・縁・字幕が重ならない位置へhappyを配置。

## 検品画像
stills_for_qc/Cxx_layer_audit_1080.pngと360.pngは、作成済みレイヤーと不足点の配置確認。完成カットや実動画からの抽出フレームではない。モデルのaudit_same_camera.pngはBlenderの実メッシュ同条件レンダー。外部G2/G3実画PASSは取得していない。

## 再現性
編集元blendは外部テクスチャ不要。SVGの文字編集には同梱フォントをインストール。docs/build_scriptsは制作時の記録で元作業環境の絶対パスを含むため、別環境で再実行する際は冒頭のパス定数を変更する。通常編集はblend/GLB/PNGから行える。
''')
(B/'C03/composition_source.json').write_text(json.dumps({'blend':'../C02/C02_C03_continuous_motion_UNFINISHED.blend','frames':[73,144],'status':'unfinished geometry, unsynced'},indent=2))
(B/'C05/composition_source.json').write_text(json.dumps({'blend':'../C04/C04_C05_succession_motion_UNFINISHED.blend','frames':[121,192],'status':'unfinished geometry, unsynced'},indent=2))
for i in range(1,7):
 (B/f'C{i:02d}/README.md').write_text(f'# C{i:02d} 編集用素材\n\nlayer_plan.jsonを参照。背景は../shared/backgrounds/。labelsはSVG＋透過PNG。docs/WORK_HANDOFF.mdのカット別対応に従って合成する。\n\n本番完成ではない。C01の写真・全硬貨の図柄刻印と史実照合が未完了。フルフレーム完成ショート動画は作っていない。\n')
(B/'README_FIRST.md').write_text('# ギザ10 Work編集素材／未完成箇所あり\n\n完成動画ではなく分離素材。docs/WORK_HANDOFF.mdとdocs/DELIVERY_STATUS.jsonを先に読む。写真原本と硬貨図柄の欠品を隠していない。作成済みラベル・背景・キャラ・台座は独立して利用できる。\n')
print('DOCS_DONE')
