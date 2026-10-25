# 日常のなぜ？ カップヌードル回｜2026-10-25 再開用復旧パッケージ

## 判定
**PARTIAL RECOVERY / NOT ORIGINAL G2 PACKET**。ChatGPTの2026-10-24 JST過去会話の検索から台本7文と承認の経緯、V2の6カットの役割、Gemini G2の主要指摘を回収し、Codexが読める実ファイルへ保存した。**当時の映像設計V2全文とG2判定原文全文、確定VOファイルは発見できていない。**

このフォルダはかつての原本に偽装するものではない。新規設計の箇所を「再構成」と明記する。台本の句読点・字幕の最終表記はユーザー確認のうえLOCK維持。字幕と音声が存在しない場合、勝手に代用しない。

## ファイル
- `01_SCRIPT_V2_RECOVERED.md`：会話履歴から回収した日本語台本7文、会話の承認記録
- `02_G2_EVIDENCE_AND_DELTAS.md`：Gemini G2の回収できた判定概要とCUT修正差分。**Gemini原文の完全な転記ではない**
- `03_STORYBOARD_V2R_PROPOSED.md`：回収した6カットの役割を踏まえて作り直した制作可能性検証用絵コンテ。**当時のV2原本ではない**
- `04_CODEX_RESTART.md`：Codexが実行できる範囲、preflight、QC、停止条件

## 承認と権限
2026-10-24 JST 01:03頃のユーザー「どうぞ」を受け、ChatGPTが台本V2をLOCKした履歴がある。映像設計V2は同日01:16頃に提示された。現在のV2Rは当時の映像設計V2全文の完全復元ではなく、原設計との差が残る可能性があるため**デザインの最終G2再審査待ち**。このブランチ上のファイル作成はmainを変更しない。

## 実在リポジトリ正本
`AGENTS.md`、`production-lock.json`、`docs/PRODUCTION_LOCK.md`、`docs/VISUAL_QUESTION_DIRECTION.md`、`docs/PRESENTER_DIRECTION.md`、`docs/WORK_HANDOFF.md`、`library-registry.json`。帯は承認原本`public/series/approved/opening_banner.png`のSHA256 `e6b63c322c996f543930a027db8981c2388e88441656655822c34bb4e2e2fd37`のみ。旧帯禁止。女性キャラは登録済み高解像度原本から。字幕は「、」だけ削除、「。」保持。単一進行バー・字幕・帯を本編親コンポジットで各1回。

## 制作停止条件
- `node tools/verify-production.mjs` / `npm run preflight` に失敗
- 見つからない原音声を別声で無断生成しようとする
- 低品質2D・静止画ズームへの縮退
- 確定していない尺や字幕タイムスタンプを「LOCK」と誤記
- モデル品質が低い、構造が誤る、G2未承認なのにREADY宣言
- 無断有料API・課金、BGM/SE追加、公開、push/merge

公式科学根拠：日清食品 https://opensearch.www.nissin.com/jp/about/history/ および https://www.nissin.com/jp/company/ir/library/report/pdf/knt_110930_01.pdf
