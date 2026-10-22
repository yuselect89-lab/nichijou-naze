$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$m = Get-Content -Raw -LiteralPath 'parts.json' | ConvertFrom-Json
if (Test-Path -LiteralPath $m.output) { throw 'Output already exists. Move it before restoring.' }
foreach ($p in $m.parts) {
  $h = (Get-FileHash -Algorithm SHA256 -LiteralPath $p.name).Hash.ToLower()
  if ($h -ne $p.sha256) { throw "Damaged part: $($p.name)" }
}
$tmp = "$($m.output).tmp"
$target = [System.IO.File]::Create((Join-Path $PSScriptRoot $tmp))
try { foreach ($p in $m.parts) {
  $inputPart = [System.IO.File]::OpenRead((Join-Path $PSScriptRoot $p.name))
  try { $inputPart.CopyTo($target) } finally { $inputPart.Dispose() }
} } finally { $target.Dispose() }
if ((Get-FileHash -Algorithm SHA256 -LiteralPath $tmp).Hash.ToLower() -ne $m.sha256) { throw 'ZIP integrity check failed' }
Move-Item -LiteralPath $tmp -Destination $m.output
Write-Host "Restored and SHA256 verified: $($m.output)"
