# 日常のなぜ？ 共通素材ライブラリ拡張 V1 納品報告

## A：再利用した既存素材・実装

- 女性キャラV02高解像度5ポーズ（通常・話す・右指差し・左指差し・考える）。旧試作8ポーズは資料として保存。
- 矢印・左右比較・拡大テンプレの1.0.1実装。新アダプター内のみ0.9倍・左44pxで右端のUI領域を確保。
- 正式な黄色帯`public/series/v1/opening_banner.png`。元PNGは変更せず共通オーバーレイで1回表示。
- 既存SeriesFrame、全編尺の進行バー、字幕の句読点処理、日本語フォント、Remotion4.0.526／30fpsの環境。
- 口・手足の独立パーツは存在せず、利用可能として登録していません。

## B：新規制作して動作検証したもの

| ID／版 | 内容 | 保存先（common_assets/nichijou_naze/以下） |
|---|---|---|
| NNZ_CHAR_FEMALE_01 / v03_expressions | surprise・happy・troubled 各1536×2304 RGBA PNG、サムネ、生成元、manifest | characters/female_v01/versions/v03_expressions/ |
| NNZ_LAYOUT_FOOTAGE_01 / 1.1.0 | 全画面画像／動画＋任意キャラ、主役の保護矩形 | layouts/v1.1.0/ |
| NNZ_LAYOUT_DIAGRAM_01 / 1.1.0 | 大きな図解＋任意キャラ。キャラなしでも成立 | layouts/v1.1.0/ |
| NNZ_LAYOUT_FOCUS_01 / 1.1.0 | 同一注目点の拡大→断面のワイプ→元の実物へ戻る | layouts/v1.1.0/ |
| NNZ_TMP_LABEL_01 / 1.1.0 | ラベル・引き出し線、位置・色・文字・開始／終了時刻 | diagram_templates/label_01/1.1.0/ |
| NNZ_TMP_STEP3_01 / 1.1.0 | 3段階の順次表示、画像／図形／文字の差し替え | diagram_templates/step3_01/1.1.0/ |
| NNZ_TMP_CROSSSECTION_01 / 1.1.0 | 外観・内部を共通キャンバスのレイヤーで制御 | diagram_templates/crosssection_01/1.1.0/ |
| NNZ_MOTION_BASIC_01 / 1.1.0 | フェード／スライド登退場、3px待機、軽いうなずき、10fポーズ切替 | animation/basic_01/1.1.0/ |

実装は`common_assets/nichijou_naze/runtime/v1.1.0/`に集約し、個別manifestから参照します。`tools/extension/new-scene.mjs`でテンプレIDと差し替えJSONを指定して呼び出せます。`tools/extension/render.mjs`で素材シーンを出力できます。

### キャラクターの実寸・生成と加工

新規3枚の生成元はすべて1024×1536pxです。元253px試作の単純拡大ではありません。V02通常立ちを参照して新たに表情・ポーズを描き起こし、微小アルファを除去し、ほぼ不透明な画素を正規化。外周をクロップし、全身2160px・足元2232pxを基準に1536×2304の透過キャンバスへ配置しました。拡大倍率・元実寸・処理内容・ハッシュはV03 manifestに記録し、加工前生成元も残しています。

ファイルは`NNZ_CHAR_FEMALE_01_pose_surprise.png`、`NNZ_CHAR_FEMALE_01_pose_happy.png`、`NNZ_CHAR_FEMALE_01_pose_troubled.png`です。V02の5枚とそのmanifestは変更していません。V03 resolverから参照することで全8ポーズを利用できます。

### 実レンダーQC

