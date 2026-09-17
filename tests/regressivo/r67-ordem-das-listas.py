# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX. NAO roda na suite normal.

BUG: (desconformidade, 3.1.2) as listas de quadros, mapas, programas e algoritmos -- que sao listas de ILUSTRACOES -- vinham DEPOIS da lista de tabelas no max-exemplo, no manual.tex e no gerador de documento, e a Norma COPPE (secao 10) mandava poe-las entre a lista de tabelas e a de abreviaturas (#148).
ABERTO: #148

A 3.1.2 do Manual UFRJ/SiBI da a ordem dos elementos pre-textuais: lista de
ilustracoes, lista de tabelas, lista de abreviaturas e siglas, lista de
simbolos, sumario. A 2.10 diz que quadro, mapa e "outros" sao ilustracoes, e a
3.1.2.2.4 admite uma lista por tipo de ilustracao -- todas antes da lista de
tabelas. A classe nao impoe ordem: quem ordena e quem escreve o .tex, e os
modelos da entrega ensinavam a ordem errada.

Cobra-se (sem compilar):
  1. em src/max-exemplo.tex e src/manual.tex, \\listoftables vem depois de toda
     \\listof... de ilustracao que o arquivo usa;
  2. em tools/geradocvazio.py, a lista LISTAS poe listoftables depois de
     listofquadros, listofprogramas e listofalgorithms;
  3. a Norma COPPE (.md e .tex) nao diz mais "entre a Lista de Tabelas e a Lista
     de Abreviaturas".
"""
import io
import os
import re
from medidas import relatar, RAIZ

ILUSTRACOES = ("listoffigures", "listofframes", "listofquadros", "listofmapas",
               "listofprograms", "listofprogramas", "listofalgorithms")

problemas = []


def le(*partes):
    return io.open(os.path.join(RAIZ, *partes), encoding="utf-8").read()


for arq in (("src", "max-exemplo.tex"), ("src", "manual.tex")):
    texto = le(*arq)
    corpo = texto.split(r"\begin{document}", 1)[-1]
    chamadas = [(m.start(), m.group(1)) for m in
                re.finditer(r"^\s*\\(listof\w+)", corpo, re.M)]
    tabelas = [p for p, n in chamadas if n == "listoftables"]
    if not tabelas:
        continue
    depois = [n for p, n in chamadas if n in ILUSTRACOES and p > tabelas[0]]
    if depois:
        problemas.append("%s: %s vem depois de \\listoftables"
                         % ("/".join(arq), ", ".join("\\" + n for n in depois)))

gerador = le("tools", "geradocvazio.py")
m = re.search(r"LISTAS\s*=\s*\[(.*?)\]\s*\n\s*\n", gerador, re.S)
if not m:
    problemas.append("tools/geradocvazio.py: nao achei a lista LISTAS")
else:
    ordem = re.findall(r'\("(\w+)"', m.group(1))
    if "listoftables" in ordem:
        i = ordem.index("listoftables")
        depois = [n for n in ordem[i + 1:] if n in ILUSTRACOES]
        if depois:
            problemas.append("tools/geradocvazio.py: %s depois de listoftables" % ", ".join(depois))

for arq in (("NORMA_COPPE_2026.md",), ("src", "NORMA_COPPE_2026.tex")):
    if re.search(r"entre a Lista de Tabelas\s+e a Lista de Abreviaturas", le(*arq)):
        problemas.append("%s (secao 10): poe as listas de ilustracao da COPPE depois da "
                         "lista de tabelas" % "/".join(arq))

relatar(problemas)
