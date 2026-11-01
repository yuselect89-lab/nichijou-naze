# 「日常のなぜ？」信号機の赤が右端｜G2映像設計 V1
作成：2026-11-01（JST）
状態：**G1 V2採用（先行QCの2修正反映）／G2 V1書面QC待ち／素材制作未実施**
正本台本：`../g1/SCRIPT_V2_20261101.md`
制作担当：Codex＝全カット用素材／可動ソース、Work＝支給音声・正式黄色帯・字幕・進行バー・本編組立

## 1. 発見と画づくりの核
**問い**：日本の横型信号機は、なぜ赤が右端なのか？
**発見**：赤信号を道路の中央寄りに置き、運転者から見やすくするため。街路樹などで道路脇から信号の一部が隠れる可能性への配慮も理由の一つ。
**Before→After**：ただの色の並び → 最も重要な赤の見落としを減らすための配置。
**冒頭の視覚的疑問**：「青→黄→赤」と並んだ横型信号機、右端の赤だけに視線を誘導する。長文巨大テロップは使用しない。
**映像文法**：写実の街角・信号（C01–C02）→同じ場所の枝の遮蔽と位置関係を写実ベース+説明オーバーレイで示す（C03–C05）→冒頭の同じ信号に戻る（C06）。
参考動画「水を沸かして凍らせたら、透明な氷になる？」から採用するのは**実物→必要な模式表現→実物**という繋がりとキャラの限定登場。見本映像そのものの転載はしない。

## 2. 法令・科学的な厳守条件
- 対象は**日本の自動車向け横型3灯式信号機**に限定。正面の灯火は**左から青・黄・赤**。縦型や歩行者信号、海外信号と混同しない。
- 「赤が右端」は全体の灯火配列の話。街路樹が伸びて信号を隠すことは**ありうる具体例**であって、すべての設置箇所で左側から必ず隠れると断言しない。
- 「道路中央寄り」は、**道路の左側に取り付けた横型信号機**を例に視認性を説明する。右側設置や道路中央上の信号に無条件に一般化しない。映像内の柱・道路・車線・進行方向を統一する。
- 道路を左側通行する車を、**正しい向きの左側車線**で描く。信号の色の順序と左側通行の整合を1フレームずつQCする。
- 点灯状態は同一時点の1灯のみ。3灯同時点灯、赤と青同時点灯等の不正確な画は禁止。街路樹再現は「想定イメージ/模式再現」表示で現実の事故映像と偽らない。
- e-Gov道路交通法施行令第3条（配列）：https://laws.e-gov.go.jp/law/335CO0000000270
- JAF（目的・街路樹例）：https://jaf.or.jp/common/kuruma-qa/category-drive/subcategory-sign/faq166
- 公的・記事の写真や図を無許可でトレース・使用しない。科学・法令の**確認**用途に限る。

## 3. VO同期・カット構成
**V2の6発話＝6カット。** このEPの支給音声は未実測。**30秒や各秒数を確定値として書かない**。切り替え位置は実VOのフレーズ境界に合わせWorkが最終決定する。全素材は独立ループ・延長可能な動きで制作し、口パク・強制速度変更なしで同期可能にする。

| Cut | G1 V2音声（アンカー） | 動き／重点 | キャラ |
|---|---|---|---|
| C01 | 横型の信号機。赤はなぜ右端にあると思いますか？ | 現物の横型信号へ寄る→右端の赤を見せる | question（後半のみ） |
| C02 | 実は、一番大切な赤信号を見えやすくするためなんです。 | 同じ信号・同じ角度で、赤の視認性を示す | reaction→reveal_intro |
| C03 | 日本は左側通行。 | 同じ通りの車線と道路脇の木・信号配置が分かる画へ移行 | focus_only |
| C04 | 道路脇の街路樹が伸びると、信号機の左側が隠れてしまうことがあります。 | 枝をイメージ上で伸ばし、信号機の左側から一部が隠れる例を可視化 | focus_only |
| C05 | そこで、一番見落としてはいけない「止まれ」の赤を、道路の中央寄りに配置。 | 同じ場所で赤が中央寄りに残り、枝より見えやすい関係を強調 | focus_only |
| C06 | つまり、あの色の順番には、赤信号を見失わないための工夫が隠されていたんです。 | 枝オーバーレイを戻し冒頭の実物に復帰、右端の赤を回収 | payoff |

