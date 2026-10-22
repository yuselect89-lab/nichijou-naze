# EP006 素材インベントリ・再利用判定 V1

対象コミット（制作開始時）: `9fc3089e49a5c4add628120cc5e6c3e9423afd88`。HTTPS Gitで `main` と一致を確認。開始時の作業ツリーはクリーン。全追跡ファイルの開始時SHA256は `evidence/v1/baseline-sha256.json`。

正式帯: `npm run preflight` 成功。原本 `public/series/approved/opening_banner.png` のSHA256は `e6b63c322c996f543930a027db8981c2388e88441656655822c34bb4e2e2fd37`。検証のみで、素材には合成していない。

## reuse

| ID | 固定版 / 表情 | 実体・用途 | 検証 |
|---|---|---|---|
| NNZ_CHAR_FEMALE_01 | v03_expressions / think | `assets/v1/character-think.png`、CUT02 | resolve / 元PNG・全依存・QCハッシュ照合成功 |
| NNZ_CHAR_FEMALE_01 | v02_highres / point_right | `assets/v1/character-point.png`、CUT03 | 同上 |
| NNZ_CHAR_FEMALE_01 | v03_expressions / happy | `assets/v1/character-happy.png`、CUT07 | 同上 |

コピーは原本とバイト単位で同一。キャラの再生成・描き直し・表情の創作・反転なし。上半身表示はレンダリング時の等比拡大とビューポートで行う。`resolve-think.json` / `resolve-point.json` / `resolve-happy.json` に原パス、ファイルハッシュ、既存QC、rightsを保持。既存 `validation/extension/character-8poses.jpg` と原画像、今回の実レンダーを確認。

権利は台帳に従い「Original series assets and AI-assisted artwork」「商用利用は元サービス・依存ライセンス条件に従う」。新たな独占権や追加許諾を主張しない。フォントは既存 `NotoSansCJKjp-Bold-subset.otf` を無加工コピーし `FONT_LICENSE.txt` を同梱。

## blocked — 使用・再生成・再承認しない

| ID | 版 |
|---|---|
| NNZ_LAYOUT_FOOTAGE_01 | 1.1.0 |
| NNZ_LAYOUT_FOCUS_01 | 1.1.0 |
| NNZ_TMP_CROSSSECTION_01 | 1.1.0 |
| NNZ_TMP_ZOOM_01 | 1.0.1 |
| NNZ_TMP_LABEL_01 | 1.1.0 |
| NNZ_MOTION_BASIC_01 | 1.1.0 |

resolveはいずれも非ゼロ。具体的な理由は `changed:package.json; unbound:public/series/approved/opening_banner.png; changed:src/integration/v1.0.1/Series.tsx`。カタログの「検品済み」表示だけでは現行の実体検査を通過しない。エラー全文・終了コードは `evidence/v1/library-commands.json` と各 `resolve-*.json` に保存。これらをimportせず、登録ハッシュや共通実装を変更しない。修復・再承認は今回の範囲外。

## create — EP固有素材として制作

制作前の `search '指 皮膚 血管 断面'` と `search '水 湯 指先'` は候補0件。検索結果は証跡JSONに保存。指示書が許可する独自CG表現を採用し、外部写真・有料APIを利用していない。

| EP専用ID | 版 | 用途 / 実体 | 出典・使用条件 |
|---|---|---|---|
| EP006_BATH_FINGER_CG | 1.0.0 | CUT01/02/03/07、`assets/v1/Scene.tsx` の Finger / Droplet / 湯船 | 今回のオリジナルSVG/React。EP006制作・編集用。実写ではない |
| EP006_FINGER_SECTION | 1.0.0 | CUT04〜06、`assets/v1/geometry.ts` と Science | 今回のオリジナル模式図。承認済み台本・G2 V2の説明に対応。医学的実寸モデルではない |
| EP006_LABELS_BACKGROUND | 1.0.0 | `Scene.tsx` の背景・短文・リーダー | EP固有の編集レイヤー。共通テンプレートの複製・再生成ではない |

`requirements.json` のstrict preflightは終了コード2、reuse 3 / create 2 / blocked 0。新規素材が必要なため初回の `ready:false` を保持し、既存素材PASSに書き換えない。create判定後に上記EP専用ソースを制作・実レンダー・セルフQCした。共通素材に限定した `reuse_requirements.json` のstrict検査は成功。EP新作の実体検査は `manifest.json` と `evidence/v1/delivery-integrity.json`、個別QCは `ASSET_QC.md` を参照。

共通台帳への登録・カタログ再生成は行っていない。新作はEP専用に留める。汎用化する場合は独立QC・ID/版・候補登録から別途実施する。
