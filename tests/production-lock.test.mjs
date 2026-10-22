import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync,mkdirSync,writeFileSync,rmSync,readFileSync} from 'node:fs';
import {tmpdir} from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createHash} from 'node:crypto';
import {verifyProduction,APPROVED_PATH} from '../tools/verify-production.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const base=JSON.parse(readFileSync(path.join(root,'production-lock.json'),'utf8'));
const samplePNG=Buffer.from('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQIHWP4z8DwHwAFgAI/ScL/nwAAAABJRU5ErkJggg==','base64');
function fixture(fn){const dir=mkdtempSync(path.join(tmpdir(),'nnz-brand-'));try{mkdirSync(path.join(dir,'public/series/approved'),{recursive:true});writeFileSync(path.join(dir,APPROVED_PATH),samplePNG);const lock=structuredClone(base);lock.banner.status='APPROVED';lock.banner.sha256=createHash('sha256').update(samplePNG).digest('hex');writeFileSync(path.join(dir,'production-lock.json'),JSON.stringify(lock));fn(dir,lock);}finally{rmSync(dir,{recursive:true,force:true});}}
test('unapproved repository fails closed',()=>assert.throws(()=>verifyProduction({root}),/PRODUCTION BLOCKED/));
test('approved original passes, but changed bytes fail',()=>fixture(dir=>{assert.equal(verifyProduction({root:dir}).path,APPROVED_PATH);writeFileSync(path.join(dir,APPROVED_PATH),Buffer.concat([samplePNG,Buffer.from([0])]));assert.throws(()=>verifyProduction({root:dir}),/SHA256/);}));
test('the known wrong asset hash is rejected',()=>fixture((dir,lock)=>{lock.banner.sha256=lock.banner.legacyNotApproved.sha256;writeFileSync(path.join(dir,'production-lock.json'),JSON.stringify(lock));assert.throws(()=>verifyProduction({root:dir}),/旧版/);}));
test('missing authorization fails closed',()=>fixture((dir,lock)=>{lock.banner.status='BLOCKED_SOURCE_NOT_VERIFIED';writeFileSync(path.join(dir,'production-lock.json'),JSON.stringify(lock));assert.throws(()=>verifyProduction({root:dir}),/未確認/);}));
