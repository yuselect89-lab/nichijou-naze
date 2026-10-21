import {bundle} from '@remotion/bundler';
import {openBrowser,selectComposition,renderStill,renderMedia} from '@remotion/renderer';
import {writeFileSync,rmSync} from 'node:fs';
const url=await bundle({entryPoint:process.cwd()+'/src/highres-validation/index.tsx'});
const browser=await openBrowser('chrome',{browserExecutable:'/usr/bin/chromium'}),observations=[];
try{
 const comp=await selectComposition({serveUrl:url,id:'NNZ-FEMALE-HIGHRES-QC',puppeteerInstance:browser});
 const times=[45,135,225,315,405,480,540,640,730,820];
 for(const frame of times)await renderStill({serveUrl:url,composition:comp,puppeteerInstance:browser,frame,output:`validation/highres/frame-${frame}.png`,imageFormat:'png',logLevel:'error',onBrowserLog:l=>{const n=l.text.indexOf('NNZ_HIGHRES_QC ');if(n>=0)observations.push(JSON.parse(l.text.slice(n+15)));}});
 await renderMedia({serveUrl:url,composition:comp,puppeteerInstance:browser,outputLocation:'validation/highres/character-layout-1080x1920.mp4',codec:'h264',crf:18,pixelFormat:'yuv420p',concurrency:3,logLevel:'error',onBrowserLog:()=>{}});
 writeFileSync('validation/highres/observations.json',JSON.stringify(observations,null,2));
}finally{await browser.close({silent:true});rmSync(url,{recursive:true,force:true});}
