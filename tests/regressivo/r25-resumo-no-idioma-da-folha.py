# -*- coding: utf-8 -*-
"""Teste de regressao da CoppeTeX. NAO roda na suite normal.

BUG: o texto que a CLASSE escreve na folha de resumo -- a frase de abertura, o
titulo, o mes, os rotulos "Orientador" e "Programa" -- estava preso ao portugues
na folha do ambiente `abstract' e ao ingles na do `foreignabstract', quaisquer
que fossem os idiomas do trabalho.

Numa tese em portugues os dois coincidem e nada aparecia. Numa tese em ingles, o
texto em ingles saia sob "Resumo da Tese apresentada...", com o titulo em
portugues, "Maio/2026" e "Orientador:", e o texto em portugues saia sob a
abertura inglesa -- as duas folhas com metade de cada idioma.

Em espanhol era pior. Como so havia duas formas, a folha do resumo em espanhol e
a do resumo em portugues saiam com o MESMO cabecalho em portugues, e nao havia
cabecalho em espanhol em lugar nenhum -- num idioma que o art. 57 da Resolucao
CEPG n. 302/2024 admite para redigir tese.

A regra passou a ser uma so: tudo o que a classe escreve numa folha de resumo
sai no idioma daquela folha. Este teste compila um trabalho com cada idioma
principal e confere, folha por folha, que cada peca saiu no idioma certo -- e,
tao importante quanto, que nenhuma peca do idioma ERRADO apareceu ali.
"""
import io
import os
import re
import shutil
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

MODELO = r"""\documentclass[dsc,%(idioma)s]{ufrj}
\usepackage{ufrj-coppe}
\title{Titulo em portugues}
\foreigntitle{Title in English}
%(titulo_proprio)s
\author{Nome}{Sobrenome}
\advisor{Primeiro}{Orientador}{D.Sc.}{UFRJ}
\examiner{Primeiro Examinador}{D.Sc.}{UFRJ}
\department{PESC}
\date{05}{2026}
\keyword{Uma}
\foreignkeyword{One}
\braziliankeyword{Uma}
%% A frase de abertura, o titulo e a orientacao sao opcao desde a #157 (a folha
%% do Anexo E nao os tem); ligados aqui, porque sao eles que este teste cobra.
\configuraresumos{true}{true}{true}{true}
\begin{document}
  \maketitle
  \frontmatter
  %(resumos)s
  \mainmatter
  \chapter{Um capitulo}
  Texto.
\end{document}
"""

# Como reconhecer cada idioma na folha: uma peca de abertura, o rotulo de
# orientacao e o mes. Sao tres pecas diferentes de propósito -- as tres vinham
# de lugares diferentes da classe, e o defeito podia voltar em uma so.
MARCAS = {
    "brazilian": ("resumo da tese apresentada a coppe/ufrj", "orientador:", "maio/2026"),
    "english":   ("abstract of thesis presented to coppe/ufrj", "advisor:", "may/2026"),
    "spanish":   ("resumen de la tesis presentada a la coppe/ufrj", "director:", "mayo/2026"),
}

# idioma principal -> (titulo proprio, resumos na ordem, folhas esperadas)
# O resumo em portugues vem sempre primeiro (3.1.2; #158), e a classe confere.
ABS = r"\begin{abstract}Corpo do resumo principal.\end{abstract}"
EST = r"\begin{foreignabstract}Corpo do resumo estrangeiro.\end{foreignabstract}"
BRA = r"\begin{brazilianabstract}Corpo em portugues.\end{brazilianabstract}"
CASOS = [
    ("brazilian", "", ABS + EST, ["brazilian", "english"]),
    ("english", "", EST + ABS, ["brazilian", "english"]),
    ("spanish", "\\titlein{spanish}{Titulo en espanol}", BRA + EST + ABS,
     ["brazilian", "english", "spanish"]),
]


def normaliza(s):
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s).strip().lower()


def folhas_de_resumo(pdf, quantas):
    """O texto de cada folha de resumo, na ordem. Elas vem logo depois da folha
    de aprovacao, que e a quarta (capa, rosto, adicional, aprovacao)."""
    saida = []
    for p in range(5, 5 + quantas):
        try:
            r = subprocess.run(["pdftotext", "-enc", "UTF-8", "-f", str(p),
                                "-l", str(p), pdf, "-"],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except OSError:
            return None
        if r.returncode != 0:
            return None
        saida.append(normaliza(r.stdout.decode("utf-8", "replace")))
    return saida


problemas = []
pasta = tempfile.mkdtemp(prefix="coppe-r25-")
ambiente = dict(os.environ)
ambiente["TEXINPUTS"] = pasta + os.pathsep + SRC + ";"
ambiente["BIBINPUTS"] = pasta + os.pathsep + SRC + ";"

try:
    for idioma, titulo, resumos, esperadas in CASOS:
        stem = "res_" + idioma
        fonte = MODELO % dict(idioma=idioma, titulo_proprio=titulo,
                              resumos=resumos)
        io.open(os.path.join(pasta, stem + ".tex"), "w",
                encoding="utf-8").write(fonte)
        for _ in range(2):
            subprocess.run(["pdflatex", "-interaction=nonstopmode",
                            stem + ".tex"], cwd=pasta, env=ambiente,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log = os.path.join(pasta, stem + ".log")
        registro = io.open(log, encoding="utf-8", errors="replace").read() \
            if os.path.exists(log) else ""
        # O PDF sai mesmo com erro, em nonstopmode: erro no log reprova, e nao
        # so a falta de PDF. Sem isto a ordem errada dos resumos (#158) passava.
        erros = [l for l in registro.splitlines() if l.startswith("!")][:2]
        if "Output written on" not in registro or erros:
            problemas.append("%s: nao compilou -- %s"
                             % (idioma, "; ".join(erros) or "sem PDF"))
            continue

        paginas = folhas_de_resumo(os.path.join(pasta, stem + ".pdf"),
                                   len(esperadas))
        if paginas is None:
            print("aviso: pdftotext indisponivel, %s pulado" % idioma)
            continue

        for n, (texto, devia) in enumerate(zip(paginas, esperadas), 1):
            for peca in MARCAS[devia]:
                if peca not in texto:
                    problemas.append(
                        "%s, folha de resumo %d: faltou a peca em %s -- %r"
                        % (idioma, n, devia, peca))
            # E nenhuma peca dos OUTROS idiomas pode estar nesta folha.
            for outro, pecas in MARCAS.items():
                if outro == devia:
                    continue
                for peca in pecas:
                    if peca in texto:
                        problemas.append(
                            "%s, folha de resumo %d: devia ser %s e tem peca de"
                            " %s -- %r" % (idioma, n, devia, outro, peca))
finally:
    shutil.rmtree(pasta, ignore_errors=True)

for x in problemas:
    print(x)
sys.exit(1 if problemas else 0)
