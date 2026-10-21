"""Finish new generated expression masters; preserve every V02 pixel."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import hashlib, json, shutil

R=Path(__file__).resolve().parents[2]
ROOT=R/'common_assets/nichijou_naze/characters/female_v01/versions/v03_expressions'
PUBLIC=R/'public'/ROOT.relative_to(R)
SOURCES={'surprise':'851a393e-373e-446a-b5c0-61344cdae4f4',
         'happy':'5384a0cb-b78f-4c80-b176-381f1c25e635',
         'troubled':'3119c516-17b1-43a4-9743-a5f2d17d801f'}
records=[]
for sub in ['poses','thumbs','sources']:(ROOT/sub).mkdir(parents=True,exist_ok=True)
for pose,uid in SOURCES.items():
    dest=ROOT/'poses'/f'NNZ_CHAR_FEMALE_01_pose_{pose}.png'
    if dest.exists():raise RuntimeError('Refusing to overwrite '+str(dest))
    src=Path('/workspace/generated_images')/f'exec-{uid}.png'
    im=Image.open(src).convert('RGBA');raw=np.array(im)
    # Remove tiny alpha specks and normalize the generator's 253-level opaque pixels.
    raw[:,:,3]=np.clip((raw[:,:,3].astype(float)-6)*255/247,0,255).round().astype('uint8')
    raw[raw[:,:,3]==0,:3]=0
    clean=Image.fromarray(raw);bbox=clean.getchannel('A').getbbox()
    # A few near-transparent outliers can expand the bbox; retain all alpha >= 16.
    substantial=clean.getchannel('A').point(lambda x:255 if x>=16 else 0).getbbox()
    crop=clean.crop(substantial);scale=min(2160/crop.height,1392/crop.width)
    scaled=crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.LANCZOS)
    canvas=Image.new('RGBA',(1536,2304));canvas.alpha_composite(scaled,((1536-scaled.width)//2,2232-scaled.height))
    a=np.array(canvas);a[a[:,:,3]<=2]=0;canvas=Image.fromarray(a)
    canvas.save(dest,optimize=True)
    canvas.resize((256,384),Image.Resampling.LANCZOS).save(ROOT/'thumbs'/f'{pose}_thumb.png')
    shutil.copy2(src,ROOT/'sources'/f'{pose}_generated.png')
    for sub,name in [('poses',dest.name),('thumbs',f'{pose}_thumb.png')]:
        (PUBLIC/sub).mkdir(parents=True,exist_ok=True)
        shutil.copy2(ROOT/sub/name,PUBLIC/sub/name)
    records.append({'pose':pose,'file':'poses/'+dest.name,'resolution':[1536,2304],
      'generated_source_resolution':list(im.size),'source':'sources/'+pose+'_generated.png',
      'source_alpha_bbox':bbox,'crop_bbox':substantial,'scale_factor':scale,
      'alpha_content_bbox':canvas.getchannel('A').getbbox(),
      'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
manifest={'asset_id':'NNZ_CHAR_FEMALE_01','version':'v03_expressions','base_version':'v02_highres',
 'description':'V02の人物デザインを参照した追加3表情。V02本体は変更しない。',
 'reference':'../../poses/NNZ_CHAR_FEMALE_01_pose_neutral.png',
 'available_poses':['neutral','talk','point_right','point_left','think',*SOURCES],
 'inherited_poses':{p:'../../poses/NNZ_CHAR_FEMALE_01_pose_'+p+'.png' for p in ['neutral','talk','point_right','point_left','think']},
 'poses':records,'background_transparency':'true RGBA alpha; no matte',
 'processing':['Reference-conditioned new expression redraw; not enlarged prototype',
 'Alpha <=6 removed; 253 opaque normalized to255; transparent RGB zeroed',
 'Crop alpha>=16 bounds; Lanczos resample; align bottom to2232 on1536x2304 canvas'],
 'native_resolution_note':'1024x1536 generated sources; delivery is normalized to1536x2304, not native2304 generation.',
 'usage_notes':['Use v03_expressions explicitly; inherited five poses resolve to unchanged V02 files.',
 'Whole-sprite motion only; no mouth or independent limb parts exist.',
 'Static expression variation; not lip-sync or a rigged animation.'],
 'qc_status':'pending_actual_render'}
(ROOT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
shutil.copy2(ROOT/'manifest.json',PUBLIC/'manifest.json')
(ROOT/'README.md').write_text('''# NNZ_CHAR_FEMALE_01 v03_expressions

驚く・喜ぶ／納得・困る／疑問の追加3ポーズ。各1536×2304 RGBA。
既存V02の5ポーズは変更しません。v03はその5ポーズを参照して全8ポーズを呼び出せます。
新規生成元は1024×1536。生成元・クロップ・倍率・ハッシュはmanifestに記録。
全身約2160px・足元2232pxでV02と基準を統一。透過端を整形した新規描き起こしです。
使用例・検証結果は共通ライブラリの拡張READMEとvalidation/extensionを参照。
''')
print(json.dumps(records,ensure_ascii=False,indent=2))
