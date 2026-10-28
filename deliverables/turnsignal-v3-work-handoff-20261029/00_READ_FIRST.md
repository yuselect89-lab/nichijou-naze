# 「日常のなぜ？」ウインカー編 V3｜Work引継ぎ一式

2026-10-29。まず `01_WORK_EXECUTION_ORDER.md` を読み、`media/` のC01〜C06と `input/VOICE_MASTER.mp3` を使用する。

目的は、32.600813秒の正式ナレーションに素材を同期し、承認済み帯・字幕・進行バーを一度だけ合成したラフMP4を作り、G3実画QCへ進めること。公開・投稿はしない。

## 現在の状態

6カットの実MP4、背景/前景/表示補正レイヤー、Pythonソース、正式音声、承認済み帯原本、素材原本、代表フレーム、QC証跡を同梱。6カットの存在は本番合格を意味しない。C01のラッチ保持、C02の実在品外観照合、VOの意味に基づくカット同期、C06の「わざわざ」同期、全体G3が未検収。

`manifest.json` は素材の制作時記録。今回の編集入口はこの文書と `01_WORK_EXECUTION_ORDER.md`。過去の未取得音声・C01不合格の記録は履歴として含むが、正式音声は取得済み、新C01はmedia/C01_1080.mp4。REJECTED素材を本編へ採用しない。

## ファイル案内

- `media/C01_1080.mp4`〜`C06_1080.mp4`：使用する6カット、1080×1920、30fps、無音。
- `input/VOICE_MASTER.mp3`：正式音声、無加工。SHA-256 `59100d30d7aca0e0809f88479cad4a9a0aada35420ebb2353f9c32af37b8f1cd`。
- `brand/public/series/approved/opening_banner.png`：承認済み正式帯原本。
- `brand/production-lock.json` と `brand/docs/`：制作ロックと共通演出基準の同梱スナップショット。
- `layers/`：分離した補正・背景・前景・説明ラベル。mediaに合成済みの要素を二重に重ねない。
- `assets/`：既存承認キャラv02_highres、manifest、権利関連記録。
- `source/`：編集可能ソース。通常の初回ラフでは再生成不要。
- `previews/` と `evidence/`：実動画/実フレームと検査記録。
- `archive_history/`：旧不合格動画。制作には使わない。
- `QC_RESULT.md`：現行素材の限界と未検収範囲。
- `WORK_CUT_MANIFEST.csv`：編集用の仮タイムライン。
- `SHA256SUMS.txt`：同梱ファイルの照合用。

元のユーザー指示と明示承認を最優先とする。本パッケージは承認済み台本の代替ではない。全文台本/SRTは未同梱であり、音声から字幕を作る場合は実際の発話と一語ずつ照合し、未確認の文を捏造しない。
