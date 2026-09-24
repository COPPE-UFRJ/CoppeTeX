# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: (desconformidade, 4.2.3.4) o intervalo de paginas saia com MEIA-RISCA ("p. 37–44"), e o Manual usa hifen ("p. 37-44") (#145).

A 4.2.3.4 do Manual UFRJ/SiBI diz que o hifen assinala a pagina inicial e a
final das partes de documentos, e todos os exemplos de referencia do Manual
usam hifen. O biblatex compoe o intervalo com \\bibrangedash (meia-risca), que o
ufrj.bbx nao redefine.

Cobra-se, com o traco exato (sem normalizar): "p. 37-44" com hifen ASCII, e
nenhuma meia-risca (U+2013) na referencia.
"""
from medidas import Documento, relatar, compacta, entrada

BIB = r"""@article{pag,
  author = {Dias, Rita},
  title = {Artigo paginado},
  journaltitle = {Revista de Teste},
  location = {Manaus},
  volume = {20},
  number = {1},
  pages = {37--44},
  year = {1991},
}
"""

problemas = []
with Documento(corpo=r"\chapter{Um}Texto.\nocite{*}\printbibliography", bib=BIB) as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    pg = d.pagina_com("Dias")
    ref = compacta(entrada(d.texto(pg), "DIAS"))
    if "p. 37-44" not in ref or "–" in ref:
        problemas.append("esperava 'p. 37-44' com hifen; saiu %r" % ref)

relatar(problemas)
