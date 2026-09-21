# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: (ferramentas e dados) os .bib gerados do ufrj.dtx, a base das adversativas e o .bib do gerador de documento tinham comentarios com % -- o preambulo do docstrip, o gabarito das referencias do Manual dentro das proprias entradas e as divergencias aceitas --, e o JabRef e outros gerenciadores de referencias nao entendem o % como comentario (#164).

A BibTeX e o biber toleram o %, e por isso ninguem via. Quem abre a base num
gerenciador de referencias ve lixo, ou perde as linhas. Desde a #164 os .bib so
tem @Comment: o gabarito e um @comment{Manual: ...} LOGO ANTES da entrada, e a
divergencia aceita um @comment{Divergencia aceita: ...}.

Cobra-se, sem compilar:
  1. nenhuma linha comecada por % nos tres .bib que o ufrj.ins gera
     (exemplo.bib, manual.bib, ufrj.bib), na base das adversativas e no .bib
     que o tools/geradocvazio.py escreve;
  2. que o tools/conferir-referencias.py leia o gabarito novo: as 34 categorias
     da secao 4.2 em cada uma das duas bases, e as divergencias aceitas;
  3. que o .bib do gerador escreva os acentos em UTF-8, e nao como \\'i.
"""
import importlib.util
import os
from medidas import relatar, SRC

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(AQUI, "..", ".."))
ADV = os.path.join(RAIZ, "tests", "adversativa", "referencias-manual.bib")


def carrega(nome, caminho):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


problemas = []

# 1. nenhuma linha de comentario com %
bases = [os.path.join(SRC, n) for n in ("exemplo.bib", "manual.bib", "ufrj.bib")] + [ADV]
gera = carrega("geradocvazio", os.path.join(RAIZ, "tools", "geradocvazio.py"))
textos = [(os.path.basename(b), open(b, encoding="utf-8").read()) for b in bases]
textos.append(("o .bib do gerador", gera.monta_bib(gera.padroes())))
for nome, texto in textos:
    ruins = [(n, l) for n, l in enumerate(texto.splitlines(), 1) if l.lstrip().startswith("%")]
    if ruins:
        n, l = ruins[0]
        problemas.append("%s: %d linha(s) comecada(s) por %%, a primeira na %d: %r"
                         % (nome, len(ruins), n, l.strip()[:70]))

# 2. o gabarito novo e lido
confere = carrega("conferir_referencias", os.path.join(RAIZ, "tools", "conferir-referencias.py"))
for base, prefixo in ((os.path.join(SRC, "exemplo.bib"), "m-"), (ADV, "pt-")):
    gab = {k: v for k, v in confere.gabaritos(base).items() if k.startswith(prefixo)}
    if len(gab) != 34:
        problemas.append("%s: o conferir-referencias leu %d gabaritos %s*, e sao 34"
                         % (os.path.basename(base), len(gab), prefixo))
    aceitas = [k for k, (ref, mot, classe) in gab.items() if mot]
    if not aceitas:
        problemas.append("%s: nenhuma divergencia aceita lida" % os.path.basename(base))

# 3. acentos do .bib do gerador
bib = gera.monta_bib(gera.padroes())
if "\\'" in bib or "\\~" in bib or "\\c{" in bib:
    problemas.append("o .bib do gerador ainda escreve acento em LaTeX (\\'i), e nao em UTF-8")

relatar(problemas)
