# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX. NAO roda na suite normal.

BUG: (desconformidade, 3.1.2.2.1 e 3.1.2.2.3) a dedicatoria saia num bloco de 60 mm encostado na margem direita, com o texto alinhado a direita -- o bloco comecava por volta de 13 cm da borda, e nao no meio da mancha (#123).
ABERTO: #123

A 2.6, a 3.1.2.2.1 e a 3.1.2.2.3 do Manual UFRJ/SiBI recomendam dedicatoria e
epigrafe digitadas com alinhamento do MEIO da mancha grafica ate a margem
direita, na parte inferior da folha. A mancha vai de 3 cm a 19 cm; o meio e 11 cm.
A classe usava um minipage de 60 mm na dedicatoria (a epigrafe ja usava meia
mancha, mas com o texto alinhado a direita).

Cobra-se, nas duas folhas:
  1. as linhas do texto comecam no meio da mancha (11 cm, 2 pt de tolerancia),
     exceto a linha da autoria da epigrafe;
  2. nada passa da margem direita;
  3. o texto esta na metade inferior da folha.
"""
from medidas import Documento, relatar, CENTRO_MANCHA, MARGEM_DIR, META_FOLHA

DEDIC = ("Dedico este trabalho a todas as pessoas que tornaram possivel cada "
         "etapa desta longa caminhada academica.")
EPIG = ("Uma citacao de epigrafe suficientemente longa para ocupar varias "
        "linhas no bloco que vai do meio da mancha ate a margem direita.")
PRE = r"""
\dedication{%s}
\epigrafe{%s}{Autor da Epigrafe}
""" % (DEDIC, EPIG)

problemas = []
with Documento(pre=PRE, corpo=r"\chapter{Um}Texto.") as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    for nome, trecho in (("dedicatoria", "Dedico este trabalho"),
                         ("epigrafe", "Uma citacao de epigrafe")):
        pg = d.pagina_com(trecho)
        if pg is None:
            problemas.append("nao achei a folha da %s" % nome)
            continue
        linhas = [ln for ln in d.linhas(pg)
                  if not (nome == "epigrafe" and ln[0].texto == "Autor")]
        if not linhas:
            problemas.append("%s: folha sem texto" % nome)
            continue
        for ln in linhas:
            if abs(ln[0].x0 - CENTRO_MANCHA) > 2.0:
                problemas.append("%s: a linha %r comeca em %.1f pt; o meio da mancha e "
                                 "%.1f pt" % (nome, " ".join(w.texto for w in ln[:3]),
                                              ln[0].x0, CENTRO_MANCHA))
                break
        if any(ln[-1].x1 > MARGEM_DIR + 0.8 for ln in linhas):
            problemas.append("%s: texto passa da margem direita" % nome)
        if linhas[0][0].y0 < META_FOLHA:
            problemas.append("%s: o texto nao esta na metade inferior da folha" % nome)

relatar(problemas)
