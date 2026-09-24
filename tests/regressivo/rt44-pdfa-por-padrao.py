# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: (desconformidade por padrao, 2.2d) sem a opcao pdfa, a classe gera PDF comum, e o arquivo de deposito tem de ser PDF/A; o gerador de documento vazio tambem vem com pdfa DESLIGADO e diz "ligue ao depositar", o contrario do que o coppe-max-exemplo recomenda (#124).

A 2.2(d) do Manual UFRJ/SiBI exige a versao digital final em PDF/A. A opcao
`pdfa' ja produz PDF/A-2b conforme pelo veraPDF, o custo de tempo e desprezivel
(TODO.md, secao 3), e os dois exemplos ja a usam. Deixa-la desligada por padrao
faz o documento de quem nao leu o manual sair fora da norma, e o gerador de
documento vazio -- que e a porta de entrada do aluno -- reforca isso.

Cobra-se:
  1. um documento SEM opcao nenhuma alem do tipo sai com a identificacao PDF/A
     (pdfaid) no XMP;
  2. a opcao `sempdfa' desliga (o PDF sai sem pdfaid);
  3. no gerador (tools/geradocvazio.py), o campo pdfa vem ligado por padrao.
"""
import io
import os
import re
from medidas import Documento, relatar, RAIZ

problemas = []

for opcoes, espera in (("dsc", True), ("dsc,sempdfa", False)):
    with Documento(opcoes=opcoes, pre=r"\begin{abstract}Resumo.\end{abstract}",
                   corpo=r"\chapter{Um}Texto.", passadas=3) as d:
        if not d.ok:
            problemas.append("%s: nao compilou: %s" % (opcoes, d.erros_do_log()))
            continue
        tem = b"pdfaid" in open(d.pdf, "rb").read()
        if tem != espera:
            problemas.append("[%s] PDF/A: %s, esperado %s"
                             % (opcoes, "sim" if tem else "nao", "sim" if espera else "nao"))

gerador = io.open(os.path.join(RAIZ, "tools", "geradocvazio.py"), encoding="utf-8").read()
m = re.search(r'\("pdfa",.*?"sim/nao",\s*(True|False)', gerador, re.S)
if not m:
    problemas.append("gerador: nao achei o campo pdfa em tools/geradocvazio.py")
elif m.group(1) != "True":
    problemas.append("gerador: o campo pdfa vem desligado por padrao")

relatar(problemas)
