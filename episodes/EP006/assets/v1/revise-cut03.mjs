// Incremental rerender after visual QC. Full reproduction uses render.mjs.
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';import {execFileSync} from 'node:child_process';
import {bundle} from '@remotion/bundler';import {openBrowser,selectComposition,renderStill,renderMedia} from '@remotion/renderer';
const here=path.dirname(fileURLToPath(import.meta.url)),ep=path.resolve(here,'../..'),p=path.join(ep,'preview/v1'),e=path.join(ep,'evidence/v1/rejected-cut03-crop');fs.mkdirSync(e);
execFileSync('node',['tools/verify-production.mjs'],{stdio:'inherit'});
fs.renameSync(path.join(p,'CUT03-1080.png'),path.join(e,'CUT03-FAIL.png'));
fs.writeFileSync(path.join(e,'reason.txt'),'Pointing hand was clipped and did not align with an explanatory target. Viewport widened; independent label and leader added in pointing direction. Only CUT03 changes; all other rendered frames retained.\n');
const url=await bundle({entryPoint:path.join(here,'index.tsx'),publicDir:ep}),browser=await openBrowser('chrome',{browserExecutable:'/usr/bin/chromium'});
try{
 const comp=await selectComposition({serveUrl:url,id:'EP006-ASSET-PREVIEW',puppeteerInstance:browser});
 await renderStill({serveUrl:url,composition:comp,frame:345,output:path.join(p,'CUT03-1080.png'),puppeteerInstance:browser,imageFormat:'png'});
 await renderMedia({serveUrl:url,composition:comp,frameRange:[300,419],outputLocation:path.join(p,'CUT03-revised-native.mp4'),codec:'h264',crf:18,pixelFormat:'yuv420p',concurrency:3,puppeteerInstance:browser,logLevel:'error'});
}finally{await browser.close({silent:true});fs.rmSync(url,{recursive:true,force:true});}
const original=path.join(p,'EP006-material-preview-1080.mp4'),old=path.join(e,'prior-native.mp4');fs.renameSync(original,old);
execFileSync('ffmpeg',['-nostdin','-v','error','-i',old,'-i',path.join(p,'CUT03-revised-native.mp4'),'-filter_complex','[0:v]trim=start_frame=0:end_frame=300,setpts=PTS-STARTPTS[a];[1:v]setpts=PTS-STARTPTS[b];[0:v]trim=start_frame=420:end_frame=1050,setpts=PTS-STARTPTS[c];[a][b][c]concat=n=3:v=1:a=0[out]','-map','[out]','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p',original],{stdio:'inherit'});
fs.renameSync(path.join(p,'CUT03-revised-native.mp4'),path.join(e,'CUT03-revision-native.mp4'));
console.log('CUT03 revision rendered and integrated; rerun postprocess.py on final native video.');
