# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: (desconformidade, 4.1.1.1.2 e 4.1.1.2a; NBR 10520:2023, 6.1.1.4) a citacao de obra que entra pelo titulo saia com o titulo INTEIRO em ITALICO e sem virgula antes do ano: "(Guia 2012, p. 7)", "(O perfil do engenheiro 1990)" (#138).

O sistema autor-data do Manual UFRJ/SiBI (4.1.1.1.2) indica o titulo de entrada
seguido do ano, SEPARADOS POR VIRGULA, e a 4.1.1.2(a) grafa a chamada so com a
inicial maiuscula, sem destaque: "(Ingles, 2012, p. 7)" para "INGLES: guia de
conversacao". O Manual adota a NBR 10520:2023, que diz como o titulo se corta
(6.1.1.4): pela unica palavra, num titulo de uma palavra; pela primeira palavra
e [...], num titulo mais longo -- "(Anteprojeto [...], 1987, p. 55)" --; e,
se o titulo comeca por artigo ou monossilabo, por ele, pela palavra seguinte e
por [...] -- "(A flor [...], 1995, p. 4)", "(Nos canaviais [...], 1995, p. 12)".
A primeira correcao (17/09/2026) deixou o titulo inteiro, porque a NBR nao
estava em specs/; o corte entrou em 18/09/2026.

Cobra-se:
  1. titulo de uma palavra, com subtitulo no campo subtitle ou digitado depois
     de ": " no title: "(Guia, 2012, p. 7)" e "(Ingles, 2012, p. 7)";
  2. titulo mais longo: "(Anteprojeto [...], 1987, p. 55)";
  3. artigo e monossilabo: "(A flor [...], 1995, p. 4)", "(O perfil [...],
     1990)" e "(Nos canaviais [...], 1995, p. 12)", sem a virgula da palavra
     cortada;
  4. artigo e so mais uma palavra: "(O Guarani, 1857)", sem [...];
  5. o shorttitle vence: "(Plano diretor, 1995)";
  6. nenhuma chamada tem italico;
  7. na lista, a entrada pelo titulo com a palavra significativa em caixa alta,
     e o artigo ou o monossilabo junto: "A FLOR prometida", "NOS CANAVIAIS,",
     "ANTEPROJETO de lei".
"""
from medidas import Documento, relatar, compacta

BIB = r"""@book{guia,
  title = {Guia},
  subtitle = {de conversação},
  location = {São Paulo},
  publisher = {Editora Exemplo},
  year = {2012},
}
@book{ingles,
  title = {Inglês: guia de conversação},
  location = {São Paulo},
  publisher = {Lonely Planet},
  year = {2012},
}
@book{perfil,
  title = {O perfil do engenheiro},
  location = {Brasília},
  publisher = {Editora Exemplo},
  year = {1990},
}
@article{anteprojeto,
  title = {Anteprojeto de lei},
  journaltitle = {Estudos e Debates},
  location = {Brasília},
  number = {13},
  pages = {51-60},
  date = {1987-01},
}
@article{flor,
  title = {A flor prometida},
  journaltitle = {Folha de S. Paulo},
  location = {São Paulo},
  pages = {4},
  date = {1995-04-02},
}
@article{canaviais,
  title = {Nos canaviais, mutilações em vez de lazer e escola},
  journaltitle = {O Globo},
  location = {Rio de Janeiro},
  pages = {12},
  date = {1995-07-16},
}
@book{guarani,
  title = {O Guarani},
  location = {Rio de Janeiro},
  publisher = {Editora Exemplo},
  year = {1857},
}
@book{plano,
  title = {Plano diretor da reforma do aparelho do Estado},
  shorttitle = {Plano diretor},
  location = {Brasília},
  publisher = {Editora Exemplo},
  year = {1995},
}
"""

CORPO = (r"\chapter{Um}Chamadas: \citep[p.~7]{guia}; \citep[p.~7]{ingles}; "
         r"\citep[p.~55]{anteprojeto}; \citep[p.~4]{flor}; \citep{perfil}; "
         r"\citep[p.~12]{canaviais}; \citep{guarani}; \citep{plano}. Fim das chamadas."
         r"\printbibliography")

problemas = []
with Documento(corpo=CORPO, bib=BIB) as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    pg = d.pagina_com("Chamadas:")
    texto = compacta(d.texto())
    i = texto.find("Chamadas:")
    j = texto.find("Fim das chamadas.")
    chamadas = texto[i:j]
    lista = texto[j:]
    for esperado in ("(Guia, 2012, p. 7)", "(Inglês, 2012, p. 7)",
                     "(Anteprojeto [...], 1987, p. 55)", "(A flor [...], 1995, p. 4)",
                     "(O perfil [...], 1990)", "(Nos canaviais [...], 1995, p. 12)",
                     "(O Guarani, 1857)", "(Plano diretor, 1995)"):
        if esperado not in chamadas:
            problemas.append("na chamada, esperava %r; saiu %r" % (esperado, chamadas[:500]))
    italicos = [f.texto for f in d.fragmentos(pg) if f.italico and
                any(p in f.texto for p in ("Guia", "Inglês", "Anteprojeto", "flor", "perfil",
                                           "canaviais", "Guarani", "Plano"))]
    if italicos:
        problemas.append("chamada pelo titulo em italico: %r" % italicos)
    for esperado in ("A FLOR prometida", "NOS CANAVIAIS, mutilações", "ANTEPROJETO de lei",
                     "O PERFIL do engenheiro", "INGLÊS: guia de conversação"):
        if esperado not in lista:
            problemas.append("na lista, esperava %r" % esperado)

relatar(problemas)
