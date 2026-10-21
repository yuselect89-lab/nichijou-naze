"""Original dummy media for layout QC. Not a product photograph or scientific source."""
from pathlib import Path
import shutil
R=Path(__file__).resolve().parents[2]
D=R/'common_assets/nichijou_naze/layouts/v1.1.0/test_media';D.mkdir(parents=True,exist_ok=True)
defs='''<defs><linearGradient id="ice" x2="1" y2="1"><stop stop-color="#ffffff" stop-opacity=".96"/><stop offset=".35" stop-color="#c6eaf3" stop-opacity=".72"/><stop offset=".7" stop-color="#f2fcff" stop-opacity=".93"/><stop offset="1" stop-color="#88bdce" stop-opacity=".78"/></linearGradient><radialGradient id="cloud"><stop stop-color="white" stop-opacity=".95"/><stop offset=".65" stop-color="white" stop-opacity=".65"/><stop offset="1" stop-color="white" stop-opacity="0"/></radialGradient></defs>'''
exterior='''<path d="M45 62Q225 20 412 62L439 421Q235 493 24 436Z" fill="url(#ice)" stroke="#edfaff" stroke-width="8"/><path d="M45 62L92 119L390 113L412 62M92 119L70 414M390 113L411 400" fill="none" stroke="white" stroke-opacity=".8" stroke-width="9"/><ellipse cx="233" cy="264" rx="114" ry="139" fill="url(#cloud)"/><path d="M81 149L75 258M115 82L221 67M391 164L405 271" fill="none" stroke="white" stroke-width="12" stroke-linecap="round"/>'''
def svg(body,w=460,h=500):return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{defs}{body}</svg>'
(D/'ice-outside.svg').write_text(svg(exterior))
shell='''<path d="M45 62Q225 20 412 62L439 421Q235 493 24 436Z" fill="#b9e8f5" stroke="#238da9" stroke-width="7"/><path d="M70 86Q230 55 389 86L413 404Q231 461 51 416Z" fill="#edfbff" stroke="#75bdce" stroke-width="4"/><path d="M49 62L70 86M412 62L389 86M439 421L413 404M24 436L51 416" stroke="#238da9" stroke-width="5"/>'''
(D/'ice-shell.svg').write_text(svg(shell))
import math
bubbles=''.join(f'<circle cx="{230+math.cos(i*2.4)*(18+(i%7)*12):.2f}" cy="{260+math.sin(i*2.4)*(25+(i%6)*15):.2f}" r="{3+i%4}" fill="white" stroke="#4f9fb4" stroke-width="1.5"/>' for i in range(75))
(D/'ice-bubbles.svg').write_text(svg(bubbles))
(D/'ice-liquid.svg').write_text(svg('<ellipse cx="230" cy="263" rx="104" ry="135" fill="#76cedf" opacity=".5" stroke="#17899d" stroke-width="3"/>'))
scene=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">{defs}<defs><linearGradient id="wall" x2="0" y2="1"><stop stop-color="#c1d6d8"/><stop offset="1" stop-color="#f2eee3"/></linearGradient><linearGradient id="table" x2=".3" y2="1"><stop stop-color="#d9d9d2"/><stop offset="1" stop-color="#a4b8b5"/></linearGradient><filter id="blur"><feGaussianBlur stdDeviation="20"/></filter><radialGradient id="shade"><stop stop-color="#39859c" stop-opacity=".3"/><stop offset="1" stop-color="#39859c" stop-opacity="0"/></radialGradient></defs><rect width="1080" height="1920" fill="url(#wall)"/><g filter="url(#blur)" opacity=".7"><rect x="30" y="110" width="180" height="780" fill="#fff"/><rect x="250" y="110" width="130" height="780" fill="#e6f6ff"/><rect x="820" y="600" width="240" height="280" rx="35" fill="#a3b6a1"/><circle cx="930" cy="580" r="90" fill="#8fb2a1"/></g><path d="M0 1020L1080 970V1920H0Z" fill="url(#table)"/><path d="M0 1110L1080 1060M0 1400L1080 1360M280 1020L180 1920M790 990L960 1920" stroke="white" stroke-opacity=".15" stroke-width="3"/><ellipse cx="540" cy="1000" rx="380" ry="90" fill="url(#shade)"/><svg x="310" y="500" width="460" height="500" viewBox="0 0 460 500">{exterior}</svg><g fill="white" opacity=".4"><ellipse cx="420" cy="1040" rx="20" ry="7"/><ellipse cx="760" cy="1008" rx="31" ry="9"/></g></svg>'''
(D/'kitchen-ice-dummy.svg').write_text(scene)
diagram='''<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920"><defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#f4fcff"/><stop offset="1" stop-color="#c8e8ed"/></linearGradient><pattern id="grid" width="60" height="60" patternUnits="userSpaceOnUse"><path d="M60 0H0V60" fill="none" stroke="#388fa1" stroke-opacity=".08" stroke-width="2"/></pattern></defs><rect width="1080" height="1920" fill="url(#bg)"/><rect width="1080" height="1920" fill="url(#grid)"/><path d="M-100 600Q500 100 1200 540M-150 1740Q600 1180 1200 1500" stroke="white" stroke-width="110" opacity=".3" fill="none"/></svg>'''
(D/'diagram-canvas.svg').write_text(diagram)
# Alternate reusable geometry verifies crosssection is not ice-specific.
carton='<path d="M110 100L230 40L350 100V440H110Z" fill="#fff0c9" stroke="#a97835" stroke-width="8"/><path d="M110 100H350M230 40V100" stroke="#a97835" stroke-width="8"/>'
(D/'carton-outside.svg').write_text(svg(carton))
(D/'carton-shell.svg').write_text(svg('<path d="M110 100L230 40L350 100V440H110Z" fill="#fff8e2" stroke="#a97835" stroke-width="8"/><path d="M130 140H330V420H130Z" fill="#def5f6" stroke="#568f98" stroke-width="5"/>'))
(D/'carton-inner.svg').write_text(svg('<path d="M137 265Q230 240 323 265V413H137Z" fill="#ffca62" opacity=".8"/>'))
P=R/'public'/D.relative_to(R);P.mkdir(parents=True,exist_ok=True)
for f in D.glob('*.svg'):shutil.copy2(f,P/f.name)
print('Wrote',len(list(D.glob('*.svg'))),'original dummy SVGs')
