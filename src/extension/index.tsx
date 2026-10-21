import React,{useEffect} from 'react';
import {registerRoot,Composition,Sequence,useCurrentFrame} from 'remotion';
import {FullFrameScene} from '../../common_assets/nichijou_naze/runtime/v1.1.0/components';
import {EpisodeChrome} from '../../common_assets/nichijou_naze/runtime/v1.1.0/Chrome';
import {Scene,validateScene} from '../../common_assets/nichijou_naze/runtime/v1.1.0/config';
import surprise from '../../common_assets/nichijou_naze/layouts/v1.1.0/examples/expression-surprise.json';
import happy from '../../common_assets/nichijou_naze/layouts/v1.1.0/examples/expression-happy.json';
import troubled from '../../common_assets/nichijou_naze/layouts/v1.1.0/examples/expression-troubled.json';
import footage from '../../common_assets/nichijou_naze/layouts/v1.1.0/examples/footage-character.json';
import diagram from '../../common_assets/nichijou_naze/layouts/v1.1.0/examples/diagram-character.json';
import focus from '../../common_assets/nichijou_naze/layouts/v1.1.0/examples/focus-crosssection-return.json';
import labels from '../../common_assets/nichijou_naze/layouts/v1.1.0/examples/label-parameters.json';
import steps from '../../common_assets/nichijou_naze/layouts/v1.1.0/examples/step3-cause.json';
import carton from '../../common_assets/nichijou_naze/layouts/v1.1.0/examples/crosssection-carton.json';
import motions from '../../common_assets/nichijou_naze/layouts/v1.1.0/examples/motions.json';
import arrow from '../../common_assets/nichijou_naze/layouts/v1.1.0/examples/legacy-arrow.json';
import compare from '../../common_assets/nichijou_naze/layouts/v1.1.0/examples/legacy-compare.json';
import zoom from '../../common_assets/nichijou_naze/layouts/v1.1.0/examples/legacy-zoom.json';

const scenes=[surprise,happy,troubled,footage,diagram,focus,labels,steps,carton,motions,arrow,compare,zoom] as unknown as Scene[];
scenes.forEach(validateScene);
const total=scenes.reduce((n,s)=>n+s.durationFrames,0);
const Reporter:React.FC<{scene:string}>=({scene})=>{const frame=useCurrentFrame();useEffect(()=>{
 let active=true;
 const report=()=>{if(!active||document.fonts.status!=='loaded'||[...document.images].some(i=>!i.complete||!i.naturalWidth))return;
 const root=document.querySelector('.nnz-extension')!;const origin=root.getBoundingClientRect();if(origin.width!==1080)return;
 const visible=(e:Element)=>{let n:Element|null=e;while(n){if(+getComputedStyle(n).opacity<.01)return false;n=n.parentElement;}return true;};
 const elements=[...document.querySelectorAll('[data-qc]')].filter(visible).map(e=>{const r=e.getBoundingClientRect();return {kind:e.getAttribute('data-qc'),x:r.x-origin.x,y:r.y-origin.y,w:r.width,h:r.height,text:e.textContent?.trim(),progress:e.getAttribute('data-progress'),part:e.getAttribute('data-part'),motion:e.getAttribute('data-motion')};});
 const images=[...document.images].map(i=>({src:new URL(i.src).pathname,width:i.naturalWidth,height:i.naturalHeight,pose:i.getAttribute('data-pose')}));
 console.log('NNZ_EXTENSION_QC '+JSON.stringify({scene,frame,elements,images}));};
 const observer=new ResizeObserver(report);observer.observe(document.body);document.fonts.ready.then(report);for(const im of document.images)im.addEventListener('load',report);report();
 return()=>{active=false;observer.disconnect();for(const im of document.images)im.removeEventListener('load',report)};
 },[scene,frame]);return null;};
const Showcase:React.FC<{qc?:boolean}>=({qc=true})=>{
 let from=0;
 return <EpisodeChrome totalFrames={total} bannerFrames={total} cues={[{fromFrame:0,toFrame:total,text:'検証用の、日本語字幕。\n表示領域を確認します。'}]}>
 {scenes.map(s=>{const start=from;from+=s.durationFrames;return <Sequence key={s.id} from={start} durationInFrames={s.durationFrames}><FullFrameScene config={s}/>{qc&&<Reporter scene={s.id}/>}</Sequence>})}
 </EpisodeChrome>;
};
const Single:React.FC<{config:Scene;overlayOnly?:boolean}>=({config,overlayOnly})=>overlayOnly?<FullFrameScene config={config}/>:<EpisodeChrome totalFrames={config.durationFrames}><FullFrameScene config={config}/></EpisodeChrome>;
const Root=()=> <><Composition id="NNZ-LIBRARY-EXTENSION-QC" component={Showcase} width={1080} height={1920} fps={30} durationInFrames={total} defaultProps={{qc:true}}/>
 <Composition id="NNZ-FULLFRAME" component={Single} width={1080} height={1920} fps={30} durationInFrames={footage.durationFrames} defaultProps={{config:footage as Scene,overlayOnly:false}} calculateMetadata={({props})=>({durationInFrames:validateScene(props.config).durationFrames})}/></>;
registerRoot(Root);
