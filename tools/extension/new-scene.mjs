import {readFileSync,writeFileSync,mkdirSync,existsSync} from 'node:fs';
import {dirname,resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {validateScene} from '../../common_assets/nichijou_naze/runtime/v1.1.0/config.ts';
const root=resolve(dirname(fileURLToPath(import.meta.url)),'../..');
export function createScene(templateID,overrides={}){
 const registry=JSON.parse(readFileSync(root+'/common_assets/nichijou_naze/runtime/v1.1.0/manifest.json','utf8'));
 const entry=registry.assets.find(a=>a.asset_id===templateID);
 if(!entry)throw Error('Unknown or unregistered template ID');
 const example=JSON.parse(readFileSync(root+'/'+entry.example,'utf8'));
 return validateScene({...example,...overrides,revision:'1.1.0'});
}
if(process.argv[1]&&resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const [id,output,overrideFile]=process.argv.slice(2);
 if(!id||!output)throw Error('Usage: node tools/extension/new-scene.mjs <templateID> <output.json> [overrides.json]');
 if(existsSync(output))throw Error('Refusing to overwrite existing scene: '+output);
 const overrides=overrideFile?JSON.parse(readFileSync(overrideFile,'utf8')):{};
 const scene=createScene(id,overrides);mkdirSync(dirname(output),{recursive:true});
 writeFileSync(output,JSON.stringify(scene,null,2)+'\n',{flag:'wx'});console.log('Created '+output);
}
