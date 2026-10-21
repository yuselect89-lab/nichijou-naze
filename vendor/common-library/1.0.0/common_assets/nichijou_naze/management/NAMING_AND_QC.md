# 命名・QC・追加ルール V1

- 共通アニメーション：`NNZ_TMP_ARROW_01` / `NNZ_TMP_COMPARE_01` / `NNZ_TMP_ZOOM_01`
- 追加予定：`NNZ_TMP_LABEL_01` / `NNZ_TMP_STEP3_01` / `NNZ_TMP_CROSSSECTION_01`
- 女性キャラ：`NNZ_CHAR_FEMALE_01`、男性キャラ予定：`NNZ_CHAR_MALE_01`
- 小道具：`NNZ_PROP_PETBOTTLE_01` / `NNZ_PROP_MILKCARTON_01`
- 回固有：`NNZ_EP004_ICE_CUT03`
- バージョン：`asset_id` は不変、`revision` を `1.0.0` → `1.1.0` に更新、元ファイルを保持
- 共通化の基準：別回でも使える、繰り返し使う見込みが高い、再制作負荷が高いもの
- 予約枠は `status=planned` と記載し、プレビューは作らない
- 受入：正方形等でなく9:16、1080×1920／30fps、帯・余白・文字可読性、素材権利、科学説明の正確性
- 検証手順：コード構文、schema、デモプレビュー、実尺、基本表示、実声・字幕との同期、Gemini G3動画QC
- 本番の正解ラベルや断定文は元資料で検証してから確定すること
