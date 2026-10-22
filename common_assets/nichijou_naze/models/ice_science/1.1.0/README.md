# 氷の科学モデル 1.1.0

EP004から独立した共有モデル。元のEP004と旧1.0.0登録は維持します。このフォルダだけで3DコードとThree.js依存が完結します。

```js
import {createReusableScene} from './index.mjs';
const scene = createReusableScene(canvas, {
  asset_id: 'NNZ_MODEL_ICE_MICRO_01',
  parameters: {cut: 5, playbackRate: 1.2, frameOffset: 0}
});
scene.draw(frame, 'all'); // 'background' / 'model' also supported
// canvasの親レイヤーでtranslate / scaleを適用
scene.dispose();
```

4つのID・パラメータ・出自・権利はmanifestに記録。manifestのcandidate表示は候補提出時の原文で、正式な利用状態と検品根拠はmanagement/operations/v1/registrations内の同ID同版レコードを参照してください。`resolve`が現在のファイル・版・QCを確認します。

科学形状は元と同じ。泡、光路、凍結速度等は模式。寸法や科学内容を変える場合は新しい版とQCが必要です。写真風の工場背景や小道具は含みません。字幕・帯・進行バーも含みません。Three.jsのMITライセンスはvendor/three/LICENSE.txt。
