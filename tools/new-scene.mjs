import {readFileSync,writeFileSync,mkdirSync,existsSync,copyFileSync,constants} from 'node:fs';
import path from 'node:path';
import {validateConfig,IDs} from './config.mjs';
const args=process.argv.slice(2),get=k=>args[args.indexOf(k)+1];
const id=get('--template'),out=get('--out');if(!IDs.includes(id)||!args.includes('--out'))throw new Error('Usage: node tools/new-scene.mjs --template ID --out episodes/EP005/cut01.json [--image path] [--left path --right path] [--pose think]');
if(existsSync(out))throw new Error('Scene exists; choose a new version filename');
if(!path.resolve(out).startsWith(path.resolve('episodes')+path.sep))throw new Error('Scene output must stay in this project episodes/ directory');
const names=['arrow','compare','zoom'],base=JSON.parse(readFileSync(`examples/${names[IDs.indexOf(id)]}.json`,'utf8'));
const ep=path.basename(path.dirname(out));
function importImage(src){if(!src||!existsSync(src))throw new Error('Replacement image not found');const rel=`episodes/${ep}/assets/${path.basename(src)}`,dest=path.join('public',rel);mkdirSync(path.dirname(dest),{recursive:true});copyFileSync(src,dest,constants.COPYFILE_EXCL);return rel;}
if(args.includes('--image'))base.image=importImage(get('--image'));
if(args.includes('--left'))base.left.image=importImage(get('--left'));
if(args.includes('--right'))base.right.image=importImage(get('--right'));
if(args.includes('--pose')){delete base.characterImage;base.characterPose=get('--pose');}
base.revision='1.0.1';validateConfig(base);mkdirSync(path.dirname(out),{recursive:true});writeFileSync(out,JSON.stringify(base,null,2),{flag:'wx'});console.log(out);
