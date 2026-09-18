# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: (desconformidade, 4.2.9 e 4.3.4) no filme, a direcao saia "Direcao de Sales Junior, Walter" -- nome invertido --, e no jogo eletronico a versao saia no FIM, depois da imprenta (#143).

Os exemplos da 4.2.9 do Manual UFRJ/SiBI escrevem "Direcao: Nome Sobrenome", em
ordem direta. A 4.3.4 diz que a versao de documento eletronico equivale a edicao
e e transcrita como consta -- portanto no lugar da edicao, antes da imprenta. O
ufrj:media do ufrj.bbx usa a string "Direcao de" e imprime os nomes como
lista crua (\\printlist), e o ufrj:mediadriver imprime a versao depois da
imprenta.

Cobra-se:
  1. "Direcao: Walter Sales Junior." e nenhum "Sales Junior, Walter";
  2. "Versao 2.1. Campinas: Editora Jogo, 2019." (versao antes da imprenta).
"""
from medidas import Documento, relatar, normaliza, entrada

BIB = r"""@movie{filme,
  title = {Um filme de teste},
  director = {Sales Júnior, Walter},
  location = {[S. l.]},
  publisher = {Produtora Exemplo},
  year = {1998},
}
@videogame{jogo,
  author = {Ramos, Tiago},
  title = {Jogo de teste},
  version = {2.1},
  location = {Campinas},
  publisher = {Editora Jogo},
  year = {2019},
}
"""

problemas = []
with Documento(corpo=r"\chapter{Um}Texto.\nocite{*}\printbibliography", bib=BIB) as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    pg = d.pagina_com("Sales")
    texto = d.texto(pg)
    filme = entrada(texto, "UM FILME")
    if "direcao: walter sales junior." not in normaliza(filme):
        problemas.append("filme: esperava 'Direcao: Walter Sales Junior.'; saiu %r" % filme)
    if "sales junior, walter" in normaliza(filme):
        problemas.append("filme: o diretor saiu com o nome invertido: %r" % filme)
    jogo = entrada(texto, "RAMOS")
    if normaliza("Versão 2.1. Campinas: Editora Jogo, 2019.") not in normaliza(jogo):
        problemas.append("jogo: esperava a versao antes da imprenta ('Versao 2.1. Campinas: "
                         "Editora Jogo, 2019.'); saiu %r" % jogo)

relatar(problemas)
