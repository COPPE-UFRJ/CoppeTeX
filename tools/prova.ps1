<#
.SYNOPSIS
    Prova de funcionamento do CoppeTeX. Tem de sair limpa antes de marcar uma
    versao.

.DESCRIPTION
    Atalho para build-check.ps1 -Scope prova, que e onde a prova mora de fato.
    Ela cobre as tres coisas que podem estar erradas sem ninguem notar:

    1. FONTE UNICA. Regera tudo a partir de coppe.dtx + coppe.ins e confere,
       pelo git, se algum arquivo distribuido mudou. Se mudou, alguem editou um
       derivado a mao e a edicao acabou de ser perdida.

    2. O QUE E DISTRIBUIDO COMPILA. A classe, os cinco exemplos por idioma, a
       versao PDF/A do exemplo, a montagem das capas e os manuais.

    3. O QUE PROVA QUE FUNCIONA. A suite de regressao em tests\ e os doze
       documentos adversativos em adversativa\ -- quatro tipos de trabalho por
       tres idiomas, cada um acionando ao mesmo tempo tudo o que a classe
       oferece --, compilados nos DOIS motores, pdfLaTeX e LuaLaTeX, e todos os
       PDF/A passados pelo veraPDF.

    Nem tests\ nem adversativa\ sao distribuidos, e nenhum dos dois sai do
    coppe.dtx: provam que a classe funciona, nao fazem parte dela.

    O veredito fica no fim de _scratch\RESULTADO.txt; o codigo de saida e o
    numero de falhas.

.EXAMPLE
    .\tools\prova.ps1
#>
$check = Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Path) "build-check.ps1"
& powershell -NoProfile -File $check -Scope prova
exit $LASTEXITCODE
