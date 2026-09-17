# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX. NAO roda na suite normal.

BUG: (inconsistencia, 2.10, 3.1.4.3, 3.1.4.4 e Norma COPPE 12) o sinal entre o numero e o titulo nao era o mesmo em toda parte: meia-risca (U+2013) na legenda, no titulo de apendice e no sumario, e travessao (U+2014) no exemplo da secao 12 da Norma COPPE (#150).
ABERTO: #150

O Manual UFRJ/SiBI chama esse sinal de travessao nas ilustracoes (2.10), nas
listas (3.1.2.2.4) e em apendices e anexos (3.1.4.3 e 3.1.4.4), embora os
exemplos dele misturem sinais. A Norma COPPE, secao 12, mostra
"APENDICE A -- Titulo" com travessao. A classe usa meia-risca (labelsep=endash,
\\textendash nos titulos e no sumario). Qual dos dois e decisao da issue; o
teste cobra so que TODOS usem o mesmo -- inclusive o exemplo da Norma.

Cobra-se que o sinal seja o mesmo em: legenda de figura, titulo de apendice,
entrada do apendice no sumario, e o exemplo da secao 12 de NORMA_COPPE_2026.md.
"""
import io
import os
import re
from medidas import Documento, relatar, compacta, RAIZ

TRACOS = "–—-"
CORPO = r"""
\chapter{Um}
\begin{figure}[h]\centering\caption{Legenda de prova}\rule{2cm}{1cm}\source{Elaboracao propria.}\end{figure}
\appendix
\chapter{Apendice de prova}
Texto.
"""


def sinal(texto, antes, depois):
    m = re.search(re.escape(antes) + r"\s*([" + TRACOS + r"])\s*" + re.escape(depois), texto)
    return m.group(1) if m else None


problemas = []
achados = {}
with Documento(pre=r"\tableofcontents", corpo=CORPO) as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    for pg in range(1, d.n_paginas() + 1):
        t = compacta(d.texto(pg))
        if "Legenda de prova" in t and "legenda" not in achados:
            achados["legenda"] = sinal(t, "Figura 1.1", "Legenda de prova")
        if "APÊNDICE A" in t and "APENDICE DE PROVA" in t:
            chave = "sumario" if "SUMÁRIO" in t else "titulo do apendice"
            achados.setdefault(chave, sinal(t, "APÊNDICE A", "APENDICE DE PROVA"))

norma = io.open(os.path.join(RAIZ, "NORMA_COPPE_2026.md"), encoding="utf-8").read()
m = re.search(r"## 12\..*?APÊNDICE A\s*([" + TRACOS + r"])", norma, re.S)
achados["Norma COPPE, secao 12"] = m.group(1) if m else None

for onde in ("legenda", "titulo do apendice", "sumario", "Norma COPPE, secao 12"):
    if achados.get(onde) is None:
        problemas.append("nao achei o sinal em: %s" % onde)
sinais = {k: v for k, v in achados.items() if v}
if len(set(sinais.values())) > 1:
    problemas.append("sinais diferentes: " + "; ".join(
        "%s: U+%04X" % (k, ord(v)) for k, v in sorted(sinais.items())))

relatar(problemas)
