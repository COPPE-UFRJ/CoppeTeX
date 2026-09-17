# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: (desconformidade, 2.4) entre o titulo de uma secao e o texto que o segue ficava menos de uma linha em branco: o espaco depois do titulo era o padrao do titlesec (2,3 ex), cerca de dois tercos de uma linha de 1,5 (#122).

A 2.4 do Manual UFRJ/SiBI pede os titulos das secoes separados do texto que os
precede E do texto que os sucede por um espaco de 1,5 -- uma linha em branco na
entrelinha do texto.

Cobra-se, para secao e subsecao: a distancia entre a base do titulo e a base da
linha de texto seguinte (e da anterior) e de pelo menos DUAS entrelinhas do
texto, medidas no proprio documento (1,5 pt de tolerancia, para a cola elastica).
"""
from medidas import Documento, relatar

TEXTO = ("Paragrafo de enchimento com texto suficiente para ocupar duas linhas "
         "inteiras na mancha, de modo que se possa medir a entrelinha do corpo "
         "do texto no proprio documento.")
CORPO = r"""
\chapter{Um}
%(t)s
\section{Secao medida}
%(t)s
\subsection{Subsecao medida}
%(t)s
""" % {"t": TEXTO}

problemas = []
with Documento(corpo=CORPO) as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    pg = d.pagina_com("Secao medida")
    linhas = d.linhas(pg)
    # entrelinha: duas linhas consecutivas do mesmo paragrafo
    base = [ln[0].y1 for ln in linhas]
    par = [i for i, ln in enumerate(linhas) if ln[0].texto == "Paragrafo"]
    if not par:
        relatar(["nao achei o paragrafo de enchimento"])
    entrelinha = linhas[par[0] + 1][0].y1 - linhas[par[0]][0].y1
    for titulo in ("SECAO", "Subsecao"):
        idx = [i for i, ln in enumerate(linhas)
               if any(w.texto.upper() == titulo.upper() for w in ln)]
        if not idx:
            problemas.append("nao achei o titulo %s" % titulo)
            continue
        i = idx[0]
        depois = linhas[i + 1][0].y1 - linhas[i][0].y1
        antes = linhas[i][0].y1 - linhas[i - 1][0].y1
        if depois < 2 * entrelinha - 1.5:
            problemas.append("%s: %.1f pt da base do titulo a base do texto seguinte; "
                             "o minimo e uma linha em branco (%.1f pt)"
                             % (titulo, depois, 2 * entrelinha))
        if antes < 2 * entrelinha - 1.5:
            problemas.append("%s: %.1f pt da base do texto anterior a base do titulo; "
                             "o minimo e uma linha em branco (%.1f pt)"
                             % (titulo, antes, 2 * entrelinha))

relatar(problemas)
