@echo off
cd /d "%~dp0"
if exist "EP005_materials_v2.zip" (echo ZIP already exists. Move it before restoring. & pause & exit /b 1)
copy /b "EP005_materials_v2.zip.part01"+"EP005_materials_v2.zip.part02"+"EP005_materials_v2.zip.part03"+"EP005_materials_v2.zip.part04"+"EP005_materials_v2.zip.part05"+"EP005_materials_v2.zip.part06"+"EP005_materials_v2.zip.part07" "EP005_materials_v2.zip" >nul
if errorlevel 1 (echo Restore failed. & pause & exit /b 1)
powershell -NoProfile -Command "$m=Get-Content -Raw parts.json | ConvertFrom-Json; if ((Get-FileHash -Algorithm SHA256 -LiteralPath $m.output).Hash.ToLower() -ne $m.sha256) { Write-Error 'ZIP integrity check failed'; exit 1 }; Write-Host 'Restored and SHA256 verified: EP005_materials_v2.zip'"
pause
