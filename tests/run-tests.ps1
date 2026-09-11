# run-tests.ps1 -- regression runner for the coppe class.
#
# Usage:
#   .\run-tests.ps1                         # run every test_*.tex in this folder
#   .\run-tests.ps1 test_brazilian_one_advisor  # run a single test (stem name)
#
# The script sets TEXINPUTS so pdflatex finds coppe.cls (and friends) in
# ..\src, runs pdflatex -> biber -> pdflatex -> pdflatex, and reports a
# pass/fail summary based on pdflatex's exit code. Aux files stay in this
# folder; clean them with `Remove-Item *.aux,*.bbl,*.bcf,*.blg,*.log,*.out,*.run.xml,*.toc,*.lof,*.lot,*.loa,*.loq,*.lol`.

param(
    [string]$Filter = ""
)

$ErrorActionPreference = "Stop"

# Make pdflatex see ../src/. The trailing ; matters on Windows -- it tells
# kpathsea "and then the normal TEXINPUTS path after this".
$here   = Split-Path -Parent $MyInvocation.MyCommand.Path
$srcDir = Resolve-Path (Join-Path $here "..\src")
$env:TEXINPUTS = "$srcDir;$here;$env:TEXINPUTS"
$env:BIBINPUTS = "$srcDir;$here;$env:BIBINPUTS"

if ($Filter) {
    $tests = @(Get-ChildItem -Path $here -Filter "$Filter.tex")
} else {
    $tests = @(Get-ChildItem -Path $here -Filter "test_*.tex")
}

if ($tests.Count -eq 0) {
    Write-Host "No test files matched." -ForegroundColor Yellow
    exit 1
}

$results = @()
foreach ($t in $tests) {
    $stem = [System.IO.Path]::GetFileNameWithoutExtension($t.Name)
    Write-Host ""
    Write-Host "=== $stem ===" -ForegroundColor Cyan

    Push-Location $here
    try {
        $ok = $true
        & pdflatex -interaction=nonstopmode -halt-on-error $t.Name | Out-Null
        if ($LASTEXITCODE -ne 0) { $ok = $false }

        if ($ok) {
            & biber $stem | Out-Null
            if ($LASTEXITCODE -ne 0) { $ok = $false }
        }
        # As listas de abreviaturas e de simbolos so aparecem depois do
        # makeindex com o estilo coppe.ist, entre a primeira passada, que
        # escreve o .abx e o .syx, e a segunda, que os imprime. Sem isto, um
        # teste dessas listas passava com elas VAZIAS.
        $ist = Join-Path $here "..\src\coppe.ist"
        if ($ok -and (Test-Path (Join-Path $here "$stem.abx"))) {
            & makeindex -s $ist -o "$stem.lab" "$stem.abx" | Out-Null
        }
        if ($ok -and (Test-Path (Join-Path $here "$stem.syx"))) {
            & makeindex -s $ist -o "$stem.los" "$stem.syx" | Out-Null
        }
        if ($ok) {
            & pdflatex -interaction=nonstopmode -halt-on-error $t.Name | Out-Null
            if ($LASTEXITCODE -ne 0) { $ok = $false }
        }
        if ($ok) {
            & pdflatex -interaction=nonstopmode -halt-on-error $t.Name | Out-Null
            if ($LASTEXITCODE -ne 0) { $ok = $false }
        }

        if ($ok) {
            Write-Host "PASS $stem" -ForegroundColor Green
            $results += [pscustomobject]@{ Name = $stem; Status = "PASS" }
        } else {
            Write-Host "FAIL $stem (see $stem.log for details)" -ForegroundColor Red
            $results += [pscustomobject]@{ Name = $stem; Status = "FAIL" }
        }
    } finally {
        Pop-Location
    }
}

Write-Host ""
Write-Host "=== Summary ===" -ForegroundColor Cyan
$results | Format-Table -AutoSize

$failed = @($results | Where-Object { $_.Status -eq "FAIL" })
if ($failed.Count -gt 0) { exit 1 } else { exit 0 }
