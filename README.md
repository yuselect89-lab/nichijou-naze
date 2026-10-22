# EP005 映像素材 V2 ダウンロード

全6カットの背景・透過MOV・ラベル・ソース・プレビュー・自己QC・引き継ぎ資料です。元ZIPは約328MB。GitHubの通常ファイル上限を超えるため、元ZIPを7分割して保存しています。元ファイルの内容は変更していません。

1. このブランチの **Code → Download ZIP** から一式をダウンロードして展開します。
2. Windows：`Restore-Windows.bat` を実行。Mac/Linux：このフォルダで `python3 restore.py` を実行（Python3が必要）。WindowsはPythonなしでPowerShell版を使用できます。スクリプトをブロックする端末では、その端末の管理方針に従ってください。
3. SHA256照合済みの `EP005_materials_v2.zip` が復元されます。そのZIPを展開し、`EP005_materials_v2/episodes/EP005/v2/README.md` を確認してください。

ChatGPT Work等のPython実行環境でも `python3 restore.py` で復元できます。7個のpartファイルを単独のZIPとして開かないでください。

実物場面は写真調の生成再現素材です。音声同期とラフMP4組み立ては次工程。元の仮尺は35秒ですが、添付VOはユーザー報告で28.68秒。台本を変更せず、ソースと前後各1秒のハンドルを使って確定音声へ合わせてください。完成本編は含まれません。

この専用配布ブランチは素材受け渡し用であり、mainやEP004の制作ファイルは変更しません。
