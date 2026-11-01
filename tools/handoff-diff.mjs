#!/usr/bin/env node
// 1エピソード/納品ディレクトリだけをSHA256比較。制作QCを代替しない。
import {createReadStream, promises as fs} from 'node:fs';
import {createHash} from 'node:crypto';
import path from 'node:path';
const argv=process.argv.slice(2), rootArg=argv[0], wi=argv.indexOf('--write');
const writeArg=wi<0?null:argv[wi+1];
const baselineArg=argv[1]&&argv[1]!=='--write'?argv[1]:null;
if(!rootArg||(wi>=0&&!writeArg)){console.error('Usage: node handoff-diff.mjs <delivery-dir> [prior.json] [--write next.json]');process.exit(2)}
const root=path.resolve(rootArg),statRoot=await fs.stat(root).catch(()=>null);
if(!statRoot?.isDirectory()){console.error('Not a directory: '+root);process.exit(2)}
const excluded=new Set([baselineArg&&path.resolve(baselineArg),writeArg&&path.resolve(writeArg)].filter(Boolean));
const files=[];
async function walk(dir){
 for(const d of (await fs.readdir(dir,{withFileTypes:true})).sort((a,b)=>a.name.localeCompare(b.name))){
  if(d.name==='.git'||d.name==='node_modules')continue;
  const p=path.join(dir,d.name);if(excluded.has(p))continue;
  if(d.isDirectory())await walk(p);
  else if(d.isFile()){
   const rel=path.relative(root,p).split(path.sep).join('/');
   const stat=await fs.stat(p);
   const hash=await new Promise((resolve,reject)=>{
    const h=createHash('sha256'),stream=createReadStream(p);
    stream.on('data',b=>h.update(b));stream.on('error',reject);
    stream.on('end',()=>resolve(h.digest('hex')));
   });
   files.push({path:rel,bytes:stat.size,sha256:hash});
  }
 }
}
await walk(root);
const prior=baselineArg?JSON.parse(await fs.readFile(path.resolve(baselineArg),'utf8')):null;
if(prior&&(!Array.isArray(prior.files)||prior.schemaVersion!==1))throw Error('Invalid manifest');
const old=new Map((prior?.files||[]).map(f=>[f.path,f])),changes=[];
for(const f of files){
 const p=old.get(f.path),state=!p?'new':p.sha256===f.sha256?'unchanged':'changed';
 if(state!=='unchanged')changes.push({path:f.path,state});old.delete(f.path);
}
for(const f of old.values())changes.push({path:f.path,state:'removed'});
const counts={new:0,changed:0,unchanged:files.length,removed:0};
for(const c of changes){counts[c.state]++;if(c.state!=='removed')counts.unchanged--}
if(writeArg){const dst=path.resolve(writeArg);await fs.mkdir(path.dirname(dst),{recursive:true});await fs.writeFile(dst,JSON.stringify({schemaVersion:1,files},null,2)+'\n')}
console.log(JSON.stringify({counts,changedFiles:changes.slice(0,30),additionalChanges:Math.max(0,changes.length-30),manifestWritten:writeArg?path.resolve(writeArg):null},null,2));
