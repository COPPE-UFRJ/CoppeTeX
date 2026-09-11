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
               manual.pdf e covers_5languages.pdf
    pdfa     - class + example_pdfa.tex, tests/test_pdfa.tex e
               tests/test_comserifa.tex, e passa os tres
               pelo veraPDF no perfil 2b. Precisa do veraPDF instalado (o
               script procura em %USERPROFILE%\verapdf e no PATH); sem ele o
               passo é PULADO, não falha.
    adversativa - os 12 documentos de adversativa/ (4 tipos x 3 idiomas),
               com o ciclo completo: biber, makeindex das listas e do indice
               remissivo, tres passadas, e veraPDF em cada um.
    all      - tudo acima. Padrão.
    prova    - `all' mais a verificacao de fonte unica (nenhum arquivo derivado
               divergiu do .dtx) e um veredito final. E o que tem de sair limpo
               antes de marcar uma versao; tools\prova.ps1 e so um atalho.

.EXAMPLE
    .\tools\build-check.ps1
    .\tools\build-check.ps1 -Scope example
#>
param(
    [ValidateSet("class", "example", "langs", "tests", "docs", "pdfa", "adversativa", "all", "prova")]
    [string]$Scope = "all"
)

$ErrorActionPreference = "Continue"

# `prova' e `all' mais duas coisas: a verificacao de fonte unica, antes, e o
# veredito, depois. O corpo do script e o mesmo.
$prova = ($Scope -eq "prova")
if ($prova) { $Scope = "all" }

$root    = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$src     = Join-Path $root "src"
# tests/ e adversativa/ ficam FORA de src/: nao sao distribuidos e nao saem do
# coppe.dtx. Provam que a classe funciona; nao fazem parte dela.
$testDir = Join-Path $root "tests"
$advDir  = Join-Path $root "adversativa"
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

