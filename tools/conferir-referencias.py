#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Confere a lista de referencias contra os exemplos do Manual UFRJ/SiBI 2026.

O gabarito nao e inventado: as 34 categorias da secao 4.2 estao em duas bases,
`src/exemplo.bib' (nomes de campo em ingles, chaves m-<item>) e
`tests/adversativa/referencias-manual.bib' (sinonimos em portugues, chaves
pt-<item>), e cada entrada vem logo depois de um @comment{Manual: ...} com a
referencia EXATAMENTE como o Manual a imprime. Este script le o que a classe
compos, liga cada numero da lista a sua chave pelo .bbl ao lado do PDF, compara
com o gabarito daquela chave e diz onde diverge. Onde a divergencia e aceita --
@comment{Divergencia aceita: ...}, com o motivo --, a comparacao e com a forma
do @comment{Classe: ...} que vem junto, e nao ha aceitacao sem ela.

Antes de tudo, confere o proprio gabarito: cada @comment{Manual: ...} tem de
aparecer, igual, no texto do PDF do Manual que esta em specs/. Um gabarito
ajustado a classe faz a comparacao passar sem provar nada (#167).

A comparacao ignora o que nao e da norma: quebras de linha e de hifenizacao do
pdftotext, os espacos que o biblatex mete dentro de URLs longas, e a diferenca
entre hifen, meia-risca e travessao. O resto conta.

    python3 tools/conferir-referencias.py
    python3 tools/conferir-referencias.py tests/adversativa/adv_dscexam_pt.pdf
    CONFERIR=-v python3 tools/conferir-referencias.py tests/adversativa/adv_dscexam_pt.pdf

Precisa de python3 e poppler (pdftotext). O documento tem de ter sido
compilado com a opcao de classe `numbers' -- e o numero no comeco de cada
entrada que separa uma referencia da seguinte no texto extraido --, e o .bbl
daquela compilacao tem de estar ao lado do PDF. Documento sem referencia
numerada NAO PASSA: conta como divergencia.

Sem argumento, confere os documentos adversativos ja compilados que carregam o
gabarito com a opcao `numbers', nos dois motores. E assim que o `--conferir' do
painel e o build-check.ps1 o chamam: a lista mora aqui, e so aqui. Ficar fora
dos dois foi o que deixou a m-diss sair errada na 4.1 com este script acusando
a divergencia para ninguem (#151).
"""
import sys, re, os, subprocess, unicodedata, glob

# Saida por um cano, no Windows: sem isto o primeiro caractere fora da
# codificacao do console derrubava o verificador no meio do relato.
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(errors="replace")
    except (ValueError, OSError):
        pass

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
ADVERSATIVA = os.path.join(RAIZ, "tests", "adversativa")
BIB = os.path.join(ADVERSATIVA, "referencias-manual.bib")
# As duas bases com gabarito: a que acompanha a classe, com os nomes de campo em
# ingles (chaves m-<item>), e a da prova, com os sinonimos em portugues (pt-<item>).
BASES = [os.path.join(RAIZ, "src", "exemplo.bib"), BIB]
# O Manual, de onde o gabarito sai. Esta no repositorio.
MANUAL = os.path.join(RAIZ, "specs",
                      "Manual para elaboração e normalização de trabalhos acadêmicos 2024.pdf")


def alvos_padrao():
    """Os adversativos compilados que servem ao gabarito: os que carregam
    referencias-manual.bib com a opcao `numbers', pdfLaTeX e LuaLaTeX."""
    alvos = []
    for tex in sorted(glob.glob(os.path.join(ADVERSATIVA, "adv_*.tex"))):
        fonte = open(tex, encoding="utf-8", errors="replace").read()
        m = re.search(r"\\documentclass\[([^\]]*)\]", fonte)
        opcoes = [o.strip() for o in m.group(1).split(",")] if m else []
        if "numbers" in opcoes and "referencias-manual.bib" in fonte:
            base = os.path.splitext(tex)[0]
            alvos += [p for p in (base + ".pdf", base + "_lua.pdf") if os.path.exists(p)]
    return alvos


def gabaritos(caminho):
    """{chave: (referencia do Manual, motivo aceito ou None, forma da classe ou None)}.

    O gabarito e o @comment{Manual: ...} LOGO ANTES da entrada. Um
    @comment{Divergencia aceita: ...} registra uma divergencia ACEITA, com o
    motivo -- o Manual tem erratas, e ha coisas que ele imprime de um jeito que
    a norma nao exige; onde o certo e divergir, isso fica escrito ao lado da
    entrada, e nao escondido no numero final.

    A divergencia aceita vem com um @comment{Classe: ...}: a referencia
    EXATAMENTE como a classe tem de compo-la. E contra ela que a entrada e
    conferida. Ate a #167 a nota bastava, e a entrada inteira passava: a nota
    do ROMANO falava do "LEVI, G;" do Manual e escondia uma virgula errada da
    classe antes das paginas ("1996, p. 7-16"), que nenhuma nota aceitava.

    Ate a #164 o gabarito eram linhas `%%' dentro da entrada, logo abaixo da
    chave; o JabRef e os outros gerenciadores de referencias nao entendem o %
    como comentario, e os .bib passaram a ter so @Comment.

    So os comentarios colados a entrada contam: qualquer outra coisa entre eles
    e a entrada -- outra entrada, outro @Comment -- desfaz a ligacao, porque o
    exemplo.bib tambem e lido, e nele ha entradas sem gabarito e comentarios
    que nao sao gabarito de ninguem.
    """
    texto = open(caminho, encoding="utf-8").read().replace("\r\n", "\n")
    saida, gab, mot, cls = {}, None, [], None
    i = 0
    while True:
        m = re.compile(r"@(\w+)\s*\{", re.I).search(texto, i)
        if not m:
            break
        tipo = m.group(1).lower()
        if tipo == "comment":
            prof, j = 1, m.end()
            while prof and j < len(texto):
                prof += {"{": 1, "}": -1}.get(texto[j], 0)
                j += 1
            corpo = " ".join(texto[m.end():j - 1].split())
            if corpo.startswith("Manual:"):
                gab, mot, cls = corpo[len("Manual:"):].strip(), [], None
            elif corpo.startswith("Divergencia aceita:") and gab is not None:
                mot.append(corpo[len("Divergencia aceita:"):].strip())
            elif corpo.startswith("Classe:") and gab is not None:
                cls = corpo[len("Classe:"):].strip()
            else:
                gab, mot, cls = None, [], None
            i = j
            continue
        k = re.match(r"\s*([^,\s]+)\s*,", texto[m.end():])
        if k and gab is not None:
            saida[k.group(1)] = (gab, " ".join(mot) if mot else None, cls)
        gab, mot, cls = None, [], None
        i = m.end()
    return saida


def _junta(s):
    """O que a comparacao com o texto do Manual olha: sem espacos, e com os
    tracos iguais -- o Manual escreve travessao onde o .bib escreve dois hifens."""
    s = unicodedata.normalize("NFC", s)
    s = s.replace("–", "-").replace("—", "-").replace("‐", "-").replace("­", "")
    s = s.replace("“", '"').replace("”", '"')
    s = re.sub(r"-{2,}", "-", s)
    return re.sub(r"\s+", "", s)


def fora_do_manual(gab, texto_manual):
    """As chaves cujo gabarito NAO aparece, igual, no texto do Manual.

    O gabarito e a referencia como o Manual a imprime, errata e tudo; a
    divergencia fica escrita ao lado, e nao corrigida em silencio no gabarito.
    Ate a #167 nada conferia isso, e 12 das 34 referencias nao eram o Manual: a
    errata corrigida sem nota ("Acesso em 28 ago." virava "Acesso em: 28 ago."),
    o dado que a classe nao compoe trocado por outro (a data "[19--?]" virava
    "1990") e o elemento que ela nao tinha simplesmente omitido (o "Procurador:"
    da patente). Com o gabarito ajustado a classe, a comparacao passava.
    """
    corpo = _junta(re.sub(r"(?m)^\s*\d{1,3}\s*$", "", texto_manual))
    return [k for k, (manual, _, _) in gab.items() if _junta(manual) not in corpo]


def confere_gabaritos():
    """Divergencias dos gabaritos das duas bases contra o texto do Manual.

    Com -layout: sem ele, o pdftotext do poppler junta a palavra partida no fim
    da linha e COME o hifen -- "melhor-foto" de uma URL sai "melhorfoto", e o
    intervalo "p. 37-44" sai "p. 3744". Com -layout a linha sai como impressa.
    """
    texto = (_saida(["pdftotext", "-enc", "UTF-8", "-layout", MANUAL, "-"])
             if os.path.exists(MANUAL) else "")
    if not texto.strip():
        print("=== o Manual nao foi lido (%s): os gabaritos NAO foram conferidos contra ele"
              % os.path.relpath(MANUAL, RAIZ))
        return 1
    dif, total = 0, 0
    for base in BASES:
        gab = gabaritos(base)
        total += len(gab)
        for chave in fora_do_manual(gab, texto):
            print("   GABARITO %s (%s) -- nao e o texto do Manual" % (chave, os.path.basename(base)))
            dif += 1
    print("=== gabaritos: %d de %d iguais ao texto do Manual" % (total - dif, total))
    return dif


def bases_do_documento(pdf):
    """As bases com gabarito que o documento carrega, pelo \\addbibresource do
    .tex ao lado do PDF. Sem o .tex, as duas."""
    base = os.path.splitext(pdf)[0]
    if base.endswith("_lua"):
        base = base[:-4]                     # o gemeo LuaLaTeX usa o mesmo .tex
    try:
        fonte = open(base + ".tex", encoding="utf-8", errors="replace").read()
    except OSError:
        return list(BASES)
    recursos = [os.path.basename(r) for r in re.findall(r"\\addbibresource\{([^}]+)\}", fonte)]
    return [b for b in BASES if os.path.basename(b) in recursos]


def chaves_do_bbl(pdf):
    """As chaves na ordem da lista de referencias, lidas do .bbl ao lado do PDF.

    No sistema numerico a marca [n] e a posicao da entrada na lista que o biber
    ordenou, e o .bbl traz essa lista. E isso que liga cada referencia composta
    a sua entrada. O casamento antigo, pelo comeco do texto, ja tinha emparelhado
    gabarito com a entrada errada, e com a mesma referencia em duas bases -- uma
    com os campos em ingles, outra em portugues -- nem teria como acertar.
    """
    try:
        texto = open(os.path.splitext(pdf)[0] + ".bbl", encoding="utf-8",
                     errors="replace").read()
    except OSError:
        return None
    m = re.search(r"\\datalist\[entry\]\{[^}]*\}(.*?)\\enddatalist", texto, re.S)
    return re.findall(r"\\entry\{([^}]+)\}", m.group(1)) if m else None


def normaliza(s):
    """Reduz a string ao que a norma fixa."""
    s = unicodedata.normalize("NFC", s)
    s = s.replace("–", "-").replace("—", "-").replace("‐", "-")
    s = s.replace("­", "")            # hifen de hifenizacao
    s = re.sub(r"-\s*\n\s*", "", s)        # palavra quebrada por hifenizacao
    s = re.sub(r"-{2,}", "-", s)          # o travessao do manual, transcrito
    s = re.sub(r"(?m)^\s*\d{1,3}\s*$", "", s)  # folio solto entre folhas
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def so_letras(s):
    """Para a comparacao: sem espacos e sem hifens.

    Espaco, porque e onde pdftotext e biblatex discordam sem que a norma tenha
    opiniao -- o biblatex quebra URLs longas metendo espacos, e o extrator os
    devolve. Hifen, pela mesma razao: numa URL quebrada entre linhas o hifen
    tipografico as vezes sobra e as vezes some. Como a supressao vale para os
    dois lados da comparacao, um intervalo de paginas continua batendo.
    """
    return re.sub(r"[\s-]+", "", normaliza(s))


def _saida(args):
    """Roda e decodifica em UTF-8 com substituicao.

    Sem isto, no Windows o Python tenta a codificacao do console e devolve None
    no primeiro acento -- e o script morria com um TypeError que nao dizia nada
    sobre o documento.
    """
    return subprocess.run(args, capture_output=True).stdout.decode("utf-8", "replace")


def referencias_do_pdf(pdf):
    """As referencias compostas, na ordem, separadas pelo numero de cada uma.

    O documento inteiro numa chamada so do pdftotext. Folha a folha, como era,
    dava o mesmo texto e custava meio segundo por folha no Windows (#151).

    Com -layout: sem ele, o texto que o LuaLaTeX compoe sai com o numero da
    referencia numa linha SOZINHA, e a limpeza dos folios (linha so com numero)
    o apagava junto -- o documento LuaLaTeX ficava sem marca nenhuma. Com
    -layout o numero e o comeco da referencia ficam na mesma linha nos dois
    motores, e o folio continua numa linha so dele.
    """
    return separa_referencias(_saida(["pdftotext", "-enc", "UTF-8", "-layout", pdf, "-"]))


def separa_referencias(todo):
    """[(numero, referencia)] do texto extraido do documento inteiro.

    Desde a #140 a lista numerica sai sem colchetes -- "1 SOBRENOME, Nome..." --,
    e a separacao pela marca [n] achava zero referencias: o documento era dado
    como "pulado" e o verificador passava sem conferir nada, de 17 a 21/09/2026
    (#167). Agora a marca e o numero no comeco da linha, com ou sem colchetes,
    e so vale o NUMERO SEGUINTE da sequencia: "156 p." ou "1979." no comeco de
    uma linha de continuacao nao partem a referencia, porque nao sao o proximo
    numero.
    """
    m = re.search(r"^\s*REFER[ÊE]NCIAS\s*$", todo, re.M)
    if not m: return []
    corpo = re.sub(r"(?m)^\s*\d{1,3}\s*$", "", todo[m.end():])
    fim = re.search(r"^\s*(AP[ÊE]NDICE|ANEXO|[ÍI]NDICE REMISSIVO)\b", corpo, re.M)
    if fim: corpo = corpo[:fim.start()]
    marcas, esperado = [], 1
    for m in re.finditer(r"(?m)^[ \t]*\[?(\d{1,3})\]?[ \t]+(?=\S)", corpo):
        if int(m.group(1)) == esperado:
            marcas.append((esperado, m.start(), m.end()))
            esperado += 1
    saida = []
    for i, (n, ini, fim) in enumerate(marcas):
        prox = marcas[i + 1][1] if i + 1 < len(marcas) else len(corpo)
        saida.append((n, normaliza(corpo[fim:prox])))
    return saida


def diferenca(esperado, obtido):
    """O primeiro ponto em que as duas divergem, com um trecho de cada lado."""
    a, b = so_letras(esperado), so_letras(obtido)
    i = 0
    while i < min(len(a), len(b)) and a[i].lower() == b[i].lower(): i += 1
    if i == len(a) == len(b): return None
    return i, esperado, obtido


def compara(gab, por_chave, verboso=False):
    """(divergencias, aceitas, linhas do relato) de um documento.

    Sem divergencia aceita, a classe tem de compor o Manual. Com ela, tem de
    compor a forma do @comment{Classe: ...} -- e so ela: o que a nota nao
    aceita continua sendo divergencia (#167). Tambem nao passam a divergencia
    aceita sem a forma da classe, que aceitaria qualquer coisa, e a nota velha,
    de uma divergencia que ja nao existe.
    """
    dif, aceitas, linhas = 0, 0, []
    for chave, (manual, motivo, classe) in gab.items():
        obtido = por_chave.get(chave)
        if obtido is None:
            linhas.append("   AUSENTE  %s" % chave); dif += 1
            continue
        if not motivo:
            if diferenca(manual, obtido) is None:
                if verboso: linhas.append("   ok       %s" % chave)
            else:
                dif += 1
                linhas += ["   DIFERE   %s" % chave,
                           "     manual: %s" % manual,
                           "     classe: %s" % obtido]
        elif not classe:
            dif += 1
            linhas += ["   SEM FORMA %s -- divergencia aceita sem o @comment{Classe: ...}; "
                       "a classe compoe:" % chave,
                       "     classe: %s" % obtido]
        elif diferenca(manual, obtido) is None:
            dif += 1
            linhas.append("   NOTA VELHA %s -- a classe ja compoe o Manual: "
                          "tire a divergencia aceita" % chave)
        elif diferenca(classe, obtido) is None:
            aceitas += 1
            if verboso: linhas.append("   aceita   %s -- %s" % (chave, motivo))
        else:
            dif += 1
            linhas += ["   DIFERE   %s (fora da divergencia aceita)" % chave,
                       "     manual: %s" % manual,
                       "     aceita: %s" % classe,
                       "     classe: %s" % obtido]
    return dif, aceitas, linhas


if __name__ == "__main__":
    # Primeiro o gabarito: se ele nao e o Manual, comparar a classe com ele nao
    # prova nada.
    total_dif = confere_gabaritos()
    alvos = sys.argv[1:]
    if not alvos:
        alvos = alvos_padrao()
        if not alvos:
            # Nada compilado ainda. Diz o que faltou, em vez de sair calado: um
            # verificador que nao conferiu nada nao pode parecer aprovacao.
            print("=== pulado: nenhum documento adversativo com o gabarito foi "
                  "compilado (coppetex.bat --adversativo)")
            print("\n=== TOTAL: %d divergencia(s) ===" % total_dif)
            sys.exit(1 if total_dif else 0)
    verboso = "-v" in os.environ.get("CONFERIR", "")
    for pdf in alvos:
        nome = os.path.basename(pdf)
        gab = {}
        for b in bases_do_documento(pdf):
            gab.update(gabaritos(b))
        compostas = referencias_do_pdf(pdf)
        if not gab:
            print("\n=== %s -- pulado (o documento nao carrega base com gabarito)" % nome)
            continue
        if not compostas:
            # Sem a opcao de classe `numbers' nao ha numero na frente de cada
            # entrada, e no estilo autor-data nao ha fronteira confiavel entre
            # uma entrada e a seguinte no texto extraido. Nao e perda: os drivers
            # do .bbx sao os mesmos nos dois sistemas de chamada. Mas um
            # documento que devia ser conferido e nao foi NAO PASSA: de 17 a
            # 21/09/2026 este ramo dizia "pulado" e o verificador aprovava a
            # prova sem ter lido uma referencia (#167).
            print("\n=== %s -- NAO CONFERIDO: nenhuma referencia numerada no texto "
                  "(compile com a opcao `numbers')" % nome)
            total_dif += 1
            continue
        chaves = chaves_do_bbl(pdf)
        # Sem o .bbl, ou com um .bbl de outra compilacao, nao ha como saber qual
        # entrada e cada [n]. Isso conta como divergencia: conferencia que nao
        # pode ser feita nao pode sair como aprovada.
        if chaves is None:
            print("\n=== %s -- sem o .bbl ao lado do PDF: nao ha como ligar [n] a chave"
                  % nome)
            total_dif += 1
            continue
        if len(chaves) != len(compostas):
            print("\n=== %s -- o .bbl lista %d entradas e o PDF compoe %d referencias: "
                  "os dois sao de compilacoes diferentes?" % (nome, len(chaves), len(compostas)))
            total_dif += 1
            continue
        por_chave = dict((chaves[num - 1], texto) for num, texto in compostas
                         if 0 < num <= len(chaves))
        print("\n=== %s -- %d referencias no gabarito, %d compostas"
              % (nome, len(gab), len(compostas)))
        dif, aceitas, linhas = compara(gab, por_chave, verboso)
        for linha in linhas:
            print(linha)
        total_dif += dif
        print("   --- %d divergencia(s), %d aceita(s)" % (dif, aceitas))
    print("\n=== TOTAL: %d divergencia(s) ===" % total_dif)
    sys.exit(1 if total_dif else 0)
