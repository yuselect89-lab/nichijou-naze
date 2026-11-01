#!/usr/bin/env node
// Samples unchanged-or-changed media into small contact sheets; NOT a substitute for G2/G3.
import {spawnSync} from 'node:child_process';
import {existsSync,mkdirSync,readdirSync,readFileSync,writeFileSync,rmSync,statSync,createReadStream,copyFileSync} from 'node:fs';
import path from 'node:path';
import {createHash} from 'node:crypto';
const argv=process.argv.slice(2),source=argv[0];
const opt=(flag,fallback)=>{const i=argv.indexOf(flag);return i<0?fallback:argv[i+1]};
if(!source||!existsSync(source)){console.error('Usage: node media-evidence.mjs <media-directory> [--out out/qc/evidence] [--prior old.json] [--limit 12]');process.exit(2)}
const root=path.resolve(source),dest=path.resolve(opt('--out','out/qc/media-evidence')),priorPath=opt('--prior',null),limit=Number(opt('--limit','12'));
if(!Number.isInteger(limit)||limit<1||limit>24)throw Error('limit must be 1..24');
if(!statSync(root).isDirectory()||dest===root)throw Error('Use a media directory and a different output directory');
const formats=/\.(?:mp4|mov|mkv|webm|gif|png|jpg|jpeg|webp)$/i;
const all=readdirSync(root,{withFileTypes:true}).filter(d=>d.isFile()&&formats.test(d.name)).map(d=>d.name).sort();
const prior=priorPath?JSON.parse(readFileSync(priorPath,'utf8')):null;
const prev=new Map((prior?.files||[]).map(f=>[f.path,f.sha256]));
mkdirSync(dest,{recursive:true});
const tmp=path.join(dest,'_evidence_frames');rmSync(tmp,{recursive:true,force:true});mkdirSync(tmp,{recursive:true});
const probe=file=>{
 const r=spawnSync('ffprobe',['-v','error','-show_entries','format=duration:stream=codec_type,width,height,r_frame_rate,pix_fmt','-of','json',file],{encoding:'utf8',maxBuffer:1048576});
 if(r.status!==0)throw Error((r.stderr||'ffprobe failed').slice(0,500));
 return JSON.parse(r.stdout);
};
const sha=file=>new Promise((resolve,reject)=>{
 const h=createHash('sha256'),s=createReadStream(file);
 s.on('data',b=>h.update(b));s.on('error',reject);s.on('end',()=>resolve(h.digest('hex')));
});
const files=[],frames=[],errors=[];let n=0,selected=0;
for(const name of all){
 const file=path.join(root,name),digest=await sha(file),same=prev.get(name)===digest;
 const info={path:name,bytes:statSync(file).size,sha256:digest,changed:!same};files.push(info);
 if(same){info.preview='UNCHANGED_PREVIOUS_MANIFEST';continue}
 if(selected>=limit){info.preview='NOT_SAMPLED_LIMIT';continue}
 selected++;
 try{
  const data=probe(file),v=(data.streams||[]).find(x=>x.codec_type==='video');
  if(!v)throw Error('no visual stream');
  const duration=Number(data.format?.duration)||0;info.width=v.width;info.height=v.height;info.durationSeconds=duration;
  const still=/\.(?:png|jpg|jpeg|webp)$/i.test(name),times=still?[null]:[Math.max(0,duration*.20),Math.max(0,duration*.70)];
  info.preview='SAMPLED_NOT_QC_PASS';info.frameIds=[];
  for(const second of times){
   const out=path.join(tmp,`frame_${String(n).padStart(4,'0')}.jpg`);
   const args=['-hide_banner','-v','error','-y'];
   if(second!==null)args.push('-ss',String(second));
   args.push('-i',file,'-frames:v','1','-vf','scale=440:440:force_original_aspect_ratio=decrease,pad=440:440:(ow-iw)/2:(oh-ih)/2:color=black,format=yuv420p','-q:v','3',out);
   const r=spawnSync('ffmpeg',args,{encoding:'utf8',maxBuffer:1048576});
   if(r.status!==0)throw Error((r.stderr||'ffmpeg extract failed').slice(0,500));
   info.frameIds.push(n);frames.push({frameIndex:n,file:name,seconds:second});n++;
  }
 }catch(e){info.preview='PREVIEW_FAILED';errors.push({path:name,error:e.message})}
}
const sheets=[];
for(let k=0;k<n;k+=12){
 const batch=path.join(tmp,'batch');rmSync(batch,{recursive:true,force:true});mkdirSync(batch,{recursive:true});
 const slice=frames.slice(k,k+12);
 slice.forEach((f,i)=>copyFileSync(path.join(tmp,`frame_${String(f.frameIndex).padStart(4,'0')}.jpg`),path.join(batch,`shot_${String(i).padStart(3,'0')}.jpg`)));
 const out=path.join(dest,`contact_${String(sheets.length+1).padStart(2,'0')}.jpg`);
 const r=spawnSync('ffmpeg',['-hide_banner','-v','error','-y','-framerate','1','-i',path.join(batch,'shot_%03d.jpg'),'-frames:v','1','-vf',`tile=3x${Math.ceil(slice.length/3)}:margin=4:padding=4`,'-q:v','3',out],{encoding:'utf8',maxBuffer:1048576});
 if(r.status!==0){errors.push({sheet:out,error:(r.stderr||'tile failed').slice(0,500)});continue}
 sheets.push(out);
}
rmSync(tmp,{recursive:true,force:true});
const packet={status:(errors.length||files.some(f=>f.preview==='NOT_SAMPLED_LIMIT'))?'EVIDENCE_INCOMPLETE':'EVIDENCE_ONLY_NOT_QC_PASS',source:root,generatedAt:new Date().toISOString(),fileCount:all.length,sampledFiles:selected,skippedByLimit:files.filter(f=>f.preview==='NOT_SAMPLED_LIMIT').length,sheets,frames,files,errors};
const json=path.join(dest,'evidence.json');writeFileSync(json,JSON.stringify(packet,null,2)+'\n');
console.log(JSON.stringify({status:packet.status,files:all.length,sampled:selected,skippedByLimit:packet.skippedByLimit,unchanged:files.filter(f=>!f.changed).length,contactSheets:sheets,summary:json,errors},null,2));
if(errors.length||packet.skippedByLimit)process.exitCode=1;
