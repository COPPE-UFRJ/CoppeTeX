# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX. NAO roda na suite normal.

BUG: (desconformidade, 4.2) a lista de referencias saia JUSTIFICADA e com palavras hifenizadas no fim da linha: toda linha que nao era a ultima de uma entrada terminava exatamente na margem direita (#118).
ABERTO: #118

A 4.2 do Manual UFRJ/SiBI diz que as referencias sao alinhadas somente a margem
esquerda, e pede expressamente que nao se use o recurso de justificar. O
ambiente de bibliografia do biblatex justifica por padrao, e nada na classe o
desligava.

Cobra-se, em entradas que ocupam mais de uma linha:
  1. as linhas que nao sao as ultimas NAO terminam todas na margem direita;
  2. nenhuma linha termina com palavra partida por hifenizacao.
"""
import re
from medidas import Documento, relatar, MARGEM_DIR

BIB = r"""@book{a,
  author = {Almeida, Joaquim Pedro de and Barbosa, Maria Aparecida and Cavalcanti, Heloisa},
  title = {Comportamento experimental de estruturas submetidas a carregamentos extraordinariamente prolongados},
  location = {Rio de Janeiro},
  publisher = {Editora Universitaria Interdisciplinar},
  year = {2010},
}
@book{b,
  author = {Bittencourt, Anastacio},
  title = {Consideracoes metodologicas sobre levantamentos bibliograficos interdisciplinares em engenharia},
  location = {Sao Paulo},
  publisher = {Editora Tecnica Especializada},
  year = {2015},
  pagetotal = {321},
}
@book{c,
  author = {Carvalho, Bartolomeu},
  title = {Instrumentacao computacional contemporanea para monitoramento estrutural permanente},
  location = {Belo Horizonte},
  publisher = {Editora Universitaria Interdisciplinar},
  year = {2018},
}
"""

problemas = []
with Documento(corpo=r"\chapter{Um}Texto.\nocite{*}\printbibliography", bib=BIB) as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    pg = d.pagina_com("Bittencourt")
    linhas = [ln for ln in d.linhas(pg) if ln[0].y0 > 120]
    # agrupa linhas em entradas: uma entrada comeca por SOBRENOME em caixa alta
    entradas = []
    for ln in linhas:
        if re.match(r"^[A-ZÁÉÍÓÚÂÊÔÃÕÇ]{3,},$", ln[0].texto):
            entradas.append([ln])
        elif entradas:
            entradas[-1].append(ln)
    if len(entradas) < 3:
        relatar(["esperava 3 entradas; achei %d" % len(entradas)])
    naoultimas = [ln for e in entradas for ln in e[:-1]]
    if not naoultimas:
        relatar(["as entradas deviam ter mais de uma linha"])
    na_margem = [ln for ln in naoultimas if abs(ln[-1].x1 - MARGEM_DIR) < 0.8]
    if len(na_margem) == len(naoultimas):
        problemas.append("as %d linhas nao finais terminam todas na margem direita "
                         "(%.1f pt): a lista esta justificada" % (len(naoultimas), MARGEM_DIR))
    partidas = [ln[-1].texto for ln in naoultimas
                if ln[-1].texto.endswith("-") and len(ln[-1].texto) > 2]
    if partidas:
        problemas.append("palavras partidas no fim da linha: %s" % ", ".join(partidas))

relatar(problemas)
