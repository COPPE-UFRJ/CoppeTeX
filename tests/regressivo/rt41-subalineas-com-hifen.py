# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: (desconformidade, 2.6) no ambiente alineas, a subalinea saia marcada com MEIA-RISCA, e o marcador ficava a direita da primeira letra do texto da alinea, e nao embaixo dela (#121).

A 2.6 do Manual UFRJ/SiBI pede a subalinea caracterizada apenas pelo HIFEN,
colocado sob a primeira letra do texto da alinea correspondente e separado do
texto da subalinea por um espaco. A classe declarava o segundo nivel com
label=-- (meia-risca) e leftmargin=1.8em, o que desloca o marcador.

Cobra-se:
  1. o marcador da subalinea e o hifen ASCII (U+002D);
  2. a borda esquerda do marcador coincide com a da primeira letra do texto da
     alinea que a contem (1,5 pt de tolerancia);
  3. entre o marcador e o texto da subalinea ha um espaco, e nao mais (ate 7 pt).
"""
from medidas import Documento, relatar

CORPO = r"""
\chapter{Um}
A frase que introduz as alineas termina por dois pontos:
\begin{alineas}
\item primeira alinea;
\item segunda alinea, que tem subalineas:
  \begin{alineas}
  \item subalinea um,
  \item subalinea dois;
  \end{alineas}
\item terceira alinea.
\end{alineas}
"""

problemas = []
with Documento(corpo=CORPO) as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    pg = d.pagina_com("subalinea um")
    linhas = d.linhas(pg)
    pai = [ln for ln in linhas if [w.texto for w in ln[:2]] == ["b)", "segunda"]]
    filha = [ln for ln in linhas if "subalinea" in [w.texto for w in ln]
             and "um," in [w.texto for w in ln]]
    if not pai or not filha:
        relatar(["nao achei a alinea b) ou a subalinea: %r"
                 % [" ".join(w.texto for w in ln) for ln in linhas[:12]]])
    texto_pai = pai[0][1]
    marcador = filha[0][0]
    if marcador.texto != "-":
        problemas.append("o marcador da subalinea e %r (U+%04X); a 2.6 pede o hifen"
                         % (marcador.texto, ord(marcador.texto[0])))
    if abs(marcador.x0 - texto_pai.x0) > 1.5:
        problemas.append("o marcador da subalinea comeca em %.1f pt; a primeira letra do "
                         "texto da alinea, em %.1f pt" % (marcador.x0, texto_pai.x0))
    # "dele separada por um espaco": o vao entre o hifen e o texto e um espaco
    # entre palavras (3 a 4 pt em corpo 12), e nao uma coluna de rotulo
    vao = filha[0][1].x0 - marcador.x1
    if vao > 7.0:
        problemas.append("entre o marcador e o texto da subalinea ha %.1f pt; a 2.6 pede um "
                         "espaco (ate 7 pt)" % vao)

relatar(problemas)
