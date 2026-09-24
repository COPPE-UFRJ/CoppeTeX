# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: nao e desconformidade com o Manual -- e o risco da propria bancada. Uma rodada completa do regressivo chama o motor perto de cem vezes, e em quase todas com a MESMA classe; desde a #154 o resultado de cada compilacao fica guardado em _scratch/cache-regressivo. Um cache mal feito e pior do que nenhum: ele faz o teste passar com um PDF velho, e a classe pode ter quebrado sem que ninguem veja.

Cobra-se, entao, o que o cache tem de garantir:
  1. o mesmo documento, com a mesma classe, vem do cache na segunda vez, e o
     PDF e byte a byte o mesmo;
  2. MUDOU A CLASSE, MUDOU A CHAVE: com outro hash dos arquivos gerados o
     resultado guardado NAO e usado -- e esta e a razao de ser do teste;
  3. mudou o documento, mudou a chave;
  4. o cache lembra a FALHA: documento que nao compila continua nao compilando
     quando o resultado vem de la (ha teste que cobra erro);
  5. COPPE_SEM_CACHE desliga tudo.
"""
import io
import os
import sys
import uuid

import medidas
from medidas import Documento, cache_gravar, cache_ler, chave_de_compilacao, relatar

problemas = []

# O documento leva uma marca DIFERENTE EM CADA RODADA. Sem ela o teste so
# valeria com o cache vazio: na segunda vez, os documentos que ele espera ver
# COMPILAR ja estariam guardados da vez anterior, e as cobrancas de numero 2 e
# 3 -- as que provam que o cache nao mascara uma mudanca -- reprovariam sem que
# houvesse defeito nenhum. Foi o que aconteceu na primeira versao deste teste.
MARCA = uuid.uuid4().hex
CORPO = r"\chapter{Um capitulo do teste do cache}Texto do capitulo, marca %s." % MARCA

# 1. a segunda vez vem do cache, e com o mesmo PDF
with Documento(corpo=CORPO) as primeiro:
    if primeiro.doCache:
        problemas.append("documento inedito veio do cache: a marca da rodada nao esta na chave")
    if not primeiro.ok:
        problemas.append("o documento nem compilou: %s" % primeiro.erros_do_log(1))
    bytes_um = io.open(primeiro.pdf, "rb").read() if os.path.exists(primeiro.pdf) else b""
    chave_um = primeiro._chave()

with Documento(corpo=CORPO) as segundo:
    if not segundo.doCache:
        problemas.append("a segunda compilacao do mesmo documento nao veio do cache")
    bytes_dois = io.open(segundo.pdf, "rb").read() if os.path.exists(segundo.pdf) else b""
    if bytes_um and bytes_um != bytes_dois:
        problemas.append("o PDF guardado no cache nao e o mesmo que o motor tinha feito")
    if not segundo.ok:
        problemas.append("o documento vindo do cache nao passa no ok: %s"
                         % segundo.erros_do_log(1))

# 2. mudou a classe, mudou a chave. O hash dos gerados e calculado uma vez por
# processo e fica em _HASH_CLASSE: trocar esse valor e o mesmo que mexer no
# .dtx, do ponto de vista da chave.
verdadeiro = medidas.hash_da_classe()
medidas._HASH_CLASSE = "0" * 64
with Documento(corpo=CORPO) as terceiro:
    if terceiro._chave() == chave_um:
        problemas.append("a chave do cache NAO leva os arquivos gerados da classe: "
                         "uma mudanca no .dtx passaria despercebida")
    if terceiro.doCache:
        problemas.append("com outra classe o resultado guardado foi usado assim mesmo")
medidas._HASH_CLASSE = verdadeiro

# 3. mudou o documento, mudou a chave
with Documento(corpo=CORPO + " Mais uma frase, que muda o documento.") as quarto:
    if quarto._chave() == chave_um:
        problemas.append("dois documentos diferentes tem a mesma chave de cache")
    if quarto.doCache:
        problemas.append("documento diferente veio do cache")

# 4. o cache lembra a falha. \naoexiste nao e comando: o log fica com uma linha
# "!" e o `ok' e falso -- e tem de continuar falso vindo do cache.
RUIM = r"\chapter{Capitulo com erro, marca %s}\naoexisteestecomando" % MARCA
with Documento(corpo=RUIM) as quinto:
    if quinto.ok:
        problemas.append("o documento com erro passou no ok: o teste nao prova nada")
with Documento(corpo=RUIM) as sexto:
    if not sexto.doCache:
        problemas.append("a segunda compilacao do documento com erro nao veio do cache")
    elif sexto.ok:
        problemas.append("o documento com erro passou a valer depois do cache")

# 5. COPPE_SEM_CACHE desliga
medidas.SEM_CACHE = True
try:
    with Documento(corpo=CORPO) as setimo:
        if setimo.doCache:
            problemas.append("COPPE_SEM_CACHE nao desligou o cache")
finally:
    medidas.SEM_CACHE = bool(os.environ.get("COPPE_SEM_CACHE"))

relatar(problemas)
