# 日常のなぜ？｜共通素材ライブラリ V1

このパッケージは **既存の制作プロジェクトとは別に管理可能な、Git登録用の独立ライブラリ**です。

## 現在の実体
- 女性キャラ：8ポーズの透過PNG実体あり（試作低解像度）
- 図解テンプレ：矢印／左右比較／拡大注目が実装済、各プレビューと設定を収録
- 部分ラベル／3ステップ／断面：**予約枠のみ・未実装**
- 男性キャラ／表情パーツ／口パク：**未実装**
- 共有素材台帳：`common_assets/nichijou_naze/management/asset_registry.xlsx` と `asset_registry.csv`

## 最初の操作
1. `index.html` をブラウザで開きプレビューを見る。
2. 使用する例を `diagram_templates/xxx/example.json` で確認する。
3. 既存Remotion制作リポジトリの `public/common_assets/nichijou_naze/` へ素材（画像類）をコピーし、`src/` 等から `.tsx` をimportする。
4. `integration/Root.example.tsx` にサンプルCompositionの登録方法を記載。

**ファイルパスの扱い**：Remotionの `staticFile` では `public/` 配下を参照します。リポジトリ内の実体は `common_assets/` なので、制作プロジェクトへの統合時には `public/` への同期が必要です。`tools/install_into_remotion.py` は既存ファイルを上書きしないコピー用の補助です。

## 運用標準
- 1080×1920、30fps、説明文の読点「、」は字幕に使用せず句点のみ残す
- 冒頭の黄色い帯 `秒で解決!!` を標準テンプレに含む
- キャラは説明を補助する。図解の主役・根拠を隠さない
- 作品ごとの画像・数値・ラベルは例から差し替える
- 人物・名称・実物の構造について正確性と権利確認を行う
- 原本データ、制作元、ライセンスを `manifest.json` と台帳に残す

## Git / Drive
- このフォルダを**独立したGitリポジトリ**にすることを推奨（既存Beyondとは別事業）。
- Google Driveは閲覧・バックアップ用（パッケージZIP副本）。
- このパッケージをGitHubへpushしたときに初めてリモート正本として扱う。ローカルZIPをGitHub保存済みとは呼ばない。
