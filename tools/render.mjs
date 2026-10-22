import {readFileSync,mkdirSync,rmSync,existsSync} from 'node:fs';
import path from 'node:path';
import {bundle} from '@remotion/bundler';
import {openBrowser,selectComposition,renderMedia} from '@remotion/renderer';
import {validateConfig} from './config.mjs';
import {verifyProduction} from './verify-production.mjs';
verifyProduction();
const [file,dest]=process.argv.slice(2);if(!file||!dest)throw new Error('Usage: npm run render -- scene.json out/cut.mp4');
if(existsSync(dest))throw new Error('Output already exists; choose a new filename');
const scene=JSON.parse(readFileSync(file,'utf8')),config=validateConfig(scene.config??scene);
if(config.mode==='overlay')throw new Error('Overlay is a transparent React layer; import TemplateScene into the parent episode. Use standalone for MP4 previews.');
const inputProps={config,cues:scene.cues??[],voiceover:scene.voiceover};
mkdirSync(path.dirname(dest),{recursive:true});
const url=await bundle({entryPoint:path.resolve('src/index.tsx')});const browser=await openBrowser('chrome',{browserExecutable:'/usr/bin/chromium'});
try{const comp=await selectComposition({serveUrl:url,id:'NNZ-TEMPLATE',inputProps,puppeteerInstance:browser});await renderMedia({serveUrl:url,composition:comp,inputProps,outputLocation:dest,codec:'h264',crf:18,pixelFormat:'yuv420p',concurrency:3,puppeteerInstance:browser,logLevel:'error',onBrowserLog:()=>{}});}finally{await browser.close({silent:true});rmSync(url,{recursive:true,force:true});}
