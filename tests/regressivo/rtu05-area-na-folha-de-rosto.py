# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: (desconformidade, modelo do SiBI) a classe escrevia "Area de concentracao: ..." no bloco da natureza da folha de rosto e da folha de aprovacao; o modelo oficial poe a area na folha adicional, entre os campos da Coleta CAPES (#155).

O modelo que a 3.1.2.1.2 do Manual manda baixar -- as duas folhas de
specs/Folha adicional T&D Coleta+ CAPES.pdf -- traz na folha de rosto o autor,
o titulo, a natureza, a linha de pesquisa, a orientacao, a cidade e o ano, e
NAO traz a area de concentracao; ela aparece na segunda folha, como o campo
"Area de concentracao da producao intelectual:". O Anexo B (folha de rosto) e
o Anexo D (folha de aprovacao) confirmam: o bloco da natureza termina no grau.
So o texto corrido da 3.1.2.1.1(e) e da 3.1.2.1.3(c) lista a area entre os
elementos das duas folhas, e o modelo tem prioridade sobre ele.

Cobra as duas metades:

1. por padrao, nenhuma folha de identidade traz a frase "Area de concentracao",
   e a folha adicional traz o valor dado em \\concentrationarea;
2. com a opcao areanafolhaderosto, a frase volta as duas folhas de identidade.
"""
from medidas import Documento, PREAMBULO_PADRAO, normaliza, relatar

AREA = "Engenharia de Sistemas e Computacao"
PRE = PREAMBULO_PADRAO + "\\concentrationarea{%s}\n" % AREA
CORPO = r"\chapter{Um}Texto."

problemas = []

# 1. o padrao: a area so na folha adicional
with Documento(preambulo=PRE, corpo=CORPO) as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    folhas = [n for n in range(1, d.n_paginas() + 1)
              if "area de concentracao" in normaliza(d.texto(n))]
    adicional = d.pagina_com("Informações Coleta CAPES") or d.pagina_com("Coleta CAPES")
    if adicional is None:
        problemas.append("nao achei a folha adicional da Coleta CAPES")
    else:
        if adicional not in folhas:
            problemas.append("a folha adicional (folha %d) nao traz o campo da area "
                             "de concentracao" % adicional)
        if normaliza(AREA) not in normaliza(d.texto(adicional)):
            problemas.append("a folha adicional (folha %d) nao traz o valor %r"
                             % (adicional, AREA))
    sobrando = [n for n in folhas if n != adicional]
    if sobrando:
        problemas.append("a area de concentracao sai em folha de identidade: folha(s) %s "
                         "(so a folha adicional pode traze-la)"
                         % ", ".join(str(n) for n in sobrando))

# 2. com a opcao, a frase volta as folhas de rosto e de aprovacao
with Documento(opcoes="dsc,areanafolhaderosto", preambulo=PRE, corpo=CORPO) as d:
    if not d.ok:
        relatar(problemas + ["com areanafolhaderosto nao compilou: %s" % d.erros_do_log()])
    rosto = d.pagina_com("Orientador: Primeiro Orientador")
    aprovacao = d.pagina_com("Aprovada em") or d.pagina_com("Aprovado em")
    for nome, pg in (("folha de rosto", rosto), ("folha de aprovacao", aprovacao)):
        if pg is None:
            problemas.append("com a opcao ligada: nao achei a %s" % nome)
            continue
        if "area de concentracao" not in normaliza(d.texto(pg)):
            problemas.append("com areanafolhaderosto, a %s (folha %d) continua sem a "
                             "frase da area de concentracao" % (nome, pg))

relatar(problemas)
