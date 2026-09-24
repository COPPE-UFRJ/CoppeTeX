# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: nao havia defeito antigo aqui -- este teste guarda a divisao dos logotipos da capa entre a classe e a unidade (#162): o da UFRJ, a esquerda, e da classe, e a unidade nao o troca nem o tira; o da direita e da unidade.

O Anexo A do Manual UFRJ/SiBI poe "Logo da UFRJ" a esquerda e "Logo do
Programa" a direita, os dois opcionais. Na 5.0 em preparacao, o
\\ufrjdeclarelogos{esquerda}{direita} deixava o estilo da unidade trocar ou
tirar tambem o da UFRJ. Decisao de 18/09/2026: a classe fixa o da UFRJ, e o
estilo declara so o dele, com \\ufrjdeclarelogo -- a COPPE, o logotipo unificado,
porque nem todo Programa tem logotipo.

Os logotipos sao vetoriais e o pdfimages nao os ve: o teste mede TINTA na
faixa de cima da capa (o rt71 faz o mesmo), separando a metade esquerda da
direita. Cobra-se:
  1. sem estilo de unidade: tinta a esquerda (UFRJ), nenhuma a direita;
  2. uma unidade que ainda use a forma antiga para pedir outro logotipo a
     esquerda: a UFRJ continua la, e o .log avisa que a forma mudou;
  3. com o estilo da COPPE: tinta dos dois lados.
"""
import io
import os
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medidas import Documento, relatar  # noqa: E402

DPI = 50
FAIXA_CM = 4.0

MODELO = r"""\documentclass[dsc]{ufrj}
%(estilo)s
\begin{document}
\title{Um trabalho qualquer}
\foreigntitle{Any work}
\author{Fulana}{de Tal}
\department{%(programa)s}
\advisor{Sicrano}{Souza}{D.Sc.}{UFRJ}
\examiner{Beltrano Silva}{D.Sc.}{UFRJ}
\date{9}{2026}
\keyword{classe}
\foreignkeyword{class}
\maketitle
\frontmatter
\begin{abstract}
Texto do resumo.
\end{abstract}
\begin{foreignabstract}
Abstract text.
\end{foreignabstract}
\tableofcontents
\mainmatter
\chapter{Um}
Texto.
\end{document}
"""
SEM_UNIDADE = r"\ufrjdeclareprogram{PPGI}{Informática}{Informatics}"
FORMA_ANTIGA = SEM_UNIDADE + "\n" + r"\ufrjdeclarelogos{logotipo-que-nao-existe}{}"
COPPE = r"\usepackage{ufrj-coppe}"


def pgm(pdf, pagina):
    pasta = tempfile.mkdtemp(prefix="ufrj-rtu06-")
    try:
        prefixo = os.path.join(pasta, "folha")
        p = subprocess.run(["pdftoppm", "-gray", "-singlefile", "-r", str(DPI),
                            "-f", str(pagina), "-l", str(pagina), pdf, prefixo],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        arq = prefixo + ".pgm"
        d = io.open(arq, "rb").read() if os.path.exists(arq) else b""
    finally:
        shutil.rmtree(pasta, ignore_errors=True)
    if not d.startswith(b"P5"):
        raise SystemExit("pdftoppm nao devolveu um PGM na folha %d: %r"
                         % (pagina, p.stderr.decode("utf-8", "replace")[:200]))
    campos, i = [], 2
    while len(campos) < 3:
        while i < len(d) and d[i:i + 1].isspace():
            i += 1
        if d[i:i + 1] == b"#":
            while i < len(d) and d[i:i + 1] != b"\n":
                i += 1
            continue
        j = i
        while j < len(d) and not d[j:j + 1].isspace():
            j += 1
        campos.append(int(d[i:j]))
        i = j
    larg, alt, _ = campos
    return larg, alt, d[i + 1:]


def tinta(pdf):
    """(esquerda, direita): pixels escuros na faixa de cima da capa."""
    larg, alt, px = pgm(pdf, 1)
    esq = dir_ = 0
    for y in range(min(int(FAIXA_CM / 2.54 * DPI), alt)):
        linha = px[y * larg:(y + 1) * larg]
        for x, b in enumerate(linha):
            if b < 200:
                if x < larg // 2:
                    esq += 1
                else:
                    dir_ += 1
    return esq, dir_


problemas = []
casos = [("sem estilo de unidade", SEM_UNIDADE, "PPGI", True, False),
         ("unidade com a forma antiga", FORMA_ANTIGA, "PPGI", True, False),
         ("estilo da COPPE", COPPE, "PESC", True, True)]
for nome, estilo, programa, quer_esq, quer_dir in casos:
    with Documento(tex=MODELO % {"estilo": estilo, "programa": programa}) as d:
        if not d.ok:
            problemas.append("%s: nao compilou: %s" % (nome, d.erros_do_log()))
            continue
        esq, dir_ = tinta(d.pdf)
        if quer_esq and esq < 50:
            problemas.append("%s: a capa sem o logotipo da UFRJ a esquerda (%d pixels)" % (nome, esq))
        if quer_dir and dir_ < 50:
            problemas.append("%s: a capa sem o logotipo da unidade a direita (%d pixels)" % (nome, dir_))
        if not quer_dir and dir_ > 0:
            problemas.append("%s: tinta a direita da capa (%d pixels), onde nao ha logotipo declarado"
                             % (nome, dir_))
        if "antiga" in nome and "mudou para" not in d.log.replace("\n", " "):
            problemas.append("%s: o .log nao avisa que \\ufrjdeclarelogos mudou" % nome)

relatar(problemas)
