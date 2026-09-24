# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: (desconformidade, 4.3.5.5.1) o mes da publicacao saia sempre abreviado no idioma do TRABALHO: um artigo de periodico em ingles de setembro saia "set. 2021" (#146).

A 4.3.5.5.1 do Manual UFRJ/SiBI manda abreviar os meses no idioma ORIGINAL da
publicacao (Anexo A da NBR 6023), e o exemplo da 4.3.2.2 traz "Sept. 2021" num
artigo em ingles. O biblatex usa as strings de mes do idioma do documento; o
campo langid da entrada existe para isso, mas so as datas devem mudar de idioma
-- "Disponivel em" e "Acesso em" continuam no idioma do trabalho.

As tabelas foram conferidas em 18/09/2026 contra o Anexo A da NBR 6023:2025, a
edicao que o Manual adota; o alemao, que o Anexo A tambem traz, entrou entao.

Cobra-se, com langid: "Sept. 2021" em ingles, "sept. 2021" em espanhol, "févr.
2021" em frances e "März 2021" em alemao -- nenhum no idioma do trabalho -- e
que "Acesso em:" continue em portugues.
"""
from medidas import Documento, relatar, compacta, entrada

BIB = r"""@article{en,
  author = {Evans, Sam},
  title = {An article about tests},
  journaltitle = {Journal of Tests},
  location = {Oxford},
  volume = {1},
  number = {2},
  pages = {1-2},
  date = {2021-09},
  langid = {english},
  url = {http://exemplo.org},
  urldate = {2022-03-30},
}
@article{es,
  author = {Fuentes, Ana},
  title = {Un artículo de prueba},
  journaltitle = {Revista de Pruebas},
  location = {Madrid},
  volume = {1},
  number = {2},
  pages = {1-2},
  date = {2021-09},
  langid = {spanish},
}
@article{fr,
  author = {Gautier, Paul},
  title = {Un article d'essai},
  journaltitle = {Revue des Essais},
  location = {Paris},
  volume = {1},
  number = {2},
  pages = {1-2},
  date = {2021-02},
  langid = {french},
}
@article{de,
  author = {Hartmann, Karl},
  title = {Ein Testartikel},
  journaltitle = {Zeitschrift für Tests},
  location = {Berlin},
  volume = {1},
  number = {2},
  pages = {1-2},
  date = {2021-03},
  langid = {ngerman},
}
"""

CASOS = [("EVANS", "Sept. 2021", "set. 2021"),
         ("FUENTES", "sept. 2021", "set. 2021"),
         ("GAUTIER", "févr. 2021", "fev. 2021"),
         ("HARTMANN", "März 2021", "mar. 2021")]

problemas = []
with Documento(corpo=r"\chapter{Um}Texto.\nocite{*}\printbibliography", bib=BIB) as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    pg = d.pagina_com("EVANS")
    texto = d.texto(pg)
    for autor, certo, errado in CASOS:
        ref = compacta(entrada(texto, autor))
        if certo not in ref:
            problemas.append("%s: esperava %r (mes no idioma da publicacao); saiu %r"
                             % (autor, certo, ref))
        elif errado in ref:
            problemas.append("%s: o mes saiu tambem no idioma do trabalho, %r: %r"
                             % (autor, errado, ref))
    ref = compacta(entrada(texto, "EVANS"))
    if "Acesso em:" not in ref:
        problemas.append("'Acesso em:' deixou de sair em portugues: %r" % ref)

relatar(problemas)
