# -*- coding: utf-8 -*-
"""Teste de regressao da CoppeTeX. NAO roda na suite normal.

BUG: a lista de simbolos saia em ordem alfabetica, e a 3.1.2.2.7 do Manual UFRJ/SiBI pede "de acordo com a ordem que aparece no texto" (#100).

A lista passa pelo makeindex, que ordena pela chave. Na ordem de aparicao a
chave e o numero da PRIMEIRA vez em que o simbolo e registrado; registrar o
mesmo simbolo de novo reaproveita o numero, e o makeindex junta as entradas.

Cobra-se, na lista pronta (.los):
  1. a ordem de aparicao: zeta, alfa, mu -- que nao e a alfabetica;
  2. um simbolo registrado duas vezes aparece UMA vez;
  3. a chave opcional e ignorada nessa ordem;
  4. com `simbolosalfabeticos', a ordem alfabetica pela chave: alfa, mu, zeta.
"""
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
SRC = os.path.join(RAIZ, "src")

DOC = r"""\documentclass[dsc%(opcao)s]{ufrj}
\makelosymbols
\title{Simbolos}
\foreigntitle{Symbols}
\author{Nome}{Sobrenome}
\advisor{Primeiro}{Orientador}{D.Sc.}{UFRJ}
\examiner{Primeiro Examinador}{D.Sc.}{UFRJ}
\department{PESC}
\date{09}{2026}
\keyword{Regressao}
\begin{document}
  \maketitle
  \frontmatter
  \begin{abstract}Resumo.\end{abstract}
  \begin{foreignabstract}Abstract.\end{foreignabstract}
  \printlosymbols
  \tableofcontents
  \mainmatter
  \chapter{Um}
  \symbl[zeta]{zetaS}{Simbolo zeta}
  \symbl[alfa]{alfaS}{Simbolo alfa}
  \symbl[zeta]{zetaS}{Simbolo zeta}
  \symbl[mu]{muS}{Simbolo mu}
  Texto.
\end{document}
"""


def lista(opcao):
    pasta = tempfile.mkdtemp(prefix="coppe-r96-")
    try:
        io.open(os.path.join(pasta, "s.tex"), "w", encoding="utf-8").write(
            DOC % {"opcao": opcao})
        amb = dict(os.environ)
        amb["TEXINPUTS"] = pasta + os.pathsep + SRC + os.pathsep
        rodar = lambda cmd: subprocess.run(cmd, cwd=pasta, env=amb,
                                           stdout=subprocess.DEVNULL,
                                           stderr=subprocess.DEVNULL)
        rodar(["pdflatex", "-interaction=nonstopmode", "s.tex"])
        rodar(["makeindex", "-s", os.path.join(SRC, "ufrj.ist"), "-o",
               "s.los", "s.syx"])
        los = os.path.join(pasta, "s.los")
        texto = io.open(los, encoding="utf-8").read() if os.path.exists(los) else ""
        return re.findall(r"\\item \[(\w+)S\]", texto)
    finally:
        shutil.rmtree(pasta, ignore_errors=True)


problemas = []
aparicao = lista("")
if aparicao != ["zeta", "alfa", "mu"]:
    problemas.append("ordem de aparicao: esperado zeta, alfa, mu; saiu %r" % aparicao)
alfabetica = lista(",simbolosalfabeticos")
if alfabetica != ["alfa", "mu", "zeta"]:
    problemas.append("simbolosalfabeticos: esperado alfa, mu, zeta; saiu %r" % alfabetica)

for x in problemas:
    print(x)
sys.exit(1 if problemas else 0)
