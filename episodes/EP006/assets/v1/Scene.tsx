import React from 'react';
import {AbsoluteFill,Img,staticFile,useCurrentFrame} from 'remotion';
import {geometry,path,smooth,TIMELINE,vesselAt} from './geometry';

export type Layer='all'|'background'|'object'|'character'|'labels'|'skin'|'tissue'|'vessels'|'outline';
export type Props={scene?:'episode'|'science'|'CUT01'|'CUT02'|'CUT03'|'CUT07';layer?:Layer;labels?:boolean};
const C={ink:'#213c42',teal:'#127a7d',cream:'#f7f5ee',pink:'#efb397'};
const show=(layer:Layer,want:Layer)=>layer==='all'||layer===want;
export const Background=()=> <AbsoluteFill style={{background:'radial-gradient(ellipse at 55% 48%, #ffffff 0%, #edf4f1 65%, #e1eeeb 100%)'}}/>;
const font=`@font-face{font-family:EP006;src:url('${staticFile('assets/v1/NotoSansCJKjp-Bold-subset.otf')}')} text{font-family:EP006,sans-serif}`;
function Pill({text,y=660,size=46}:{text:string;y?:number;size?:number}){
  return <g data-layer="labels"><rect x={150} y={y-52} width={740} height={88} rx={44} fill="white" stroke="#d6e4df" strokeWidth={2}/><text x={520} y={y+8} textAnchor="middle" fontSize={size} fill={C.ink}>{text}</text></g>;
}
/** Surface illustration, independently constructed CG; deliberately not presented as a photograph. */
export function Finger({wrinkle=0,x=0,y=0,scale=1}:{wrinkle?:number;x?:number;y?:number;scale?:number}){
  return <g data-layer="finger-CG" transform={`translate(${x} ${y}) scale(${scale})`}>
    <defs>
      <linearGradient id="fingerShade" x1="0" y1="0" x2="0.2" y2="1"><stop offset="0" stopColor="#f7dac4"/><stop offset=".5" stopColor="#efb89b"/><stop offset="1" stopColor="#ce8c73"/></linearGradient>
      <linearGradient id="nailShade" x1="0" y1="0" x2="0" y2="1"><stop stopColor="#fff3e8"/><stop offset="1" stopColor="#e1b2a0"/></linearGradient>
    </defs>
    <path d="M180 910 C340 902 480 890 650 900 C790 900 850 963 850 1050 C850 1150 767 1227 650 1227 C480 1268 320 1250 180 1230 Z" fill="url(#fingerShade)" stroke="#ad7865" strokeWidth={5}/>
    <path d="M600 916 Q720 895 786 955 Q806 981 802 1010 Q705 1031 604 1008 Z" fill="url(#nailShade)" stroke="#bd8e7c" strokeWidth={4}/>
    <path d="M622 926 Q722 914 776 958" fill="none" stroke="#fff8ed" strokeWidth={8} strokeLinecap="round"/>
    {[300,430,560].map((cx,i)=><g key={cx} opacity={wrinkle}>
      <path d={`M${cx-16} ${1165+i*4} Q${cx+24} 1198 ${cx-8} 1232`} fill="none" stroke="#a96c5b" strokeWidth={8} strokeLinecap="round"/>
      <path d={`M${cx-6} ${1165+i*4} Q${cx+33} 1198 ${cx+2} 1232`} fill="none" stroke="#f9dbc3" strokeWidth={5} strokeLinecap="round"/>
    </g>)}
    <path d="M205 946 Q390 920 524 934" fill="none" stroke="#ffe6d1" strokeWidth={11} strokeLinecap="round" opacity=".65"/>
  </g>;
}
function Droplet({x,y}:{x:number;y:number}){return <g transform={`translate(${x} ${y})`}><path d="M0 -18 C-32 16 -26 38 0 38 C26 38 32 16 0 -18Z" fill="#b2e5e8" stroke="#68adb6" strokeWidth={3}/><path d="M-12 12 Q-18 25 -8 29" stroke="white" fill="none" strokeWidth={5} strokeLinecap="round"/></g>;}
function Character({pose,opacity=1}:{pose:string;opacity?:number}){
  // Original full-resolution sprite is cropped by viewport only; no redraw, retouch or pose invention.
  return <div data-layer="character" style={{position:'absolute',left:115,top:950,width:pose==='point'?700:530,height:510,overflow:'hidden',opacity}}>
    <Img src={staticFile(`assets/v1/character-${pose}.png`)} style={{position:'absolute',left:-100,top:-20,width:700,height:1050,maxWidth:'none'}}/>
  </div>;
}
export function Science({frame,layer='all',labels=true}:{frame:number;layer?:Layer;labels?:boolean}){
  const g=geometry(frame),o=path(g.outer),i=path(g.inner);
  const vessel='M198 1108 C300 1085 350 1135 440 1094 S620 1088 757 1067';
  const branches=['M350 1104 Q370 1020 465 1003','M540 1093 Q566 1160 635 1152'];
  const allow=(l:Layer)=>layer==='object'||show(layer,l);
  return <svg style={{position:'absolute',inset:0}} width="1080" height="1920" viewBox="0 0 1080 1920" data-scene="single-finger-section" data-frame={frame} data-camera="fixed-1080-1920">
    <style>{font}</style>
    <defs><linearGradient id="tissueShade" x1="0" y1="0" x2="0" y2="1"><stop stopColor="#fbe1c8"/><stop offset="1" stopColor="#eab792"/></linearGradient><clipPath id="tissueClip"><path d={i}/></clipPath></defs>
    <g data-subject-count="1" data-layer="section" data-camera-transform="identity">
      {allow('tissue')&&<path data-layer="tissue" data-boundary={i} d={i} fill="url(#tissueShade)"/>}
      {allow('vessels')&&<g data-layer="vessels" clipPath="url(#tissueClip)" fill="none" strokeLinecap="round" strokeLinejoin="round">
        {[vessel,...branches].map((d,n)=><React.Fragment key={n}><path d={d} stroke="#b66568" strokeWidth={n?g.vesselWidth*.7+9:g.vesselWidth+10}/><path d={d} stroke="#e99591" strokeWidth={n?g.vesselWidth*.7:g.vesselWidth}/></React.Fragment>)}
        {[.05,.2,.35,.5,.65,.8,.95].map((t,n)=>{const [x,y]=vesselAt(t);return <ellipse key={t} cx={x} cy={y} rx={g.bloodRadius*1.3} ry={g.bloodRadius} fill="#b64c58" opacity={n%2?g.bloodOpacity:1} stroke="none"/>;})}
      </g>}
      {allow('skin')&&<path data-layer="epidermis" data-inner-boundary={i} d={`${o} ${i}`} fill="#d78b76" fillRule="evenodd"/>}
      {allow('outline')&&<g data-layer="outline" fill="none"><path d={o} stroke="#92594c" strokeWidth={7} strokeLinejoin="round"/><path d={i} stroke="#bb8069" strokeWidth={3}/><path d="M615 884 Q737 881 795 963" stroke="#f9e6d2" strokeWidth={10} strokeLinecap="round"/></g>}
    </g>
    {labels&&show(layer,'labels')&&<g data-layer="labels">
      <Pill text={frame<150?'血管が細くなる':frame<270?'中が少ししぼむ':'皮膚に折り目'} size={48}/>
      {frame<150&&<><text x="190" y="772" fontSize="37" fill={C.teal}>自律神経の働きが関わる</text><path d="M690 789 L729 995" fill="none" stroke={C.teal} strokeWidth={4}/></>}
      <text x="190" y="1400" fontSize="31" fill="#6f817e">指腹の側面・しくみを示す模式図</text>
      <text x="200" y="839" fontSize="31" fill="#92594c">皮膚</text><path d="M270 829 L300 860" stroke="#92594c" strokeWidth={3}/>
      <text x="650" y="1325" fontSize="31" fill="#a45660">小血管</text><path d="M700 1285 L720 1118" stroke="#a45660" strokeWidth={3}/>
    </g>}
  </svg>;
}
export const Scene:React.FC<Props>=({scene='episode',layer='all',labels=true})=>{
  const f=useCurrentFrame();let cut=scene,t=f;
  if(scene==='episode'){
    const c=TIMELINE.find(c=>f>=c.from&&f<c.to)!;
    cut=c.cut as typeof scene;t=f-c.from;
    if(f>=420&&f<870){cut='science';t=f-420;}
  }
  const science=cut==='science';
  const object=show(layer,'object'),lab=labels&&show(layer,'labels');
  return <AbsoluteFill style={{fontFamily:'EP006,sans-serif',background:'transparent'}}>
    {show(layer,'background')&&<Background/>}
    {science?<Science frame={t} layer={layer} labels={labels}/>:<>
      <svg style={{position:'absolute',inset:0}} width="1080" height="1920" viewBox="0 0 1080 1920"><style>{font}</style>
        {cut==='CUT01'&&<>
          {object&&<>
            <ellipse cx="520" cy="1300" rx="350" ry="64" fill="#b9d8d4" opacity=".35"/>
            <rect x="150" y="1030" width="740" height="360" rx="100" fill="#f9ffff" stroke="#b1d6d2" strokeWidth="12"/>
            <rect x="180" y="1060" width="680" height="290" rx="80" fill="#b8e1e2"/>
            <g transform={`translate(0 ${-150+155*smooth(t/35)-155*smooth((t-115)/30)})`}><Finger wrinkle={smooth((t-95)/20)}/></g>
            {t<145&&<path d="M185 1178 Q340 1158 500 1178 T855 1178 L855 1270 Q855 1350 775 1350 H260 Q185 1350 185 1270Z" fill="#b1dfe2" opacity=".86"/>}
            <path d="M200 1180 Q350 1160 510 1180 T850 1180" stroke="#f2ffff" strokeWidth="7" fill="none"/>
            {t>145&&<><Droplet x={700} y={1040}/><Droplet x={530} y={1070}/></>}
          </>}
          {lab&&<><Pill text={t<40?'湯船へ':t<130?'しばらく浸すと…':'シワシワ!?'} size={52}/>{t>=40&&t<130&&<g><circle cx="520" cy="820" r="49" stroke={C.teal} strokeWidth="6" fill="white"/><path d="M520 790 V820 L542 835" stroke={C.teal} strokeWidth="6" fill="none" strokeLinecap="round"/><text x="520" y="935" textAnchor="middle" fill={C.teal} fontSize="33">時間がたってから</text></g>}</>}
        </>}
        {(cut==='CUT02'||cut==='CUT03'||cut==='CUT07')&&<>
          {object&&<><Finger wrinkle={1} x={250} y={100} scale={.70}/><Droplet x={730} y={1050}/>
            {cut==='CUT03'&&<g opacity={smooth((t-10)/30)}><circle cx="650" cy="875" r="108" fill="none" stroke={C.teal} strokeWidth="8"/><path d="M720 957 L775 1018" stroke={C.teal} strokeWidth="13" strokeLinecap="round"/></g>}
          </>}
          {lab&&<><Pill text={cut==='CUT02'?'水を吸ったから？':cut==='CUT03'?'指先の内側へ':'中が少ししぼむ'} size={48}/>
            {cut==='CUT07'&&<text x="670" y="1320" textAnchor="middle" fontSize="39" fill={C.teal}><tspan x="700">↓</tspan><tspan x="700" dy="62">皮膚に折り目</tspan></text>}
            {cut==='CUT02'&&<text x="710" y="1230" textAnchor="middle" fontSize="110" fill={C.teal}>?</text>}
            {cut==='CUT03'&&<g><text x="805" y="1325" textAnchor="middle" fontSize="36" fill={C.teal}>内側へ</text><path d="M805 1260 V1100 M805 1100 L790 1120 M805 1100 L820 1120" stroke={C.teal} strokeWidth="5" fill="none"/></g>}
          </>}
        </>}
      </svg>
      {show(layer,'character')&&(cut==='CUT02'||cut==='CUT03'||cut==='CUT07')&&<Character pose={cut==='CUT02'?'think':cut==='CUT03'?'point':'happy'} opacity={cut==='CUT03'?1-smooth((t-65)/25):1}/>}
    </>}
  </AbsoluteFill>;
};
