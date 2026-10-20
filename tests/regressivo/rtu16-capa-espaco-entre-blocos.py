# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: nao havia defeito antigo aqui -- este teste guarda o espacamento do bloco institucional da capa. Ate outubro de 2026 as linhas saiam todas na mesma entrelinha simples, e o nome da unidade, que na COPPE ocupa duas linhas, se confundia com a universidade acima e com o Programa abaixo: quatro linhas igualmente espacadas, sem dizer quais eram um bloco so.

Os modelos da UFRJ separam os TRES blocos da capa -- a universidade, a unidade
e o Programa -- por um vao maior, e mantem juntas as linhas de dentro do nome
da unidade, que sao um nome so partido para caber na largura. Medido no modelo
da Escola de Belas Artes, na mesma escala da capa da COPPE: o vao entre blocos
e 1,4 vez o de uma linha para a seguinte dentro do mesmo bloco.

Cobra-se, na capa de um trabalho da COPPE (nome do Instituto em duas linhas):
  1. as duas linhas do nome da unidade continuam na entrelinha simples da
     classe -- o respiro e ENTRE blocos, e nao dentro de um nome;
  2. o vao da universidade para a unidade, e o da unidade para o Programa,
     e de 1,3 a 1,5 vez esse -- o respiro do modelo, nem menos nem o dobro;
  3. os dois vaos entre blocos sao iguais.

A classe compoe a capa sozinha, e nenhum estilo de unidade a redefine: o que
este teste cobra na COPPE vale para a Poli e para qualquer unidade nova.
"""
from medidas import Documento, normaliza, relatar, texto_da_linha

# A entrelinha simples do corpo de 12 pt que a 2.2(b) do Manual fixa.
ENTRELINHA = 14.5
TOL = 0.5
RAZAO_MIN, RAZAO_MAX = 1.3, 1.5

BLOCO = ["UNIVERSIDADE FEDERAL DO RIO DE JANEIRO",
         "INSTITUTO ALBERTO LUIZ COIMBRA DE",
         "PÓS-GRADUAÇÃO E PESQUISA DE ENGENHARIA",
         "PROGRAMA DE ENGENHARIA DE SISTEMAS E COMPUTAÇÃO"]

problemas = []
with Documento(corpo=r"\chapter{Um}Texto.") as d:
    if not d.ok:
        problemas.append("nao compilou: %s" % d.erros_do_log())
    else:
        linhas = d.linhas(1)
        bases = []
        for esperada in BLOCO:
            alvo = normaliza(esperada)
            for ln in linhas:
                if normaliza(texto_da_linha(ln)) == alvo:
                    bases.append(ln[0].y1)
                    break
            else:
                problemas.append("a capa nao traz a linha '%s'" % esperada)
        if len(bases) == len(BLOCO):
            # universidade -> unidade, dentro da unidade, unidade -> Programa
            entre1, dentro, entre2 = (bases[1] - bases[0],
                                      bases[2] - bases[1],
                                      bases[3] - bases[2])
            if abs(dentro - ENTRELINHA) > TOL:
                problemas.append(
                    "as duas linhas do nome da unidade estao a %.2f pt uma da "
                    "outra; sao um nome so, e ficam na entrelinha simples "
                    "(%.1f pt)" % (dentro, ENTRELINHA))
            for rotulo, vao in (("da universidade para a unidade", entre1),
                                ("da unidade para o Programa", entre2)):
                razao = vao / dentro
                if not RAZAO_MIN <= razao <= RAZAO_MAX:
                    problemas.append(
                        "o vao %s e %.2f pt, %.2f vez a entrelinha de dentro "
                        "do bloco (%.2f pt); os modelos da UFRJ pedem de %.1f "
                        "a %.1f" % (rotulo, vao, razao, dentro,
                                    RAZAO_MIN, RAZAO_MAX))
            if abs(entre1 - entre2) > TOL:
                problemas.append(
                    "os dois vaos entre blocos sao diferentes: %.2f pt acima "
                    "da unidade e %.2f pt abaixo dela" % (entre1, entre2))

relatar(problemas)
