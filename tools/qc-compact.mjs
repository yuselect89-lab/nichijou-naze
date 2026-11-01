#!/usr/bin/env node
// Save the ENTIRE QC transcript locally. Give the AI bounded output; never equate exit 0 with QC PASS.
import {spawn} from 'node:child_process';
import {createWriteStream, mkdirSync} from 'node:fs';
import path from 'node:path';
const argv=process.argv.slice(2), marker=argv.indexOf('--');
if(marker<0||marker===argv.length-1){console.error('Usage: node qc-compact.mjs [--out log-file] [--tail 20] -- command [args...]');process.exit(2)}
const opts=argv.slice(0,marker),cmd=argv.slice(marker+1);
let logPath=null,tailCount=20;
for(let i=0;i<opts.length;i++){
 if(opts[i]==='--out'&&opts[i+1])logPath=opts[++i];
 else if(opts[i]==='--tail'&&opts[i+1])tailCount=Number(opts[++i]);
 else{console.error('Unknown option '+opts[i]);process.exit(2)}
}
if(!Number.isInteger(tailCount)||tailCount<1||tailCount>100)process.exit(2);
if(!logPath)logPath=`out/qc/${path.basename(cmd[0]).replace(/[^\w.-]/g,'_')}-${Date.now()}-${process.pid}.log`;
mkdirSync(path.dirname(path.resolve(logPath)),{recursive:true});
const stream=createWriteStream(logPath,{flags:'wx'}),child=spawn(cmd[0],cmd.slice(1),{stdio:['inherit','pipe','pipe'],shell:false});
let lines=0,tail=[],issues=[],issueCount=0,bytes=0;
const buffers={stdout:'',stderr:''};
const important=/(?:\b(?:ERROR|WARN|FAIL|BLOCK|HOLD|MISSING|PASS)\b|警告|未確認|不一致|エラー|失敗|異常|不足|指摘|要修正|要判断|★)/i;
function line(s){
 lines++;
 if(important.test(s)){issueCount++;if(issues.length<50)issues.push(s.slice(0,450))}
 tail.push(s.slice(0,450));if(tail.length>tailCount)tail.shift();
}
for(const pipe of [child.stdout,child.stderr]){
 pipe.on('data',b=>{
  bytes+=b.length;stream.write(b);
  const key=pipe===child.stdout?'stdout':'stderr';buffers[key]+=b.toString('utf8');let idx;
  while((idx=buffers[key].indexOf('\n'))>=0){line(buffers[key].slice(0,idx).replace(/\r$/,''));buffers[key]=buffers[key].slice(idx+1)}
  if(buffers[key].length>65536){line(buffers[key].slice(0,500));buffers[key]=''}
 });
}
child.on('error',e=>{stream.write('\n[SPAWN ERROR] '+e.message+'\n');console.error('Cannot execute command: '+e.message);process.exitCode=127});
child.on('close',async(code,signal)=>{
 for(const v of Object.values(buffers))if(v)line(v);
 stream.end();await new Promise(resolve=>stream.once('finish',resolve));
 const result={status:code===0?'EXECUTED_ZERO_EXIT_NOT_QC_PASS':'COMMAND_FAILED',exitCode:code,signal,log:path.resolve(logPath),bytes,lines,matchingLines:issueCount,interesting:issues.slice(0,25),additionalInteresting:Math.max(0,issueCount-25),tail};
 console.log(JSON.stringify(result,null,2));
 if(code!==0)process.exitCode=code||1;
});
