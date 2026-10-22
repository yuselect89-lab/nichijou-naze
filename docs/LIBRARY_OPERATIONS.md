# 日常のなぜ？ 共通素材ライブラリ 運用V1

既存の `library-registry.json` と各素材manifestを正本にし、現行の素材台帳JSON/CSV/Excelへ版単位で追記します。検索用の別データベースは作りません。

- [GitHubで見られる素材一覧](../common_assets/nichijou_naze/management/CATALOG.md)
- [検索画面](../common_assets/nichijou_naze/management/catalog.html)（ダウンロード後にHTMLを開く）
- [別EPのテスト](../episodes/LIBRARY_REUSE_TEST/README.md)
- [検査結果](../validation/library-ops/final-report.json)

## 実行環境

検索・照合はNode.js >=22。レンダリングは既存のRemotion4.0.526、Chromium、ffmpegを利用。Excel台帳の更新はPython3とopenpyxl3.1.5が必要です（`python -m pip install -r tools/library/requirements.txt`）。バックアップと復元はPython標準ライブラリだけで動きます。

本番制作では、既存の[制作引き渡し](WORK_HANDOFF.md)と[女性キャラ演出基準](PRESENTER_DIRECTION.md)を先に読みます。今回の360px全身表示はAPIの機能検証専用で、本番の推奨配置やG2/G3合格例ではありません。問い・反応・締めでは原本から表情の読める上半身を配置し、現象の核心は図解に譲ってください。

## 次回制作時

```bash
node tools/library.mjs doctor
node tools/library.mjs search 考える
node tools/library.mjs search '光 散乱'
node tools/library.mjs search 氷 --include-episode
node tools/library.mjs resolve NNZ_CHAR_FEMALE_01 v03_expressions think
node tools/library.mjs preflight episodes/LIBRARY_REUSE_TEST/requirements.json out/library/preflight.json --strict
node tools/library.mjs check episodes/LIBRARY_REUSE_TEST/manifest.json
```

`AGENTS.md`に制作前の照合を必須手順として登録しました。preflightは必要素材を構造化したneedsリストから検索します。自由文を完全に理解する自動エージェントではないため、用途を「光 散乱」のような短い語、またはIDで指定してください。

- **reuse**：版・実ファイル・SHA256・QC・表情・パラメータを検証。既存素材を利用。
- **adapt**：既存候補で不足する能力がある。元を残し新しい版を制作・QC。
- **create**：検索で一致する素材がない項目のみ。新規制作候補。
- **blocked**：版不足・ファイル変化・未検品・不正入力。勝手に作り直さず解決。

`--strict`はreuse以外があれば終了コード2。制作の実行は止めます。通常のテストレンダラーもpreflightと最新ファイル照合を通します。素材の自動画像生成・課金API呼び出しは実装していません。

## 版固定と互換性

`manifest.json`の `assets[]` で `asset_id` と `version` を必須にします。旧EP004の `cuts[].shared_assets[].id/version/pose` もそのまま解決できます。版が見つからなければエラーで、最新への置き換えは行いません。表情の存在しない版もエラーになります。

`resolve`はentrypoint、選択表情、全依存ファイル、パラメータ、権利、QCを返します。`check`はファイルの現状を再照合します。台帳上に計画があるだけの素材や未検品候補は本番利用可能には含めません。

## EP004の登録判定

旧1.0.0の9資源は参照・IDを維持。写真風の背景・氷・注水・工場はEP固有の再現素材として、通常の共通検索から除外します。`--include-episode`で利用可能です。

再利用価値のある4つのモデルを `common_assets/nichijou_naze/models/ice_science/1.1.0/` に独立させました。

|ID|新しい版|用途|
|---|---|---|
|NNZ_MODEL_ICE_MICRO_01|1.1.0|気泡の拡大・光散乱|
|NNZ_MODEL_FREEZING_CELL_01|1.1.0|製氷皿の凍結断面|
|NNZ_MODEL_ICECAN_AIR_01|1.1.0|製氷缶の送気|
|NNZ_MODEL_ICECAN_DRAIN_01|1.1.0|中心液体の吸引|

