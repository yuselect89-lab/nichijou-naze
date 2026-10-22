"""Build explicit provenance manifests; never edits the common library or original EP files."""
from pathlib import Path
import json,hashlib,subprocess
from PIL import Image,ImageDraw
EP=Path(__file__).resolve().parents[2]; ROOT=EP.parents[1]; E=EP/'evidence/v1'; A=EP/'assets/v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return str(p.relative_to(ROOT))
def write(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
base=json.loads((E/'baseline-sha256.json').read_text())
changed=[p for p,h in base.items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h]
assert not changed,changed
shared=[]
for key,version,pose in [('think','v03_expressions','think'),('point','v02_highres','point_right'),('happy','v03_expressions','happy')]:
    resolved=json.loads((E/f'resolve-{key}.json').read_text()); assert resolved['check']['ok']
    assert sha(A/f'character-{key}.png')==resolved['file_hashes'][resolved['selected_file']]
    shared.append({'asset_id':'NNZ_CHAR_FEMALE_01','version':version,'pose':pose,'source':resolved['selected_file'],'sha256':sha(ROOT/resolved['selected_file']),'delivery_copy':rel(A/f'character-{key}.png'),'rights':resolved['rights'],'qc_reference':resolved['qc'],'verification':rel(E/f'resolve-{key}.json')})
rights={'basis':'Original EP006 SVG/React explanatory artwork created for this request; not live-action footage or a medical measurement.','usage':'EP006 production and editing; inherited character and font rights remain conditional on their source terms.','license_files':[rel(A/'FONT_LICENSE.txt')]}
source=A/'Scene.tsx'; geom=A/'geometry.ts'
timeline=[('CUT01',0,180,0,180,'CUT01','question'),('CUT02',180,300,0,120,'CUT02','reaction'),('CUT03',300,420,0,120,'CUT03','reveal_intro'),('CUT04',420,570,0,150,'science','focus_only'),('CUT05',570,690,150,270,'science','focus_only'),('CUT06',690,870,270,450,'science','focus_only'),('CUT07',870,1050,0,180,'CUT07','payoff')]
cuts=[]
for cut,start,end,ss,se,scene,role in timeline:
    key={'CUT02':'think','CUT03':'point','CUT07':'happy'}.get(cut)
    reference=next((a for a in shared if key and a['delivery_copy'].endswith(f'character-{key}.png')),None)
    cut_rights={'original':rights,**({'character':reference['rights']} if reference else {})}
    layers=['background','object','labels']+(['character'] if key else [])
    if scene=='science':layers=['background','tissue','vessels','skin','outline','labels']
    item={'cut':cut,'asset_id':f'EP006_{cut}_MATERIAL','version':'1.0.0','role':role,'source':rel(source),'sha256':sha(source),'global_start_end':{'start':start,'end':end,'unit':'frame','end_exclusive':True,'status':'provisional'},'source_start_end':{'start':ss,'end':se,'unit':'frame','end_exclusive':True,'status':'provisional'},'duration_status':'provisional / VO duration not supplied','scene':scene,'layer':layers,'reference':['SCRIPT_LOCK_V4.md','G2_STORYBOARD_V2.md','G2_DECISION_20261022.md'],'rights':cut_rights,'preview':rel(EP/f'preview/v1/{cut}-360.png'),'review_video':rel(A/f'{cut}-review-1080.mp4'),'review_video_sha256':sha(A/f'{cut}-review-1080.mp4'),'transparent_sources':True,'shared_assets':([{'asset_id':reference['asset_id'],'version':reference['version'],'pose':reference['pose']}] if reference else []),'layer_sources':[{'layer':layer,'source':rel(source),'sha256':sha(source),'props':{'scene':scene,'layer':layer,'labels':layer=='labels'}} for layer in layers]}
    if scene=='science':item.update({'continuous_group':'EP006_FINGER_SECTION','continuous_source':rel(geom),'continuous_source_sha256':sha(geom),'reset_at_cut_boundary':False,'frame_argument':'single shared scienceFrame over 0..449','camera':'fixed / identity','subject_count':1})
    write(A/f'{cut}.asset.json',item);cuts.append(item)
files=[{'path':rel(p),'sha256':sha(p),'bytes':p.stat().st_size} for folder in [EP/'assets/v1',EP/'preview/v1'] for p in sorted(folder.rglob('*')) if p.is_file()]
manifest={'schema_version':1,'project':'EP006','delivery_version':'1.0.0','delivery_scope':'episode-specific visual assets; no VO, subtitles, BGM, SE, progress or approved banner burned in','base_git_commit':'9fc3089e49a5c4add628120cc5e6c3e9423afd88','delivery_commit_lookup':'git log -1 --format=%H -- episodes/EP006/manifest.json','fps':30,'width':1080,'height':1920,'duration_status':'provisional','total_preview_frames':1050,'script_lock':{'path':rel(EP/'SCRIPT_LOCK_V4.md'),'sha256':sha(EP/'SCRIPT_LOCK_V4.md'),'modified':False},'assets':shared,'episode_assets':[{'asset_id':'EP006_BATH_FINGER_CG','version':'1.0.0','source':rel(source),'sha256':sha(source),'rights':rights,'status':'episode-local / rendered / self-QC; not common-library registration'},{'asset_id':'EP006_FINGER_SECTION','version':'1.0.0','source':rel(geom),'sha256':sha(geom),'rights':rights,'status':'episode-local / rendered / self-QC; not medical or G3 approval'}],'cuts':cuts,'files':files,'runtime_dependencies':{'node':'24.19.0','remotion':'4.0.526','react':'18.3.1','typescript':'5.9.3','browser':'/usr/bin/chromium','ffmpeg':'7.1.5','postprocess':'Python 3 / Pillow'},'qc':{'geometry':rel(E/'geometry-qc.json'),'media':rel(E/'media-qc.json'),'alpha':rel(E/'alpha-qc.json'),'cut_boundaries':rel(E/'boundary-qc.json'),'report':rel(EP/'ASSET_QC.md'),'external_G3':'not performed'},'unresolved':['VO file / timing not provided','Live-action finger footage not acquired: independent SVG CG used under production instructions','Final parent compositing and external G3 not performed','Six unused common template IDs remain blocked by integrity mismatch','GitHub push/publication not performed']}
write(EP/'manifest.json',manifest)
assert all(sha(ROOT/f['path'])==f['sha256'] for f in files)
write(E/'delivery-integrity.json',{'status':'PASS','baseline_tracked_files_checked':len(base),'baseline_changed_files':changed,'script_lock_sha256':sha(EP/'SCRIPT_LOCK_V4.md'),'delivery_asset_files_checked':len(files),'shared_character_copies_byte_identical':True,'scope':'file integrity, not external G3 approval'})
# Reserved-region overlays are evidence only, never burned into asset media.
for cut in ['CUT01','CUT03','CUT06','CUT07']:
    im=Image.open(EP/f'preview/v1/{cut}-360.png').convert('RGBA'); overlay=Image.new('RGBA',im.size);d=ImageDraw.Draw(overlay)
    for box,color,label in [((38,110,324,194),'#927640','banner alpha bbox'),((32,503,328,597),'#865d7e','parent captions'),((310,0,359,639),'#467882','right UI'),((32,26,328,31),'#927640','progress')]:
        d.rectangle(box,outline=color,width=2);d.text((box[0]+3,box[1]+3),label,fill=color)
    Image.alpha_composite(im,overlay).convert('RGB').save(E/f'{cut}-safe-area-guide.jpg',quality=94)
print('Manifest and baseline integrity PASS:',len(files),'asset/preview files;',len(base),'original tracked files unchanged')
