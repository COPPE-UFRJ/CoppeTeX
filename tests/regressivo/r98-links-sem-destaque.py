# -*- coding: utf-8 -*-
"""Teste de regressao da CoppeTeX. NAO roda na suite normal.

BUG: todo link saia com MOLDURA -- vermelha nas referencias, verde nas
citacoes, ciano nas URLs --, que o TeXstudio e o Foxit mostram. A classe
carregava o hyperref sem opcao nenhuma, e a moldura e o padrao dele. O Manual
UFRJ/SiBI (2.1b) quer o texto na cor preta.

Cobra-se: por padrao, nenhuma moldura e nenhuma cor, com e sem pdfa;
linkscommoldura poe a moldura; linkscoloridos pinta o texto; semlinks vence as
duas; um \\hypersetup no preambulo vence as opcoes. E, de carona, que
listasnosumario continua pondo as listas no sumario e que sem ela elas ficam
fora.
"""
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zlib

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
SRC = os.path.join(RAIZ, "src")

DOC = r"""\documentclass[dsc,%(opcoes)s]{coppe}
%(preambulo)s
\title{Links}
\foreigntitle{Links}
\author{Nome}{Sobrenome}
\advisor{Primeiro}{Orientador}{D.Sc.}{UFRJ}
\examiner{Primeiro Examinador}{D.Sc.}{UFRJ}
\department{PESC}
\date{09}{2026}
\keyword{Regressao}
\foreignkeyword{Regression}
\approvaldate{1 de setembro de 2026}
\concentrationarea{Engenharia}
\productiontype{bibliographic}
\linkedproject{no}
\begin{document}
  \maketitle
  \frontmatter
  \begin{abstract}Resumo.\end{abstract}
  \begin{foreignabstract}Abstract.\end{foreignabstract}
  \listoffigures
  \tableofcontents
  \mainmatter
  \chapter{Um}\label{cap:um}
  Veja o capitulo~\ref{cap:um} e \url{https://ufrj.br}.
  \begin{figure}[h]\caption{Uma figura}\end{figure}
  \begin{lstlisting}
resultado = calcula_uma_coisa_com_nome_comprido(primeiro_argumento, segundo_argumento, terceiro)
  \end{lstlisting}
\end{document}
"""


def compila(opcoes, preambulo=""):
    pasta = tempfile.mkdtemp(prefix="coppe-r98-")
    try:
        doc = DOC % {"opcoes": opcoes, "preambulo": preambulo}
        io.open(os.path.join(pasta, "l.tex"), "w", encoding="utf-8").write(doc)
        amb = dict(os.environ)
        amb["TEXINPUTS"] = pasta + os.pathsep + SRC + os.pathsep
        for _ in range(2):
            subprocess.run(["pdflatex", "-interaction=nonstopmode", "l.tex"],
                           cwd=pasta, env=amb, stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)
        pdf = os.path.join(pasta, "l.pdf")
        if not os.path.exists(pdf):
            return None
        dados = open(pdf, "rb").read()
        molduras = set(re.findall(rb"/Border\s*\[([^\]]*)\]", dados))
        # Operadores de cor RGB que nao sao cinza, em todos os fluxos. O
        # logotipo tem os seus; o que interessa e a DIFERENCA para o padrao.
        cores = 0
        for m in re.finditer(rb"stream\r?\n", dados):
            fim = dados.find(b"endstream", m.end())
            try:
                fluxo = zlib.decompress(dados[m.end():fim])
            except zlib.error:
                continue
            cores += len([c for c in re.findall(rb"([\d.]+) ([\d.]+) ([\d.]+) rg", fluxo)
                          if len(set(c)) > 1])
        toc = io.open(os.path.join(pasta, "l.toc"), encoding="latin-1").read()
        return molduras, cores, "listoffigures" in toc.lower() or "figuras" in toc.lower()
    finally:
        shutil.rmtree(pasta, ignore_errors=True)


problemas = []
com_moldura = lambda m: any(b.split()[-1:] != [b"0"] for b in m)

padrao = compila("")
if padrao is None:
    print("o documento padrao nao compilou")
    sys.exit(1)
m0, c0, toc0 = padrao
if com_moldura(m0):
    problemas.append("padrao: link com moldura %r" % m0)
if toc0:
    problemas.append("padrao: a lista de figuras entrou no sumario")

casos = [
    ("pdfa", False, False),
    ("semlinks", False, False),
    ("linkscommoldura", True, False),
    ("linkscoloridos", False, True),
    ("pdfa,linkscoloridos", False, True),
    ("linkscoloridos,semlinks", False, False),
    ("linkscommoldura,semlinks", False, False),
    # A seta curva da linha quebrada na listagem: preta por padrao (nao soma
    # cor ao padrao), vermelha com setavermelha -- inclusive sob pdfa, que ja
    # derrubou a seta colorida uma vez.
    ("setavermelha", False, True),
    ("pdfa,setavermelha", False, True),
]
for opcoes, moldura, cor in casos:
    r = compila(opcoes)
    if r is None:
        problemas.append("%s: nao compilou" % opcoes)
        continue
    m, c, _ = r
    if com_moldura(m) != moldura:
        problemas.append("%s: moldura %s, esperava %s" % (opcoes, m, moldura))
    if (c > c0) != cor:
        problemas.append("%s: cor %d contra %d do padrao, esperava %s"
                         % (opcoes, c, c0, "cor" if cor else "sem cor"))

r = compila("", r"\hypersetup{colorlinks=true}")
if r is None or r[1] <= c0:
    problemas.append("\\hypersetup do autor nao venceu o padrao")

r = compila("listasnosumario")
if r is None or not r[2]:
    problemas.append("listasnosumario: a lista de figuras nao entrou no sumario")

for x in problemas:
    print(x)
sys.exit(1 if problemas else 0)
