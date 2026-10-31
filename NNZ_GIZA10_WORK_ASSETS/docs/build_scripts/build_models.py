import bpy,bmesh,math,json,os
from pathlib import Path
from mathutils import Vector,Matrix
B=Path('/workspace/work/NNZ_GIZA10_WORK_ASSETS');I=Path('/workspace/work/giza10_asset_input/04_GEOMETRY_INPUT')
models=json.loads((I/'GEOMETRY_MANIFEST.json').read_text())
def reset():
 bpy.ops.wm.read_factory_settings(use_empty=True)
 bpy.context.preferences.filepaths.save_version=0
 s=bpy.context.scene;s.unit_settings.system='METRIC';s.render.engine='CYCLES';s.cycles.samples=16;s.cycles.use_denoising=False
 s.render.film_transparent=True;s.render.resolution_x=720;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA'
 s.render.threads_mode='FIXED';s.render.threads=2
 s.world=bpy.data.worlds.new('Studio');s.world.use_nodes=True;s.world.node_tree.nodes.get('Background').inputs[0].default_value=(.17,.20,.25,1);s.world.node_tree.nodes.get('Background').inputs[1].default_value=.4
 s.view_settings.view_transform='AgX'
 return s
def material(name,color,metal=0):
 m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*color,1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=.28
 return m
def import_coin(item):
 before=set(bpy.data.objects);bpy.ops.import_scene.gltf(filepath=str(I/(item['name']+'.glb')))
 imported=set(bpy.data.objects)-before;mesh=[o for o in imported if o.type=='MESH'][0]
 baked=mesh.data.copy();baked.transform(Matrix.Rotation(math.pi/2,4,'X') @ Matrix.Scale(.001,4) @ mesh.matrix_world)
 for o in imported:bpy.data.objects.remove(o,do_unlink=True)
 obj=bpy.data.objects.new(item['name'],baked);bpy.context.collection.objects.link(obj)
 bronze=item['diameter_mm']==23.5
 col=(.48,.25,.105) if bronze else (.57,.61,.66)
 obj.data.materials.clear();obj.data.materials.append(material('Copper_bronze' if bronze else 'Nickel_or_silver_reference',col,.82))
 obj['face_design_status']='MISSING - DO NOT USE AS FINISHED COIN';obj['rim_count_depth_status']='UNVERIFIED';obj['diameter_source']='G2 V2 provided';obj['thickness_source']='INPUT MODEL ESTIMATE';obj['source_geometry']=item['name']+'.glb'
 bm=bmesh.new();bm.from_mesh(obj.data)
 boundary=sum(e.is_boundary for e in bm.edges);nonmanifold=sum(not e.is_manifold for e in bm.edges);bm.free()
 bpy.context.view_layer.update()
 obj['units']='metres';obj['actual_face_relief_present']=False
 return obj,{'name':obj.name,'diameter_m':list(obj.dimensions),'vertices':len(obj.data.vertices),'faces':len(obj.data.polygons),'boundary_edges':boundary,'nonmanifold_edges':nonmanifold,'face_design':'MISSING','rim_parameters':'UNVERIFIED','production_ready':False}
def camera(s,loc=(.023,-.036,.024),target=(0,0,0),scale=.036):
 bpy.ops.object.camera_add(location=loc);c=bpy.context.object;c.rotation_euler=(Vector(target)-c.location).to_track_quat('-Z','Y').to_euler();c.data.clip_start=.0001;c.data.clip_end=10;c.data.type='ORTHO';c.data.ortho_scale=scale;s.camera=c;return c
def light():
 for name,loc,power,size in [('Key',(-.035,-.025,.07),.25,.05),('Rim',(.04,.02,.035),.18,.035)]:
  bpy.ops.object.light_add(type='AREA',location=loc);o=bpy.context.object;o.name=name;o.data.energy=power;o.data.shape='DISK';o.data.size=size;o.rotation_euler=(-o.location).to_track_quat('-Z','Y').to_euler()
def key(o,frame,location=None,rotation=None):
 if location is not None:o.location=location;o.keyframe_insert('location',frame=frame)
 if rotation is not None:o.rotation_euler=rotation;o.keyframe_insert('rotation_euler',frame=frame)
def save(p):
 bpy.context.scene['DELIVERY_STATUS']='PARTIAL: face designs missing; rim parameters unverified; no audio';bpy.ops.wm.save_as_mainfile(filepath=str(p))
audit=[]
for item in models:
 s=reset();obj,report=import_coin(item);camera(s);light()
 target=B/'3d_models'/item['name'];target.mkdir(exist_ok=True)
 # A genuine editable turntable action with hold frames; no audio or fixed narration timing.
 s.render.fps=24;s.frame_start=1;s.frame_end=72
 key(obj,1,rotation=(0,0,0));key(obj,12,rotation=(0,0,0));key(obj,60,rotation=(0,0,math.tau));key(obj,72,rotation=(0,0,math.tau))
 s.frame_set(1);save(target/'model_UNFINISHED.blend')
 bpy.ops.object.select_all(action='DESELECT');obj.select_set(True);bpy.context.view_layer.objects.active=obj
 bpy.ops.export_scene.gltf(filepath=str(target/'model_UNFINISHED.glb'),use_selection=True,export_extras=True,export_animations=True)
 bpy.ops.wm.obj_export(filepath=str(target/'model_UNFINISHED.obj'),export_selected_objects=True)
 s.render.filepath=str(target/'audit_same_camera.png');bpy.ops.render.render(write_still=True)
 report['files']=[str(p.relative_to(B)) for p in target.iterdir() if p.is_file()];audit.append(report)
