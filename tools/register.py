from pathlib import Path
import json,hashlib,shutil
from fontTools.ttLib import TTCollection
r=Path(__file__).resolve().parent.parent
fonts=TTCollection('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc')
f=next(f for f in fonts.fonts if any(n.nameID==1 and n.toUnicode()=='Noto Sans CJK JP' for n in f['name'].names))
dest=r/'public/series/v1/NotoSansCJKjp-Bold.otf'
if not dest.exists():f.save(dest)
if (r/'library-registry.json').exists():
    print('Existing registry retained; new asset versions must be registered explicitly.')
    raise SystemExit(0)
vendor=r/'vendor/common-library/1.0.0'
entries=json.loads((vendor/'common_assets/nichijou_naze/management/asset_registry.json').read_text())
registry={'library':'nichijou-naze','upstreamVersion':'1.0.0','integrationVersion':'1.0.1','activeTemplates':[{ 'id':x['Asset ID'],'revision':'1.0.1','upstreamRevision':'1.0.0','implementation':'src/integration/v1.0.1/Templates.tsx'} for x in entries if x['Asset ID'] in ['NNZ_TMP_ARROW_01','NNZ_TMP_COMPARE_01','NNZ_TMP_ZOOM_01']],'character':{'id':'NNZ_CHAR_FEMALE_01','revision':'1.0.0','status':'prototype','poses':[]},'plannedOnly':[x['Asset ID'] for x in entries if x['ステータス']=='planned'],'banner':{'path':'public/series/v1/opening_banner.png','source':'Existing EP004_ICE/shared/opening_banner.png','sha256':hashlib.sha256((r/'public/series/v1/opening_banner.png').read_bytes()).hexdigest(),'note':'Uploaded message also shows a round 30-second banner, but no separate original file was present in the supplied ZIP. Existing EP004 banner reused without redesign.'},'originalFiles':{str(p.relative_to(vendor)):hashlib.sha256(p.read_bytes()).hexdigest() for p in vendor.rglob('*') if p.is_file()}}
for p in sorted((r/'public/common_assets/nichijou_naze/characters/female_v01/poses').glob('*.png')):registry['character']['poses'].append({'pose':p.stem,'path':str(p.relative_to(r/'public')),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(r/'library-registry.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2))
