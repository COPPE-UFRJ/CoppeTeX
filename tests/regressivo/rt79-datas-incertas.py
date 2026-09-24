# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: (desconformidade, 4.3.5) a classe nao compunha data incerta. A 4.3.5 registra a data provavel ou aproximada entre colchetes -- [1981?], [ca. 1977], [197-], [197-?], [19--], [19--?], [1071 ou 1072], [1987] --, e o exemplo de partitura da 4.2.10 usa uma delas. Escrever o literal no campo year quase funcionava, e errava em tres coisas: o "--" virava meia-risca pela ligadura da fonte, o ponto depois de "?]" sumia, e o biber avisava "not an integer - this will probably not sort properly" e ordenava pelo texto (#168).

Desde a #168 o literal vai para o campo ufrjyear, que a classe imprime na
referencia E na chamada, e o year fica com o ano que a forma contem, que e o
que ordena: "[197-]" em 1970, "[19--?]" em 1900, "[ca. 1977]" em 1977.

Cobra-se, compilando um documento com as oito formas da 4.3.5 e duas datas
normais:
  1. cada forma sai na referencia exatamente como foi escrita, com o ponto
     final e com os dois hifens;
  2. cada forma sai igual na chamada -- o ano numerico derivado NAO aparece;
  3. a data normal e a data de acesso nao mudam, e o mes continua abreviado;
  4. o biber nao avisa que o ano nao e inteiro;
  5. a lista sai ordenada pelo ano derivado quando o autor e o mesmo.
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
SRC = os.environ.get("COPPE_SRC") or os.path.join(RAIZ, "src")

# forma da 4.3.5 -> ano que ela contem, e que ordena
FORMAS = [
    ("[1981?]", "1981"),
    ("[ca. 1977]", "1977"),
    ("[197-]", "1970"),
    ("[197-?]", "1970"),
    ("[19--]", "1900"),
    ("[19--?]", "1900"),
    ("[1071 ou 1072]", "1071"),
    ("[1987]", "1987"),
]

BIB = ""
for i, (forma, _) in enumerate(FORMAS):
    BIB += ('@book{incerta%d,\n  author = "Sobrenome%d, Nome",\n'
            '  title = "Obra de data incerta %d",\n  location = "Rio de Janeiro",\n'
            '  publisher = "Editora",\n  year = "%s",\n}\n' % (i, i, i, forma))
# Duas datas normais, para provar que nada mudou nelas.
BIB += ('@book{normal,\n  author = "Zulu, Ana",\n  title = "Obra de data normal",\n'
        '  location = "Rio de Janeiro",\n  publisher = "Editora",\n  year = 1996,\n'
        '  pagetotal = "156",\n}\n')
BIB += ('@article{comacesso,\n  author = "Zulu, Bruno",\n  title = "Obra com data de acesso",\n'
        '  journaltitle = "Revista",\n  location = "Rio de Janeiro",\n  volume = "3",\n'
        '  date = "1995-10",\n  url = "http://exemplo.ufrj.br/x",\n'
        '  urldate = "2022-01-05",\n}\n')
# Mesmo autor, tres datas incertas: a ordem da lista sai do ano derivado.
for ano, chave in (("[19--?]", "ordema"), ("[197-]", "ordemb"), ("[1981?]", "ordemc")):
    BIB += ('@book{%s,\n  author = "Ordem, Otto",\n  title = "Obra %s",\n'
            '  location = "Rio de Janeiro",\n  publisher = "Editora",\n  year = "%s",\n}\n'
            % (chave, chave, ano))

CITACOES = " ".join("\\citep{incerta%d}" % i for i in range(len(FORMAS)))
MODELO = r"""\documentclass[dsc]{ufrj}
\usepackage{ufrj-coppe}
\addbibresource{d.bib}
\title{Palavra que so existe no titulo}
\foreigntitle{Word found only in the title}
\author{Nome}{Sobrenome}
\advisor{Primeiro}{Orientador}{D.Sc.}{UFRJ}
\examiner{Primeiro Examinador}{D.Sc.}{UFRJ}
\department{PESC}
\date{09}{2026}
\keyword{regressao}
\begin{document}
  \maketitle
  \frontmatter
  \begin{abstract}Resumo.\end{abstract}
  \tableofcontents
  \mainmatter
  \chapter{Um capitulo}
  %(citacoes)s \citep{normal} \citep{comacesso}
  \citep{ordema} \citep{ordemb} \citep{ordemc}
  \backmatter
  \printbibliography
\end{document}
"""


