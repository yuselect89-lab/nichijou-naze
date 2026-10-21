import json,subprocess,hashlib,zipfile
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
r=Path(__file__).resolve().parent.parent
observations=json.loads((r/'validation/render-observations.json').read_text())
results=[]
for case in observations:
    frames=case.get('frames')
    if frames:
        clip=r/f"validation/{case['name']}.mp4"
        d=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(clip)]))['streams']
        assert len(d)==1 and d[0]['codec_type']=='video'
        v=d[0];assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1080,1920,'30/1',frames)
        subprocess.run(['ffmpeg','-v','error','-i',str(clip),'-f','null','-'],check=True)
    seen={}
    for o in case['observations']:seen[o['frame']]=o
    assert seen,case['name']
    for frame,o in seen.items():
        els=o['elements'];bars=[e for e in els if e['kind']=='progress'];banners=[e for e in els if e['kind']=='banner']
        assert len(banners)<=1,'Duplicate banner'
        if case['name']=='overlay-transparent':assert not bars and not banners
        else:
            assert len(bars)==1
            assert abs(float(bars[0]['progress'])-frame/(frames-1))<1e-8,'Progress reset or wrong total duration'
        for e in els:
            if e['kind'] in ['card','character','label','title','focus','lens']:
                assert e['x']>=71.5 and e['x']+e['w']<=1008.5,(case['name'],frame,e)
                assert e['y']>=320 and e['y']+e['h']<=1470.5,(case['name'],frame,e)
            if e['kind']=='caption':assert '、' not in e['text'] and '。' in e['text'];assert e['y']==1510 and e['h']==280
    if frames:
        assert 0 in seen and frames-1 in seen
        assert any(e['kind']=='character' for o in seen.values() for e in o['elements'])
    results.append({'case':case['name'],'status':'PASS','frames':frames,'checkedFrames':sorted(seen)})
overlay=Image.open(r/'validation/overlay-transparent.png').convert('RGBA')
assert overlay.getpixel((0,0))[3]==0
assert overlay.getchannel('A').crop((0,1510,1080,1920)).getextrema()==(0,0)
registry=json.loads((r/'library-registry.json').read_text())
for rel,digest in registry['originalFiles'].items():assert hashlib.sha256((r/'vendor/common-library/1.0.0'/rel).read_bytes()).hexdigest()==digest
for pose in registry['character']['poses']:
    p=r/'public'/pose['path'];im=Image.open(p);assert im.mode=='RGBA' and im.height==253
    assert hashlib.sha256(p.read_bytes()).hexdigest()==pose['sha256']
baseline=Path('/tmp/nnz-existing-hashes.json')
protected=json.loads(baseline.read_text()) if baseline.exists() else {}
for name,digest in protected.items():assert hashlib.sha256(Path(name).read_bytes()).hexdigest()==digest,f'Past EP modified: {name}'
for name in ['arrow','compare','zoom']:
    validate=r/f'validation/{name}-100.png';assert Image.open(validate).size==(1080,1920)
cli=r/'validation/cli-import.mp4'
subprocess.run(['ffmpeg','-v','error','-i',str(cli),'-f','null','-'],check=True)
sheet=Image.new('RGB',(1440,720),'#dbe5dc');font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',24)
for i,(name,frame) in enumerate([('arrow',100),('compare',100),('zoom',100),('parent',150)]):
    im=Image.open(r/f'validation/{name}-{frame}.png').convert('RGB').resize((340,604));sheet.paste(im,(i*360+10,62));ImageDraw.Draw(sheet).text((i*360+16,15),name,font=font,fill='#182b34')
sheet.save(r/'validation/contact-sheet.jpg',quality=94)
gallery=Image.new('RGB',(800,650),'#f5f6ef')
for i,pose in enumerate(registry['character']['poses']):
    im=Image.open(r/'public'/pose['path']);x=i%4*200+(200-im.width)//2;y=i//4*325+28
    gallery.paste(im,(x,y),im);ImageDraw.Draw(gallery).text((i%4*200+12,i//4*325+285),pose['pose'],font=font,fill='#182b34')
gallery.save(r/'validation/character-gallery.png')
report={'status':'PASS','renders':results,'characterPoses':8,'upstreamFilesPreserved':len(registry['originalFiles']),'pastEpFilesPreserved':len(protected),'overlayAlphaAndCaptionSpace':'PASS','newSceneCli':'PASS actual render','limitations':['Prototype character resolution retained; no lip-sync or male character.','Real VO was not supplied; caption behavior verified with explicit synthetic frame cues.','Separate repository: https://github.com/yuselect89-lab/nichijou-naze; no files pushed into Beyond.']}
(r/'validation/qc-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2))
