# 女性解説キャラ v02_highres 納品記録

## 完成したファイル

保存先：`common_assets/nichijou_naze/characters/female_v01/`

| ファイル | ポーズ | 実寸 |
|---|---|---|
| `poses/NNZ_CHAR_FEMALE_01_pose_neutral.png` | 通常立ち | 1536×2304 RGBA |
| `poses/NNZ_CHAR_FEMALE_01_pose_talk.png` | 話す | 1536×2304 RGBA |
| `poses/NNZ_CHAR_FEMALE_01_pose_point_right.png` | 画面右へ指差し | 1536×2304 RGBA |
| `poses/NNZ_CHAR_FEMALE_01_pose_point_left.png` | 画面左へ指差し | 1536×2304 RGBA |
| `poses/NNZ_CHAR_FEMALE_01_pose_think.png` | 考える | 1536×2304 RGBA |

サムネイル5枚は `thumbs/`。元の描き起こしは `sources/v02_highres/`。全身高を約2160px、上下の透明余白を約72pxに統一。輪郭外の極小alphaと透明画素下RGBを整理しました。

## 解像度の記録

既存253px高の切り出しの拡大ではなく、資料を参照して高精細に描き起こした画像を整形したものです。生成元は通常1024×1536、thinkは887×1774。新しい描き起こしをトリミング・透過整理・Lanczos拡縮して1536×2304へ揃えています。ネイティブ2304px生成ではありません。生成元サイズ・切出し範囲・倍率をmanifestに残し、元の生成画像も保存しました。

## manifestと台帳

- キャラID：`NNZ_CHAR_FEMALE_01` を維持。
- 版：`v02_highres`。
- `manifest.json`：デザイン基準、生成元実寸、全ファイル名・解像度・透過・用途・加工方法・SHA-256・検証参照を登録。
- `versions/v02_highres/manifest.json`：版のスナップショット。
- `library-registry.json`：旧情報を `legacyCharacter` に保持し、現行の5ポーズを登録。
- `common_assets/nichijou_naze/management/asset_registry.json/csv/xlsx`：旧試作行を残して新版を追加。Active列で新版を明示。
- `index.html`：5ポーズの選択・透過PNG保存・背景切替を追加。GitHub Pages等のサイト公開はしていません。

## 実際の動画検証

`src/highres-validation/index.tsx` が再利用できる確認シーンです。

`validation/highres/character-layout-1080x1920.mp4` は1080×1920／30fps／840フレーム（28秒）の**無音検証動画**。既存動画を変更したものではありません。

1. 5ポーズを中央に1220px高で大表示。
2. 指差しを左右に寄せ、1100px高で配置。
3. 矢印・比較・拡大テンプレと共存させ、図解補助サイズ280px高で表示。
4. 黄色い既存帯と2行字幕を併用。
5. PNGの実alphaを画面位置へ投影し、帯／字幕領域への描画の重なりがないことを確認。
6. 全840フレームをデコード。ファイル破損・解像度・fps・フレーム数を検査。
7. 白・暗・チェック背景で透過端を目視。

結果：`validation/highres/qc-report.json`。画面一覧は `contact-sheet.jpg`、透過確認は `alpha-backgrounds.jpg`。個別スクリーンショットは `frame-*.png` です。

旧試作・vendor・過去の検証出力・旧ZIPの99ファイルをSHA-256で照合し、変更していません。別事業のBeyondには追加・変更していません。

## 今後のEPから使う

```json
{"characterVersion":"v02_highres","characterPose":"think"}
```

既存の `characterImage` があればそれが優先されるので、上の指定で使う場合はその明示パスを削除します。新規シーン作成CLIは優先5ポーズに新版を設定。既存のEP設定・examplesは自動移行しません。

ランタイムコピーは `public/common_assets/nichijou_naze/characters/female_v01/`。同期コマンドは `python tools/highres/install.py`。同一ファイルはスキップし、異なる既存画像は上書きしません。

## 残課題

優先5ポーズは完成・登録・画面検証済みです。静止画のtalkポーズであり、口パク・口形分離は含みません。少しの角度・表情差は残り、同一リグからの完全一致ではありません。元生成の実解像度は上記のとおりで、極端な4K拡大を想定していません。今回確認した全身高1200px前後以下の使用を推奨します。

次の候補は驚く・喜ぶ・困る。今回は必須5ポーズに集中し、それらの試作を高解像度版と偽って追加していません。
