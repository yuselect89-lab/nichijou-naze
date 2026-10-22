import {createScienceScene} from './source/science3d.mjs';
import {createAerationScene} from './source/industrial.mjs';
import {createIceScene} from './source/drain3d.mjs';
export const modelIDs=['NNZ_MODEL_ICE_MICRO_01','NNZ_MODEL_FREEZING_CELL_01','NNZ_MODEL_ICECAN_AIR_01','NNZ_MODEL_ICECAN_DRAIN_01'];
export function createReusableScene(canvas,{asset_id,parameters={}}){
 if(!modelIDs.includes(asset_id))throw Error('Unknown model ID');
 const rate=parameters.playbackRate??1,offset=parameters.frameOffset??0;
 if(!Number.isFinite(rate)||rate<.25||rate>2||!Number.isFinite(offset)||offset<0||offset>194)throw Error('Invalid animation parameters');
 const cut=parameters.cut??5;if(![4,5].includes(cut))throw Error('Micro view must be cut4 or5');
 const engine=asset_id==='NNZ_MODEL_ICE_MICRO_01'?createScienceScene(canvas,cut):asset_id==='NNZ_MODEL_FREEZING_CELL_01'?createScienceScene(canvas,7):asset_id==='NNZ_MODEL_ICECAN_AIR_01'?createAerationScene(canvas):createIceScene(canvas);
 const last=asset_id==='NNZ_MODEL_FREEZING_CELL_01'?194:asset_id==='NNZ_MODEL_ICE_MICRO_01'?(cut===4?149:104):164;
 return {draw(frame,mode='all'){if(!Number.isFinite(frame)||!['all','background','model'].includes(mode))throw Error('Invalid draw arguments');const sourceFrame=Math.max(0,Math.min(last,offset+frame*rate));return {...engine.draw(sourceFrame,mode),asset_id,sourceFrame}},dispose(){engine.dispose()}};
}
