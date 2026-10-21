import {bundle} from '@remotion/bundler';
import {openBrowser,selectComposition,renderStill,renderMedia} from '@remotion/renderer';
import {writeFileSync,rmSync,copyFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
const root=process.cwd(),serveUrl=await bundle({entryPoint:root+'/EP004_ICE_V3/source/index.jsx'});
const browser=await openBrowser('chrome',{browserExecutable:'/usr/bin/chromium',chromiumOptions:{gl:'swangle'}});
const opts={serveUrl,puppeteerInstance:browser,chromiumOptions:{gl:'swangle'},logLevel:'error'};
const observations=[];
const log=l=>{const n=l.text.indexOf('EP004_V3_QC ');if(n>=0)observations.push(JSON.parse(l.text.slice(n+12)));};
const ffmpeg=args=>{const r=spawnSync('ffmpeg',['-v','error','-y',...args],{stdio:'inherit'});if(r.status)throw Error('ffmpeg failed')};
try{
 if(!process.argv.includes('--overlays-only')){
 const c1=await selectComposition({...opts,id:'EP004-V3-CUT01'});
 for(const frame of [0,52,104])await renderStill({...opts,composition:c1,frame,output:`EP004_ICE_V3/preview/cut01-${frame}.png`,imageFormat:'png'});
 await renderMedia({...opts,composition:c1,outputLocation:'EP004_ICE_V3/cut01/animation.mp4',codec:'h264',crf:17,pixelFormat:'yuv420p',concurrency:2});console.log('Cut01 complete');
 for(const frame of [0,15,30,45,60,85,110,135,150,164]){
  const inputProps={layer:'composite',report:true},composition=await selectComposition({...opts,id:'EP004-V3-CUT09',inputProps});
  await renderStill({...opts,composition,inputProps,frame,output:`EP004_ICE_V3/preview/cut09-${frame}.png`,imageFormat:'png',onBrowserLog:log});console.log('Cut09 still',frame);
 }
 writeFileSync('EP004_ICE_V3/qc/render_observations.json',JSON.stringify(observations,null,2));
 for(const layer of ['background','model']){
  const inputProps={layer},composition=await selectComposition({...opts,id:'EP004-V3-CUT09',inputProps});
  await renderStill({...opts,composition,inputProps,frame:85,output:`EP004_ICE_V3/cut09/${layer}.png`,imageFormat:'png'});
 }
 let previous=-1;const inputProps={layer:'base',report:false},composition=await selectComposition({...opts,id:'EP004-V3-CUT09',inputProps});
 await renderMedia({...opts,composition,inputProps,outputLocation:'EP004_ICE_V3/cut09/base_animation.mp4',codec:'h264',crf:17,pixelFormat:'yuv420p',concurrency:2,onProgress:p=>{const percent=Math.floor(p.progress*10);if(percent!==previous){previous=percent;console.log('Cut09 3D',percent*10+'%')}}});
 console.log('Cut09 3D complete');
 }
 for(const layer of ['character','labels']){
  const props={layer},comp=await selectComposition({...opts,id:'EP004-V3-CUT09',inputProps:props});
  await renderMedia({...opts,composition:comp,inputProps:props,outputLocation:`EP004_ICE_V3/cut09/${layer}_overlay.webm`,codec:'vp9',imageFormat:'png',pixelFormat:'yuva420p',crf:15,concurrency:2});console.log(layer,'alpha complete');
 }
 ffmpeg(['-i','EP004_ICE_V3/cut09/base_animation.mp4','-c:v','libvpx-vp9','-i','EP004_ICE_V3/cut09/character_overlay.webm','-c:v','libvpx-vp9','-i','EP004_ICE_V3/cut09/labels_overlay.webm','-filter_complex','[0:v][1:v]overlay=0:0[a];[a][2:v]overlay=0:0,format=yuv420p[out]','-map','[out]','-an','-c:v','libx264','-crf','17','-preset','medium','-r','30','-frames:v','165','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','EP004_ICE_V3/cut09/animation.mp4']);
 copyFileSync('EP004_ICE_V3/preview/cut09-85.png','EP004_ICE_V3/cut09/main.png');
 copyFileSync('EP004_ICE_V3/preview/cut01-52.png','EP004_ICE_V3/cut01/main.png');
 console.log('Stage1 rendering complete');
}finally{await browser.close({silent:true});rmSync(serveUrl,{recursive:true,force:true});}
