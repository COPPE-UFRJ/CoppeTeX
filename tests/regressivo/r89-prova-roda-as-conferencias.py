# -*- coding: utf-8 -*-
"""Teste de regressao da CoppeTeX (ferramentas). NAO roda na suite normal.

BUG: a prova da versao nao rodava tools/conferir-referencias.py nem tools/conferir-norma.py; a referencia m-diss do exemplo.bib saiu errada na 4.1 (r66) com o verificador acusando a divergencia -- mas ninguem o chamava (#151).
ABERTO: #151

O PAINEL.md diz que `--tudo --regressivo --conferir --dist' tem de sair limpo
antes de marcar uma versao. O `--conferir' do painel roda
conferir-referencias-cruzadas.py, conferir-manual.py e versao.py; o escopo
`prova' do build-check.ps1 roda o conferir-manual. Os dois verificadores que
comparam o PDF com o Manual -- o que mede margens, folio, contagem e sumario, e o
que compara cada referencia com o gabarito -- ficaram de fora dos dois caminhos.

Cobra-se (sem compilar) que conferir-referencias.py e conferir-norma.py sejam
chamados pelo --conferir do painel OU pelo escopo prova do build-check.ps1.
"""
import io
import os
from medidas import relatar, RAIZ

painel = io.open(os.path.join(RAIZ, "tools", "painel.py"), encoding="utf-8").read()
build = io.open(os.path.join(RAIZ, "tools", "build-check.ps1"), encoding="utf-8").read()

problemas = []
for script in ("conferir-referencias.py", "conferir-norma.py"):
    if script not in painel and script not in build:
        problemas.append("%s nao e chamado nem pelo painel (--conferir) nem pelo build-check (prova)"
                         % script)

relatar(problemas)
