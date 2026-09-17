# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: (inconsistencia, Norma COPPE 2) a capa compunha a segunda linha da instituicao como "INSTITUTO ALBERTO LUIZ COIMBRA DE POS-GRADUACAO E PESQUISA DE ENGENHARIA", e a Norma COPPE 2026 manda "Instituto Alberto Luiz Coimbra de Pos-Graduacao e Pesquisa de Engenharia (COPPE)" (#129).

A 3.1.1 do Manual UFRJ/SiBI pede o nome da instituicao e deixa os niveis em
aberto; a secao 2 da Norma COPPE fixa as tres linhas. Classe e Norma tem de dizer
a mesma coisa -- qual das duas muda e decisao da issue. O teste le a Norma e
confere a capa contra ela, entao passa com qualquer das duas correcoes.

Cobra-se: o texto do item 2 da secao 2 de NORMA_COPPE_2026.md (sem a marcacao
markdown) aparece na capa.
"""
import io
import os
import re
from medidas import Documento, relatar, normaliza, RAIZ

norma = io.open(os.path.join(RAIZ, "NORMA_COPPE_2026.md"), encoding="utf-8").read()
m = re.search(r"## 2\..*?\n2\.\s+(.*?)\n3\.", norma, re.S)
if not m:
    relatar(["nao achei o item 2 da secao 2 da Norma COPPE"])
esperado = re.sub(r"\*\*", "", m.group(1))
esperado = re.sub(r"\s+", " ", esperado).strip()

problemas = []
with Documento(pre=r"\begin{abstract}Resumo.\end{abstract}", corpo=r"\chapter{Um}Texto.") as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    capa = normaliza(d.texto(1))
    if normaliza(esperado) not in capa:
        problemas.append("a capa nao traz %r, como manda a secao 2 da Norma COPPE; traz %r"
                         % (esperado, d.texto(1).split("\n")[1:4]))

relatar(problemas)
