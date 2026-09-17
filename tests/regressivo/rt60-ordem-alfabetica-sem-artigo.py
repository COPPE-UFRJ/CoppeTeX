# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX. NAO roda na suite normal.

BUG: (desconformidade, 4.2) na ordem alfabetica da lista de referencias, o artigo inicial de uma entrada pelo titulo contava: "O PERFIL do engenheiro" ficava entre os sobrenomes com O, antes de OLIVEIRA (#141).
ABERTO: #141

A 4.2 do Manual UFRJ/SiBI diz que artigos e palavras monossilabicas nao sao
considerados para efeito de alfabetacao -- "O PERFIL" alfabeta por PERFIL. O
ufrj.bbx ordena com sorting=nyt sobre o titulo inteiro.

Cobra-se a ordem das entradas na lista: NABUCO, OLIVEIRA, O PERFIL, QUINTANA.
"""
from medidas import Documento, relatar

BIB = r"""@book{n,
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
@book{q,
  author = {Quintana, Caio},
  title = {Livro de Quintana},
  location = {Recife},
  publisher = {Editora Exemplo},
  year = {2000},
}
"""

problemas = []
with Documento(corpo=r"\chapter{Um}Texto.\nocite{*}\printbibliography", bib=BIB) as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    pg = d.pagina_com("Nabuco")
    texto = d.texto(pg)
    ordem = sorted((texto.find(s), s) for s in ("NABUCO", "OLIVEIRA", "O PERFIL", "QUINTANA"))
    saiu = [s for pos, s in ordem if pos >= 0]
    if saiu != ["NABUCO", "OLIVEIRA", "O PERFIL", "QUINTANA"]:
        problemas.append("ordem da lista: esperava NABUCO, OLIVEIRA, O PERFIL, QUINTANA; saiu %s"
                         % ", ".join(saiu))

relatar(problemas)
