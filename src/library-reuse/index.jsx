import React,{useRef,useState,useLayoutEffect} from 'react';
import {registerRoot,Composition,AbsoluteFill,useCurrentFrame,delayRender,continueRender,cancelRender} from 'remotion';
import {createReusableScene} from '../../common_assets/nichijou_naze/models/ice_science/1.1.0/index.mjs';
import {CharacterLayer,LabelOverlay,ArrowOverlay} from '../../common_assets/nichijou_naze/runtime/v1.1.0/components';
import {fonts,FontReady} from '../integration/v1.0.1/Series';
export const ReuseScene=({asset_id='NNZ_MODEL_ICE_MICRO_01',parameters={cut:5,playbackRate:1.2},view={scale:.86,x:12,y:80},character=null,qc=false})=>{
 const frame=useCurrentFrame(),ref=useRef(),engine=useRef();const [h]=useState(()=>delayRender('Reusable 3D model',{timeoutInMilliseconds:120000}));
 useLayoutEffect(()=>{try{engine.current=createReusableScene(ref.current,{asset_id,parameters});const state=engine.current.draw(frame);if(qc)console.log('REUSE_QC '+JSON.stringify(state));continueRender(h)}catch(e){cancelRender(e)}return()=>engine.current?.dispose()},[]);
 useLayoutEffect(()=>{if(engine.current){const state=engine.current.draw(frame);if(qc)console.log('REUSE_QC '+JSON.stringify(state))}},[frame]);
 return <AbsoluteFill className="nnz" style={{background:'#edf4f2'}}><style>{fonts}</style><FontReady/><canvas ref={ref} width={1080} height={1920} style={{position:'absolute',inset:0,width:1080,height:1920,transform:`translate(${view.x}px,${view.y}px) scale(${view.scale})`,transformOrigin:'500px 790px'}}/>{character&&<><CharacterLayer durationFrames={60} config={character}/><LabelOverlay labels={[{id:'reuse',text:'気泡と光',anchor:{x:500,y:825},box:{x:110,y:350,width:380,height:90},fromFrame:0}]}/><ArrowOverlay arrows={[{from:{x:280,y:450},to:{x:465,y:755},fromFrame:7}]}/></>}</AbsoluteFill>;
};
registerRoot(()=> <Composition id="NNZ-REUSE" component={ReuseScene} width={1080} height={1920} fps={30} durationInFrames={195} defaultProps={{}}/>);
