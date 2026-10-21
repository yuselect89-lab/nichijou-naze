# NNZ_TMP_ZOOM_01｜拡大注目

**実装済（V1）**。元画像の注目ポイントに丸を表示し、拡大ルーペを出します。

- デモ設定：`example.json`
- 差し替え定義：`schema.json`
- Remotion実装：`template.tsx`（30fps、1080×1920向け）
- 確認動画：`preview.mp4`／代表フレーム：`thumb.png`
- 推奨尺：5秒

**注意**：highlight.x/yは0〜1。対象位置は画像の座標を測りながら微調整。

使用方法：対象位置、拡大率、ラベルを指定します。 `template.tsx` はRemotionプロジェクトの `src/` などから読み込みます。素材の参照パスは `public/common_assets/nichijou_naze/` に共通素材を配置した場合の表記です。
