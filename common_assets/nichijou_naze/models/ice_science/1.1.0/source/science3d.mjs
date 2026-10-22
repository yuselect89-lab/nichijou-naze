import * as T from '../vendor/three/three.module.js';
import {freezingState} from './states.mjs';
export function createScienceScene(canvas,cut){
 const renderer=new T.WebGLRenderer({canvas,alpha:true,antialias:true,preserveDrawingBuffer:true});renderer.setSize(1080,1920,false);renderer.setPixelRatio(1);renderer.outputColorSpace=T.SRGBColorSpace;renderer.toneMapping=T.ACESFilmicToneMapping;renderer.toneMappingExposure=1.12;renderer.shadowMap.enabled=true;renderer.shadowMap.type=T.PCFSoftShadowMap;
 const scene=new T.Scene();scene.background=new T.Color('#eaf1ef');
 const camera=new T.OrthographicCamera(-2.7,2.7,4.8,-4.8,.1,80);camera.position.set(4,6.5,13);camera.lookAt(0,2,0);camera.updateMatrixWorld();
 const rig=new T.Group();scene.add(rig);const backdrop=new T.Group();scene.add(backdrop);
 const mat=(color,extra={})=>new T.MeshPhysicalMaterial({color,roughness:.21,...extra});
 const ice=mat('#dff7ff',{transmission:0,transparent:true,opacity:.20,depthWrite:false,thickness:.5,ior:1.31,roughness:.09,clearcoat:.7}),water=mat('#43b4cc',{transmission:.25,roughness:.2}),white=mat('#e6eeeb',{roughness:.83}),trayMat=mat('#bccdce',{roughness:.38}),air=new T.MeshPhysicalMaterial({color:'#edfcff',transmission:.7,roughness:.08,ior:1.0,transparent:true,opacity:.38,side:T.DoubleSide,depthWrite:false});
 const cavity=new T.ShaderMaterial({transparent:true,depthWrite:false,depthTest:false,uniforms:{strength:{value:1}},vertexShader:'varying vec3 n;varying vec3 v;void main(){vec4 p=modelViewMatrix*vec4(position,1.0);n=normalize(normalMatrix*normal);v=normalize(-p.xyz);gl_Position=projectionMatrix*p;}',fragmentShader:'uniform float strength;varying vec3 n;varying vec3 v;void main(){float rim=pow(1.0-abs(dot(normalize(n),normalize(v))),2.0);float shine=pow(max(0.0,dot(normalize(n),normalize(vec3(-.5,.8,1.0)))),28.0);gl_FragColor=vec4(mix(vec3(.22,.49,.57),vec3(1.0),shine),strength*(.07+.80*rim+.7*shine));}'});const env=new T.Scene();env.background=new T.Color('#e4edf1');for(const [x,y,z,w,h,c] of [[-4,3,0,5,7,'#ffffff'],[4,3,0,4,6,'#dbeaf3'],[0,6,-3,6,4,'#ffffff'],[0,1,-4,3,7,'#537d87']]){const p=new T.Mesh(new T.PlaneGeometry(w,h),new T.MeshBasicMaterial({color:c,side:T.DoubleSide}));p.position.set(x,y,z);p.lookAt(0,2,0);env.add(p);}
 const pmrem=new T.PMREMGenerator(renderer);scene.environment=pmrem.fromScene(env,.03,.1,30).texture;
 scene.add(new T.HemisphereLight('#f1faff','#a0b9b8',2.1));const key=new T.DirectionalLight('#ffffff',3.3);key.position.set(-5,8,7);key.castShadow=true;key.shadow.mapSize.set(1024,1024);key.shadow.camera.left=-5;key.shadow.camera.right=5;key.shadow.camera.top=7;key.shadow.camera.bottom=-3;key.shadow.normalBias=.02;scene.add(key);const fill=new T.DirectionalLight('#c9efff',1.8);fill.position.set(4,5,-3);scene.add(fill);
 function box(name,x,y,z,w,h,d,m,parent=rig){const o=new T.Mesh(new T.BoxGeometry(w,h,d),m);o.name=name;o.position.set(x,y,z);o.castShadow=true;o.receiveShadow=true;parent.add(o);return o;}
 box('Countertop',0,-.17,0,20,.25,20,mat('#ccd9d3',{roughness:.47,metalness:.1}),backdrop);box('Wall',0,4,-4,22,9,.1,white,backdrop);
 for(const y of [1,2.5,4,5.5,7])box('Wall joint',0,y,-3.94,22,.013,.015,mat('#c5d7d4'),backdrop);
 box('Window glow',-5,4.8,-3.82,3,4,.05,new T.MeshBasicMaterial({color:'#f7fcff'}),backdrop);
 const bubbleGroup=new T.Group();rig.add(bubbleGroup);const bubbles=[];
 for(let i=0;i<(cut===5?13:cut===7?200:76);i++){
  const angle=i*2.399963,r=.12+.55*((i*37%101)/101),y=Math.sin(i*1.71)*.63;
  const o=new T.Mesh(new T.SphereGeometry(cut===5?.12+(i%3)*.024:.025+(i%4)*.008,16,12),cavity.clone());o.position.set(Math.cos(angle)*r,2.2+y,Math.sin(angle)*r*.8);if(cut===7){o.position.x*=.45;o.position.y=2.2+(o.position.y-2.2)*.45;o.position.z*=.45;o.scale.setScalar(.65);}o.renderOrder=10;bubbleGroup.add(o);bubbles.push(o);
  if(cut===5&&i===0)o.position.set(0,2.2,.25);
 }
 const gas=new T.Group();rig.add(gas);const markers=[];
 for(let i=0;i<22;i++){const o=new T.Mesh(new T.OctahedronGeometry(.035),new T.MeshBasicMaterial({color:'#c98727',transparent:true,depthTest:false}));o.renderOrder=11;gas.add(o);markers.push({o,n:new T.Vector3(Math.sin(i*2.4)*.8,Math.cos(i*1.7)*.8,Math.sin(i*.9)*.7)});}
 const walls=[];for(let i=0;i<5;i++)walls.push(box('Growing solid ice wall'+i,0,2.2,0,1,1,1,ice));
 const liquid=box('Liquid core',0,2.2,.03,1,1,1,water);const centerIce=box('Last frozen center',0,2.2,.03,.72,.7,.68,ice.clone());centerIce.material.transparent=true;centerIce.material.opacity=0;
 const simpleIce=box('Magnified ice',0,2.2,0,3.4,3.1,2.0,ice);const edgeLines=new T.LineSegments(new T.EdgesGeometry(simpleIce.geometry),new T.LineBasicMaterial({color:'#8bbaca',transparent:true,opacity:.65}));edgeLines.position.copy(simpleIce.position);rig.add(edgeLines);
 const tray=[];tray.push(box('Household tray base',0,.57,0,3.45,.16,2.48,trayMat));for(const x of [-1.68,1.68])tray.push(box('Tray side',x,2.18,0,.13,3.15,2.48,trayMat));tray.push(box('Tray back',0,2.18,-1.18,3.45,3.15,.13,trayMat));
 const beams=new T.Group();rig.add(beams);const rays=[];
 function ray(points,color,radius=.018){const curve=new T.CatmullRomCurve3(points.map(p=>new T.Vector3(...p)),false,'centripetal');const o=new T.Mesh(new T.TubeGeometry(curve,30,radius,8,false),new T.MeshBasicMaterial({color,transparent:true,opacity:.8}));beams.add(o);return {curve,o};}
 const incident=ray([[-2.05,2.2,.25],[0,2.2,.25]],'#df9b16',.035);rays.push(incident);
 for(const [x,y,z] of [[1.9,3.5,.2],[2,2.6,.8],[1.8,1.1,.3],[-1.8,3.4,.5],[-1.5,1.0,.5],[.3,3.9,-.8],[1.2,2.1,1.8]])rays.push(ray([[0,2.2,.25],[x,y,z]],'#c48e20',.018));
 const pulses=rays.map(()=>{const o=new T.Mesh(new T.SphereGeometry(.048,12,8),new T.MeshBasicMaterial({color:'#fff6c2'}));beams.add(o);return o;});
 // One consistent screen placement, leaving actual fullbleed3D surroundings visible.
 camera.zoom=.99;camera.updateProjectionMatrix();camera.updateMatrixWorld();const desiredY=790;const v=new T.Vector3(0,2.2,0).project(camera);const pp=1920/(9.6/camera.zoom);const up=new T.Vector3().setFromMatrixColumn(camera.matrixWorld,1),right=new T.Vector3().setFromMatrixColumn(camera.matrixWorld,0);camera.position.addScaledVector(up,((1-v.y)*960-desiredY)/-pp).addScaledVector(right,40/pp);camera.updateMatrixWorld();
 const project=(p)=>{const q=p.clone().project(camera);return {x:(q.x+1)*540,y:(1-q.y)*960};};
 const modelPoints=[];for(const x of [-1.8,1.8])for(const y of [.45,3.9])for(const z of [-1.3,1.3])modelPoints.push(project(new T.Vector3(x,y,z)));
 const bounds={left:Math.min(...modelPoints.map(p=>p.x)),right:Math.max(...modelPoints.map(p=>p.x)),top:Math.min(...modelPoints.map(p=>p.y)),bottom:Math.max(...modelPoints.map(p=>p.y))};
 function draw(frame,mode='all'){
  const st=freezingState(frame),q=st.progress;
  simpleIce.visible=cut!==7;edgeLines.visible=cut!==7;walls.forEach(o=>o.visible=cut===7);liquid.visible=cut===7;centerIce.visible=cut===7;gas.visible=cut===7;tray.forEach(o=>o.visible=cut===7);beams.visible=cut===5;
  if(cut===7){
   const x=st.halfX,y=st.halfY,z=st.halfZ;
   const values=[[-(1.5+x)/2,2.2,0,1.5-x,3,2],[(1.5+x)/2,2.2,0,1.5-x,3,2],[0,.7+(1.5-y)/2,0,2*x,1.5-y,2],[0,3.7-(1.5-y)/2,0,2*x,1.5-y,2],[0,2.2,-(1+z)/2,2*x,2*y,1-z]];
   walls.forEach((o,i)=>{const [a,b,c,d,e,f]=values[i];o.position.set(a,b,c);o.scale.set(Math.max(.001,d),Math.max(.001,e),Math.max(.001,f));});
   liquid.scale.set(2*x,2*y,2*z);liquid.material.transparent=true;liquid.material.opacity=st.liquidOpacity;centerIce.material.opacity=1-st.liquidOpacity;
   for(const {o,n} of markers){o.position.set(n.x*x,2.2+n.y*y,n.z*z);o.material.opacity=st.gasMarkerOpacity;}
   bubbles.forEach(o=>{o.material.uniforms.strength.value=st.bubbleOpacity;});
  }else{bubbles.forEach(o=>{o.material.uniforms.strength.value=1});}
  if(cut===4){rig.rotation.y=.08*Math.sin(frame/150*Math.PI);camera.zoom=.99+.08*Math.min(1,frame/149);camera.updateProjectionMatrix();}
  if(cut===5){pulses.forEach((o,i)=>{const phase=((frame/30*.75)-(i? .36:0))%1;o.visible=phase>=0;o.position.copy(rays[i].curve.getPointAt(Math.max(0,phase)));});}
  rig.visible=mode!=='background';backdrop.visible=mode!=='model';scene.background=mode==='model'?null:new T.Color('#eaf1ef');renderer.setClearColor('#eaf1ef',mode==='model'?0:1);renderer.render(scene,camera);
  return {frame,cut,...st,mode,bounds,bubbleCount:bubbles.length,airCavities:true,rayBranches:cut===5?7:0,boilingBubblesRepresentDissolvedGas:false};
 }
 draw(0);return {draw,dispose(){scene.traverse(o=>{o.geometry?.dispose()});renderer.dispose();pmrem.dispose()}};
}
