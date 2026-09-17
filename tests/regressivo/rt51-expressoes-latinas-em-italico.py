# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX. NAO roda na suite normal.

BUG: (desconformidade, 4.2.1.3c e 4.1.2.2) nas referencias, "In:", "et al.", "S. l." e "s. n." saiam em redondo (#132).
ABERTO: #132

A 4.2.1.3(c) do Manual UFRJ/SiBI pede a expressao "In:" em italico; a 4.1.2.2
pede em italico todas as expressoes latinas e suas abreviaturas; e os exemplos
do Manual compoem "et al.", "[S. l.]" e "[s. n.]" em italico. O ufrj.bbx
redefine a macro in: sem enfase, a bibstring andothers vem sem enfase do
brazilian.lbx, e o que o autor digita no campo location/publisher sai como
digitou.

Cobra-se, na lista de referencias, que cada uma destas saia em fonte italica
(o colchete e a pontuacao podem ficar em redondo): In, et al., S. l., s. n.
"""
from medidas import Documento, relatar

BIB = r"""@incollection{inc,
  author = {Pereira, Joana},
  title = {Um capítulo de teste},
  booktitle = {Livro coletivo},
  editor = {Ramos, Tiago},
  location = {Salvador},
  publisher = {Editora Exemplo},
  year = {2015},
  pages = {10-20},
}
@article{etal,
  author = {Lima, Ana and others},
  title = {Um artigo de teste},
  journaltitle = {Revista de Teste},
  location = {Manaus},
  volume = {3},
  number = {2},
  pages = {5-9},
  year = {2019},
}
@book{sl,
  author = {Nunes, Pedro},
  title = {Livro sem local nem editora},
  location = {[S. l.]},
  publisher = {[s. n.]},
  year = {1990},
}
"""

problemas = []
with Documento(corpo=r"\chapter{Um}Texto.\nocite{*}\printbibliography", bib=BIB) as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    pg = d.pagina_com("Pereira")
    frags = d.fragmentos(pg)
    italicos = [f.texto.strip() for f in frags if f.italico]
    for alvo in ("In", "et al", "S. l", "s. n"):
        if not any(alvo in t for t in italicos):
            onde = [f.texto for f in frags if alvo in f.texto]
            problemas.append("%r nao saiu em italico (esta em %r)" % (alvo, onde[:1]))

relatar(problemas)
