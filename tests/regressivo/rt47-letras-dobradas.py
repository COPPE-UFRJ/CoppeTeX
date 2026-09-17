# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX. NAO roda na suite normal.

BUG: (desconformidade, 3.1.4.3, 3.1.4.4 e 2.6f) o vigesimo setimo apendice, anexo ou alinea parava a compilacao com "Counter too large", porque a letra vinha de \\Alph e \\alph, que so vao ate Z (#127).
ABERTO: #127

O Manual UFRJ/SiBI manda usar letras maiusculas DOBRADAS quando se esgotam as
letras do alfabeto na identificacao de apendices e anexos (AA, AB...), e letras
dobradas nas alineas (aa, ab...). O caso e raro, mas a regra e explicita.

Cobra-se: o documento com 27 apendices e uma lista de 27 alineas compila, o 27.o
apendice sai como "APENDICE AA" e a 27.a alinea como "aa)".
"""
from medidas import Documento, relatar, normaliza

apendices = "\n".join(r"\chapter{Apendice numero %d}Texto." % i for i in range(1, 28))
alineas = "\n".join(r"\item item de numero %d;" % i for i in range(1, 28))
CORPO = r"""
\chapter{Um}
Lista longa:
\begin{alineas}
%s
\end{alineas}
\appendix
%s
""" % (alineas, apendices)

problemas = []
with Documento(corpo=CORPO) as d:
    if not d.ok or "Counter too large" in d.log:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    texto = normaliza(d.texto())
    if "apendice aa - apendice numero 27" not in texto:
        problemas.append("o 27.o apendice nao saiu como APENDICE AA")
    if "aa) item de numero 27" not in texto:
        problemas.append("a 27.a alinea nao saiu como aa)")

relatar(problemas)
