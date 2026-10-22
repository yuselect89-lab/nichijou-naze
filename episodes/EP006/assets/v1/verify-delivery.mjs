import fs from 'node:fs';import path from 'node:path';import {createHash} from 'node:crypto';import {fileURLToPath} from 'node:url';import {execFileSync} from 'node:child_process';
const ep=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..'),root=path.resolve(ep,'../..');
const digest=p=>createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const manifest=JSON.parse(fs.readFileSync(path.join(ep,'manifest.json'),'utf8'));
for(const f of manifest.files){const p=path.resolve(root,f.path);if(!p.startsWith(root+path.sep)||digest(p)!==f.sha256)throw Error('Changed/missing delivery file: '+f.path);}
const baseline=JSON.parse(fs.readFileSync(path.join(ep,'evidence/v1/baseline-sha256.json'),'utf8'));
for(const [p,h]of Object.entries(baseline))if(digest(path.join(root,p))!==h)throw Error('Protected pre-existing file changed: '+p);
process.chdir(root);execFileSync('node',['tools/verify-production.mjs'],{stdio:'inherit'});execFileSync('node',['tools/library.mjs','check','episodes/EP006/manifest.json'],{stdio:'pipe'});
console.log(`PASS: ${manifest.files.length} delivered files, ${Object.keys(baseline).length} unchanged pre-existing files, approved banner and shared references`);
