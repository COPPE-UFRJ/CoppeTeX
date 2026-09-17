# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX. NAO roda na suite normal.

BUG: (desconformidade, 4.3.4, 4.3.6.1 e 4.3.7) no livro (e no relatorio), o campo edition numerico saia como ordinal ("3ª ed."), volumes saia como "2 vol." ANTES da imprenta, e a serie saia antes da imprenta, sem parenteses e sem virgula antes do numero (#133).
ABERTO: #133

Pelo Manual UFRJ/SiBI: a edicao e o numero seguido de ponto e da abreviatura
("3. ed.", 4.3.4); o numero de volumes vai na descricao fisica, depois da
imprenta, com a abreviatura "v." (4.2.1.1 e 4.3.6.1); a serie vai no fim, entre
parenteses, com virgula antes da numeracao (4.2.1.1d e 4.3.7). O ufrj.bbx nao
redefine os drivers book e report: valem os do biblatex padrao, e o formato de
edicao do brazilian.lbx.

Cobra-se, no texto das referencias:
  1. "ROCHA, Beatriz. Livro com edicao. 3. ed. Curitiba: Editora Exemplo, 2001."
  2. "TEIXEIRA, Caio. Obra em volumes. Belem: Editora Exemplo, 1999. 2 v."
  3. "VIEIRA, Denise. Livro de colecao. Goiania: Editora Exemplo, 2005. 120 p. (Colecao Teste, 7)."
  4. "XAVIER, Elias. Relatorio de colecao. Natal: Instituto Exemplo, 2007. 30 p. (Relatorios Tecnicos, 12)."
"""
from medidas import Documento, relatar, normaliza, entrada

BIB = r"""@book{ed,
  author = {Rocha, Beatriz},
  title = {Livro com edição},
  edition = {3},
  location = {Curitiba},
  publisher = {Editora Exemplo},
  year = {2001},
}
@book{vol,
  author = {Teixeira, Caio},
  title = {Obra em volumes},
  location = {Belém},
  publisher = {Editora Exemplo},
  year = {1999},
  volumes = {2},
}
@book{ser,
  author = {Vieira, Denise},
  title = {Livro de coleção},
  location = {Goiânia},
  publisher = {Editora Exemplo},
  year = {2005},
  pagetotal = {120},
  series = {Coleção Teste},
  number = {7},
}
@report{rel,
  author = {Xavier, Elias},
  title = {Relatório de coleção},
  institution = {Instituto Exemplo},
  location = {Natal},
  year = {2007},
  pagetotal = {30},
  series = {Relatórios Técnicos},
  number = {12},
}
"""
ESPERADOS = [
    "ROCHA, Beatriz. Livro com edição. 3. ed. Curitiba: Editora Exemplo, 2001.",
    "TEIXEIRA, Caio. Obra em volumes. Belém: Editora Exemplo, 1999. 2 v.",
    "VIEIRA, Denise. Livro de coleção. Goiânia: Editora Exemplo, 2005. 120 p. (Coleção Teste, 7).",
    "XAVIER, Elias. Relatório de coleção. Natal: Instituto Exemplo, 2007. 30 p. (Relatórios Técnicos, 12).",
]

problemas = []
with Documento(corpo=r"\chapter{Um}Texto.\nocite{*}\printbibliography", bib=BIB) as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    pg = d.pagina_com("Rocha")
    texto = d.texto(pg)
    alvo = normaliza(texto)
    for esperado in ESPERADOS:
        if normaliza(esperado) not in alvo:
            sobrenome = esperado.split(",")[0]
            problemas.append("esperava %r\n        saiu     %r" % (esperado, entrada(texto, sobrenome)))

relatar(problemas)
