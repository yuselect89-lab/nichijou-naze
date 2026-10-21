import React,{useRef,useState,useEffect,useLayoutEffect} from 'react';
import {registerRoot,Composition,AbsoluteFill,Img,staticFile,useCurrentFrame,delayRender,continueRender,cancelRender} from 'remotion';
import {createIceScene} from './scene3d.mjs';
import {drainageState,smooth} from './physics.mjs';
import {CharacterLayer} from '../../common_assets/nichijou_naze/runtime/v1.1.0/components';
import {FontReady,fonts} from '../../src/integration/v1.0.1/Series';
const ThreeScene=({mode='all',report=false})=>{
 const ref=useRef(null),engine=useRef(null),frame=useCurrentFrame();const [handle]=useState(()=>delayRender('EP004 V3 3D scene'));
 useLayoutEffect(()=>{try{engine.current=createIceScene(ref.current);const st=engine.current.draw(frame,mode);if(report)console.log('EP004_V3_QC '+JSON.stringify(st));continueRender(handle);}catch(e){cancelRender(e)}return()=>{engine.current?.dispose();engine.current=null}},[]);
 useLayoutEffect(()=>{if(engine.current){const st=engine.current.draw(frame,mode);if(report)console.log('EP004_V3_QC '+JSON.stringify(st));}},[frame,mode]);
 return <canvas ref={ref} style={{position:'absolute',inset:0,width:1080,height:1920}}/>;
};
const Char=()=> <CharacterLayer durationFrames={165} config={{side:'left',top:1140,height:320,entry:'fade',enterFrame:13,exitFrame:145,idle:true,nodAt:[110],poses:[{fromFrame:0,pose:'point_right'}]}}/>;
const Labels=()=>{const f=useCurrentFrame(),st=drainageState(f),waterY=1096-(st.coreHeight*.5+.005)*150.68;return <>
 <div style={{position:'absolute',left:90,top:330,color:'#276173',fontSize:36,fontWeight:700,letterSpacing:2}}>製氷缶の断面 <span style={{fontSize:28}}>模式図</span></div>
 <svg width="1080" height="1920" style={{position:'absolute',inset:0,pointerEvents:'none'}}><defs><marker id="a" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="none" stroke="#087f9b" strokeWidth="2"/></marker></defs>
 <g opacity={smooth(f/12)}><path d={`M220 554L186 744M495 1285L347 ${waterY}`} stroke="white" strokeWidth="9"/><path d={`M220 554L186 744M495 1285L347 ${waterY}`} stroke="#347e91" strokeWidth="3"/>
 <circle cx="186" cy="744" r="7" fill="#347e91"/><circle cx="347" cy={waterY} r="7" fill="#347e91"/></g>
 {st.flowing&&<><path d="M402 730V600" stroke="white" strokeWidth="15"/><path d="M402 730V600" stroke="#087f9b" strokeWidth="7" markerEnd="url(#a)"/><path d="M751 960V1060" stroke="white" strokeWidth="15"/><path d="M751 960V1060" stroke="#087f9b" strokeWidth="7" markerEnd="url(#a)"/></>}
 </svg>
 {[{text:'固体の氷',x:90,y:470,w:270,from:0},{text:'液体の水',x:350,y:1285,w:290,from:0},{text:'吸水管',x:620,y:330,w:260,from:20},{text:'排出先',x:650,y:1370,w:250,from:40}].map(l=><div key={l.text} data-qc="diagram-label" style={{position:'absolute',left:l.x,top:l.y,width:l.w,height:84,display:'grid',placeItems:'center',borderRadius:20,background:'#fffffff2',border:'2px solid #b3d6db',boxShadow:'0 5px 18px #31555b14',fontSize:40,fontWeight:700,opacity:smooth((f-l.from)/12)}}>{l.text}</div>)}
 </>};
export const Cut09=({layer='composite',report=false})=><AbsoluteFill className="nnz" style={{background:['character','labels','overlay','model'].includes(layer)?'transparent':'#eef3f1'}}><style>{fonts}</style><FontReady/>{!['character','labels','overlay'].includes(layer)&&<ThreeScene mode={layer==='background'?'background':layer==='model'?'model':'all'} report={report}/>}{['composite','character','overlay'].includes(layer)&&<Char/>}{['composite','labels','overlay'].includes(layer)&&<Labels/>}</AbsoluteFill>;
const Cut01=()=>{const f=useCurrentFrame();return <AbsoluteFill><Img src={staticFile('ep004-v3/cut01/background.png')} style={{width:1080,height:1920,objectFit:'cover',transform:`scale(${1+.035*f/104})`,transformOrigin:'50% 50%'}}/></AbsoluteFill>};
const Root=()=> <><Composition id="EP004-V3-CUT01" component={Cut01} width={1080} height={1920} fps={30} durationInFrames={105}/><Composition id="EP004-V3-CUT09" component={Cut09} width={1080} height={1920} fps={30} durationInFrames={165} defaultProps={{layer:'composite',report:false}}/></>;
registerRoot(Root);
