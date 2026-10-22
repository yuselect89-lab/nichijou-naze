from pathlib import Path
import shutil,subprocess,json,os,hashlib
R=Path(__file__).resolve().parents[2];repo=R.parent
assert 'complete 7' in Path('/tmp/nnz-full-final7.log').read_text(),'Cut07 render still running'
assert 'complete 8' in Path('/tmp/nnz-full-final8-stills.log').read_text(),'Cut08 render still running'
assert (R/'qc/full_v3/cut08_label_revision.json').exists(),'Cut08 label finishing still pending'
D=R/'qc/full_v3/revised_cut07'
for name in ['main.png','base_animation.mp4','labels_overlay.webm','animation.mp4']:assert (D/name).stat().st_size>0
for p in D.iterdir():shutil.move(p,R/'cut07'/p.name)
D.rmdir()
def run(args,env=None):subprocess.run(args,cwd=repo,env={**os.environ,**(env or {})},check=True)
run(['node','EP004_ICE_V3/source/full_v3/render.mjs','--media'],{'CUTS':'7','LAYERS':'base'})
run(['python','EP004_ICE_V3/source/full_v3/encoded_previews.py'])
run(['python','EP004_ICE_V3/source/full_v3/metadata.py'])
run(['python','EP004_ICE_V3/source/full_v3/previews.py'])
run(['python','EP004_ICE_V3/source/full_v3/qc.py'])
print('ALL CUTS RENDERED / TECHNICAL QC PASS. Inspect final contact sheet before packaging.')
