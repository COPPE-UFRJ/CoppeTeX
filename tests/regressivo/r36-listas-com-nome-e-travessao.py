# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: (desconformidade, 3.1.2.2.4 e 3.1.2.2.5) as entradas das listas pre-textuais de ilustracoes e de tabelas traziam so o numero e o titulo ("4.1 Titulo ..... 27"), sem o nome especifico da ilustracao e sem o travessao (#116).

A 3.1.2.2.4 do Manual UFRJ/SiBI pede, em cada item da lista de ilustracoes, o
nome especifico, o travessao, o titulo e o numero da folha -- "Figura 4.1 -
Titulo". A 3.1.2.2.5 pede o nome especifico tambem na lista de tabelas. Vale
para toda lista de ilustracao que a classe gera: figuras, quadros, programas,
algoritmos e os flutuantes criados com \\newcoppefloat.

Cobra-se, na folha de cada lista, a entrada no formato
"<Nome> 1.1 - <titulo>" (o traco e comparado sem distinguir a largura).
"""
from medidas import Documento, relatar, normaliza

PACOTES = r"\newcoppefloat{mapa}{Mapa}{Lista de Mapas}"
PRE = r"""
\listoffigures
\listofframes
\listofmapas
\listofprograms
\listofalgorithms
\listoftables
\tableofcontents
"""
CORPO = r"""
\chapter{Um}
\begin{figure}[h]\centering\caption{Titulo da figura}\rule{2cm}{1cm}\source{Elaboracao propria.}\end{figure}
\begin{quadro}[h]\centering\caption{Titulo do quadro}\fbox{Q}\source{Elaboracao propria.}\end{quadro}
\begin{mapa}[h]\centering\caption{Titulo do mapa}\fbox{M}\source{Elaboracao propria.}\end{mapa}
\begin{lstlisting}[caption={Titulo do programa}]
x = 1
\end{lstlisting}
\source{Elaboracao propria.}
\begin{algorithm}[H]\caption{Titulo do algoritmo}$x \leftarrow 1$\;\end{algorithm}
\source{Elaboracao propria.}
\begin{table}[h]\centering\caption{Titulo da tabela}\begin{tabular}{c}\hline a\\\hline\end{tabular}\source{Elaboracao propria.}\end{table}
"""
LISTAS = [
    ("LISTA DE FIGURAS", "Figura 1.1 - Titulo da figura"),
    ("LISTA DE QUADROS", "Quadro 1.1 - Titulo do quadro"),
    ("LISTA DE MAPAS", "Mapa 1.1 - Titulo do mapa"),
    ("LISTA DE PROGRAMAS", "Programa 1.1 - Titulo do programa"),
    ("LISTA DE ALGORITMOS", "Algoritmo 1.1 - Titulo do algoritmo"),
    ("LISTA DE TABELAS", "Tabela 1.1 - Titulo da tabela"),
]

problemas = []
with Documento(pacotes=PACOTES, pre=PRE, corpo=CORPO, passadas=3) as d:
    if not d.ok:
        relatar(["nao compilou: %s" % d.erros_do_log()])
    for titulo, esperado in LISTAS:
        pg = None
        for i in range(1, d.n_paginas() + 1):
            primeiras = [f.texto.strip() for f in d.fragmentos(i)[:3]]
            if any(normaliza(p) == normaliza(titulo) for p in primeiras):
                pg = i
                break
        if pg is None:
            problemas.append("nao achei a folha da %s" % titulo.lower())
            continue
        texto = normaliza(d.texto(pg))
        if normaliza(esperado) not in texto:
            linha = [l for l in d.texto(pg).splitlines() if "Titulo" in l]
            problemas.append("%s: esperava %r; saiu %r"
                             % (titulo.lower(), esperado, linha[0].strip() if linha else ""))

relatar(problemas)
