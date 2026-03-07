# 이 파일은 www.edumgt.co.kr 의 에듀엠지티에 저작권이 있습니다
﻿param(
    [Parameter(Mandatory = $true)]
    [int]$Day,

    [ValidateSet("solution", "launcher", "assignment", "basic", "advanced", "challenge")]
    [string]$Target = "solution"
)

$ErrorActionPreference = "Stop"
$RootDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$DayText = "{0:D2}" -f $Day

for ($n = 1; $n -le 500; $n++) {
    $classId = "class{0:D3}" -f $n
    $classDir = Join-Path $RootDir $classId
    $notesFile = Join-Path $classDir "instructor_notes.md"

    if (-not (Test-Path $notesFile)) {
        continue
    }

    $isMatched = Select-String -Path $notesFile -Pattern "Day\s+$DayText\b" -Encoding UTF8 -Quiet
    if (-not $isMatched) {
        continue
    }

    switch ($Target) {
        "solution" { $pyFile = Join-Path $classDir "${classId}_solution.py" }
        "launcher" { $pyFile = Join-Path $classDir "${classId}.py" }
        "assignment" { $pyFile = Join-Path $classDir "${classId}_assignment.py" }
        "basic" { $pyFile = Join-Path $classDir "${classId}_assignment_basic.py" }
        "advanced" { $pyFile = Join-Path $classDir "${classId}_assignment_advanced.py" }
        "challenge" { $pyFile = Join-Path $classDir "${classId}_assignment_challenge.py" }
    }

    if (-not (Test-Path $pyFile)) {
        Write-Host "Skip ${classId}: file not found ($pyFile)"
        continue
    }

    Write-Host "========== $classId ($Target) =========="
    & python $pyFile
    if ($LASTEXITCODE -ne 0) {
        throw "Execution failed: $classId ($Target)"
    }
    Write-Host ""
}
