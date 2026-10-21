import test from 'node:test';
import assert from 'node:assert/strict';
import {drainageState,parameters as p} from './physics.mjs';
test('intake completes before pumping starts; no gas is injected in this shot',()=>{
 assert.equal(drainageState(0).insert,0);assert.equal(drainageState(27).insert,1);assert.equal(drainageState(27).removedVolume,0);
 assert.equal(drainageState(30).flowing,false);assert.equal(drainageState(45).flowing,true);
});
test('every frame loses core liquid continuously and gains exactly that amount in receiver',()=>{
 let last=drainageState(0);const initial=last.sourceVolume;
 for(let f=0;f<165;f++){
  const s=drainageState(f);assert.ok(s.coreHeight<=last.coreHeight+1e-12);assert.ok(s.receiverHeight>=last.receiverHeight-1e-12);
  assert.ok(last.coreHeight-s.coreHeight<.045,'No sudden disappearance');
  assert.ok(Math.abs(s.sourceVolume+s.receiverVolume-initial)<1e-10,'Prescribed volume balance');
  assert.ok(s.receiverHeight<1.40,'No overflow in receiver geometry');last=s;
 }
});
test('end retains hollow solid shell and a small physically reachable liquid residual',()=>{
 const end=drainageState(164);assert.equal(end.drainFraction,1);assert.ok(Math.abs(end.coreHeight-p.residualHeight)<1e-10);assert.ok(end.receiverVolume>4.4);assert.equal(end.flowing,false);
 assert.ok(end.surfaceHeight>1.045,'Suction mouth reaches the residual level');
});
