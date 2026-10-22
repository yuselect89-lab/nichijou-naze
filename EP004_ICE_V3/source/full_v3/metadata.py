from pathlib import Path
import json,hashlib,shutil
R=Path(__file__).resolve().parents[2];repo=R.parent
manifest=json.loads((R/'source/full_v3/stage1_metadata/manifest.json').read_text())
manifest.update(version='V3_full',stage=2,status='self_qc_pending',scope='10 individual silent cut assets. No full-episode movie. Stage1 Cut01/Cut09 preserved; remaining cuts approved by user.',created_at='2026-10-22',shared_registry='common_assets/nichijou_naze/props/ice_v3/v1.0.0/manifest.json')
narrations=[s for s in (R/'source/LOCKED_NARRATION_V8.txt').read_text().split('\n\n') if s.strip()]
frames=[105,195,120,150,105,75,195,165,165,123]
actions=['承認済み。白い中心を持つ実写風の氷を緩やかに拡大。','沸騰→冷却→注水→疑問符。完成した氷は表示しない。','条件による白濁量の違いを示す実写風例。','実写風の白い中心を追いかけて気泡の立体拡大模式へ移行。','氷内部の空洞と入射光・複数方向の散乱光。光路は模式。','実写風沸騰背景と別枠の溶存気体模式。大泡とは別物。一部の気体は残る。','製氷皿断面。外側から凍結し気体が中心へ移動。後半は中心へ寄り、最後に微細な空洞として残る。','工場の製氷缶。外側から凍結。橙色の送気管がゆっくり撹拌。中心の液体は残す。','承認済み。上から吸水管を入れ液体だけを連続排出。外側の固体と少量の残水を保持。','仕上げ工程後へ時間が移る。左右同照明・同程度サイズの氷を比較。']
char={2:['think','troubled'],3:['surprise'],4:['point_right'],8:['point_right'],9:['point_right'],10:['happy']}
old={c['cut']:c for c in manifest['cuts']}
manifest['cuts']=[];start=0
for i,n in enumerate(frames,1):
 cut=f'cut{i:02}';d=R/cut
 if i in (1,9):
  c=old[cut];c['status']='approved_stage1_preserved'
 else:
  c={'cut':cut,'narration':narrations[i-1].strip(),'start_seconds':start/30,'duration_seconds':n/30,'frames':n,'status':'rendering','files':[],'animation':actions[i-1],'editable_source':'source/full_v3/index.jsx','layers':['base_animation.mp4','labels_overlay.webm']+(['character_overlay.webm'] if i in char else []),'origin':'new original 3D/SVG-style diagram and AI photographic reenactments; character assets reused','notes':[]}
 c['start_seconds']=start/30;c['duration_seconds']=n/30;c['frames']=n
 c['narration']=narrations[i-1].strip();c['animation']=actions[i-1]
 c['shared_assets']=[{'id':'NNZ_CHAR_FEMALE_01','version':'v03_expressions' if p in ('troubled','surprise','happy') else 'v02_highres','pose':p} for p in char.get(i,[])]
 c['files']=[{'file':str(p.relative_to(R)),'type':'video' if p.suffix in ('.mp4','.webm') else 'still' if p.suffix=='.png' else 'source','bytes':p.stat().st_size} for p in sorted(d.iterdir()) if p.is_file()]
 c['notes']=['仮尺。V8の完成VOに合わせた同期はChatGPT Work。','animation.mp4はプレビュー用合成。編集時はbaseと透過レイヤーを推奨。字幕・帯・進行バー・音声なし。']+(['実写風画像はAIによる再現。実験映像ではない。'] if i in (1,2,3,6,10) else ['拡大・速度・形状・光路は理解のための模式表現。'])
 manifest['cuts'].append(c);start+=n
manifest['total_frames']=start
manifest['limitations']=['公式参考URLはこの環境のネットワーク制限により再取得できない。公式画像は不使用。','黄色い帯は素材に焼き込まない。元の正式帯画像の独立ファイル未確認。Work側で提供済み原本を使用。','VO・字幕・全編編集・G3はChatGPT Work/Gemini Pro担当。Google Drive連携なし。']
(R/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print('Manifest:10cuts,',start,'frames')
