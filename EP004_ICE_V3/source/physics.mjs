export const parameters={width:1.15,depth:1.16,initialHeight:3.38,residualHeight:.035,bottom:1.025,receiverWidth:1.04,receiverDepth:3.72,receiverBottom:.435};
export const smooth=x=>{const t=Math.max(0,Math.min(1,x));return t*t*(3-2*t)};
export function drainageState(frame){
 const t=frame/30,p=parameters,insert=smooth(t/.85),q=smooth((t-1.02)/3.95);
 const height=p.initialHeight-(p.initialHeight-p.residualHeight)*q;
 const initialVolume=p.width*p.depth*p.initialHeight,sourceVolume=p.width*p.depth*height;
 const removed=initialVolume-sourceVolume,receiverHeight=removed/(p.receiverWidth*p.receiverDepth);
 return {frame,time:t,insert,drainFraction:q,coreHeight:height,surfaceHeight:p.bottom+height,sourceVolume,removedVolume:removed,receiverHeight,receiverVolume:p.receiverWidth*p.receiverDepth*receiverHeight,flowing:q>.00001&&q<.99999};
}
