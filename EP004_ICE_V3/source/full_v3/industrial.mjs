import * as T from '../vendor/three/three.module.js';
import {parameters as P,smooth} from '../physics.mjs';
import {aerationState} from './states.mjs';

export function createAerationScene(canvas){
 const renderer=new T.WebGLRenderer({canvas,alpha:true,antialias:true,preserveDrawingBuffer:true});
 renderer.setSize(1080,1920,false);renderer.setPixelRatio(1);renderer.outputColorSpace=T.SRGBColorSpace;renderer.toneMapping=T.ACESFilmicToneMapping;renderer.toneMappingExposure=1.15;
 renderer.shadowMap.enabled=true;renderer.shadowMap.type=T.PCFSoftShadowMap;
 const scene=new T.Scene();scene.background=new T.Color('#e9f0ee');
 const camera=new T.OrthographicCamera(-2.8,2.8,4.977,-4.977,.1,100);camera.position.set(3,9.6,18);camera.lookAt(.05,2.25,0);camera.updateMatrixWorld();
 const groups={};for(const n of ['ice','can','liquid','pipe','receiver','set']){groups[n]=new T.Group();groups[n].name=n;scene.add(groups[n]);}
 const physical=(c,extra={})=>new T.MeshPhysicalMaterial({color:c,roughness:.23,...extra});
 const mats={ice:physical('#e1f6ff',{roughness:.065,transmission:.94,thickness:.8,ior:1.31,attenuationColor:'#9fdde9',attenuationDistance:7,clearcoat:.85,clearcoatRoughness:.1}),iceEdge:physical('#e7fbff',{roughness:.18}),steel:physical('#a4b6ba',{metalness:.85,roughness:.27}),edge:physical('#d7e6e8',{metalness:.8,roughness:.2}),water:physical('#259dbb',{roughness:.19,transmission:.24,thickness:.12,ior:1.333,clearcoat:.55}),surface:physical('#53c2d0',{roughness:.28,transmission:.12,ior:1.333,clearcoat:.25}),hose:physical('#c9eef0',{roughness:.12,transparent:true,opacity:.37,depthWrite:false}),flow:physical('#038da6',{roughness:.15,emissive:'#005f7f',emissiveIntensity:.15}),white:physical('#e5ece8',{roughness:.9}),floor:physical('#cbd5cf',{metalness:.25,roughness:.43}),receiver:physical('#bdeaf0',{transparent:true,opacity:.2,roughness:.1,depthWrite:false}),dark:physical('#1e505e',{metalness:.4,roughness:.28})};
 const mesh=(geometry,material,group,name)=>{const o=new T.Mesh(geometry,material);o.name=name;groups[group].add(o);o.castShadow=true;o.receiveShadow=true;return o;};
 const box=(name,x,y,z,w,h,d,mat,group)=>{const o=mesh(new T.BoxGeometry(w,h,d),mat,group,name);o.position.set(x,y,z);return o;};
 const tube=(name,points,radius,mat,group,curveType='catmull')=>{let c;
 if(curveType==='poly'){c=new T.CurvePath();for(let i=1;i<points.length;i++)c.add(new T.LineCurve3(new T.Vector3(...points[i-1]),new T.Vector3(...points[i])));}
 else c=new T.CatmullRomCurve3(points.map(p=>new T.Vector3(...p)),false,'centripetal');
 const o=mesh(new T.TubeGeometry(c,100,radius,12,false),mat,group,name);return {object:o,curve:c};};
 const cylinder=(name,radius,length,mat,group)=>mesh(new T.CylinderGeometry(radius,radius,length,24),mat,group,name);
 // Neutral photographic-style room illumination generated from original emissive geometry.
 const envScene=new T.Scene();envScene.background=new T.Color('#e9f1f3');
 const panel=(x,y,z,w,h,color)=>{const o=new T.Mesh(new T.PlaneGeometry(w,h),new T.MeshBasicMaterial({color,side:T.DoubleSide}));o.position.set(x,y,z);o.lookAt(0,1,0);envScene.add(o);};
 panel(-4,3,0,5,7,'#ffffff');panel(4,2,1,4,6,'#ecf6ff');panel(0,5,-2,6,3,'#ffffff');panel(0,0,3,8,3,'#a7b8b8');panel(1,1,-4,3,8,'#4d737b');
 const pmrem=new T.PMREMGenerator(renderer);scene.environment=pmrem.fromScene(envScene,.04,.1,30).texture;
 const ambient=new T.HemisphereLight('#edf8ff','#a0a99f',2.4);scene.add(ambient);
 const key=new T.DirectionalLight('#f6fcff',4.0);key.position.set(-5,9,7);key.castShadow=true;key.shadow.mapSize.set(1024,1024);key.shadow.camera.left=-6;key.shadow.camera.right=6;key.shadow.camera.top=8;key.shadow.camera.bottom=-5;key.shadow.normalBias=.025;key.shadow.bias=-.00015;scene.add(key);
 const fill=new T.DirectionalLight('#d8f6ff',1.8);fill.position.set(4,5,-5);scene.add(fill);
 const CX=-.6;
 // Contiguous U-shaped freezing shell. Inner opening shrinks smoothly; final dimensions match approved Cut09.
 const outline=[[-1.38,.58],[1.38,.58],[1.38,4.6],[.62,4.6],[.62,1.0],[-.62,1.0],[-.62,4.6],[-1.38,4.6]];
 const shape=new T.Shape();outline.forEach(([x,y],i)=>i?shape.lineTo(x+CX,y):shape.moveTo(x+CX,y));shape.closePath();
 const iceGeo=new T.ExtrudeGeometry(shape,{depth:1.4,bevelEnabled:true,bevelSize:.028,bevelThickness:.028,bevelSegments:3,steps:1});iceGeo.translate(0,0,-.76);const solid=mesh(iceGeo,mats.ice,'ice','INVARIANT_CONTIGUOUS_ICE');
 box('Ice back wall',CX,2.8,-.78,1.23,3.6,.2,mats.ice,'ice');
 const edgeGeo=new T.EdgesGeometry(iceGeo,35);const lines=new T.LineSegments(edgeGeo,new T.LineBasicMaterial({color:'#a8dce9',transparent:true,opacity:.66}));groups.ice.add(lines);
 for(const x of [-1.46,1.46]){box('Can side',CX+x,2.56,-.08,.11,4.18,1.68,mats.steel,'can');box('Bright cut edge',CX+x,2.56,.78,.045,4.18,.045,mats.edge,'can');}
 box('Can base',CX,.47,-.08,3.03,.16,1.68,mats.steel,'can');
 // The opaque back is omitted in this explanatory cutaway too, so the ICE can be seen through.
 for(const x of [CX-1.1,CX+1.1])box('Can foot',x,.22,-.1,.34,.35,.9,mats.steel,'can');
 const liquid=box('CENTRAL_LIQUID',CX,P.bottom+P.initialHeight/2,.035,P.width,P.initialHeight,P.depth,mats.water,'liquid');liquid.castShadow=false;
 const surfaceGeo=new T.PlaneGeometry(P.width,P.depth,28,22);surfaceGeo.rotateX(-Math.PI/2);
 const surface=mesh(surfaceGeo,mats.surface,'liquid','DESCENDING_MENISCUS');surface.position.set(CX,P.bottom+P.initialHeight,.035);surface.castShadow=false;
 const meniscusEdge=tube('Visible free surface edge',[[CX-P.width/2,P.bottom+P.initialHeight,.62],[CX+P.width/2,P.bottom+P.initialHeight,.62]],.013,mats.surface,'liquid','poly').object;
 // Fixed discharge hose and descending intake. Unlike a gas inlet, this is a suction-only path.
 const upperPoints=[[CX+.24,4.83,.02],[CX+.25,5.03,.02],[CX+.48,5.14,.02],[1.40,5.14,.02],[1.63,4.96,.02],[1.63,1.98,.02]];
 const upper=tube('Discharge hose',upperPoints,.081,mats.hose,'pipe');
 const upperFlow=tube('Water inside hose',upperPoints,.034,mats.flow,'pipe');upperFlow.object.castShadow=false;
 const intake=cylinder('Descending suction lance',.081,1,mats.hose,'pipe');const inside=cylinder('Water rising in lance',.036,1,mats.flow,'pipe');inside.castShadow=false;
 const tip=cylinder('Suction intake mouth',.095,.11,mats.dark,'pipe');tip.position.set(CX+.24,1.06,.02);
 box('Small suction pump',1.18,5.14,.02,.32,.30,.29,mats.edge,'pipe');box('Pump blue inset',1.18,5.14,.18,.17,.12,.025,mats.flow,'pipe');
 // Receiver has real depth, matching the volume balance, rather than an undersized bucket.
 const RX=1.63,RZ=-1.30,RW=1.12,RD=3.8,RB=.39,RH=1.46;
 box('Receiver base',RX,RB,RZ,RW,.06,RD,mats.receiver,'receiver');
 for(const x of [RX-RW/2,RX+RW/2])box('Receiver side',x,RB+RH/2,RZ,.035,RH,RD,mats.receiver,'receiver');
 box('Receiver back',RX,RB+RH/2,RZ-RD/2,RW,RH,.035,mats.receiver,'receiver');
 tube('Receiver rim',[[RX-RW/2,RB+RH,RZ+RD/2],[RX-RW/2,RB+RH,RZ-RD/2],[RX+RW/2,RB+RH,RZ-RD/2],[RX+RW/2,RB+RH,RZ+RD/2]],.025,mats.edge,'receiver','poly');
 const collected=box('COLLECTED_LIQUID',RX,P.receiverBottom,RZ,P.receiverWidth,.01,P.receiverDepth,mats.water,'liquid');collected.castShadow=false;
 const collectedSurface=box('Rising received surface',RX,P.receiverBottom,RZ,P.receiverWidth,.012,P.receiverDepth,mats.surface,'liquid');collectedSurface.castShadow=false;
 const jet=cylinder('Visible discharge stream',.038,1,mats.flow,'liquid');jet.position.x=RX;jet.position.z=.02;jet.castShadow=false;
 // Moving highlights show a direction and not extra air bubbles being injected.
 const pulses=[];for(let i=0;i<7;i++){const o=mesh(new T.SphereGeometry(.052,10,8),new T.MeshBasicMaterial({color:'#b8fbff'}),'pipe','Liquid flow highlight');o.scale.set(.68,1.7,.68);o.castShadow=false;pulses.push(o);}
 // All original background geometry; no logos, textures or factory stock images.
 box('Worktop',0,-.12,0,22,.26,18,mats.floor,'set');box('Tile wall',0,4.4,-3.7,22,9,.15,mats.white,'set');
 const seam=physical('#b9ccc9',{roughness:1});for(const y of [1,2.5,4,5.5,7])box('Horizontal tile joint',0,y,-3.61,22,.015,.012,seam,'set');for(const x of [-6,-3,0,3,6])box('Vertical tile joint',x,4.4,-3.61,.015,9,.012,seam,'set');
 box('Soft window surround',-4.5,5.2,-3.48,2.6,4.5,.15,mats.edge,'set');box('Daylight glazing',-4.5,5.2,-3.36,2.25,4.15,.06,new T.MeshBasicMaterial({color:'#f7fcff'}),'set');
 box('Distant stainless unit',4,2,-2.8,2.2,3.7,1,mats.steel,'set');

 const airGroup=new T.Group();scene.add(airGroup);
 const airMat=new T.MeshPhysicalMaterial({color:'#d59a3a',roughness:.28,transparent:true,opacity:1});
 const airCurve=new T.CatmullRomCurve3([new T.Vector3(CX-1,5.12,.02),new T.Vector3(CX+.24,5.12,.02),new T.Vector3(CX+.24,1.06,.02)]);
 const airHose=new T.Mesh(new T.TubeGeometry(airCurve,80,.065,12,false),airMat);airHose.renderOrder=9;airMat.depthTest=false;airGroup.add(airHose);
 const diffuser=new T.Mesh(new T.CylinderGeometry(.12,.12,.12,20),airMat);diffuser.position.set(CX+.24,1.07,.02);diffuser.renderOrder=9;airGroup.add(diffuser);
 const airBubbles=[];for(let i=0;i<14;i++){const o=new T.Mesh(new T.SphereGeometry(.045+(i%3)*.009,12,10),new T.MeshPhysicalMaterial({color:'#f5ffff',transparent:true,opacity:.7,roughness:.1,transmission:0,ior:1.0,depthTest:false}));o.renderOrder=10;airGroup.add(o);airBubbles.push(o);}
 const residual=[];for(let i=0;i<9;i++){const o=new T.Mesh(new T.OctahedronGeometry(.025),new T.MeshBasicMaterial({color:'#b78737',depthTest:false}));o.renderOrder=11;groups.liquid.add(o);residual.push(o);}
 for(let i=0;i<3;i++)box('Other freezing cans',-4.4-i*1.4,2.3,-2.2,1.1,4.4,1.1,mats.steel,'set');

 const targetPoints=[];
 for(const n of ['ice','can','receiver','pipe']){
  groups[n].updateWorldMatrix(true,true);const b=new T.Box3().setFromObject(groups[n]);
  for(const x of [b.min.x,b.max.x])for(const y of [b.min.y,b.max.y])for(const z of [b.min.z,b.max.z])targetPoints.push(new T.Vector3(x,y,z));
 }
 // Fit all important 3D geometry into the established safe area without shrinking the backdrop.
 camera.updateMatrixWorld();const local=targetPoints.map(p=>p.clone().applyMatrix4(camera.matrixWorldInverse));
 const minX=Math.min(...local.map(p=>p.x)),maxX=Math.max(...local.map(p=>p.x)),minY=Math.min(...local.map(p=>p.y)),maxY=Math.max(...local.map(p=>p.y));
 const h=Math.max((maxX-minX)*1920/800,(maxY-minY)*1920/1000),pp=1920/h;
 const right=new T.Vector3().setFromMatrixColumn(camera.matrixWorld,0),up=new T.Vector3().setFromMatrixColumn(camera.matrixWorld,1);
 const deltaX=(minX+maxX)/2-(500-540)/pp,deltaY=(minY+maxY)/2-(960-865)/pp;
 camera.position.addScaledVector(right,deltaX).addScaledVector(up,deltaY);camera.left=-h*.5625/2;camera.right=h*.5625/2;camera.top=h/2;camera.bottom=-h/2;camera.updateProjectionMatrix();camera.updateMatrixWorld();
 const project=(x,y,z)=>{const v=new T.Vector3(x,y,z).project(camera);return {x:(v.x+1)*540,y:(1-v.y)*960};};
 const anchors={solid:project(CX-1.0,3.3,.66),water:project(CX,2.9,.64),pipe:project(CX+.24,4.45,.02),outlet:project(RX,1.98,.02),receiver:project(RX,1.15,.45),coreBottom:project(CX,1.02,.64)};
 const projected=targetPoints.map(p=>project(p.x,p.y,p.z));const importantBounds={left:Math.min(...projected.map(p=>p.x)),right:Math.max(...projected.map(p=>p.x)),top:Math.min(...projected.map(p=>p.y)),bottom:Math.max(...projected.map(p=>p.y))};
 const solidSignature=Array.from(solid.geometry.attributes.position.array).reduce((n,v,i)=>n+v*(i%13+1),0);
 function draw(frame,mode='all'){
  const st=aerationState(frame),q=st.freezeProgress;
  const outline=[[-1.38,.58],[1.38,.58],[1.38,4.6],[st.innerHalf,4.6],[st.innerHalf,st.bottom-.025],[-st.innerHalf,st.bottom-.025],[-st.innerHalf,4.6],[-1.38,4.6]];
  const shape=new T.Shape();outline.forEach(([x,y],i)=>i?shape.lineTo(x+CX,y):shape.moveTo(x+CX,y));shape.closePath();
  const g=new T.ExtrudeGeometry(shape,{depth:1.4,bevelEnabled:true,bevelSize:.028,bevelThickness:.028,bevelSegments:3,steps:1});g.translate(0,0,-.76);solid.geometry.dispose();solid.geometry=g;lines.geometry.dispose();lines.geometry=new T.EdgesGeometry(g,35);
  const width=2*st.innerHalf-.09;liquid.scale.set(width/P.width,st.liquidHeight/P.initialHeight,1);liquid.position.y=st.bottom+st.liquidHeight/2;
  surface.scale.x=width/P.width;surface.position.y=4.413;meniscusEdge.visible=false;
  for(const [name,group] of Object.entries(groups))group.visible=mode==='all'||(mode==='background'?name==='set':name!=='set');
  groups.receiver.visible=false;groups.pipe.visible=false;collected.visible=false;collectedSurface.visible=false;jet.visible=false;
  airGroup.visible=mode!=='background';airMat.opacity=1-st.withdraw;
  airBubbles.forEach((o,i)=>{const phase=(frame*.013+i/14)%1;o.position.set(CX+.24+Math.sin(phase*8+i)*.08,1.14+phase*3.1,.02+Math.cos(i+phase*5)*.05);o.visible=st.airActive;});
  residual.forEach((o,i)=>o.position.set(CX+Math.sin(i*2.4+frame/180)*st.innerHalf*.6,1.4+(i%5)*.55,Math.cos(i)*.32));
  camera.zoom=.78+.22*smooth(frame/35);camera.updateProjectionMatrix();scene.background=mode==='model'?null:new T.Color('#e9f0ee');renderer.setClearColor('#e9f0ee',mode==='model'?0:1);renderer.render(scene,camera);
  return {frame,cut:8,...st,mode,anchors,importantBounds,geometryMatchesCut09AtEnd:q===1,airInjection:true,suction:false,fastVortex:false,waterLevel:4.405};
 }
 draw(0);return {draw,anchors,renderer,dispose(){scene.traverse(o=>{if(o.geometry)o.geometry.dispose();});renderer.dispose();pmrem.dispose();}};
}
