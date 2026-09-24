# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: (desconformidade, 2.6) as folhas de resumo e de abstract nao tinham TITULO: abriam direto na frase "Resumo da Tese apresentada a COPPE/UFRJ...", alinhada a esquerda (#114).

A 2.6 do Manual UFRJ/SiBI lista o resumo entre os titulos sem indicativo
numerico, que sao CENTRALIZADOS -- a mesma lista de agradecimentos, sumario e
referencias. A frase de abertura da COPPE pode continuar (Norma COPPE, secoes 6
a 8), mas abaixo de um titulo "RESUMO"; o resumo em lingua estrangeira leva o
titulo na lingua dele ("ABSTRACT").

Cobra-se, na folha de cada resumo: um pedaco de texto que e exatamente o
titulo, em caixa alta, centralizado na mancha (entre 3 cm e 19 cm).
"""
from medidas import Documento, relatar, CENTRO_MANCHA

PRE = r"""
\begin{abstract}Texto corrido do resumo em portugues.\end{abstract}
\begin{foreignabstract}Running text of the foreign abstract.\end{foreignabstract}
"""

problemas = []
with Documento(pre=PRE, corpo=r"\chapter{Um}Texto.") as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    for trecho, titulo in (("Texto corrido do resumo em portugues", "RESUMO"),
                           ("Running text of the foreign abstract", "ABSTRACT")):
        pg = d.pagina_com(trecho)
        if pg is None:
            problemas.append("nao achei a folha do %s" % titulo.lower())
            continue
        cands = [f for f in d.fragmentos(pg) if f.texto.strip() == titulo]
        if not cands:
            problemas.append("folha %d (%s): nao ha titulo %r; a folha abre com %r"
                             % (pg, titulo.lower(), titulo,
                                d.fragmentos(pg)[0].texto if d.fragmentos(pg) else ""))
            continue
        f = cands[0]
        centro = f.esq + f.larg / 2.0
        if abs(centro - CENTRO_MANCHA) > 3.0:
            problemas.append("folha %d: o titulo %r nao esta centralizado "
                             "(centro em %.1f pt, a mancha em %.1f pt)"
                             % (pg, titulo, centro, CENTRO_MANCHA))

relatar(problemas)
