# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: (desconformidade, 2.2b e 2.6) os titulos saiam em corpo MAIOR que o do texto: capitulo e titulos sem indicativo em \\Large (17,28 pt), secao em \\large (14,4 pt), e os dois titulos da folha adicional em \\large (#113).

A 2.2(b) do Manual UFRJ/SiBI fixa fonte tamanho 12 para o trabalho e so admite
corpo MENOR, e uniforme, para citacao longa, nota de rodape, paginacao e
legendas. A 2.6 lista os recursos do destaque gradativo dos titulos -- negrito,
italico ou grifo, redondo, caixa-alta ou versal --, e tamanho nao e um deles. O
proprio Manual compoe todos os titulos em corpo 12.

Cobra-se, no PDF, que nenhum destes saia acima de 12 pt: titulo de capitulo, de
secao e de subsecao, titulo sem indicativo (Agradecimentos, Sumario), titulo de
apendice e os dois titulos da folha adicional.
"""
from medidas import Documento, relatar, normaliza

PRE = r"""
\chapter*{Agradecimentos}
Texto dos agradecimentos.
\begin{abstract}Resumo.\end{abstract}
\tableofcontents
"""
CORPO = r"""
\chapter{Capitulo primario}
Texto.
\section{Secao secundaria}
Texto.
\subsection{Secao terciaria}
Texto.
\appendix
\chapter{Um apendice}
Texto.
"""
ALVOS = [
    ("Informacoes Coleta CAPES", "titulo da folha adicional"),
    ("Ficha catalografica", "titulo da ficha, na folha adicional"),
    ("AGRADECIMENTOS", "titulo sem indicativo (Agradecimentos)"),
    ("SUMARIO", "titulo do sumario"),
    ("CAPITULO PRIMARIO", "titulo de capitulo"),
    ("SECAO SECUNDARIA", "titulo de secao"),
    ("Secao terciaria", "titulo de subsecao"),
    ("UM APENDICE", "titulo de apendice"),
]

problemas = []
with Documento(pre=PRE, corpo=CORPO) as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    maiores = {}
    for pg in range(1, d.n_paginas() + 1):
        for f in d.fragmentos(pg):
            t = normaliza(f.texto)
            for chave, _ in ALVOS:
                # termina com o titulo: pega "1 CAPITULO PRIMARIO" e deixa de
                # fora a linha do sumario, que traz o pontilhado e o numero
                if t.endswith(normaliza(chave)):
                    if chave not in maiores or f.corpo > maiores[chave][1].corpo:
                        maiores[chave] = (pg, f)
    for chave, descricao in ALVOS:
        if chave not in maiores:
            problemas.append("nao achei o %s no PDF" % descricao)
            continue
        pg, f = maiores[chave]
        if f.corpo > 12.5:
            problemas.append("%s em corpo %.1f pt na folha %d (o Manual pede 12): %r"
                             % (descricao, f.corpo, pg, f.texto))

relatar(problemas)
