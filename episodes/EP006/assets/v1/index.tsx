import React from 'react';
import {Composition,registerRoot} from 'remotion';
import {Scene} from './Scene';
const Root=()=> <>
  <Composition id="EP006-ASSET-PREVIEW" component={Scene} width={1080} height={1920} fps={30} durationInFrames={1050} defaultProps={{scene:'episode' as const,layer:'all' as const,labels:true}}/>
  <Composition id="EP006-SCIENCE-CONTINUOUS" component={Scene} width={1080} height={1920} fps={30} durationInFrames={450} defaultProps={{scene:'science' as const,layer:'all' as const,labels:true}}/>
  {(['CUT01','CUT02','CUT03','CUT07'] as const).map((cut)=><Composition key={cut} id={`EP006-${cut}`} component={Scene} width={1080} height={1920} fps={30} durationInFrames={cut==='CUT02'||cut==='CUT03'?120:180} defaultProps={{scene:cut,layer:'all' as const,labels:true}}/>)}
</>;
registerRoot(Root);
