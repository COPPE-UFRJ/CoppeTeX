# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX. NAO roda na suite normal.

BUG: (desconformidade, 4.2 e Anexo E) a referencia do trabalho no alto do resumo saia JUSTIFICADA, com o TITULO SEM DESTAQUE e com meia-risca antes da vinculacao academica, diferente da mesma referencia na lista de referencias (#119).
ABERTO: #119

O Anexo E do Manual UFRJ/SiBI mostra a referencia do resumo com o titulo em
negrito, alinhada a esquerda. A 4.2 manda alinhar as referencias so a margem
esquerda e usar o MESMO destaque de titulo em todas as referencias do
documento; a lista de referencias da classe poe o titulo em negrito e usa
travessao antes da vinculacao academica (driver thesis do ufrj.bbx). A
referencia do resumo e composta a parte, em \\ufrj@refresumo, e nao segue nada
disso.

Cobra-se, na folha do resumo:
  1. o titulo do trabalho sai em negrito, e o subtitulo nao;
  2. as linhas da referencia, fora a ultima, nao terminam todas na margem direita;
  3. o sinal antes da vinculacao academica e o travessao (U+2014).
"""
from medidas import Documento, relatar, MARGEM_DIR, compacta

PREAMBULO = r"""\title{Composicao tipografica de referencias bibliograficas em trabalhos academicos de engenharia}
\subtitle{um estudo de caso}
\foreigntitle{Proof document}
\author{Nome}{Sobrenome}
\advisor{Primeiro}{Orientador}{D.Sc.}{UFRJ}
\examiner{Primeiro Examinador}{D.Sc.}{UFRJ}
\department{PESC}
\date{09}{2026}
\keyword{regressao}
"""

problemas = []
with Documento(preambulo=PREAMBULO, pre=r"\begin{abstract}Texto do resumo.\end{abstract}",
               corpo=r"\chapter{Um}Texto.") as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    pg = d.pagina_com("Texto do resumo")
    frags = d.fragmentos(pg)
    negrito = " ".join(f.texto for f in frags if f.negrito)
    if "Composicao tipografica" not in negrito:
        problemas.append("o titulo do trabalho nao esta em negrito na referencia do resumo")
    if "um estudo de caso" in negrito:
        problemas.append("o subtitulo saiu em negrito; so o titulo leva destaque")

    linhas = d.linhas(pg)
    i0 = [i for i, ln in enumerate(linhas) if ln[0].texto == "SOBRENOME,"]
    # a referencia vai da linha do SOBRENOME ate a linha antes do texto do resumo
    i1 = [i for i, ln in enumerate(linhas) if [w.texto for w in ln[:3]] == ["Texto", "do", "resumo."]]
    if not i0 or not i1:
        relatar(problemas + ["nao achei a referencia no alto do resumo"])
    ref = linhas[i0[0]:i1[0]]
    if len(ref) < 3:
        problemas.append("a referencia devia ocupar ao menos 3 linhas; ocupa %d" % len(ref))
    else:
        naoultimas = ref[:-1]
        if all(abs(ln[-1].x1 - MARGEM_DIR) < 0.8 for ln in naoultimas):
            problemas.append("a referencia do resumo esta justificada: as %d linhas nao "
                             "finais terminam todas na margem direita" % len(naoultimas))
    texto = compacta(d.texto(pg))
    if "— Instituto Alberto Luiz Coimbra" not in texto:
        antes = texto.split("Instituto Alberto Luiz Coimbra")[0][-3:]
        problemas.append("antes da vinculacao academica esperava o travessao (U+2014); "
                         "saiu %r" % antes)

relatar(problemas)
