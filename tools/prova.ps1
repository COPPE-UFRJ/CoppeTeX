<#
.SYNOPSIS
    Prova de funcionamento do CoppeTeX. Rode antes de marcar uma versao.

.DESCRIPTION
    Uma versao so sai depois que este comando termina limpo. Ele nao e um
    atalho para o build-check: e a definicao do que "funciona" significa nesta
    classe, e cobre as tres coisas que podem estar erradas sem ninguem notar.

    1. FONTE UNICA. Regera tudo a partir de coppe.dtx + coppe.ins e depois
       confere, pelo git, se algum arquivo distribuido mudou. Se mudou, alguem
       editou um derivado a mao e a edicao acabou de ser perdida -- que e
       exatamente o que se quer descobrir antes de publicar, e nao depois.

    2. O QUE E DISTRIBUIDO COMPILA. A classe, os cinco exemplos por idioma, a
       versao PDF/A do exemplo, a montagem das capas e os manuais.

    3. O QUE PROVA QUE FUNCIONA. A suite de regressao em tests/ e os doze
       documentos adversativos em adversativa/ -- quatro tipos de trabalho por
       tres idiomas, cada um acionando ao mesmo tempo tudo o que a classe
       oferece --, compilados nos DOIS motores, pdfLaTeX e LuaLaTeX, e todos os
       PDF/A passados pelo veraPDF.

    Nem tests/ nem adversativa/ sao distribuidos, e nenhum dos dois sai do
    coppe.dtx: provam que a classe funciona, nao fazem parte dela.

.PARAMETER SemGit
    Pula a verificacao de fonte unica (item 1). Util quando se esta no meio de
    uma edicao do .dtx e so se quer saber se compila.

.EXAMPLE
    .\tools\prova.ps1
#>
param([switch]$SemGit)

$ErrorActionPreference = "Continue"
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$check = Join-Path $root "tools\build-check.ps1"

function Titulo($t) {
    Write-Host ""
    Write-Host ("=" * 72) -ForegroundColor Cyan
    Write-Host "  $t" -ForegroundColor Cyan
    Write-Host ("=" * 72) -ForegroundColor Cyan
}

$problemas = @()

Titulo "1. Fonte unica: tudo sai de coppe.dtx + coppe.ins"
if ($SemGit) {
    Write-Host "pulado (-SemGit)" -ForegroundColor DarkGray
} elseif (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "git nao encontrado; verificacao de fonte unica pulada" -ForegroundColor Yellow
} else {
    Push-Location $root
    $antes = & git status --porcelain -- src 2>$null
    & powershell -NoProfile -File $check -Scope class | Out-Null
    $depois = & git status --porcelain -- src 2>$null
    Pop-Location
    $novos = @($depois | Where-Object { $antes -notcontains $_ })
    if ($novos.Count -gt 0) {
        Write-Host "Regerar a partir do .dtx MUDOU arquivos que estavam limpos:" -ForegroundColor Red
        $novos | ForEach-Object { Write-Host "   $_" -ForegroundColor Red }
        Write-Host "Alguem editou um arquivo derivado a mao. A edicao acabou de ser perdida." -ForegroundColor Red
        $problemas += "fonte unica"
    } else {
        Write-Host "ok -- nenhum derivado divergia do .dtx" -ForegroundColor Green
    }
}

Titulo "2 e 3. Compila, passa nos testes, passa no veraPDF"
& powershell -NoProfile -File $check -Scope all
$falhas = $LASTEXITCODE
if ($falhas -ne 0) { $problemas += "$falhas passo(s) de build" }

Titulo "Veredito"
$res = Join-Path $root "_scratch\RESULTADO.txt"
if (Test-Path $res) {
    $txt = Get-Content $res
    $conf = @($txt | Select-String "PDF/A-2b CONFORME").Count
    $nao  = @($txt | Select-String "isCompliant=false").Count
    $passos = ($txt | Select-String "=== \d+ passos") -replace '.*=== ', '' -replace ' ===.*', ''
    Write-Host "  passos de build .......... $passos"
    Write-Host "  PDFs conformes com PDF/A . $conf"
    if ($nao -gt 0) { Write-Host "  PDFs NAO conformes ....... $nao" -ForegroundColor Red; $problemas += "$nao PDF/A nao conforme" }
    if (@($txt | Select-String "pulado   veraPDF").Count -gt 0) {
        Write-Host "  veraPDF .................. NAO RODOU (nao instalado)" -ForegroundColor Yellow
        $problemas += "veraPDF nao rodou"
    }
    if (@($txt | Select-String "pulado   adversativa/lualatex").Count -gt 0) {
        Write-Host "  LuaLaTeX ................. NAO RODOU (nao instalado)" -ForegroundColor Yellow
        $problemas += "LuaLaTeX nao rodou"
    }
}
Write-Host ""
if ($problemas.Count -eq 0) {
    Write-Host "  PROVA COMPLETA. Pode marcar a versao." -ForegroundColor Green
    exit 0
} else {
    Write-Host "  NAO PASSOU: $($problemas -join '; ')" -ForegroundColor Red
    Write-Host "  Detalhes em _scratch\RESULTADO.txt e _scratch\build-logs\." -ForegroundColor Red
    exit 1
}
