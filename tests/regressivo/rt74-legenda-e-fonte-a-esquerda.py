# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: (exemplo do Manual, 2.10 e Figura 1) a legenda e a fonte das ilustracoes saiam CENTRALIZADAS, e o unico exemplo do Manual -- a Figura 1 -- as alinha a esquerda, na margem da ilustracao; a Norma COPPE §11 mandava centralizar a fonte (#160).

A 2.10 do Manual UFRJ/SiBI nao fixa o alinhamento, e diz que "tipo, numero de
ordem, titulo, fonte, legenda e notas devem respeitar as margens da
ilustracao". Onde o texto nao decide, vale o exemplo: na Figura 1 (secao 3), a
identificacao "Figura 1 - Estrutura do Trabalho Academico" e a fonte "Adaptada
de: ..." comecam na margem esquerda da ilustracao.

Cobra-se, medindo a caixa de cada palavra (pdftotext -bbox):
  1. sem \\illustrationwidth, legenda curta e fonte comecam na margem esquerda
     da mancha, a 3 cm da borda -- e nao centralizadas;
  2. com \\illustrationwidth{6cm} e a ilustracao centrada, legenda e fonte
     comecam na margem esquerda da ILUSTRACAO: a 3 cm + (16 cm - 6 cm)/2 = 8 cm
     da borda.
"""
from medidas import Documento, relatar

CM = 72.0 / 2.54   # 1 cm em pontos PostScript, a unidade do pdftotext -bbox
TOL = 3.0

CORPO = r"""\chapter{Um}
Texto antes.
\begin{figure}[h]
  \centering
  \caption{Curta}
  \rule{12cm}{1cm}
  \source{Primeira fonte.}
\end{figure}
\begin{figure}[h]
  \centering
  \illustrationwidth{6cm}
  \caption{Estreita}
  \rule{6cm}{1cm}
  \source{Segunda fonte.}
\end{figure}
Texto depois.
"""


problemas = []
with Documento(corpo=CORPO) as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    pg = d.pagina_com("Curta")
    margem = 3 * CM
    estreita = (3 + (16 - 6) / 2.0) * CM
    for palavra, esperado, caso in (("Curta", margem, "legenda sem largura"),
                                    ("Primeira", margem, "fonte sem largura"),
                                    ("Estreita", estreita, "legenda de 6 cm"),
                                    ("Segunda", estreita, "fonte de 6 cm")):
        # a palavra da legenda vem depois de "Figura 1.1 --"; mede-se o comeco
        # da LINHA: a primeira palavra dela, "Figura" ou "Fonte:"
        linhas = d.linhas(pg)
        x = None
        for linha in linhas:
            if any(p.texto.startswith(palavra) for p in linha):
                x = min(p.x0 for p in linha)
                break
        if x is None:
            problemas.append("%s: nao achei a linha com %r" % (caso, palavra))
        elif abs(x - esperado) > TOL:
            problemas.append("%s: a linha comeca a %.1f pt da borda; esperava %.1f pt "
                             "(alinhada a esquerda, na margem %s)"
                             % (caso, x, esperado,
                                "da mancha" if esperado == margem else "da ilustracao"))

relatar(problemas)
