# -*- coding: utf-8 -*-
"""Teste de regressao da CoppeTeX. NAO roda na suite normal.

BUG: abreviaturas e siglas saiam sempre numa lista so, e a 3.1.2.2.6 do Manual UFRJ/SiBI recomenda listas separadas (#101).

Com \\makelosiglas no preambulo, as siglas -- as de \\sigla e as de \\acron -- vao
para a Lista de Siglas (.sgx -> .lsg), e a outra passa a se chamar Lista de
Abreviaturas. Sem \\makelosiglas, nada muda para quem ja escrevia: as siglas
continuam na lista de abreviaturas, que se chama Lista de Abreviaturas e Siglas.

Cobra-se as duas metades, nas listas prontas e no titulo que sai no PDF.
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

DOC = r"""\documentclass[dsc]{ufrj}
\makeloabbreviations
%(siglas)s
\newsigla{ufrj}{UFRJ}{Universidade Federal do Rio de Janeiro}
\title{Siglas}
\foreigntitle{Acronyms}
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
  \printloabbreviations
  %(imprime)s
  \tableofcontents
  \mainmatter
  \chapter{Um}
  A \sigla{ufrj} e a ABNT.\acron{ABNT}{Associacao Brasileira de Normas Tecnicas}
  \abbrev{fig.}{figura}
\end{document}
"""


def compila(separada):
    pasta = tempfile.mkdtemp(prefix="coppe-r97-")
    try:
        doc = DOC % {"siglas": "\\makelosiglas" if separada else "",
                     "imprime": "\\printlosiglas" if separada else ""}
        io.open(os.path.join(pasta, "s.tex"), "w", encoding="utf-8").write(doc)
        amb = dict(os.environ)
        amb["TEXINPUTS"] = pasta + os.pathsep + SRC + os.pathsep
        rodar = lambda cmd: subprocess.run(cmd, cwd=pasta, env=amb,
                                           stdout=subprocess.DEVNULL,
                                           stderr=subprocess.DEVNULL)
        rodar(["pdflatex", "-interaction=nonstopmode", "s.tex"])
        ist = os.path.join(SRC, "ufrj.ist")
        for ext, saida in (("abx", "lab"), ("sgx", "lsg")):
            if os.path.exists(os.path.join(pasta, "s." + ext)):
                rodar(["makeindex", "-s", ist, "-o", "s." + saida, "s." + ext])
        rodar(["pdflatex", "-interaction=nonstopmode", "s.tex"])

        def ler(ext):
            c = os.path.join(pasta, "s." + ext)
            return io.open(c, encoding="utf-8", errors="replace").read() \
                if os.path.exists(c) else ""
        txt = subprocess.run(["pdftotext", "-enc", "UTF-8", "s.pdf", "-"],
                             cwd=pasta, stdout=subprocess.PIPE,
                             stderr=subprocess.DEVNULL).stdout.decode("utf-8", "replace")
        return ler("lab"), ler("lsg"), txt.upper(), ler("log")
    finally:
        shutil.rmtree(pasta, ignore_errors=True)


problemas = []

lab, lsg, pdf, log = compila(True)
if "Output written" not in log:
    problemas.append("separada: nao compilou")
for s in ("[UFRJ]", "[ABNT]"):
    if s not in lsg:
        problemas.append("separada: %s nao esta na lista de siglas" % s)
    if s in lab:
        problemas.append("separada: %s continua na lista de abreviaturas" % s)
if "[fig.]" not in lab:
    problemas.append("separada: a abreviatura sumiu da lista de abreviaturas")
if "LISTA DE SIGLAS" not in pdf:
    problemas.append("separada: o PDF nao tem o titulo Lista de Siglas")
if "ABREVIATURAS E SIGLAS" in pdf:
    problemas.append("separada: a lista de abreviaturas ainda diz 'e Siglas'")

lab, lsg, pdf, log = compila(False)
for s in ("[UFRJ]", "[ABNT]", "[fig.]"):
    if s not in lab:
        problemas.append("junta: %s nao esta na lista de abreviaturas" % s)
if "LISTA DE ABREVIATURAS E SIGLAS" not in pdf:
    problemas.append("junta: o titulo deixou de ser Lista de Abreviaturas e Siglas")

for x in problemas:
    print(x)
sys.exit(1 if problemas else 0)
