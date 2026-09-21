# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: (desconformidade, 3.1.2) num trabalho em ingles ou espanhol, o resumo em portugues -- a lingua vernacula -- vinha DEPOIS do estrangeiro: a Norma COPPE §7 ordenava os resumos pelo idioma principal, e os exemplos em ingles, espanhol, frances e italiano seguiam a §7 (#158).

A 3.1.2 do Manual UFRJ/SiBI da a ordem: "...resumo em lingua vernacula, resumo
em lingua estrangeira...". A lingua vernacula e o portugues: a 3.1.2.1.5 faz do
resumo estrangeiro "a versao do resumo em lingua vernacula no idioma de
divulgacao internacional". O resumo em portugues vem primeiro qualquer que seja
o idioma do trabalho, e a classe confere pela lingua de cada folha, e nao pelo
ambiente: num trabalho em ingles o resumo em portugues e o foreignabstract;
num em espanhol, o brazilianabstract.

Cobra-se:
  1. na ordem certa, nenhum erro -- em portugues (abstract, foreignabstract),
     em ingles (foreignabstract, abstract) e em espanhol (brazilianabstract,
     foreignabstract, abstract);
  2. fora dela, o erro "Fora da ordem da 3.1.2", nomeando o ambiente do resumo
     em portugues e o do estrangeiro que veio antes.
"""
from medidas import Documento, relatar

MODELO = r"""\documentclass[%(opcoes)s]{ufrj}
\usepackage{ufrj-coppe}
\title{Documento de prova}
\foreigntitle{Proof document}
\author{Nome}{Sobrenome}
\advisor{Primeiro}{Orientador}{D.Sc.}{UFRJ}
\examiner{Primeiro Examinador}{D.Sc.}{UFRJ}
\department{PESC}
\date{09}{2026}
\keyword{regressao}
\foreignkeyword{regression}
\braziliankeyword{regressao}
\begin{document}
\maketitle
\frontmatter
%(resumos)s
\tableofcontents
\mainmatter
\chapter{Um}
Texto.
\end{document}
"""


def r(amb):
    return "\\begin{%s}Texto do resumo.\\end{%s}" % (amb, amb)


CERTOS = [("dsc", ["abstract", "foreignabstract"]),
          ("english,dsc", ["foreignabstract", "abstract"]),
          ("spanish,dsc", ["brazilianabstract", "foreignabstract", "abstract"])]
ERRADOS = [("dsc", ["foreignabstract", "abstract"], "abstract", "foreignabstract"),
           ("english,dsc", ["abstract", "foreignabstract"], "foreignabstract", "abstract"),
           ("spanish,dsc", ["abstract", "foreignabstract", "brazilianabstract"],
            "brazilianabstract", "foreignabstract")]

problemas = []
for opcoes, ordem in CERTOS:
    with Documento(tex=MODELO % {"opcoes": opcoes, "resumos": "\n".join(r(a) for a in ordem)}) as d:
        if "Fora da ordem" in d.log or not d.ok:
            problemas.append("%s, %s: na ordem certa, saiu erro: %s"
                             % (opcoes, " > ".join(ordem), d.erros_do_log()))
for opcoes, ordem, pt, antes in ERRADOS:
    with Documento(tex=MODELO % {"opcoes": opcoes, "resumos": "\n".join(r(a) for a in ordem)}) as d:
        colado = d.log.replace("\n", "")
        if "Fora da ordem da 3.1.2" not in d.log:
            problemas.append("%s, %s: o resumo em portugues depois do estrangeiro, e nenhum erro"
                             % (opcoes, " > ".join(ordem)))
        elif ("\\begin{%s}" % pt) not in colado or ("\\begin{%s}" % antes) not in colado:
            problemas.append("%s, %s: o erro nao nomeia \\begin{%s} e \\begin{%s}"
                             % (opcoes, " > ".join(ordem), pt, antes))

relatar(problemas)
