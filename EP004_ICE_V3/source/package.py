from pathlib import Path
import json,hashlib,zipfile
R=Path(__file__).resolve().parents[1];repo=R.parent
report=json.loads((R/'qc/stage1_report.json').read_text());assert report['technical_result']=='PASS'
files=[p for p in R.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='SHA256SUMS.txt']
(R/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(R))+'\n' for p in sorted(files)))
files.append(R/'SHA256SUMS.txt')
support=[
 'package.json','package-lock.json','tsconfig.json',
 'common_assets/nichijou_naze/runtime/v1.1.0/components.tsx',
 'common_assets/nichijou_naze/runtime/v1.1.0/config.ts',
 'src/integration/v1.0.1/Series.tsx','src/integration/v1.0.1/Templates.tsx','src/integration/captions.ts','src/integration/character.ts',
 'public/series/v1/NotoSansCJKjp-Bold.otf','public/series/v1/FONT_LICENSE.txt',
 'public/common_assets/nichijou_naze/characters/female_v01/poses/NNZ_CHAR_FEMALE_01_pose_point_right.png',
 'public/ep004-v3/cut01/background.png']
files.extend(repo/p for p in support)
dest=repo/'releases/EP004_ICE_V3_stage1.zip'
if dest.exists():raise RuntimeError('Refusing to overwrite existing release')
with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in sorted(files):z.write(p,str(p.relative_to(repo)))
 z.writestr('README_STAGE1.txt','EP004白い氷V3 第1段階。EP004_ICE_V3/index.htmlを開いてプレビューしてください。\nCut01・Cut09のみ。残り8カットは品質承認待ちです。詳細はEP004_ICE_V3/README.md。\n再レンダリングはZIPルートからnpm ci --cache /tmp/nnz-v3-npm-cache、node EP004_ICE_V3/source/render.mjs。\n')
 z.writestr('PACKAGE_SHA256SUMS.txt',''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(repo))+'\n' for p in sorted(files)))
with zipfile.ZipFile(dest) as z:assert z.testzip() is None
assert dest.stat().st_size<100_000_000
print(json.dumps({'zip':str(dest.relative_to(repo)),'bytes':dest.stat().st_size,'files':len(files),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()},indent=2))
