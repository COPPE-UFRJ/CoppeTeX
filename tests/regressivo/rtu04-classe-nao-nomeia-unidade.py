# -*- coding: utf-8 -*-
"""Teste de regressao da CoppeTeX. NAO roda na suite normal.

BUG: nao havia defeito antigo aqui -- este teste guarda, no CODIGO, a separacao em camadas da v5.0: nada do que a classe ufrj gera pode nomear a COPPE nem nenhum dado dela.

Ate a v4.1 o nome do Instituto, os treze Programas, o logotipo, "a COPPE/UFRJ",
"em Ciencias" e a norma do colofao estavam espalhados pelo meio da classe, e os
pacotes de idioma carregavam "a la COPPE/UFRJ". A v5.0 os tirou dali e os pos no
estilo ufrj-coppe.sty. O rtu01 prova pelo PDF que a classe sozinha nao escreve
nada disso; este prova pelo codigo, e pega o que o PDF nao pega: um dado da
COPPE que voltasse para um ramo que o documento do rtu01 nao percorre.

Le os arquivos que o ufrj.ins gera -- a classe, os estilos de bibliografia, os
pacotes de idioma, o estilo do glossario --, ignora os comentarios, e procura os
nomes. A marca CoppeTeX e o endereco do repositorio (COPPE-UFRJ/CoppeTeX) sao
permitidos: sao o projeto, e nao a unidade.
"""
import io
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
SRC = os.path.join(RAIZ, "src")

GERADOS = ["ufrj.cls", "ufrj.bbx", "ufrj.cbx", "ufrj.dbx", "ufrj-numeric.bbx",
           "ufrj-numeric.cbx", "brazilian-ufrj.lbx", "english-ufrj.lbx",
           "spanish-ufrj.lbx", "french-ufrj.lbx", "italian-ufrj.lbx",
           "ufrj-lang-spanish.def", "ufrj-lang-french.def",
           "ufrj-lang-italian.def", "ufrj.ist"]

# O que e da COPPE. As siglas dos Programas vao com fronteira de palavra: PEC e
# PEM sao pedacos de palavras comuns em outros contextos, e PPE aparece em nada
# da classe.
PROIBIDOS = [
    (re.compile(r"COPPE(?!-UFRJ/CoppeTeX)"), "a sigla COPPE"),
    (re.compile(r"(?i)coppe(?!-ufrj/coppetex|tex)"), "o nome coppe"),
    (re.compile(r"Coimbra"), "o nome do Instituto"),
    (re.compile(r"coppe-logo"), "o logotipo da COPPE"),
    (re.compile(r"Ci[eê]ncias|of Science|en Ciencias|en Sciences|in Scienze"),
     "o nome que a COPPE da ao grau"),
    (re.compile(r"\b(PEB|PEC|PEE|PEM|PEMM|PEN|PENO|PENT|PEP|PEQ|PESC|PET|PPE)\b"),
     "a sigla de um Programa da COPPE"),
]

problemas = []
for nome in GERADOS:
    caminho = os.path.join(SRC, nome)
    if not os.path.exists(caminho):
        problemas.append("%s nao existe -- rode o ufrj.ins" % nome)
        continue
    comentario = "%" if not nome.endswith(".ist") else "%%"
    for n, linha in enumerate(io.open(caminho, encoding="utf-8").read().splitlines(), 1):
        codigo = linha.lstrip()
        if not codigo or codigo.startswith(comentario):
            continue
        for padrao, oque in PROIBIDOS:
            if padrao.search(codigo):
                problemas.append("%s:%d nomeia %s: %s" % (nome, n, oque, codigo[:80]))

for x in problemas:
    print(x)
sys.exit(1 if problemas else 0)