### C01｜実物と疑問
- 実写の横型3灯式信号機をカメラの前方に大きく表示。道路背景は実在感、車は安全な停止状態。撮影権利が確保できない場合は**無ブランドの写実AI再現**とし、実物撮影と称さない。
- カメラは道路の左脇側から信号へ緩く寄る。最初の1秒で「信号」と認識でき、最後に右端が視線の焦点。赤灯の位置が画面右端のShorts UIと重ならないよう信号全体を中央付近へ。
- primary_text：`N/A: visual-first`（信号機の並び自体が主役）。secondary_text：必要なら短く「なぜ右端？」。
- size_hierarchy：右端赤灯＞短い問い。weight_strategy：短い問いは正規Bold。luminance_strategy：赤灯をくっきり、周囲の街角は自然な輝度。typeface_reason：短時間で読める既存ゴシック。
- presenter：`NNZ_CHAR_FEMALE_01`を疑問の後半に上半身で短く出し、赤灯を見て考える。信号と問いを遮らない。

### C02｜「見えやすい」先出し
- C01と同一の信号・背景。左右の青と黄を少し視覚的に抑え、右端の赤の輪郭だけ1回ゆるやかに強調（街の信号そのものは描き換えない）。
- primary_text：「大切な赤を見やすく」。secondary_text：なし。size_hierarchy：赤灯＞短い主役句。weight_strategy：Bold。luminance_strategy：赤灯の輪郭＞文字＞背景。typeface_reason：日本語ゴシック、読速を優先。
- presenter：驚きの一瞬→機構説明に入る前に退場。小さな全身マスコット常駐は禁止。

### C03｜左側通行と配置
- 写実道路のカメラを少し引き、道路左側を進行する車両・**道路左端の街路樹**・横型信号が同時に分かるアングルへ。必要なら地面に矢印を1本だけ合成し、左側通行が直感的に理解できるようにする。
- primary_text：「左側通行」。secondary_text：なし。size_hierarchy：道路と車線方向＞短い語。weight_strategy：Bold。luminance_strategy：走行方向の矢印と語を背景から分離。typeface_reason：説明用ゴシック。
- focus_only：キャラ退場。**信号位置と進行向きがC04/C05と同一**になるよう世界座標固定。

### C04｜枝による遮蔽の模式再現
- C03と同じ通り・信号の位置。道路脇左の木の枝が**時間圧縮／半透明モーション**で伸び、左側の青い灯火付近から一部を覆い始める例を示す。次第に黄まで隠れるような過剰な遮蔽は不可。赤が右側で相対的に見やすいことを素直に示す。
- **「想定イメージ」**を小さく表示。自然映像上の枝アニメは模型の仮定であり実写の樹木成長ではない。
- primary_text：「左側が隠れることも」。secondary_text：「想定イメージ」。size_hierarchy：遮蔽の動き＞短い語＞小注記。weight_strategy：主Bold／補Regular。luminance_strategy：葉の輪郭で信号が隠れる状態を明瞭に、枝が暗すぎて全信号を消さない。typeface_reason：注釈も即読可能なゴシック。
- focus_only：キャラなし。**木の枝を道路中央から突然出さない**。

### C05｜右端の赤＝中央寄り
- C04と同一アングルのまま。信号の灯火順を保ち、赤灯までの位置関係を**道路脇→道路中央**の短い補助矢印で示す。赤灯は枝の影響を受けにくい例として見せ、他の灯火の光を不自然に点灯させない。
- 「右端」だけではなく**「道路の中央寄り」**が主たる発見。車道の中心を誤認させる架空の車線標示を描かない。枝の影響は補足として残す。
- primary_text：「赤は中央寄り」。secondary_text：「見落としにくく」。size_hierarchy：赤の位置＞主役句＞補足。weight_strategy：Bold／Regular。luminance_strategy：赤灯と位置矢印を高コントラスト、他は控えめ。typeface_reason：説明図解と相性のよいゴシック。
- focus_only：キャラなし。リアル映像＋必要最小限の線で理解を優先。

### C06｜実物へ戻して納得
- 枝のイメージを取り除き、**C01と同じ信号の角度／灯火順**へ戻る。青・黄・赤の3灯並びを見せ、右端の赤を一度だけわずかに強調。最後に余韻を残す。文字カードだけで締めない。
- primary_text：「赤を見失わない工夫」。secondary_text：なし。size_hierarchy：信号＞主役語。weight_strategy：正規Bold。luminance_strategy：赤灯・主役語を優先、背景過度に暗くしない。typeface_reason：短く一読できるゴシック。
- presenter：高解像度承認キャラの上半身、納得した表情で短く。顔が信号とYouTube UIに干渉するなら登場時刻／配置を調整。

