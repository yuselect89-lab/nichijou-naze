# Codex最終制作指示｜フロントガラス黒い帯と点々｜省コスト版
2026-11-02／対象：`yuselect89-lab/nichijou-naze`
**G1 V2 PASS／G2 V1書面MINORをV2で2点是正／素材制作・実画QC・G3未実施。**

## 実行
採用台本とG2 V2映像設計を変更せず、**C01〜C08全カットの実際に使える無音映像素材、共通マスター／必要最小限の編集可能ソース、実画QC、Work引継ぎ指示書を一括ZIP納品**。書面・プロンプトだけの納品や完成動画一本の組立は担当外（本編編集はWork）。

## 読む正本（全文の再転記禁止）
1. `episodes/WINDSHIELD_BLACK_DOTS/g2/NNZ_WINDSHIELD_BLACK_DOTS_G2_VISUAL_DESIGN_V2_20261102.md`（V1からC05・C07のみ是正、8カットすべての正本）
2. `episodes/WINDSHIELD_BLACK_DOTS/g2/NNZ_WINDSHIELD_BLACK_DOTS_G2_V1_QC_MINOR_RESOLVED_20261102.md`（指摘と差分）
3. `episodes/WINDSHIELD_BLACK_DOTS/g1/SCRIPT_V2_20261102.md`（G1 PASS台本）
4. 最新`AGENTS.md`、`production-lock.json`と対象工程の既存制作LOCK、`docs/CONTEXT_EFFICIENCY_POLICY.md`。

## 守るべき核心
- **C05〜C06**：完成車の黒帯をUVが貫通しない。C05は接着剤の性質、C06で遮蔽を示す。
- **C07後半**：「製造時／模式図」で**接着剤・車体・UVを消し、ガラス単体の加熱・曲げ加工**へ。C07前半の見た目から時間・対象を明確に切り替える。実測熱画像・製造後の太陽熱と混同しない。
- **C01/C08同一車・同一ドット配置**、C03〜C07は同一断面マスターの部品表示切替。黒帯とガラスと接着剤の位置関係を捏造しない。実物接写→奥行きある模型→同じ実物へ復帰。白背景の小玩具・静止画ズーム連打で代用しない。
- **2つのマスターを再利用**し、8カットごとに有料AI動画生成しない。必要な動きだけ生成し、同じ失敗の無制限再生成禁止。未承認素材はPASS扱いしない。
- 制作前にLOCK・台帳・`node tools/verify-production.mjs`・`npm run preflight`等の既定検証を実行。正式帯・字幕・進行バー・VO・BGM/SEはCodex素材に焼き込まずWorkへ。既存キャラ・文字4原則・360pxとYouTube UI安全域遵守。台本・音声変更禁止、音声提出要求禁止。
- 音声尺は未実測。**C07前後半の理解できる発話時間をWorkの実VOで確認**できるようカット素材は尺調整可能にし、仮の固定30秒へ詰め込まない。

## 一括納品の完了条件
C01〜C08の無音レンダーMP4、共通マスター/編集可能レイヤー、生成元・権利・manifest・SHA256、C05/C06のUV・C07の表示切替と熱の実画QC（連続動作・360px確認）、`WORK_ASSEMBLY.md`。ZIP再展開と全8カットのデコードを確認。**G2書面の条件充足は実画G2 PASSやG3 PASSを意味しない。**
