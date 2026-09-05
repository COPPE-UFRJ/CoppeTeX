<#
.SYNOPSIS
    Verificação de build da CoppeTeX. Regenera a classe, compila os exemplos
    e roda a suíte de testes, deixando todos os logs em _scratch/build-logs/.

.DESCRIPTION
    Existe porque o ambiente onde o Claude edita os arquivos não tem um TeX
    completo: ele enxerga a pasta do repositório, mas não o TeX Live/MiKTeX do
    Windows. Este script roda no Windows, no TeX de verdade, e escreve um
    resultado em texto que pode ser lido de volta do lado de lá.

    Não altera nada versionado: toda a saída vai para _scratch/, que é ignorado
    pelo git.

.PARAMETER Scope
    class    - só regenera coppe.cls e companhia a partir de coppe.ins (rápido)
    example  - class + example.tex
    langs    - class + os cinco example_<lang>.tex
    tests    - class + a suíte tests/run-tests.ps1
    docs     - class + coppe.pdf (manual), NORMA_COPPE_2026.pdf,
               futuremanual2026.pdf e covers_5languages.pdf
    all      - tudo acima. Padrão.

.EXAMPLE
    .\tools\build-check.ps1
    .\tools\build-check.ps1 -Scope example
#>
param(
    [ValidateSet("class", "example", "langs", "tests", "docs", "all")]
    [string]$Scope = "all"
)

$ErrorActionPreference = "Continue"

$root    = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$src     = Join-Path $root "src"
$testDir = Join-Path $root "tests"
$logDir  = Join-Path $root "_scratch\build-logs"
$result  = Join-Path $root "_scratch\RESULTADO.txt"

New-Item -ItemType Directory -Force -Path $logDir | Out-Null

$env:TEXINPUTS = "$src;$testDir;$env:TEXINPUTS"
$env:BIBINPUTS = "$src;$testDir;$env:BIBINPUTS"

$lines  = @()
$failed = 0
$ran    = 0

function Add-Line([string]$s) { $script:lines += $s; Write-Host $s }

function Invoke-Step {
    param([string]$Name, [string]$Dir, [scriptblock]$Body)
    $script:ran++
    Push-Location $Dir
    try {
        $out = & $Body 2>&1
        $code = $LASTEXITCODE
        $out | Out-File -FilePath (Join-Path $logDir "$Name.log") -Encoding utf8
        if ($code -ne 0) {
            $script:failed++
            Add-Line "FALHOU   $Name  (exit $code)"
            # as três primeiras linhas de erro do TeX ajudam a diagnosticar daqui
            $errs = $out | Select-String -Pattern '^!' | Select-Object -First 3
            foreach ($e in $errs) { Add-Line "         $($e.Line)" }
        } else {
            Add-Line "ok       $Name"
        }
    } finally { Pop-Location }
}

function Build-Tex {
    param([string]$Stem, [string]$Dir, [switch]$WithBiber)
    Invoke-Step "$Stem-1" $Dir { & pdflatex -interaction=nonstopmode -halt-on-error "$Stem.tex" }
    if ($WithBiber) { Invoke-Step "$Stem-biber" $Dir { & biber $Stem } }
    Invoke-Step "$Stem-2" $Dir { & pdflatex -interaction=nonstopmode -halt-on-error "$Stem.tex" }
    Invoke-Step "$Stem-3" $Dir { & pdflatex -interaction=nonstopmode -halt-on-error "$Stem.tex" }
}

Add-Line "=== build-check  escopo=$Scope  $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ==="
Add-Line "pdflatex: $((Get-Command pdflatex -ErrorAction SilentlyContinue).Source)"
Add-Line "biber:    $((Get-Command biber -ErrorAction SilentlyContinue).Source)"
Add-Line ""

# 1. Regenerar a classe a partir do .dtx -- sempre, porque tudo depende disso.
Invoke-Step "coppe.ins" $src { & pdflatex -interaction=nonstopmode coppe.ins }

if ($Scope -in @("example", "all")) { Build-Tex -Stem "example" -Dir $src -WithBiber }

if ($Scope -in @("langs", "all")) {
    foreach ($l in @("pt", "en", "es", "fr", "it")) {
        Build-Tex -Stem "example_$l" -Dir $src -WithBiber
    }
}

if ($Scope -in @("docs", "all")) {
    # O manual sai do .dtx, nao de um .tex: o proprio coppe.dtx traz a secao
    # driver. Precisa de makeindex para o indice remissivo e para o glossario
    # de comandos, e de tres passadas para as referencias cruzadas.
    Invoke-Step "coppe-1" $src { & pdflatex -interaction=nonstopmode coppe.dtx }
    Invoke-Step "coppe-idx" $src { & makeindex -s gind.ist -o coppe.ind coppe.idx }
    Invoke-Step "coppe-glo" $src { & makeindex -s gglo.ist -o coppe.gls coppe.glo }
    Invoke-Step "coppe-2" $src { & pdflatex -interaction=nonstopmode coppe.dtx }
    Invoke-Step "coppe-3" $src { & pdflatex -interaction=nonstopmode coppe.dtx }

    Build-Tex -Stem "futuremanual2026"     -Dir $src -WithBiber
    Build-Tex -Stem "NORMA_COPPE_2026"     -Dir $src

    # covers_5languages monta uma montagem das cinco capas a partir de PNGs
    # extraidos dos example_<lang>.pdf. Sem pdftoppm (poppler) nao ha como
    # gerar os PNGs, e o passo e pulado em vez de falhar.
    if (Get-Command pdftoppm -ErrorAction SilentlyContinue) {
        Push-Location $src
        foreach ($l in @("pt", "en", "es", "fr", "it")) {
            # -singlefile da o nome exato "cover_<l>.png". Sem ele o pdftoppm
            # acrescenta o numero da pagina com tantos digitos quantos tiver a
            # ultima pagina pedida, e o nome varia entre versoes.
            & pdftoppm -png -r 150 -f 1 -l 1 -singlefile "example_$l.pdf" "cover_$l" 2>&1 | Out-Null
        }
        Pop-Location
        Build-Tex -Stem "covers_5languages" -Dir $src
    } else {
        Add-Line "pulado   covers_5languages (pdftoppm nao encontrado)"
    }
}

if ($Scope -in @("tests", "all")) {
    Invoke-Step "suite" $testDir { & powershell -NoProfile -File (Join-Path $testDir "run-tests.ps1") }
}

Add-Line ""
Add-Line "=== $ran passos, $failed falha(s) ==="

# Tamanho dos PDFs gerados, para detectar página a mais/a menos sem abrir o PDF.
Add-Line ""
Add-Line "--- PDFs ---"
Get-ChildItem -Path $src -Filter *.pdf -ErrorAction SilentlyContinue |
    Sort-Object Name |
    ForEach-Object { Add-Line ("{0,-34} {1,9} bytes  {2}" -f $_.Name, $_.Length, $_.LastWriteTime.ToString("HH:mm:ss")) }

$lines | Out-File -FilePath $result -Encoding utf8
Write-Host ""
Write-Host "Resultado em _scratch\RESULTADO.txt e logs em _scratch\build-logs\"
exit $failed
