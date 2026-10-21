import React from 'react';
import {AbsoluteFill,Img,OffthreadVideo,Sequence,useCurrentFrame} from 'remotion';
import {asset,FontReady,fonts} from '../../../../src/integration/v1.0.1/Series';
import {Diagram as LegacyDiagram,Config as LegacyConfig} from '../../../../src/integration/v1.0.1/Templates';
import {Scene,Character,Media,Label,Arrow,Step,CrossSection,characterFile,characterRect,motionAt,poseWeights,focusAt,smooth,validateScene} from './config';

export const FullMedia:React.FC<{media:Media;style?:React.CSSProperties}>=({media,style})=>{
 const css:React.CSSProperties={position:'absolute',inset:0,width:'100%',height:'100%',objectFit:'cover',objectPosition:media.objectPosition??'50% 50%',...style};
 return media.kind==='video'?<OffthreadVideo data-qc="background" src={asset(media.src)} muted style={css}/>:<Img data-qc="background" src={asset(media.src)} style={css}/>;
};
export const CharacterLayer:React.FC<{config:Character;durationFrames:number}>=({config:c,durationFrames})=>{
 const frame=useCurrentFrame(),r=characterRect(c),m=motionAt(c,frame,durationFrames);
 return <div data-qc="character" data-motion={JSON.stringify(m)} style={{position:'absolute',left:r.x,top:r.y,width:r.width,height:r.height,opacity:m.opacity,transform:`translate(${m.x}px,${m.y}px) rotate(${m.rotation}deg)`,transformOrigin:'50% 95%',filter:'drop-shadow(0 3px 2px #ffffffbb) drop-shadow(0 6px 7px #182b3438)'}}>
 {poseWeights(c,frame).map(p=><Img key={p.pose} data-pose={p.pose} src={asset(characterFile(p.pose))} style={{position:'absolute',inset:0,width:'100%',height:'100%',objectFit:'contain',opacity:p.opacity}}/>)}</div>;
};
export const LabelOverlay:React.FC<{labels:Label[]}>=({labels})=>{const f=useCurrentFrame();return <>{labels.map(l=>{
 const v=smooth(f,l.fromFrame,12)*(l.toFrame===undefined?1:1-smooth(f,l.toFrame-12,12));const b=l.box;
 const endX=Math.max(b.x,Math.min(l.anchor.x,b.x+b.width)),endY=Math.max(b.y,Math.min(l.anchor.y,b.y+b.height));
 return <React.Fragment key={l.id}><svg width="1080" height="1920" style={{position:'absolute',inset:0,opacity:v,pointerEvents:'none'}}><path d={`M${l.anchor.x} ${l.anchor.y}L${endX} ${endY}`} stroke="white" strokeWidth={11}/><path d={`M${l.anchor.x} ${l.anchor.y}L${endX} ${endY}`} stroke={l.color??'#087c94'} strokeWidth={5}/><circle cx={l.anchor.x} cy={l.anchor.y} r={10} fill={l.color??'#087c94'} stroke="white" strokeWidth={4}/></svg>
 <div data-qc="label" style={{position:'absolute',left:b.x,top:b.y,width:b.width,height:b.height,opacity:v,transform:`translateY(${(1-v)*8}px)`,padding:'10px 18px',display:'flex',alignItems:'center',justifyContent:'center',borderRadius:22,background:'#fffffff5',border:`3px solid ${l.color??'#087c94'}`,fontSize:42,fontWeight:700,textAlign:'center',lineHeight:1.3,boxShadow:'0 5px 16px #182b3420'}}>{l.text}</div></React.Fragment>;
 })}</>};
