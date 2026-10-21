import React from 'react';
import {AbsoluteFill} from 'remotion';
import {SeriesFrame,Cue} from '../../../../src/integration/v1.0.1/Series';

/** One per episode, OUTSIDE Sequences. Reuses the unchanged series overlay. */
export const EpisodeChrome:React.FC<{children:React.ReactNode;cues?:Cue[];voiceover?:string;totalFrames?:number;bannerFrames?:number}>=props=><AbsoluteFill className="nnz-extension">
 <style>{`.nnz-extension [data-qc="caption"]{width:824px!important;top:1500px!important;height:240px!important;font-size:54px!important}`}</style>
 <SeriesFrame {...props}/>
 </AbsoluteFill>;
