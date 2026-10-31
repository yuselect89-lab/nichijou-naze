from pathlib import Path
import json,hashlib,zipfile,subprocess,shutil,math
B=Path(__file__).resolve().parents[1]
tech=json.loads((B/'docs/technical_qc.json').read_text());layout=json.loads((B/'docs/layout_qc.json').read_text());alpha=json.loads((B/'docs/alpha_qc.json').read_text())
presenter=json.loads((B/'docs/presenter_integrity_qc.json').read_text());assert presenter['result']=='PASS'
assert hashlib.sha256((B/'docs/reference_locks/02_G2_V2_VISUAL_DESIGN_LOCK_UNCHANGED.md').read_bytes()).hexdigest()=='8abf8efbee0a32c41967a860ba49deafdf3e858a9e18ef99db43ad3513287010'
assert tech['technical_result']=='PASS' and len(tech['records'])==38 and len(alpha)==22
collisions=json.loads((B/'docs/photo_collision_qc.json').read_text());assert all(r['photo_photo_presenter_and_label_max_overlap_pixels']==0 for r in collisions)
assert all(r['max_presenter_photo_overlap_pixels']==r['max_content_pixels_in_caption_reservation']==r['max_content_pixels_in_right_ui_reservation']==0 for r in layout)
for i in range(1,7):
 c=f'C{i:02d}';s=json.loads((B/'scenes'/(c+'.json')).read_text());n=math.ceil(s['duration']*24);frames=sorted(set([0,n//4,n//2,3*n//4,n-1]));expression='+'.join(f'eq(n\\,{f})'for f in frames)
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(B/'previews_1080'/(c+'_G2_V3_silent.mp4')),'-vf',f'select={expression},scale=360:640,tile=5x1','-frames:v','1','-threads','1',str(B/'qc'/(c+'_ACTUAL_VIDEO_MOTION_STRIP.png'))],check=True)
(B/'docs/INTERNAL_VISUAL_QC.md').write_text('''# G2 V3 R1 内部実画検査

旧版の実画受入はMAJOR。旧版の内部検査では人物切れを見落とした。本R1では固定切抜きを廃止し、髪・手・上半身全体の派生画像一致、クリップ前の全フレーム境界、実動画アルファ一致の検査を追加。受入再判定・Gemini外部審査は未実施。詳細はMAJOR_R1_REPAIR.md。

全6カットを候補として実装。外部G2実画PASS、V3正式LOCK、本編完成・公開PASSは取得していない。

確認方法：エンコード済み1080/360 MP4から代表フレームと5時点の列を抽出し、直接レンダーの中間動作と合わせて目視比較。scenesの位置・不透明度変化、25時点/カットの安全域検査と全735フレームの写真同士・人物/説明文字と写真の不透明領域交差検査、全38動画の全フレームデコードを実行。リアルタイム視聴による第三者の意味理解評価や音声との同期実測とは区別する。

- C01：前半の大きい写真で右手前の縁の明暗を360pxでも確認。後半は写真を右へ縮小し、questionと分離。写真は元画素以下、追従ガイドは独立レイヤー。原本バイト一致・外部の鮮明度合否は未確認。
- C02→C03：同一の10円写真と台座を継続。C02の空の高い台座を「頂点」と予告し、C03で中央10円台座がそれを越えて上がる。1951年・最高額＝10円・到達後の反応を確認。
- C04：穴なし菊花50円と鳳凰100円を写真で確認。10円が下段へ移り、50円、100円が順に高位へ入る。年号と額面は独立文字。人物を上部の別領域へ移し、写真と交差しないよう修正。写真に重なる補助矢印を省略し、台座の段階移動を主演出にした。写真の微細な刻印文字が全て360pxで読めるという判定ではなく、図柄は写真、額面・年代は独立ラベルで伝える設計。
- C05：初めに3枚と共通の縁模式図。1959年の別写真が横から入り、旧10円は残る。変身・溶解なし。「模式図」を残して新旧比較へ接続。
- C06：同じ340pxの新旧写真パネル、同じ300pxの模式図。ギザあり/なしと年代を分離。頂点の光を図解層で回収し、写真の下に置く。payoffは上部の空き領域に配置。実測同条件の側面写真比較とは称さない。

レイアウト：写真同士・人物と写真・説明文字と写真の交差は全735フレームで0。安全域は全カット25時点で、人物と写真の不透明領域交差0、字幕予約Y1510〜1790への侵入0、右UI予約X940〜1080への侵入0。写真の退場・登場途中も透明安全枠を適用。実アプリのUI差、正式帯・字幕等を加えた最終本編はWorkのG3で再確認。

技術：22本のqtrle/ARGB透過MOV、16本のMP4（各6カット＋連続A/B、1080/360）を全デコード。音声0。22本のアルファ抽出でも透明背景・不透明主役・右安全枠を確認。写真の表示寸法は元の片面画素数以下。完全な制作リポジトリでpreflightと31件のテストを実行。

残る制約：写真は転送コピーで原本バイト未照合。公開前に最終動画のCC BY-SA継承範囲と表示方法を確認。音声の1950/1951不一致は未解決。BGM/SE/字幕/正式帯/CTA/進行バーは素材へ合成していない。V2正本は保持。
''')
status={'revision':'R1','previous_acceptance':'MAJOR','presenter_integrity_result':'PASS','work_acceptance_recheck':'NOT_PERFORMED','scope':'All six cuts implemented as G2 V3 review-candidate separated assets','technical_result':'PASS','native_cut_scenes':6,'lossless_alpha_movies':22,'review_movies_1080_and_360':16,'full_decodes':38,'external_g2_visual_pass':False,'v3_locked':False,'upstream_photo_binary_match_verified':False,'audio_year_1950_vs_1951_resolved':False,'audio_accessed_or_modified':False,'publication_status':'HOLD pending external G2, audio-year resolution and Work G3 / final license scope','v2_lock_unchanged':True,'paid_generation_used':False}
(B/'docs/DELIVERY_STATUS.json').write_text(json.dumps(status,ensure_ascii=False,indent=2))
# Only authoritative validation logs are delivered; earlier render revisions remain in work/.
archive_logs=B.parent/'giza10_v3_intermediate_logs';archive_logs.mkdir(exist_ok=True)
for p in (B/'docs').glob('render*.log'):shutil.move(str(p),str(archive_logs/p.name))
for p in B.rglob('__pycache__'):shutil.rmtree(p)
files=[]
for p in sorted(B.rglob('*')):
 if p.is_file()and p.name not in ['ASSET_MANIFEST.json','SHA256SUMS.txt']:
  files.append({'file':str(p.relative_to(B)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(B/'ASSET_MANIFEST.json').write_text(json.dumps({'design':'G2 V3 CANDIDATE','files':files},ensure_ascii=False,indent=2))
(B/'SHA256SUMS.txt').write_text('\n'.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(B)) for p in sorted(B.rglob('*')) if p.is_file()and p.name!='SHA256SUMS.txt')+'\n')
zpath=B.parent/'NNZ_GIZA10_G2_V3_R1_ALL_CUTS_20261031.zip'
with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(B.rglob('*')):
  if p.is_file():z.write(p,arcname=str(Path(B.name)/p.relative_to(B)))
with zipfile.ZipFile(zpath)as z:assert z.testzip()is None;count=len(z.namelist())
print(json.dumps({'archive':str(zpath),'bytes':zpath.stat().st_size,'files':count,'zip_crc':'PASS','status':status},ensure_ascii=False),flush=True)
