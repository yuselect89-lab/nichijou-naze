"""Append immutable admitted versions to existing ledger; preserve historical rows."""
from pathlib import Path
import json,csv
from openpyxl import load_workbook
R=Path(__file__).resolve().parents[2];M=R/'common_assets/nichijou_naze/management';reg=json.loads((R/'library-registry.json').read_text());rows=json.loads((M/'asset_registry.json').read_text());old=len(rows);keys={(r['Asset ID'],r['Version']) for r in rows}
for path in reg['libraryOperations']['registrations']:
 a=json.loads((R/path).read_text());key=(a['asset_id'],a['version'])
 if key not in keys:rows.append({'Asset ID':a['asset_id'],'種別':a['kind'],'名前・用途':a['name'],'ステータス':'self_qc_render_verified','Version':a['version'],'相対パス':path,'使用回':a['origin_project'],'権利・制作元':a['rights']['basis'],'QC':a['qc']['report'],'備考':'Immutable standalone reusable version. '+a['scope'],'Active':True});keys.add(key)
(M/'asset_registry.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
with (M/'asset_registry.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
wb=load_workbook(M/'asset_registry.xlsx');ws=wb.active
for a in rows[old:]:ws.append([a.get(k) for k in rows[0]])
wb.save(M/'asset_registry.xlsx')
print('Ledger appended',len(rows)-old,'rows')
