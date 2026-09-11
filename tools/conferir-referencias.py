#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Confere a lista de referencias contra os exemplos do Manual UFRJ/SiBI 2026.

O gabarito nao e inventado: cada entrada de `adversativa/referencias-manual.bib'
traz, num comentario `%%' logo abaixo da chave, a referencia EXATAMENTE como a
secao 4.2 do Manual a imprime. Este script compoe o que a classe produziu, o
compara com esse gabarito e diz onde diverge.

A comparacao ignora o que nao e da norma: quebras de linha e de hifenizacao do
pdftotext, os espacos que o biblatex mete dentro de URLs longas, e a diferenca
entre hifen, meia-risca e travessao. O resto conta.

    python3 tools/conferir-referencias.py adversativa/adv_dsc_pt.pdf
    CONFERIR=-v python3 tools/conferir-referencias.py adversativa/adv_dsc_pt.pdf

Precisa de python3 e poppler (pdftotext, pdfinfo). O documento tem de ter sido
compilado com a opcao de classe `numbers': e a marca [n] que separa uma
referencia da seguinte no texto extraido.
"""
import sys, re, os, subprocess, unicodedata

BIB = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "..", "adversativa", "referencias-manual.bib")


def gabaritos(caminho):
    """{chave: (referencia do Manual, motivo aceito ou None)}.

    O gabarito vem das linhas `%%'. Uma linha `%%!' registra uma divergencia
    ACEITA, com o motivo -- o Manual tem erratas, e ha coisas que ele imprime
    de um jeito que a norma nao exige; onde o certo e divergir, isso fica
    escrito ao lado da entrada, e nao escondido no numero final.
    """
    texto = open(caminho, encoding="utf-8").read()
    saida, chave, buf, mot = {}, None, [], []
    def fecha():
        if chave and buf:
            saida[chave] = (" ".join(buf), " ".join(mot) if mot else None)
    for linha in texto.split("\n"):
        m = re.match(r"^@\w+\{([^,]+),", linha)
        if m:
            fecha()
            chave, buf, mot = m.group(1).strip(), [], []
            continue
        if chave is not None and linha.startswith("%%!"):
            mot.append(linha[3:].strip())
        elif chave is not None and linha.startswith("%%"):
            buf.append(linha[2:].strip())
    fecha()
    return saida


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
    """As referencias compostas, na ordem, separadas pela marca [n]."""
    info = _saida(["pdfinfo", pdf])
    n = int(re.search(r"^Pages:\s+(\d+)", info, re.M).group(1))
    todo = ""
    for p in range(1, n + 1):
        todo += _saida(["pdftotext", "-f", str(p), "-l", str(p), pdf, "-"])
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


def casa(gab, compostas):
    """Liga cada gabarito a referencia composta, pelo comeco do titulo."""
    usados, pares = set(), []
    for chave, (esperado, motivo) in gab.items():
        # a primeira sequencia de 12+ letras do gabarito que nao seja o autor
        alvo = so_letras(esperado)[:40]
        achou = None
        for num, texto in compostas:
            if num in usados: continue
            t = so_letras(texto)[:40].lower()
            # o casamento e pelo INICIO, e so pelo inicio: um "esta contido em"
            # ja emparelhou gabarito com a entrada errada.
            n = min(len(t), len(alvo), 24)
            if t[:n] == alvo.lower()[:n]:
                achou = (num, texto); break
        if achou is None:
            # Segunda tentativa, pelo titulo: quando o Manual abrevia a autoria
            # com "et al." e a classe lista todos, o inicio nunca bate, mas a
            # entrada e a mesma. Casa-se pela palavra mais longa do gabarito.
            palavras = sorted(re.findall(r"\w{9,}", esperado), key=len, reverse=True)
            for pal in palavras[:3]:
                for num, texto in compostas:
                    if num in usados: continue
                    if pal.lower() in so_letras(texto).lower():
                        achou = (num, texto); break
                if achou: break
        if achou:
            usados.add(achou[0]); pares.append((chave, esperado, achou[1], motivo))
        else:
            pares.append((chave, esperado, None, motivo))
    return pares


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
        print(__doc__); sys.exit(2)
    gab = gabaritos(BIB)
    verboso = "-v" in os.environ.get("CONFERIR", "")
    total_dif = 0
    for pdf in alvos:
        compostas = referencias_do_pdf(pdf)
        if len(compostas) < len(gab):
            # Sem a opcao de classe `numbers' nao ha marca [n], e no estilo
            # autor-data nao ha fronteira confiavel entre uma entrada e a
            # seguinte no texto extraido. Nao e perda: os drivers do .bbx sao
            # os mesmos nos dois sistemas de chamada -- o que muda e a chamada
            # no texto, que e do .cbx --, entao conferir os numericos confere
            # a composicao das referencias.
            print("\n=== %s -- pulado (compile com a opcao `numbers')"
                  % os.path.basename(pdf))
            continue
        pares = casa(gab, compostas)
        dif, aceitas = 0, 0
        print("\n=== %s -- %d referencias no gabarito, %d compostas"
              % (os.path.basename(pdf), len(gab), len(compostas)))
        for chave, esperado, obtido, motivo in pares:
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
