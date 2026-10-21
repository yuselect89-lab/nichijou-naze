import React,{useState,useEffect} from 'react';
import {AbsoluteFill,Img,useCurrentFrame,interpolate,Easing,delayRender,continueRender,cancelRender} from 'remotion';
import {asset,fonts,FontReady} from './Series';
import {characterPath} from '../character';
export const IDs=['NNZ_TMP_ARROW_01','NNZ_TMP_COMPARE_01','NNZ_TMP_ZOOM_01'] as const;
export type ID=typeof IDs[number];
type Choice={image:string;label:string;marker:string};
export type Config={id:ID;revision?:string;mode?:'standalone'|'overlay';showTitle?:boolean;title:string;durationSeconds:number;image?:string;characterImage?:string;characterPose?:string;characterVersion?:'prototype'|'v02_highres';arrows?:{x1:number;y1:number;x2:number;y2:number;label?:string;color?:string}[];left?:Choice;right?:Choice;highlight?:{x:number;y:number};zoom?:number;label?:string};
const ease=(f:number,a:number,b:number)=>interpolate(f,[a,b],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:Easing.out(Easing.cubic)});
const Card:React.FC<{children:React.ReactNode;style:React.CSSProperties}>=({children,style})=><div data-qc="card" style={{position:'absolute',background:'#ffffffed',border:'4px solid #dce7dd',borderRadius:30,boxShadow:'0 12px 34px #4262521f',...style}}>{children}</div>;
const Mascot:React.FC<{config:Config;side?:'left'|'right'}>=({config,side='right'})=>{
 const frame=useCurrentFrame();const source=config.characterImage??characterPath(config.characterPose??'neutral',config.characterVersion);
 const highres=config.characterVersion==='v02_highres';
 return <Img data-qc="character" src={asset(source)} style={{position:'absolute',top:highres?1170:1197,[side]:96,height:highres?280:253,width:'auto',maxWidth:highres?187:148,objectFit:'contain',opacity:ease(frame,20,38)}}/>;
};
const Arrow:React.FC<{config:Config}>=({config:c})=>{const f=useCurrentFrame();return <>
 <Card style={{top:520,left:108,width:864,height:650,display:'grid',placeItems:'center',opacity:ease(f,2,24)}}><Img src={asset(c.image!)} style={{width:500,height:600,objectFit:'contain'}}/></Card>
 <svg width="1080" height="1920" style={{position:'absolute',inset:0,pointerEvents:'none'}}><defs>{(c.arrows??[]).map((a,i)=><marker key={i} id={`head-${i}`} viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 0L10 5L0 10Z" fill={a.color??'#ed694c'}/></marker>)}</defs>
 {(c.arrows??[]).map((a,i)=>{const v=ease(f,22+i*13,38+i*13);return <g key={i} opacity={v}><path d={`M${a.x1} ${a.y1}L${a.x1+(a.x2-a.x1)*v} ${a.y1+(a.y2-a.y1)*v}`} stroke={a.color??'#ed694c'} strokeWidth={12} fill="none" markerEnd={`url(#head-${i})`}/>{a.label&&<text data-qc="label" x={a.x2} y={a.y2-28} fontSize={40} fontWeight={700} textAnchor="middle" fill="#a63c2d" stroke="white" strokeWidth={8} paintOrder="stroke">{a.label}</text>}</g>;})}</svg><Mascot config={c}/>
 </>;};
const Compare:React.FC<{config:Config}>=({config:c})=>{const f=useCurrentFrame();return <>
 {[c.left!,c.right!].map((it,i)=><Card key={i} style={{top:520,left:96+i*456,width:432,height:650,padding:16,opacity:ease(f,8+i*17,25+i*17),transform:`translateX(${(i===0?-1:1)*(1-ease(f,8+i*17,25+i*17))*24}px)`,display:'flex',flexDirection:'column',alignItems:'center'}}><div data-qc="label" style={{fontSize:44,fontWeight:700,marginTop:16,textAlign:'center'}}>{it.label}</div><Img src={asset(it.image)} style={{width:310,height:430,objectFit:'contain'}}/><div data-qc="label" style={{fontSize:72,fontWeight:700,color:it.marker==='○'?'#239864':'#c84c40',opacity:ease(f,56,77)}}>{it.marker}</div></Card>)}
 <div data-qc="label" style={{position:'absolute',top:1270,left:310,width:460,textAlign:'center',fontSize:50,fontWeight:700,opacity:ease(f,64,86)}}>違いはここ！</div><Mascot config={c}/>
 </>;};
function useImageSize(src:string){const [size,setSize]=useState({w:500,h:700});const [handle]=useState(()=>delayRender('NNZ image geometry'));useEffect(()=>{const image=new window.Image();image.onload=()=>{setSize({w:image.naturalWidth,h:image.naturalHeight});continueRender(handle)};image.onerror=()=>cancelRender(new Error(`Cannot load ${src}`));image.src=asset(src);},[src,handle]);return size;}
const Zoom:React.FC<{config:Config}>=({config:c})=>{const f=useCurrentFrame(),size=useImageSize(c.image!);const k=Math.min(550/size.w,560/size.h),w=size.w*k,h=size.h*k,left=540-w/2,top=815-h/2,p=c.highlight!,z=c.zoom!;const x=left+p.x*w,y=top+p.y*h,reveal=ease(f,40,62),lens=280;
 return <><Card style={{top:520,left:225,width:630,height:590,opacity:ease(f,6,26)}}><Img src={asset(c.image!)} style={{position:'absolute',width:w,height:h,left:left-229,top:top-524}}/></Card>
 <div data-qc="focus" style={{position:'absolute',left:x-50,top:y-50,width:100,height:100,border:'9px solid #de6946',borderRadius:'50%',opacity:reveal}}/>
 <svg style={{position:'absolute',inset:0,width:1080,height:1920,pointerEvents:'none'}}><path d={`M${x+50} ${y+50}L755 1260`} stroke="#de6946" strokeWidth={8} fill="none" opacity={reveal}/></svg>
 <div data-qc="lens" style={{position:'absolute',left:615,top:1120,width:lens,height:lens,borderRadius:'50%',overflow:'hidden',border:'10px solid #de6946',background:'white',opacity:reveal}}><Img src={asset(c.image!)} style={{position:'absolute',width:w*z,height:h*z,maxWidth:'none',left:(lens-20)/2-p.x*w*z,top:(lens-20)/2-p.y*h*z}}/></div>
 <div data-qc="label" style={{position:'absolute',left:560,top:1410,width:390,fontSize:40,fontWeight:700,textAlign:'center',opacity:reveal}}>{c.label}</div><Mascot config={c} side="left"/></>;
};
export const Diagram:React.FC<{config:Config}>=({config})=><AbsoluteFill className="nnz" style={{background:'transparent'}}><style>{fonts}</style><FontReady/>{(config.mode!=='overlay'||config.showTitle)&&<div data-qc="title" style={{position:'absolute',left:96,top:335,width:888,height:150,fontSize:56,fontWeight:700,lineHeight:1.25,textAlign:'center'}}>{config.title}</div>}{config.id==='NNZ_TMP_ARROW_01'?<Arrow config={config}/>:config.id==='NNZ_TMP_COMPARE_01'?<Compare config={config}/>:<Zoom config={config}/>}</AbsoluteFill>;
