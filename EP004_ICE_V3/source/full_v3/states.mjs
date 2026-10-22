import {smooth} from '../physics.mjs';
export function freezingState(frame){const q=smooth((frame-12)/165);return {progress:q,halfX:1.48-1.12*q,halfY:1.45-1.10*q,halfZ:.98-.64*q,gasMarkerOpacity:1-smooth((q-.68)/.24),bubbleOpacity:smooth((q-.67)/.27),liquidOpacity:1-smooth((q-.82)/.18)};}
export function aerationState(frame){const q=smooth((frame-35)/105);return {freezeProgress:q,innerHalf:1.26-.64*q,bottom:.63+.395*q,liquidHeight:3.775-.395*q,airActive:frame>=38&&frame<141,withdraw:smooth((frame-141)/23),liquidRemoved:0};}
export function degasState(frame){const q=smooth((frame-5)/60);return {fraction:q,retained:6,escaping:8,fullyDepleted:false};}
export const durationFrames={2:195,3:120,4:150,5:105,6:75,7:195,8:165,10:123};
