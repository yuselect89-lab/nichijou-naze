# 素材一覧

このパックは一部制作済み。機械読取り用の全ファイル名・SHA256・用途・権利・注意点は ASSET_REGISTER.json。全6カット本番素材が完成したことは意味しない。

| ファイル／グループ | 用途 | 状態・注意点 |
|---|---|---|
| C01〜C06/labels/*.svg, *.png | G2の短ラベル。SVGは文字編集、PNGは透過ラスタ | 作成・画像検査済み。音声字幕ではない |
| shared/backgrounds/exhibition_clean_1080x1920.png | 文字・コイン・キャラなしの共通背景 | 作成済み |
| shared/characters/*_original.png | 登録済み4役の原本 | コピーのSHA一致確認済み |
| shared/characters/*_upperbody.png | 原本と分離した上半身クロップ | 役割ごとに独立配置。表情の描き替えなし |
| C01, C03, C04, C06/presenter_entrance_sequence/*.png | 640×820 RGBA、24fps、各36枚の登場素材 | 位相・尺は編集用。口パク・肢体アニメではない |
| C01/guide_sequence/*.png | 720×160 RGBA、24fps、48枚のガイド | 実写真の縁へWorkで移動・回転する。写真なし |
| shared/podium/podium_rise.blend | 編集可能な立体台座と上昇アクション | コインを含まない独立ソース |
| shared/podium/podium_static.png | 1080×1920 RGBA台座静止レイヤー | コイン・ラベル・キャラ・背景なし |
| shared/podium/rise_sequence/*.png | 1080×1920 RGBA、12fps、30枚の上昇素材 | 2.5秒の任意編集ハンドル。実音声尺ではない |
| C02/C02_C03_continuous_motion_UNFINISHED.blend | 同じ旧10円の回転・上昇と台座 | 硬貨の図柄・刻印が未完成。完成クリップではない |
| C04/C04_C05_succession_motion_UNFINISHED.blend | 10→50→100の序列と1959別モデル導入 | 硬貨の図柄・刻印が未完成。完成クリップではない |
| C06/C06_matched_tilt_UNFINISHED.blend | 別2モデルの同縮尺・同角度の傾き | ギザ数・深さの史実未検証。完成クリップではない |
| 3d_models/*/model_UNFINISHED.blend, glb, obj, mtl | 4種類の編集可能な作業用メッシュ | m単位、回転action付き。図柄・刻印なし、本番HOLD |
| 3d_models/*/audit_same_camera.png | 同じカメラ・照明での実メッシュ検査 | 4枚。実物照合済みという意味ではない |
| 3d_models/original_input/ | 受領した初期メッシュ・manifest | 原本不変保存 |
| C06/comparison_dividers.png | 上下比較の独立区切り線 | 硬貨そのものの代用品ではない |
| stills_for_qc/Cxx_layer_audit_1080.png, 360.png | 6カット各2サイズのレイヤー配置確認 | 不足点を明記。完成動画からの抽出ではない |
| docs/reference_locks/ | 最新受領指示・G2原文・権利条件 | 原文を改変しない |
| docs/WORK_HANDOFF.md | 台本対応・レイヤー・参照・尺・残作業 | Workの編集入口 |
| docs/RIGHTS_LOG.md, rights_manifest.json | 利用素材の権利と未取得候補の監査 | 写真は未取得・未使用 |
| shared/fonts/ | Noto CJK Regular/Boldとライセンス | SVGの字形再現用、OFL |

## 完成していない必須部分
C01実写真の原本・画質監査、4硬貨の図柄・刻印、ギザ本数/深さ/厚みの実物照合、最終実画QC、ユーザーへの取得可能なZIPの配布。これらが解消するまでは「素材一式完成」と扱わない。
