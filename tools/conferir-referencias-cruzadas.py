#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Caca referencia cruzada quebrada em TODOS os .log do projeto.

Um \\ref para um rotulo que nao existe nao interrompe a compilacao: sai "??" na
pagina e um aviso no .log, e o PDF e gerado. O mesmo vale para uma citacao com
chave inexistente, para um rotulo declarado duas vezes, e para o caso em que o
documento pede mais uma passada e ninguem a roda. Nenhum desses aparece no
codigo de saida do pdflatex, e por isso nenhum deles aparece no harness.

Este script le os .log e cobra os quatro:

  * Reference `x' on page N undefined
  * Citation `x' on page N undefined
  * Label `x' multiply defined
  * Rerun to get cross-references right   (faltou uma passada)

    python3 tools/conferir-referencias-cruzadas.py
    python3 tools/conferir-referencias-cruzadas.py src/manual.log

Sem argumento, varre src/, tests/, tests/adversativa/ e tests/regressivo/. Sai
com codigo 1 se achar qualquer coisa.
"""
import glob
import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PADROES = [
    ("referencia indefinida", re.compile(r"Reference [`'\"]([^'\"]+)['\"] on page (\S+) undefined")),
    ("citacao indefinida", re.compile(r"Citation [`'\"]([^'\"]+)['\"] on page (\S+) undefined")),
    ("rotulo repetido", re.compile(r"Label [`'\"]([^'\"]+)['\"] multiply defined")),
]
# (o aviso generico de rerun foi deliberadamente retirado; ver o comentario abaixo)


def logs(argv):
    if argv:
        return argv
    achados = []
    for pasta in ("src", "tests", os.path.join("tests", "adversativa"),
                  os.path.join("tests", "regressivo")):
        achados += sorted(glob.glob(os.path.join(RAIZ, pasta, "*.log")))
    return achados


def main():
    arquivos = logs(sys.argv[1:])
    if not arquivos:
        print("nenhum .log encontrado -- compile antes")
        return 1

    total = 0
    for caminho in arquivos:
        # O .log inteiro, e nao um pedaco dele.
        #
        # Aqui houve um erro que vale registrar, porque ele APROVAVA errado:
        # este script cortava o texto no ULTIMO "LaTeX2e <", na crenca de que o
        # arquivo guardasse varias passadas e que o ultimo banner marcasse o
        # comeco da ultima. Nao guarda -- o pdflatex REESCREVE o .log a cada
        # passada, e "This is pdfTeX" aparece uma vez em cada arquivo. O que
        # aparece duas vezes e o BANNER, que o LaTeX repete no fim do log, logo
        # antes do resumo de avisos. O corte jogava fora o corpo da passada, que
        # e justamente onde estao os quatro avisos procurados aqui, e o script
        # passou a dizer "nenhuma referencia quebrada" sempre.
        #
        # ACOPLAMENTO: tools/build-check.ps1 lia o .log pela mesma regra, e pelo
        # mesmo motivo. Os dois foram corrigidos juntos.
        texto = io.open(caminho, encoding="utf-8", errors="replace").read()
        nome = os.path.relpath(caminho, RAIZ)
        achados = []
        for rotulo, padrao in PADROES:
            for m in padrao.finditer(texto):
                achados.append("%s: %s" % (rotulo, m.group(1)))
        # O aviso generico ("There were undefined references") NAO entra aqui.
        # O biblatex o dispara nos documentos em espanhol mesmo com tudo
        # resolvido: o pacote de idioma registra o mapeamento em
        # \AtBeginDocument e o contador de refsection so fecha na passada
        # seguinte. Conferido: nenhum desses documentos tem "??" na pagina.
        # So conta a prova -- uma referencia ou citacao NOMEADA como indefinida,
        # que e o que os padroes acima procuram.
        # nao duplicar o mesmo aviso repetido em varias passadas do mesmo log
        vistos = []
        for a in achados:
            if a not in vistos:
                vistos.append(a)
        if vistos:
            total += len(vistos)
            print("\n%s" % nome)
            for a in vistos:
                print("   ERRO  %s" % a)

    if total == 0:
        print("ok  %d log(s) lidos, nenhuma referencia quebrada" % len(arquivos))
    else:
        print("\n=== %d problema(s) em %d log(s) ===" % (total, len(arquivos)))
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
