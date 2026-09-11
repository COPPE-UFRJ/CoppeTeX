# -*- coding: utf-8 -*-
"""Teste de regressao da CoppeTeX. NAO roda na suite normal.

BUG: o passo que copia para dist/ levava junto o README.md da raiz e os cinco
exemplos por idioma. O README da raiz e a proposta para a CPGP; o de dist/ e um
guia de instalacao para quem so quer usar a classe. A copia sobrescrevia o guia
a cada execucao (issue #75). Estava escrito em dois lugares -- no src/doall.bat
e no Makefile -- e os dois divergiram.

Este teste nao compila nada: ele le a lista. Defeito de lista se conserta
apagando uma linha, e volta do mesmo jeito, em qualquer um dos lugares onde a
lista for copiada. O que se cobra e que ela continue existindo em UM lugar so.

Sobre os exemplos por idioma, a regra MUDOU e vale explicar por que. Eles foram
todos tirados de dist/ de uma vez, como material de desenvolvimento. Depois
voltaram tres: o art. 57 da Resolucao CEPG n. 302/2024 admite portugues, ingles
e espanhol para redigir uma tese, e quem vai escrever em ingles precisa de um
exemplo em ingles tanto quanto quem escreve em portugues precisa do dele.
Frances e italiano continuam fora: os pacotes desses dois idiomas vao junto,
porque sao a demonstracao do mecanismo de extensao, mas nao ha respaldo
normativo para redigir uma tese neles, e um exemplo na pasta da entrega seria
um convite a faze-lo.
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
    for proibido in ("example_fr", "example_it", "example_pdfa"):
        if proibido in lista:
            problemas.append(
                "PARA_DIST leva %s -- so vai exemplo dos idiomas que o art. 57 "
                "da Res. CEPG 302/2024 admite" % proibido)
    # E o outro lado: o que tem de estar la. Um arquivo que sai da lista sem
    # querer nao quebra nada no ato -- a distribuicao simplesmente fica sem ele,
    # e quem descobre e o aluno, depois.
    for preciso in ("coppe.cls", "coppe.pdf", "manual.pdf", "coppe-quickref.pdf",
                    "example.tex", "example.pdf",
                    "example_en.tex", "example_en.pdf",
                    "example_es.tex", "example_es.pdf",
                    "latexmkrc", "coppe.ist", "ufrj-logo.pdf"):
        if '"%s"' % preciso not in lista:
            problemas.append("PARA_DIST nao leva %s" % preciso)

    # E, o que pegou de verdade: toda base de referencias que um exemplo da
    # entrega DECLARA tem de estar na lista. A tipos.bib nao estava, e o
    # example.tex a declara -- quem baixava a entrega recebia um PDF com as
    # citacoes em branco. Perguntar ao proprio .tex e melhor que manter uma
    # segunda lista aqui, que envelheceria do mesmo jeito.
    for exemplo in ("example", "example_en", "example_es"):
        fonte = ler("src/%s.tex" % exemplo)
        for base in re.findall(r"\\addbibresource\{([^}]+)\}", fonte):
            if '"%s"' % base not in lista:
                problemas.append(
                    "PARA_DIST nao leva %s, que o %s.tex declara em "
                    "\\addbibresource" % (base, exemplo))

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
