"""Create immutable download ZIPs; no former releases are modified."""
from pathlib import Path
import json,zipfile,hashlib
R=Path(__file__).resolve().parents[2]
qc=json.loads((R/'validation/extension/qc-report.json').read_text());assert qc['result']=='PASS'
char=R/'common_assets/nichijou_naze/characters/female_v01/versions/v03_expressions'
def package(name,files):
 dest=R/'releases'/name
 if dest.exists():raise RuntimeError('Refusing to overwrite '+name)
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for f in sorted(set(files)):z.write(f,str(f.relative_to(R)))
  checksums=''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(R))+'\n' for f in sorted(set(files)))
  z.writestr('PACKAGE_SHA256SUMS.txt',checksums)
 with zipfile.ZipFile(dest) as z:assert z.testzip() is None
 assert dest.stat().st_size<100_000_000,'GitHub regular file limit'
 print(json.dumps({'zip':name,'bytes':dest.stat().st_size,'files':len(files),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest()}))
small=[p for p in char.rglob('*') if p.is_file()]+[R/'validation/extension/character-8poses.jpg',R/'validation/extension/alpha-backgrounds.jpg']
package('NNZ_CHAR_FEMALE_01_v03_expressions.zip',small)
prefixes=['common_assets','public','src','tools','tests','docs','vendor','examples']
files=[]
for folder in prefixes:files.extend(p for p in (R/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
# Keep every pose/source/implementation. Full36screenshots remain in GitHub;
# this convenient ZIP includes the gallery, atlases, two videos and representative frames.
v=R/'validation/extension'
preview_names=['character-8poses.jpg','alpha-backgrounds.jpg','contact-sheet.jpg','focus-sequence.jpg',
 'library-extension-1080x1920.mp4','video-background-1080x1920.mp4','video-background-60.png',
 'qc-report.json','samples.json','observations.json','protected-files-before.json']
sample_frames=[('expression-surprise',85),('expression-happy',85),('expression-troubled',85),('footage-character',85),('diagram-character',85),('focus-crosssection-return',110),('label-parameters',85),('step3-cause',170),('crosssection-carton',75),('motions',95),('legacy-arrow',85),('legacy-compare',85),('legacy-zoom',85)]
files.extend(v/name for name in preview_names)
files.extend(v/f'{scene}-{frame}.png' for scene,frame in sample_frames)
files.extend(R/name for name in ['package.json','package-lock.json','tsconfig.json','.gitignore','library-registry.json','README.md'])
package('NNZ_COMMON_LIBRARY_EXTENSION_v1.1.0.zip',files)