# As listas de abreviaturas e de simbolos NAO saem de uma passada do pdflatex:
# a primeira passada escreve .abx e .syx, o makeindex os ordena com o estilo
# coppe.ist em .lab e .los, e so a passada seguinte os imprime. Sem esse passo
# as listas saem do que estivesse em disco -- ou seja, do build anterior, ou de
# uma versao da classe que ja mudou. Era o caso do example.pdf ate aqui: o
# escopo `adversativa' rodava o makeindex e os demais nao, e a lista de
# abreviaturas do exemplo, que e o documento que todo mundo abre, vinha de um
# .lab velho.
function Build-Tex {
    param([string]$Stem, [string]$Dir, [switch]$WithBiber)
    Invoke-Step "$Stem-1" $Dir { & pdflatex -interaction=nonstopmode -halt-on-error "$Stem.tex" }
    if ($WithBiber) { Invoke-Step "$Stem-biber" $Dir { & biber $Stem } }
    if (Test-Path (Join-Path $Dir "$Stem.abx")) {
        Invoke-Step "$Stem-lab" $Dir { & makeindex -s (Join-Path $script:src "coppe.ist") -o "$Stem.lab" "$Stem.abx" }
    }
    if (Test-Path (Join-Path $Dir "$Stem.syx")) {
        Invoke-Step "$Stem-los" $Dir { & makeindex -s (Join-Path $script:src "coppe.ist") -o "$Stem.los" "$Stem.syx" }
    }
    Invoke-Step "$Stem-2" $Dir { & pdflatex -interaction=nonstopmode -halt-on-error "$Stem.tex" }

    # Tres passadas bastam para referencia cruzada, e NAO bastam quando o
    # documento traz \nocite{*}: a lista de citacoes so fica completa depois da
    # segunda passada, e o biblatex pede o biber de novo. Sem isso o documento
    # sai com "There were undefined references" e ninguem ve, porque o pdflatex
    # devolve zero assim mesmo.
    #
    # Em vez de fixar um numero de passadas, pergunta-se ao .log: enquanto ele
    # pedir, roda mais um ciclo, ate tres vezes. Se depois disso ainda pedir, e
    # defeito do documento e o passo falha.
    # O .log as vezes guarda MAIS DE UMA passada, uma atras da outra. Ler o
    # arquivo inteiro faz um aviso da primeira passada -- que a segunda ja
    # resolveu -- parecer um problema atual. So a ultima passada conta, e ela
    # comeca no ultimo banner do LaTeX.
    function Ultima-Passada([string]$caminho) {
        if (-not (Test-Path $caminho)) { return "" }
        $t = Get-Content $caminho -Raw -ErrorAction SilentlyContinue
        if (-not $t) { return "" }
        $i = $t.LastIndexOf("LaTeX2e <")
        if ($i -gt 0) { return $t.Substring($i) }
        return $t
    }

    $log = Join-Path $Dir "$Stem.log"
    for ($i = 1; $i -le 3; $i++) {
        if (-not (Test-Path $log)) { break }
        $txt = Ultima-Passada $log
        $pedeBiber = $txt -match 'Please \(re\)run Biber'
        $pedeLatex = $txt -match 'Rerun to get|There were undefined references'
        if (-not ($pedeBiber -or $pedeLatex)) { break }
        if ($WithBiber -and $pedeBiber) {
            Invoke-Step "$Stem-biber$($i+1)" $Dir { & biber $Stem }
        }
        Invoke-Step "$Stem-$($i+2)" $Dir { & pdflatex -interaction=nonstopmode -halt-on-error "$Stem.tex" }
    }
    Invoke-Step "$Stem-final" $Dir { & pdflatex -interaction=nonstopmode -halt-on-error "$Stem.tex" }

    # Veredito de referencia. Exige PROVA, e nao o resumo generico: o aviso
    # "There were undefined references" e disparado pelo biblatex nos documentos
    # em espanhol mesmo com tudo resolvido, porque o pacote de idioma registra o
    # mapeamento em \AtBeginDocument e o contador de refsection so fecha na
    # passada seguinte. Falhar por causa dele reprovaria documento correto.
    #
    # Prova e uma referencia ou citacao NOMEADA como indefinida -- que e o que
    # produz o "??" na pagina.
    $txt = Ultima-Passada $log
    $m = [regex]::Matches($txt, "(?m)^.*(Reference|Citation) ``[^']+' on page .* undefined.*$")
    if ($m.Count -gt 0) {
        $script:failed++
        Add-Line "FALHOU   $Stem-referencias  ($($m.Count) referencia(s) sem resolver)"
        foreach ($x in ($m | Select-Object -First 3)) { Add-Line "         $($x.Value.Trim())" }
    }
}

# Le so a ULTIMA passada de um .log: o arquivo as vezes guarda mais de uma, e um
# aviso da primeira, que a segunda ja resolveu, nao e problema atual.
function Get-UltimaPassada([string]$caminho) {
    if (-not (Test-Path $caminho)) { return "" }
    $t = Get-Content $caminho -Raw -ErrorAction SilentlyContinue
    if (-not $t) { return "" }
    $i = $t.LastIndexOf("LaTeX2e <")
    if ($i -gt 0) { return $t.Substring($i) }
    return $t
}

# Roda mais passadas enquanto o documento pedir, e cobra se ele continuar
# pedindo. Serve aos documentos adversativos, que nao usam Build-Tex.
function Estabilizar {
    param([string]$Stem, [string]$Dir, [string]$Motor, [string]$Fonte, [string]$JobName)
    $log = Join-Path $Dir "$Stem.log"
    for ($i = 1; $i -le 3; $i++) {
        $txt = Get-UltimaPassada $log
        $pedeBiber = $txt -match 'Please \(re\)run Biber'
        $pedeLatex = $txt -match 'Rerun to get|There were undefined references|Please rerun LaTeX'
        if (-not ($pedeBiber -or $pedeLatex)) { break }
        if ($pedeBiber) { Invoke-Step "$Stem-biber$($i+1)" $Dir { & biber $Stem } }
        if ($JobName) {
            Invoke-Step "$Stem-r$i" $Dir { & $Motor -interaction=nonstopmode -halt-on-error -jobname $JobName $Fonte }
        } else {
            Invoke-Step "$Stem-r$i" $Dir { & $Motor -interaction=nonstopmode -halt-on-error $Fonte }
        }
    }
    # Mesma regra do Build-Tex: so falha com prova -- uma referencia ou citacao
    # nomeada como indefinida. Ver o comentario la.
    $txt = Get-UltimaPassada $log
    $m = [regex]::Matches($txt, "(?m)^.*(Reference|Citation) ``[^']+' on page .* undefined.*$")
    if ($m.Count -gt 0) {
        $script:failed++
        Add-Line "FALHOU   $Stem-referencias  ($($m.Count) referencia(s) sem resolver)"
        foreach ($x in ($m | Select-Object -First 3)) { Add-Line "         $($x.Value.Trim())" }
    }
}

