# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

HISTORIA: o src/ufrj.ist estava no .gitignore, sozinho entre os gerados que
eram versionados em src/; numa copia limpa do repositorio ele nao existia, e a
copia para a distribuicao parava com "FALTOU ufrj.ist" (achado do Codex, PR
#171).

Desde a reorganizacao de outubro de 2026 a regra mudou de lado: src/ so tem
FONTE, e o que os .ins geram vai para build/, fora do git. O que se baixa sao
as dist-* e normas/, e essas sim sao versionadas. Este teste cobra as tres
coisas que mantem isso de pe:

  1. nenhum arquivo que um .ins gera esta versionado em src/ -- um gerado em
     src/ e uma segunda fonte, e a edicao feita nele se perde;
  2. tudo o que o gerador copia de src/ ou da raiz esta versionado -- senao,
     numa copia limpa, a montagem para no meio;
  3. todo arquivo que cada dist-* deve ter esta versionado -- quem clona o
     repositorio tem de receber a distribuicao inteira, sem compilar nada.

O teste nao roda o git em si -- ele le a lista `git ls-files'.
"""
import io
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "tools"))

from medidas import relatar  # noqa: E402
import distribuicoes as D  # noqa: E402

problemas = []

p = subprocess.run(["git", "ls-files"], cwd=RAIZ, stdout=subprocess.PIPE,
                   stderr=subprocess.PIPE)
if p.returncode != 0:
    print("aviso: git ls-files falhou, nada foi conferido")
    relatar([])
versionados = set(p.stdout.decode("utf-8", "replace").splitlines())

# 1. O que os .ins geram, lido dos proprios .ins.
gerados = set()
for ins in D.INS:
    texto = io.open(os.path.join(D.SRC, ins), encoding="utf-8").read()
    gerados.update(re.findall(r"\\file\{([^}]+)\}", texto))
gerados.add("latexmkrc")
for nome in sorted(gerados):
    if "src/" + nome in versionados:
        problemas.append("src/%s e gerado por um .ins e esta versionado em src/: "
                         "tire-o do git (git rm --cached); ele vai para build/"
                         % nome)

# 2 e 3.
for d, entradas in sorted(D.DISTRIBUICOES.items()):
    for sub, nome, (origem, caminho) in entradas:
        if origem in ("src", "raiz"):
            rel = ("src/" + caminho) if origem == "src" else caminho
            if rel not in versionados:
                problemas.append("%s vai para %s mas NAO esta versionado" % (rel, d))
    for rel in D.esperado(d):
        if "%s/%s" % (d, rel) not in versionados:
            problemas.append("%s/%s nao esta versionado: numa copia limpa a "
                             "distribuicao vem incompleta" % (d, rel))

relatar(problemas)
