import {readFileSync,writeFileSync,mkdirSync,rmSync,existsSync} from 'node:fs';
import {bundle} from '@remotion/bundler';
import {openBrowser,selectComposition,renderMedia,renderStill} from '@remotion/renderer';
import {validateConfig} from './config.mjs';
const serveUrl=await bundle({entryPoint:process.cwd()+'/src/index.tsx'});
const browser=await openBrowser('chrome',{browserExecutable:'/usr/bin/chromium'});
const selected=process.argv.slice(2).filter(a=>a!=='--stills-only'),stillsOnly=process.argv.includes('--stills-only');
const report=selected.length&&existsSync('validation/render-observations.json')?JSON.parse(readFileSync('validation/render-observations.json','utf8')).filter(r=>!selected.includes(r.name)):[];mkdirSync('validation',{recursive:true});
try{
 for(const name of ['arrow','compare','zoom','parent']){
  if(selected.length&&!selected.includes(name))continue;
  const inputProps=name==='parent'?{}:{config:validateConfig(JSON.parse(readFileSync(`examples/${name}.json`,'utf8'))),qc:true};
  const id=name==='parent'?'NNZ-OVERLAY-VALIDATION':'NNZ-TEMPLATE';
  const comp=await selectComposition({serveUrl,id,inputProps,puppeteerInstance:browser});
  const observations=[];
  const onBrowserLog=log=>{const p=log.text.indexOf('NNZ_QC ');if(p>=0)observations.push(JSON.parse(log.text.slice(p+7)));};
  const moments=name==='parent'?[0,30,90,150,269,359]:[0,30,100,comp.durationInFrames-1];
  for(const frame of moments)await renderStill({serveUrl,composition:comp,inputProps,frame,puppeteerInstance:browser,output:`validation/${name}-${frame}.png`,imageFormat:'png',onBrowserLog,logLevel:'error'});
  if(!stillsOnly)await renderMedia({serveUrl,composition:comp,inputProps,puppeteerInstance:browser,outputLocation:`validation/${name}.mp4`,codec:'h264',crf:18,pixelFormat:'yuv420p',concurrency:3,logLevel:'error',onBrowserLog:()=>{}});
  report.push({name,frames:comp.durationInFrames,observations});console.log(`Rendered ${name}: ${comp.durationInFrames} frames`);
 }
 if(!selected.length||selected.includes('overlay-transparent')){
 const overlay={...JSON.parse(readFileSync('examples/zoom.json','utf8')),mode:'overlay'};
 const props={config:overlay,qc:true};
 const comp=await selectComposition({serveUrl,id:'NNZ-TEMPLATE',inputProps:props,puppeteerInstance:browser});
 const observations=[];
 await renderStill({serveUrl,composition:comp,inputProps:props,frame:100,puppeteerInstance:browser,output:'validation/overlay-transparent.png',imageFormat:'png',logLevel:'error',onBrowserLog:l=>{const p=l.text.indexOf('NNZ_QC ');if(p>=0)observations.push(JSON.parse(l.text.slice(p+7)));}});
 report.push({name:'overlay-transparent',observations});
 }
 writeFileSync('validation/render-observations.json',JSON.stringify(report,null,2));
}finally{await browser.close({silent:true});rmSync(serveUrl,{recursive:true,force:true});}
