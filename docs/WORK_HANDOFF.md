# ChatGPT Work 引渡し

**保存先：`/workspace/nichijou-naze/`。Beyond Translationの制作プロジェクトには入れない。**

1. この独立プロジェクトを使用し `npm ci`。既存EP003/EP004を移動・変更する必要はない。
2. `library-registry.json` と `examples/` からテンプレIDと版を選ぶ。利用可能なのは女性8ポーズ、矢印、左右比較、拡大の3種類。その他は予約枠。
3. `node tools/new-scene.mjs --template <ID> --image <差し替え画像> --pose <ポーズ> --out episodes/<EP名>/<Cut名>.json`。比較の場合は `--left` と `--right`。同名ファイルは上書きしない。
4. 各図のラベル・矢印の端点・拡大対象をJSONで調整。実体は原本ではなく導入版1.0.1を使う。
5. 素材MP4単体は `npm run render -- <設定JSON> <新しい出力名.mp4>`。
6. 本編のReact合成には `TemplateScene config={{...config,mode:'overlay'}}` を使う。帯・進行バー・字幕は本編側で一度だけ描く。透過を保持したい場合、H.264の単体MP4を本編へ貼らず、Reactレイヤーか透過PNGを使う。
7. 字幕のフレームは確定VOに合わせる。SeriesFrameのcue範囲は**本編のグローバルフレーム**。Sequence内の局所フレームを渡さない。読点除去と句点維持は共通処理で行う。
8. 従来のEPの `manifest.json` にテンプレID・版・設定参照・書出し素材名・仮尺をカット単位で追記する。既存のキーを置き換えない。例は `docs/manifest-cut-example.json`。

## 検証プレビュー

- `validation/arrow.mp4`：矢印テンプレ 150フレーム。
- `validation/compare.mp4`：左右比較 180フレーム。
- `validation/zoom.mp4`：拡大 150フレーム。
- `validation/parent.mp4`：360フレームの**検証用本編**。90フレームから180フレームの比較を合成。既存動画ではない。
- `validation/overlay-transparent.png`：帯・進行バー・字幕を持たない透過合成レイヤー。
- `validation/cli-import.mp4`：差し替えCLIで生成した設定とthinkポーズの実出力。

実VO・実EPの言語内容・科学的妥当性・本番権利の承認は今回の検証に含めない。キャラは試作解像度で、拡大用の高解像度版・口パク・男性版は未制作。

## 黄色い帯

EP004で使った既存PNG/SVGをそのまま再利用。テンプレ原本内のCSS黄色帯を重ねてはいない。メッセージ添付に見える丸型・約30入りの画像は元ファイルとしてZIPに含まれていないため、この導入では置換していない。元の画像を使う場合は、その実体を新しい版の共有素材として追加し、過去版を残す。

## GitHub

専用リポジトリで管理する。Beyond Translationへpushしない。現時点でGitHub APIへのアクセスは403のため、環境からの新規作成は不可。空の非公開リポジトリのURLを受領後、HTTPS Git経由でアクセスを確認してからこの独立リポジトリをpushする。APIの403だけで既存HTTPS Git認証が無効とは判断しない。トークンをチャットへ貼らせない。
