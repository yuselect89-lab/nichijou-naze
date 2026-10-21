#!/usr/bin/env python3
"""Copy public images + TSX templates to an existing Remotion project without overwriting by default."""
import argparse,shutil
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--target',required=True,help='Directory containing package.json and src/')
p.add_argument('--overwrite',action='store_true');a=p.parse_args()
base=Path(__file__).resolve().parent.parent/'common_assets/nichijou_naze';out=Path(a.target)
if not (out/'package.json').exists() or not (out/'src').is_dir():raise SystemExit('Target is not a verified Remotion/React project (package.json + src/ required)')
files=list((base/'characters').rglob('*.png'))+list((base/'props').rglob('*.svg'))+list((base/'diagram_templates').rglob('*.tsx'))
written=[];skipped=[]
for src in files:
 rel=src.relative_to(base)
 dest=out/('src/common_assets/nichijou_naze' if src.suffix=='.tsx' else 'public/common_assets/nichijou_naze')/rel
 if dest.exists() and not a.overwrite:skipped.append(str(dest));continue
 dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest);written.append(str(dest))
print(f'copied={len(written)} skipped={len(skipped)}')
if skipped:print('Files existed; no overwrite. Use --overwrite only after reviewing changes.')