形状や物理計算は元のEP004から変更せず、依存importを独立フォルダ内へ変更。Three.jsとMITライセンスも同梱し、EP004ディレクトリに依存しません。APIは `createReusableScene(canvas,{asset_id,parameters})` → `draw(frame,mode)` / `dispose()`。再生速度・開始フレーム・微細気泡ビューを調整できます。位置・縮尺は親レイヤーで変更。科学的な形状変更は別版でQCが必要です。検品は運用上の自己QCであり、独立したG3科学レビューではありません。

## 新規素材の候補登録と正式登録

```bash
node tools/library.mjs candidate path/to/new-manifest.json
# 実レンダリング・目視・権利・依存確認後
node tools/library.mjs register path/to/new-manifest.json path/to/QC.json
node tools/library.mjs catalog
```

候補manifestの形式は `models/ice_science/1.1.0/manifest.json`。ID・版・名称・種類・entrypoint・files・preview・origin_project・parameter_schema・dependencies・tags・rightsを記録します。QCは `result: PASS`、空でない全PASSのchecks、`verified_assets: [ID@VERSION]`、依存・プレビュー・ライセンスを含む `file_hashes` が必須です。登録前に現在の実ファイルと照合。自己申告のPASS文字列だけでは登録できません。

登録レコードは `management/operations/v1/registrations/<ID>/<version>.json` に排他的に作成し、既存registryへ追記します。同じ版の再登録を拒否し、ロックで同時更新を防ぎます。既存台帳の行はそのまま保持します。万一registry更新後の台帳書き出しだけが失敗した場合は、`python tools/library/sync-ledger.py`で派生台帳を同期できます。

旧版のQCは当初のファイルハッシュを `legacy-integrity.json` に固定。catalogを再生成しても、変更された素材を自動で再承認することはありません。新しい版を登録してください。

## ChatGPT Workへの受け渡し

```bash
node tools/library.mjs export episodes/LIBRARY_REUSE_TEST/manifest.json /tmp/nnz-new-episode
```

未作成の別ディレクトリへ、必要な共通素材・依存コード・public素材・フォント・QC・再生方法をコピーします。`asset-lock.json`は元パスとSHA256を保持。例の `--locked` レンダラーはそれを検査し、元EPを参照しません。Node>=22 / npm依存 / Chromium WebGL2（swangle）/ ffmpegが必要です。NPM依存を除く素材の再生成は不要です。

汎用アセットの再生API・既存runtimeのconfig例はカタログのparameters_noteを参照してください。複雑なdiagram configは既存 `validateScene` / `validateConfig` を併用します。帯・全編進行バー・字幕は本編で一度だけ重ねます。

## バックアップとDrive

```bash
node tools/library.mjs catalog
node tools/library.mjs backup
python tools/library/restore.py releases/<BACKUP_ID>/backup-index.json /tmp/nnz-restored-library
```

日時（Asia/Tokyo）付きの新規フォルダに複数ZIP・全ファイルSHA256・各ZIPのSHA256を保存します。過去バックアップは上書きしません。restoreは全ZIPのハッシュとパストラバーサルを検査し、未作成フォルダへ復元して再照合します。

指定Google Driveへの接続はHTTP403で失敗し、Driveコネクターや認証済みGoogle identityも利用できません。**Driveへは保存していません。** 保存先と状態は `validation/library-ops/backup-status.json`。ローカル／GitHubの検証済みバックアップを使用してください。

## 保守上の範囲

検索画面は作成時点の一覧。制作時にはCLIで再検証してください。旧写真の権利は元のAIサービス条件に従い、第三者の独占的権利や法的保証まで付与するものではありません。口パク・独立した手足リグは未制作で、静止ポーズからあると判定しません。正式な元の黄色い帯は別途の本編素材として扱い、今回の共通モデルへ焼き込んでいません。
