# -*- coding: utf-8 -*-
"""Teste de regressao da CoppeTeX. NAO roda na suite normal.

BUG: quem copiava so o coppe.cls para a pasta do trabalho recebia do TeX um
"File `coppe-logo' not found" sem nenhuma pista de que o arquivo vem COM a
classe. A classe passou a dizer isso, e a nomear o arquivo que falta.

Para reproduzir e preciso uma instalacao capenga de proposito: a classe e os
estilos num diretorio temporario, SEM os logotipos, e o TEXINPUTS apontando so
para la. E por isso que este teste e um .py e nao um .tex -- ele precisa mexer
no ambiente antes de chamar o pdflatex.
"""
import glob
import io
import os
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
SRC = os.path.join(RAIZ, "src")

DOC = r"""\documentclass[dsc]{coppe}
\title{Sem logotipo}
\foreigntitle{Without a logo}
\author{Nome}{Sobrenome}
\advisor{Primeiro}{Orientador}{D.Sc.}{UFRJ}
\examiner{Primeiro Examinador}{D.Sc.}{UFRJ}
\department{PESC}
\date{09}{2026}
\keyword{Regressao}
\begin{document}
  \maketitle
\end{document}
"""

pasta = tempfile.mkdtemp(prefix="coppe-r91-")
problemas = []
try:
    # Tudo o que a classe carrega, MENOS as imagens: sem .pdf e sem .eps.
    for padrao in ("*.cls", "*.bbx", "*.cbx", "*.dbx", "*.lbx", "*.def",
                   "*.ist", "*.bib"):
        for f in glob.glob(os.path.join(SRC, padrao)):
            shutil.copy(f, pasta)
    io.open(os.path.join(pasta, "semlogo.tex"), "w", encoding="utf-8").write(DOC)

    ambiente = dict(os.environ)
    ambiente["TEXINPUTS"] = pasta + ";"
    ambiente["BIBINPUTS"] = pasta + ";"
    p = subprocess.run(["pdflatex", "-interaction=nonstopmode", "semlogo.tex"],
                       cwd=pasta, env=ambiente,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    log = os.path.join(pasta, "semlogo.log")
    texto = ""
    if os.path.exists(log):
        texto = io.open(log, encoding="utf-8", errors="replace").read()

    if p.returncode == 0:
        problemas.append("compilou sem os logotipos, e devia ter parado")
    if "ufrj-logo" not in texto:
        problemas.append("a mensagem nao nomeia o arquivo que falta")
    if "Class coppe Error" not in texto:
        problemas.append("o erro nao veio da classe: e o do TeX, sem pista nenhuma")
finally:
    shutil.rmtree(pasta, ignore_errors=True)

for x in problemas:
    print(x)
sys.exit(1 if problemas else 0)
