# -*- coding: utf-8 -*-
"""Teste de regressao da CoppeTeX. NAO roda na suite normal.

BUG: o passo que copia para a distribuicao levava junto o README.md da raiz e
os cinco exemplos por idioma. O README da raiz apresenta o projeto; o de cada
distribuicao e um guia de uso. A copia sobrescrevia o guia a cada execucao
(issue #75). A lista estava escrita em dois lugares -- no src/doall.bat e no
Makefile -- e os dois divergiram.

Desde a reorganizacao de outubro de 2026 sao TRES distribuicoes (dist-coppe,
dist-poli e dist-biblatex), e a lista de cada uma vive em UM lugar so:
tools/distribuicoes.py. Este teste nao compila nada: ele le essa lista e
cobra que

  1. o README de cada dist venha de src/distribuicao/<dist>, e nao da raiz;
  2. nao va exemplo de idioma que o art. 57 da Res. CEPG 302/2024 nao admite;
  3. va tudo o que cada distribuicao precisa, inclusive toda base .bib que um
     exemplo dela declara em \\addbibresource;
  4. ninguem mais tenha lista propria (o painel ja teve);
  5. nenhuma dist-* tenha arquivo fora da lista, que iria para o zip.
"""
import io
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "tools"))

import distribuicoes as D  # noqa: E402

problemas = []


def ler(*partes):
    caminho = os.path.join(RAIZ, *partes)
    if not os.path.exists(caminho):
        problemas.append("%s nao existe" % "/".join(partes))
        return ""
    return io.open(caminho, encoding="utf-8", errors="replace").read()


PRECISA = {
    "dist-coppe": ["README.md", "COPYING.txt", "ufrj.cls", "ufrj-coppe.sty",
                   "migracao/coppe.cls", "latexmkrc", "ufrj.ist", "exemplo.bib",
                   "coppe-min-exemplo.tex", "coppe-max-exemplo.tex",
                   "coppetex/logos/ufrj-logo.pdf", "coppetex/logos/coppe-logo.pdf",
                   "manuais/ufrj.pdf", "manuais/ufrj-coppe.pdf", "manuais/manual.pdf",
                   "manuais/ufrj-quickref.pdf", "manuais/coppe-quickref.pdf",
                   "manuais/coppe-min-exemplo.pdf", "manuais/coppe-max-exemplo.pdf",
                   "exemplos/example_en.tex", "exemplos/example_es.tex",
                   "coppetex/spanish-ufrj.lbx", "coppetex/ufrj-lang-spanish.def",
                   "norma/NORMA_COPPE_2026.pdf"],
    "dist-poli": ["README.md", "COPYING.txt", "ufrj.cls", "ufrj-poli.sty",
                  "migracao/poli.cls", "latexmkrc", "ufrj.ist", "exemplo.bib",
                  "poli-min-exemplo.tex", "poli-max-exemplo.tex",
                  "coppetex/logos/ufrj-logo.pdf", "coppetex/logos/poli-logo.pdf",
                  "manuais/ufrj.pdf", "manuais/ufrj-poli.pdf",
                  "manuais/poli-quickref.pdf",
                  "norma/NORMA_POLI_2026.pdf"],
    "dist-biblatex": ["README.md", "COPYING.txt", "exemplo-biblatex.tex",
                      "exemplo.bib"],
}
# O biblatex inteiro vai em todas: em coppetex/ nas da COPPE e da Poli, e na
# raiz na do biblatex, que e feita para copiar para o projeto de outra pessoa.
for d in PRECISA:
    PRECISA[d] += [("coppetex/" + n) if d != "dist-biblatex" else n
                   for n in D.BIBLATEX]

for d, entradas in sorted(D.DISTRIBUICOES.items()):
    esperado = D.esperado(d)
    # 1. README da distribuicao, e nao o da raiz.
    for sub, nome, (origem, caminho) in entradas:
        if nome == "README.md" and not (origem == "src" and
                                        caminho.startswith("distribuicao/")):
            problemas.append("%s: o README.md vem de %s/%s, e nao de "
                             "src/distribuicao" % (d, origem, caminho))
    # 2. Idiomas sem respaldo normativo nao tem exemplo.
    for proibido in ("example_fr", "example_it", "example_pdfa", "example_pt"):
        if any(proibido in rel for rel in esperado):
            problemas.append("%s leva %s -- so vai exemplo dos idiomas que o "
                             "art. 57 da Res. CEPG 302/2024 admite" % (d, proibido))
    # 3. O que tem de estar la.
    for preciso in PRECISA.get(d, []):
        if preciso not in esperado:
            problemas.append("%s nao leva %s" % (d, preciso))
    # ... e toda base que um exemplo dela declara.
    for rel in esperado:
        if not rel.endswith(".tex"):
            continue
        origem = [o for s, n, o in entradas
                  if ((s + "/" + n) if s else n) == rel][0]
        fonte = D._origem(origem)
        if not os.path.exists(fonte):
            continue          # o --conferir do gerador diz o que falta gerar
        texto = io.open(fonte, encoding="utf-8", errors="replace").read()
        pasta = rel.rsplit("/", 1)[0] if "/" in rel else ""
        for base in re.findall(r"\\addbibresource\{([^}]+)\}", texto):
            # A base pode estar na raiz da dist ou ao lado do exemplo.
            if base not in esperado and (pasta + "/" + base) not in esperado:
                problemas.append("%s nao leva %s, que o %s declara em "
                                 "\\addbibresource" % (d, base, rel))

# 4. A lista existe num lugar so.
painel = ler("tools", "painel.py")
if re.search(r"(?m)^PARA_DIST\s*=", painel):
    problemas.append("tools/painel.py voltou a ter lista propria (PARA_DIST); "
                     "a lista e a de tools/distribuicoes.py")
for antigo in (("src", "doall.bat"), ("src", "Makefile")):
    if os.path.exists(os.path.join(RAIZ, *antigo)):
        problemas.append("%s voltou; a lista tem de existir em um lugar so"
                         % "/".join(antigo))

# O rodador da primeira camada nao pode voltar a parar no banner do makeindex.
# No Windows PowerShell 5.1, o que um executavel escreve em stderr vira
# ErrorRecord; com "Stop", o banner do makeindex derrubava a suite inteira.
runtests = ler("tests", "run-tests.ps1")
if re.search(r'ErrorActionPreference\s*=\s*"Stop"', runtests):
    problemas.append('tests/run-tests.ps1 voltou a "Stop": o banner do '
                     "makeindex derruba a suite")

# 5. Nada fora da lista em nenhuma distribuicao.
for d in sorted(D.DISTRIBUICOES):
    for rel in D.sobras(d):
        problemas.append("%s/ tem %s, que nao esta na lista -- rode "
                         "python tools/distribuicoes.py --montar" % (d, rel))

for x in problemas:
    print(x)
sys.exit(1 if problemas else 0)
