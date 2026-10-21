# 日常のなぜ？ 独立制作環境 / 共通ライブラリ導入版

導入先は **`/workspace/nichijou-naze/`**。Beyond Translationとは独立したpackage.json・依存関係・Remotion入口・public・Git管理を持つ専用プロジェクトです。BeyondのRoot・共通部品・依存宣言・過去EPは変更していません。

## 登録した実体

- `NNZ_CHAR_FEMALE_01`：8ポーズ。`neutral / talk / point_left / point_right / think / surprise / happy / troubled`。
- `NNZ_TMP_ARROW_01`：矢印説明。
- `NNZ_TMP_COMPARE_01`：左右比較。
- `NNZ_TMP_ZOOM_01`：拡大・注目。

テンプレIDと原本の1.0.0は維持し、導入版を **1.0.1** として別パスに実装しました。`library-registry.json` が有効テンプレ・キャラ・原本ハッシュ・帯の参照元を記録します。男性キャラ・口パク・部分ラベル・3ステップ・断面テンプレは未実装の予約枠のままです。

## ファイルの場所

| パス | 内容 |
|---|---|
| `vendor/common-library/1.0.0/` | 添付ZIPの原本。内容を変更しない |
| `public/common_assets/nichijou_naze/` | installerで配置した共有PNG/SVG |
| `src/common_assets/nichijou_naze/` | installerで配置した元テンプレTSX。変更せず参照用に保持 |
| `src/integration/v1.0.1/` | 字幕領域・重複帯・拡大位置などを対応した導入版 |
| `src/Root.tsx` / `src/index.tsx` | 日常のなぜ専用のRemotion登録と入口 |
| `public/series/v1/` | 再利用する既存EP004黄色帯と日本語フォント |
| `examples/*.json` | 3テンプレの差し替え設定例 |
| `validation/` | この環境で実レンダリングした動画・画像・検査結果 |

元ZIPの `tools/install_into_remotion.py` と `integration/Root.example.tsx` は確認して利用しました。installerは初回に15ファイルをコピー。既存ファイルを上書きするオプションは使っていません。原本READMEの矢印／比較の見出しにZOOM IDが記載されている箇所は原本の誤記として保持し、登録にはschema/exampleの正しいIDを使います。

元サンプルのComposition名に含まれる `_` はRemotion 4.0.526では使用できません。**設定上のテンプレIDは変更せず**、Remotion上のComposition名だけ `NNZ-TMP-ARROW-01` のようにハイフンへ変換しています。汎用レンダリング入口は `NNZ-TEMPLATE` です。

## 単体で使う

```bash
cd /workspace/nichijou-naze
npm ci --cache /workspace/.npm --no-audit --no-fund
npm run studio -- --port=3005 --no-open
npm run render -- examples/arrow.json out/arrow-v1.mp4
```

書き出し先にファイルがある場合は停止します。新しい名前を指定してください。Chrome自動取得に依存せず、検証環境では `/usr/bin/chromium` を指定します。

新EPの設定を作る例：

```bash
node tools/new-scene.mjs --template NNZ_TMP_ARROW_01 --image /path/to/image.svg --pose think --out episodes/EP005/cut01.json
npm run render -- episodes/EP005/cut01.json out/ep005-cut01-v1.mp4
```

差し替え画像は独立した `public/episodes/EP005/assets/` へ新規コピーします。既存の同名画像・設定ファイルは上書きしません。比較では `--left` と `--right`、拡大では `--image` を使います。矢印の端点、注目座標、見出しなどは生成したJSONで指定します。テンプレ本体をEPごとにコピーして修正する必要はありません。

## 既存本編へ合成する

`mode: "standalone"` は本テンプレの背景、既存黄色帯、全尺進行バーを描きます。`mode: "overlay"` は透過レイヤーで、背景・帯・進行バー・字幕を描きません。タイトルも既定では隠し、必要なら `showTitle: true` を明示します。

```tsx
import {Sequence} from 'remotion';
import {TemplateScene} from './src/Root';
import {SeriesFrame} from './src/integration/v1.0.1/Series';

// 本編全体を一度だけ包む。各SequenceをSeriesFrameで包まない。
<SeriesFrame cues={voAlignedCues} voiceover="episodes/EP005/vo.wav">
  <Sequence from={cutStartFrame} durationInFrames={cutFrames}>
    <TemplateScene config={{...sceneConfig, mode:'overlay'}} />
  </Sequence>
</SeriesFrame>
```

上のimportはプロジェクト直下の説明用例です。実際のソースファイルの位置に応じて相対パスを合わせてください。本編側にすでに帯・進行バー・字幕がある場合はSeriesFrameを追加せず、TemplateSceneのoverlayだけを合成します。

`SeriesFrame` は本編のグローバルフレーム／全尺で0→100%の進行バーを描きます。各カットでリセットしません。秒数字・カウントダウンはありません。字幕はVOに合わせた `{fromFrame,toFrame,text}` を受け取り、読点「、」だけを除去して句点「。」と改行を残します。字幕が重なる・全尺を超える場合は停止します。実VOは今回未支給なので、声そのものとの同期は未検証です。検証には明示したフレーム範囲の日本語字幕を使っています。

既存黄色帯は `/workspace/EP004_ICE/shared/opening_banner.png/svg` の実体を無加工でコピーしました。ユーザーのメッセージに見える「約30」入りの丸型画像はZIP内に元データがなく、今回再制作・置換していません。新たな「約30」の表記も追加していません。

## レイアウト

1080×1920 / 30fps。中央x=540、左右同幅を基本とし、字幕は x=96..984、y=1510..1790。キャラは原本の253px高を保ち、y=1197..1450の補助枠へ配置します。拡大ルーペとラベルもy=1470より上へ移しました。左右比較のカードは幅432、左右余白96、間隔24です。

Zoomは画像の実際の縦横比を読み、object-fit時の余白を含めて注目位置を計算します。ルーペでも同じ縦横比を維持します。新しい素材を指定した場合も0..1の注目座標を使えます。

女性キャラは試作用の123〜148×253px PNGです。高解像度化・口パク・表情パーツは制作していません。原本の権利・類似性に関する注意は維持します。今回の導入を本番内容や権利の承認とは扱いません。

## テンプレ追加・更新

1. 原本 `vendor/` と導入版 `v1.0.1/` はそのまま保持。
2. 新版は `src/integration/v1.1.0/` 等へ別パスで作成。
3. 実装コンポーネントをRootへ登録し、`tools/config.mjs` の対応ID／版の検証と `library-registry.json` を同時に追加。旧版を自動的に新版へ読み替えない。
4. 新しいschema・example・出典・実レンダー・検査結果を版ごとに保存。
5. 動作確認後、新EPのJSONで版を明示。過去EPのJSON・素材・出力は移行しない。

未登録ID・未対応版はエラーにする設計です。予約枠に名前があるだけで利用可能とは扱いません。

## ChatGPT Workへの引渡し

このプロジェクト一式、`examples/`、`library-registry.json`、検証プレビュー、`docs/WORK_HANDOFF.md` を渡します。既存EP003/EP004のmanifest形式は変更しません。新しいカットで生成した素材動画は、従来どおりEPのcutフォルダへ配置し、そのEPのmanifestにファイル名・仮尺・テンプレID・版・設定JSON参照を追加してください。原本EPのmanifestを共通ライブラリ導入のために書き換える必要はありません。
