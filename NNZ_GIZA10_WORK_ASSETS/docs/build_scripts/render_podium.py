import bpy,json
from pathlib import Path
B=Path('/workspace/work/NNZ_GIZA10_WORK_ASSETS')
bpy.ops.wm.open_mainfile(filepath=str(B/'shared/podium/podium_rise.blend'))
s=bpy.context.scene;s.cycles.samples=8;s.cycles.use_denoising=False
s.render.resolution_x=1080;s.render.resolution_y=1920
p=B/'shared/podium/rise_sequence';p.mkdir(exist_ok=True)
for k in range(30):
 s.frame_set(1+k*2);s.render.filepath=str(p/f'{k+1:04d}.png');bpy.ops.render.render(write_still=True)
(B/'shared/podium/motion.json').write_text(json.dumps({'sequence':'rise_sequence/%04d.png','frames':30,'fps':12,'duration_editorial_seconds':2.5,'source_fps':24,'source_frames':[1,59,2],'resolution':[1080,1920],'alpha':'RGBA straight','scope':'isolated podium; no coins/labels/presenter/audio'},indent=2))
print('PODIUM_SEQUENCE_DONE')
