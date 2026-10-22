from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parents[2];repo=R.parent
assert json.loads((R/'qc/full_v3/report.json').read_text())['technical_result']=='PASS'
excluded={'__pycache__'}
files=sorted(p for p in R.rglob('*') if p.is_file() and not excluded.intersection(p.parts) and p.name!='SHA256SUMS.txt')
(R/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(R))+'\n' for p in files))
files.append(R/'SHA256SUMS.txt')
parts={
 'EP004_ICE_V3_full_A_cuts01-05.zip':[p for p in files if p.relative_to(R).parts[0] in [f'cut{i:02}' for i in range(1,6)]],
 'EP004_ICE_V3_full_B_cuts06-10.zip':[p for p in files if p.relative_to(R).parts[0] in [f'cut{i:02}' for i in range(6,11)]],
 'EP004_ICE_V3_full_C_sources-preview.zip':[p for p in files if not p.relative_to(R).parts[0].startswith('cut') and not ('preview' in p.parts and p.suffix=='.png' and 'safezone' not in p.name and 'contact' not in p.name and 'comparison' not in p.name)]
}
support=['package.json','package-lock.json','tsconfig.json','common_assets/nichijou_naze/runtime/v1.1.0/components.tsx','common_assets/nichijou_naze/runtime/v1.1.0/config.ts','src/integration/v1.0.1/Series.tsx','src/integration/v1.0.1/Templates.tsx','src/integration/captions.ts','src/integration/character.ts','public/series/v1/NotoSansCJKjp-Bold.otf','public/series/v1/FONT_LICENSE.txt','tools/ice-assets.mjs']
parts['EP004_ICE_V3_full_C_sources-preview.zip'] += [repo/x for x in support]
parts['EP004_ICE_V3_full_C_sources-preview.zip'] += [p for p in (repo/'public/ep004-v3').rglob('*') if p.is_file()]
parts['EP004_ICE_V3_full_C_sources-preview.zip'] += [p for p in (repo/'common_assets/nichijou_naze/props/ice_v3/v1.0.0').rglob('*') if p.is_file()]
for pose in ['think','troubled','surprise','point_right','happy']:
 base=repo/'public/common_assets/nichijou_naze/characters/female_v01';base=base/'versions/v03_expressions' if pose in ['troubled','surprise','happy'] else base
 parts['EP004_ICE_V3_full_C_sources-preview.zip'].append(base/f'poses/NNZ_CHAR_FEMALE_01_pose_{pose}.png')
reports=[]
for name,ps in parts.items():
 dest=repo/'releases'/name
 assert not dest.exists(),'Refuse to replace a published package: '+name
 ps=sorted(set(ps))
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in ps:z.write(p,str(p.relative_to(repo)))
  z.writestr('README_DELIVERY.txt','EP004 白い氷 V3 全10カット。A・B・Cの3つのZIPを同じ場所に展開してください。\nEP004_ICE_V3/index.html でプレビュー。編集仕様はEP004_ICE_V3/README.md。\nA=Cut01–05 B=Cut06–10 C=ソースとプレビューと依存素材。全編MP4なし。\n')
  z.writestr(name.removesuffix('.zip')+'_SHA256SUMS.txt',''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(repo))+'\n' for p in ps))
 with zipfile.ZipFile(dest) as z:assert z.testzip() is None
 assert dest.stat().st_size<100_000_000,(name,dest.stat().st_size)
 reports.append({'file':'releases/'+name,'bytes':dest.stat().st_size,'files':len(ps),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()})
(repo/'releases/EP004_ICE_V3_full_packages.json').write_text(json.dumps(reports,indent=2)+'\n')
print(json.dumps(reports,indent=2))
