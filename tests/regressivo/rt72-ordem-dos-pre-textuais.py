# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: (desconformidade, 3.1.2) a classe nao conferia a ordem dos elementos pre-textuais: um sumario antes das listas, uma lista de tabelas antes da de figuras ou uma dedicatoria antes da folha de aprovacao saiam como o autor escrevesse (#148).

A 3.1.2 do Manual UFRJ/SiBI da a ordem: folha de rosto, folha adicional,
errata, folha de aprovacao, dedicatoria, agradecimentos, epigrafe, resumo em
lingua vernacula, resumo em lingua estrangeira, lista de ilustracoes, lista de
tabelas, lista de abreviaturas e siglas, lista de simbolos e sumario. Os
modelos ensinavam a ordem das listas errada, e a classe nao dizia nada. Agora,
entre o \\maketitle e o \\mainmatter, um elemento fora da ordem e erro, com a
mensagem dizendo o que mover; e a falta do sumario, que a 3.1.2.1.6 exige, e
aviso.

Cobra-se:
  1. na ordem certa, nenhum erro;
  2. \\tableofcontents antes de \\listoftables, \\listoftables antes de
     \\listoffigures, \\printlosymbols antes de \\printloabbreviations, e
     \\dedication antes do \\frontmatter: erro "Fora da ordem da 3.1.2", que
     nomeia os dois comandos;
  3. \\epigrafe na abertura de um capitulo, depois do \\mainmatter, e aceita
     (3.1.2.2.3);
  4. sem \\tableofcontents, o aviso de que o sumario falta.
"""
from medidas import Documento, relatar

MODELO = r"""\documentclass[dsc]{ufrj}
\usepackage{ufrj-coppe}
\title{Documento de prova}
\author{Nome}{Sobrenome}
\advisor{Primeiro}{Orientador}{D.Sc.}{UFRJ}
\examiner{Primeiro Examinador}{D.Sc.}{UFRJ}
\department{PESC}
\date{09}{2026}
\keyword{regressao}
\makelosymbols
\makeloabbreviations
\begin{document}
\maketitle
%(antes)s
\frontmatter
%(pre)s
\mainmatter
\chapter{Um}
%(corpo)s
Texto.
\end{document}
"""

CERTO = r"""\dedication{A alguem.}
\chapter*{Agradecimentos}
Obrigado.
\epigrafe{Uma frase.}{Autor}
\listoffigures
\listofquadros
\listoftables
\printloabbreviations
\printlosymbols
\tableofcontents
"""

ERRADOS = [
    ("", r"\tableofcontents" "\n" r"\listoftables", r"\listoftables", r"\tableofcontents"),
    ("", r"\listoftables" "\n" r"\listoffigures", r"\listoffigures", r"\listoftables"),
    ("", r"\printlosymbols" "\n" r"\printloabbreviations" "\n" r"\tableofcontents",
     r"\printloabbreviations", r"\printlosymbols"),
    (r"\dedication{A alguem.}", r"\tableofcontents", r"\frontmatter", r"\dedication"),
]


def compila(antes="", pre="", corpo=""):
    return Documento(tex=MODELO % {"antes": antes, "pre": pre, "corpo": corpo},
                     makeindex=True)


problemas = []

with compila(pre=CERTO, corpo=r"\epigrafe{Outra frase.}{Outro autor}") as d:
    erros = [l for l in d.log.splitlines() if "Fora da ordem" in l]
    if erros or not d.ok:
        problemas.append("na ordem certa, com epigrafe depois do \\mainmatter, saiu erro: %s"
                         % (erros or d.erros_do_log()))
    if "Falta o sumario" in d.log:
        problemas.append("com \\tableofcontents, a classe avisou que falta o sumario")

for antes, pre, cmd, anterior in ERRADOS:
    with compila(antes=antes, pre=pre) as d:
        # o TeX quebra a linha do log na coluna 79, no meio da palavra: os
        # nomes dos comandos se procuram no log sem as quebras
        colado = d.log.replace("\n", "")
        if "Fora da ordem da 3.1.2" not in d.log:
            problemas.append("%s depois de %s: nenhum erro de ordem" % (cmd, anterior))
        elif cmd not in colado or anterior not in colado:
            problemas.append("%s depois de %s: o erro nao nomeia os dois comandos"
                             % (cmd, anterior))

with compila(pre=r"\listoffigures") as d:
    if "Falta o sumario" not in d.log:
        problemas.append("sem \\tableofcontents, nenhum aviso de que falta o sumario")

relatar(problemas)
