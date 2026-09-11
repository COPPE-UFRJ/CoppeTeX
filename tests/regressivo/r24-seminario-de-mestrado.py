# -*- coding: utf-8 -*-
"""Teste de regressao da CoppeTeX. NAO roda na suite normal.

BUG: nao havia como compor um Seminario de Mestrado. Ele e requisito obrigatorio
de alguns Programas -- o de Engenharia Mecanica entre eles -- e tecnicamente NAO
e um exame de qualificacao: sao momentos diferentes do curso. Quem precisava
dele compunha com `mscexam' e trocava o titulo a mao, o que sai errado em quatro
folhas de uma vez: capa, folha de rosto, folha de aprovacao e o alto dos
resumos.

A opcao `mscsem' veio por pedido de fora (PR #61). A implementacao daquele PR
mexia no coppe.cls, que e gerado e seria apagado na geracao seguinte, e esquecia
o \\@coppeexametrue -- sem ele o seminario sairia com folha adicional da Coleta
CAPES, ficha catalografica e a referencia no alto do resumo, tres coisas que so
cabem a trabalho depositado na biblioteca.

Este teste e um .py, e nao um .tex, porque cobre a opcao nos CINCO idiomas da
classe de uma vez. Em cada um ele cobra as duas metades do defeito: que a
palavra "Seminario" apareca onde o tipo do trabalho aparece, e que as tres
folhas de quem vai a deposito NAO aparecam.
"""
import io
import os
import re
import subprocess
import sys
import tempfile
import unicodedata

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(errors="replace")
    except (ValueError, OSError):
        pass

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
SRC = os.path.join(RAIZ, "src")

# idioma -> (opcao da classe, comando de titulo proprio, palavra-chave extra)
IDIOMAS = [
    ("brazilian", "", ""),
    ("english", "", ""),
    ("spanish", "spanish", r"\braziliankeyword{Terceiro}"),
    ("french", "french", r"\braziliankeyword{Terceiro}"),
    ("italian", "italian", r"\braziliankeyword{Terceiro}"),
]

MODELO = r"""\documentclass[mscsem,%(opcao)s]{coppe}
\title{Seminario de teste}
\foreigntitle{Test seminar}
%(titulo_proprio)s
\author{Nome}{Sobrenome}
\advisor{Primeiro}{Orientador}{D.Sc.}{UFRJ}
\examiner{Primeiro Examinador}{D.Sc.}{UFRJ}
\department{PEM}
\date{09}{2026}
\dataaprovacao{15 de setembro de 2026}
\keyword{Regressao}
\foreignkeyword{Regression}
%(extra)s
\begin{document}
  \maketitle
  \frontmatter
  \begin{abstract}Resumo de teste.\end{abstract}
  \begin{foreignabstract}Test abstract.\end{foreignabstract}
  %(terceiro)s
  \tableofcontents
  \mainmatter
  \chapter{Um capitulo}
  Texto.
\end{document}
"""


def normaliza(s):
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s).strip().lower()


def texto_do_pdf(pdf):
    try:
        p = subprocess.run(["pdftotext", "-enc", "UTF-8", pdf, "-"],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError:
        return None
    if p.returncode != 0:
        return None
    return p.stdout.decode("utf-8", "replace")


problemas = []
pasta = tempfile.mkdtemp(prefix="coppe-r24-")
ambiente = dict(os.environ)
ambiente["TEXINPUTS"] = pasta + os.pathsep + SRC + ";"
ambiente["BIBINPUTS"] = pasta + os.pathsep + SRC + ";"

try:
    for idioma, opcao, extra in IDIOMAS:
        stem = "sem_" + idioma
        titulo = ""
        terceiro = ""
        if opcao:
            titulo = "\\titlein{%s}{Seminario de prueba}" % opcao
            terceiro = "\\begin{brazilianabstract}Resumo.\\end{brazilianabstract}"
        fonte = MODELO % dict(opcao=idioma, titulo_proprio=titulo,
                              extra=extra, terceiro=terceiro)
        io.open(os.path.join(pasta, stem + ".tex"), "w",
                encoding="utf-8").write(fonte)

        for _ in range(2):
            p = subprocess.run(["pdflatex", "-interaction=nonstopmode",
                                stem + ".tex"], cwd=pasta, env=ambiente,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log = os.path.join(pasta, stem + ".log")
        registro = ""
        if os.path.exists(log):
            registro = io.open(log, encoding="utf-8", errors="replace").read()
        if "Output written on" not in registro:
            erros = [l for l in registro.splitlines() if l.startswith("!")][:2]
            problemas.append("%s: nao compilou -- %s"
                             % (idioma, "; ".join(erros) or "sem PDF"))
            continue

        texto = texto_do_pdf(os.path.join(pasta, stem + ".pdf"))
        if texto is None:
            print("aviso: pdftotext indisponivel, %s conferido so pelo log" % idioma)
            continue
        t = normaliza(texto)

        # 1. O tipo do trabalho e SEMINARIO, e nao exame de qualificacao. Sai em
        #    portugues em toda a identidade institucional, qualquer que seja o
        #    idioma de redacao (Norma COPPE, secao 4), e em ingles na folha do
        #    abstract.
        if "seminario" not in t:
            problemas.append("%s: a palavra Seminario nao aparece no documento" % idioma)
        if "seminar of" not in t and "abstract of seminar" not in t:
            problemas.append("%s: a folha do abstract nao diz Seminar" % idioma)
        if "exame de qualificacao" in t or "qualifying exam" in t:
            problemas.append("%s: saiu como exame de qualificacao" % idioma)

        # 2. Seminario NAO vai para a biblioteca: sem folha da Coleta CAPES, sem
        #    ficha catalografica e sem a referencia no alto dos resumos.
        if "informacoes coleta capes" in t:
            problemas.append("%s: saiu com a folha adicional da Coleta CAPES" % idioma)
        if "ficha catalografica" in t:
            problemas.append("%s: saiu com a ficha catalografica" % idioma)
        if "sobrenome, nome. seminario de teste" in t:
            problemas.append("%s: saiu com a referencia no alto do resumo" % idioma)
finally:
    import shutil
    shutil.rmtree(pasta, ignore_errors=True)

for x in problemas:
    print(x)
sys.exit(1 if problemas else 0)
