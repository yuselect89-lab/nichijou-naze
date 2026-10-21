export type Rect={x:number;y:number;width:number;height:number};
export type Point={x:number;y:number};
export type Media={src:string;kind?:'image'|'video';objectPosition?:string};
export const layoutIDs=['NNZ_LAYOUT_FOOTAGE_01','NNZ_LAYOUT_DIAGRAM_01','NNZ_LAYOUT_FOCUS_01'] as const;
export const diagramIDs=['NNZ_TMP_LABEL_01','NNZ_TMP_STEP3_01','NNZ_TMP_CROSSSECTION_01'] as const;
export const poses=['neutral','talk','point_right','point_left','think','surprise','happy','troubled'] as const;
export type Pose=typeof poses[number];
export type Character={side?:'left'|'right';height?:number;top?:number;enterFrame?:number;exitFrame?:number;transitionFrames?:number;entry?:'fade'|'slide';idle?:boolean;nodAt?:number[];poses:{fromFrame:number;pose:Pose}[]};
export type Label={id:string;text:string;anchor:Point;box:Rect;fromFrame:number;toFrame?:number;color?:string};
export type Arrow={from:Point;to:Point;fromFrame:number;color?:string};
export type Step={text:string;fromFrame:number;image?:string;shape?:'dots'|'inward'|'bubbles';color?:string};
export type CrossPart={id:string;image:string;fromFrame:number;toFrame?:number;opacity?:number};
export type CrossSection={outside:string;parts:CrossPart[];region:Rect;cutLine?:string};
export type Focus={target:Point;zoom:number;zoomFromFrame:number;revealFromFrame:number;revealFrames:number;returnFromFrame?:number};
export type Scene={id:string;revision:'1.1.0';layout:typeof layoutIDs[number];durationFrames:number;background:Media;title?:string;
 character?:Character;labels?:Label[];arrows?:Arrow[];steps?:Step[];crossSection?:CrossSection;focus?:Focus;
 legacyOverlay?:{id:'NNZ_TMP_ARROW_01'|'NNZ_TMP_COMPARE_01'|'NNZ_TMP_ZOOM_01';fromFrame:number;durationFrames:number;config:Record<string,unknown>};
 protectedSubjects?:Rect[]};
