# -*- coding: utf-8 -*-
"""Teste de regressao da CoppeTeX. NAO roda na suite normal.

BUG: a distribuicao (hoje dist-coppe, dist-poli e dist-biblatex) e a unica
coisa que o aluno baixa, e nada garantia que ela
bastasse. Ela ja saiu incompleta mais de uma vez -- sem os pacotes de idioma,
sem o latexmkrc, sem o guia rapido, sem a tipos.bib --, e o defeito so aparecia
do lado de la, na maquina de quem foi escrever a tese. Aqui, no repositorio,
tudo compila porque src/ esta no caminho de busca do TeX e supre o que faltar.

Este teste tira essa muleta. Copia a arvore de dist/ para uma pasta temporaria,
aponta o TEXINPUTS SO para ela, e compila. Se algum arquivo estiver faltando na
entrega, falha aqui.

E cobra tambem a ARRUMACAO, que tem uma regra so: o que esta na raiz de dist/
funciona sem voce mexer em nada. O resto da classe mora em coppetex/, que a
propria classe poe no \\input@path -- o TEXINPUTS daqui aponta so para a raiz,
sem //, e por isso o teste cobra tambem esse mecanismo. Os exemplos em ingles e
espanhol estao em exemplos/, e a documentacao manda trazer o .tex para a raiz:
o teste compila os dois exemplos em portugues onde eles estao, e os outros dois
depois de fazer isso. Se a instrucao estiver errada, falha aqui.

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
# Por distribuicao: (documento, pasta cujo conteudo tem de vir para a raiz
# antes de compilar). Cada dist-* tem de bastar sozinha.
EXEMPLOS = {
    "dist-coppe": [("coppe-min-exemplo", None), ("coppe-max-exemplo", None),
                   ("example_en", "exemplos"), ("example_es", "exemplos")],
    "dist-poli": [("poli-min-exemplo", None), ("poli-max-exemplo", None)],
    "dist-biblatex": [("exemplo-biblatex", None)],
}

problemas = []


def compila(pasta, stem, ambiente, nome="dist"):
    """Compila e devolve a lista de problemas daquele documento."""
    achados = []
    for passo in (["pdflatex", "-interaction=nonstopmode", stem + ".tex"],
                  ["biber", stem],
                  ["pdflatex", "-interaction=nonstopmode", stem + ".tex"]):
        p = subprocess.run(passo, cwd=pasta, env=ambiente,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # O BIBER tem de ser cobrado pelo codigo de saida DELE, e nao pelo do
        # pdflatex. Faltando uma base .bib na entrega, o biber reclama e sai com
        # erro, mas o pdflatex seguinte compila assim mesmo e escreve "Output
        # written on": sai um PDF com as citacoes em branco. Foi exatamente o
        # que aconteceu -- a tipos.bib ficou de fora e este teste aprovou.
        if passo[0] == "biber" and p.returncode != 0:
            saida = p.stdout.decode("utf-8", "replace")
            faltou = [l.strip() for l in saida.splitlines()
                      if "not found" in l or "Cannot find" in l][:2]
            achados.append("%s: o biber falhou (exit %d)%s"
                           % (stem, p.returncode,
                              " -- " + "; ".join(faltou) if faltou else ""))

    log = os.path.join(pasta, stem + ".log")
    texto = io.open(log, encoding="utf-8", errors="replace").read() \
        if os.path.exists(log) else ""
    # O PDF pode ja existir, vindo copiado da entrega, entao a presenca dele nao
    # prova nada. O que prova e o log da compilacao que acabou de rodar.
    # O PDF sai mesmo com erro, em nonstopmode: erro no log reprova, e nao
    # so a falta de PDF. O r24 e o r25 passavam assim com os resumos fora da
    # ordem (#158).
    erros = [l for l in texto.splitlines() if l.startswith("!")][:3]
    if "Output written on" not in texto or erros:
        achados.append(("%s nao compilou so com o que ha em " + nome + "/: %s")
                       % (stem, "; ".join(erros) or "sem PDF de saida"))

    # Um "not found" que nomeie um arquivo NOSSO e arquivo que faltou na
    # entrega. O biblatex anuncia, em toda compilacao, que nao achou o
    # biblatex-dm.cfg -- que e opcional e de quem usa o pacote, nao nosso.
    for linha in texto.splitlines():
        if "not found" not in linha:
            continue
        if ("coppe" in linha or "ufrj" in linha or "latexmkrc" in linha
                or ".bib" in linha):
            achados.append("%s: %s" % (stem, linha.strip()[:100]))
            break

    # Citacao sem resolver e o sintoma de base .bib faltando que CHEGA ao PDF:
    # sai "[?]" na pagina e a bibliografia vem curta.
    citacoes = re.findall(
        r"Citation [`'\"]([^'\"]+)['\"] on page \S+ undefined", texto)
    if citacoes:
        achados.append(("%s: %d citacao(oes) sem resolver so com o que ha em"
                        " " + nome + "/ -- a primeira e `%s'")
                       % (stem, len(citacoes), citacoes[0]))
    return achados


for nome_dist, exemplos in sorted(EXEMPLOS.items()):
    DIST = os.path.join(RAIZ, nome_dist)
    if not os.path.isdir(DIST):
        problemas.append("nao existe a pasta %s/" % nome_dist)
    else:
        for stem, subpasta in exemplos:
            pasta = tempfile.mkdtemp(prefix="coppe-r93-")
            try:
                # A arvore INTEIRA, e nao so os arquivos da raiz: os logotipos, os
                # manuais e os exemplos por idioma estao em subpastas.
                for raiz, _, nomes in os.walk(DIST):
                    destino = os.path.join(pasta, os.path.relpath(raiz, DIST))
                    if not os.path.isdir(destino):
                        os.makedirs(destino)
                    for nome in nomes:
                        shutil.copy2(os.path.join(raiz, nome),
                                     os.path.join(destino, nome))

                # A instrucao que a documentacao da: traga para a raiz o conteudo da
                # pasta do idioma.
                if subpasta:
                    de = os.path.join(pasta, subpasta)
                    if not os.path.isdir(de):
                        problemas.append("%s/ nao traz a pasta %s/" % (nome_dist, subpasta))
                        continue
                    for nome in os.listdir(de):
                        shutil.copy2(os.path.join(de, nome),
                                     os.path.join(pasta, nome))

                if not os.path.exists(os.path.join(pasta, stem + ".tex")):
                    problemas.append("%s/ nao traz %s.tex" % (nome_dist, stem))
                    continue

                ambiente = dict(os.environ)
                # SO a pasta temporaria. O ";" no fim ainda deixa o TeX ver a arvore
                # da instalacao (babel, biblatex e os demais pacotes de CTAN); o que
                # fica de fora e o src/ deste repositorio, que e a muleta.
                ambiente["TEXINPUTS"] = pasta + ";"
                ambiente["BIBINPUTS"] = pasta + ";"
                problemas += compila(pasta, stem, ambiente, nome_dist)
            finally:
                shutil.rmtree(pasta, ignore_errors=True)

for x in problemas:
    print(x)
sys.exit(1 if problemas else 0)