## 4. モデル・素材の制作仕様
- `EXT_STREET_MASTER`：日本の街路、左側通行の道路、道路左側の横型信号機と木（**C01–C06同一空間、位置固定**）。可能なら自前・適切なライセンスの実写素材。なければAI生成の写実再現を制作する前提で設計し、素材調達待ちで工程を止める仕様にしない。
- `SIGNAL_LAMP_MASTER`：信号本体の**左右3灯を位置制御できる分離レイヤー**。青→黄→赤を画像生成の誤生成に任せず、編集可能なパーツで正確に固定。表示中は赤1灯の点灯状態を基本とする。
- `BRANCH_MASK`：道路左側からのみ進入する葉と枝の覆い。C04/C05で同じループ・同じ深度を使用し、「想定イメージ」を明示。木と信号の奥行き関係が崩れないようマスク・透過レイヤーで制御。
- `ROAD_CENTER_GUIDE`：赤灯が**道路中央寄りに位置する相対関係**を示す説明線。車線・矢印が道路規制表示と誤認されないよう、説明用オーバーレイとして使用。
- `CHAR_ASSETS`：登録済み `NNZ_CHAR_FEMALE_01` の思案・驚き・納得（高解像度元画像）。重ねるだけの小さい全身は禁止。
- `LABELS`：文字レイヤーは全部別管理。日本語フォント・ウェイト・ライセンスとフォールバックを確認。AI生成の誤字を採用しない。
- AI実写再現を使う際は生成プロンプト・モデル・権利記録をmanifestに残す。見本やJAFの写真を無断で模写・転載しない。

### 写実背景生成プロンプト案（Codex発注時）
> Documentary-realistic Japanese urban intersection seen from a safe roadside camera, left-hand road traffic, a single horizontally mounted three-lamp traffic signal on the left side of the roadway, signal facing approaching cars, clearly ordered left-to-right as blue/green, amber, red, roadside tree to the left of the signal, realistic poles and road markings, daylight, 9:16 portrait, consistent fixed camera geometry and no branding. The rightmost red lens must remain visible. No lettering, no signs or overlays, no duplicated signals, no wrong-direction traffic, no simultanously illuminated contradictory lights. Keep signal geometry stable for overlay layers.

**重要**：生成器が灯火配置・道路の向き・枝の前後関係を間違えた場合、誤生成を完成品としない。実際の3灯は別パーツとして正しい位置で合成する。赤灯が右側で道路中央寄りにあることをC03/C05で独立検証する。

## 5. シリーズLOCK・実画QC
- 1080×1920、9:16。黄色帯は `production-lock.json` 正本 `public/series/approved/opening_banner.png` の指定SHAを維持。Codex素材に正式帯・字幕・進行バーを焼き込まず、Workで一度だけ合成する。
- 字幕は Work で「、」除去、「。」維持。字幕・Shorts UI・帯の安全域は既存テンプレに従う。360px実画で、赤・枝・テキスト・キャラの顔が隠れないこと。
- 文字デザイン4原則は上記全カットに `primary_text`、`secondary_text`、`size_hierarchy`、`weight_strategy`、`luminance_strategy`、`typeface_reason` として指定。既存ロックで許可されない色・書体で装飾しない。
- 音声は未実測。秒数、開始時刻、最後の発話尺を勝手に確定しない。支給音声や台本の編集・高速化をしない。音声提出要求禁止。
- `AGENTS.md`、`production-lock.json`、`docs/PRODUCTION_LOCK.md`、`docs/WORK_HANDOFF.md`、`docs/PRESENTER_DIRECTION.md`、`docs/TYPOGRAPHY_4_PRINCIPLES.md`、`docs/VISUAL_QUESTION_DIRECTION.md`、`docs/CONTEXT_EFFICIENCY_POLICY.md`に準拠。
- Codex実制作へ移る前に `npm run preflight`、素材台帳検索、必要素材 `requirements.json`・`node tools/library.mjs preflight ... --strict`、レンダーQCを実施。実画QCは実行したもののみPASSとする。
- 3色の並びが正しいか、右端赤が道路中央寄りになっているか、木の枝が覆うのは道路脇の左側か、場面間で配置が変化しないか、視覚的な反例になっていないか、360px可読性をチェック。
- Codexは**全カット素材と可動ソース・QC・Work引継ぎZIP**を作る担当。Workは本編完成MP4を作る。G2設計時点では素材作成の完了を宣言しない。

## 6. 状態
- G1：V2修正を採用。先行外部QCの「V2採用ならG2移行可能」を適用。V2について独立した再QCは未受領。
- G2：**V1書面作成済み・QC待ち**。素材制作へはG2書面PASS後に移す。
- VO：実尺・発話位置未実測。仮尺の動画長を固定しない。
- モデル／画像／MP4：実制作と実画QCは未実施。
