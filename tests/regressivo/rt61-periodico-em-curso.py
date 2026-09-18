# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: (desconformidade, 4.3.5.5.1) a publicacao periodica ainda corrente, com data em aberto (date = {1950/}), saia "1950/." -- e o gabarito da propria classe registrava isso como divergencia ACEITA em tests/adversativa/referencias-manual.bib (#142).

A 4.3.5.5.1 do Manual UFRJ/SiBI: quando a publicacao e corrente, indica-se o ano
de inicio seguido de HIFEN, um espaco e ponto ("1950- ."). A classe troca o
\\bibdaterangesep por barra, para acertar o intervalo de meses ("jan./jun."), e o
mesmo separador valia para o intervalo aberto de anos. Da para distinguir os
dois casos: o intervalo aberto tem endyear definido e vazio.

Cobra-se: "REVISTA DE TESTE. Aracaju: Editora Exemplo, 1950- ." e nenhum "1950/".
"""
from medidas import Documento, relatar, compacta

BIB = r"""@periodical{rev,
  title = {Revista de Teste},
  location = {Aracaju},
  publisher = {Editora Exemplo},
  date = {1950/},
}
@article{art,
  author = {Silva, Ana},
  title = {Artigo com meses},
  journaltitle = {Revista de Teste},
  location = {Aracaju},
  volume = {2},
  number = {1},
  pages = {1-5},
  date = {2003-04/2003-06},
}
"""

problemas = []
with Documento(corpo=r"\chapter{Um}Texto.\nocite{*}\printbibliography", bib=BIB) as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    pg = d.pagina_com("Aracaju")
    texto = compacta(d.texto(pg))
    if "REVISTA DE TESTE. Aracaju: Editora Exemplo, 1950- ." not in texto:
        i = texto.find("REVISTA DE TESTE")
        problemas.append("esperava 'REVISTA DE TESTE. Aracaju: Editora Exemplo, 1950- .'; saiu %r"
                         % texto[i:i + 55])
    if "1950/" in texto:
        problemas.append("o intervalo aberto saiu com barra ('1950/')")
    # o intervalo de meses continua com barra
    if "abr./jun. 2003" not in texto:
        problemas.append("o intervalo de meses deixou de sair 'abr./jun. 2003'")

relatar(problemas)
