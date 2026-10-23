import test from 'node:test';
import assert from 'node:assert/strict';
import {mkdtempSync, readFileSync, rmSync, writeFileSync} from 'node:fs';
import {tmpdir} from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const checker = path.join(root, 'tools', 'visual_pdca_qc.py');
const toolsPresent = ['python3', 'ffmpeg', 'ffprobe'].every(bin => spawnSync(bin, ['-version'], {stdio:'ignore'}).status === 0);

function spawn(command, args) {
  const result = spawnSync(command, args, {encoding:'utf8', timeout:30000});
  assert.notEqual(result.error?.code, 'ETIMEDOUT', command + ' timed out');
  return result;
}
function fixture(where, visual) {
  const mp4 = path.join(where, visual + '.mp4');
  const filter = visual === 'still' ? 'color=c=gray:size=320x480:rate=30:duration=2' : 'testsrc2=size=320x480:rate=30:duration=2';
  const rendered = spawn('ffmpeg', ['-hide_banner','-loglevel','error','-y','-f','lavfi','-i',filter,
    '-f','lavfi','-i','sine=frequency=300:sample_rate=48000:duration=2',
    '-c:v','libx264','-threads','1','-pix_fmt','yuv420p','-c:a','aac','-t','2',mp4]);
  assert.equal(rendered.status, 0, rendered.stderr);
  const cfg = path.join(where, visual + '.json');
  writeFileSync(cfg, JSON.stringify({
    candidate:mp4, width:320, height:480, fps:'30/1', frames:60, duration:2,
    motion_windows:[{name:'planned_explanation',start:0.2,end:1.2,crop:[0,0,160,160],min_motion:2.0}]
  }));
  const report = path.join(where, visual + '-report.json');
  const checked = spawn('python3', [checker,'--config',cfg,'--out',report]);
  return {checked, result:JSON.parse(readFileSync(report,'utf8'))};
}

test('visual PDCA checker: real motion passes the technical motion gate but final status stays HOLD',
  {skip: !toolsPresent && 'Requires Python3, FFmpeg and FFprobe'},
  () => {
    const dir = mkdtempSync(path.join(tmpdir(),'nnz-visual-'));
    try {
      const {checked,result} = fixture(dir,'moving');
      assert.equal(checked.status,0,checked.stderr);
      assert.equal(result.automatic_pass,true);
      assert.equal(result.overall_status,'HOLD');
      assert.equal(result.review_gates.external_g2_g3,'NOT_REVIEWED');
    } finally {rmSync(dir,{recursive:true,force:true});}
  });

test('visual PDCA checker: missing planned motion must FAIL rather than PASS',
  {skip: !toolsPresent && 'Requires Python3, FFmpeg and FFprobe'},
  () => {
    const dir = mkdtempSync(path.join(tmpdir(),'nnz-visual-'));
    try {
      const {checked,result} = fixture(dir,'still');
      assert.equal(checked.status,2,checked.stderr);
      assert.equal(result.automatic_pass,false);
      assert.equal(result.automatic_checks.planned_motion_planned_explanation.status,'FAIL');
      assert.equal(result.overall_status,'HOLD');
    } finally {rmSync(dir,{recursive:true,force:true});}
  });