export const ArrowOverlay:React.FC<{arrows:Arrow[]}>=({arrows})=>{const f=useCurrentFrame();return <svg width="1080" height="1920" style={{position:'absolute',inset:0,pointerEvents:'none'}}>{arrows.map((a,i)=>{const v=smooth(f,a.fromFrame,18),x=a.from.x+(a.to.x-a.from.x)*v,y=a.from.y+(a.to.y-a.from.y)*v,angle=Math.atan2(a.to.y-a.from.y,a.to.x-a.from.x)*180/Math.PI;return <g key={i} opacity={v}><path d={`M${a.from.x} ${a.from.y}L${x} ${y}`} stroke="white" strokeWidth={16} strokeLinecap="round"/><path d={`M${a.from.x} ${a.from.y}L${x} ${y}`} stroke={a.color??'#e36044'} strokeWidth={9}/><path d="M-24 -15L4 0L-24 15Z" fill={a.color??'#e36044'} stroke="white" strokeWidth={3} transform={`translate(${x} ${y}) rotate(${angle})`}/></g>})}</svg>};
const StepGlyph:React.FC<{shape?:string;color:string;progress:number}>=({shape,color,progress})=><svg viewBox="0 0 220 220" width="220" height="220"><rect x="15" y="15" width="190" height="190" rx="35" fill="#d5f5fb" stroke={color} strokeWidth={5}/>{Array.from({length:13},(_,i)=>{const angle=i*2.4,r=shape==='bubbles'?28:shape==='inward'?70*(1-progress*.75):70;const x=110+Math.cos(angle)*r*(.3+(i%4)*.2),y=110+Math.sin(angle)*r;return <circle key={i} cx={x} cy={y} r={shape==='bubbles'?7:5} fill={shape==='bubbles'?'white':color} stroke={color} strokeWidth={2}/>;})}{shape==='inward'&&<path d="M25 110H65M195 110H155M110 25V65M110 195V155" stroke="#087c94" strokeWidth={5}/>}</svg>;
export const Step3Overlay:React.FC<{steps:Step[]}>=({steps})=>{const f=useCurrentFrame();return <>{steps.map((s,i)=>{const v=smooth(f,s.fromFrame,16),next=steps[i+1],active=f>=s.fromFrame&&(!next||f<next.fromFrame);return <React.Fragment key={i}>
 <div data-qc="step" data-step={i+1} style={{position:'absolute',left:90,top:350+i*370,width:820,height:330,opacity:v,transform:`translateY(${(1-v)*25}px)`,border:`4px solid ${active?s.color??'#087c94':'#c8dfe4'}`,borderRadius:38,background:active?'#fffffff5':'#ffffffe5',boxShadow:'0 8px 30px #20607112',display:'flex',alignItems:'center',padding:30,gap:24}}>
 <div style={{position:'absolute',left:28,top:14,fontSize:28,color:'#326475'}}>0{i+1}</div>
 {s.image?<Img src={asset(s.image)} style={{width:220,height:220,objectFit:'contain'}}/>:<StepGlyph shape={s.shape} color={s.color??'#087c94'} progress={smooth(f,s.fromFrame,40)}/>}
 <div style={{fontSize:46,fontWeight:700,lineHeight:1.5,maxWidth:490,whiteSpace:'pre-line'}}>{s.text}</div></div>
 {i<2&&<svg data-qc="step-link" width="1080" height="1920" style={{position:'absolute',inset:0,opacity:smooth(f,steps[i+1].fromFrame-12,12)}}><path d={`M500 ${690+i*370}v20m-15-10 15 15 15-15`} stroke="#087c94" strokeWidth={7} fill="none"/></svg>}</React.Fragment>})}</>};