- `validation/extension/library-extension-1080x1920.mp4`：78秒・2340フレーム、1080×1920／30fps、H.264、無音。
- `validation/extension/video-background-1080x1920.mp4`：4秒・120フレーム。同じ解像度で動画背景の読み込みとキャラ合成を検証。
- 36枚の実レンダースクリーンショット、13の検証シーンと追加1つの動画背景シーン。
- 追加3表情の大表示・小表示、旧5ポーズとの一覧比較、白／暗色／チェック背景上のアルファを目視確認。
- 拡大→断面→実物の推移を9時点で確認。氷と紙容器の2形状でレイヤー差し替え、表示・非表示を検証。
- キャラ登退場・うなずき・待機・ポーズ切替、ラベル位置・色・時刻変更、3段階の順序を確認。
- 帯・字幕・進行バーの二重表示なし。字幕の読点を除去し句点を保持。進行は親の2340f全尺に対応し、先頭0・末尾100%でカットごとに戻らないことを確認。
- 右端・下部のセーフゾーン、キャラの実アルファ領域、図解と字幕の位置をDOM観測で照合。既存ファイル162点のSHA-256一致を確認。
- 両MP4を全フレームデコードしてエラーなし。テスト17件とTypeScriptチェックを実施。

QCの機械記録・実寸・対象ファイルハッシュ・制限事項は`validation/extension/qc-report.json`。背景は自作の検証用SVGとその動画で、実写写真の代用テスト素材です。実際のEPの科学表現やナレーション同期まで合格したという意味ではありません。

### 更新した管理情報

- `library-registry.json`：1.1.0拡張・新3図解・V03の追加登録。既存の正式V02指定を維持。
- `common_assets/nichijou_naze/management/asset_registry.json / .csv / .xlsx`：V03・レイアウト3・図解3・動作1の8行を追加。旧版の行も保存。
- 各版manifest：ID・版・保存場所・用途・必要パラメータ・サンプル・プレビュー・QC参照を登録。
- 共通プレビュー`common_assets/nichijou_naze/runtime/v1.1.0/preview.html`、8ポーズ一覧と全画面コンタクトシートを追加。
- 既存EP・過去レンダー・旧キャラ素材・別事業リポジトリは変更していません。新しい公開サイトも作っていません。

## C：制作したが本番利用できないもの

今回の必須制作物に該当なし。静止表情と全体モーションには次の制限があります。

- 描き起こしごとに頭の角度・陰影に軽い差があります。完全に同じ顔を固定したリグではありません。
- 口パク・手足の独立運動・歩行は提供していません。うなずきは体全体の微小回転です。
- ポーズ切替では10fの間2枚が重なります。滑らかな関節アニメーションへのモーフではありません。
- 新しい実写背景を使うときは対象矩形・注目点・断面位置を合わせて再QCしてください。自動被写体追跡はありません。
- 本番のVOが未提供のため、字幕・段階の開始時刻は編集側で同期してください。検証字幕を本番へ流用しないでください。

## D：未実施・今後の候補

- Google Driveへの同期は未実施。この環境にDrive接続・認証がなく、指定ホストもネットワーク許可先ではありません。指定フォルダのアクセス権を確認できないため、更新や代替フォルダ作成は行っていません。
- 本格的な口パク、関節リグ、歩行、顔の厳密な共通パーツ化は今後の候補。今回の必須範囲外です。
- 実際のEP素材との構図調整とVO同期・最終動画QCは今後の制作時に行います。

## ChatGPT Workへの受け渡し

GitHubリポジトリ`yuselect89-lab/nichijou-naze`の`releases/NNZ_COMMON_LIBRARY_EXTENSION_v1.1.0.zip`をダウンロードしてください。展開後のルートから`npm ci`、`npx remotion studio src/extension/index.tsx`で確認できます。素材だけ必要な場合は`releases/NNZ_CHAR_FEMALE_01_v03_expressions.zip`に新規3ポーズと生成元・サムネ・manifest・8ポーズの比較画像をまとめています。V03キャラ単体ZIPには継承元の旧5ポーズは含めず、既存V02ライブラリと併用します。

詳しい使い方、パラメータ、親オーバーレイと素材単体の分離は`common_assets/nichijou_naze/runtime/v1.1.0/README.md`をご覧ください。
