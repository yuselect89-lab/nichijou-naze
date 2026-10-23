# 映像品質の再現性検証（試験導入・2026-10-23）

次の新規EPから、下記を既存の制作フローに追加する。詳細は `docs/VISUAL_PDCA_STANDARD.md`。元の制作仕様・原本・G2/G3を変更・省略しない。

- ChatGPT（設計）は企画時に視聴者が「何を見てなぜ理解するか」を記述する。形式だけ合う図解や、使途のないCGを採用しない。CGは本編で利用可。冒頭は題材の現象を直感的に認識できる映像とする。
- Codex（素材）は共通台帳を確認し、核心となる数秒の動きを先に試作。実動画を見て形状の破綻・装飾の過剰・図解の見やすさを確認してから量産する。試作の不合格理由を残す。
- Work（合成）はLOCK音声・正式帯・字幕・単一進行バーを正本通りに合成する。書き出し直後に `npm run preflight` と `npm test` と `python3 tools/visual_pdca_qc.py --config episodes/<EP>/visual_pdca_case.json --out episodes/<EP>/visual_pdca_report.json` を実行し、失敗は隠さない。
- 技術検査のPASSは、視覚品質・ナレーションとの整合・外部Gemini G2/G3のPASSを意味しない。ユーザーに初歩的な不具合検出を依存せず、映像の実物を音声あり・なし・360pxで見る。
- 初稿の修正回数、仕様違反件数、G2/G3判断を次の2〜3EPで計測し、EP006のみで安定再現を断定しない。

---

# 最優先：制作仕様ロック（2026-10-22）

新規EPの制作・編集・ラフMP4・最終書き出し・素材納品の前に、必ず `production-lock.json` を開き、`node tools/verify-production.mjs` を実行する。非ゼロ終了なら作業を止める。元ファイルは2026-10-22に承認済みで登録された。無断加工・別素材への置換は禁止。

- **正式帯の判断根拠はChatGPTの記憶・過去のプロンプト・本ファイルの古い説明ではない。** `production-lock.json` と実ファイルの SHA256 が一致することだけが機械的な承認条件。
- `public/series/v1/opening_banner.png` は旧流用画像であり、正式帯として使わない。EP005の「秒で解決!!」という誤った文言指示は撤回する。
- 正式元画像は `public/series/approved/opening_banner.png`。`production-lock.json` に記録された SHA256 に一致する場合のみ使用可能。不一致・欠落・未承認なら制作を停止する。
- 背景・キャラ・図解・音声などは既存の登録台帳・原本から検証して再利用。共通素材を無断上書きせず、仕様変更は明示承認・版更新・差分テストを必要とする。
- 本編には正式帯・単一進行バー・字幕を一度だけ合成。字幕は読点「、」のみを除去し、句点「。」を残す。
- 変更方法と再確認事項は `docs/PRODUCTION_LOCK.md` に記載。

---

# 日常のなぜ？ 制作入口

**問いの冒頭は映像優先で設計する。** 必ず `docs/VISUAL_QUESTION_DIRECTION.md` を読み、実物・動作・短い語句・視覚的な意外性の組み合わせを検討する。長い問いの文章をそのまま巨大なテロップにすることを標準にしない。黄色い正式帯は `production-lock.json` の承認済みPNGを変更せず別レイヤーで維持する。素材の実在と台本・VOのLOCKを検査し、G2/G3では冒頭の視覚的理解とキャラの役割を確認する。

この専用リポジトリの新規制作・修正は、最初に `docs/WORK_HANDOFF.md` と `docs/PRESENTER_DIRECTION.md` を読む。

女性キャラは案内役。表情が読める上半身の問いかけ・反応・締めと、現象に集中する図解場面を設計する。小さい全身キャラを常時隅で動かすだけの配置を本番標準にしない。既存コードの小さい初期値をそのまま最終配置に採用しない。

素材制作前に登録台帳と実体・版・依存・プレビューを検証し、再利用を優先する。背景・ラベル・キャラは分離して納品し、正式帯・単一進行バー・字幕を本編側で一度だけ合成する。字幕は読点除去・句点保持。360px幅の動画で表情・図解・UIとの干渉を検品し、G2/G3にもキャラ演出の確認を含める。

ユーザーの最新の明示指示を優先し、承認済み台本・音声の変更や投稿は依頼範囲内で行う。

---

# 日常のなぜ？ 制作時の共通素材運用

このリポジトリは「日常のなぜ？」専用。Beyond Translationの事業素材を混在させない。

新しいEPの素材制作では、画像生成や素材の新規作成を始める前に必ず次を実行する。

1. `node tools/library.mjs search <用途>` で既存素材を確認する。EPの氷写真等が必要な場合は `--include-episode`。
2. `episodes/<EP>/requirements.json` を作り、`node tools/library.mjs preflight <requirements.json> <report.json> --strict` を実行する。needsの形式は `episodes/LIBRARY_REUSE_TEST/requirements.json` を参照。
3. `reuse`は再生成しない。`adapt`は元を保存し、新バージョンとQCを用意する。`create`の項目だけを新規制作候補にする。`blocked`は実在・版・QC・入力を修正し、見つからないと決めつけて新規生成しない。
4. 各manifestにIDとバージョンを固定し、`node tools/library.mjs check <manifest.json>` を通す。暗黙の最新版へ置換しない。
5. 新規の汎用素材は `candidate` で未検品登録し、実際に描画・再生・権利・依存を確認する。検品後に `register <candidate-manifest> <QC-report>`。同一ID/版の上書きは禁止。
6. `catalog.v1.json`、`catalog.html`、`CATALOG.md`は派生物。手で別台帳を作らず `node tools/library.mjs catalog` で更新する。
7. 別EPへ `export` し、依存を含む `asset-lock.json` と再生方法を渡す。元EPがなくても共通素材を使えることを確認する。

ライブラリ保守・候補QC自体は新規EP制作とは別の検証工程。`--qc-candidate`は検品専用で、本番利用のQCゲートを回避するために使わない。

既存EP、旧バージョン、納品済みZIPは変更しない。帯・全編進行バー・字幕の責務を既存本編レイヤーから分散させない。字幕は読点「、」を除き句点「。」を残す。