(B/'3d_models/model_manifest.json').write_text(json.dumps(audit,indent=2))
# Shared 3-D podium with a real rise action. It can render independently of unverified coins.
s=reset();s.render.resolution_x=1080;s.render.resolution_y=1920
pedestalmat=material('Exhibition_blue',(.035,.08,.12),.25);gold=material('Warm_edge',(.8,.49,.17),.7)
for n,x,y,h in [('Left',-.017,.004,.004),('Top',0,.006,.012),('Right',.017,.004,.007)]:
 bpy.ops.mesh.primitive_cube_add(size=1,location=(x,y,h/2));o=bpy.context.object;o.name='Podium_'+n;o.dimensions=(.015,.018,h);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(pedestalmat)
 bevel=o.modifiers.new('Soft edges','BEVEL');bevel.width=.0006;bevel.segments=3;o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
 if n=='Top':key(o,1,location=(x,y,-h/2));key(o,12,location=(x,y,-h/2));key(o,48,location=(x,y,h/2));key(o,60,location=(x,y,h/2))
 bpy.ops.mesh.primitive_cube_add(size=1,location=(x,y,h+.0001));o=bpy.context.object;o.name='Podium_highlight_'+n;o.dimensions=(.014,.017,.0002);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(gold)
 if n=='Top':key(o,1,location=(x,y,0));key(o,12,location=(x,y,0));key(o,48,location=(x,y,h+.0001));key(o,60,location=(x,y,h+.0001))
cam=camera(s,loc=(.042,-.082,.065),target=(0,0,.005),scale=.105);light();s.render.fps=24;s.frame_start=1;s.frame_end=60
p=B/'shared/podium';p.mkdir(exist_ok=True);s.frame_set(60);save(p/'podium_rise.blend');s.render.filepath=str(p/'podium_static.png');bpy.ops.render.render(write_still=True)
# Export independent native action sources C02->C03 and C04->C05, with actual animation but unfinished coin geometry.
for block in ['C02_C03','C04_C05','C06']:
 s=reset();s.render.resolution_x=1080;s.render.resolution_y=1920;s.render.fps=24
 cam=camera(s,loc=(.03,-.075,.10),target=(0,0,0),scale=.095);light()
 if block=='C02_C03':
  coin,_=import_coin(models[0]);s.frame_end=144
  for f,a,y,z in [(1,1.2,0,0),(24,1.2,0,0),(72,.7,0,.003),(120,.18,.012,.012),(144,.18,.012,.012)]:key(coin,f,location=(0,y,z),rotation=(a,0,(f-1)*.008))
  key(cam,1,location=(.03,-.075,.10));key(cam,144,location=(.02,-.055,.12))
  # Native animated podium accompanies coin rise, independently editable.
  bpy.ops.mesh.primitive_cube_add(size=1,location=(0,.012,-.008));o=bpy.context.object;o.name='Top_podium';o.dimensions=(.029,.029,.012);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(material('Podium',(.035,.08,.12),.25));key(o,72,location=(0,.012,-.008));key(o,120,location=(0,.012,.005))
  dest=B/'C02/C02_C03_continuous_motion_UNFINISHED.blend';cuts={'C02':[1,72],'C03':[73,144]}
 elif block=='C04_C05':
  s.frame_end=192
  paths=[[(1,(0,0,0)),(36,(0,0,0)),(72,(-.018,-.012,0)),(144,(-.018,-.012,0)),(180,(-.025,.018,-.015))],[(1,(-.08,.005,0)),(24,(-.08,.005,0)),(60,(0,.008,.012)),(144,(0,.008,.012))],[(1,(.08,.01,0)),(72,(.08,.01,0)),(108,(.018,.026,.024)),(144,(.018,.026,.024))],[(1,(.09,-.01,0)),(144,(.09,-.01,0)),(180,(-.018,-.012,0)),(192,(-.018,-.012,0))]]
  for item,path in zip([models[0],models[2],models[3],models[1]],paths):
   coin,_=import_coin(item)
   for f,loc in path:key(coin,f,location=loc)
   key(coin,108,rotation=(0,0,0));key(coin,132,rotation=(.9,0,0));key(coin,144,rotation=(.9,0,0))
  dest=B/'C04/C04_C05_succession_motion_UNFINISHED.blend';cuts={'C04':[1,120],'C05':[121,192]}
 else:
  s.frame_end=72
  for item,y in [(models[0],.018),(models[1],-.018)]:
   coin,_=import_coin(item)
   for f,a in [(1,.15),(12,.15),(48,1.05),(72,1.05)]:key(coin,f,location=(0,y,0),rotation=(a,0,0))
  # Orthographic view along common axis: same angle, scale and light for both.
  cam.location=(0,-.075,.10);cam.rotation_euler=(Vector((0,0,0))-cam.location).to_track_quat('-Z','Y').to_euler()
  dest=B/'C06/C06_matched_tilt_UNFINISHED.blend';cuts={'C06':[1,72]}
 s.frame_set(1);s['cut_ranges_unsynced']=json.dumps(cuts);save(dest)
print('MODELS_AND_RIGS_DONE')
