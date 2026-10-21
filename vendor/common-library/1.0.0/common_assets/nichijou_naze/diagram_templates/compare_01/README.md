# NNZ_TMP_ZOOM_01｜左右比較

**実装済（V1）**。左右の対象物を入れ替えて違いを示します。

- デモ設定：`example.json`
- 差し替え定義：`schema.json`
- Remotion実装：`template.tsx`（30fps、1080×1920向け）
- 確認動画：`preview.mp4`／代表フレーム：`thumb.png`
- 推奨尺：5秒

**注意**：「○/×」は評価ではなく条件付きの差異表示の例。正解の意味は毎回確認。

使用方法：左・右の画像と見出しを差し替えます。 `template.tsx` はRemotionプロジェクトの `src/` などから読み込みます。素材の参照パスは `public/common_assets/nichijou_naze/` に共通素材を配置した場合の表記です。
