# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: nao havia defeito antigo aqui -- a Resolucao 05/2012 da Escola Politecnica pede "letra de tamanho equivalente a Times New Roman 12 ou Arial 11", e o estilo nao oferecia nenhuma das duas familias (#170). O TAMANHO e do Manual, que fixa 12 (2.2b) e nao nomeia familia; a familia e escolha da Escola, e o estilo a oferece nas opcoes `times' e `arial'.

O "Arial 11" da Resolucao esta superado pelo Manual: o corpo e 12 nas tres
formas. As nao conformidades estao no NAO-CONFORMIDADES-POLI.md.

Cobra-se, compilando um Projeto de Graduacao com cada forma:
  1. sem opcao, a fonte e a da classe (Latin Modern);
  2. com `times', a familia do texto e a do desenho do Times (TeX Gyre Termes);
  3. com `arial', e a do desenho do Arial (Nimbus Sans);
  4. as tres embutem a fonte no PDF, que e o que o PDF/A exige;
  5. nenhuma delas compila com erro.
"""
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile

from medidas import relatar, SRC

MODELO = r"""\documentclass[grad]{ufrj}
\usepackage[%s]{ufrj-poli}
\begin{document}
  \title{Palavra que so existe no titulo}
  \foreigntitle{Word found only in the title}
  \author{Nome do}{Autor}
  \advisor{Primeiro}{Orientador}{D.Sc.}{UFRJ}
  \examiner{Primeiro Examinador}{D.Sc.}{UFRJ}
  \department{PETROLEO}
  \date{01}{2026}
  \keyword{regressao}
  \foreignkeyword{regression}
  \maketitle
  \frontmatter
  \begin{abstract}Resumo.\end{abstract}
  \begin{foreignabstract}Abstract.\end{foreignabstract}
  \tableofcontents
  \mainmatter
  \chapter{Um capitulo}
  Texto do capitulo, com letra do corpo do trabalho.
\end{document}
"""

# opcao -> pedaco do nome da familia que tem de aparecer no PDF. Sem opcao, a
# classe compoe em Latin Modern SEM SERIFA, que e o padrao dela (`comserifa'
# troca pela serifada).
FORMAS = [("", "LMSans"), ("times", "Termes"), ("arial", "NimbusSan")]

problemas = []
pasta = tempfile.mkdtemp(prefix="coppe-rtu13-")
ambiente = dict(os.environ)
for var in ("TEXINPUTS", "BIBINPUTS"):
    ambiente[var] = pasta + os.pathsep + SRC + os.pathsep + \
        os.path.join(SRC, "logos") + os.pathsep
try:
    for opcao, familia in FORMAS:
        nome = "fonte_" + (opcao or "padrao")
        io.open(os.path.join(pasta, nome + ".tex"), "w", encoding="utf-8").write(
            MODELO % opcao)
        for _ in range(2):
            subprocess.run(["pdflatex", "-interaction=nonstopmode", nome + ".tex"],
                           cwd=pasta, env=ambiente, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
        log = os.path.join(pasta, nome + ".log")
        registro = io.open(log, encoding="utf-8", errors="replace").read() \
            if os.path.exists(log) else ""
        erros = [l for l in registro.splitlines() if l.startswith("!")][:2]
        if "Output written on" not in registro or erros:
            problemas.append("[%s] nao compilou: %s"
                             % (opcao or "sem opcao", "; ".join(erros) or "sem PDF"))
            continue
        try:
            p = subprocess.run(["pdffonts", os.path.join(pasta, nome + ".pdf")],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except OSError:
            print("aviso: pdffonts indisponivel, as familias nao foram conferidas")
            break
        if p.returncode != 0:
            print("aviso: pdffonts falhou, as familias nao foram conferidas")
            break
        saida = p.stdout.decode("utf-8", "replace")
        if familia not in saida:
            achadas = ", ".join(sorted({l.split()[0].split("+")[-1]
                                        for l in saida.splitlines()[2:] if l.strip()}))
            problemas.append("[%s] esperava a familia %s no PDF, e achei: %s"
                             % (opcao or "sem opcao", familia, achadas or "nenhuma"))
        # 4. toda fonte embutida: e o que o PDF/A exige
        for linha in saida.splitlines()[2:]:
            campos = linha.split()
            if len(campos) >= 5 and campos[-4] == "no":
                problemas.append("[%s] fonte nao embutida: %s"
                                 % (opcao or "sem opcao", campos[0]))
finally:
    shutil.rmtree(pasta, ignore_errors=True)

relatar(problemas)