Add-Line ("=== build-check  escopo=" + $(if ($prova) { "prova" } else { $Scope }) + "  $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ===")
$provaProblemas = @()

# Fonte unica: regerar a partir do .dtx nao pode mudar nada que estivesse
# limpo. Se mudou, alguem editou um derivado a mao e a edicao acaba de ser
# perdida -- que e o que se quer descobrir antes de publicar, e nao depois.
if ($prova) {
    if (Get-Command git -ErrorAction SilentlyContinue) {
        Push-Location $root
        $gitAntes = @(& git status --porcelain -- src 2>$null)
        Pop-Location
        Push-Location $src
        & pdflatex -interaction=nonstopmode coppe.ins 2>&1 | Out-Null
        Pop-Location
        Push-Location $root
        $gitDepois = @(& git status --porcelain -- src 2>$null)
        Pop-Location
        $novos = @($gitDepois | Where-Object { $gitAntes -notcontains $_ })
        if ($novos.Count -gt 0) {
            Add-Line "FALHOU   fonte unica: regerar do .dtx mudou arquivo que estava limpo"
            foreach ($n in $novos) { Add-Line "         $n" }
            $script:failed++
            $provaProblemas += "fonte unica"
        } else {
            Add-Line "ok       fonte unica (nenhum derivado divergia do .dtx)"
        }
    } else {
        Add-Line "pulado   fonte unica (git nao encontrado)"
        $provaProblemas += "fonte unica nao verificada"
    }
}
Add-Line ""
Add-Line "pdflatex: $((Get-Command pdflatex -ErrorAction SilentlyContinue).Source)"
Add-Line "biber:    $((Get-Command biber -ErrorAction SilentlyContinue).Source)"
Add-Line ""

# 1. Regenerar TUDO a partir do .dtx -- sempre, porque tudo depende disso.
# O coppe.ins gera a classe, os estilos biblatex, os pacotes de idioma, as
# bases .bib, os exemplos nos cinco idiomas, o example_pdfa, a montagem das
# capas, a suite de testes e o latexmkrc.
Invoke-Step "coppe.ins" $src { & pdflatex -interaction=nonstopmode coppe.ins }

# O latexmkrc sai do docstrip como latexmkrc.tex: o \openout do TeX acrescenta
# .tex a todo nome sem extensao, e nao ha como pedir a ele o nome exato. Poe no
# lugar aqui, para que a geracao continue sendo um comando so para quem usa o
# harness.
$mkrcGen = Join-Path $src "latexmkrc.tex"
if (Test-Path $mkrcGen) {
    Copy-Item $mkrcGen (Join-Path $src "latexmkrc") -Force
    Add-Line "ok       latexmkrc (de latexmkrc.tex)"
}

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

    # O manual envelhece em silencio: um comando novo entra na classe e ninguem o
    # documenta, e nada quebra. Este passo cobra isso, e tambem confere se a
    # tabela "onde ver cada coisa" ainda aponta para as linhas certas do
    # example.tex. Sem python instalado o passo e PULADO, nao falha.
    if (Get-Command python -ErrorAction SilentlyContinue) {
        Invoke-Step "conferir-manual" $root { & python (Join-Path $root "tools\conferir-manual.py") }
    } else {
        Add-Line "pulado   conferir-manual (python nao encontrado)"
    }

    # A referencia rapida em ingles. Duas passadas, e nao uma: e uma longtable,
    # que so acerta a largura das colunas depois de se ver por inteiro.
    Invoke-Step "quickref-1" $src { & pdflatex -interaction=nonstopmode -halt-on-error coppe-quickref.tex }
    Invoke-Step "quickref-2" $src { & pdflatex -interaction=nonstopmode -halt-on-error coppe-quickref.tex }

    Build-Tex -Stem "manual"     -Dir $src -WithBiber
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

