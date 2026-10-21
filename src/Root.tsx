import React,{useEffect} from 'react';
import {Composition,Sequence,useCurrentFrame} from 'remotion';
import {Diagram,Config} from './integration/v1.0.1/Templates';
import {SeriesFrame,Cue} from './integration/v1.0.1/Series';
import arrow from '../examples/arrow.json';
import compare from '../examples/compare.json';
import zoom from '../examples/zoom.json';
type Props={config:Config;cues?:Cue[];voiceover?:string;qc?:boolean};
const Reporter=()=>{const f=useCurrentFrame();useEffect(()=>{let active=true;const root=document.querySelector('.nnz')!;const report=()=>{if(!active)return;const origin=root.getBoundingClientRect();if(origin.width!==1080||document.fonts.status!=='loaded'||[...document.images].some(i=>!i.complete||!i.naturalWidth))return;const opacity=(e:Element)=>{let n:Element|null=e;while(n){if(Number(getComputedStyle(n).opacity)<.01)return false;n=n.parentElement}return true;};const elements=[...document.querySelectorAll('[data-qc]')].filter(opacity).map(e=>{const r=e.getBoundingClientRect();return {kind:e.getAttribute('data-qc'),x:r.x-origin.x,y:r.y-origin.y,w:r.width,h:r.height,text:e.textContent?.trim(),progress:e.getAttribute('data-progress')}});console.log('NNZ_QC '+JSON.stringify({frame:f,elements}));};const observer=new ResizeObserver(report);observer.observe(root);for(const i of document.images)i.addEventListener('load',report);document.fonts.ready.then(report);report();return()=>{active=false;observer.disconnect();for(const i of document.images)i.removeEventListener('load',report)};},[f]);return null;};
export const TemplateScene:React.FC<Props>=({config,cues=[],voiceover,qc})=>{const diagram=<><Diagram config={config}/>{qc&&<Reporter/>}</>;return config.mode==='overlay'?diagram:<SeriesFrame cues={cues} voiceover={voiceover}>{diagram}</SeriesFrame>;};
const overlay={...compare,mode:'overlay'} as Config;
const ParentValidation=()=><SeriesFrame cues={[{fromFrame:120,toFrame:190,text:'これは検証用の、\n日本語字幕です。'}]}><Sequence from={90} durationInFrames={180}><TemplateScene config={overlay}/></Sequence><Reporter/></SeriesFrame>;
export const Root=()=> <>
 {[arrow,compare,zoom].map(c=><Composition key={c.id} id={c.id.replace(/_/g,'-')} component={TemplateScene} width={1080} height={1920} fps={30} durationInFrames={Math.round(c.durationSeconds*30)} defaultProps={{config:c as Config,qc:false}} calculateMetadata={({props})=>({durationInFrames:Math.round(props.config.durationSeconds*30),props})}/>)}
 <Composition id="NNZ-TEMPLATE" component={TemplateScene} width={1080} height={1920} fps={30} durationInFrames={150} defaultProps={{config:arrow as Config,qc:false}} calculateMetadata={({props})=>({durationInFrames:Math.round(props.config.durationSeconds*30),props})}/>
 <Composition id="NNZ-OVERLAY-VALIDATION" component={ParentValidation} width={1080} height={1920} fps={30} durationInFrames={360}/>
 </>;
