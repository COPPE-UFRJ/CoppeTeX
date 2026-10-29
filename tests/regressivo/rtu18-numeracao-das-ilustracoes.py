# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: (desconformidade, 2.10 e 2.11) figuras, tabelas, quadros, programas, algoritmos e os flutuantes de \\newufrjfloat eram numerados dentro do capitulo ("Figura 4.1"); o Manual pede o "numero de ordem de ocorrencia no texto", e os exemplos dele e da NBR 14724 (5.8) sao todos "Figura 1", "Quadro 1", "Tabela 1".

A numeracao corre no trabalho todo por padrao; a opcao numeracaoporcapitulo
devolve a do capitulo. Cobra as duas, com uma ilustracao de cada especie em
cada um de dois capitulos: na lista, a do segundo capitulo e a numero 2 no
padrao e a 2.1 com a opcao. As equacoes seguem a mesma opcao: a do segundo
capitulo sai (2) no padrao e (2.1) com ela.
"""
from medidas import Documento, relatar, normaliza

PACOTES = r"\newufrjfloat{mapa}{Mapa}{Lista de Mapas}"
PRE = r"""
\listoffigures
\listofframes
\listofmapas
\listofprograms
\listofalgorithms
\listoftables
\tableofcontents
"""
UM = r"""
\begin{figure}[h]\centering\caption{Figura do cap %(c)s}\rule{2cm}{1cm}\source{Elaboracao propria.}\end{figure}
\begin{quadro}[h]\centering\caption{Quadro do cap %(c)s}\fbox{Q}\source{Elaboracao propria.}\end{quadro}
\begin{mapa}[h]\centering\caption{Mapa do cap %(c)s}\fbox{M}\source{Elaboracao propria.}\end{mapa}
\begin{lstlisting}[caption={Programa do cap %(c)s}]
x = 1
\end{lstlisting}
\source{Elaboracao propria.}
\begin{algorithm}[H]\caption{Algoritmo do cap %(c)s}$x \leftarrow 1$\;\end{algorithm}
\source{Elaboracao propria.}
\begin{table}[h]\centering\caption{Tabela do cap %(c)s}\begin{tabular}{c}\hline a\\\hline\end{tabular}\source{Elaboracao propria.}\end{table}
\begin{equation}x_{%(c)s} = 1\label{eq:%(c)s}\end{equation}
Equacao do cap %(c)s: (\ref{eq:%(c)s}) fim.
"""
CORPO = (r"\chapter{Um}" + UM % {"c": "um"} + "\n\\clearpage\n"
         + r"\chapter{Dois}" + UM % {"c": "dois"})

LISTAS = [("LISTA DE FIGURAS", "Figura"), ("LISTA DE QUADROS", "Quadro"),
          ("LISTA DE MAPAS", "Mapa"), ("LISTA DE PROGRAMAS", "Programa"),
          ("LISTA DE ALGORITMOS", "Algoritmo"), ("LISTA DE TABELAS", "Tabela")]

problemas = []
for opcoes, primeiro, segundo in (("dsc", "1", "2"),
                                  ("dsc,numeracaoporcapitulo", "1.1", "2.1")):
    with Documento(opcoes=opcoes, pacotes=PACOTES, pre=PRE, corpo=CORPO,
                   passadas=3) as d:
        if not d.ok:
            problemas.append("%s: nao compilou: %s" % (opcoes, d.erros_do_log()))
            continue
        corpo = normaliza(" ".join(d.texto(i) for i in range(1, d.n_paginas() + 1)))
        for numero, cap in ((primeiro, "um"), (segundo, "dois")):
            esperado = "Equacao do cap %s: (%s) fim" % (cap, numero)
            if normaliza(esperado) not in corpo:
                problemas.append("%s: esperava %r no texto" % (opcoes, esperado))
        for titulo, nome in LISTAS:
            pg = None
            for i in range(1, d.n_paginas() + 1):
                primeiras = [f.texto.strip() for f in d.fragmentos(i)[:3]]
                if any(normaliza(p) == normaliza(titulo) for p in primeiras):
                    pg = i
                    break
            if pg is None:
                problemas.append("%s: nao achei a folha da %s" % (opcoes, titulo.lower()))
                continue
            texto = normaliza(d.texto(pg))
            for numero, cap in ((primeiro, "um"), (segundo, "dois")):
                esperado = "%s %s - %s do cap %s" % (nome, numero, nome, cap)
                if normaliza(esperado) not in texto:
                    linha = [l for l in d.texto(pg).splitlines() if "do cap " + cap in l]
                    problemas.append("%s, %s: esperava %r; saiu %r"
                                     % (opcoes, titulo.lower(), esperado,
                                        linha[0].strip() if linha else ""))

relatar(problemas)
