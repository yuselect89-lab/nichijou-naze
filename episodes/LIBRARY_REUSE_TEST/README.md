# 別EPの再利用テスト

画像生成は0回。EP004由来の3Dコードを共通モデル1.1.0として独立登録し、既存v03キャラクター・ラベル・基本モーションを組み合わせています。

- `requirements.json`：制作前の必要素材リスト。
- `manifest.json`：使用するID・バージョン・表情・パラメータ・必要ファイル・再生方法。
- `view`：配置を中央からx12/y80へ変更、縮尺0.86。
- 3Dの`playbackRate`：1.2。形状・物理構造は変更していません。
- キャラは右側へ配置、考える→喜ぶ。全身スプライトのフェード・待機・うなずきのみ。
- 短い説明ラベルと矢印は既存runtime/v1.1.0を再利用。

```bash
node tools/library.mjs preflight episodes/LIBRARY_REUSE_TEST/requirements.json out/library/preflight.json --strict
node tools/library.mjs check episodes/LIBRARY_REUSE_TEST/manifest.json
node tools/library/render-reuse.mjs episodes/LIBRARY_REUSE_TEST/manifest.json
node tools/library.mjs export episodes/LIBRARY_REUSE_TEST/manifest.json /tmp/nnz-new-episode
```

別フォルダへ出力後：

```bash
cd /tmp/nnz-new-episode
npm ci
node tools/library/render-reuse.mjs episodes/LIBRARY_REUSE_TEST/manifest.json --locked
```

`asset-lock.json`で依存ファイルを照合。export先は未作成の別ディレクトリを指定してください。Node>=22、Chromium `/usr/bin/chromium`、ffmpegが必要です。素材側は一切再生成しません。初回の`--qc-candidate`は未登録モデルの検証専用で、通常制作には使いません。

この小型全身配置は読み込み・配置・ポーズ切替の機能検証専用です。本番標準にしません。新しい本編ではdocs/PRESENTER_DIRECTION.mdを読み、役割ごとの上半身クロップ・表情の読みやすさ・図解との干渉を別途QCしてください。
