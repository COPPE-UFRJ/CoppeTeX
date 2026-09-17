# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX. NAO roda na suite normal.

BUG: (desconformidade, 4.2.1.1e e 4.3.8.3) as entradas @mastersthesis e @phdthesis -- as que o Google Academico, o Zotero e o JabRef exportam -- saiam como "2016. Diss. de mestr. COPPE/UFRJ, Rio de Janeiro, 2016." e "Tese Universidade...", sem o grau entre parenteses e sem o travessao antes da vinculacao academica; e um tipo digitado por extenso com curso saia "( em Engenharia ...)" (#137).
ABERTO: #137

A 4.3.8.3 do Manual UFRJ/SiBI pede, no trabalho academico: tipo do trabalho,
grau e curso entre parenteses, vinculacao academica, local e data; os exemplos
da 4.2.1.1 escrevem "Dissertacao (Mestrado em ...) -- Vinculacao, Local, ano".
No driver thesis do coppe.bbx: o tipo sai pela bibstring abreviada (mathesis ->
"Diss. de mestr."); o grau so e achado para os tipos proprios da classe
(mscdiss, dscthesis...); o travessao vem com \\setunit*, que nao dispara quando o
campo course esta vazio; e o formato de course monta "(<grau> em <curso>)" mesmo
com o grau vazio.

Cobra-se, no texto das referencias:
  1. @mastersthesis: "... 2016. Dissertacao (Mestrado) - COPPE/UFRJ, Rio de Janeiro, 2016."
  2. @phdthesis: "... 2020. Tese (Doutorado) - Universidade Federal do Rio de Janeiro, Rio de Janeiro, 2020."
  3. tipo literal com curso: nao aparece "( em", e aparece "- COPPE/UFRJ, Rio de Janeiro, 1994."
  4. controle, que ja funcionava: type=mscdiss com course.
"""
from medidas import Documento, relatar, normaliza, entrada

BIB = r"""@mastersthesis{m,
  author = {Souza, Marina},
  title = {Uma dissertação de teste},
  school = {COPPE/UFRJ},
  address = {Rio de Janeiro},
  year = {2016},
}
@phdthesis{d,
  author = {Tavares, Nilo},
  title = {Uma tese de teste},
  school = {Universidade Federal do Rio de Janeiro},
  address = {Rio de Janeiro},
  year = {2020},
}
@thesis{l,
  author = {Ubaldo, Otávio},
  title = {Uma tese com tipo literal},
  type = {Tese de D.Sc.},
  course = {Engenharia Metalúrgica e de Materiais},
  institution = {COPPE/UFRJ},
  location = {Rio de Janeiro},
  year = {1994},
}
@thesis{c,
  author = {Valente, Paula},
  title = {Uma dissertação com curso},
  type = {mscdiss},
  course = {Engenharia Civil},
  institution = {COPPE/UFRJ},
  location = {Rio de Janeiro},
  year = {2019},
}
"""
ESPERADOS = [
    ("SOUZA", "SOUZA, Marina. Uma dissertação de teste. 2016. Dissertação (Mestrado) — COPPE/UFRJ, Rio de Janeiro, 2016."),
    ("TAVARES", "TAVARES, Nilo. Uma tese de teste. 2020. Tese (Doutorado) — Universidade Federal do Rio de Janeiro, Rio de Janeiro, 2020."),
    ("VALENTE", "VALENTE, Paula. Uma dissertação com curso. 2019. Dissertação (Mestrado em Engenharia Civil) — COPPE/UFRJ, Rio de Janeiro, 2019."),
]

problemas = []
with Documento(corpo=r"\chapter{Um}Texto.\nocite{*}\printbibliography", bib=BIB) as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    pg = d.pagina_com("Souza")
    texto = d.texto(pg)
    for sobrenome, esperado in ESPERADOS:
        if normaliza(esperado) not in normaliza(texto):
            problemas.append("esperava %r\n        saiu     %r" % (esperado, entrada(texto, sobrenome)))
    lit = entrada(texto, "UBALDO")
    if "( em" in lit:
        problemas.append("tipo literal com curso saiu com '( em': %r" % lit)
    if normaliza("— COPPE/UFRJ, Rio de Janeiro, 1994.") not in normaliza(lit):
        problemas.append("tipo literal: faltou o travessao antes da vinculacao academica: %r" % lit)

relatar(problemas)
