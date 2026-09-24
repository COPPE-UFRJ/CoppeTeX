# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: (desconformidade, 4.2) na ordem alfabetica da lista de referencias, o artigo inicial de uma entrada pelo titulo contava: "O PERFIL do engenheiro" ficava entre os sobrenomes com O, antes de OLIVEIRA (#141).

A 4.2 do Manual UFRJ/SiBI diz que "os artigos e palavras monossilabicas nao
sao considerados para efeito de alfabetacao" -- "O PERFIL" alfabeta por PERFIL,
e "NOS CANAVIAIS" por CANAVIAIS. O ufrj.bbx ordenava com sorting=nyt sobre o
titulo inteiro. A primeira correcao (17/09/2026) tirou so o artigo; o
monossilabo entrou em 18/09/2026, com a mesma lista de palavras que decide a
caixa alta da entrada e o corte do titulo na chamada (#138).

Cobra-se:
  1. a ordem das entradas na lista: NOS CANAVIAIS, CASTRO, NABUCO, OLIVEIRA,
     O PERFIL, QUINTANA;
  2. que a lista de palavras do \\clist_const do ufrj.bbx e a do mapa de
     sorttitle (\\regexp, que nao expande macro) sejam a mesma.
"""
import os
import re
from medidas import Documento, relatar, SRC

BIB = r"""@book{c,
  author = {Castro, Ana},
  title = {Livro de Castro},
  location = {Recife},
  publisher = {Editora Exemplo},
  year = {2000},
}
@book{n,
  author = {Nabuco, Ana},
  title = {Livro de Nabuco},
  location = {Recife},
  publisher = {Editora Exemplo},
  year = {2000},
}
@book{o,
  author = {Oliveira, Bia},
  title = {Livro de Oliveira},
  location = {Recife},
  publisher = {Editora Exemplo},
  year = {2000},
}
@book{p,
  title = {O perfil do engenheiro},
  location = {Recife},
  publisher = {Editora Exemplo},
  year = {2000},
}
@book{nos,
  title = {Nos canaviais, mutilações em vez de lazer e escola},
  location = {Recife},
  publisher = {Editora Exemplo},
  year = {2000},
}
@book{q,
  author = {Quintana, Caio},
  title = {Livro de Quintana},
  location = {Recife},
  publisher = {Editora Exemplo},
  year = {2000},
}
"""

ESPERADA = ["NOS CANAVIAIS", "CASTRO", "NABUCO", "OLIVEIRA", "O PERFIL", "QUINTANA"]

problemas = []

# 2. as duas listas do ufrj.bbx
bbx = open(os.path.join(SRC, "ufrj.bbx"), encoding="utf-8").read()
m1 = re.search(r"\\clist_const:Nn \\c_ufrj_naosignificativas_clist\s*\{(.*?)\}", bbx, re.S)
m2 = re.search(r"matchi=\\regexp\{\\A\(([^)]*)\)", bbx)
if not m1 or not m2:
    problemas.append("ufrj.bbx: nao achei a lista (%s) ou o mapa de sorttitle (%s)"
                     % (bool(m1), bool(m2)))
else:
    lista = [p.strip() for p in m1.group(1).split(",") if p.strip()]
    mapa = m2.group(1).split("|")
    if lista != mapa:
        problemas.append("ufrj.bbx: a lista de palavras nao significativas e o mapa de "
                         "sorttitle diferem: so na lista %s; so no mapa %s"
                         % (sorted(set(lista) - set(mapa)), sorted(set(mapa) - set(lista))))

# 1. a ordem da lista
with Documento(corpo=r"\chapter{Um}Texto.\nocite{*}\printbibliography", bib=BIB) as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    pg = d.pagina_com("NABUCO")
    texto = d.texto(pg)
    ordem = sorted((texto.find(s), s) for s in ESPERADA)
    saiu = [s for pos, s in ordem if pos >= 0]
    if saiu != ESPERADA:
        problemas.append("ordem da lista: esperava %s; saiu %s"
                         % (", ".join(ESPERADA), ", ".join(saiu)))

relatar(problemas)