if ($Scope -in @("adversativa", "all")) {
    # Revisao adversativa: 4 tipos de documento x 3 idiomas, cada um acionando
    # o maximo possivel da API ao mesmo tempo. Ciclo COMPLETO -- e o unico lugar
    # do harness onde o makeindex das listas de abreviaturas e de simbolos e do
    # indice remissivo tambem roda, que e o que essas listas exigem de verdade.
    $env:TEXINPUTS = "$src;$advDir;$env:TEXINPUTS"
    $advDocs = Get-ChildItem -Path $advDir -Filter "adv_*.tex" -ErrorAction SilentlyContinue |
        Sort-Object Name | ForEach-Object { [System.IO.Path]::GetFileNameWithoutExtension($_.Name) }
    if (-not $advDocs) { Add-Line "pulado   adversativa (nenhum adv_*.tex)" }

    # Sonda de fluxos: compila SEM morewrites so para registrar quantos \write
    # cada parte consome. Estoura de proposito e NAO entra na contagem de
    # falhas -- o valor dela e o log, nao o PDF.
    $probe = Join-Path $advDir "_writes_probe.tex"
    if (Test-Path $probe) {
        Push-Location $advDir
        $out = & pdflatex -interaction=nonstopmode "_writes_probe.tex" 2>&1
        Pop-Location
        $out | Out-File -FilePath (Join-Path $logDir "_writes_probe.log") -Encoding utf8
        Add-Line ""
        Add-Line "--- fluxos de escrita consumidos (sem morewrites) ---"
        foreach ($l in ($out | Select-String -Pattern '@@FLUXO')) {
            Add-Line ("         " + ($l.Line -replace '^.*@@FLUXO ', ''))
        }
        Add-Line ""
    }
    foreach ($stem in $advDocs) {
        Invoke-Step "$stem-1"    $advDir { & pdflatex -interaction=nonstopmode -halt-on-error "$stem.tex" }
        Invoke-Step "$stem-biber" $advDir { & biber $stem }
        # as listas de abreviaturas e de simbolos passam pelo makeindex com o
        # estilo coppe.ist; o indice remissivo, pelo makeindex padrao
        Invoke-Step "$stem-lab" $advDir { & makeindex -s (Join-Path $src "coppe.ist") -o "$stem.lab" "$stem.abx" }
        Invoke-Step "$stem-los" $advDir { & makeindex -s (Join-Path $src "coppe.ist") -o "$stem.los" "$stem.syx" }
        Invoke-Step "$stem-idx" $advDir { & makeindex "$stem.idx" }
        Invoke-Step "$stem-2"    $advDir { & pdflatex -interaction=nonstopmode -halt-on-error "$stem.tex" }
        Invoke-Step "$stem-3"    $advDir { & pdflatex -interaction=nonstopmode -halt-on-error "$stem.tex" }
        Estabilizar -Stem $stem -Dir $advDir -Motor "pdflatex" -Fonte "$stem.tex"
    }

    # Segunda passada, com LuaLaTeX. E a outra saida documentada para o teto de
    # 16 fluxos, e vale saber que a classe inteira compila nos dois motores --
    # nao so que compila num deles. -jobname mantem os dois PDFs lado a lado,
    # para que o veraPDF possa julgar os dois.
    if (Get-Command lualatex -ErrorAction SilentlyContinue) {
        foreach ($stem in $advDocs) {
            $lj = "${stem}_lua"
            Invoke-Step "$lj-1"     $advDir { & lualatex -interaction=nonstopmode -halt-on-error -jobname $lj "$stem.tex" }
            Invoke-Step "$lj-biber" $advDir { & biber $lj }
            Invoke-Step "$lj-lab"   $advDir { & makeindex -s (Join-Path $src "coppe.ist") -o "$lj.lab" "$lj.abx" }
            Invoke-Step "$lj-los"   $advDir { & makeindex -s (Join-Path $src "coppe.ist") -o "$lj.los" "$lj.syx" }
            Invoke-Step "$lj-idx"   $advDir { & makeindex "$lj.idx" }
            Invoke-Step "$lj-2"     $advDir { & lualatex -interaction=nonstopmode -halt-on-error -jobname $lj "$stem.tex" }
            Invoke-Step "$lj-3"     $advDir { & lualatex -interaction=nonstopmode -halt-on-error -jobname $lj "$stem.tex" }
            Estabilizar -Stem $lj -Dir $advDir -Motor "lualatex" -Fonte "$stem.tex" -JobName $lj
        }
    } else {
        Add-Line "pulado   adversativa/lualatex (lualatex nao encontrado)"
    }
}

