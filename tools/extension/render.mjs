import {bundle} from '@remotion/bundler';
import {openBrowser,selectComposition,renderStill,renderMedia} from '@remotion/renderer';
import {writeFileSync,rmSync,readFileSync,mkdirSync} from 'node:fs';
import {validateScene} from '../../common_assets/nichijou_naze/runtime/v1.1.0/config.ts';
import {validateConfig as validateLegacy} from '../config.mjs';
const root=process.cwd(),base='common_assets/nichijou_naze/layouts/v1.1.0/examples/';
const single=process.argv[2];
if(single){
 const config=validateScene(JSON.parse(readFileSync(single,'utf8')));
 if(config.legacyOverlay)validateLegacy({...config.legacyOverlay.config,id:config.legacyOverlay.id,mode:'overlay',characterVersion:'v02_highres'});
 mkdirSync('out/extension',{recursive:true});
 const serveUrl=await bundle({entryPoint:root+'/src/extension/index.tsx'});
 const browser=await openBrowser('chrome',{browserExecutable:'/usr/bin/chromium'});
 try{const inputProps={config};const composition=await selectComposition({serveUrl,id:'NNZ-FULLFRAME',inputProps,puppeteerInstance:browser});await renderMedia({serveUrl,composition,inputProps,puppeteerInstance:browser,outputLocation:`out/extension/${config.id}.mp4`,codec:'h264',crf:18,concurrency:3,logLevel:'error'});}finally{await browser.close({silent:true});rmSync(serveUrl,{recursive:true,force:true});}
 process.exit(0);
}
const ids=JSON.parse(readFileSync(base+'playlist.json','utf8')),configs=ids.map(id=>validateScene(JSON.parse(readFileSync(base+id+'.json','utf8'))));
for(const c of configs)if(c.legacyOverlay)validateLegacy({...c.legacyOverlay.config,id:c.legacyOverlay.id,mode:'overlay',characterVersion:'v02_highres'});
mkdirSync('validation/extension',{recursive:true});
const serveUrl=await bundle({entryPoint:root+'/src/extension/index.tsx'}),observations=[];
const browser=await openBrowser('chrome',{browserExecutable:'/usr/bin/chromium'});
try{
 const composition=await selectComposition({serveUrl,id:'NNZ-LIBRARY-EXTENSION-QC',puppeteerInstance:browser});
 let from=0;const samples=[];
 for(const c of configs){const locals=c.id==='expression-surprise'?[0,85]:c.id==='focus-crosssection-return'?[0,24,49,64,80,110,180,205,239]:c.id==='motions'?[0,7,30,70,95,130,150,180,226,239]:c.id==='crosssection-carton'?[10,75,165]:c.id==='step3-cause'?[30,100,170]:[Math.min(85,c.durationFrames-1)];
 for(const local of locals)samples.push({scene:c.id,local,frame:from+local});from+=c.durationFrames;}
 samples.push({scene:configs.at(-1).id,local:179,frame:composition.durationInFrames-1});
 for(const s of samples){const file=`validation/extension/${s.scene}-${s.local}.png`;
  await renderStill({serveUrl,composition,puppeteerInstance:browser,frame:s.frame,output:file,imageFormat:'png',logLevel:'error',onBrowserLog:l=>{const n=l.text.indexOf('NNZ_EXTENSION_QC ');if(n>=0)observations.push(JSON.parse(l.text.slice(n+17)));}});
  console.log('Still',s.scene,s.local);
 }
 writeFileSync('validation/extension/samples.json',JSON.stringify(samples,null,2));writeFileSync('validation/extension/observations.json',JSON.stringify(observations,null,2));
 console.log('Rendering',composition.durationInFrames,'frames at1080x1920');
 let last=-1;
 const videoComposition=await selectComposition({serveUrl,id:'NNZ-LIBRARY-EXTENSION-QC',inputProps:{qc:false},puppeteerInstance:browser});
 await renderMedia({serveUrl,composition:videoComposition,inputProps:{qc:false},puppeteerInstance:browser,outputLocation:'validation/extension/library-extension-1080x1920.mp4',codec:'h264',crf:18,pixelFormat:'yuv420p',concurrency:3,logLevel:'error',onBrowserLog:()=>{},onProgress:p=>{const percent=Math.floor(p.progress*10);if(percent!==last){last=percent;console.log('MP4',percent*10+'%');}}});
}finally{await browser.close({silent:true});rmSync(serveUrl,{recursive:true,force:true});}
