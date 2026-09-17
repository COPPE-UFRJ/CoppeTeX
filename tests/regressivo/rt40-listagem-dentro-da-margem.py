# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: (desconformidade, 2.3) nas listagens de codigo com numeracao de linha (ambientes python, java, xml, html e prolog da classe), os numeros das linhas saiam DENTRO da margem esquerda, a cerca de 2,6 cm da borda (#120).

A 2.3 do Manual UFRJ/SiBI fixa a margem esquerda em 3 cm. O listings poe o
numero da linha a esquerda do codigo, a `numbersep' dele, e sem `xleftmargin'
o numero invade a margem.

Cobra-se, na folha da listagem, que nenhum texto comece antes de 3 cm.
"""
from medidas import Documento, relatar, MARGEM_ESQ

CORPO = r"""
\chapter{Um}
Texto antes da listagem.
\begin{python}[caption={Uma listagem numerada}]
def soma(a, b):
    return a + b
\end{python}
\source{Elaboracao propria.}
"""

problemas = []
with Documento(corpo=CORPO) as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    pg = d.pagina_com("Uma listagem numerada")
    fora = [w for w in d.palavras(pg) if w.x0 < MARGEM_ESQ - 1.0]
    if fora:
        problemas.append("texto dentro da margem esquerda (3 cm = %.1f pt): %s"
                         % (MARGEM_ESQ, ", ".join("%r em %.1f pt" % (w.texto, w.x0)
                                                  for w in fora[:6])))

relatar(problemas)
