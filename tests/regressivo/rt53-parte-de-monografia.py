# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: (desconformidade, 4.2.1.3) na parte de monografia (incollection, inbook), o autor do livro (bookauthor) e o subtitulo do livro (booksubtitle) SUMIAM, e o capitulo saia depois das paginas e separado da data por virgula ("1996. p. 23-64, cap. 1"; "1994, cap. 3") (#134).

A 4.2.1.3 do Manual UFRJ/SiBI pede, depois de "In:", a referencia completa da
monografia -- autor, titulo e subtitulo --, repetindo o autor quando e o mesmo
da parte; e os exemplos trazem "cap. 1, p. 23-64", com o capitulo antes das
paginas, depois de ponto. O driver ufrj:partdriver imprime so editor e
booktitle, e poe chapter depois de pages.

Cobra-se, no texto das referencias:
  1. "QUEIROZ, Fabio. O capitulo do autor. In: QUEIROZ, Fabio. O livro do mesmo autor. Maceio: Editora Exemplo, 1994. cap. 3."
  2. "BARROS, Gilda. Um capitulo com paginas. In: CAMPOS, Hugo (org.). Coletanea de estudos: volume comemorativo. Vitoria: Editora Exemplo, 1996. cap. 1, p. 23-64."
"""
from medidas import Documento, relatar, normaliza, entrada

BIB = r"""@incollection{cap1,
  author = {Queiroz, Fábio},
  title = {O capítulo do autor},
  bookauthor = {Queiroz, Fábio},
  booktitle = {O livro do mesmo autor},
  location = {Maceió},
  publisher = {Editora Exemplo},
  year = {1994},
  chapter = {3},
}
@incollection{cap2,
  author = {Barros, Gilda},
  title = {Um capítulo com páginas},
  editor = {Campos, Hugo},
  booktitle = {Coletânea de estudos},
  booksubtitle = {volume comemorativo},
  location = {Vitória},
  publisher = {Editora Exemplo},
  year = {1996},
  chapter = {1},
  pages = {23-64},
}
"""
ESPERADOS = [
    "QUEIROZ, Fábio. O capítulo do autor. In: QUEIROZ, Fábio. O livro do mesmo autor. Maceió: Editora Exemplo, 1994. cap. 3.",
    "BARROS, Gilda. Um capítulo com páginas. In: CAMPOS, Hugo (org.). Coletânea de estudos: volume comemorativo. Vitória: Editora Exemplo, 1996. cap. 1, p. 23-64.",
]

problemas = []
with Documento(corpo=r"\chapter{Um}Texto.\nocite{*}\printbibliography", bib=BIB) as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    pg = d.pagina_com("Queiroz")
    texto = d.texto(pg)
    for esperado in ESPERADOS:
        if normaliza(esperado) not in normaliza(texto):
            sobrenome = esperado.split(",")[0]
            problemas.append("esperava %r\n        saiu     %r" % (esperado, entrada(texto, sobrenome)))

relatar(problemas)
