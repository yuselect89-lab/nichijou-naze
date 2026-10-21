import React from 'react';
import {Composition,registerRoot,Sequence,Img,staticFile,useCurrentFrame} from 'remotion';
import {SeriesFrame,FontReady} from '../integration/v1.0.1/Series';
import {TemplateScene} from '../Root';
import {Config} from '../integration/v1.0.1/Templates';
import {characterPath} from '../integration/character';
import arrow from '../../examples/arrow.json';
import compare from '../../examples/compare.json';
import zoom from '../../examples/zoom.json';
const poses=['neutral','talk','point_right','point_left','think'];
const Large=({pose,side='center'}:{pose:string;side?:'center'|'left'|'right'})=><Img data-highres="character" src={staticFile(characterPath(pose,'v02_highres'))} style={{position:'absolute',height:side==='center'?1220:1100,width:'auto',top:side==='center'?280:350,...(side==='center'?{left:540-1220/3}:side==='left'?{left:96}:{right:96})}}/>;
const Inspector=()=>{const frame=useCurrentFrame();React.useEffect(()=>{let active=true;const root=document.querySelector('.nnz')!;const run=()=>{if(!active)return;const origin=root.getBoundingClientRect();if(origin.width!==1080||[...document.images].some(i=>!i.complete||!i.naturalWidth)||document.fonts.status!=='loaded')return;const images=[...document.querySelectorAll('[data-highres],[data-qc="character"],[data-qc="caption"],[data-qc="progress"],[data-qc="banner"]')].map(e=>{const r=e.getBoundingClientRect();return {kind:e.getAttribute('data-qc')??'large-character',x:r.x-origin.x,y:r.y-origin.y,width:r.width,height:r.height,text:e.textContent}});console.log('NNZ_HIGHRES_QC '+JSON.stringify({frame,images}));};const ob=new ResizeObserver(run);ob.observe(root);document.fonts.ready.then(run);for(const i of document.images)i.addEventListener('load',run);run();return()=>{active=false;ob.disconnect();for(const i of document.images)i.removeEventListener('load',run)}},[frame]);return null;};
const QC=()=> <SeriesFrame bannerFrames={840} cues={[{fromFrame:0,toFrame:840,text:'高解像度素材の、\n画面配置を確認します。'}]}><FontReady/>
 {poses.map((pose,i)=><Sequence key={pose} from={i*90} durationInFrames={90}><Large pose={pose}/></Sequence>)}
 <Sequence from={450} durationInFrames={60}><Large pose="point_right" side="left"/></Sequence>
 <Sequence from={510} durationInFrames={60}><Large pose="point_left" side="right"/></Sequence>
 {[arrow,compare,zoom].map((c,i)=><Sequence key={c.id} from={570+i*90} durationInFrames={90}><TemplateScene config={{...c,mode:'overlay',characterImage:undefined,characterPose:i===0?'point_left':i===1?'point_right':'think',characterVersion:'v02_highres'} as Config}/></Sequence>)}
 <Inspector/></SeriesFrame>;
registerRoot(()=> <Composition id="NNZ-FEMALE-HIGHRES-QC" component={QC} width={1080} height={1920} fps={30} durationInFrames={840}/>);
