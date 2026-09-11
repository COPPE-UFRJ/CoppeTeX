#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Confere o manual contra a classe: nenhum comando publico pode ficar de fora.

O manual e o exemplo envelhecem em silencio. Um comando novo entra na classe e
ninguem o documenta; uma linha do example.tex se desloca e a tabela "onde ver
cada coisa funcionando" passa a apontar para o lugar errado. Nenhuma das duas
coisas quebra a compilacao, e por isso nenhuma das duas aparece sozinha.

Este script olha tres coisas:

  1. Todo comando e ambiente PUBLICO que a classe define aparece no manual,
     marcado com \\DescribeMacro ou \\DescribeEnv?
  2. Toda opcao de classe aparece na secao de opcoes?
  3. Os numeros de linha da tabela "onde ver" ainda batem com o example.tex?

O que NAO e cobrado: comandos internos (os que levam @ no nome), os quatro
comandos de montagem de folha que o manual lista de proposito na secao
"Comandos que voce nao deve chamar", e os logotipos da familia TeX, que sao
enfeite tipografico e nao API.

    python3 tools/conferir-manual.py

Sai com codigo 1 se algo estiver fora do lugar, para poder entrar no harness.
"""
import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DTX = os.path.join(RAIZ, "src", "coppe.dtx")
CLS = os.path.join(RAIZ, "src", "coppe.cls")
EXEMPLO = os.path.join(RAIZ, "src", "example.tex")

# Logotipos da familia TeX e afins: a classe os define para uso tipografico,
# nao sao interface de quem escreve uma tese.
ENFEITE = {
    "TeX", "LaTeX", "LaTeXe", "BibTeX", "pdfTeX", "pdfLaTeX", "LuaLaTeX",
    "XeLaTeX", "MiKTeX", "CoppeTeX",
}

# Redefinicoes de comandos do proprio LaTeX, documentadas onde fazem sentido
# (ou nao documentadas de proposito, por serem o comando padrao inalterado).
PADRAO_LATEX = {
    "and", "appendixname", "cleardoublepage", "csname", "familydefault",
    "filedate", "filename", "fileversion", "footnoterule", "headrulewidth",
    "item", "numberline", "protect", "theFancyVerbLine", "glossaryname",
    "listabbreviationname", "listsymbolname", "lstlistingname",
    "lstlistlistingname", "quadroname", "listquadroname",
    "quadroautorefname", "cpsourcename",
}

# Ambientes internos do mecanismo de listas, nunca escritos a mao.
ENV_INTERNO = {"theglossary", "theindex"}


def ler(caminho):
    return io.open(caminho, encoding="utf-8", errors="replace").read()


def definidos(cls):
    cmds = set()
    cmds |= set(re.findall(r"\\(?:new|renew|provide)command\*?\s*\{?\\([A-Za-z@]+)", cls))
    cmds |= set(re.findall(r"\\let\\([A-Za-z@]+)\s*\\", cls))
    cmds |= set(re.findall(r"\\def\\([A-Za-z@]+)", cls))
    envs = set(re.findall(r"\\(?:new|renew)environment\*?\s*\{([A-Za-z@]+)\}", cls))
    envs |= set(re.findall(r"\\lstnewenvironment\{([A-Za-z@]+)\}", cls))
    envs |= set(re.findall(r"\\newfloat\{([A-Za-z@]+)\}", cls))
    opts = set(re.findall(r"\\DeclareOption\{([^}]*)\}", cls))
    publicos = {c for c in cmds if "@" not in c}
    return publicos, envs, opts


def documentados(dtx):
    macros = set(re.findall(r"\\DescribeMacro\{\\([A-Za-z@]+)\}", dtx))
    envs = set(re.findall(r"\\DescribeEnv\{([A-Za-z@]+)\}", dtx))
    # A secao "Comandos que voce nao deve chamar" lista os de montagem de folha.
    naochame = set(re.findall(r"\|\\(make[A-Za-z]+)\|", dtx))
    naochame |= set(re.findall(r"\|\\(coppefinal[a-z]+)\|", dtx))
    return macros, envs, naochame


def onde_ver(dtx, exemplo):
    """Confere a tabela de linhas do example.tex."""
    linhas_ex = exemplo.split("\n")
    problemas = []
    # linhas da tabela: ... & |\comando| & 123 \\
    for cmd, num in re.findall(r"&\s*\|\\([A-Za-z@]+)\|\s*&\s*(\d+)\s*\\\\", dtx):
        n = int(num)
        if n < 1 or n > len(linhas_ex):
            problemas.append((cmd, n, "fora do arquivo"))
            continue
        if not re.search(r"\\" + cmd + r"(?![A-Za-z])", linhas_ex[n - 1]):
            real = None
            for i, l in enumerate(linhas_ex, 1):
                if re.search(r"\\" + cmd + r"(?![A-Za-z])", l):
                    real = i
                    break
            problemas.append((cmd, n, "esta na linha %s" % (real or "nenhuma")))
    return problemas


def main():
    cls, dtx, exemplo = ler(CLS), ler(DTX), ler(EXEMPLO)
    cmds, envs, opts = definidos(cls)
    docmac, docenv, naochame = documentados(dtx)

    faltam_cmd = sorted(
        c for c in cmds
        if c not in docmac and c not in ENFEITE and c not in PADRAO_LATEX
        and c not in naochame
    )
    faltam_env = sorted(e for e in envs if e not in docenv and e not in ENV_INTERNO)
    faltam_opt = sorted(o for o in opts if ("texttt{%s}" % o) not in dtx)
    desalinhadas = onde_ver(dtx, exemplo)

    erros = 0
    print("=== conferir-manual: %d comandos publicos, %d ambientes, %d opcoes"
          % (len(cmds), len(envs), len(opts)))

    if faltam_cmd:
        erros += len(faltam_cmd)
        print("\nERRO  %d comando(s) publico(s) sem \\DescribeMacro no manual:"
              % len(faltam_cmd))
        for c in faltam_cmd:
            print("        \\%s" % c)
    else:
        print("ok    todo comando publico esta documentado")

    if faltam_env:
        erros += len(faltam_env)
        print("\nERRO  %d ambiente(s) sem \\DescribeEnv no manual:" % len(faltam_env))
        for e in faltam_env:
            print("        %s" % e)
    else:
        print("ok    todo ambiente esta documentado")

    if faltam_opt:
        erros += len(faltam_opt)
        print("\nERRO  %d opcao(oes) de classe nao citada(s) no manual:" % len(faltam_opt))
        for o in faltam_opt:
            print("        %s" % o)
    else:
        print("ok    toda opcao de classe esta documentada")

    if desalinhadas:
        erros += len(desalinhadas)
        print("\nERRO  %d linha(s) da tabela 'onde ver' nao batem com o example.tex:"
              % len(desalinhadas))
        for cmd, n, obs in desalinhadas:
            print("        \\%-22s manual diz %-5d %s" % (cmd, n, obs))
    else:
        print("ok    a tabela 'onde ver' bate com o example.tex")

    print("\n=== %d problema(s) ===" % erros)
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