export const CrossSectionOverlay:React.FC<{config:CrossSection;reveal:number}>=({config:c,reveal})=>{const f=useCurrentFrame(),r=c.region;return <div data-qc="crosssection" style={{position:'absolute',left:r.x,top:r.y,width:r.width,height:r.height}}>
 <Img data-qc="outside" src={asset(c.outside)} style={{position:'absolute',inset:0,width:'100%',height:'100%',objectFit:'fill',opacity:1-reveal}}/>
 <div style={{position:'absolute',inset:0,clipPath:`inset(0 ${(1-reveal)*100}% 0 0)`}}>
 {c.parts.map(p=>{const opacity=smooth(f,p.fromFrame,16)*(p.toFrame===undefined?1:1-smooth(f,p.toFrame-12,12))*(p.opacity??1);return <Img key={p.id} data-qc="cross-part" data-part={p.id} src={asset(p.image)} style={{position:'absolute',inset:0,width:'100%',height:'100%',objectFit:'fill',opacity}}/>})}</div>
 {reveal>0&&reveal<1&&<div style={{position:'absolute',top:0,bottom:0,left:`${reveal*100}%`,width:5,background:c.cutLine??'#e8b64a',boxShadow:'0 0 12px white'}}/>}</div>};

/** Only foreground/background. Band, global progress and captions belong to SeriesFrame. */
export const FullFrameScene:React.FC<{config:Scene}>=({config:c})=>{
 validateScene(c);const f=useCurrentFrame();const focus=c.focus?focusAt(c.focus,f):null;
 const target=c.focus?.target??{x:540,y:700};
 const t=focus?Math.min(1,(focus.zoom-1)/(c.focus!.zoom-1)):0;
 const dx=(540-target.x)*t,dy=(700-target.y)*t;
 const reveal=focus?.reveal??(c.crossSection?smooth(f,20,30):0);
 return <AbsoluteFill className="nnz"><style>{fonts}</style><FontReady/>
 <div style={{position:'absolute',inset:0,overflow:'hidden'}}><div style={{position:'absolute',inset:0,transformOrigin:`${target.x}px ${target.y}px`,transform:`translate(${dx}px,${dy}px) scale(${focus?.zoom??1})`}}><FullMedia media={c.background}/></div></div>
 {c.crossSection&&<div style={{position:'absolute',inset:0,opacity:reveal}}><div style={{position:'absolute',inset:0,background:'linear-gradient(180deg,#effaffaa 0%,#effafff5 25%,#e7f5f7f5 70%,#f4f7f888 100%)'}}/><CrossSectionOverlay config={c.crossSection} reveal={reveal}/></div>}
 {c.title&&<div data-qc="title" style={{position:'absolute',left:90,top:325,width:820,fontSize:48,fontWeight:700,color:'#163944',textAlign:'center',textShadow:'0 2px 5px white,0 0 16px white'}}>{c.title}</div>}
 {c.steps&&<Step3Overlay steps={c.steps}/>}{c.arrows&&<ArrowOverlay arrows={c.arrows}/>}{c.labels&&<LabelOverlay labels={c.labels}/>}
 {c.character&&<CharacterLayer config={c.character} durationFrames={c.durationFrames}/>}
 {c.legacyOverlay&&<Sequence from={c.legacyOverlay.fromFrame} durationInFrames={c.legacyOverlay.durationFrames}><AbsoluteFill style={{transform:'translateX(-44px) scale(.9)',transformOrigin:'540px 960px'}}><LegacyDiagram config={{...c.legacyOverlay.config,id:c.legacyOverlay.id,mode:'overlay',showTitle:false,characterVersion:'v02_highres'} as LegacyConfig}/></AbsoluteFill></Sequence>}
 {c.focus&&focus&&focus.reveal<.02&&<svg width="1080" height="1920" style={{position:'absolute',inset:0,pointerEvents:'none',opacity:smooth(f,5,12)*(1-smooth(f,c.focus.revealFromFrame,12))}}><circle data-qc="focus-ring" cx={target.x+dx} cy={target.y+dy} r={85*(focus.zoom/1.5)} fill="none" stroke="white" strokeWidth={12}/><circle cx={target.x+dx} cy={target.y+dy} r={85*(focus.zoom/1.5)} fill="none" stroke="#e5a53a" strokeWidth={6}/></svg>}
 </AbsoluteFill>;
};
