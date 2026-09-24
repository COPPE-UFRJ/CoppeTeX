# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: (desconformidade, 2.5 e 4.1.2) a segunda linha de uma nota de rodape voltava para a margem esquerda, em vez de alinhar sob a primeira letra do texto da nota; o numero saia recuado; e uma nota longa podia continuar na folha seguinte (#117).

A 2.5 e a 4.1.2 do Manual UFRJ/SiBI pedem a nota alinhada, a partir da segunda
linha, abaixo da primeira letra da primeira palavra, destacando o numero
expoente -- e a 4.2 repete a regra para referencia em nota. A 4.1.2 pede ainda
que a nota fique na folha da chamada, evitando continuar na seguinte. A classe
herdava o \\@makefntext do book: numero numa caixa de 1,8 em, a partir de um
recuo, e as linhas seguintes na margem.

Cobra-se:
  1. o numero da nota comeca na margem esquerda (3 cm);
  2. a segunda e a terceira linhas comecam onde comeca o texto da primeira;
  3. uma nota longa chamada no pe da folha nao e dividida entre duas folhas.
"""
from medidas import Documento, relatar, MARGEM_ESQ, normaliza

NOTA = ("Esta nota de rodape e longa de proposito, com texto bastante para "
        "ocupar tres linhas inteiras na area das notas, de modo que se possa "
        "medir onde comeca cada linha dela em relacao a primeira letra da "
        "primeira palavra, que e o que a norma manda alinhar.")

problemas = []

# --- 1 e 2: alinhamento ------------------------------------------------------
with Documento(corpo=r"\chapter{Um}Texto com nota.\footnote{%s}" % NOTA) as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    pg = d.pagina_com("Esta nota de rodape e longa")
    palavras = d.palavras(pg)
    # a nota: a palavra "Esta" do pe da folha, e o numero "1" logo a esquerda
    # dela, mais alto (expoente) -- por isso nao se agrupa por linha aqui
    primeira = [w for w in palavras if w.texto == "Esta" and w.y0 > 600]
    if not primeira:
        relatar(["nao achei a primeira palavra da nota"])
    primeira = primeira[0]
    marca = [w for w in palavras if w.texto == "1" and w.x1 <= primeira.x0 + 0.5
             and abs(w.y1 - primeira.y1) < 8]
    if not marca:
        relatar(["nao achei o numero da nota antes da primeira palavra"])
    marca = marca[0]
    if abs(marca.x0 - MARGEM_ESQ) > 1.5:
        problemas.append("o numero da nota comeca em %.1f pt, e nao na margem (%.1f pt)"
                         % (marca.x0, MARGEM_ESQ))
    linhas = [ln for ln in d.linhas(pg) if ln[0].y1 > primeira.y1 + 2]
    seguintes = linhas[:2]
    if len(seguintes) < 2:
        problemas.append("a nota devia ter tres linhas; tem %d" % (1 + len(seguintes)))
    for n, ln in enumerate(seguintes, 2):
        if abs(ln[0].x0 - primeira.x0) > 1.5:
            problemas.append("linha %d da nota comeca em %.1f pt; o texto da primeira "
                             "linha comeca em %.1f pt" % (n, ln[0].x0, primeira.x0))

# --- 3: nota longa no pe da folha --------------------------------------------
LONGA = " ".join(["Frase de enchimento da nota longa numero %d." % i for i in range(1, 40)])
CORPO = (r"\chapter{Dois}" + "\n" + r"\vspace*{15.5cm}" + "\n"
         r"Paragrafo com a chamada MARCADORDANOTA\footnote{" + LONGA +
         " FIMDANOTALONGA}." + "\n\nOutro paragrafo depois.")
with Documento(corpo=CORPO) as d:
    if not d.ok:
        relatar(problemas + ["nota longa: nao compilou: %s" % d.erros_do_log()])
    chamada = d.pagina_com("MARCADORDANOTA")
    fim = d.pagina_com("FIMDANOTALONGA")
    inicio = d.pagina_com("Frase de enchimento da nota longa numero 1.")
    if chamada is None or fim is None or inicio is None:
        problemas.append("nota longa: nao achei a chamada ou a nota no PDF")
    elif not (chamada == inicio == fim):
        problemas.append("nota longa dividida: chamada na folha %s, nota da folha %s "
                         "a folha %s" % (chamada, inicio, fim))

relatar(problemas)
