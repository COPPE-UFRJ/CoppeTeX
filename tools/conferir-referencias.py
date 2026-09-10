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
    """{chave: referencia como o Manual a imprime}, lida dos comentarios %%."""
    texto = open(caminho, encoding="utf-8").read()
    saida, chave, buf = {}, None, []
    for linha in texto.split("\n"):
        m = re.match(r"^@\w+\{([^,]+),", linha)
        if m:
            if chave and buf: saida[chave] = " ".join(buf)
            chave, buf = m.group(1).strip(), []
            continue
        if chave is not None and linha.startswith("%%"):
            buf.append(linha[2:].strip())
        elif chave is not None and buf and not linha.startswith("%%"):
            saida[chave] = " ".join(buf); buf = []
    if chave and buf: saida[chave] = " ".join(buf)
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
    """Para a comparacao: sem espacos nenhum, que e onde pdftotext e biblatex
    discordam sem que a norma tenha opiniao."""
    return re.sub(r"\s+", "", normaliza(s))


def referencias_do_pdf(pdf):
    """As referencias compostas, na ordem, separadas pela marca [n]."""
    info = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
    n = int(re.search(r"^Pages:\s+(\d+)", info, re.M).group(1))
    todo = ""
    for p in range(1, n + 1):
        todo += subprocess.run(["pdftotext", "-f", str(p), "-l", str(p), pdf, "-"],
                               capture_output=True, text=True).stdout
    m = re.search(r"^\s*REFER[ÊE]NCIAS\s*$", todo, re.M)
    if not m: return []
    corpo = todo[m.end():]
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
    for chave, esperado in gab.items():
        # a primeira sequencia de 12+ letras do gabarito que nao seja o autor
        alvo = so_letras(esperado)[:40]
        achou = None
        for num, texto in compostas:
            if num in usados: continue
            t = so_letras(texto)
            # compara pelo inicio, tolerando caixa
            if t[:40].lower() == alvo.lower() or alvo.lower()[:24] in t.lower():
                achou = (num, texto); break
        if achou:
            usados.add(achou[0]); pares.append((chave, esperado, achou[1]))
        else:
            pares.append((chave, esperado, None))
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
        pares = casa(gab, compostas)
        dif = 0
        print("\n=== %s -- %d referencias no gabarito, %d compostas"
              % (os.path.basename(pdf), len(gab), len(compostas)))
        for chave, esperado, obtido in pares:
            if obtido is None:
                print("   AUSENTE  %s" % chave); dif += 1; continue
            d = diferenca(esperado, obtido)
            if d is None:
                if verboso: print("   ok       %s" % chave)
            else:
                dif += 1
                print("   DIFERE   %s" % chave)
                print("     manual: %s" % esperado)
                print("     classe: %s" % obtido)
        total_dif += dif
        print("   --- %d divergencia(s)" % dif)
    print("\n=== TOTAL: %d divergencia(s) ===" % total_dif)
    sys.exit(1 if total_dif else 0)
