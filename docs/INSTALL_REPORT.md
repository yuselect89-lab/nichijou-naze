# 導入記録

## 調査結果

- `/workspace/daily-why-ep003/`：Remotionで制作したEP003素材・ソース・仮タイミング。
- `/workspace/EP004_ICE/`：cut01〜10、manifest.json、PNG/SVG、カット別無音MP4、ChatGPT Work向けREADME。素材のみの方式。
- `/workspace/beyond-translation/`：別事業の既存Remotion制作環境。今回の導入先にはしない。過去のGitHub納品コピーも移動・削除しない。
- 日常のなぜ専用の統合Root／共通ライブラリ管理プロジェクトは未設置だったため、独立した `/workspace/nichijou-naze/` を新設。
- Node 24.19.0、Remotion 4.0.526、Chromium、ffmpegを使用。npm依存関係は独立ディレクトリに導入。既存node_modulesへのリンクは使用しない。

## 追加ファイル

- `package.json` / `package-lock.json` / `tsconfig.json` / `.gitignore`：独立環境。
- `vendor/common-library/1.0.0/**`：添付ZIPを安全に展開した変更しない原本。
- `public/common_assets/nichijou_naze/**` / `src/common_assets/nichijou_naze/**`：既存installerで新規コピーした画像・原本TSX、15ファイル。上書きモード不使用。再実行は copied=0 / skipped=15。
- `public/series/v1/**`：既存EP004の帯と日本語フォント／ライセンス。帯PNG/SVGは同一内容をコピー。日本語フォントはホストのNoto Sans CJK JP Boldを同梱。
- `src/integration/captions.ts` / `src/integration/v1.0.1/**`：導入用アダプタと字幕・全尺進行バー。
- `src/Root.tsx` / `src/index.tsx`：独立Remotion登録。元Rootの上書きなし。
- `examples/**` / `library-registry.json`：呼出設定、版、8ポーズ、原本ハッシュ。
- `tools/**` / `tests/**`：呼出・非上書きインポート・レンダー・検査。
- `validation/**`：今回の実レンダーと計測。既存EPの完成動画ではない。
- `docs/**` / `README.md`：引渡し・調査・運用仕様。
- `episodes/INTEGRATION_TEST/**` / `public/episodes/INTEGRATION_TEST/**`：差し替えCLIの実動確認用。実EPの原稿ではない。

既存のEP003／EP004の148ファイルを導入前後でSHA-256照合し変更なし。Beyondの作業ツリーも変更なし。添付ZIP原本は `library-registry.json` のファイル別ハッシュで照合。

## 実装時に対応した点

1. `_` 入りの元Composition名はRemotion実行時に拒否される。設定のテンプレIDを維持して登録名だけハイフンに変更。
2. 元のキャラ下端・Zoomラベルが字幕領域に重なるため、導入版でy=1470までに収めた。
3. 元Compareのpadding/borderによる実幅超過をborder-boxで修正し、左右幅・余白を対称にした。
4. Zoomは実画像の縦横比とobject-fitの余白から注目点を計算し、ルーペ内で縦横比を変えない。
5. 帯・進行バー・字幕はSeriesFrameに集約。overlayには含めない。進行バーは本編フレーム／本編総フレームで算出。
6. Remotionの初期非表示DOMや画像読込前の幅0を誤計測しないよう、検査は画像・フォント読込後にキャンバス相対座標を測る。実レンダーの可視配置で判定。

## 検証

`validation/qc-report.json`、`validation/render-observations.json`、検証MP4と一覧画像を参照。3テンプレ、途中からの合成、本編字幕、全尺進行バー、透過overlay、差し替えCLIの実出力を検証。実VOは未支給のため実声との同期は未検証。表示制御は明示したフレーム範囲の日本語検証字幕で確認。

## 未完了・制約

- 専用GitHubリポジトリURL待ち。新規作成APIはHTTP 403。Beyondへのアップロードはしない。
- メッセージに表示される丸型・約30入りの帯は元ファイルがZIPに未収録。既存EP004帯を再利用済み。
- 女性キャラは試作解像度。男性版・口パク・表情分離・予約テンプレ3種は元から未制作であり、今回追加しない。
- 既存動画の変更・公開、本番内容や科学・権利の承認は実施していない。
