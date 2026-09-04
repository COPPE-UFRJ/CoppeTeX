<#
.SYNOPSIS
    Fica observando _scratch\BUILD_REQUEST e roda build-check.ps1 quando ele
    aparece. Deixe rodando numa janela do PowerShell enquanto trabalhamos.

.DESCRIPTION
    O Claude edita os arquivos por um ambiente que não tem TeX completo. Com
    este observador ligado, ele cria um arquivo _scratch\BUILD_REQUEST, este
    script compila no seu TeX do Windows e escreve _scratch\RESULTADO.txt --
    que ele consegue ler. Assim a verificação de cada passo acontece sem você
    precisar rodar nada a cada vez.

    Pare com Ctrl+C a qualquer momento. Nada aqui altera arquivo versionado.

.EXAMPLE
    .\tools\watch-build.ps1
#>
param([int]$IntervalSeconds = 3)

$root    = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$scratch = Join-Path $root "_scratch"
$request = Join-Path $scratch "BUILD_REQUEST"
$done    = Join-Path $scratch "BUILD_DONE"
$check   = Join-Path $root "tools\build-check.ps1"

New-Item -ItemType Directory -Force -Path $scratch | Out-Null

Write-Host "Observando $request" -ForegroundColor Cyan
Write-Host "Ctrl+C para parar." -ForegroundColor DarkGray

while ($true) {
    if (Test-Path $request) {
        $scope = (Get-Content $request -Raw -ErrorAction SilentlyContinue).Trim()
        if ([string]::IsNullOrWhiteSpace($scope)) { $scope = "all" }
        Remove-Item $request -Force -ErrorAction SilentlyContinue
        Remove-Item $done    -Force -ErrorAction SilentlyContinue

        Write-Host ""
        Write-Host "--> build ($scope) $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor Yellow
        & powershell -NoProfile -File $check -Scope $scope
        $code = $LASTEXITCODE

        "concluido=$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') escopo=$scope falhas=$code" |
            Out-File -FilePath $done -Encoding utf8
        Write-Host "--> pronto (falhas=$code)" -ForegroundColor Yellow
    }
    Start-Sleep -Seconds $IntervalSeconds
}
