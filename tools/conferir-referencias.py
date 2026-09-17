#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Confere a lista de referencias contra os exemplos do Manual UFRJ/SiBI 2026.

O gabarito nao e inventado: as 34 categorias da secao 4.2 estao em duas bases,
`src/exemplo.bib' (nomes de campo em ingles, chaves m-<item>) e
`tests/adversativa/referencias-manual.bib' (sinonimos em portugues, chaves
pt-<item>), e cada entrada traz, num comentario `%%' logo abaixo da chave, a
referencia EXATAMENTE como o Manual a imprime. Este script le o que a classe
compos, liga cada [n] a sua chave pelo .bbl ao lado do PDF, compara com o
gabarito daquela chave e diz onde diverge.

A comparacao ignora o que nao e da norma: quebras de linha e de hifenizacao do
pdftotext, os espacos que o biblatex mete dentro de URLs longas, e a diferenca
entre hifen, meia-risca e travessao. O resto conta.

    python3 tools/conferir-referencias.py
    python3 tools/conferir-referencias.py tests/adversativa/adv_dscexam_pt.pdf
    CONFERIR=-v python3 tools/conferir-referencias.py tests/adversativa/adv_dscexam_pt.pdf

Precisa de python3 e poppler (pdftotext). O documento tem de ter sido
compilado com a opcao de classe `numbers' -- e a marca [n] que separa uma
referencia da seguinte no texto extraido --, e o .bbl daquela compilacao tem de
estar ao lado do PDF.

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
    """{chave: (referencia do Manual, motivo aceito ou None)}.

    O gabarito vem das linhas `%%' LOGO ABAIXO da linha da chave; o bloco acaba
    na primeira linha que nao comeca por `%%'. Uma linha `%%!' registra uma
    divergencia ACEITA, com o motivo -- o Manual tem erratas, e ha coisas que
    ele imprime de um jeito que a norma nao exige; onde o certo e divergir, isso
    fica escrito ao lado da entrada, e nao escondido no numero final.

    So o bloco colado a chave, porque o exemplo.bib tambem e lido, e nele ha
    entradas sem gabarito e comentarios `%%' que nao sao gabarito de ninguem.
    """
    texto = open(caminho, encoding="utf-8").read()
    saida, chave, buf, mot = {}, None, [], []
    def fecha():
        if chave is not None and buf:
            saida[chave] = (" ".join(buf), " ".join(mot) if mot else None)
    for linha in texto.split("\n"):
        linha = linha.rstrip("\r")
        m = re.match(r"^@\w+\{\s*([^,\s]+)\s*,", linha)
        if m:
            fecha()
            chave, buf, mot = m.group(1), [], []
            continue
        if chave is not None and linha.startswith("%%!"):
            mot.append(linha[3:].strip())
            continue
        if chave is not None and linha.startswith("%%"):
            buf.append(linha[2:].strip())
            continue
        fecha()
        chave, buf, mot = None, [], []
    fecha()
    return saida


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
    """As referencias compostas, na ordem, separadas pela marca [n].

    O documento inteiro numa chamada so do pdftotext. Folha a folha, como era,
    dava o mesmo texto e custava meio segundo por folha no Windows (#151).
    """
    todo = _saida(["pdftotext", pdf, "-"])
    m = re.search(r"^\s*REFER[ÊE]NCIAS\s*$", todo, re.M)
    if not m: return []
    corpo = re.sub(r"(?m)^\s*\d{1,3}\s*$", "", todo[m.end():])
    fim = re.search(r"^\s*(AP[ÊE]NDICE|ANEXO|[ÍI]NDICE REMISSIVO)\b", corpo, re.M)
    if fim: corpo = corpo[:fim.start()]
    pedacos = re.split(r"\n\s*\[(\d+)\]\s*", "\n" + corpo)
    saida = []
    for i in range(1, len(pedacos) - 1, 2):
        saida.append((int(pedacos[i]), normaliza(pedacos[i + 1])))
    return saida


def diferenca(esperado, obtido):
    """O primeiro ponto em que as duas divergem, com um trecho de cada lado."""
    a, b = so_letras(esperado), so_letras(obtido)
    i = 0
    while i < min(len(a), len(b)) and a[i].lower() == b[i].lower(): i += 1
    if i == len(a) == len(b): return None
    return i, esperado, obtido


if __name__ == "__main__":
    alvos = sys.argv[1:]
    if not alvos:
        alvos = alvos_padrao()
        if not alvos:
            # Nada compilado ainda. Diz o que faltou, em vez de sair calado: um
            # verificador que nao conferiu nada nao pode parecer aprovacao.
            print("=== pulado: nenhum documento adversativo com o gabarito foi "
                  "compilado (coppetex.bat --adversativo)")
            sys.exit(0)
    verboso = "-v" in os.environ.get("CONFERIR", "")
    total_dif = 0
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
            # Sem a opcao de classe `numbers' nao ha marca [n], e no estilo
            # autor-data nao ha fronteira confiavel entre uma entrada e a
            # seguinte no texto extraido. Nao e perda: os drivers do .bbx sao
            # os mesmos nos dois sistemas de chamada -- o que muda e a chamada
            # no texto, que e do .cbx --, entao conferir os numericos confere
            # a composicao das referencias.
            print("\n=== %s -- pulado (compile com a opcao `numbers')" % nome)
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
        dif, aceitas = 0, 0
        print("\n=== %s -- %d referencias no gabarito, %d compostas"
              % (nome, len(gab), len(compostas)))
        for chave, (esperado, motivo) in gab.items():
            obtido = por_chave.get(chave)
            if obtido is None:
                print("   AUSENTE  %s" % chave); dif += 1; continue
            d = diferenca(esperado, obtido)
            if d is None:
                if verboso: print("   ok       %s" % chave)
            elif motivo:
                aceitas += 1
                if verboso:
                    print("   aceita   %s -- %s" % (chave, motivo))
            else:
                dif += 1
                print("   DIFERE   %s" % chave)
                print("     manual: %s" % esperado)
                print("     classe: %s" % obtido)
        total_dif += dif
        print("   --- %d divergencia(s), %d aceita(s)" % (dif, aceitas))
    print("\n=== TOTAL: %d divergencia(s) ===" % total_dif)
    sys.exit(1 if total_dif else 0)
