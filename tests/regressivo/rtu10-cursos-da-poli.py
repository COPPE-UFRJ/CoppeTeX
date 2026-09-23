# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: nao havia defeito antigo aqui -- o estilo da Escola Politecnica nasceu (#170) com as treze siglas de DEPARTAMENTO da antiga poli.cls, e elas nao sao os cursos: cobriam nove cursos, e a Escola tem treze de Engenharia mais o de Nanotecnologia. Faltavam Ambiental, Controle e Automacao, Petroleo, e Metalurgica e Materiais separados. Quem fizesse Projeto de Graduacao num deles nao tinha sigla para pedir.

A lista e a da propria Escola (poli.ufrj.br/ensino/graduacao/cursos), conferida
em 23/09/2026. Este teste a guarda: se a Escola criar um curso, ele falha ate
alguem declarar o curso novo -- e e esse o ponto.

Cobra-se, sem compilar, lendo o src/ufrj-poli.sty gerado:
  1. cada curso da lista tem um \\ufrjdeclareprogram, com o nome do curso;
  2. todo curso de Engenharia confere um titulo declarado (o argumento
     opcional), e o titulo comeca por "Engenheiro";
  3. as siglas de departamento da poli.cls continuam declaradas, para o
     trabalho escrito com ela;
  4. nenhuma sigla declarada duas vezes no mesmo ramo da opcao
     `civilpordepartamento' -- a segunda apagaria a primeira.
"""
import io
import os
import re
import sys

from medidas import relatar, SRC

STY = os.path.join(SRC, "ufrj-poli.sty")

# curso -> nome como a Escola o escreve. Nanotecnologia nao e Engenharia, e por
# isso nao entra na cobranca do titulo.
CURSOS = {
    "AMBIENTAL": "Engenharia Ambiental",
    "CIVIL": "Engenharia Civil",
    "COMPUTACAO": "Engenharia de Computação e Informação",
    "CONTROLE": "Engenharia de Controle e Automação",
    "ELETRICA": "Engenharia Elétrica",
    "ELETRONICA": "Engenharia Eletrônica e de Computação",
    "MATERIAIS": "Engenharia de Materiais",
    "MECANICA": "Engenharia Mecânica",
    "METALURGICA": "Engenharia Metalúrgica",
    "NAVAL": "Engenharia Naval e Oceânica",
    "NUCLEAR": "Engenharia Nuclear",
    "PETROLEO": "Engenharia de Petróleo",
    "PRODUCAO": "Engenharia de Produção",
    "NANOTECNOLOGIA": "Nanotecnologia",
}
DEPARTAMENTOS = ["DCC", "DES", "DEG", "DET", "DHIMA", "DEE", "DEM", "DMM",
                 "DNC", "DENO", "DEI", "ECI", "DEL"]

problemas = []
if not os.path.exists(STY):
    problemas.append("o ufrj-poli.sty nao foi gerado: rode pdflatex ufrj-poli.ins em src/")
    relatar(problemas)

texto = io.open(STY, encoding="utf-8").read()
# \ufrjdeclareprogram[<titulo>]{<sigla>}{<curso>}{<ingles>}, em uma ou mais linhas
DECL = re.compile(r"\\ufrjdeclareprogram(?:\[([^\]]*)\])?\s*\{(\w+)\}\s*\{([^}]*)\}\s*\{([^}]*)\}")
declarados = {}
for titulo, sigla, curso, ingles in DECL.findall(texto):
    declarados.setdefault(sigla, []).append((titulo or "", " ".join(curso.split()), ingles))

# 1 e 2. todo curso da Escola esta la, com o nome certo e com titulo
for sigla, nome in CURSOS.items():
    if sigla not in declarados:
        problemas.append("falta o curso %s (%s): nenhum \\ufrjdeclareprogram{%s}"
                         % (sigla, nome, sigla))
        continue
    titulo, curso, _ = declarados[sigla][0]
    if curso != nome:
        problemas.append("%s: o curso esta como %r, e a Escola o chama de %r"
                         % (sigla, curso, nome))
    if nome.startswith("Engenharia") and not titulo.startswith("Engenheiro"):
        problemas.append("%s: o titulo conferido esta %r, e devia comecar por Engenheiro"
                         % (sigla, titulo))

# 3. as siglas da poli.cls continuam aceitas
for sigla in DEPARTAMENTOS:
    if sigla not in declarados:
        problemas.append("a sigla %s da poli.cls saiu do estilo: o trabalho escrito "
                         "com ela para de compilar" % sigla)

# 4. nenhuma sigla duas vezes no mesmo ramo do \if
ramos = re.split(r"\\if@ufrjpolidepcivil|\\else|\\fi", texto)
for ramo in ramos:
    vistas = [s for _, s, _, _ in DECL.findall(ramo)]
    repetidas = sorted({s for s in vistas if vistas.count(s) > 1})
    if repetidas:
        problemas.append("sigla declarada duas vezes no mesmo ramo: %s"
                         % ", ".join(repetidas))

relatar(problemas)
