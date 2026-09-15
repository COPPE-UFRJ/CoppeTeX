# -*- coding: utf-8 -*-
"""Teste de regressao da CoppeTeX. NAO roda na suite normal.

BUG: a conversao para UTF-8 (#88) pegou a \\CharacterTable do .dtx -- "Acute accent \\' Left paren" virou "Acute accent Ĺeft paren" -- e o docstrip a copiou para todo arquivo gerado.

A tabela era a lista de caracteres que o pacote doc conferia para saber se o
.dtx tinha chegado inteiro. Nela o \\' vinha seguido de espacos e do rotulo da
coluna seguinte, e um conversor que aceita espaco entre o acento e a letra --
como tem de aceitar, para {\\' a} -- juntou os dois. O manual parou de compilar
com "Character table corrupted". E, escrita com %%, ela era metacomentario: o
docstrip a copiava para o cabecalho da classe, dos estilos, das bases .bib e dos
exemplos.

A documentacao atual do pacote doc lista \\CharacterTable e \\CheckSum como
obsoletos ("neither should be used in new developments"), e os dois sairam do
.dtx. Este teste cobra que nao voltem -- nem ao .dtx, nem a src/, nem a dist/.

O mesmo conversor estragou a tabela literate do listings, que troca UTF-8 por
sequencias de acento DE PROPOSITO (o listings nao le UTF-8 no pdfLaTeX): virou
{ç}{ç}1, e toda listagem com acento estourava a pilha de grupos do TeX. Tambem
se cobra que ela continue com as sequencias de acento.
"""
import io
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))

problemas = []
USO = re.compile(r"\\(CharacterTable|CheckSum)\b")

for pasta in ("src", "dist"):
    for raiz, _, nomes in os.walk(os.path.join(RAIZ, pasta)):
        for nome in nomes:
            if os.path.splitext(nome)[1] not in (".dtx", ".ins", ".tex", ".cls",
                                                 ".bbx", ".cbx", ".lbx", ".dbx",
                                                 ".def", ".bib", ".ist"):
                continue
            caminho = os.path.join(raiz, nome)
            texto = io.open(caminho, encoding="utf-8", errors="replace").read()
            m = USO.search(texto)
            if m:
                problemas.append("%s: usa \\%s, que o pacote doc declara obsoleto"
                                 % (os.path.relpath(caminho, RAIZ), m.group(1)))

dtx = io.open(os.path.join(RAIZ, "src", "ufrj.dtx"), encoding="utf-8").read()
m = re.search(r"literate=%(.*?)\n\}", dtx, re.S)
if not m:
    problemas.append("ufrj.dtx: sumiu a tabela literate do listings")
elif "{{\\" not in m.group(1):
    problemas.append("ufrj.dtx: a tabela literate perdeu as sequencias de acento")

for x in problemas:
    print(x)
sys.exit(1 if problemas else 0)
