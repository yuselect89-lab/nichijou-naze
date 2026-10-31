from pathlib import Path
from PIL import Image
import json,hashlib,struct,xml.etree.ElementTree as ET
B=Path('/workspace/work/NNZ_GIZA10_WORK_ASSETS');errors=[];counts={};alpha=0
for folder in [*[f'C{i:02d}' for i in range(1,7)],'shared','3d_models','stills_for_qc','docs']:
 if not (B/folder).is_dir() or not any((B/folder).iterdir()):errors.append('missing folder '+folder)
for p in B.rglob('*'):
 if not p.is_file():continue
 ext=p.suffix.lower();counts[ext]=counts.get(ext,0)+1
 try:
  if ext=='.png':
   with Image.open(p) as im:im.verify()
   with Image.open(p) as im:
    if 'A' in im.getbands() and im.getchannel('A').getextrema()[0]==0:alpha+=1
    if 'labels' in p.parts or p.parent.name.endswith('_sequence'):
     if im.mode!='RGBA':errors.append('missing RGBA '+str(p.relative_to(B)))
  elif ext=='.json':json.loads(p.read_text())
  elif ext=='.svg':ET.parse(p)
  elif ext=='.glb':
   b=p.read_bytes();magic,ver,n=struct.unpack_from('<4sII',b)
   assert magic==b'glTF' and ver==2 and n==len(b),'invalid GLB header'
   clen,ctyp=struct.unpack_from('<II',b,12);assert ctyp==0x4E4F534A
   d=json.loads(b[20:20+clen]);assert d.get('meshes'),'no meshes'
  elif ext=='.obj':
   txt=p.read_text();assert '\nv ' in txt and '\nf ' in txt,'missing obj geometry'
  elif ext in ['.mp4','.mov','.mp3','.wav','.ogg','.flac','.m4a']:errors.append('unexpected completed-video/audio format '+str(p.relative_to(B)))
 except Exception as e:errors.append(str(p.relative_to(B))+': '+str(e))
seqs=[('C01/guide_sequence',48),('shared/podium/rise_sequence',30)]+[(f'{c}/presenter_entrance_sequence',36) for c in ['C01','C03','C04','C06']]
seqreport=[]
for name,n in seqs:
 fs=sorted((B/name).glob('*.png'));expected=[f'{i:04d}.png' for i in range(1,n+1)]
 if [f.name for f in fs]!=expected:errors.append('sequence frame mismatch '+name)
 hashes={hashlib.sha256(f.read_bytes()).hexdigest() for f in fs}
 if len(hashes)<2:errors.append('motion is static '+name)
 seqreport.append({'sequence':name,'frames':len(fs),'different_frames':len(hashes)})
for i in range(1,7):
 c=f'C{i:02d}';d=json.loads((B/c/'layer_plan.json').read_text())
 for path in [d['background'],d.get('presenter')]+[v[k] for v in d['labels'] for k in ['png','svg']]:
  if path and not (B/path).is_file():errors.append('broken reference '+path)
readback=json.loads((B/'docs/blender_readback.json').read_text())
if len(readback)!=8 or any(not r['open_ok'] or r['audio_datablocks'] for r in readback):errors.append('Blender source readback failed')
report={'technical_result':'PASS' if not errors else 'FAIL','production_complete':False,'notice':'File integrity only. C01 photo absent; historical faces missing; external visual QC not performed; distribution unresolved.','files_by_extension':counts,'transparent_pngs':alpha,'sequences':seqreport,'blend_readback_count':len(readback),'errors':errors}
(B/'docs/asset_technical_qc.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
