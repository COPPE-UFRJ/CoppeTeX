# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: nao havia defeito antigo aqui -- o estilo do Instituto de Computacao (ufrj-ic, para o PPGI) nasceu em outubro de 2026 com os dados do Projeto Jacurutu, o modelo LaTeX mantido no PPGI, e este teste guarda o que o estilo promete.

O PPGI e oferecido por DOIS institutos, e o Jacurutu nomeia os dois na capa e
na natureza; o logotipo do PPGI fica a direita da capa, na altura do da UFRJ.

Cobra-se, numa dissertacao do PPGI:
  1. a capa traz os dois institutos, cada um na sua linha, e o Programa com a
     sigla: "PROGRAMA DE POS-GRADUACAO EM INFORMATICA (PPGI)";
  2. a folha de rosto traz a natureza do Jacurutu, com os dois institutos e o
     titulo de Mestre em Informatica;
  3. a tinta do logotipo do PPGI tem 0,70 da altura da do logotipo da UFRJ --
     a mesma razao da capa do Jacurutu (17,6 mm para 25,1 mm), medida na
     pagina composta, e nao no arquivo.

E num trabalho de conclusao do Bacharelado em Ciencia da Computacao (grad):
  4. a capa traz so o Instituto de Computacao e "CURSO DE BACHARELADO EM
     CIENCIA DA COMPUTACAO", e nada do Instituto Tercio Pacitti nem do PPGI;
  5. a natureza fala em Bacharel em Ciencia da Computacao;
  6. o logotipo do PPGI NAO sai -- a graduacao tem outro --, e sem o
     ic-logo.pdf o log avisa.
"""
import io
import os
import subprocess

from medidas import Documento, relatar, normaliza

TEX = r"""\documentclass[msc]{ufrj}
\usepackage{ufrj-ic}
\begin{document}
\title{Documento de prova}
\foreigntitle{Proof document}
\author{Nome}{Sobrenome}
\advisor{Ana}{Silva}{D.Sc.}{UFRJ}
\examiner{Ana Silva}{D.Sc.}{PPGI/UFRJ}
\department{PPGI}
\date{03}{2026}
\concentrationarea{Ciência da Computação}
\keyword{regressao}
\foreignkeyword{regression}
\maketitle
\frontmatter
\begin{abstract}Resumo.\end{abstract}
\begin{foreignabstract}Abstract.\end{foreignabstract}
\tableofcontents
\mainmatter
\chapter{Um}Texto.
\end{document}
"""

CAPA = ["INSTITUTO DE COMPUTAÇÃO",
        "INSTITUTO TÉRCIO PACITTI DE APLICAÇÕES E PESQUISAS COMPUTACIONAIS",
        "PROGRAMA DE PÓS-GRADUAÇÃO EM INFORMÁTICA (PPGI)"]
NATUREZA = ("Dissertação de Mestrado apresentada ao Programa de Pós-Graduação em "
            "Informática, Instituto de Computação e Instituto Tércio Pacitti de "
            "Aplicações e Pesquisas Computacionais, Universidade Federal do Rio de "
            "Janeiro, como requisito parcial à obtenção do título de Mestre em "
            "Informática.")
RAZAO, TOL = 0.70, 0.04
DPI = 150


def le_pgm(caminho):
    d = open(caminho, "rb").read()
    partes, i = [], 0
    while len(partes) < 4:
        while d[i:i + 1].isspace():
            i += 1
        j = i
        while not d[j:j + 1].isspace():
            j += 1
        partes.append(d[i:j])
        i = j
    i += 1
    w, h = int(partes[1]), int(partes[2])
    return w, h, d[i:i + w * h]


def altura_da_tinta(w, px, x0, x1, ymax):
    linhas = [y for y in range(ymax)
              if any(px[y * w + x] < 128 for x in range(x0, x1))]
    return (linhas[-1] - linhas[0] + 1) if linhas else 0


problemas = []
with Documento(tex=TEX) as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    capa = [normaliza(l) for l in d.texto(1).splitlines()]
    for linha in CAPA:
        if normaliza(linha) not in capa:
            problemas.append("capa: falta a linha %r" % linha)
    if normaliza(NATUREZA) not in normaliza(d.texto(2)):
        problemas.append("folha de rosto: a natureza nao e a do Jacurutu")

    base = os.path.join(d.pasta, "capa")
    subprocess.run(["pdftoppm", "-gray", "-r", str(DPI), "-f", "1", "-l", "1",
                    "-singlefile", os.path.join(d.pasta, d.nome + ".pdf"), base],
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if not os.path.exists(base + ".pgm"):
        problemas.append("nao consegui rasterizar a capa com o pdftoppm")
    else:
        w, h, px = le_pgm(base + ".pgm")
        faixa = int(h * 0.20)
        ufrj = altura_da_tinta(w, px, 0, w // 2, faixa)
        ppgi = altura_da_tinta(w, px, w // 2, w, faixa)
        if not ufrj or not ppgi:
            problemas.append("capa: nao achei os dois logotipos no alto da folha")
        elif abs(ppgi / float(ufrj) - RAZAO) > TOL:
            problemas.append("capa: o logotipo do PPGI tem %.2f da altura do da "
                             "UFRJ; no Jacurutu sao %.2f" % (ppgi / float(ufrj), RAZAO))

GRAD = TEX.replace(r"\documentclass[msc]{ufrj}", r"\documentclass[grad]{ufrj}") \
          .replace(r"\department{PPGI}", r"\department{BCC}") \
          .replace(r"\concentrationarea{Ciência da Computação}", "")
with Documento(tex=GRAD) as d:
    if not d.ok:
        relatar(problemas + ["grad: nao compilou: %s" % d.erros_do_log()])
    capa = normaliza(d.texto(1))
    for linha in ("INSTITUTO DE COMPUTAÇÃO",
                  "CURSO DE BACHARELADO EM CIÊNCIA DA COMPUTAÇÃO"):
        if normaliza(linha) not in capa:
            problemas.append("grad, capa: falta %r" % linha)
    for linha in ("TÉRCIO PACITTI", "PPGI", "PÓS-GRADUAÇÃO"):
        if normaliza(linha) in capa:
            problemas.append("grad, capa: %r e do PPGI, e nao da graduacao" % linha)
    if normaliza("título de Bacharel em Ciência da Computação") not in normaliza(d.texto(2)):
        problemas.append("grad: a natureza nao fala em Bacharel em Ciencia da Computacao")
    log = io.open(os.path.join(d.pasta, d.nome + ".log"), encoding="latin-1").read()
    if "ppgi-logo" in log:
        problemas.append("grad: o logotipo do PPGI entrou na capa da graduacao")
    if "ic-logo.pdf" not in log:
        problemas.append("grad: sem o ic-logo.pdf, o log devia avisar")

relatar(problemas)
