# Codex再開指示｜給油ノズル G2 V2｜403回避済み素材を使用
記録：2026-11-01
対象：**既に採用済み** G2 V2／全8カットをCodexで編集用素材として制作する工程

## 重要：ユーザーへの環境設定依頼を中止
Codex実行環境で `v3b.fal.media`、`tatsuno-corporation.com` がHTTP 403でも、**両URLへの直接アクセスは不要**。
外部URLの許可設定追加や音声再アップロードをユーザーに依頼せず、下記代替を使って続行する。

## 復旧済みのC01動画
- GitHub原本：`episodes/GAS_NOZZLE/assets/generated/C01_autostop_ai_reenactment.mp4`
- URL：https://github.com/yuselect89-lab/nichijou-naze/blob/main/episodes/GAS_NOZZLE/assets/generated/C01_autostop_ai_reenactment.mp4
- fal生成履歴の原本をGitHub Actionsで回収し、SHA256を記録済み
- SHA256：`13e93aceae0b43fe50e4c7cff1829b9d4c926dbb8851baaa896e55085dbfee81`
- 技術メタデータ：**1080×1920、5.184秒、H.264、AAC音声トラックあり**（音声なしという生成指示と異なるのでCodex素材には音声を残さない）
- **実画の自動停止動作のQCは未完了**。冒頭のレバーが手動操作ではなく自動解除で動くこと、形状破綻がないことを実フレームで検査。ダメなら修正生成を手配する。完成扱いにしない。
- 素材はC01（0–4.16秒）に合わせてトリミングし、C02へ自然につながるよう同一ソースを再利用。元の5.184秒原本は改変せず残す。
- 素材からAACなど音声を**削除**し、Work側の承認済みVOを邪魔しないこと。

## メーカーPDFの取得代替（検知口の正確さを確認するための内部資料）
GitHub Actions run： https://github.com/yuselect89-lab/nichijou-naze/actions/runs/41282110781

アーティファクト名：`gas-nozzle-reference-for-qc`（保存期間7日）
取得例：
```bash
gh run download 41282110781 --repo yuselect89-lab/nichijou-naze -n gas-nozzle-reference-for-qc -D /tmp/gas-nozzle-reference
```
中身：`tatsuno_nozzle_reference.pdf`
- 本資料は**内部の正確さ確認に限る**。公開本編にPDFの画像や写真を許諾なしに転載しない。
- PDFの「ノズル管（筒先）」先端側面にある小さな「センサー孔」と、主な吐出口を区別して描く。
- PDFを取り込めない場合でも、正確さが確認できない画像を完成と扱わない。外部サイトの直接アクセスが必須だと決めつけない。

## 続行する制作作業（最終指示書準拠）
1. `episodes/GAS_NOZZLE/g2/NNZ_GAS_NOZZLE_G2_VISUAL_DESIGN_V2_20261101.md`、同期CSV、再QC、`AI_GENERATION_OVERRIDE_20261101.md`を確認する。
2. C01生成済み素材を実再生QCし採用可否を判定。動画生成済みと**QC PASS**は別。
3. C04の正しい検知口を写実AI生成し、C05断面モデルと部位・構造を連続させる。C08はこの素材を再利用。
4. C03およびC05–C07をG2設計書どおり全制作。C05–C07では同一モデル・部品IDを使用し、ダイヤフラム→ロック解除→バネで主弁閉鎖を省略しない。
5. C02はC01と同じ素材から質問とキャラの演出を作る。
6. 正本 `AGENTS.md`、`production-lock.json`、各種LOCK、`docs/TYPOGRAPHY_4_PRINCIPLES.md` を守り、`npm run preflight`と既定のライブラリ検証を通す。
7. **全8カットの無音編集用素材・ソース・Work引継ぎ資料・G2実物QC・SHA256を一つのZIPへ納品**。完成動画の組立はWorkが担当。音声提出の要求禁止。
8. `40.124063秒`の音声基準尺と台本G1 V1.1は変更しない。字幕・黄色帯・単一進行バーを素材へ二重焼き込みしない。

## 進捗の正しい表現
- 回収成功：C01生成動画の実ファイル、メーカー参照PDFの内部用データ
- 未完：C01実画QC、C04生成と整合QC、C02／C03／C05–C08完成素材、Work用ZIP
- **GitHubへ回収できたことは全8カット完成を意味しない**。
