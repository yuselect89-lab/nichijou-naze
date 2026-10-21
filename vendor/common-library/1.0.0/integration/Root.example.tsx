/** Example: import the 3 templates into your existing Remotion Root. */
import React from 'react';
import {Composition} from 'remotion';
import {ArrowTemplate} from './common_assets/nichijou_naze/diagram_templates/arrow_01/template';
import {CompareTemplate} from './common_assets/nichijou_naze/diagram_templates/compare_01/template';
import {ZoomTemplate} from './common_assets/nichijou_naze/diagram_templates/zoom_01/template';
const P='common_assets/nichijou_naze/';
export const NNZTemplates:React.FC=()=> <>
  <Composition id="NNZ_TMP_ARROW_01" component={ArrowTemplate} width={1080} height={1920} fps={30} durationInFrames={150} defaultProps={{title:'内部からの圧力',durationSeconds:5,image:P+'props/pet_bottle/bottle_diagram.svg',characterImage:P+'characters/female_v01/poses/point_left.png',arrows:[{x1:530,y1:925,x2:360,y2:875,label:'押す'},{x1:530,y1:1000,x2:742,y2:960,label:'圧力'}]}} />
  <Composition id="NNZ_TMP_COMPARE_01" component={CompareTemplate} width={1080} height={1920} fps={30} durationInFrames={180} defaultProps={{title:'切欠きはどっち？',durationSeconds:6,left:{image:P+'props/milk_carton/carton_notch.svg',label:'切欠きあり',marker:'○'},right:{image:P+'props/milk_carton/carton_plain.svg',label:'切欠きなし',marker:'×'},characterImage:P+'characters/female_v01/poses/point_right.png'}} />
  <Composition id="NNZ_TMP_ZOOM_01" component={ZoomTemplate} width={1080} height={1920} fps={30} durationInFrames={150} defaultProps={{title:'ここに注目！',durationSeconds:5,image:P+'props/milk_carton/carton_notch.svg',highlight:{x:.30,y:.18},zoom:2.6,label:'上端の切欠き',characterImage:P+'characters/female_v01/poses/point_right.png'}} />
</>;
