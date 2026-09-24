# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: (falta, 2.7 e 3.1.2.1.6) um trabalho em mais de um volume nao tinha como manter UMA sequencia de folhas do primeiro ao ultimo volume, nem como trazer o SUMARIO COMPLETO em cada volume; \\volumes e \\volume so imprimiam "Volume 1 de 2" (#126).

A 2.7 do Manual UFRJ/SiBI manda manter uma unica sequencia de numeracao das
folhas do primeiro ao ultimo volume; a 3.1.2.1.6 manda o sumario completo em
cada volume. Cada volume e um .tex compilado a parte, entao a classe precisa
ler o que o outro volume gerou.

API proposta pela issue (se mudar, mude aqui):

    \\volumefiles{vol1,vol2}   % no preambulo dos DOIS volumes; sinonimo \\arquivosdosvolumes

que (a) no volume 2, continua a contagem de folhas depois da ultima folha do
volume 1, lida do .aux dele; e (b) em cada volume, compoe o sumario com as
entradas de todos os volumes, lidas dos .toc.

Cobra-se, depois de compilar vol1, vol2, vol1, vol2:
  1. o sumario do volume 1 traz o capitulo do volume 2, e vice-versa;
  2. o primeiro folio do volume 2 e maior que o ultimo folio do volume 1.
"""
import re
import shutil
import tempfile
import os
import io
import subprocess
from medidas import relatar, SRC

MODELO = r"""\documentclass[dsc]{ufrj}
\usepackage{ufrj-coppe}
\volumefiles{vol1,vol2}
\volumes{2}
\volume{%(n)s}
\title{Obra em dois volumes}
\foreigntitle{Two-volume work}
\author{Nome}{Sobrenome}
\advisor{Primeiro}{Orientador}{D.Sc.}{UFRJ}
\examiner{Primeiro Examinador}{D.Sc.}{UFRJ}
\department{PESC}
\date{09}{2026}
\keyword{regressao}
\begin{document}
\maketitle
\frontmatter
\begin{abstract}Resumo.\end{abstract}
\tableofcontents
\mainmatter
%(corpo)s
\end{document}
"""

problemas = []
pasta = tempfile.mkdtemp(prefix="coppe-r46-")
try:
    amb = dict(os.environ)
    amb["TEXINPUTS"] = pasta + os.pathsep + SRC + os.pathsep + os.path.join(SRC, "logos") + os.pathsep
    io.open(os.path.join(pasta, "vol1.tex"), "w", encoding="utf-8").write(
        MODELO % {"n": "1", "corpo": r"\chapter{Capitulo do primeiro volume}Texto.\clearpage Mais.\clearpage Mais."})
    io.open(os.path.join(pasta, "vol2.tex"), "w", encoding="utf-8").write(
        MODELO % {"n": "2", "corpo": r"\chapter{Capitulo do segundo volume}Texto."})
    for stem in ("vol1", "vol2", "vol1", "vol2", "vol1", "vol2"):
        subprocess.run(["pdflatex", "-interaction=nonstopmode", stem + ".tex"], cwd=pasta,
                       env=amb, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def texto(stem, f=None, l=None):
        cmd = ["pdftotext", "-enc", "UTF-8"]
        if f:
            cmd += ["-f", str(f), "-l", str(l or f)]
        p = subprocess.run(cmd + [os.path.join(pasta, stem + ".pdf"), "-"],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return p.stdout.decode("utf-8", "replace")

    for stem in ("vol1", "vol2"):
        if not os.path.exists(os.path.join(pasta, stem + ".pdf")):
            log = io.open(os.path.join(pasta, stem + ".log"), encoding="utf-8",
                          errors="replace").read() if os.path.exists(os.path.join(pasta, stem + ".log")) else ""
            relatar(["%s nao compilou (o comando \\volumefiles existe?): %s"
                     % (stem, [l for l in log.splitlines() if l.startswith("!")][:2])])
    t1, t2 = texto("vol1").upper(), texto("vol2").upper()
    if "CAPITULO DO SEGUNDO VOLUME" not in t1:
        problemas.append("o sumario do volume 1 nao traz o capitulo do volume 2")
    if "CAPITULO DO PRIMEIRO VOLUME" not in t2:
        problemas.append("o sumario do volume 2 nao traz o capitulo do volume 1")

    def folios(stem):
        saida = []
        n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(
            ["pdfinfo", os.path.join(pasta, stem + ".pdf")], stdout=subprocess.PIPE
        ).stdout.decode()).group(1))
        for i in range(1, n + 1):
            primeira = [l.strip() for l in texto(stem, i).splitlines() if l.strip()]
            if primeira and re.fullmatch(r"\d+", primeira[0]):
                saida.append(int(primeira[0]))
        return saida

    f1, f2 = folios("vol1"), folios("vol2")
    if not f1 or not f2:
        problemas.append("nao achei os folios dos dois volumes (%r, %r)" % (f1, f2))
    elif min(f2) <= max(f1):
        problemas.append("o volume 2 recomeca a numeracao: primeiro folio %d, e o volume 1 "
                         "termina em %d" % (min(f2), max(f1)))
finally:
    shutil.rmtree(pasta, ignore_errors=True)

relatar(problemas)
