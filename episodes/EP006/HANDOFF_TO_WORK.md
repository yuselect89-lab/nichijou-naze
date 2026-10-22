# EP006 ChatGPT Work向け素材引渡し V1

入口は `manifest.json`、一覧は `preview/v1/contact-sheet-7cuts.jpg`。素材実体は `assets/v1/`、QCは `ASSET_QC.md` と `evidence/v1/`。この納品は**映像素材のみ**。台本は `SCRIPT_LOCK_V4.md`、映像設計は `G2_STORYBOARD_V2.md` が正本。改稿・VO生成・BGM生成・投稿をしていない。

## 読み込み

`assets/v1/Scene.tsx` は独立したSVG/React素材。`geometry.ts` はCUT04〜06の共通変形計算。Remotion / @remotion/cli 4.0.526、React 18.3.1、Node 24.19.0、Chromium、FFmpegで実検証済み。依存宣言・lockfileは変更していない。

リポジトリルートで `npm ci --cache /workspace/.npm --no-audit --no-fund`（再導入時）、`npm run preflight`、`npm run check`、`npm test`。EPソースの型検査は `./node_modules/.bin/tsc --project episodes/EP006/assets/v1/tsconfig.json`。

素材用Studio:

```bash
cd /workspace/nichijou-naze
npx remotion studio episodes/EP006/assets/v1/index.tsx --public-dir=episodes/EP006 --port=3006 --no-open
```

CLI入口は `index.tsx`。Composition `EP006-ASSET-PREVIEW`（全7カット）、`EP006-SCIENCE-CONTINUOUS`（断面一本）、`EP006-CUT01/02/03/07`。このpublic-dirでは素材ファイルが `assets/v1/` から配信される。親本編のpublic-dirが通常の `public/` の場合は、**新しいEP専用パスへ** `assets/v1/` のPNG/OTFをコピーして、staticFile参照をその配置に合わせる。既存の共通publicファイルを上書きしない。

完全再レンダーは `node episodes/EP006/assets/v1/render.mjs`。既存の全体MP4があれば安全のため停止するので、再制作は新しい納品版のディレクトリを用意してから行う。今回の最終出力はCUT03修正を `revise-cut03.mjs` で部分再レンダー後に結合し、`export-alpha.mjs` で透明見本を出力、`postprocess.py` で最終動画を再検査した。これらの修正ユーティリティは現在の納品へ重複実行しない。

## レイヤー

`Scene` の `layer` は `background / object / character / labels / all`。科学図解の `Science` は `skin / tissue / vessels / outline / labels / object / all` に分離。`object` は背景・キャラ・ラベルを含めない。`labels={false}` で主要短文を除く。静止見本のalpha PNGだけで連続アニメを代用しない。

例（Scienceのframeは親から渡す明示的な相対フレーム）:

```tsx
import {Science, Background} from './episodes/EP006/assets/v1/Scene';

// CUT04〜06全体を一度だけ配置し、同一のscienceFrameを全レイヤーに渡す。
<>
  <Background />
  <Science frame={scienceFrame} layer="tissue" labels={false} />
  <Science frame={scienceFrame} layer="vessels" labels={false} />
  <Science frame={scienceFrame} layer="skin" labels={false} />
  <Science frame={scienceFrame} layer="outline" labels={false} />
  <Science frame={scienceFrame} layer="labels" />
</>
```

SVG同士を重ねる時は同じ1080×1920・位置・scaleを維持。皮膚だけを別移動しない。簡単には `<Science frame={scienceFrame} layer="object" labels={false}/>` を一度置き、ラベルを別レイヤーにする。

キャラは無加工の原PNG。CUT02/03/07の `Scene` を `layer="character"` で読み込むと今回の上半身配置を保持できる。CUT03のキャラはローカル65〜90フレームで退場し、その後CUT04に出さない。

## 暫定タイムライン（30fps、endはexclusive）

