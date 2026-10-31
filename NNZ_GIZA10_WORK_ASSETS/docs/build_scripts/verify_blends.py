import bpy,json
from pathlib import Path
B=Path('/workspace/work/NNZ_GIZA10_WORK_ASSETS');rows=[]
for p in sorted(B.rglob('*.blend')):
 bpy.ops.wm.open_mainfile(filepath=str(p));s=bpy.context.scene
 row={'file':str(p.relative_to(B)),'open_ok':True,'mesh_objects':sum(o.type=='MESH' for o in s.objects),'actions':len(bpy.data.actions),'audio_datablocks':len(bpy.data.sounds),'animation_moves':[]}
 for o in s.objects:
  if o.animation_data and o.animation_data.action:
   s.frame_set(s.frame_start);a=list(o.location)+list(o.rotation_euler)
   s.frame_set(s.frame_end);z=list(o.location)+list(o.rotation_euler)
   row['animation_moves'].append({'object':o.name,'start':a,'end':z,'different':a!=z})
 rows.append(row)
(B/'docs/blender_readback.json').write_text(json.dumps(rows,indent=2))
print('BLEND_READBACK',len(rows),'audio',sum(x['audio_datablocks'] for x in rows))
