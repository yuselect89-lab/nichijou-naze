# 共通ライブラリ拡張 1.1.0

実物を全画面で見せ、キャラで疑問を提示し、同じ注目箇所を拡大して大きな図解へ移るためのReact／Remotion部品です。動画1本やEP用の科学図解を完成させる作業ではありません。
全画面の画像・動画を差し込む設計で、背景写真を固定しません。付属SVGはすべて自作の配置検証用ダミーであり、実写写真やEP004の確定科学素材ではありません。

## 起動とレンダリング

リポジトリのルートで実行します。既存Remotion4.0.526、React18、Chromium、日本語フォントを再利用します。

```sh
npm ci
npx remotion studio src/extension/index.tsx
node tools/extension/render.mjs common_assets/nichijou_naze/layouts/v1.1.0/examples/footage-character.json
```

最後のコマンドの出力先は`out/extension/footage-character.mp4`。JSONを複製してID・素材パス・フレーム時刻を変更すれば別EPで再利用できます。動画背景は`background: {src: "episodes/EPxxx/shot.mp4", kind: "video"}`。無音で読み込みます。画像は`kind: "image"`または省略。`src`は`public/`以下の相対パス（`public/`自体は書かない）かアクセス可能なHTTPS URLです。遠隔素材よりローカル保存を推奨します。動画はシーン尺以上を用意し、開始位置の調整は元動画のトリムで行います。

IDから新規シーンを呼び出すCLIもあります。

```sh
node tools/extension/new-scene.mjs NNZ_TMP_LABEL_01 episodes/EP005/cut01.json overrides.json
node tools/extension/render.mjs episodes/EP005/cut01.json
```

`overrides.json`は差し替えたいトップレベル項目だけ指定します（例：`id`、`background`、`labels`）。配列とネストしたオブジェクトは項目全体を置き換える浅いマージです。既存シーンの上書きは拒否します。新しい背景では`protectedSubjects`・注目点・ラベル座標も対象物の位置に合わせて指定してください。

新規シーンを組み立てるときは`validateScene(config)`を呼び出してください。未対応バージョン・未制作ポーズ・不正時刻・主役の隠れ・字幕領域への侵入をエラーにします。既存1.0.1のCLIとJSONは変更していません。1.1.0用JSONは上記の専用コマンドで使います。

## 画面と共通演出

1080×1920、30fps。`FullFrameScene`は全画面背景と前景だけを表示します。`LabelOverlay`、`ArrowOverlay`、`Step3Overlay`、`CrossSectionOverlay`、`CharacterLayer`も個別にインポートできます。素材側に字幕・黄色帯・進行バーは含みません。

```tsx
import {EpisodeChrome} from './common_assets/nichijou_naze/runtime/v1.1.0/Chrome';
import {FullFrameScene} from './common_assets/nichijou_naze/runtime/v1.1.0/components';
// Remotionの親Composition内。ChromeはSequenceの外で1回だけ。
<EpisodeChrome totalFrames={episodeFrames} cues={voiceoverAlignedCues}>
  <Sequence from={cutStart} durationInFrames={config.durationFrames}>
    <FullFrameScene config={config}/>
  </Sequence>
</EpisodeChrome>
```

本編へ合成するときは既存の共通オーバーレイを親に1つだけ置きます。単体確認では`NNZ-FULLFRAME`が`EpisodeChrome`で包みます。外側に共通オーバーレイがある場合は`overlayOnly: true`をinputPropsで指定するか、`FullFrameScene`だけを使ってください。

`EpisodeChrome`は既存`SeriesFrame`と正式な`public/series/v1/opening_banner.png`を変更せず使用。字幕幅だけを1.1.0内に限定したCSSで824pxへ調整し、右端160pxを空けます。字幕はx96,y1500,w824,h240、下端1740。通常の帯は冒頭90f＋12fフェード。検証動画では干渉確認のため全尺表示します。
進行バーは親Compositionの全尺に同期し、Sequenceごとにリセットしません。0〜100%、秒数字・カウントダウンなし。字幕の読点「、」を除去し句点「。」を保持します。ナレーション同期は編集側から`{fromFrame,toFrame,text}`を渡してください。今回の検証字幕はダミーで、音声との同期実績ではありません。

前景セーフゾーンはx72〜920,y320〜1480。右端x920以降・字幕下端1740以降に重要情報を置きません。背景は全面に敷き、セーフゾーンのために背景を縮めません。プラットフォームUIや表示端末による差は各EPの最終QCで確認してください。

## IDと主要パラメータ

| ID | 主要指定 | サンプルJSON |
|---|---|---|
| NNZ_LAYOUT_FOOTAGE_01 | background、character、protectedSubjects | footage-character |
| NNZ_LAYOUT_DIAGRAM_01 | background、任意character、図解レイヤー | diagram-character |
| NNZ_LAYOUT_FOCUS_01 | focus、crossSection、background | focus-crosssection-return |
| NNZ_TMP_LABEL_01 | labelsの文字・点・矩形・色・時刻 | label-parameters |
| NNZ_TMP_STEP3_01 | steps[3]の文字・画像または図形・時刻 | step3-cause |
| NNZ_TMP_CROSSSECTION_01 | outside、parts、region | crosssection-carton |
| NNZ_MOTION_BASIC_01 | characterの登場・退場・うなずき・ポーズ | motions |

