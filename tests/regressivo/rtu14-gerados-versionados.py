# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: o src/ufrj.ist estava no .gitignore, sozinho entre os gerados -- a ufrj.cls, os .bbx/.cbx/.dbx, os .lbx, os .def, a exemplo.bib e os .sty das unidades sao todos versionados, e so ele nao era. Numa copia limpa do repositorio, portanto, o arquivo nao existia: o `painel.py --dist' parava com "FALTOU ufrj.ist", o rtu04 nao rodava e as listas da classe chamavam o makeindex com um estilo inexistente. O achado e do Codex, na revisao do PR #171.

Este teste generaliza o defeito, em vez de so consertar o caso: TODO arquivo
que o painel copia de src/ para dist/ tem de estar versionado no git. Um
arquivo gerado que nao esta no repositorio e um arquivo que so existe na
maquina de quem o gerou.

O teste nao roda o git em si -- ele le a lista `git ls-files', que e o que o
repositorio de fato guarda.
"""
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "tools"))

from medidas import relatar  # noqa: E402

problemas = []

try:
    import painel
except ImportError as erro:
    print("aviso: o painel.py nao pode ser lido (%s), a lista nao foi conferida" % erro)
    relatar([])

p = subprocess.run(["git", "ls-files"], cwd=RAIZ, stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE)
if p.returncode != 0:
    print("aviso: git ls-files falhou, a lista nao foi conferida")
    relatar([])
versionados = set(p.stdout.decode("utf-8", "replace").splitlines())

# A lista do painel e (subpasta em dist, nome). O arquivo vem sempre de src/,
# em src/ ou em src/logos/. Os PDFs dos manuais sao gerados na compilacao e tem
# regra propria no .gitignore -- o que se cobra aqui e a FONTE de texto.
GERADOS_NAO_TEXTO = (".pdf", ".eps", ".png")

for subpasta, nome in painel.PARA_DIST:
    if nome.endswith(GERADOS_NAO_TEXTO):
        continue
    for candidato in ("src/" + nome, "src/logos/" + nome):
        if candidato in versionados:
            break
    else:
        if not os.path.exists(os.path.join(RAIZ, "src", nome)):
            problemas.append("%s nem existe em src/ -- a lista do painel esta errada"
                             % nome)
        else:
            problemas.append("src/%s vai para a dist/ mas NAO esta versionado: "
                             "numa copia limpa do repositorio ele nao existe" % nome)

relatar(problemas)
