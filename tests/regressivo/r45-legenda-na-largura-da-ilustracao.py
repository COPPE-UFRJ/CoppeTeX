# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX. NAO roda na suite normal.

BUG: (desconformidade, 2.10) legenda e fonte de uma ilustracao estreita ocupavam a largura inteira da mancha, e nao havia na classe como limita-las a largura da ilustracao (#125).
ABERTO: #125

A 2.10 do Manual UFRJ/SiBI pede que tipo, numero de ordem, titulo, fonte,
legenda e notas respeitem as margens da ILUSTRACAO. Como a legenda vem antes do
conteudo, a classe nao sabe a largura dele na hora de compor a legenda; a
correcao proposta e um comando que o autor da no inicio do flutuante com a
largura da ilustracao, e que vale para a legenda e para o \\source:

    \\begin{figure}
      \\illustrationwidth{4cm}      % sinonimo em portugues: \\largurailustracao
      \\caption{...}
      \\includegraphics[width=4cm]{...}
      \\source{...}
    \\end{figure}

(O NOME do comando e proposta da issue; se mudar, mude aqui.)

Cobra-se: com \\illustrationwidth{4cm}, todas as linhas da legenda e da fonte
ficam dentro dos 4 cm centralizados da ilustracao (1 pt de tolerancia).
"""
from medidas import Documento, relatar, cm, CENTRO_MANCHA

CORPO = r"""
\chapter{Um}
Texto.
\begin{figure}[h]
\centering
\illustrationwidth{4cm}
\caption{Uma legenda propositalmente muito mais longa do que a largura da ilustracao}
\rule{4cm}{2cm}
\source{Uma fonte tambem mais longa do que a propria ilustracao estreita.}
\end{figure}
"""

problemas = []
with Documento(corpo=CORPO) as d:
    if not d.ok:
        relatar(["nao compilou (o comando \\illustrationwidth existe?): %s"
                 % d.erros_do_log()])
    pg = d.pagina_com("Uma legenda propositalmente")
    esq, dir_ = CENTRO_MANCHA - cm(2.0), CENTRO_MANCHA + cm(2.0)
    for ln in d.linhas(pg):
        t = " ".join(w.texto for w in ln)
        if any(p in t for p in ("Figura", "legenda", "ilustracao", "Fonte:", "fonte",
                                "estreita", "propria")):
            if ln[0].x0 < esq - 1.0 or ln[-1].x1 > dir_ + 1.0:
                problemas.append("linha %r vai de %.1f a %.1f pt; a ilustracao, de %.1f a %.1f pt"
                                 % (t[:50], ln[0].x0, ln[-1].x1, esq, dir_))

relatar(problemas)
