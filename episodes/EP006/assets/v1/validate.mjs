import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import assert from 'node:assert/strict';
import {geometry,state,SCIENCE_FRAMES} from './geometry.ts';
const ep=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const area=p=>Math.abs(p.reduce((s,[x,y],i)=>{const [xx,yy]=p[(i+1)%p.length];return s+x*yy-xx*y},0)/2);
const a0=area(geometry(0).inner);let maxStep=0;
for(let f=0;f<SCIENCE_FRAMES;f++){
 const g=geometry(f);assert.deepEqual(g.skinInner,g.tissueBoundary,'Skin / tissue boundaries must coincide at every sample');
 assert(g.vesselWidth>=23&&g.bloodRadius>=6,'Vessels and blood must not vanish');
 assert.equal(g.outer.length,geometry(0).outer.length,'Topology cannot change');
 assert(area(g.inner)/a0>.9,'No exaggerated overall collapse');
 assert(g.outer.every(p=>p.every(Number.isFinite)));
 if(f){const prev=geometry(f-1);g.outer.forEach(([x,y],i)=>{maxStep=Math.max(maxStep,Math.hypot(x-prev.outer[i][0],y-prev.outer[i][1]))});}
}
assert(maxStep<1,'No geometric jump (max point displacement <1px per frame)');
assert.deepEqual(geometry(385),geometry(449),'Final wrinkles held for 65 frames');
assert.equal(state(150).vessel,1);assert.equal(state(150).volume,0);assert.equal(state(270).volume,1);assert.equal(state(270).wrinkle,0);
const result={status:'PASS',frames_checked:SCIENCE_FRAMES,shared_boundary_samples_per_frame:geometry(0).inner.length,max_surface_displacement_px_per_frame:maxStep,final_hold_frames:65,final_tissue_area_ratio:area(geometry(449).inner)/a0,scope:'Geometry invariants only; not medical validation or visual G3',checks:['skin/tissue shared boundary all frames','fixed topology','nonzero vessels','bounded local deformation','continuous frame progression','ordered cause stages','final hold']};
fs.writeFileSync(path.join(ep,'evidence/v1/geometry-qc.json'),JSON.stringify(result,null,2));console.log(result);
