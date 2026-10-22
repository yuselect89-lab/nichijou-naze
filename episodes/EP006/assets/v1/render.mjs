import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
import {bundle} from '@remotion/bundler';
import {openBrowser,selectComposition,renderStill,renderMedia} from '@remotion/renderer';
const here=path.dirname(fileURLToPath(import.meta.url));
const ep=path.resolve(here,'../..'),root=path.resolve(ep,'../..'),out=path.join(ep,'preview/v1');
process.chdir(root);
execFileSync('node',['tools/verify-production.mjs'],{stdio:'inherit'});
fs.mkdirSync(out,{recursive:true});
const full=path.join(out,'EP006-material-preview-1080.mp4');
if(fs.existsSync(full))throw Error('Preview exists; use a new delivery version rather than overwriting');
const url=await bundle({entryPoint:path.join(here,'index.tsx'),publicDir:ep});
const browser=await openBrowser('chrome',{browserExecutable:'/usr/bin/chromium'});
const results=[];
try{
 const comp=await selectComposition({serveUrl:url,id:'EP006-ASSET-PREVIEW',puppeteerInstance:browser});
 const frames=[['CUT01',160],['CUT02',240],['CUT03',345],['CUT04',420],['CUT05',650],['CUT06',830],['CUT07',970]];
 for(const [cut,frame] of frames){
   const output=path.join(out,`${cut}-1080.png`);
   await renderStill({serveUrl:url,composition:comp,frame,output,puppeteerInstance:browser,imageFormat:'png'});
   results.push({type:'still',cut,frame,output:path.relative(root,output)});console.log(`Still ${cut} frame ${frame}`);
 }
 const science=await selectComposition({serveUrl:url,id:'EP006-SCIENCE-CONTINUOUS',puppeteerInstance:browser});
 for(const [name,frame] of [['01-start',0],['02-vasoconstriction',90],['03-volume',230],['04-folds-hold',410],['boundary-149',149],['boundary-150',150],['boundary-269',269],['boundary-270',270]]){
   await renderStill({serveUrl:url,composition:science,frame,output:path.join(out,`science-${name}.png`),puppeteerInstance:browser,imageFormat:'png'});
   results.push({type:'science-stage',name,frame});
 }
 // Alpha exports are examples of each editable layer; videos below are opaque review media only.
 for(const layer of ['object','skin','tissue','vessels','outline','labels']){
   await renderStill({serveUrl:url,composition:{...science,props:{...science.props,scene:'science',layer,labels:true}},frame:410,output:path.join(here,`science-${layer}-frame410.png`),puppeteerInstance:browser,imageFormat:'png'});
 }
 await renderStill({serveUrl:url,composition:{...comp,props:{...comp.props,scene:'episode',layer:'character',labels:false}},frame:240,output:path.join(here,'CUT02-character-alpha.png'),puppeteerInstance:browser,imageFormat:'png'});
 console.log('Rendering all seven cuts at 1080x1920 / 30fps (provisional, silent)');
 await renderMedia({serveUrl:url,composition:comp,outputLocation:full,codec:'h264',crf:18,pixelFormat:'yuv420p',concurrency:3,puppeteerInstance:browser,logLevel:'error',onProgress:({progress})=>{const p=Math.floor(progress*100);if(p%10===0&&p!==globalThis.lastProgress){globalThis.lastProgress=p;console.log(`Render ${p}%`);}}});
 results.push({type:'video',frames:1050,width:1080,height:1920,fps:30,output:path.relative(root,full)});
 fs.writeFileSync(path.join(ep,'evidence/v1/render-results.json'),JSON.stringify(results,null,2));
}finally{await browser.close({silent:true});fs.rmSync(url,{recursive:true,force:true});}
