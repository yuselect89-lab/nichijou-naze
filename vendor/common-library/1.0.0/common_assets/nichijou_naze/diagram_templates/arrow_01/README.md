# NNZ_TMP_ZOOM_01｜矢印説明

**実装済（V1）**。図や商品写真に「方向・圧力・流れ」を順に表示します。

- デモ設定：`example.json`
- 差し替え定義：`schema.json`
- Remotion実装：`template.tsx`（30fps、1080×1920向け）
- 確認動画：`preview.mp4`／代表フレーム：`thumb.png`
- 推奨尺：5秒

**注意**：矢印端点は1080×1920キャンバス上のピクセル座標。

使用方法：矢印の開始・終了座標を設定して画像を差し替えます。 `template.tsx` はRemotionプロジェクトの `src/` などから読み込みます。素材の参照パスは `public/common_assets/nichijou_naze/` に共通素材を配置した場合の表記です。
