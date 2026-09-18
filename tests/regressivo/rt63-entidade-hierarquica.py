# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: (desconformidade, 4.1.1.2, 4.3.2.13 e 4.4.1) a chamada de obra de entidade com orgao subordinado repetia a hierarquia inteira, e em caixa alta: "(BRASIL. Ministerio da Educacao, 1995)" (#144).

Historia. A primeira correcao (17/09/2026) partiu de uma regra que a classe
tinha: o autor digitava a entrada da entidade em caixa alta -- "BRASIL.
Ministerio da Educacao" --, a lista deixava todo nome com ponto como viera, e a
chamada convertia a caixa alta de volta, errando em sigla ("IBGE" virava
"Ibge"). Em 18/09/2026 a regra foi invertida, como pede o Manual: a caixa alta
e trabalho do estilo. O autor digita o nome como ele se escreve, a LISTA poe em
caixa alta a entrada -- o nome ate o primeiro ". ", sem o qualificador entre
parenteses, como nos exemplos da 4.3.2.13 --, e a CHAMADA usa a entrada como
foi digitada (4.1.1.2; NBR 10520:2023, 6.1.1.2 e 6.1.1.3).

Cobra-se, com o .bib digitado como se escreve:
  1. na lista, a entrada em caixa alta e o resto como foi digitado --
     "BRASIL. Ministerio da Educacao.", "RIO DE JANEIRO (Estado). Secretaria do
     Meio Ambiente.", "BIBLIOTECA NACIONAL (Brasil).", "IBGE. Coordenacao de
     Geografia.", "ASSOCIACAO BRASILEIRA DE NORMAS TECNICAS." -- e o autor
     pessoal com o sobrenome inteiro em caixa alta, "SOUZA, Maria.";
  2. nas chamadas, a entrada como foi digitada -- "(Brasil, 1995)",
     "(Universidade Federal do Rio de Janeiro, 1998)", "(Rio de Janeiro
     (Estado), 2000)", "(IBGE, 2011)" -- e nenhum resto da hierarquia.
"""
from medidas import Documento, relatar, compacta

BIB = r"""@book{gov,
  author = {{Brasil. Ministério da Educação}},
  title = {Plano de teste},
  location = {Brasília},
  publisher = {Editora Exemplo},
  year = {1995},
}
@online{ufrj,
  author = {{Universidade Federal do Rio de Janeiro. Sistema de Bibliotecas e Informação}},
  title = {Base de teste},
  location = {Rio de Janeiro},
  year = {1998},
  url = {http://exemplo.ufrj.br},
  urldate = {2022-03-30},
}
@book{estado,
  author = {{Rio de Janeiro (Estado). Secretaria do Meio Ambiente}},
  title = {Relatório de teste},
  location = {Rio de Janeiro},
  publisher = {Secretaria do Meio Ambiente},
  year = {2000},
}
@book{bn,
  author = {{Biblioteca Nacional (Brasil)}},
  title = {Catálogo de teste},
  location = {Rio de Janeiro},
  publisher = {Biblioteca Nacional},
  year = {2001},
}
@book{ibge,
  author = {{IBGE. Coordenação de Geografia}},
  title = {Atlas de teste},
  location = {Rio de Janeiro},
  publisher = {IBGE},
  year = {2011},
}
@book{abnt,
  author = {{Associação Brasileira de Normas Técnicas}},
  title = {Norma de teste},
  location = {Rio de Janeiro},
  publisher = {ABNT},
  year = {2018},
}
@book{pessoa,
  author = {Souza, Maria},
  title = {Livro de teste},
  location = {Rio de Janeiro},
  publisher = {Editora Exemplo},
  year = {2003},
}
"""

CORPO = (r"\chapter{Um}Chamadas: \citep{gov}, \citep{ufrj}, \citep{estado}, "
         r"\citep{bn}, \citep{ibge}, \citep{abnt} e \citep{pessoa}. Fim das chamadas."
         r"\printbibliography")

problemas = []
with Documento(corpo=CORPO, bib=BIB) as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    texto = compacta(d.texto())
    i = texto.find("Chamadas:")
    j = texto.find("Fim das chamadas.")
    chamadas = texto[i:j]
    lista = texto[j:]
    for esperado in ("BRASIL. Ministério da Educação.",
                     "UNIVERSIDADE FEDERAL DO RIO DE JANEIRO. Sistema de Bibliotecas e Informação.",
                     "RIO DE JANEIRO (Estado). Secretaria do Meio Ambiente.",
                     "BIBLIOTECA NACIONAL (Brasil).",
                     "IBGE. Coordenação de Geografia.",
                     "ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS.",
                     "SOUZA, Maria."):
        if esperado not in lista:
            problemas.append("na lista, esperava %r" % esperado)
    for esperado in ("(Brasil, 1995)", "(Universidade Federal do Rio de Janeiro, 1998)",
                     "(Rio de Janeiro (Estado), 2000)", "(Biblioteca Nacional (Brasil), 2001)",
                     "(IBGE, 2011)", "(Associação Brasileira de Normas Técnicas, 2018)",
                     "(Souza, 2003)"):
        if esperado not in chamadas:
            problemas.append("na chamada, esperava %r; saiu %r" % (esperado, chamadas[:400]))
    for resto in ("Ministério", "Sistema de Bibliotecas", "Secretaria", "Coordenação"):
        if resto in chamadas:
            problemas.append("a chamada traz %r, da hierarquia, que so vai na lista" % resto)

relatar(problemas)
