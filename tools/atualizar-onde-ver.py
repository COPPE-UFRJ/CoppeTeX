#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Atualiza os numeros de linha da tabela "onde ver cada coisa" do manual.

A tabela do manual aponta, para cada comando, a linha do example.tex em que ele
aparece pela primeira vez. Esses numeros se deslocam a cada edicao do exemplo, e
nada quebra quando isso acontece: a tabela simplesmente passa a mentir.

tools/conferir-manual.py acusa o desalinhamento; este script o conserta, lendo o
example.tex atual e reescrevendo a coluna de linhas no coppe.dtx.

    python3 tools/atualizar-onde-ver.py

Rode depois de mexer no exemplo, e rode o conferir-manual.py em seguida.
"""
import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DTX = os.path.join(RAIZ, "src", "coppe.dtx")
EXEMPLO = os.path.join(RAIZ, "src", "example.tex")


def main():
    exemplo = io.open(EXEMPLO, encoding="utf-8", errors="replace").read().split("\n")
    dtx = io.open(DTX, encoding="utf-8", newline="").read()

    def primeira(cmd):
        for i, l in enumerate(exemplo, 1):
            if re.search(r"\\" + cmd + r"(?![A-Za-z])", l):
                return i
        return None

    mudou = []

    def troca(m):
        cmd, antigo = m.group(2), int(m.group(3))
        novo = primeira(cmd)
        if novo is None or novo == antigo:
            return m.group(0)
        mudou.append((cmd, antigo, novo))
        return "%s|\\%s|%s%d" % (m.group(1), cmd, m.group(4), novo)

    # ... & |\comando| & 123 \\
    padrao = re.compile(r"(&\s*)\|\\([A-Za-z@]+)\|(\s*&\s*)(\d+)(?=\s*\\\\)")

    def sub(m):
        cmd, antigo = m.group(2), int(m.group(4))
        novo = primeira(cmd)
        if novo is None or novo == antigo:
            return m.group(0)
        mudou.append((cmd, antigo, novo))
        return "%s|\\%s|%s%d" % (m.group(1), cmd, m.group(3), novo)

    novo_dtx = padrao.sub(sub, dtx)

    if not mudou:
        print("ok  a tabela ja esta em dia")
        return 0

    io.open(DTX, "w", encoding="utf-8", newline="").write(novo_dtx)
    print("atualizadas %d linha(s) da tabela:" % len(mudou))
    for cmd, antigo, novo in mudou:
        print("   \\%-22s %4d -> %4d" % (cmd, antigo, novo))
    return 0


if __name__ == "__main__":
    sys.exit(main())
