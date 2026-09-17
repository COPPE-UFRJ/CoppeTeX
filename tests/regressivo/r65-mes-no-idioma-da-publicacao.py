# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX. NAO roda na suite normal.

BUG: (desconformidade, 4.3.5.5.1) o mes da publicacao saia sempre abreviado no idioma do TRABALHO: um artigo de periodico em ingles de setembro saia "set. 2021" (#146).
ABERTO: #146

A 4.3.5.5.1 do Manual UFRJ/SiBI manda abreviar os meses no idioma ORIGINAL da
publicacao (Anexo A da NBR 6023), e o exemplo da 4.3.2.2 traz "Sept. 2021" num
artigo em ingles. O biblatex usa as strings de mes do idioma do documento; o
campo langid da entrada existe para isso, mas so as datas devem mudar de idioma
-- "Disponivel em" e "Acesso em" continuam no idioma do trabalho.

Cobra-se, com langid = {english}: "Sept. 2021" (e nao "set. 2021"), e que
"Acesso em:" continue em portugues.
"""
from medidas import Documento, relatar, compacta, entrada

BIB = r"""@article{mes,
  author = {Evans, Sam},
  title = {An article about tests},
  journaltitle = {Journal of Tests},
  location = {Oxford},
  volume = {1},
  number = {2},
  pages = {1-2},
  date = {2021-09},
  langid = {english},
  url = {http://exemplo.org},
  urldate = {2022-03-30},
}
"""

problemas = []
with Documento(corpo=r"\chapter{Um}Texto.\nocite{*}\printbibliography", bib=BIB) as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    pg = d.pagina_com("Evans")
    ref = compacta(entrada(d.texto(pg), "EVANS"))
    if "Sept. 2021" not in ref:
        problemas.append("esperava 'Sept. 2021' (mes no idioma da publicacao); saiu %r" % ref)
    if "Acesso em:" not in ref:
        problemas.append("'Acesso em:' deixou de sair em portugues: %r" % ref)

relatar(problemas)
