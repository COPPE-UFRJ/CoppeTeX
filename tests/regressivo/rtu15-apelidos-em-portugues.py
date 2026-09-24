# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: nao havia defeito antigo aqui -- este teste guarda a regra dos DOIS NOMES da 5.0. Todo comando que a classe cria tem nome em ingles, que carrega o codigo, e apelido em portugues, e os dois fazem exatamente a mesma coisa. Ate a 5.0 os apelidos estavam espalhados pelo codigo, cada um ao lado da sua definicao, e onze comandos tinham o codigo no nome em portugues: um comando novo nascia com um nome so e ninguem percebia.

Cobra-se:
  1. o mesmo trabalho escrito TODO em portugues e TODO em ingles sai com o
     mesmo texto, folha por folha -- e o que prova que o apelido nao e um
     comando parecido, mas o mesmo comando;
  2. os dois nomes de cada par existem no ufrj.cls gerado;
  3. os apelidos estao todos no bloco unico do fim da classe, e nenhum par foi
     declarado fora dele -- quem cobra isso e o tools/conferir-manual.py, que
     este teste chama.
"""
import os
import re
import subprocess
import sys

from medidas import Documento, normaliza, relatar, SRC

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))

problemas = []

# --------------------------------------------------------------------------
# 1. o mesmo trabalho nos dois idiomas de comando
# --------------------------------------------------------------------------
MODELO = r"""\documentclass[dsc]{ufrj}
\usepackage{ufrj-coppe}
%% As quatro listas e a declaracao de sigla so valem no preambulo.
\%(makelosiglas)s
\%(makeloabreviaturas)s
\%(makelosimbolos)s
\%(makelistaglossario)s
\%(newsigla)s{ufrj}{UFRJ}{Universidade Federal do Rio de Janeiro}
\begin{document}
\title{Palavra que so existe no titulo}
\%(tituloestrangeiro)s{Word found only in the title}
\author{Nome do}{Autor}
\%(orientador)s{Primeiro}{Orientador}{D.Sc.}{UFRJ}
\%(coorientador)s{Segundo}{Coorientador}{D.Sc.}{UFRJ}
\%(examinador)s{Primeiro Examinador}{D.Sc.}{UFRJ}
\%(departamento)s{PESC}
\date{09}{2026}
\%(dataaprovacao)s{1 de janeiro de 2026}
\%(areaconcentracao)s{Area declarada no teste}
\%(linhapesquisa)s{Linha declarada no teste}
\%(nomeprojeto)s{Projeto declarado no teste}
\%(agenciafomento)s{CNPq}{Bolsa de doutorado}
\%(palavrachave)s{regressao}
\%(palavrachaveestrangeira)s{regression}
\%(cidade)s{Macae}
\%(estado)s{RJ}
\%(pais)s{Brasil}
\%(universidade)s{Universidade Federal do Rio de Janeiro}
\maketitle
\frontmatter
\%(dedicatoria)s{A quem leu o manual ate o fim.}
\begin{abstract}Resumo do teste dos apelidos.\end{abstract}
\begin{foreignabstract}Abstract of the alias test.\end{foreignabstract}
\%(printloabreviaturas)s
\%(printlosiglas)s
\%(printlosimbolos)s
\tableofcontents
\mainmatter
\chapter{Capitulo do teste}
A \%(sigla)s{ufrj} aparece uma vez com a forma completa.
A \%(abreviatura)s{Prof.}{Professor} e a \%(acronimo)s{PESC}{Programa de
Engenharia de Sistemas e Computacao} vao para as listas, e o
\%(simbolo)s{$\alpha$}{coeficiente de teste} tambem. O
\%(termoglossario)s{termo do teste}{o que este teste prova} entra no glossario.

\begin{figure}[htbp]
  \caption{Legenda da ilustracao do teste}
  \%(largurailustracao)s{4cm}
  \centering\rule{4cm}{1cm}
  \%(fonte)s{Autor, 2026}
\end{figure}

\%(anexo)s
\chapter{Anexo do teste}
Texto do anexo.
\backmatter
\%(printlistaglossario)s
\end{document}
"""

INGLES = {
    "tituloestrangeiro": "foreigntitle", "orientador": "advisor",
    "coorientador": "coadvisor", "examinador": "examiner",
    "departamento": "department", "dataaprovacao": "approvaldate",
    "areaconcentracao": "concentrationarea", "linhapesquisa": "researchline",
    "nomeprojeto": "projectname", "agenciafomento": "fundingagency",
    "palavrachave": "keyword", "palavrachaveestrangeira": "foreignkeyword",
    "cidade": "city", "estado": "state", "pais": "country",
    "universidade": "university", "makelosiglas": "makeloacronyms",
    "makeloabreviaturas": "makeloabbreviations",
    "makelosimbolos": "makelosymbols", "makelistaglossario": "makeglossarylist",
    "newsigla": "defineacronym", "dedicatoria": "dedication",
    "printloabreviaturas": "printloabbreviations",
    "printlosiglas": "printloacronyms", "printlosimbolos": "printlosymbols",
    "sigla": "useacronym", "abreviatura": "abbrev", "acronimo": "acron",
    "simbolo": "symbl", "termoglossario": "glossaryterm",
    "largurailustracao": "illustrationwidth", "fonte": "source",
    "anexo": "annex", "printlistaglossario": "printglossarylist",
}
PORTUGUES = dict((chave, chave) for chave in INGLES)

textos = {}
for idioma, nomes in (("portugues", PORTUGUES), ("ingles", INGLES)):
    with Documento(tex=MODELO % nomes, makeindex=True, nome="apelidos") as d:
        if not d.ok:
            problemas.append("[%s] nao compilou: %s"
                             % (idioma, d.erros_do_log(2) or "sem PDF"))
            textos[idioma] = None
            continue
        textos[idioma] = [normaliza(d.texto(p))
                          for p in range(1, d.n_paginas() + 1)]

if textos.get("portugues") and textos.get("ingles"):
    pt, en = textos["portugues"], textos["ingles"]
    if len(pt) != len(en):
        problemas.append("o documento em portugues tem %d folha(s) e o em ingles %d"
                         % (len(pt), len(en)))
    for i, (a, b) in enumerate(zip(pt, en), 1):
        if a != b:
            problemas.append("a folha %d difere entre os dois idiomas de comando:\n"
                             "  portugues: %s\n  ingles   : %s" % (i, a[:200], b[:200]))
            break

# --------------------------------------------------------------------------
# 2. os dois nomes de cada par existem no .cls gerado
# --------------------------------------------------------------------------
cls = open(os.path.join(SRC, "ufrj.cls"), encoding="utf-8", errors="replace").read()
for pt_nome, en_nome in sorted(INGLES.items()):
    for nome in (pt_nome, en_nome):
        if not re.search(r"\\%s\b" % nome, cls):
            problemas.append("\\%s nao existe no ufrj.cls gerado" % nome)

# --------------------------------------------------------------------------
# 3. a regra do bloco unico, cobrada pelo conferir-manual
# --------------------------------------------------------------------------
p = subprocess.run([sys.executable, os.path.join(RAIZ, "tools", "conferir-manual.py")],
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=RAIZ)
saida = p.stdout.decode("utf-8", "replace")
if p.returncode != 0:
    problemas.append("o conferir-manual.py reprovou:\n%s"
                     % "\n".join(l for l in saida.splitlines() if l.startswith("ERRO")
                                 or l.startswith("        "))[:600])
elif "dois nomes" not in saida:
    problemas.append("o conferir-manual.py nao esta cobrando a regra dos dois nomes")

relatar(problemas)
