# 日常のなぜ？ 制作入口

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
