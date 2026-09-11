# -*- coding: utf-8 -*-
"""Teste de regressao da CoppeTeX. NAO roda na suite normal.

BUG: a pasta dist/ e a unica coisa que o aluno baixa, e nada garantia que ela
bastasse. Ela ja saiu incompleta mais de uma vez -- sem os pacotes de idioma,
sem o latexmkrc, sem o guia rapido --, e o defeito so aparecia do lado de la,
na maquina de quem foi escrever a tese. Aqui, no repositorio, tudo compila
porque src/ esta no caminho de busca do TeX e supre o que faltar.

Este teste tira essa muleta. Copia dist/ para uma pasta temporaria, aponta o
TEXINPUTS SO para ela, e compila os tres exemplos -- portugues, ingles e
espanhol. Se algum arquivo estiver faltando na entrega, falha aqui.

Demora mais que os outros: sao tres documentos com biber e duas passadas cada.
"""
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(errors="replace")
    except (ValueError, OSError):
        pass

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
DIST = os.path.join(RAIZ, "dist")

EXEMPLOS = ["example", "example_en", "example_es"]

problemas = []
pasta = tempfile.mkdtemp(prefix="coppe-r93-")
try:
    if not os.path.isdir(DIST):
        problemas.append("nao existe a pasta dist/")
    else:
        for nome in os.listdir(DIST):
            de = os.path.join(DIST, nome)
            if os.path.isfile(de):
                shutil.copy2(de, pasta)

        ambiente = dict(os.environ)
        # SO a pasta temporaria. O ";" no fim ainda deixa o TeX ver a arvore da
        # instalacao (onde estao o babel, o biblatex e os demais pacotes de
        # CTAN); o que fica de fora e o src/ deste repositorio, que e a muleta.
        ambiente["TEXINPUTS"] = pasta + ";"
        ambiente["BIBINPUTS"] = pasta + ";"

        for stem in EXEMPLOS:
            if not os.path.exists(os.path.join(pasta, stem + ".tex")):
                problemas.append("dist/ nao traz %s.tex" % stem)
                continue
            for passo in (["pdflatex", "-interaction=nonstopmode", stem + ".tex"],
                          ["biber", stem],
                          ["pdflatex", "-interaction=nonstopmode", stem + ".tex"]):
                p = subprocess.run(passo, cwd=pasta, env=ambiente,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
                # O BIBER tem de ser cobrado pelo codigo de saida dele, e nao
                # pelo do pdflatex. Faltando uma base .bib na entrega, o biber
                # reclama e sai com erro, mas o pdflatex seguinte compila assim
                # mesmo e escreve "Output written on": sai um PDF com as
                # citacoes em branco. Foi exatamente o que aconteceu -- a
                # tipos.bib ficou de fora de dist/ e este teste aprovou.
                if passo[0] == "biber" and p.returncode != 0:
                    saida = p.stdout.decode("utf-8", "replace")
                    faltou = [l.strip() for l in saida.splitlines()
                              if "not found" in l or "Cannot find" in l][:2]
                    problemas.append(
                        "%s: o biber falhou (exit %d)%s" %
                        (stem, p.returncode,
                         " -- " + "; ".join(faltou) if faltou else ""))
            log = os.path.join(pasta, stem + ".log")
            texto = ""
            if os.path.exists(log):
                texto = io.open(log, encoding="utf-8", errors="replace").read()
            # O PDF ja existia -- veio copiado de dist/ --, entao a presenca
            # dele nao prova nada. O que prova e o log da compilacao que
            # acabou de rodar.
            if "Output written on" not in texto:
                erros = [l for l in texto.splitlines() if l.startswith("!")][:3]
                problemas.append("%s nao compilou so com o que ha em dist/: %s"
                                 % (stem, "; ".join(erros) or "sem PDF de saida"))
            # Um "not found" que nomeie um arquivo NOSSO e arquivo que faltou
            # na entrega. O biblatex anuncia, em toda compilacao, que nao achou
            # o biblatex-dm.cfg -- que e opcional e de quem usa o pacote, nao
            # nosso. Cobrar todo "not found" reprovava uma compilacao correta.
            for linha in texto.splitlines():
                if "not found" not in linha:
                    continue
                if ("coppe" in linha or "ufrj" in linha
                        or "latexmkrc" in linha or ".bib" in linha):
                    problemas.append("%s: %s" % (stem, linha.strip()[:100]))
                    break

            # Citacao sem resolver e o sintoma de base .bib faltando que CHEGA
            # ao PDF: sai "[?]" na pagina e a bibliografia vem curta. O pdflatex
            # devolve zero assim mesmo.
            citacoes = re.findall(r"Citation [`'\"]([^'\"]+)['\"] on page \S+ undefined",
                                  texto)
            if citacoes:
                problemas.append(
                    "%s: %d citacao(oes) sem resolver so com o que ha em dist/"
                    " -- a primeira e `%s'" % (stem, len(citacoes), citacoes[0]))
finally:
    shutil.rmtree(pasta, ignore_errors=True)

for x in problemas:
    print(x)
sys.exit(1 if problemas else 0)
