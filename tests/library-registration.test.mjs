import test from 'node:test';import assert from 'node:assert/strict';import fs from 'node:fs';import os from 'node:os';import path from 'node:path';import {sha,registrationRecords} from '../tools/library/core.mjs';
test('promotion binds exact files and QC, then rejects duplicates and stale bytes',()=>{const root=fs.mkdtempSync(path.join(os.tmpdir(),'nnz-promote-'));try{
 const files={'a.mjs':'export const value=1;','p.png':'preview fixture','license.txt':'Original content'};for(const [p,s]of Object.entries(files))fs.writeFileSync(path.join(root,p),s);
 const a={asset_id:'NNZ_NEW_01',version:'1.0.0',name:'New reusable asset',kind:'model',entrypoint:'a.mjs',files:['a.mjs'],preview:'p.png',origin_project:'TEST',parameter_schema:{},dependencies:[],tags:['test'],rights:{license_files:['license.txt']}};
 const q={result:'PASS',checks:[{name:'actual render',status:'PASS'}],verified_assets:['NNZ_NEW_01@1.0.0'],file_hashes:Object.fromEntries(Object.entries(files).map(([p,s])=>[p,sha(s)]))};fs.writeFileSync(path.join(root,'qc.json'),JSON.stringify(q));
 const [record]=registrationRecords({assets:[a]},'qc.json',{assets:[]},root);assert.equal(record.production_ready,true);assert.equal(record.file_hashes['license.txt'],sha(files['license.txt']));assert.throws(()=>registrationRecords({assets:[a]},'qc.json',{assets:[record]},root),/immutable/);
 fs.writeFileSync(path.join(root,'a.mjs'),'changed');assert.throws(()=>registrationRecords({assets:[a]},'qc.json',{assets:[]},root),/stale/);
 }finally{fs.rmSync(root,{recursive:true})}});
