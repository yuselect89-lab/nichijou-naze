export const cleanCaption=(s:string)=>s.replace(/、/g,'');
export const episodeProgress=(frame:number,totalFrames:number)=>Math.min(1,Math.max(0,frame/Math.max(1,totalFrames-1)));
export function validateCues(cues:{fromFrame:number;toFrame:number;text:string}[],totalFrames:number){
 let end=0;
 for(const c of cues){if(!Number.isInteger(c.fromFrame)||!Number.isInteger(c.toFrame)||c.fromFrame<end||c.toFrame<=c.fromFrame||c.toFrame>totalFrames||typeof c.text!=='string')throw new Error('Caption frames must be ordered, non-overlapping and within the episode');if(cleanCaption(c.text).split('\n').length>2)throw new Error('Caption may have at most two lines');end=c.toFrame;}
}
