# 氷の共通プロップ V1.0.0

9件のIDを登録。画像とThree.jsシーンの資源セットであり、既存テンプレを置き換えません。

```bash
node tools/ice-assets.mjs NNZ_MODEL_ICECAN_DRAIN_01
node tools/ice-assets.mjs NNZ_PROP_ICE_COMPARE_PHOTO_01
```

`manifest.json` のsourceはリポジトリルート基準。ソースを二重管理せず、版を固定したEP004_ICE_V3へ参照しています。EP004_ICE_V3/sourceとpublic/ep004-v3を一緒に維持してください。

3D APIはcanvasを渡して生成し、draw(frame,mode)で更新、終了時dispose()。mode=background/modelで背景と透過モデルを分離可能。frameは30fpsのローカル時刻。型・配色等を変更する場合は新バージョンを作成。サイズと形の基準は各ソースに明記。

キャラクターは既存v02/v03、ラベルと図解を重ねる場合は既存runtime/v1.1.0を使用。帯・字幕・進行バーは本編側へ一度だけ配置。

写真はAI再現。模式図は気泡寸法や凍結速度を実測として使わない。公式参考ページの再取得とG3は別途必要。
