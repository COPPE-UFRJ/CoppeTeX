# -*- coding: utf-8 -*-
"""Teste de regressao da CoppeTeX. NAO roda na suite normal.

BUG: o glossario so existia escrito a mao, o indice punha as palavras acentuadas
depois do z, e sem latexmk as listas e o indice saiam vazios. Tres defeitos,
cobrados juntos porque dividem o mesmo caminho (makeindex):

1. O glossario so existia escrito a mao (theglossary), na ordem em que o autor
   digitava. Agora ha a forma automatica: \\makeglossarylist, \\glossaryterm e
   \\printglossarylist, em ordem alfabetica.
2. O makeindex ordena por BYTES, e em UTF-8 toda letra acentuada vinha depois
   do z: "Arvore", "etica" e "indice" saiam no fim do indice, depois de
   "Zebra". A NBR 6034 pede ordem alfabetica. A classe da a chave sem acento a
   cada nivel da entrada que nao tem chave propria; a chave do autor vence.
3. No TeXstudio, que roda so o pdflatex, as listas e o indice saiam vazios. A
   classe roda o makeindex sozinha no fim da compilacao (shell escape
   restrito); a opcao semmakeindex desliga.

Nenhum passo deste teste roda o makeindex por fora: e isso que se cobra.
"""
import io
import os
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
SRC = os.path.join(RAIZ, "src")

DOC = r"""\documentclass[dsc%(opcoes)s]{ufrj}
\usepackage{ufrj-coppe}
%(preambulo)s
\title{Glossario e indice}
\foreigntitle{Glossary and index}
\author{Nome}{Sobrenome}
\advisor{Primeiro}{Orientador}{D.Sc.}{UFRJ}
\examiner{Primeiro Examinador}{D.Sc.}{UFRJ}
\department{PESC}
\date{09}{2026}
\keyword{Regressao}
\begin{document}
  \mainmatter
  \chapter{Um}
  Texto.%(texto)s
  \backmatter
  %(fim)s
\end{document}
"""

TERMOS = r"""
  \glossaryterm{Zebra}{um animal listrado.}
  \glossaryterm{Árvore}{uma planta lenhosa.}
  \glossaryterm{abacate}{uma fruta.}
  \index{Zebra}\index{índice}\index{ação}\index{ação!rápida}\index{acaso}
  \index{Árvore}\index{ética|see{moral}}\index{citação}\index{zz@índice manual}
"""


def compila(opcoes="", preambulo="", texto=TERMOS, fim="", passadas=2):
    pasta = tempfile.mkdtemp(prefix="coppe-r99-")
    try:
        doc = DOC % {"opcoes": opcoes, "preambulo": preambulo,
                     "texto": texto, "fim": fim}
        io.open(os.path.join(pasta, "g.tex"), "w", encoding="utf-8").write(doc)
        # O ufrj.ist vai ao lado do documento, como na pasta do aluno: o
        # makeindex procura o estilo ali e na arvore do TeX, e nao no TEXINPUTS.
        shutil.copy(os.path.join(SRC, "ufrj.ist"), pasta)
        amb = dict(os.environ)
        amb["TEXINPUTS"] = pasta + os.pathsep + SRC + os.pathsep
        for _ in range(passadas):
            subprocess.run(["pdflatex", "-interaction=nonstopmode", "g.tex"],
                           cwd=pasta, env=amb, stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL)

        def ler(ext):
            c = os.path.join(pasta, "g." + ext)
            return io.open(c, encoding="utf-8", errors="replace").read() \
                if os.path.exists(c) else None
        pdf = os.path.join(pasta, "g.pdf")
        txt = subprocess.run(["pdftotext", "-enc", "UTF-8", pdf, "-"],
                             stdout=subprocess.PIPE, stderr=subprocess.DEVNULL
                             ).stdout.decode("utf-8", "replace") \
            if os.path.exists(pdf) else ""
        return {"log": ler("log") or "", "lgs": ler("lgs"), "ind": ler("ind"),
                "idx": ler("idx") or "", "pdf": txt}
    finally:
        shutil.rmtree(pasta, ignore_errors=True)


