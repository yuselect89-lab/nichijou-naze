# ChatGPT Work 引き渡し

対象：EP004「白い氷」V3 / 台本V8 LOCK。

- A・B・Cの納品ZIPを同じ場所へ展開。
- `manifest.json`のcut順に、各cutの`animation.mp4`を仮配置。これは無音の合成プレビュー素材。
- 個別調整する場合は`base_animation.mp4`を使い、必要な`labels_overlay.webm`と`character_overlay.webm`を一度ずつ合成。Cut01は`animation.mp4`のみでよい。
- 素材は1080×1920、30fps。合計1398フレーム＝仮46.6秒。VOが完成したら同期を調整する。
- Cut02は結果を先に見せない。Cut06の金色の印は溶存気体の模式記号。
- Cut07の`base_render.mp4`は寄りを適用する前の元動画。通常は寄り済み`base_animation.mp4`を使う。
- Cut08の橙色は送気、Cut09の青色は吸水。Cut09で外側の固体を消さない。
- Cut09→10は仕上げ工程を省略して完成品を紹介する時間移動。吸い出した直後に一体の透明氷へ変化する演出を追加しない。

## Work側で必要な素材・作業

VO、VO同期の日本語字幕、正式な黄色い帯の原本、全編に同期する0→100%の進行バー、BGM/SE、全編編集、G3。

帯・字幕・進行バーは各cutには含まれていません。字幕は読点「、」を使わず句点「。」を残してください。詳細領域はmanifestのsafe_zones。

正式帯画像の独立ファイルはこの環境で確認できていません。元の添付原本をWork側で配置してください。VOは未支給のため音声・字幕同期は行っていません。

## 確認資料

- `preview/full_v3/contact_sheet.jpg`：10カット一覧
- `preview/full_v3/cut*-sequence.jpg`：科学工程の連続フレーム
- `preview/full_v3/cut*-safezone-360.png`：スマートフォン相当の領域確認
- `qc/full_v3/report.json`：ファイル検査と自己QC。G3の代替ではない
- `licenses/`：生成由来と依存ライセンス
- `README.md`：編集・再レンダリング手順と制約
