import {readFileSync,existsSync} from 'node:fs';
import {createHash} from 'node:crypto';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
export const APPROVED_PATH='public/series/approved/opening_banner.png';
const PNG_SIG=Buffer.from([137,80,78,71,13,10,26,10]);
export function verifyProduction({root=process.cwd(),lockFile='production-lock.json'}={}) {
 const lockPath=path.resolve(root,lockFile);
 if(!existsSync(lockPath)) throw new Error('PRODUCTION BLOCKED: production-lock.json がありません');
 const lock=JSON.parse(readFileSync(lockPath,'utf8'));
 if(lock.schemaVersion!==1||lock.project!=='nichijou-naze') throw new Error('PRODUCTION BLOCKED: 制作仕様の版またはプロジェクトが不正です');
 const b=lock.banner;
 if(!b || b.path!==APPROVED_PATH) throw new Error('PRODUCTION BLOCKED: 正式帯の固定パスが変更されています');
 if(b.status!=='APPROVED') throw new Error('PRODUCTION BLOCKED: 正式帯の元画像が未確認です。勝手に作成・代用しないでください');
 if(typeof b.sha256!=='string'||!/^[a-f0-9]{64}$/.test(b.sha256)) throw new Error('PRODUCTION BLOCKED: 承認済み帯のSHA256が未登録です');
 if(b.sha256===b.legacyNotApproved?.sha256) throw new Error('PRODUCTION BLOCKED: 旧版の帯は承認済みに変更できません');
 const resolved=path.resolve(root,b.path);
 if(!resolved.startsWith(path.resolve(root)+path.sep)) throw new Error('PRODUCTION BLOCKED: パスが制作環境外です');
 if(!existsSync(resolved)) throw new Error('PRODUCTION BLOCKED: 正式帯のPNGが存在しません');
 const bytes=readFileSync(resolved);
 if(bytes.length<PNG_SIG.length||!bytes.subarray(0,8).equals(PNG_SIG)) throw new Error('PRODUCTION BLOCKED: 正式帯はPNGではありません');
 const actual=createHash('sha256').update(bytes).digest('hex');
 if(actual!==b.sha256) throw new Error('PRODUCTION BLOCKED: 正式帯のSHA256が一致しません（別画像への差し替え）');
 return {assetId:b.assetId,path:b.path,sha256:actual};
}
if(process.argv[1] && path.resolve(process.argv[1])===fileURLToPath(import.meta.url)) {
 try { const result=verifyProduction(); console.log('PRODUCTION PREFLIGHT PASS: '+JSON.stringify(result)); }
 catch(err) { console.error(String(err.message||err)); process.exitCode=1; }
}
