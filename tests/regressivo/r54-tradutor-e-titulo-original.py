# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX. NAO roda na suite normal.

BUG: (desconformidade, 4.3.2.10 e 4.3.8.1) o tradutor saia como "Trad. por ALMEIDA, Julia" -- nome invertido e sobrenome em caixa alta, como se fosse autor --, e o titulo original (origtitle) nao saia (#135).
ABERTO: #135

A 4.3.2.10 do Manual UFRJ/SiBI poe os outros tipos de responsabilidade depois
do titulo, respeitando o texto da folha de rosto: "Traducao de Nome Sobrenome",
em ordem direta. A 4.3.8.1 pede, em nota, o titulo original: "Traducao de:
<titulo original>". O coppe.bbx declara o tradutor com o mesmo formato de nome do
autor (family-given, e o \\mkbibnamefamily poe em caixa alta), e nenhum driver
imprime origtitle.

Cobra-se, no texto da referencia:
  1. "Traducao de Julia Almeida" (ou "Traducao Julia Almeida"), em ordem direta;
  2. nao aparece "ALMEIDA, Julia" nem "Trad. por";
  3. "Traducao de: A new house".
"""
import re
from medidas import Documento, relatar, normaliza, entrada

BIB = r"""@book{trad,
  author = {Hughes, Ian},
  title = {Uma casa nova},
  translator = {Almeida, Júlia},
  origtitle = {A new house},
  location = {Porto Alegre},
  publisher = {Editora Exemplo},
  year = {1993},
  pagetotal = {21},
}
"""

problemas = []
with Documento(corpo=r"\chapter{Um}Texto.\nocite{*}\printbibliography", bib=BIB) as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    pg = d.pagina_com("Hughes")
    texto = d.texto(pg)
    ref = entrada(texto, "HUGHES")
    alvo = normaliza(ref)
    if not re.search(r"traducao (de )?julia almeida", alvo):
        problemas.append("o tradutor nao saiu em ordem direta depois do titulo: %r" % ref)
    if "almeida, julia" in alvo or "trad. por" in alvo:
        problemas.append("o tradutor saiu como autor (\"Trad. por ALMEIDA, Julia\"): %r" % ref)
    if "traducao de: a new house" not in alvo:
        problemas.append("faltou a nota do titulo original (\"Traducao de: A new house\"): %r" % ref)

relatar(problemas)