def em_ordem(texto, palavras):
    pos = [texto.find(p) for p in palavras]
    return -1 not in pos and pos == sorted(pos)


problemas = []

def erros(nome, r):
    e = [l for l in r["log"].splitlines() if l.startswith("! ")]
    if e:
        problemas.append("%s: erro -- %s" % (nome, e[0][:90]))
    if r["log"].find("restricted \\write18 enabled") < 0 \
            and r["log"].find("\\write18 enabled") < 0:
        problemas.append("%s: shell escape desligado nesta maquina; o teste "
                         "nao prova nada" % nome)

# --- automatico, com makeidx: so pdflatex duas vezes -----------------------
r = compila(preambulo=r"\makeglossarylist\usepackage{makeidx}\makeindex",
            fim=r"\printglossarylist\printindex")
erros("automatico", r)
if r["lgs"] is None:
    problemas.append("automatico: a classe nao rodou o makeindex do glossario")
elif not em_ordem(r["lgs"], ["abacate", "Árvore", "Zebra"]):
    problemas.append("automatico: glossario fora da ordem alfabetica")
if r["ind"] is None:
    problemas.append("automatico: a classe nao rodou o makeindex do indice")
else:
    if not em_ordem(r["ind"], ["ação", "rápida", "acaso", "Árvore", "citação",
                               "ética", "índice", "Zebra", "índice manual"]):
        problemas.append("automatico: indice fora da ordem alfabetica -- %s"
                         % " / ".join(l.strip() for l in r["ind"].splitlines()
                                      if "item" in l))
for titulo in ("GLOSSÁRIO", "ÍNDICE REMISSIVO"):
    if titulo not in r["pdf"].upper():
        problemas.append("automatico: o PDF nao tem %s" % titulo)
if "definição" in r["pdf"] or "uma planta lenhosa" not in r["pdf"]:
    problemas.append("automatico: as definicoes do glossario nao sairam no PDF")
# As remissivas da NBR 6034 sao "ver" e "ver tambem"; o babel dava "veja".
if "ética, ver moral" not in r["pdf"]:
    problemas.append("automatico: a remissiva nao saiu como 'ver'")
if "zz@índice manual" not in r["idx"]:
    problemas.append("automatico: a chave do autor nao foi respeitada")

# --- imakeidx: a chave vale tambem ----------------------------------------
r = compila(preambulo=r"\usepackage{imakeidx}\makeindex", fim=r"\printindex",
            texto=r"\index{Zebra}\index{Árvore}\index{ação}\index{acaso}")
erros("imakeidx", r)
if r["ind"] is None or not em_ordem(r["ind"], ["ação", "acaso", "Árvore", "Zebra"]):
    problemas.append("imakeidx: indice fora da ordem alfabetica")

# --- semmakeindex: a classe nao roda nada ---------------------------------
r = compila(opcoes=",semmakeindex",
            preambulo=r"\makeglossarylist\usepackage{makeidx}\makeindex",
            fim=r"\printglossarylist\printindex")
erros("semmakeindex", r)
if r["lgs"] is not None or r["ind"] is not None:
    problemas.append("semmakeindex: a classe rodou o makeindex mesmo assim")

# --- \glossaryterm sem \makeglossarylist: aviso, nao erro ------------------
r = compila(preambulo="", texto=r"\glossaryterm{Termo}{definicao}", fim="")
erros("sem makeglossarylist", r)
if "sem \\makeglossarylist" not in r["log"].replace("\n", ""):
    problemas.append("sem makeglossarylist: a classe nao avisou")

# --- manual: theglossary continua funcionando -----------------------------
r = compila(texto="", fim=r"\begin{theglossary}\item[Termo] definida a mao.\end{theglossary}")
erros("manual", r)
if "definida a mao" not in r["pdf"] or "GLOSSÁRIO" not in r["pdf"].upper():
    problemas.append("manual: o theglossary nao saiu")

for x in problemas:
    print(x)
sys.exit(1 if problemas else 0)
