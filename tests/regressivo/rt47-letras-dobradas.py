# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: (desconformidade, 3.1.4.3, 3.1.4.4 e 2.6f) o vigesimo setimo apendice, anexo ou alinea parava a compilacao com "Counter too large", porque a letra vinha de \\Alph e \\alph, que so vao ate Z (#127).

O Manual UFRJ/SiBI manda usar letras maiusculas DOBRADAS quando se esgotam as
letras do alfabeto na identificacao de apendices e anexos, e letras dobradas
nas alineas. O caso e raro, mas a regra e explicita. Nem o Manual nem a NBR
14724:2024 dao exemplo, e a classe le "dobrada" ao pe da letra: a mesma letra
repetida -- AA, BB, CC..., e nao a contagem do Excel, AA, AB, AC. O 27.o sai
igual nas duas leituras; o 28.o as separa, e por isso e cobrado tambem.

Cobra-se: o documento com 28 apendices e uma lista de 28 alineas compila; o
27.o apendice sai "APENDICE AA" e o 28.o "APENDICE BB"; a 27.a alinea sai
"aa)" e a 28.a "bb)".
"""
from medidas import Documento, relatar, normaliza

apendices = "\n".join(r"\chapter{Apendice numero %d}Texto." % i for i in range(1, 29))
alineas = "\n".join(r"\item item de numero %d;" % i for i in range(1, 29))
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
    for esperado, o_que in (("apendice aa - apendice numero 27", "o 27.o apendice como APENDICE AA"),
                            ("apendice bb - apendice numero 28", "o 28.o apendice como APENDICE BB"),
                            ("aa) item de numero 27", "a 27.a alinea como aa)"),
                            ("bb) item de numero 28", "a 28.a alinea como bb)")):
        if esperado not in texto:
            problemas.append("nao saiu %s" % o_que)
    if "apendice ab" in texto or "ab) item" in texto:
        problemas.append("saiu a contagem do Excel (AB), e nao a letra dobrada (BB)")

relatar(problemas)
