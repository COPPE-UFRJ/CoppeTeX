# -*- coding: utf-8 -*-
"""Teste de regressao da CoppeTeX. NAO roda na suite normal.

BUG: os verificadores liam so o trecho do .log depois do ULTIMO "LaTeX2e <",
na crenca de que o arquivo guardasse varias passadas. Nao guarda -- o pdflatex
reescreve o .log a cada passada. O que aparece duas vezes e o BANNER, que o
LaTeX repete no fim do log, logo antes do resumo de avisos. O corte jogava fora
o corpo da passada, onde estao os avisos NOMEADOS, e o verificador de
referencias cruzadas passou a aprovar qualquer coisa.

Verificador que nunca reprova e pior que verificador nenhum: parece que alguem
conferiu. Este teste monta um .log com a forma exata de um log de verdade --
banner no comeco, avisos no meio, banner de novo no fim -- e cobra que o
verificador ache os avisos.
"""
import io
import os
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
VERIFICADOR = os.path.join(RAIZ, "tools", "conferir-referencias-cruzadas.py")

LOG = """This is pdfTeX, Version 3.141592653-2.6-1.40.27 (MiKTeX 25.3)
entering extended mode
LaTeX2e <2024-11-01> patch level 2
L3 programming layer <2025-07-19>
(./exemplo.tex

LaTeX Warning: Reference `naoexiste' on page 3 undefined on input line 42.

LaTeX Warning: Citation `tambemnao' on page 3 undefined on input line 43.

[3] (./exemplo.aux)
 ***********
LaTeX2e <2024-11-01> patch level 2
L3 programming layer <2025-07-19>
 ***********

LaTeX Warning: There were undefined references.

Output written on exemplo.pdf (3 pages).
"""

problemas = []

pasta = tempfile.mkdtemp(prefix="coppe-r90-")
caminho = os.path.join(pasta, "exemplo.log")
io.open(caminho, "w", encoding="utf-8").write(LOG)

p = subprocess.run([sys.executable, VERIFICADOR, caminho],
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
saida = p.stdout.decode("utf-8", "replace")

if p.returncode == 0:
    problemas.append("o verificador APROVOU um log com duas referencias quebradas")
if "naoexiste" not in saida:
    problemas.append("a referencia indefinida nao foi nomeada na saida")
if "tambemnao" not in saida:
    problemas.append("a citacao indefinida nao foi nomeada na saida")

# E o contrario: um log limpo, com os mesmos dois banners, tem de passar.
limpo = LOG.replace("""
LaTeX Warning: Reference `naoexiste' on page 3 undefined on input line 42.

LaTeX Warning: Citation `tambemnao' on page 3 undefined on input line 43.
""", "").replace("LaTeX Warning: There were undefined references.", "")
caminho2 = os.path.join(pasta, "limpo.log")
io.open(caminho2, "w", encoding="utf-8").write(limpo)
p2 = subprocess.run([sys.executable, VERIFICADOR, caminho2],
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
if p2.returncode != 0:
    problemas.append("o verificador REPROVOU um log limpo")

try:
    os.remove(caminho)
    os.remove(caminho2)
    os.rmdir(pasta)
except OSError:
    pass

for x in problemas:
    print(x)
sys.exit(1 if problemas else 0)
