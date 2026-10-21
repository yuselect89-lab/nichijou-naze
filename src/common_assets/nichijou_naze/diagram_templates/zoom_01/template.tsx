import React from 'react';
import {useCurrentFrame,Base,Mascot,Card,Img,asset,ease} from '../_shared/layout';
export type ZoomProps={id?:string;title:string;durationSeconds:number;image:string;highlight:{x:number;y:number};zoom:number;label:string;characterImage?:string};
export const ZoomTemplate:React.FC<ZoomProps>=({title,image,highlight,zoom,label,characterImage})=>{
 const f=useCurrentFrame();const appear=ease(f,6,26);const reveal=ease(f,40,62);const centerX=540,centerY=920;
 const ringX=centerX+(highlight.x-.5)*550,ringY=centerY+(highlight.y-.5)*620;
 const clipSize=402,offsetX=clipSize/2-highlight.x*660*zoom,offsetY=clipSize/2-highlight.y*750*zoom;
 return <Base title={title}>
  <Card style={{position:'absolute',top:535,left:225,width:630,height:775,display:'grid',placeItems:'center',opacity:appear}}>
   <Img src={asset(image)} style={{width:550,height:650,objectFit:'contain'}}/>
  </Card>
  <div style={{position:'absolute',left:ringX-70,top:ringY-70,width:140,height:140,border:'12px solid #ed684a',borderRadius:'50%',opacity:reveal,boxShadow:'0 0 0 11px #fff9'}}/>
  <svg style={{position:'absolute',inset:0,width:'100%',height:'100%',pointerEvents:'none'}} viewBox="0 0 1080 1920">
   <path d={`M${ringX+70} ${ringY+70}L655 1280`} fill="none" stroke="#ed684a" strokeWidth={12} strokeLinecap="round" opacity={reveal}/>
  </svg>
  <div style={{position:'absolute',top:1180,left:584,width:clipSize,height:clipSize,borderRadius:'50%',overflow:'hidden',border:'14px solid #e97443',background:'white',boxShadow:'0 14px 35px #314e4550',transform:`scale(${.65+.35*reveal})`,opacity:reveal}}>
    <Img src={asset(image)} style={{position:'absolute',width:660*zoom,height:750*zoom,maxWidth:'none',left:offsetX,top:offsetY}}/>
  </div>
  <div style={{position:'absolute',top:1640,left:505,fontSize:47,fontWeight:900,background:'#fff6df',padding:'18px 28px',borderRadius:20,opacity:reveal}}>{label}</div>
  <Mascot source={characterImage} side="left" fade={ease(f,46,72)}/>
 </Base>;
};
export default ZoomTemplate;
