$ErrorActionPreference = 'Stop'

$candidates = @()
if ($env:PET_HARU_PYTHON) { $candidates += $env:PET_HARU_PYTHON }
$candidates += @('python', 'py')
$python = $null
foreach ($candidate in $candidates) {
    try {
        & $candidate -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)' 2>$null
        if ($LASTEXITCODE -eq 0) { $python = $candidate; break }
    }
    catch { }
}
if (-not $python) { throw 'Python 3.10+ was not found. Set PET_HARU_PYTHON to its executable path.' }

& $python (Join-Path $PSScriptRoot 'generate_previews.py')

