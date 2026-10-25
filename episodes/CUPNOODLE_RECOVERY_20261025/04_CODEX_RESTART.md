# Codexへ：カップヌードル回の復旧後作業

## 入口
ブランチ `recovery/cupnoodle-20261025` の `episodes/CUPNOODLE_RECOVERY_20261025/`。mainと既存EPに対する上書き、merge、pushは禁止。まずREADME、台本、G2差分、V2R絵コンテを全部読む。**前回の『何も見つからない』状態は、今回この4ファイルの新規保存で一部解消した。**

## ①原本と登録素材を最初に検査（無課金）
- `AGENTS.md`、`production-lock.json`、`docs/WORK_HANDOFF.md`、`docs/PRODUCTION_LOCK.md`、`docs/VISUAL_QUESTION_DIRECTION.md`、`docs/PRESENTER_DIRECTION.md`、`library-registry.json` を開く。
- `node tools/verify-production.mjs`、`npm run preflight`、`npm test` を実行。どれか失敗→HOLDしログ保存。正式帯SHA256と原本実ファイル検証。
- `node tools/library.mjs doctor`、`node tools/library.mjs search カップ`、`node tools/library.mjs search 麺`、`node tools/library.mjs search 断面`、`node tools/library.mjs search water` 等を実施。登録台帳、実ファイル、依存、権利、プレビュー、再生を照合。
- 専用 `requirements.json` を作り、ライブラリ `preflight <requirements> <report> --strict` を実施。strictでcreate/blockedの場合の終了コードは失敗扱いではなく、それぞれの不足品の判断材料。**blocked素材は勝手に生成せず報告**。
- 共有素材は reuse/adapt/create/blocked に分類。adaptと新作はEP側で新バージョン・QC後のcandidate登録。初めから本ライブラリ原本を上書きしない。
- VO既存実ファイルを探索し、存在/尺/ハッシュを報告。なければ `VO_NOT_FOUND`。未承認でElevenLabs生成しない。

## ②現時点で許可される作業
読み取り、正本の整合性検査、登録済み高解像度キャラのレイヤー配置検査、**モデルの構造・質感・対流表現が成立するかを示すローカル無課金QC用プロトタイプ**。本編動画、最終納品素材、量産、外部課金、公開、main改変は禁止。V2Rの新規設計部分はG2再確認とユーザー承認待ち。

試作品はEP固有の `output/PROBE_20261025/` に限定し、全カット完成を宣言せず、(A) 側面接触が読める3D静止検証、(B) 注湯→底空間→周り込みの短い**実動作**検証を提出。簡易棒とラベルで誤魔化した見た目なら自己FAILとする。

## ③報告書（必須）
`SOURCE_RECONCILIATION.md`：会話から回収済み台本7文、ユーザーの「どうぞ」、G2主要修正、未取得の「当時の原V2/G2全文・VO」を明確に区別。
`ASSET_REUSE_DECISIONS.md`：素材ごとに資産ID、版、実在、ハッシュ、権利、依存、QC、判断、保存先。
`PROBE_QC.md`：実ファイル、レンダリング条件、解像度、360px判定、破綻の実例。FAILなら素材不採用。
`UNBLOCK_MATRIX.md`：台本 RECOVERED / V2R G2 WAIT / VO NOT_FOUND or VERIFIED / material probe PASS or FAIL / PRODUCTION HOLD or READY。

## 引き渡し条件
独立G2でV2R承認、ユーザー映像設計の承認、正本ハッシュと素材QC合格、VOと秒数同期が揃ったときだけ次の全カット制作工程へ。作業・課金・音の独断変更は禁止。
