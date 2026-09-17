# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX. NAO roda na suite normal.

BUG: (desconformidade, 4.1.1.1.1 e 4.4.2) com a opcao numbers, a chamada saia entre COLCHETES ("[1, p. 30]"), a lista de referencias numerava com colchetes ("[1] SOBRENOME..."), e nada avisava que o sistema numerico estava sendo usado junto com notas de rodape (#140).
ABERTO: #140

A 4.1.1.1.1 do Manual UFRJ/SiBI admite duas formas de indicar o numero: entre
PARENTESES, alinhado ao texto, ou sobrescrito -- e o numero da pagina vem depois,
separado por virgula: "(1, p. 30)". Colchete nao e nenhuma das duas. A mesma
secao, e a 4.4.2, dizem que o sistema numerico nao deve ser usado quando ha notas
de rodape. O coppe-numeric.cbx herda o numeric-comp do biblatex sem mudar o
delimitador, e o coppe-numeric.bbx rotula a lista com \\mkbibbrackets.

Cobra-se, com numbers:
  1. as chamadas saem "(1, p. 30)" e "(2)", e nao ha "[1" nem "[2" no documento;
  2. a lista de referencias nao usa colchetes nos rotulos;
  3. um documento com numbers e \\footnote gera no .log um aviso da classe que
     cita a secao 4.1.1.1.1.
"""
from medidas import Documento, relatar, compacta

BIB = r"""@book{a,
  author = {Almeida, Ana},
  title = {Primeiro livro},
  location = {Recife},
  publisher = {Editora Exemplo},
  year = {2001},
}
@book{b,
  author = {Borges, Beto},
  title = {Segundo livro},
  location = {Recife},
  publisher = {Editora Exemplo},
  year = {2002},
}
"""
CORPO = r"""\chapter{Um}
Uma chamada \cite[p.~30]{a} e outra \cite{b}. Com nota\footnote{Uma nota de rodape.}.
\printbibliography
"""

problemas = []
with Documento(opcoes="dsc,numbers", corpo=CORPO, bib=BIB) as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    todo = compacta(d.texto())
    pg = d.pagina_com("Uma chamada")
    corpo = compacta(d.texto(pg))
    trecho = corpo[corpo.find("Uma chamada"):corpo.find("Uma chamada") + 60]
    if "(1, p. 30)" not in corpo or "(2)" not in corpo:
        problemas.append("chamadas numericas: esperava '(1, p. 30)' e '(2)'; saiu %r" % trecho)
    if "[1" in todo or "[2" in todo:
        problemas.append("ha colchetes de chamada ou de rotulo no documento")
    if "4.1.1.1.1" not in d.log:
        problemas.append("numbers com nota de rodape: nenhum aviso no .log citando a 4.1.1.1.1")

relatar(problemas)
