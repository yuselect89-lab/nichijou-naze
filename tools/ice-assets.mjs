import {readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
const url=new URL('../common_assets/nichijou_naze/props/ice_v3/v1.0.0/manifest.json',import.meta.url),m=JSON.parse(readFileSync(url,'utf8'));
const id=process.argv[2];if(!id){console.log(m.assets.map(a=>`${a.asset_id}  ${a.name}`).join('\n'));}else{const a=m.assets.find(a=>a.asset_id===id);if(!a)throw Error('Unknown asset ID: '+id);console.log(JSON.stringify({...a,repositoryRoot:fileURLToPath(new URL('../',import.meta.url))},null,2));}
