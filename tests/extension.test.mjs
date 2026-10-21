import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {validateScene,characterFile,motionAt,poseWeights,focusAt} from '../common_assets/nichijou_naze/runtime/v1.1.0/config.ts';
import {createScene} from '../tools/extension/new-scene.mjs';
const dir='common_assets/nichijou_naze/layouts/v1.1.0/examples/';
const load=id=>JSON.parse(readFileSync(dir+id+'.json','utf8'));
test('all registered examples validate and local media really exists',()=>{
 const scenes=JSON.parse(readFileSync(dir+'playlist.json','utf8')).map(load);
 const media=s=>{assert.ok(existsSync('public/'+s),'Missing '+s)};
 for(const c of scenes){validateScene(c);media(c.background.src);if(c.crossSection){media(c.crossSection.outside);c.crossSection.parts.forEach(p=>media(p.image));}c.character?.poses.forEach(p=>media(characterFile(p.pose)));}
 assert.equal(scenes.length,13);
});
test('new expression paths never substitute old prototype or rewrite V02',()=>{
 for(const p of ['surprise','happy','troubled'])assert.match(characterFile(p),/versions\/v03_expressions\/poses/);
 for(const p of ['neutral','talk','point_left','point_right','think'])assert.match(characterFile(p),/female_v01\/poses\/NNZ_CHAR/);
 assert.throws(()=>characterFile('walk'));
});
test('protected subjects and captions are enforced on changed parameters',()=>{
 const c=load('footage-character');c.protectedSubjects.push({x:90,y:1100,width:240,height:360});assert.throws(()=>validateScene(c),/covers protected/);
 const b=load('footage-character');b.labels[0].box.x=850;assert.throws(()=>validateScene(b),/safe zone|rectangle/);
 const d=load('footage-character');d.character.top=1470;assert.throws(()=>validateScene(d),/safe zone/);
});
test('step and pose sequencing reject backward or too-fast cues',()=>{
 const c=load('step3-cause');c.steps[2].fromFrame=30;assert.throws(()=>validateScene(c),/ordered/);
 const d=load('motions');d.character.poses[2].fromFrame=67;assert.throws(()=>validateScene(d),/spacing/);
});
test('whole-sprite motion remains continuous with finite opacity, no scale deformation',()=>{
 const c=load('motions'),a=c.character;
 let previous=motionAt(a,0,c.durationFrames);
 for(let f=0;f<c.durationFrames;f++){
  const m=motionAt(a,f,c.durationFrames);assert.ok(m.opacity>=0&&m.opacity<=1);assert.ok(Math.abs(m.y-previous.y)<1.6);assert.ok(Math.abs(m.rotation)<=1.4);assert.equal(m.scale,undefined);
  const weights=poseWeights(a,f);assert.ok(Math.abs(weights.reduce((n,x)=>n+x.opacity,0)-1)<1e-9);previous=m;
 }
 assert.equal(motionAt(a,0,c.durationFrames).opacity,0);assert.ok(motionAt(a,239,c.durationFrames).opacity<.02);
});
test('focus holds the target through reveal and returns to original framing',()=>{
 const c=load('focus-crosssection-return').focus;
 assert.equal(focusAt(c,0).zoom,1);assert.equal(focusAt(c,60).zoom,1.5);assert.equal(focusAt(c,110).reveal,1);
 assert.equal(focusAt(c,230).zoom,1);assert.equal(focusAt(c,230).reveal,0);
 const bad=load('focus-crosssection-return');bad.focus.returnFromFrame=90;assert.throws(()=>validateScene(bad),/Return too early/);
});
test('parts and labels cannot end before they start; legacy overlay cannot duplicate mascot',()=>{
 const c=load('crosssection-carton');c.crossSection.parts[1].toFrame=5;assert.throws(()=>validateScene(c),/Part end/);
 const d=load('legacy-arrow');d.character=load('motions').character;assert.throws(()=>validateScene(d),/own mascot/);
});
test('template ID plus overrides creates a reusable scene without changing the source',()=>{
 const original=load('label-parameters');
 const c=createScene('NNZ_TMP_LABEL_01',{id:'EP005-cut01',labels:[{id:'a',text:'対象',anchor:{x:540,y:700},box:{x:90,y:400,width:240,height:100},fromFrame:12}]});
 assert.equal(c.id,'EP005-cut01');assert.equal(c.labels.length,1);assert.equal(c.labels[0].fromFrame,12);assert.deepEqual(load('label-parameters'),original);
 assert.throws(()=>createScene('NNZ_TMP_UNMADE_99'));
});
