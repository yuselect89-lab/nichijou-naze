import fs from 'node:fs';import path from 'node:path';import {fileURLToPath} from 'node:url';
import {bundle} from '@remotion/bundler';import {openBrowser,selectComposition,renderStill} from '@remotion/renderer';
const here=path.dirname(fileURLToPath(import.meta.url)),ep=path.resolve(here,'../..');
const url=await bundle({entryPoint:path.join(here,'index.tsx'),publicDir:ep}),browser=await openBrowser('chrome',{browserExecutable:'/usr/bin/chromium'});
try{
 const comp=await selectComposition({serveUrl:url,id:'EP006-SCIENCE-CONTINUOUS',puppeteerInstance:browser});
 for(const layer of ['object','skin','tissue','vessels','outline','labels'])await renderStill({serveUrl:url,composition:{...comp,props:{scene:'science',layer,labels:true}},frame:410,output:path.join(here,`science-${layer}-frame410.png`),puppeteerInstance:browser,imageFormat:'png'});
 const episode=await selectComposition({serveUrl:url,id:'EP006-ASSET-PREVIEW',puppeteerInstance:browser});
 for(const [cut,frame] of [['CUT02',240],['CUT03',345],['CUT07',970]])await renderStill({serveUrl:url,composition:{...episode,props:{scene:'episode',layer:'character',labels:false}},frame,output:path.join(here,`${cut}-character-alpha.png`),puppeteerInstance:browser,imageFormat:'png'});
}finally{await browser.close({silent:true});fs.rmSync(url,{recursive:true,force:true});}
console.log('Alpha layer exports rendered; inspect with postprocess.py');
