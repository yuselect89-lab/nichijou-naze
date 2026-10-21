import React from 'react';
import {AbsoluteFill, Img, staticFile, useCurrentFrame, interpolate, Easing} from 'remotion';
export const W=1080;export const H=1920;
export const ease=(frame:number,start:number,end:number)=>interpolate(frame,[start,end],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:Easing.out(Easing.cubic)});
export const asset=(path:string)=>path.startsWith('http')?path:staticFile(path.replace(/^\//,''));
export const Base:React.FC<{title:string,children:React.ReactNode}>=({title,children})=><AbsoluteFill style={{background:'linear-gradient(180deg,#faf8ec 0%,#edf5f0 100%)',fontFamily:'Noto Sans CJK JP, sans-serif',color:'#182b34'}}>
  <div style={{position:'absolute',top:125,left:45,width:990,height:142,background:'#ffd750',borderRadius:32,display:'flex',alignItems:'center',justifyContent:'center',boxShadow:'0 13px 0 #e8b83b',fontSize:64,fontWeight:950}}>秒で解決!!</div>
  <div style={{position:'absolute',top:320,left:65,right:65,fontSize:59,fontWeight:950,textAlign:'center',lineHeight:1.3}}>{title}</div>
  {children}
</AbsoluteFill>;
export const Mascot:React.FC<{source?:string,side?:'left'|'right',fade?:number}>=({source,side='right',fade=1})=>source?<Img src={asset(source)} style={{position:'absolute',bottom:175,[side]:62,width:282,height:390,objectFit:'contain',opacity:fade,filter:'drop-shadow(5px 11px 6px #3f587b24)'}}/>:null;
export const Card:React.FC<{children:React.ReactNode,style?:React.CSSProperties}>=({children,style})=><div style={{background:'#ffffffed',border:'5px solid #dce7dd',borderRadius:33,boxShadow:'0 18px 50px #4262521f',...style}}>{children}</div>;
export {React,AbsoluteFill,Img,staticFile,useCurrentFrame,interpolate};
