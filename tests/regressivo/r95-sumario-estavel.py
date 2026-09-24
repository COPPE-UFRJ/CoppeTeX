# -*- coding: utf-8 -*-
"""Teste de regressao da CoppeTeX. NAO roda na suite normal.

BUG: a largura da coluna de indicativos do sumario, salva no .aux, alternava a cada passada (42,4 pt, 13,2 pt, 42,4 pt...) e o latexmk rodava o pdflatex ate o limite, terminando com "pdflatex needed too many passes" (#98).

\\ufrj@tocnumberline mede cada indicativo enquanto o sumario e composto e guarda
o maior no .aux, para a passada seguinte. Ela nao era protegida, e as entradas
de capitulo passam por \\MakeUppercase, que EXPANDE o argumento: a medicao ficava
embaralhada de um jeito que dependia do valor da passada anterior. O PDF saia
certo, e por isso ninguem via -- mas o .aux nunca ficava igual, e no Overleaf
toda tese rodava cinco passadas e terminava com erro.

O teste compila um documento minimo -- dois capitulos, os cinco niveis de secao,
um apendice e um anexo -- quatro vezes e cobra que o valor salvo seja o MESMO na
terceira e na quarta passada. Com a classe antiga ele saia 42,4 / 6,6 / 42,4.
(O r04 nao serve: com um capitulo so, o defeito nao aparece.)
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
\usepackage{ufrj-coppe}
\title{Sumario estavel}
\foreigntitle{Stable table of contents}
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
  \tableofcontents
  \mainmatter
  \chapter{Um}
  \section{Secao}
  \subsection{Subsecao}
  \subsubsection{Subsubsecao}
  \paragraph{Quinaria}
  Texto.
  \chapter{Dois}
  Texto.
  \appendix
  \chapter{Apendice}
  Texto.
  \annex
  \chapter{Anexo}
  Texto.
\end{document}
"""

problemas = []
pasta = tempfile.mkdtemp(prefix="coppe-r95-")
try:
    io.open(os.path.join(pasta, "estavel.tex"), "w", encoding="utf-8").write(DOC)
    ambiente = dict(os.environ)
    classe = os.environ.get("COPPE_R95_CLASSE", SRC)
    ambiente["TEXINPUTS"] = pasta + os.pathsep + classe + os.pathsep + SRC + os.pathsep
    valores = []
    for _ in range(4):
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "estavel.tex"],
                       cwd=pasta, env=ambiente,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        aux = os.path.join(pasta, "estavel.aux")
        texto = io.open(aux, encoding="utf-8", errors="replace").read() \
            if os.path.exists(aux) else ""
        m = re.search(r"\\gdef\\ufrj@tocnumsaved\{([^}]*)\}", texto)
        valores.append(m.group(1) if m else None)
    if valores[2] is None or valores[3] is None:
        problemas.append("o .aux nao traz \\ufrj@tocnumsaved: %r" % valores)
    elif valores[2] != valores[3]:
        problemas.append("a largura do sumario nao estabiliza: %s" % " -> ".join(
            str(v) for v in valores))
finally:
    shutil.rmtree(pasta, ignore_errors=True)

for x in problemas:
    print(x)
sys.exit(1 if problemas else 0)
