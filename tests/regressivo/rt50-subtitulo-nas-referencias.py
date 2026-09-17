# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX. NAO roda na suite normal.

BUG: (desconformidade, 4.3.3 e 4.2) com o campo subtitle, a referencia separava titulo e subtitulo por PONTO ("Titulo. subtitulo"), punha o subtitulo em NEGRITO junto com o titulo, e na entrada pelo titulo passava a primeira palavra do subtitulo para caixa alta ("GUIA. PARA desenvolver") (#131).
ABERTO: #131

A 4.3.3 do Manual UFRJ/SiBI separa titulo e subtitulo por dois pontos, e os
exemplos da 4.2 destacam so o titulo -- o subtitulo fica sem destaque. Na
entrada pelo titulo (4.3.2.14), so a primeira palavra do TITULO vai em caixa
alta. O biblatex usa \\subtitlepunct (ponto, por padrao) e aplica o formato do
titulo aos dois campos; o ufrj.bbx nao redefinia nenhum dos dois.

O campo subtitle (e o sinonimo subtitulo) esta documentado no max-exemplo, mas
nenhuma base da entrega o usava, e por isso o defeito nunca apareceu.

Cobra-se:
  1. "MOREIRA, Clara. Metodologia aplicada: um guia pratico. Niteroi: ..." (dois pontos);
  2. o negrito dessa entrada e so "Metodologia aplicada";
  3. entrada pelo titulo: "ENGENHARIA: conceitos basicos." (caixa exata);
  4. a entrada pelo titulo nao tem negrito.
"""
from medidas import Documento, relatar, normaliza, compacta

BIB = r"""@book{sub,
  author = {Moreira, Clara},
  title = {Metodologia aplicada},
  subtitle = {um guia prático},
  location = {Niterói},
  publisher = {Editora Exemplo},
  year = {2012},
}
@book{tit,
  title = {Engenharia},
  subtitle = {conceitos básicos},
  location = {Recife},
  publisher = {Editora Exemplo},
  year = {2014},
}
"""

problemas = []
with Documento(corpo=r"\chapter{Um}Texto.\nocite{*}\printbibliography", bib=BIB) as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    pg = d.pagina_com("Moreira")
    texto = d.texto(pg)
    if normaliza("MOREIRA, Clara. Metodologia aplicada: um guia prático. Niterói: Editora Exemplo, 2012.") \
            not in normaliza(texto):
        linha = [l for l in texto.splitlines() if "MOREIRA" in l]
        problemas.append("titulo e subtitulo nao separados por dois pontos: %r"
                         % (linha[0] if linha else ""))
    frags = d.fragmentos(pg)
    negrito = [f.texto.strip() for f in frags if f.negrito and f.corpo < 13]
    if any("guia" in n for n in negrito):
        problemas.append("o subtitulo saiu em negrito: %r" % negrito)
    if not any(n.startswith("Metodologia aplicada") for n in negrito):
        problemas.append("o titulo nao saiu em negrito: %r" % negrito)
    if "ENGENHARIA: conceitos básicos." not in compacta(texto):
        linha = [l for l in texto.splitlines() if "ENGENHARIA" in l.upper()]
        problemas.append("entrada pelo titulo: esperava 'ENGENHARIA: conceitos básicos.'; saiu %r"
                         % (linha[0] if linha else ""))
    if any("ENGENHARIA" in n.upper() or "conceitos" in n for n in negrito):
        problemas.append("a entrada pelo titulo tem negrito, e nao deve ter (4.2)")

relatar(problemas)
