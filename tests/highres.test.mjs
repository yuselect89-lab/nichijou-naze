import test from 'node:test';
import assert from 'node:assert/strict';
import {characterPath} from '../src/integration/character.ts';
import {validateConfig} from '../tools/config.mjs';
import {readFileSync} from 'node:fs';
test('legacy character selection retains exact prototype paths',()=>{assert.equal(characterPath('neutral'),'common_assets/nichijou_naze/characters/female_v01/poses/neutral.png')});
test('v02 resolves the five named production files without silently using prototype',()=>{for(const p of ['neutral','talk','point_right','point_left','think'])assert.match(characterPath(p,'v02_highres'),new RegExp(`NNZ_CHAR_FEMALE_01_pose_${p}\\.png$`));assert.throws(()=>characterPath('surprise','v02_highres'))});
test('template validator rejects missing highres poses and unknown versions',()=>{const c=JSON.parse(readFileSync('examples/arrow.json'));assert.throws(()=>validateConfig({...c,characterVersion:'v02_highres',characterPose:'surprise'}));assert.throws(()=>validateConfig({...c,characterVersion:'v99'}));validateConfig({...c,characterVersion:'v02_highres',characterPose:'think'})});