if ($Scope -in @("pdfa", "all")) {
    # Os dois documentos que saem com a opcao de classe pdfa: o exemplo inteiro
    # (bibliografia, listas, figuras, tcolorbox -- transparencia) e o teste
    # curto das paginas pre-textuais. Validar so o curto nao diria nada sobre o
    # que vai para o deposito.
    Build-Tex -Stem "example_pdfa" -Dir $src     -WithBiber
    Build-Tex -Stem "test_pdfa"    -Dir $testDir -WithBiber
    # A opcao `comserifa' volta o documento para a familia serifada. A pergunta que
    # interessa nao e se compila -- e se o documento com serifa continua sendo
    # PDF/A, que e o que a 2.2(d) exige do deposito. Sem fonte vetorial nao ha
    # PDF/A, e era assim que a classe inteira saia antes do lmodern: em Type 3.
    Build-Tex -Stem "test_comserifa" -Dir $testDir -WithBiber

    # O veraPDF nao esta no PATH depois da instalacao padrao no Windows; o
    # instalador deixa o .bat na raiz da pasta escolhida. Procura-se ali antes
    # de recorrer ao PATH.
    $veraCandidates = @(
        (Join-Path $env:USERPROFILE "verapdf\verapdf.bat"),
        (Join-Path $env:USERPROFILE "verapdf\bin\verapdf.bat"),
        "C:\Program Files\verapdf\verapdf.bat"
    )
    $vera = $veraCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
    if (-not $vera) {
        $cmd = Get-Command verapdf -ErrorAction SilentlyContinue
        if ($cmd) { $vera = $cmd.Source }
    }

    if (-not $vera) {
        Add-Line "pulado   veraPDF (nao encontrado em %USERPROFILE%\verapdf nem no PATH)"
    } else {
        Add-Line ""
        Add-Line "veraPDF: $vera"
        $veraTargets = @(
            @{ Stem = "example_pdfa";   Dir = $src },
            @{ Stem = "test_pdfa";      Dir = $testDir },
            @{ Stem = "test_comserifa"; Dir = $testDir })
        # todo documento adversativo e compilado com a opcao pdfa: se algum
        # deles ja foi gerado, valida-se tambem
        $advDirV = Join-Path $root "adversativa"
        if (Test-Path $advDirV) {
            foreach ($f in (Get-ChildItem -Path $advDirV -Filter "adv_*.pdf" -ErrorAction SilentlyContinue | Sort-Object Name)) {
                $veraTargets += @{ Stem = [System.IO.Path]::GetFileNameWithoutExtension($f.Name); Dir = $advDirV }
            }
        }
        foreach ($t in $veraTargets) {
            $pdf = Join-Path $t.Dir "$($t.Stem).pdf"
            $rep = Join-Path $logDir "verapdf-$($t.Stem).xml"
            if (-not (Test-Path $pdf)) { Add-Line "FALHOU   verapdf:$($t.Stem)  (PDF nao foi gerado)"; $script:failed++; continue }
            $script:ran++
            # --format xml da o machine-readable report, que e o unico que traz
            # a clausula e o numero do teste de cada regra reprovada.
            # stderr NAO pode ir para o mesmo arquivo: o veraPDF escreve log do
            # Java em stderr, e misturado ao stdout ele corrompe o XML.
            $err = Join-Path $logDir "verapdf-$($t.Stem).err"
            & $vera --flavour 2b --format xml $pdf 2> $err | Out-File -FilePath $rep -Encoding utf8
            $code = $LASTEXITCODE

            # Resumo legivel dentro do RESULTADO.txt: sem isto o relatorio so
            # existe como XML de varios MB, que nao se le daqui.
            $compliant = $null
            $failures  = @()
            try {
                $raw = Get-Content $rep -Raw
                $i = $raw.IndexOf("<?xml")
                if ($i -gt 0) { $raw = $raw.Substring($i) }
                [xml]$x = $raw
                $vr = $x.SelectSingleNode("//validationReport")
                if ($vr) { $compliant = $vr.isCompliant }
                foreach ($r in $x.SelectNodes("//rule[@status='FAILED']")) {
                    $desc = $r.description
                    if ($desc) { $desc = ($desc -replace '\s+', ' ').Trim() }
                    $failures += [pscustomobject]@{
                        Clause = $r.clause
                        Test   = $r.testNumber
                        Checks = $r.failedChecks
                        Desc   = $desc
                    }
                }
            } catch { Add-Line "         (nao consegui ler $rep : $_)" }

            if ($compliant -eq "true") {
                Add-Line "ok       verapdf:$($t.Stem)  PDF/A-2b CONFORME"
            } else {
                $script:failed++
                Add-Line "FALHOU   verapdf:$($t.Stem)  (exit $code, isCompliant=$compliant, $($failures.Count) regra(s))"
                foreach ($f in $failures) {
                    Add-Line ("         {0} teste {1}: {2} falha(s)" -f $f.Clause, $f.Test, $f.Checks)
                    if ($f.Desc) {
                        $d = $f.Desc
                        if ($d.Length -gt 150) { $d = $d.Substring(0, 150) + "..." }
                        Add-Line "           $d"
                    }
                }
            }
        }
    }
}

