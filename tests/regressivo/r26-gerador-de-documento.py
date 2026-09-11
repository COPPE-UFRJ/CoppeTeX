# -*- coding: utf-8 -*-
"""Teste de regressao da CoppeTeX. NAO roda na suite normal.

BUG: nao ha defeito antigo aqui -- este teste nasce junto com o gerador, e o
motivo de existir e que um gerador de documento erra de um jeito particular:
ele produz um arquivo que PARECE certo e so quebra quando alguem compila. Quem
gera nao compila, e quem compila e o aluno, na vespera.

O teste gera dois documentos e COMPILA os dois, so com o que ha na entrega:

  1. o padrao, que e o que sai de quem aperta Gerar sem mexer em nada;
  2. um com tudo ligado ao mesmo tempo -- capitulos em arquivos separados,
     apendices, anexos, glossario, indice remissivo e todas as listas --,
     que e onde as opcoes se atrapalham entre si, se e que se atrapalham.

Cobra compilacao limpa nos dois: biber sem erro, PDF escrito, nenhuma citacao
sem resolver e nenhum aviso alem do que a classe emite de proposito.
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
GERADOR = os.path.join(RAIZ, "tools", "geradocvazio.py")

# O unico aviso que a classe emite de proposito em toda compilacao no pdfTeX.
ESPERADOS = ["you should try compiling with LuaLaTeX"]

CASOS = [
    ("padrao", []),
    ("completo", ["--conteudo=sim", "--tipo=msc", "--programa=PEM",
                  "--n_apendices=2", "--n_anexos=1", "--n_coorientadores=1",
                  "--glossario=sim", "--indice=sim",
                  "--listofquadros=sim", "--listofprogramas=sim",
                  "--listofalgorithms=sim"]),
]

problemas = []

for nome, extras in CASOS:
    pasta = tempfile.mkdtemp(prefix="coppe-r26-")
    try:
        p = subprocess.run([sys.executable, GERADOR, "--gerar",
                            "--pasta=" + pasta] + extras,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if p.returncode != 0:
            problemas.append("%s: o gerador falhou -- %s"
                             % (nome, p.stdout.decode("utf-8", "replace")[-200:]))
            continue
        if not os.path.exists(os.path.join(pasta, "main.tex")):
            problemas.append("%s: nao saiu o main.tex" % nome)
            continue

        # A entrega inteira ao lado, que e o que a documentacao manda fazer.
        for raiz, _, nomes in os.walk(DIST):
            destino = os.path.join(pasta, os.path.relpath(raiz, DIST))
            if not os.path.isdir(destino):
                os.makedirs(destino)
            for arq in nomes:
                shutil.copy2(os.path.join(raiz, arq),
                             os.path.join(destino, arq))

        ambiente = dict(os.environ)
        ambiente["TEXINPUTS"] = pasta + ";"
        ambiente["BIBINPUTS"] = pasta + ";"

        def roda(*cmd):
            return subprocess.run(list(cmd), cwd=pasta, env=ambiente,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT)

        roda("pdflatex", "-interaction=nonstopmode", "main.tex")
        b = roda("biber", "main")
        if b.returncode != 0:
            problemas.append("%s: o biber falhou (exit %d)" % (nome, b.returncode))
        ist = os.path.join(pasta, "coppe.ist")
        for ext, saida in (("abx", "lab"), ("syx", "los")):
            if os.path.exists(os.path.join(pasta, "main." + ext)):
                roda("makeindex", "-s", ist, "-o", "main." + saida,
                     "main." + ext)
        if os.path.exists(os.path.join(pasta, "main.idx")):
            roda("makeindex", "main.idx")
        for _ in range(2):
            roda("pdflatex", "-interaction=nonstopmode", "main.tex")

        log = os.path.join(pasta, "main.log")
        texto = io.open(log, encoding="utf-8", errors="replace").read() \
            if os.path.exists(log) else ""
        if "Output written on" not in texto:
            erros = [l for l in texto.splitlines() if l.startswith("!")][:3]
            problemas.append("%s: nao compilou -- %s"
                             % (nome, "; ".join(erros) or "sem PDF"))
            continue

        citacoes = re.findall(
            r"Citation [`'\"]([^'\"]+)['\"] on page \S+ undefined", texto)
        if citacoes:
            problemas.append("%s: citacao sem resolver -- `%s'"
                             % (nome, citacoes[0]))

        # Nenhum aviso alem dos declarados. Um documento que a ferramenta
        # escreve nao tem desculpa para sair com aviso: quem o recebe nao sabe
        # se o aviso e dele ou da ferramenta.
        for linha in texto.splitlines():
            if "Warning" not in linha or "Package: " in linha:
                continue
            if any(e in linha for e in ESPERADOS):
                continue
            problemas.append("%s: aviso inesperado -- %s"
                             % (nome, linha.strip()[:90]))
            break
    finally:
        shutil.rmtree(pasta, ignore_errors=True)

# A opcao de baixar a classe do GitHub NAO e exercitada aqui: um teste que
# depende da rede falha no avia~o, no proxy da universidade e no dia em que o
# GitHub estiver fora, e um teste que falha por motivo alheio deixa de ser lido.
# O que da para cobrar sem rede e a REGRA de o que vem e o que nao vem -- se ela
# mudar sem querer, o aluno recebe um exemplo junto do documento em branco que
# pediu, ou pior, fica sem a classe.
sys.path.insert(0, os.path.join(RAIZ, "tools"))
try:
    import geradocvazio
except ImportError as e:
    problemas.append("nao consegui importar o gerador: %s" % e)
else:
    if not any(c[0] == "baixar" for c in geradocvazio.CAMPOS):
        problemas.append("sumiu a opcao de baixar a classe do GitHub")
    for precisa in ("coppe.cls", "coppe.ist", "latexmkrc",
                    "brazilian-coppe.lbx", "coppe-logo.pdf"):
        if not geradocvazio._serve_para_compilar(precisa):
            problemas.append("o download deixaria de trazer %s" % precisa)
    for nao_precisa in ("example.tex", "example_en.pdf", "tipos.bib",
                        "README.md", "coppe.dtx"):
        if geradocvazio._serve_para_compilar(nao_precisa):
            problemas.append("o download traria %s, que nao serve a um"
                             " documento em branco" % nao_precisa)

for x in problemas:
    print(x)
sys.exit(1 if problemas else 0)