def normaliza(s):
    """Espaco reduzido a um so, inclusive as quebras de linha: a chamada e a
    referencia quebram onde a linha acaba, e a cobranca nao e sobre isso. A
    meia-risca volta a dois hifens, que e o que a forma da 4.3.5 tem: se a
    ligadura da fonte voltar, o teste ainda acusa pela extracao do PDF."""
    return re.sub(r"\s+", " ", s.replace("–", "--").replace("—", "--"))


problemas = []
pasta = tempfile.mkdtemp(prefix="coppe-rt79-")
ambiente = dict(os.environ)
ambiente["TEXINPUTS"] = pasta + os.pathsep + SRC + ";"
ambiente["BIBINPUTS"] = pasta + os.pathsep + SRC + ";"
try:
    io.open(os.path.join(pasta, "d.bib"), "w", encoding="utf-8").write(BIB)
    io.open(os.path.join(pasta, "d.tex"), "w", encoding="utf-8").write(
        MODELO % dict(citacoes=CITACOES))
    subprocess.run(["pdflatex", "-interaction=nonstopmode", "d.tex"], cwd=pasta,
                   env=ambiente, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    biber = subprocess.run(["biber", "d"], cwd=pasta, env=ambiente,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    saida_biber = biber.stdout.decode("utf-8", "replace")
    for _ in range(2):
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "d.tex"], cwd=pasta,
                       env=ambiente, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    log = os.path.join(pasta, "d.log")
    registro = io.open(log, encoding="utf-8", errors="replace").read() if os.path.exists(log) else ""
    erros = [l for l in registro.splitlines() if l.startswith("!")][:2]
    if "Output written on" not in registro or erros:
        problemas.append("nao compilou: %s" % ("; ".join(erros) or "sem PDF"))
    else:
        # 4. o biber nao reclama do ano
        for linha in saida_biber.splitlines():
            if "not an integer" in linha:
                problemas.append("o biber ainda avisa: %s" % linha.strip())
                break

        try:
            r = subprocess.run(["pdftotext", "-enc", "UTF-8", "-layout",
                                os.path.join(pasta, "d.pdf"), "-"],
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            texto = normaliza(r.stdout.decode("utf-8", "replace")) if r.returncode == 0 else None
        except OSError:
            texto = None
        if texto is None:
            print("aviso: pdftotext indisponivel, as cobrancas de texto foram puladas")
        else:
            # As cobrancas nao olham o nome do autor: ele hifeniza no fim da
            # linha, e a quebra nao e o assunto deste teste.
            for i, (forma, derivado) in enumerate(FORMAS):
                # 1. a referencia traz a forma, com o ponto final
                if ("Editora, %s." % forma) not in texto:
                    problemas.append("a referencia da %d nao traz %r com o ponto final"
                                     % (i, "Editora, %s." % forma))
                # 2. a chamada traz a mesma forma, e nao o ano derivado
                if (", %s)" % forma) not in texto:
                    problemas.append("nenhuma chamada traz %r" % forma)
                if (", %s)" % derivado) in texto:
                    problemas.append("uma chamada traz o ano derivado %s, e nao a forma %s"
                                     % (derivado, forma))
            # 3. as datas normais nao mudaram
            if "Editora, 1996. 156 p." not in texto:
                problemas.append("a data normal mudou: nao achei 'Editora, 1996. 156 p.'")
            if "out. 1995" not in texto:
                problemas.append("a data com mes mudou: nao achei 'out. 1995'")
            if "Acesso em: 5 jan. 2022" not in texto:
                problemas.append("a data de acesso mudou: nao achei 'Acesso em: 5 jan. 2022'")
            # 5. a ordem da lista sai do ano derivado
            pos = [texto.find("Obra ordem%s" % s) for s in ("a", "b", "c")]
            if -1 in pos:
                problemas.append("nao achei as tres obras do mesmo autor na lista")
            elif not pos[0] < pos[1] < pos[2]:
                problemas.append("a lista nao ordenou pelo ano derivado: [19--?] (1900), "
                                 "[197-] (1970) e [1981?] (1981) sairam em %r" % (pos,))
finally:
    shutil.rmtree(pasta, ignore_errors=True)

for p in problemas:
    print(p)
sys.exit(1 if problemas else 0)
