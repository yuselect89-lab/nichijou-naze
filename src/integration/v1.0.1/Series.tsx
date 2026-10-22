import React,{createContext,useContext,useState,useEffect} from 'react';
import {AbsoluteFill,Img,Audio,staticFile,useCurrentFrame,useVideoConfig,interpolate,delayRender,continueRender,cancelRender} from 'remotion';
import {cleanCaption,episodeProgress,validateCues} from '../captions';
export type Cue={fromFrame:number;toFrame:number;text:string};
export {cleanCaption};
const Clock=createContext({frame:0,totalFrames:1});
export const useEpisodeClock=()=>useContext(Clock);
export const asset=(s:string)=>/^https?:/.test(s)?s:staticFile(s.replace(/^\//,''));
export const fonts=`@font-face{font-family:NNZJP;src:url('${staticFile('series/v1/NotoSansCJKjp-Bold.otf')}') format('opentype');font-weight:700;font-display:block}.nnz,.nnz *{box-sizing:border-box}.nnz{font-family:NNZJP,'Noto Sans CJK JP',sans-serif;color:#182b34}`;
export const FontReady=()=>{const [handle]=useState(()=>delayRender('NNZ Japanese font'));useEffect(()=>{document.fonts.load('700 56px NNZJP').then(()=>continueRender(handle)).catch(cancelRender)},[handle]);return null;};
export const SeriesFrame:React.FC<{children:React.ReactNode;cues?:Cue[];voiceover?:string;totalFrames?:number;bannerFrames?:number}>=({children,cues=[],voiceover,totalFrames,bannerFrames=90})=>{
 const frame=useCurrentFrame(),video=useVideoConfig(),total=totalFrames??video.durationInFrames;
 validateCues(cues,total);
 const progress=episodeProgress(frame,total);
 const cue=cues.find(c=>frame>=c.fromFrame&&frame<c.toFrame);
 const opacity=frame<bannerFrames?1:interpolate(frame,[bannerFrames,bannerFrames+12],[1,0],{extrapolateLeft:'clamp',extrapolateRight:'clamp'});
 return <Clock.Provider value={{frame,totalFrames:total}}><AbsoluteFill className="nnz" style={{background:'linear-gradient(180deg,#faf8ec,#edf5f0)'}}>
 <style>{fonts}</style>{children}
 <div data-qc="progress" data-progress={progress} style={{position:'absolute',top:78,left:96,width:888,height:14,borderRadius:7,background:'#d7dfd7',overflow:'hidden'}}><div style={{height:'100%',width:`${progress*100}%`,background:'#e2aa29'}}/></div>
 {opacity>0&&<Img data-qc="banner" src={staticFile('series/approved/opening_banner.png')} style={{position:'absolute',inset:0,width:1080,height:1920,opacity,pointerEvents:'none'}}/>}
 {cue&&<div data-qc="caption" style={{position:'absolute',left:96,top:1510,width:888,height:280,display:'flex',alignItems:'center',justifyContent:'center',textAlign:'center',fontSize:60,fontWeight:700,lineHeight:1.4,whiteSpace:'pre-line',padding:'14px 20px',borderRadius:24,background:'#152d38ee',color:'white'}}>{cleanCaption(cue.text)}</div>}
 {voiceover&&<Audio src={asset(voiceover)}/>}</AbsoluteFill></Clock.Provider>;
};
