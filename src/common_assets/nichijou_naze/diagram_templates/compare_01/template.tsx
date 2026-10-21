import React from 'react';
import {useCurrentFrame,Base,Mascot,Card,Img,asset,ease} from '../_shared/layout';
type Choice={image:string;label:string;marker:string};
export type CompareProps={id?:string;title:string;durationSeconds:number;left:Choice;right:Choice;characterImage?:string};
export const CompareTemplate:React.FC<CompareProps>=({title,left,right,characterImage})=>{
 const f=useCurrentFrame();
 const render=(it:Choice,i:number)=>{const v=ease(f,8+i*17,25+i*17);return <Card key={i} style={{width:448,height:825,opacity:v,transform:`translateX(${(i===0?-1:1)*(1-v)*140}px)`,display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'flex-start',padding:18}}>
   <div style={{fontSize:44,fontWeight:900,textAlign:'center',marginTop:35}}>{it.label}</div>
   <Img src={asset(it.image)} style={{width:376,height:590,objectFit:'contain'}}/>
   <div style={{fontSize:89,fontWeight:950,color:it.marker==='○'?'#239864':'#e25346',opacity:ease(f,56,77)}}>{it.marker}</div>
  </Card>};
 return <Base title={title}>
  <div style={{position:'absolute',top:535,left:70,right:70,display:'flex',gap:14,justifyContent:'space-between'}}>{render(left,0)}{render(right,1)}</div>
  <div style={{position:'absolute',top:1425,left:352,fontSize:58,color:'#4e6a76',fontWeight:950,opacity:ease(f,64,86)}}>違いはここ！</div>
  <Mascot source={characterImage} fade={ease(f,65,86)}/>
 </Base>;
};
export default CompareTemplate;
