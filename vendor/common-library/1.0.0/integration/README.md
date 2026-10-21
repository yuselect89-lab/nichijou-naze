# Remotionへの組込

既存の `bt-motion` (Remotion 4.0.526) を想定しています。既存Root.tsxは**上書きしません**。

1. `python tools/install_into_remotion.py --target /path/to/remotion-project` で素材とTSXコードをインストールします（デフォルトは既存ファイルを上書きしません）。
2. プロジェクトの `src/Root.tsx` にあるComposition群へ `NNZTemplates` を読み込んで配置します。
3. `integration/Root.example.tsx` は説明用のサンプルです。参照パスは実環境に合わせて調整してください。
4. `npx remotion studio` でコンポジションを確認後 `npx remotion render NNZ_TMP_ARROW_01 out/arrow.mp4` のように書き出します。

## 注意
- スプライトは小さな試作用透過PNGです。大きく拡大する場合は高解像度素材で差し替えてください。
- プレビューMP4は共通描画仕様を検証するための参考レンダリングです。最終Remotion書き出しと微小な差異があります。
- 台本・音声・焼き込み字幕を入れるのは本編組立時です。プレビューは無音です。
