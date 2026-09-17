# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX. NAO roda na suite normal.

BUG: (desconformidade, 4.1.1.2 e 4.4.1) a chamada de obra de entidade com orgao subordinado repetia a hierarquia inteira, e em caixa alta: "(BRASIL. Ministerio da Educacao, 1995)" (#144).
ABERTO: #144

A classe tem uma regra deliberada para o nome da entidade na LISTA (comentario
junto de \\coppe@ucfamily no coppe.dtx): nome com ponto sai exatamente como o
autor digitou, e o autor digita a entidade superior em caixa alta --
"BRASIL. Ministerio da Educacao" --, como pede a 4.3.2.13 do Manual UFRJ/SiBI.
A lista sai certa. A CHAMADA nao: o exemplo de entidade governamental da
4.1.1.2 cita so a entrada, com inicial maiuscula -- "(Brasil, 1995)" --, e a
4.4.1 diz que a chamada segue a entrada da referencia, mas nao a grafia dela.
Nada na documentacao ensina a usar shortauthor, e o max-exemplo nao mostra.

Cobra-se, com o .bib digitado como a classe pede:
  1. na lista, "BRASIL. Ministerio da Educacao." e
     "UNIVERSIDADE FEDERAL DO RIO DE JANEIRO. Sistema de Bibliotecas e Informacao." (ja passa);
  2. nas chamadas, "(Brasil, 1995)" e "(Universidade Federal do Rio de Janeiro, 1998)".
"""
from medidas import Documento, relatar, compacta

BIB = r"""@book{gov,
  author = {{BRASIL. Ministério da Educação}},
  title = {Plano de teste},
  location = {Brasília},
  publisher = {Editora Exemplo},
  year = {1995},
}
@online{ufrj,
  author = {{UNIVERSIDADE FEDERAL DO RIO DE JANEIRO. Sistema de Bibliotecas e Informação}},
  title = {Base de teste},
  location = {Rio de Janeiro},
  year = {1998},
  url = {http://exemplo.ufrj.br},
  urldate = {2022-03-30},
}
"""

problemas = []
with Documento(corpo=r"\chapter{Um}Chamadas: \citep{gov} e \citep{ufrj}.\printbibliography", bib=BIB) as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    texto = compacta(d.texto())
    for esperado in ("BRASIL. Ministério da Educação.",
                     "UNIVERSIDADE FEDERAL DO RIO DE JANEIRO. Sistema de Bibliotecas e Informação."):
        if esperado not in texto:
            problemas.append("na lista, esperava %r" % esperado)
    i = texto.find("Chamadas:")
    for esperado in ("(Brasil, 1995)", "(Universidade Federal do Rio de Janeiro, 1998)"):
        if esperado not in texto:
            problemas.append("na chamada, esperava %r; saiu %r" % (esperado, texto[i:i + 130]))

relatar(problemas)
