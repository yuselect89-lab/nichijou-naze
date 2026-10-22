/** EP006 original explanatory model, not anatomical measurement. No camera motion. */
export type Point = [number, number];
export const clamp = (x:number) => Math.max(0, Math.min(1, x));
export const smooth = (x:number) => { const t=clamp(x); return t*t*(3-2*t); };
export const SCIENCE_FRAMES=450;
export function state(frame:number) {
  return {vessel:smooth((frame-25)/95), volume:smooth((frame-155)/100), wrinkle:smooth((frame-285)/100)};
}
export function geometry(frame:number) {
  const s=state(frame); const outer:Point[]=[];
  // Single side section, distal end points right. Local inward folds on the finger pad.
  for(let x=180;x<=650;x+=5) outer.push([x,875-12*Math.sin((x-180)/470*Math.PI)]);
  for(let i=1;i<=90;i++){const a=-Math.PI/2+i*Math.PI/90; outer.push([650+200*Math.cos(a),1050+175*Math.sin(a)-10*s.volume*smooth(a/(Math.PI/2))]);}
  for(let x=645;x>=180;x-=5){
    const base=1225+30*Math.sin((650-x)/470*Math.PI);
    const folds=[300,430,560].reduce((n,c)=>n+34*Math.exp(-Math.pow((x-c)/19,2)),0);
    outer.push([x,base-10*s.volume-folds*s.wrinkle]);
  }
  // The exact same inner boundary is used for BOTH epidermis and tissue; no separated layer.
  const inner:Point[]=outer.map(([x,y])=>[x+(500-x)*0.035,y+(1050-y)*0.12]);
  return {outer,inner,skinInner:inner,tissueBoundary:inner,vesselWidth:46-23*s.vessel,
    bloodRadius:9-3*s.volume,bloodOpacity:1-0.58*s.volume,...s};
}
export function path(points:Point[]){return points.map(([x,y],i)=>`${i?'L':'M'}${x.toFixed(3)},${y.toFixed(3)}`).join(' ')+' Z';}
export function vesselAt(t:number):Point{
  const p:Point[]=t<.5?[[198,1108],[300,1085],[350,1135],[440,1094]]:[[440,1094],[530,1053],[620,1088],[757,1067]];
  const u=t<.5?t*2:(t-.5)*2,v=1-u;
  return [0,1].map(k=>v*v*v*p[0][k]+3*v*v*u*p[1][k]+3*v*u*u*p[2][k]+u*u*u*p[3][k]) as Point;
}
export const TIMELINE = [
  {cut:'CUT01',from:0,to:180,role:'question'},
  {cut:'CUT02',from:180,to:300,role:'reaction'},
  {cut:'CUT03',from:300,to:420,role:'reveal_intro'},
  {cut:'CUT04',from:420,to:570,role:'focus_only'},
  {cut:'CUT05',from:570,to:690,role:'focus_only'},
  {cut:'CUT06',from:690,to:870,role:'focus_only'},
  {cut:'CUT07',from:870,to:1050,role:'payoff'},
];