Add-Line ""
Add-Line "=== $ran passos, $failed falha(s) ==="

# Tamanho dos PDFs gerados, para detectar página a mais/a menos sem abrir o PDF.
Add-Line ""
Add-Line "--- PDFs ---"
Get-ChildItem -Path $src -Filter *.pdf -ErrorAction SilentlyContinue |
    Sort-Object Name |
    ForEach-Object { Add-Line ("{0,-34} {1,9} bytes  {2}" -f $_.Name, $_.Length, $_.LastWriteTime.ToString("HH:mm:ss")) }

if ($prova) {
    Add-Line ""
    Add-Line "=================== VEREDITO DA PROVA ==================="
    $conf = @($lines | Where-Object { $_ -match "PDF/A-2b CONFORME" }).Count
    Add-Line ("  passos ................... {0}" -f $ran)
    Add-Line ("  falhas ................... {0}" -f $failed)
    Add-Line ("  PDFs conformes PDF/A-2b .. {0}" -f $conf)
    if (@($lines | Where-Object { $_ -match "pulado   veraPDF" }).Count -gt 0) {
        Add-Line "  veraPDF .................. NAO RODOU"
        $provaProblemas += "veraPDF nao rodou"
    }
    if (@($lines | Where-Object { $_ -match "pulado   adversativa/lualatex" }).Count -gt 0) {
        Add-Line "  LuaLaTeX ................. NAO RODOU"
        $provaProblemas += "LuaLaTeX nao rodou"
    }
    if ($failed -eq 0 -and $provaProblemas.Count -eq 0) {
        Add-Line "  PROVA COMPLETA -- pode marcar a versao."
    } else {
        Add-Line ("  NAO PASSOU: " + (($provaProblemas + @("$failed falha(s)")) -join "; "))
    }
    Add-Line "========================================================"
}

$lines | Out-File -FilePath $result -Encoding utf8
Write-Host ""
Write-Host "Resultado em _scratch\RESULTADO.txt e logs em _scratch\build-logs\"
exit $failed
