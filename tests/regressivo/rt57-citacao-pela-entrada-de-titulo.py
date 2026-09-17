# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX. NAO roda na suite normal.

BUG: (desconformidade, 4.1.1.1.2 e 4.1.1.2a) a citacao de obra que entra pelo titulo saia com o titulo INTEIRO em ITALICO e sem virgula antes do ano: "(Guia 2012, p. 7)", "(O perfil do engenheiro 1990)" (#138).
ABERTO: #138

O sistema autor-data do Manual UFRJ/SiBI (4.1.1.1.2) indica o titulo de entrada
seguido do ano, SEPARADOS POR VIRGULA; a 4.1.1.2(a) grafa a chamada so com a
inicial maiuscula, sem destaque; e o exemplo da secao traz a chamada so com a
palavra de entrada, sem o subtitulo. O estilo authoryear do biblatex usa, sem
autor, o labeltitle em \\mkbibemph e o separa do ano por espaco.

Cobra-se:
  1. \\citep[p.~7]{guia} sai "(Guia, 2012, p. 7)";
  2. \\citep{perfil} (titulo com artigo) sai "(O perfil..., 1990)", com virgula antes do ano;
  3. nenhuma das duas chamadas tem italico.
"""
import re
from medidas import Documento, relatar, compacta

BIB = r"""@book{guia,
  title = {Guia},
  subtitle = {de conversação},
  location = {São Paulo},
  publisher = {Editora Exemplo},
  year = {2012},
}
@book{perfil,
  title = {O perfil do engenheiro},
  location = {Brasília},
  publisher = {Editora Exemplo},
  year = {1990},
}
"""

problemas = []
with Documento(corpo=r"\chapter{Um}Primeira chamada \citep[p.~7]{guia}; segunda chamada \citep{perfil}.",
               bib=BIB) as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    pg = d.pagina_com("Primeira chamada")
    texto = compacta(d.texto(pg))
    trecho = texto[texto.find("Primeira chamada"):texto.find("segunda chamada") + 60]
    if "(Guia, 2012, p. 7)" not in texto:
        problemas.append("esperava '(Guia, 2012, p. 7)'; saiu %r" % trecho)
    if not re.search(r"\(O perfil[^()]*, 1990\)", texto):
        problemas.append("esperava '(O perfil..., 1990)' com virgula antes do ano; saiu %r" % trecho)
    italicos = [f.texto for f in d.fragmentos(pg) if f.italico and
                ("Guia" in f.texto or "perfil" in f.texto)]
    if italicos:
        problemas.append("chamada pelo titulo em italico: %r" % italicos)

relatar(problemas)
