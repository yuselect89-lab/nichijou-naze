"""Recheck actual media and source layouts; fail on first unsuccessful command."""
from pathlib import Path
import subprocess,sys
B=Path(__file__).resolve().parents[1]
for f in ['validate_delivery.py','check_alpha.py','check_presenter_integrity.py','check_photo_collisions.py','check_all_frame_safety.py']:
 subprocess.run([sys.executable,str(B/'source'/f)],cwd=B,check=True)
print('DELIVERY_CHECKS_PASS; external visual review and audio correction are separate, not implied.')
