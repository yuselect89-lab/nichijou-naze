# 素材台帳

| パス | 用途・編集方法 | 状態 |
|---|---|---|
| C01〜C06/photos_motion_RGBA.mov | 実物の平面写真だけの無音アニメーション | qtrle/ARGB、1080×1920、24fps |
| C01〜C06/diagram_motion_RGBA.mov | 台座、ガイド、模式図だけ | 同条件の独立透過レイヤー |
| C01〜C06/labels_motion_RGBA.mov | 説明テロップだけ | 字幕・帯・CTAを含まない |
| C01/C03/C04/C06/presenter_motion_RGBA.mov | 役割ごとの女性案内役だけ | C02/C05は人物なし |
| scenes/Cxx.json | 各要素の位置/尺度/不透明度/キーフレーム | 編集の正本、音声実測ではない |
| scenes/Cxx.svg | 4グループの自己完結SMILアニメーション | 写真を平面として表示、回転なし |
| assets/photos | 元転送コピーと表裏の円形切出しPNG | 原本バイト一致は未検証 |
| assets/diagrams | 台座・縁模式図・ガイドの独立PNG | 正確な溝数や断面の再現ではない |
| assets/labels | ラスタPNGと文字編集用SVG | Noto CJK JP 正規Regular/Bold |
| assets/characters | 個別の上半身PNG | 登録済み原本からクロップ |
| assets/reuse_input / reference_input | 全ての再作成用の依存入力 | ネットワークなしで再作成可能 |
| previews_1080 / previews_360 | 各6カット＋PREVIEW_A/B | G2実画用、無音、完成本編ではない |
| qc/Cxx_1080.png・360.png | エンコード済みMP4からの実抽出フレーム | 代表6カット各サイズ |
| qc/Cxx/frame_* | 中間動作の直接レンダー検査フレーム | 実動画抽出と区別 |
| docs/PHOTO_RIGHTS.json | 使用写真の出典・版・著者・加工・表示文 | 全5素材、CC BY-SA 3.0 |
| docs/preflight_and_tests.log | 完全リポジトリでの検査 | 31件の実テスト、0件PASSではない |
| source/render_project.py | 全レイヤー再レンダー | Pillow + ffmpeg |

全ファイルのSHA256はSHA256SUMS.txt、一覧はASSET_MANIFEST.json。
