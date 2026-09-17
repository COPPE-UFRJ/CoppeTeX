# -*- coding: utf-8 -*-
"""Teste de regressao da CoppeTeX (LuaLaTeX). NAO roda na suite normal.

BUG: (LuaLaTeX) a classe carregava fontenc T1 tambem no LuaLaTeX, e todo caractere digitado fora do ASCII e das letras acentuadas do Latin-1 saia TROCADO ou SUMIA: "nº" saia "nž", "§" saia "ğ", "°" saia "ř", "«»" saia "ńż"; travessao, meia-risca, aspas curvas, reticencias e "œ" sumiam, com um "Missing character" no .log e nada no terminal (#152).
ABERTO: #152

No LuaLaTeX o texto de entrada e Unicode e vai direto para a fonte: o caractere
U+00BA ocupa a posicao 186, e na codificacao T1 a posicao 186 e o "ž". O
inputenc, que faz essa ponte no pdfLaTeX, nao existe no LuaLaTeX. As fontes
Latin Modern em OpenType (codificacao TU, a padrao do LaTeX nos motores Unicode)
tem os glifos nos lugares certos. A conferencia das referencias achou o defeito
no gemeo LuaLaTeX da suite adversativa: "Decreto nž 42.822" (#151).

Cobra-se, compilando a mesma amostra com os dois motores:
  1. no LuaLaTeX, cada caractere sai no texto do PDF como foi digitado -- ou
     como o pdfLaTeX o compoe (o pdfLaTeX grafa as reticencias com tres pontos);
  2. o .log do LuaLaTeX nao traz "Missing character".
Sem lualatex instalado, o teste e PULADO com aviso.
"""
import re
import shutil
from medidas import Documento, relatar

# Os que um trabalho da COPPE digita de fato: ordinais e paragrafo em leis e
# normas, grau, aspas e travessao no texto, sinais de conta, e letras de nomes
# estrangeiros nas referencias (Erdős, Łukasiewicz, Grœbner).
AMOSTRA = [u"º", u"ª", u"§", u"°", u"—", u"–", u"“", u"”", u"‘", u"’", u"…",
           u"«", u"»", u"€", u"±", u"×", u"µ", u"·", u"²", u"½", u"¿", u"¡",
           u"œ", u"ß", u"Ł", u"ő", u"ã", u"ç", u"É"]

CORPO = u"\\chapter{Um}\n" + u"\n\n".join(
    u"Caso %02d: [%s]." % (i, c) for i, c in enumerate(AMOSTRA))


def compostos(d):
    pg = d.pagina_com("Caso 00")
    texto = d.texto(pg)
    saida = {}
    for i in range(len(AMOSTRA)):
        m = re.search(r"Caso %02d: \[(.*?)\]" % i, texto)
        saida[i] = m.group(1) if m else None
    return saida


if not shutil.which("lualatex"):
    print("aviso: lualatex nao encontrado, teste PULADO")
    raise SystemExit(0)

problemas = []
with Documento(corpo=CORPO, passadas=1) as d:
    if not d.ok:
        relatar(["pdflatex: nao compilou: %s" % d.erros_do_log()])
    referencia = compostos(d)

with Documento(corpo=CORPO, passadas=1, motor="lualatex") as d:
    if not d.ok:
        relatar(["lualatex: nao compilou: %s" % d.erros_do_log()])
    lua = compostos(d)
    faltas = sorted(set(re.findall(r"Missing character: There is no .*?\(U\+([0-9A-F]+)\)", d.log)))

trocados = [u"%s saiu %r" % (c, lua[i]) for i, c in enumerate(AMOSTRA)
            if lua[i] not in (c, referencia[i])]
if trocados:
    problemas.append(u"LuaLaTeX: %d de %d caracteres sairam trocados ou sumiram: %s"
                     % (len(trocados), len(AMOSTRA), u"; ".join(trocados)))
if faltas:
    problemas.append(u"LuaLaTeX: Missing character no .log para U+%s" % u", U+".join(faltas))

relatar(problemas)
