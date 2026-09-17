# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX. NAO roda na suite normal.

BUG: (desconformidade, 3.1.2.1.6 e Norma COPPE 14) no sumario, Referencias, Apendices, Anexos e Indice comecavam na MARGEM ESQUERDA, e nao na coluna em que comecam os titulos das secoes numeradas (#115).
ABERTO: #115

A 3.1.2.1.6 do Manual UFRJ/SiBI recomenda alinhar os titulos pela margem do
titulo do indicativo mais extenso, e diz que isso vale inclusive para os
elementos pos-textuais -- e o sumario do proprio Manual faz assim. A Norma COPPE
(secao 14) transformou a recomendacao em regra: todo titulo comeca numa mesma
coluna. Na classe, as entradas sem \\numberline caiam na margem.

Cobra-se, na folha do sumario: a borda esquerda de REFERENCIAS, APENDICE A,
ANEXO A e INDICE e a mesma da de um titulo numerado (INTRODUCAO), com 1,5 pt de
tolerancia.
"""
from medidas import Documento, relatar, normaliza

BIB = r"""@book{livro,
  author = {Autor, Primeiro},
  title = {Um livro qualquer},
  location = {Rio de Janeiro},
  publisher = {Editora},
  year = {2001},
}
"""
PRE = r"\tableofcontents"
CORPO = r"""
\chapter{Introducao}
Texto \cite{livro}.\index{termo}
\printbibliography
\appendix
\chapter{Primeiro apendice}
Texto.
\annex
\chapter{Primeiro anexo}
Texto.
\printindex
"""

problemas = []
with Documento(pacotes=r"\usepackage{makeidx}\makeindex", pre=PRE, corpo=CORPO,
               bib=BIB, makeindex=True, passadas=3) as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    pg = None
    for i in range(1, d.n_paginas() + 1):
        if any(f.texto.strip().upper() in ("SUMÁRIO", "SUMARIO") for f in d.fragmentos(i)):
            pg = i
            break
    if pg is None:
        relatar(["nao achei o sumario"])

    def borda(prefixo):
        for linha in d.linhas(pg):
            # a linha comeca pelo indicativo (numero) ou direto pelo titulo
            palavras = [w for w in linha if normaliza(w.texto) not in ("",)]
            for j, w in enumerate(palavras):
                if normaliza(w.texto).startswith(normaliza(prefixo)):
                    return w.x0
        return None

    coluna = borda("INTRODUCAO")
    if coluna is None:
        relatar(["nao achei INTRODUCAO no sumario"])
    for alvo in ("REFERENCIAS", "APENDICE", "ANEXO", "INDICE"):
        x = borda(alvo)
        if x is None:
            problemas.append("nao achei %s no sumario" % alvo)
        elif abs(x - coluna) > 1.5:
            problemas.append("%s comeca em %.1f pt; os titulos numerados, em %.1f pt"
                             % (alvo, x, coluna))

relatar(problemas)
