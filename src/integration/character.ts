export const highresPoses=['neutral','talk','point_right','point_left','think'] as const;
export function characterPath(pose:string,version:string='prototype'){
 if(version==='v02_highres'){
  if(!(highresPoses as readonly string[]).includes(pose))throw new Error('This pose has no high-resolution asset yet');
  return `common_assets/nichijou_naze/characters/female_v01/poses/NNZ_CHAR_FEMALE_01_pose_${pose}.png`;
 }
 if(version!=='prototype')throw new Error('Unsupported character version');
 return `common_assets/nichijou_naze/characters/female_v01/poses/${pose}.png`;
}
