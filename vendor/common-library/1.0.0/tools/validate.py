#!/usr/bin/env python3
from pathlib import Path
import json,subprocess
from jsonschema import validate
from PIL import Image
r=Path(__file__).resolve().parent.parent/'common_assets/nichijou_naze'
for name,frames in [('arrow_01',150),('compare_01',180),('zoom_01',150)]:
 p=r/'diagram_templates'/name
 conf=json.loads((p/'example.json').read_text())
 schema=json.loads((p/'schema.json').read_text())
 validate(conf,schema)
 assert (p/'template.tsx').stat().st_size>400
 assert Image.open(p/'thumb.png').size==(1080,1920)
 d=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=width,height,r_frame_rate,nb_frames','-of','json',str(p/'preview.mp4')]))['streams'][0]
 assert d['width']==1080 and d['height']==1920 and d['r_frame_rate']=='30/1' and int(d['nb_frames'])==frames,(name,d)
 print('PASS',name,frames,'frames')
assert len(list((r/'characters/female_v01/poses').glob('*.png')))==8
for name in ['label_01','step3_01','crosssection_01']:
 assert '未実装' in (r/'diagram_templates'/name/'README.md').read_text()
print('PASS 8 female poses + 3 planned placeholders')
