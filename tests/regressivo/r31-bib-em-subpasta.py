# -*- coding: utf-8 -*-
"""Teste de regressao da CoppeTeX. NAO roda na suite normal.

BUG: nao havia defeito antigo aqui -- ha uma pergunta que precisava de resposta
provada. Quem escreve uma tese nao gosta de dezenas de arquivos na raiz do
trabalho, e os `.bib' sao os unicos que dariam para mudar de lugar sem mexer na
busca do LaTeX. O gerador passou a por o `.bib' numa subpasta (`referencias/',
por padrao), e a documentacao passou a recomenda-la. Uma recomendacao dessas
tem de estar sob teste, porque ela falha do lado do aluno e na vespera.

Este teste cobra as duas metades da resposta.

1. O caminho relativo FUNCIONA, e funciona com o que o aluno tem: o `.bib' numa
   subpasta, o BIBINPUTS apontando so para a pasta do trabalho -- sem o src/
   para socorrer -- e a citacao resolvida no PDF.

2. O caminho relativo tambem PROTEGE, e e este o motivo de recomenda-lo. Um
   nome pelado passa pela busca do kpathsea: se o arquivo nao estiver na pasta
   do trabalho, o biber acha, em silencio, o arquivo de mesmo nome que vem na
   distribuicao do TeX, e a tese sai com a bibliografia de outra pessoa. Com a
   subpasta no caminho nao ha busca: ou o arquivo esta ali, ou o biber para com
   erro. O teste prova as duas coisas, uma contra a outra.

A segunda metade depende de haver um `.bib' na distribuicao para servir de
sombra. Ela usa o `xampl.bib', que vem no TeX Live e no MiKTeX; se nao estiver
instalado, essa metade e PULADA com aviso, e nunca aprovada em silencio.
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

BIB = u"""@book{livro-da-subpasta,
  author    = {Sobrenome, Autor da Base},
  title     = {O livro que mora na subpasta},
  publisher = {Editora de Teste},
  address   = {Rio de Janeiro},
  year      = {2026},
}
"""

MODELO = r"""\documentclass[dsc]{coppe}
%(recursos)s
\title{Bibliografia em subpasta}
\foreigntitle{Bibliography in a subfolder}
\author{Nome}{Sobrenome}
\advisor{Primeiro}{Orientador}{D.Sc.}{UFRJ}
\examiner{Primeiro Examinador}{D.Sc.}{UFRJ}
\department{PESC}
\date{09}{2026}
\keyword{Regressao}
\begin{document}
  \maketitle
  \frontmatter
  \begin{abstract}Resumo.\end{abstract}
  \begin{foreignabstract}Abstract.\end{foreignabstract}
  \tableofcontents
  \mainmatter
  \chapter{Um capitulo}
  Texto com citacao \cite{%(chave)s}.
  \backmatter
  \printbibliography
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


def kpsewhich(nome):
    try:
        p = subprocess.run(["kpsewhich", nome], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    except OSError:
        return None
    saida = p.stdout.decode("utf-8", "replace").strip()
    return saida or None


problemas = []
pasta = tempfile.mkdtemp(prefix="coppe-r31-")
# A classe vem do src/, que e o que esta sendo testado; o .bib NAO pode vir de
# lugar nenhum senao da subpasta, e por isso o BIBINPUTS aponta so para a pasta
# do trabalho. Sem isso o teste passaria por engano, achando o arquivo no src/.
ambiente = dict(os.environ)
ambiente["TEXINPUTS"] = pasta + os.pathsep + SRC + ";"
ambiente["BIBINPUTS"] = pasta + ";"


def compila(stem, recursos, chave, passadas=3):
    fonte = MODELO % dict(recursos=recursos, chave=chave)
    io.open(os.path.join(pasta, stem + ".tex"), "w",
            encoding="utf-8").write(fonte)
    subprocess.run(["pdflatex", "-interaction=nonstopmode", stem + ".tex"],
                   cwd=pasta, env=ambiente, stdout=subprocess.PIPE,
                   stderr=subprocess.STDOUT)
    b = subprocess.run(["biber", stem], cwd=pasta, env=ambiente,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    saida_biber = b.stdout.decode("utf-8", "replace")
    for _ in range(passadas - 1):
        subprocess.run(["pdflatex", "-interaction=nonstopmode", stem + ".tex"],
                       cwd=pasta, env=ambiente, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT)
    registro = ""
    caminho_log = os.path.join(pasta, stem + ".log")
    if os.path.exists(caminho_log):
        registro = io.open(caminho_log, encoding="utf-8",
                           errors="replace").read()
    return b.returncode, saida_biber, registro


try:
    # ---- 1. o caminho relativo funciona -----------------------------------
    sub = os.path.join(pasta, "referencias")
    os.makedirs(sub)
    io.open(os.path.join(sub, "refs.bib"), "w", encoding="utf-8").write(BIB)

    rc, saida, registro = compila(
        "sub", "\\addbibresource{referencias/refs.bib}", "livro-da-subpasta")
    if rc != 0:
        problemas.append("biber falhou com o .bib na subpasta (codigo %d)" % rc)
    if "Cannot find" in saida:
        problemas.append("biber nao achou o .bib na subpasta")
    if "Output written on" not in registro:
        problemas.append("o documento com .bib em subpasta nao compilou")
    if "There were undefined references" in registro:
        problemas.append("citacao sem resolver com o .bib na subpasta")
    texto = texto_do_pdf(os.path.join(pasta, "sub.pdf"))
    if texto is None:
        print("aviso: pdftotext indisponivel, a metade 1 ficou so no log")
    elif "o livro que mora na subpasta" not in normaliza(texto):
        problemas.append("a referencia da subpasta nao saiu na bibliografia")

    # ---- 2. o nome pelado e que e perigoso --------------------------------
    sombra = kpsewhich("xampl.bib")
    if not sombra:
        print("aviso: xampl.bib nao esta instalado, a metade 2 foi PULADA")
    else:
        # 2a. Nome pelado, arquivo ausente da pasta: o biber ACHA o da
        #     distribuicao. E este o risco de que a subpasta protege.
        rc, saida, registro = compila(
            "pelado", "\\addbibresource{xampl.bib}", "article-minimal")
        if "Cannot find" in saida:
            problemas.append(
                "o nome pelado nao alcancou o xampl.bib da distribuicao: o "
                "teste perdeu o sentido, confira a instalacao")
        # 2b. O mesmo nome com a subpasta no caminho: nao ha busca, ha erro.
        rc, saida, registro = compila(
            "comcaminho", "\\addbibresource{referencias/xampl.bib}",
            "article-minimal")
        if "Cannot find" not in saida:
            problemas.append(
                "com a subpasta no caminho o biber ainda achou um xampl.bib "
                "fora da pasta: a protecao que a documentacao promete nao "
                "existe")
finally:
    shutil.rmtree(pasta, ignore_errors=True)

for x in problemas:
    print(x)
sys.exit(1 if problemas else 0)
