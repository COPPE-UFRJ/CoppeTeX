# -*- coding: utf-8 -*-
"""Teste de regressao da CoppeTeX. NAO roda na suite normal.

BUG: o passo que copia para dist/ levava junto o README.md da raiz e os cinco
exemplos por idioma. O README da raiz e a proposta para a CPGP; o de dist/ e um
guia de instalacao para quem so quer usar a classe. A copia sobrescrevia o guia
a cada execucao, e os cinco exemplos voltavam para a distribuicao depois de
terem sido tirados de proposito (issue #75). Estava escrito em dois lugares --
no src/doall.bat e no Makefile -- e os dois divergiram.

Este teste nao compila nada: ele le a lista. Defeito de lista se conserta
apagando uma linha, e volta do mesmo jeito, em qualquer um dos lugares onde a
lista for copiada. O que se cobra e que ela continue existindo em UM lugar so e
que os dois nomes proibidos nao estejam nela.
"""
import io
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))

problemas = []


def ler(rel):
    caminho = os.path.join(RAIZ, rel.replace("/", os.sep))
    if not os.path.exists(caminho):
        problemas.append("%s nao existe" % rel)
        return ""
    return io.open(caminho, encoding="utf-8", errors="replace").read()


# 1. A lista que vale, em tools/painel.py.
painel = ler("tools/painel.py")
m = re.search(r"PARA_DIST\s*=\s*\[(.*?)\]", painel, re.S)
if not m:
    problemas.append("nao achei a lista PARA_DIST em tools/painel.py")
else:
    lista = m.group(1)
    if "README" in lista:
        problemas.append("PARA_DIST leva um README -- o de dist/ e outro documento")
    for proibido in ("example_pt", "example_en", "example_es",
                     "example_fr", "example_it"):
        if proibido in lista:
            problemas.append(
                "PARA_DIST leva %s -- os exemplos por idioma sao material de "
                "desenvolvimento (issue #75)" % proibido)

# 2. Nem o doall.bat nem o Makefile podem ter voltado a ter lista propria.
doall = ler("src/doall.bat")
if re.search(r"(?im)^\s*copy\b", doall):
    problemas.append("src/doall.bat voltou a copiar por conta propria; "
                     "a lista tem de existir em um lugar so")

makefile = ler("src/Makefile")
alvo = makefile.split("build:", 1)[-1].split("\nhelp:", 1)[0]
if re.search(r"(?m)^\t*cp -vp \$\(PACKAGE_NAME\)", alvo):
    problemas.append("o alvo build do src/Makefile voltou a ter lista propria")

# 3. O rodador da primeira camada nao pode voltar a parar no banner do
#    makeindex. No Windows PowerShell 5.1, o que um executavel escreve em
#    stderr vira ErrorRecord; com "Stop", o banner do makeindex -- que sai em
#    stderr e termina com codigo 0 -- derrubava a suite inteira no meio.
runtests = ler("tests/run-tests.ps1")
if re.search(r'ErrorActionPreference\s*=\s*"Stop"', runtests):
    problemas.append('tests/run-tests.ps1 voltou a "Stop": o banner do '
                     "makeindex derruba a suite")

for x in problemas:
    print(x)
sys.exit(1 if problemas else 0)
