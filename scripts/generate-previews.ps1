$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$python = 'C:\Users\USERWCARLOS01\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
$petTools = 'C:\Users\USERWCARLOS01\.codex\plugins\cache\openai-curated-remote\work-pets\0.1.6\skills\create-pet\scripts'
$atlas = Join-Path $root 'assets\sprites\haru-urara-spritesheet.png'
$frames = Join-Path $root 'assets\frames'
$previews = Join-Path $root 'previews'

New-Item -ItemType Directory -Force -Path $previews | Out-Null
& $python (Join-Path $PSScriptRoot 'extract-atlas-frames.py')
& $python (Join-Path $petTools 'make_contact_sheet.py') $atlas --output (Join-Path $previews 'contact-sheet.png')
& $python (Join-Path $petTools 'make_direction_qa_sheet.py') $atlas --output (Join-Path $previews 'look-directions.png')
& $python (Join-Path $petTools 'render_animation_previews.py') --frames-root $frames --output-dir (Join-Path $previews 'animations')

Write-Host "Previews generated in $previews"

