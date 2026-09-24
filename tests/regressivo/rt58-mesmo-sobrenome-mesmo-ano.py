# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: (desconformidade, 4.1.1.2b) autores com o mesmo sobrenome saiam desambiguados com o prenome ANTES do sobrenome ("Orlando Braga, 1987"), e a desambiguacao valia para o documento inteiro, mesmo quando os anos eram diferentes (#139).

A 4.1.1.2(b) do Manual UFRJ/SiBI: quando houver autores com o mesmo sobrenome e
a MESMA data, acrescentam-se as iniciais dos prenomes, e se a coincidencia
persistir, o prenome por extenso -- na forma "(Sobrenome, I., ano)" e
"(Sobrenome, Prenome, ano)". Sem coincidencia de ano, nao se acrescenta nada.
O biblatex resolve com uniquename=minyearinit/minyearfull, mas imprime o
prenome antes do sobrenome se o formato de labelname nao for redefinido.

Cobra-se, nas chamadas:
  (Braga, Orlando, 1987) (Braga, Osvaldo, 1987)  -- iniciais iguais no mesmo ano
  (Braga, O., 1966) (Braga, P., 1966)            -- iniciais bastam
  (Braga, 1970)                                  -- ano sem coincidencia
"""
from medidas import Documento, relatar, compacta

BIB = "\n".join(r"""@book{%s,
  author = {Braga, %s},
  title = {Obra %s},
  location = {Recife},
  publisher = {Editora Exemplo},
  year = {%s},
}""" % (k, prenome, k, ano) for k, prenome, ano in (
    ("b1", "Orlando", "1987"), ("b2", "Osvaldo", "1987"),
    ("b3", "Oscar", "1966"), ("b4", "Pedro", "1966"), ("b5", "Rui", "1970")))
ESPERADAS = ["(Braga, Orlando, 1987)", "(Braga, Osvaldo, 1987)",
             "(Braga, O., 1966)", "(Braga, P., 1966)", "(Braga, 1970)"]

problemas = []
with Documento(corpo=r"\chapter{Um}Chamadas: \citep{b1} \citep{b2} \citep{b3} \citep{b4} \citep{b5}.",
               bib=BIB) as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    pg = d.pagina_com("Chamadas:")
    texto = compacta(d.texto(pg))
    trecho = texto[texto.find("Chamadas:"):texto.find("Chamadas:") + 160]
    for esperada in ESPERADAS:
        if esperada not in texto:
            problemas.append("faltou %s" % esperada)
    if problemas:
        problemas.append("saiu: %r" % trecho)

relatar(problemas)