`layouts/v1.1.0/examples/`にJSON一式、`config.ts`に完全な型と検証関数、`schema.json`にJSON Schemaがあります。

### 全画面レイアウト

`background.src`の任意の画像・動画を`object-fit:cover`で全画面表示。`objectPosition`で構図を調整します。キャラが不要なら`character`を省略します。主役の画面上の矩形を`protectedSubjects`に指定すると、キャラ矩形との重なりを拒否します。差し替え背景の重要部分は必ずこの矩形も更新してください。被写体追跡や自動検出ではありません。

FOCUSでは`focus.target`はcover適用後の1080×1920上の注目点。24fで`zoom`倍に拡大し、中心をx540,y700へ誘導します。`revealFromFrame`から`revealFrames`で同じ部分を左→右へ断面表示し、`returnFromFrame`があれば30fで元の映像へ戻します。目印リングと境界線で説明箇所を保持します。前景画像と背景の形が連続するよう、拡大後の対象矩形と`crossSection.region`を揃えてください。付属氷サンプルは元x310,y500,w460,h500、1.5倍後x195,y325,w690,h750です。

### ラベル・3段階・断面

ラベルは`{id,text,anchor:{x,y},box:{x,y,width,height},fromFrame,toFrame?,color?}`。42px文字、短い文言を想定。12fで順次登場・退場。引き出し線は矩形の最も近い辺へ接続。文字と箱の幅の最終確認は実レンダーで行います。

STEP3はちょうど3項目、`fromFrame`をナレーションに合わせて個別指定します。46px文字と220px画像、各段330px。`image`があれば任意SVG/PNGに、なければ`shape: dots | inward | bubbles`の模式図に差し替えます。これらの記号は科学対象の実物形状や肉眼で見える溶存気体ではありません。EPでは台本と科学QCに合わせて図解を選んでください。前後を矢印でつなぎ、表示済み段階を残します。主領域を大きく使うためキャラは標準で非表示です。

断面は外観画像`outside`と透過レイヤー`parts[]`を共通キャンバス・同じ座標で用意します。レイヤーごとに開始・終了・不透明度を指定し、外観は断面の出現と同時に隠します。ラベル・矢印を別レイヤーで併用できます。検証は氷と紙容器の2形状で実施。形状を自動生成したり、物理的な切断・凍結を計算したりする機能ではありません。

### キャラクターと基本動作

`character.poses`は`[{fromFrame:0,pose:'neutral'},{fromFrame:65,pose:'talk'},...]`。V03追加3表情とV02既存5ポーズを明示的に解決します。旧5ポーズのPNG・manifest・既存キャラパス関数は不変です。

`side: left | right`、`height`、`top`で配置。`entry: fade | slide`、`enterFrame`、`exitFrame`、`transitionFrames`で登退場。`idle`は振幅3pxの上下動、`nodAt:[90,145]`は24fの約1.4度の軽いうなずき。ポーズ切替は10fのクロスフェードです。体全体を動かし、顔や手足を変形させません。クロスフェード中には短時間2ポーズが重なります。カットをまたぐリギングや本格的な口パク・歩行は未対応です。

### 旧テンプレートとの併用

`legacyOverlay`に既存ARROW／COMPARE／ZOOMのIDと既存形式の`config`を渡せます。元の1.0.1実装・拡大座標計算を再利用し、`mode:overlay,showTitle:false,characterVersion:v02_highres`で表示します。今回の合成アダプター内だけ0.9倍・左44px移動し、右端920px以内へ収めます。旧テンプレ本体や旧EPの出力は変更しません。旧テンプレに含まれるキャラの二重表示を防ぐため、同じシーンの`character`とは併用不可です。新しいラベル・矢印は前後のレイヤーとして独立に配置できます。旧テンプレのカード配置は維持し、新規の全画面標準とは区別します。

## バージョンと共有

既存V02は引き続き正式な5ポーズとして保持。追加表情は`characters/female_v01/versions/v03_expressions/`。新テンプレは`diagram_templates/*/1.1.0/`、レイアウトと実装はそれぞれ`layouts/v1.1.0/`と`runtime/v1.1.0/`。今後の更新は新しいバージョンディレクトリを追加し、既存EPの参照先を固定します。

GitHubのZIPには必要PNG・生成元・SVG・TSX・設定例・manifest・台帳・プレビュー・検証MP4・旧実装とフォント／帯を含めます。画像は各シーンの代表画面と推移の一覧を同梱し、検証した全36画面はGitHubの`validation/extension/`に保存しています。ZIP内の`PACKAGE_SHA256SUMS.txt`は同梱ファイル用、リポジトリの`HANDOFF_SHA256SUMS.txt`は過去成果物を含むリポジトリ全体用です。ChatGPT WorkはZIPを展開してREADMEを参照し、背景・台本同期時刻・対象矩形を差し替えて編集できます。node_modulesは含めず、npm ciで再現します。

Google Driveはこの環境に接続機能・認証がなく、ネットワーク許可先にも含まれないため未更新です。別のDriveフォルダは作成していません。
