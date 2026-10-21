export const IDs=['NNZ_TMP_ARROW_01','NNZ_TMP_COMPARE_01','NNZ_TMP_ZOOM_01'];
export const poses=['neutral','talk','point_left','point_right','think','surprise','happy','troubled'];
export function validateConfig(c){
 if(!IDs.includes(c.id))throw new Error('Unknown or unimplemented template ID');
 if(c.revision&&c.revision!=='1.0.1')throw new Error('Unsupported template revision; do not silently use another revision');
 if(!['standalone','overlay'].includes(c.mode??'standalone'))throw new Error('mode must be standalone or overlay');
 if(!(c.durationSeconds>=2&&c.durationSeconds<=20))throw new Error('durationSeconds must be 2..20');
 if(typeof c.title!=='string'||c.title.length>32)throw new Error('title must be at most 32 characters');
 if(c.characterPose&&!poses.includes(c.characterPose))throw new Error('Unknown character pose');
 if(c.characterVersion&&!['prototype','v02_highres'].includes(c.characterVersion))throw new Error('Unknown character version');
 if(c.characterVersion==='v02_highres'&&!['neutral','talk','point_right','point_left','think'].includes(c.characterPose??'neutral'))throw new Error('No high-resolution asset for that pose');
 if(c.id!=='NNZ_TMP_COMPARE_01'&&typeof c.image!=='string')throw new Error('image is required');
 if(c.id==='NNZ_TMP_ARROW_01'){
  if(!Array.isArray(c.arrows)||c.arrows.length<1||c.arrows.length>8)throw new Error('1..8 arrows required');
  for(const a of c.arrows)for(const k of ['x1','x2','y1','y2'])if(!Number.isFinite(a[k]))throw new Error('Arrow coordinates must be finite');
  for(const a of c.arrows)if(Math.min(a.x1,a.x2)<96||Math.max(a.x1,a.x2)>984||Math.min(a.y1,a.y2)<520||Math.max(a.y1,a.y2)>1420)throw new Error('Arrow leaves the diagram safe zone');
 }
 if(c.id==='NNZ_TMP_COMPARE_01')for(const k of ['left','right'])if(!c[k]||['image','label','marker'].some(p=>typeof c[k][p]!=='string'))throw new Error('left/right need image label marker');
 if(c.id==='NNZ_TMP_ZOOM_01'&&(!c.highlight||![c.highlight.x,c.highlight.y].every(n=>Number.isFinite(n)&&n>=0&&n<=1)||!(c.zoom>=1.2&&c.zoom<=5)||typeof c.label!=='string'))throw new Error('Invalid zoom region');
 return c;
}