export const clamp01=(n:number)=>Math.max(0,Math.min(1,n));
export const smooth=(frame:number,start:number,length:number)=>{const t=clamp01((frame-start)/length);return t*t*(3-2*t)};
export const intersects=(a:Rect,b:Rect)=>a.x<b.x+b.width&&a.x+a.width>b.x&&a.y<b.y+b.height&&a.y+a.height>b.y;
export function characterFile(pose:string){
 if(!(poses as readonly string[]).includes(pose))throw Error('Unknown production pose: '+pose);
 const root='common_assets/nichijou_naze/characters/female_v01/';
 return root+(['surprise','happy','troubled'].includes(pose)?'versions/v03_expressions/':'')+'poses/NNZ_CHAR_FEMALE_01_pose_'+pose+'.png';
}
export function characterRect(c:Character):Rect{
 const height=c.height??420,width=height*2/3;
 return {x:c.side==='right'?900-width:90,y:c.top??1045,width,height};
}
export function motionAt(c:Character,frame:number,duration:number){
 const transition=c.transitionFrames??14,enter=smooth(frame,c.enterFrame??0,transition);
 const exit=smooth(frame,c.exitFrame??duration-transition,transition);
 const idle=c.idle===false?0:Math.sin(frame*Math.PI/60)*3;
 const nod=(c.nodAt??[]).reduce((sum,start)=>{const t=(frame-start)/24;return sum+(t>=0&&t<=1?Math.sin(t*2*Math.PI)*1.4:0)},0);
 return {opacity:enter*(1-exit),x:(c.entry==='fade'?0:(c.side==='right'?1:-1)*36)*(1-enter+exit),y:idle+exit*10,rotation:nod};
}
export function poseWeights(c:Character,frame:number){
 const timeline=c.poses,fade=10;
 const active=timeline.reduce((n,p,i)=>frame>=p.fromFrame?i:n,0),current=timeline[active];
 if(active===0)return [{pose:current.pose,opacity:1}];
 const mix=smooth(frame,current.fromFrame,fade);
 return [{pose:timeline[active-1].pose,opacity:1-mix},{pose:current.pose,opacity:mix}].filter(x=>x.opacity>0);
}
export function focusAt(c:Focus,frame:number){
 const zoom=smooth(frame,c.zoomFromFrame,24),reveal=smooth(frame,c.revealFromFrame,c.revealFrames);
 const back=c.returnFromFrame===undefined?0:smooth(frame,c.returnFromFrame,30);
 return {zoom:1+(c.zoom-1)*zoom*(1-back),reveal:reveal*(1-back),back};
}
function number(n:unknown,min:number,max:number,name:string){if(typeof n!=='number'||!Number.isFinite(n)||n<min||n>max)throw Error(name+' out of range');}
function frame(n:number,max:number,name:string){number(n,0,max,name);if(!Number.isInteger(n))throw Error(name+' must be integer');}
function rect(r:Rect){for(const k of ['x','y','width','height'] as const)number(r[k],0,k==='y'||k==='height'?1920:1080,k);if(!r.width||!r.height||r.x+r.width>1080||r.y+r.height>1920)throw Error('Invalid rectangle');}
function point(p:Point){number(p.x,0,1080,'x');number(p.y,0,1920,'y');}
function media(s:string){if(typeof s!=='string'||!s.trim()||s.startsWith('/')||s.split('/').includes('..')||/^(data|javascript):/.test(s))throw Error('Use a public-relative media path or HTTPS URL');if(s.includes('://')&&!s.startsWith('https://'))throw Error('HTTPS media only');}
function safe(r:Rect){if(r.x<72||r.x+r.width>920||r.y<320||r.y+r.height>1480)throw Error('Foreground leaves Shorts safe zone');}
export function validateScene(c:Scene):Scene{
 if(c.revision!=='1.1.0'||!layoutIDs.includes(c.layout))throw Error('Unknown layout/revision');
 if(typeof c.id!=='string'||!c.id)throw Error('Scene ID required');
 frame(c.durationFrames,3600,'durationFrames');if(c.durationFrames<60)throw Error('Scene needs at least60frames');
 media(c.background.src);if(c.background.kind&&!['image','video'].includes(c.background.kind))throw Error('Unsupported media kind');
 if(c.title&&c.title.length>20)throw Error('Title exceeds20characters');
 for(const s of c.protectedSubjects??[]){rect(s);safe(s);}
 if(c.character){const a=c.character,r=characterRect(a);rect(r);safe(r);if(a.side&&!['left','right'].includes(a.side))throw Error('Character side');
  number(r.height,260,1150,'character height');if(a.entry&&!['fade','slide'].includes(a.entry))throw Error('Character entry');
  frame(a.transitionFrames??14,30,'transitionFrames');if((a.transitionFrames??14)<8)throw Error('Transition too short');
  const start=a.enterFrame??0,end=a.exitFrame??c.durationFrames-(a.transitionFrames??14);
  frame(start,c.durationFrames,'enter');frame(end,c.durationFrames,'exit');if(end<start+(a.transitionFrames??14)||end+(a.transitionFrames??14)>c.durationFrames)throw Error('Entry/exit timing');
  if(!a.poses?.length||a.poses[0].fromFrame!==0)throw Error('Pose timeline must start at0');
  a.poses.forEach((p,i)=>{characterFile(p.pose);frame(p.fromFrame,c.durationFrames-1,'pose frame');if(i&&p.fromFrame<a.poses[i-1].fromFrame+10)throw Error('Pose cues need10frames spacing');});
  for(const n of a.nodAt??[])frame(n,c.durationFrames-24,'nod');
  for(const s of c.protectedSubjects??[])if(intersects(r,s))throw Error('Character covers protected subject');
 }
 const ids=new Set<string>();
 for(const l of c.labels??[]){if(!l.id||ids.has(l.id))throw Error('Duplicate label ID');ids.add(l.id);point(l.anchor);rect(l.box);safe(l.box);if(l.box.width<180||l.box.height<70||!l.text||l.text.length>14)throw Error('Label size/text');frame(l.fromFrame,c.durationFrames-1,'label');if(l.toFrame!==undefined){frame(l.toFrame,c.durationFrames,'label end');if(l.toFrame<=l.fromFrame)throw Error('Label end');}if(c.character&&intersects(l.box,characterRect(c.character)))throw Error('Label overlaps character');}
 for(const a of c.arrows??[]){point(a.from);point(a.to);frame(a.fromFrame,c.durationFrames-1,'arrow');}
 if(c.steps){if(c.steps.length!==3)throw Error('STEP3 needs3steps');c.steps.forEach((s,i)=>{if(!s.text||s.text.length>18)throw Error('Step text');frame(s.fromFrame,c.durationFrames-1,'step');if(i&&s.fromFrame<c.steps![i-1].fromFrame+12)throw Error('Steps must be ordered');if(s.image)media(s.image);if(s.shape&&!['dots','inward','bubbles'].includes(s.shape))throw Error('Step shape');});if(c.character&&intersects(characterRect(c.character),{x:90,y:350,width:820,height:1080}))throw Error('STEP3 uses main area; hide character or select a different layout');}
 if(c.crossSection){media(c.crossSection.outside);rect(c.crossSection.region);safe(c.crossSection.region);if(!c.crossSection.parts.length)throw Error('Crosssection parts required');const pids=new Set<string>();for(const p of c.crossSection.parts){if(pids.has(p.id))throw Error('Duplicate part ID');pids.add(p.id);media(p.image);frame(p.fromFrame,c.durationFrames-1,'part');if(p.toFrame!==undefined){frame(p.toFrame,c.durationFrames,'part end');if(p.toFrame<=p.fromFrame)throw Error('Part end');}number(p.opacity??1,0,1,'part opacity');}}
 if(c.focus){point(c.focus.target);number(c.focus.zoom,1.2,3,'zoom');frame(c.focus.zoomFromFrame,c.durationFrames-24,'zoom start');frame(c.focus.revealFromFrame,c.durationFrames-1,'reveal start');frame(c.focus.revealFrames,90,'reveal duration');if(c.focus.revealFrames<8||c.focus.revealFromFrame<c.focus.zoomFromFrame+24)throw Error('Reveal must follow zoom');if(c.focus.revealFromFrame+c.focus.revealFrames>c.durationFrames)throw Error('Reveal duration');if(c.focus.returnFromFrame!==undefined){frame(c.focus.returnFromFrame,c.durationFrames-30,'return');if(c.focus.returnFromFrame<c.focus.revealFromFrame+c.focus.revealFrames+12)throw Error('Return too early');}}
 if(c.layout==='NNZ_LAYOUT_FOCUS_01'&&(!c.focus||!c.crossSection))throw Error('Focus layout needs focus and crosssection');
 if(c.legacyOverlay){frame(c.legacyOverlay.fromFrame,c.durationFrames-1,'legacy start');frame(c.legacyOverlay.durationFrames,c.durationFrames,'legacy duration');if(c.legacyOverlay.fromFrame+c.legacyOverlay.durationFrames>c.durationFrames)throw Error('Legacy overlay duration');if(c.character)throw Error('Legacy overlay includes its own mascot; do not add another');}
 return c;
}
