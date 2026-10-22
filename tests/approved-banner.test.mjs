import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {verifyProduction} from '../tools/verify-production.mjs';
const lock=JSON.parse(readFileSync('production-lock.json','utf8'));
test('user-supplied approved banner hash matches original bytes',()=>{
 const file=readFileSync(lock.banner.path);
 assert.equal(createHash('sha256').update(file).digest('hex'),'e6b63c322c996f543930a027db8981c2388e88441656655822c34bb4e2e2fd37');
 assert.equal(verifyProduction().sha256,lock.banner.sha256);
 assert.equal(lock.banner.dimensions.width,2000);assert.equal(lock.banner.dimensions.height,2000);
});
test('production series uses approved source at natural aspect ratio',()=>{
 const s=readFileSync('src/integration/v1.0.1/Series.tsx','utf8');
 assert.match(s,/series\/approved\/opening_banner\.png/);
 assert.doesNotMatch(s,/series\/v1\/opening_banner\.png/);
 assert.match(s,/width:920,height:920,objectFit:'contain'/);
});