| CUT | 全体preview | 素材相対区間 | provisional秒 |
|---|---|---|---|
| 01 | 0〜180 | CUT01ローカル0〜180 | 6 |
| 02 | 180〜300 | CUT02ローカル0〜120 | 4 |
| 03 | 300〜420 | CUT03ローカル0〜120 | 4 |
| 04 | 420〜570 | **同一Scienceの0〜150** | 5 |
| 05 | 570〜690 | **同一Scienceの150〜270** | 4 |
| 06 | 690〜870 | **同一Scienceの270〜450** | 6 |
| 07 | 870〜1050 | CUT07ローカル0〜180 | 6 |

CUT04〜06は別コンポジションへ分けてframe=0に戻さない。連続プレビューは `preview/v1/CUT04-06-continuous-1080.mp4`、スマホ確認は同 `-360.mp4`。CUT別MP4は切り位置を確認する参考素材であり、3枚の別図として切り替えるものではない。

## VO実尺へ合わせる

本番VOは未確認、35秒は仮の検査用タイムライン。VOを早回ししない。CUT04/05/06の確定フレーム数をN4/N5/N6とした時、CUT04〜06の累積フレームfを、区間ごとに `[0,N4]→[0,150]`、`[N4,N4+N5]→[150,270]`、`[N4+N5,N4+N5+N6]→[270,450]` へ連続的に写像してScienceへ渡す。端点をclampし、最後は449で保持する。必要なら完成保持区間（原ソース385〜449）を伸ばす。数値は編集のためのソース時間であり、医学的収縮率ではない。

CUT01は「浸す→時間経過→上げる」の順序と読める保持を残す。CUT03は退場が科学図解より前に完了するよう、ローカル120フレームへ同様にリタイムする。CUT07は同じ右向きの指腹の3本のシワへ接続。指先CGはオリジナル説明表現であり、撮影した実物映像ではない。

## 親本編の責務 / G3条件

正式帯は `production-lock.json` に一致する原本を縦横比維持で一度だけ合成。進行バーは本編全尺で一つ、字幕・VO・BGM/SEは本編側。VO台本を変更せず、字幕のみ読点「、」除去・句点「。」保持。素材MP4に透明性を期待しない。

素材の重要部分は帯の不透明域より下、字幕y1510より上、右UI予約x930より左に配置済み。**合成後に実360px・音声あり/なし・冒頭連続再生で再検査**する。正式帯/字幕の実表示時間、キャラ表情と科学図解への退場、皮膚密着、因果の順番、形成後保持を含め、完成ラフをGemini Pro G3へ提出する。素材セルフQCをG3 PASSとして流用しない。

## 固定・追跡・権利

共通キャラの固定ID/版・権利は `LIBRARY_DECISIONS.md`。全素材のSHA256は `manifest.json`、全納品ファイルの一覧は `DELIVERY_SHA256SUMS.txt`。`node assets/v1/validate.mjs` 相当のコマンドはリポジトリルートから `node episodes/EP006/assets/v1/validate.mjs`。共通参照は `node tools/library.mjs check episodes/EP006/manifest.json`。

受領時の一括検証は、リポジトリルートで `node episodes/EP006/assets/v1/verify-delivery.mjs`（納品75ファイル・既存660ファイル・正式帯・共通参照）、および `sha256sum -c episodes/EP006/DELIVERY_SHA256SUMS.txt`。チェックサム一覧は一覧自身を除くEP006ファイルを含み、不合格記録はevidence配下と明示されている。

開始コミットは `9fc3089e49a5c4add628120cc5e6c3e9423afd88`。納品コミットは `git log -1 --format=%H -- episodes/EP006/manifest.json` で取得できる。SHAを自己参照するためmanifest内に納品コミット自身のSHAを埋め込まない。GitHub push・公開は未実施。既存EP・原画像・共通台帳・台本LOCKは無変更。
