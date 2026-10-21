import React from 'react';
import {AbsoluteFill,Img,useCurrentFrame,Base,Mascot,Card,asset,ease} from '../_shared/layout';
export type Arrow={x1:number;y1:number;x2:number;y2:number;label?:string;color?:string};
export type ArrowProps={id?:string;title:string;durationSeconds:number;image:string;arrows:Arrow[];characterImage?:string};
export const ArrowTemplate:React.FC<ArrowProps>=({title,image,arrows,characterImage})=>{
 const f=useCurrentFrame();const rise=ease(f,2,24);
 return <Base title={title}>
  <Card style={{position:'absolute',top:520,left:108,width:864,height:850,display:'grid',placeItems:'center',transform:`scale(${.94+.06*rise})`,opacity:rise}}>
    <Img src={asset(image)} style={{width:555,height:730,objectFit:'contain'}}/>
  </Card>
  <svg viewBox="0 0 1080 1920" style={{position:'absolute',inset:0,pointerEvents:'none',width:'100%',height:'100%'}}>
   <defs><marker id="arrHead" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="#ed694c"/></marker></defs>
   {arrows.map((a,i)=>{const v=ease(f,22+i*13,38+i*13);const X=a.x1+(a.x2-a.x1)*v,Y=a.y1+(a.y2-a.y1)*v;
   return <g key={i} opacity={v}>
     <path d={`M${a.x1} ${a.y1}L${X} ${Y}`} stroke={a.color||'#ed694c'} strokeWidth={13} strokeLinecap="round" fill="none" markerEnd="url(#arrHead)"/>
     {a.label&&<text x={a.x2} y={a.y2-28} fill="#be4537" stroke="white" strokeWidth={10} paintOrder="stroke" fontSize={37} fontWeight="900" textAnchor="middle">{a.label}</text>}
   </g>})}
  </svg>
  <Mascot source={characterImage} fade={ease(f,24,43)}/>
 </Base>;
};
export default ArrowTemplate;
