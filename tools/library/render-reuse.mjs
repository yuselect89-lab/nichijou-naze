import fs from 'node:fs';import path from 'node:path';import {bundle} from '@remotion/bundler';import {openBrowser,selectComposition,renderStill,renderMedia} from '@remotion/renderer';
import {ROOT,read,resolve,refsOf,preflight,sha,safe} from './core.mjs';import {buildCatalog} from './adapters.mjs';
const project=process.argv[2]??'episodes/LIBRARY_REUSE_TEST/manifest.json',m=read(project),locked=process.argv.includes('--locked'),candidate=process.argv.includes('--qc-candidate');
if(candidate&&locked)throw Error('Choose candidate QC or locked handoff, not both');
if(!candidate&&!locked){let c=buildCatalog();let p=preflight(c,read(m.requirements??path.posix.join(path.posix.dirname(project),'requirements.json')));if(!p.ready)throw Error('Preflight blocked: '+JSON.stringify(p.decisions));for(const r of refsOf(m)){const a=resolve(c,r);if(a.asset_id==='NNZ_MODEL_ICE_MICRO_01'&&a.entrypoint!=='common_assets/nichijou_naze/models/ice_science/1.1.0/index.mjs')throw Error('Unsupported model runtime binding');}}
if(locked){const lock=read('asset-lock.json');for(const f of lock.files){const {digest}=await import('./core.mjs');if(digest(f.path)!==f.sha256)throw Error('Exported dependency changed: '+f.path)};}
const dir=locked?'out/reuse':'validation/library-ops';fs.mkdirSync(path.join(ROOT,dir),{recursive:true});
const serveUrl=await bundle({entryPoint:path.join(ROOT,'src/library-reuse/index.jsx')});const browser=await openBrowser('chrome',{browserExecutable:'/usr/bin/chromium',chromiumOptions:{gl:'swangle'}});const opts={serveUrl,puppeteerInstance:browser,chromiumOptions:{gl:'swangle'},logLevel:'error',timeoutInMilliseconds:120000};const observations=[];
const log=l=>{if(l.text.includes('REUSE_QC '))observations.push(JSON.parse(l.text.split('REUSE_QC ')[1]))};
try{
 if(candidate){for(const [asset_id,frames] of [['NNZ_MODEL_ICE_MICRO_01',[0,90]],['NNZ_MODEL_FREEZING_CELL_01',[0,170]],['NNZ_MODEL_ICECAN_AIR_01',[45,130]],['NNZ_MODEL_ICECAN_DRAIN_01',[0,160]]]){
 const inputProps={asset_id,parameters:{},view:{scale:1,x:0,y:0},character:null,qc:true},composition=await selectComposition({...opts,id:'NNZ-REUSE',inputProps});for(const [i,frame] of frames.entries()){await renderStill({...opts,composition,inputProps,frame,output:path.join(ROOT,dir,asset_id+(i?'-end':'-start')+'.png'),imageFormat:'png',onBrowserLog:log});console.log('QC still',asset_id,frame);}}
 }
 const model=m.assets.find(a=>a.asset_id==='NNZ_MODEL_ICE_MICRO_01');const inputProps={asset_id:model.asset_id,parameters:model.parameters,view:m.view,character:m.character,qc:false};let composition=await selectComposition({...opts,id:'NNZ-REUSE',inputProps});composition={...composition,durationInFrames:m.durationFrames};
 for(const frame of [12,42])await renderStill({...opts,composition,inputProps,frame,output:path.join(ROOT,dir,`reuse-${frame}.png`),imageFormat:'png'});
 if(!process.argv.includes('--stills-only'))await renderMedia({...opts,composition,inputProps,outputLocation:path.join(ROOT,dir,'reuse-test.mp4'),codec:'h264',crf:18,pixelFormat:'yuv420p',concurrency:1});
 fs.writeFileSync(path.join(ROOT,dir,'render-observations.json'),JSON.stringify(observations,null,2)+'\n');console.log('Reuse render complete',dir);
}finally{await browser.close({silent:true});fs.rmSync(serveUrl,{recursive:true,force:true})}
