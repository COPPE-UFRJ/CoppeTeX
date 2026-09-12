# -*- coding: utf-8 -*-
"""Gerador de documento vazio da CoppeTeX.

    coppetex-novo.bat                 abre a janela
    coppetex-novo.bat --gerar         gera com os padroes da COPPE, sem perguntar
    coppetex-novo.bat --ajuda         a lista de todos os campos

Escreve os dois arquivos com que um trabalho comeca -- o `.tex' e o `.bib' --
ja preenchidos com a estrutura que a norma pede e com os cinco capitulos de
sempre: Introducao, Fundamentacao Teorica, Materiais e Metodos, Resultados e
Conclusoes.

Existe porque comecar do example.tex significa APAGAR: ele e um documento de
demonstracao, cheio de figuras, tabelas, quadros e comentarios que ensinam, e
quem vai escrever a tese passa a primeira hora limpando o que nao vai usar.
Aqui e o contrario -- o documento sai com o esqueleto e com o texto de
preenchimento, e voce escreve por cima.

Como na janela, assim na linha de comando: os campos sao os mesmos, definidos
uma vez so em CAMPOS, e as duas portas leem dessa mesma lista. Nao ha um
caminho que saiba fazer o que o outro nao sabe.
"""
import io
import os
import shutil
import sys

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(errors="replace")
    except (ValueError, OSError):
        pass

# O texto de preenchimento que a propria CoppeTeX usa nos exemplos. Ele existe
# para que o documento gerado COMPILE e tenha o que mostrar em cada folha: uma
# secao vazia nao revela margem, espacamento nem entrada no sumario.
FILLER = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod "
    "tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim "
    "veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea "
    "commodo consequat. Duis aute irure dolor in reprehenderit in voluptate "
    "velit esse cillum dolore eu fugiat nulla pariatur."
)

CAPITULOS = [
    ("introducao", "Introdu\u00e7\u00e3o"),
    ("fundamentacao", "Fundamenta\u00e7\u00e3o Te\u00f3rica"),
    ("metodos", "Materiais e M\u00e9todos"),
    ("resultados", "Resultados"),
    ("conclusoes", "Conclus\u00f5es"),
]

# Um paragrafo a mais no primeiro capitulo, com uma citacao de verdade. Serve a
# duas coisas: mostra a forma dos dois comandos de citacao, e deixa a
# bibliografia com uma entrada -- sem isso o documento gerado compila com
# "Empty bibliography", que e um aviso feio para quem esta comecando.
EXEMPLO_CITACAO = (
    "Uma cita\u00e7\u00e3o indireta vai entre par\u00eanteses, assim "
    "\\citep{sobrenome2026livro}; uma cita\u00e7\u00e3o em que o autor faz parte da "
    "frase sai como em \\citet{sobrenome2026artigo}. As duas formas remetem \u00e0 "
    "mesma entrada do arquivo de refer\u00eancias."
)

PROGRAMAS = [
    ("PESC", "Engenharia de Sistemas e Computa\u00e7\u00e3o"),
    ("PEB", "Engenharia Biom\u00e9dica"),
    ("PEC", "Engenharia Civil"),
    ("PEE", "Engenharia El\u00e9trica"),
    ("PEM", "Engenharia Mec\u00e2nica"),
    ("PEMM", "Engenharia Metal\u00fargica e de Materiais"),
    ("PEN", "Engenharia Nuclear"),
    ("PENO", "Engenharia Oce\u00e2nica"),
    ("PENT", "Engenharia de Nanotecnologia"),
    ("PEP", "Engenharia de Produ\u00e7\u00e3o"),
    ("PEQ", "Engenharia Qu\u00edmica"),
    ("PET", "Engenharia de Transportes"),
    ("PPE", "Planejamento Energ\u00e9tico"),
]

TIPOS = [
    ("dsc", "Tese de Doutorado"),
    ("msc", "Disserta\u00e7\u00e3o de Mestrado"),
    ("dscexam", "Exame de Qualifica\u00e7\u00e3o de Doutorado"),
    ("mscexam", "Exame de Qualifica\u00e7\u00e3o de Mestrado"),
    ("mscsem", "Semin\u00e1rio de Mestrado"),
]

IDIOMAS = [
    ("brazilian", "Portugu\u00eas"),
    ("english", "Ingl\u00eas"),
    ("spanish", "Espanhol"),
    ("french", "Franc\u00eas (n\u00e3o admitido para tese)"),
    ("italian", "Italiano (n\u00e3o admitido para tese)"),
]

MESES = [("%02d" % i, n) for i, n in enumerate(
    ["Janeiro", "Fevereiro", "Mar\u00e7o", "Abril", "Maio", "Junho", "Julho",
     "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"], 1)]

# Cada campo: chave, aba, rotulo, tipo, padrao, opcoes, explicacao.
#
# tipo: "texto", "escolha", "sim/nao", "inteiro", "multilinha"
#
# O padrao de tudo e o padrao COMPLETO da COPPE, como no example.tex: quem
# aperta Gerar sem mexer em nada recebe um trabalho com todas as folhas que a
# norma preve. Tirar e escolha de quem gera, e nao o contrario.
CAMPOS = [
    # --- Arquivos -----------------------------------------------------------
    ("pasta", "Arquivos", "Pasta onde gerar", "texto", ".", None,
     "Vazio ou '.' e a pasta em que voce esta"),
    ("tex", "Arquivos", "Nome do arquivo .tex", "texto", "main.tex", None, ""),
    ("bib", "Arquivos", "Nome do arquivo .bib", "texto", "references.bib", None, ""),
    ("pastabib", "Arquivos", "Pasta das referências", "texto",
     "referencias", None,
     "O .bib vai para esta subpasta; vazio deixa na raiz"),
    ("conteudo", "Arquivos", "Um arquivo por capitulo, na pasta conteudo/",
     "sim/nao", False, None,
     "Cria conteudo/ com os cinco capitulos e os traz com \\input"),
    ("baixar", "Arquivos", "Baixar a classe do GitHub", "sim/nao", False, None,
     "Traz a classe, os estilos e os logotipos, ja no idioma escolhido"),
    # --- Trabalho -----------------------------------------------------------
    ("tipo", "Trabalho", "Tipo do trabalho", "escolha", "dsc", TIPOS, ""),
    ("idioma", "Trabalho", "Idioma de reda\u00e7\u00e3o", "escolha", "brazilian",
     IDIOMAS, "O art. 57 da Res. CEPG 302/2024 admite os tres primeiros"),
    ("programa", "Trabalho", "Programa", "escolha", "PESC", PROGRAMAS, ""),
    ("titulo", "Trabalho", "T\u00edtulo em portugu\u00eas", "texto",
     "T\u00edtulo do Trabalho", None, ""),
    ("subtitulo", "Trabalho", "Subt\u00edtulo (opcional)", "texto", "", None,
     "Vazio nao imprime subtitulo"),
    ("titulo_en", "Trabalho", "T\u00edtulo em ingl\u00eas", "texto",
     "Title of the Work", None, ""),
    ("titulo_idioma", "Trabalho",
     "T\u00edtulo no idioma principal, se n\u00e3o for pt nem en", "texto", "", None,
     "Só usado quando o idioma e espanhol, frances ou italiano"),
    ("autor_nome", "Trabalho", "Nome do autor", "texto", "Nome do", None, ""),
    ("autor_sobrenome", "Trabalho", "Sobrenome do autor", "texto", "Autor",
     None, ""),
    ("mes", "Trabalho", "M\u00eas do dep\u00f3sito", "escolha", "%02d" % 1, MESES, ""),
    ("ano", "Trabalho", "Ano do dep\u00f3sito", "texto", "2026", None, ""),
    # --- Banca --------------------------------------------------------------
    ("n_orientadores", "Banca", "Quantos orientadores", "inteiro", 1, (1, 3), ""),
    ("n_coorientadores", "Banca", "Quantos coorientadores", "inteiro", 0, (0, 3), ""),
    ("n_examinadores", "Banca", "Quantos examinadores", "inteiro", 3, (0, 8),
     "A folha de aprova\u00e7\u00e3o aguenta oito nomes numa folha s\u00f3"),
    ("dataaprovacao", "Banca", "Data da defesa", "texto", "", None,
     "Vazio faz a folha escrever 'a ser determinada'"),
    # --- Folha adicional ----------------------------------------------------
    ("areaconcentracao", "Folha adicional", "\u00c1rea de concentra\u00e7\u00e3o", "texto",
     "\u00c1rea de Concentra\u00e7\u00e3o", None, ""),
    ("linhapesquisa", "Folha adicional", "Linha de pesquisa", "texto",
     "Linha de Pesquisa", None, "Vazio n\u00e3o imprime a linha"),
    ("tipoproducao", "Folha adicional", "Tipo de produ\u00e7\u00e3o", "escolha",
     "bibliografica",
     [("bibliografica", "Bibliogr\u00e1fica"), ("artistica", "Art\u00edstica"),
      ("tecnologica", "Tecnol\u00f3gica"), ("tecnica", "T\u00e9cnica")], ""),
    ("projetovinculado", "Folha adicional", "Vinculado a projeto de pesquisa",
     "escolha", "nao", [("sim", "Sim"), ("nao", "N\u00e3o")], ""),
    ("nomeprojeto", "Folha adicional", "Nome do projeto", "texto", "", None,
     "S\u00f3 se houver projeto vinculado"),
    ("n_agencias", "Folha adicional", "Quantas ag\u00eancias de fomento", "inteiro",
     1, (0, 4), ""),
    ("ficha", "Folha adicional", "Arquivo da ficha catalogr\u00e1fica", "texto", "",
     None, "Vazio deixa a moldura reservada; a ficha vem do gerador do SiBI"),
    # --- Op\u00e7\u00f5es da classe -----------------------------------------------
    ("pdfa", "Op\u00e7\u00f5es", "PDF/A-2b (obrigat\u00f3rio no dep\u00f3sito)", "sim/nao",
     False, None, "Ligue ao depositar; atrapalha durante a escrita"),
    ("numbers", "Op\u00e7\u00f5es", "Cita\u00e7\u00f5es num\u00e9ricas [1]", "sim/nao", False, None,
     "Sem isto, autor-data"),
    ("comserifa", "Op\u00e7\u00f5es", "Com serifa", "sim/nao", False, None,
     "O padr\u00e3o \u00e9 sem serifa desde a 4.1"),
    ("semlinks", "Op\u00e7\u00f5es", "Links sem cor nem moldura", "sim/nao", False,
     None, "Para quem vai imprimir"),
    ("doublespacing", "Op\u00e7\u00f5es", "Espa\u00e7o duplo", "sim/nao", False, None,
     "S\u00f3 se o seu Programa pedir"),
    ("twoside", "Op\u00e7\u00f5es", "Margens espelhadas (frente e verso)", "sim/nao",
     False, None, "S\u00f3 para quem vai imprimir e encadernar"),
    ("coorientador", "Op\u00e7\u00f5es", "Coorientadores nas folhas de resumo",
     "sim/nao", False, None, ""),
    ("orientadorexamina", "Op\u00e7\u00f5es", "Orientador na folha de aprova\u00e7\u00e3o",
     "sim/nao", False, None, "Ligue se no seu Programa ele integra a banca"),
    ("rascunhoficha", "Op\u00e7\u00f5es", "Ficha de rascunho enquanto escreve",
     "sim/nao", False, None, "Nunca vale para dep\u00f3sito"),
    ("listasnosumario", "Op\u00e7\u00f5es", "Listas pr\u00e9-textuais no sum\u00e1rio", "sim/nao",
     False, None, "A 3.1.2.1.6 as mant\u00e9m fora dele"),
    ("resumosemreferencia", "Op\u00e7\u00f5es", "Resumo sem a refer\u00eancia no alto",
     "sim/nao", False, None, "S\u00f3 se o resumo n\u00e3o couber numa folha com ela"),
    # --- Estrutura ----------------------------------------------------------
    ("dedicatoria", "Estrutura", "Dedicat\u00f3ria", "sim/nao", True, None, ""),
    ("agradecimentos", "Estrutura", "Agradecimentos", "sim/nao", True, None, ""),
    ("resumo_pt", "Estrutura", "Resumo em portugu\u00eas", "sim/nao", True, None,
     "Obrigat\u00f3rio; desligue s\u00f3 se souber o que est\u00e1 fazendo"),
    ("resumo_terceiro", "Estrutura",
     "Terceiro resumo (trabalho em espanhol)", "sim/nao", False, None,
     "Obrigat\u00f3rio quando nem o principal nem o estrangeiro est\u00e3o em portugu\u00eas"),
    ("listoffigures", "Estrutura", "Lista de figuras", "sim/nao", True, None, ""),
    ("listoftables", "Estrutura", "Lista de tabelas", "sim/nao", True, None, ""),
    ("listofquadros", "Estrutura", "Lista de quadros", "sim/nao", False, None, ""),
    ("listofprogramas", "Estrutura", "Lista de programas", "sim/nao", False,
     None, ""),
    ("listofalgorithms", "Estrutura", "Lista de algoritmos", "sim/nao", False,
     None, ""),
    ("abreviaturas", "Estrutura", "Lista de abreviaturas e siglas", "sim/nao",
     True, None, ""),
    ("simbolos", "Estrutura", "Lista de s\u00edmbolos", "sim/nao", True, None, ""),
    ("n_apendices", "Estrutura", "Quantos ap\u00eandices", "inteiro", 0, (0, 6),
     "Texto seu, que complementa a argumenta\u00e7\u00e3o"),
    ("n_anexos", "Estrutura", "Quantos anexos", "inteiro", 0, (0, 6),
     "Documento de terceiro, que fundamenta ou comprova"),
    ("glossario", "Estrutura", "Gloss\u00e1rio p\u00f3s-textual", "sim/nao", False, None, ""),
    ("indice", "Estrutura", "\u00cdndice remissivo", "sim/nao", False, None, ""),
    ("colofao", "Estrutura", "Colof\u00e3o no fim", "sim/nao", True, None,
     "Diz com que vers\u00e3o da classe o documento foi composto"),
]

ABAS = ["Arquivos", "Trabalho", "Banca", "Folha adicional", "Op\u00e7\u00f5es",
        "Estrutura"]

OPCOES_CLASSE = ["pdfa", "numbers", "comserifa", "semlinks", "doublespacing",
                 "twoside", "coorientador", "orientadorexamina",
                 "rascunhoficha", "listasnosumario", "resumosemreferencia"]

LISTAS = [("listoffigures", "\\listoffigures"),
          ("listoftables", "\\listoftables"),
          ("listofquadros", "\\listofquadros"),
          ("listofprogramas", "\\listofprogramas"),
          ("listofalgorithms", "\\listofalgorithms"),
          ("abreviaturas", "\\printloabbreviations"),
          ("simbolos", "\\printlosymbols")]


def padroes():
    return dict((c[0], c[4]) for c in CAMPOS)


def campo(chave):
    for c in CAMPOS:
        if c[0] == chave:
            return c
    raise KeyError(chave)


def caminho_bib(v, nome_bib):
    """O caminho do .bib como o \\addbibresource tem de escreve-lo.

    Com a pasta preenchida sai "referencias/refs.bib", e e assim que se quer:
    o biber abre o caminho relativo e NAO procura mais nada. Um nome pelado,
    ao contrario, ele procura -- e acha, se nao existir na pasta do trabalho, o
    arquivo de mesmo nome que vier na distribuicao do TeX. Barra para frente
    tambem no Windows, que e o que o TeX entende em todo lugar.
    """
    sub = (v.get("pastabib") or "").strip().strip("/\\")
    return "%s/%s" % (sub, nome_bib) if sub else nome_bib


# ---------------------------------------------------------------------------
# O documento
# ---------------------------------------------------------------------------
def monta_tex(v, nome_bib):
    """O .tex do trabalho, conforme as escolhas."""
    L = []
    A = L.append

    opcoes = [v["tipo"]]
    if v["idioma"] != "brazilian":
        opcoes.append(v["idioma"])
    for o in OPCOES_CLASSE:
        if v.get(o):
            opcoes.append(o)

    A("%% Gerado por tools/geradocvazio.py, da CoppeTeX.")
    A("%% Troque o conteudo e apague o que nao usar.")
    A("%%")
    A("%% Para compilar:  pdflatex %s ; biber %s ; pdflatex ; pdflatex"
      % (v["tex"][:-4], v["tex"][:-4]))
    A("%% Ou, mais curto:  latexmk -pdf %s" % v["tex"][:-4])
    A("")
    A("\\documentclass[%s]{coppe}" % ",".join(opcoes))
    A("")
    A("\\addbibresource{%s}%% a sua base de referencias" % caminho_bib(v, nome_bib))
    if v["abreviaturas"]:
        A("\\makeloabbreviations")
    if v["simbolos"]:
        A("\\makelosymbols")
    if v["indice"]:
        A("\\usepackage{makeidx}\\makeindex")
    A("")
    A("\\begin{document}")
    A("")
    A("  \\title{%s}" % v["titulo"])
    if v["subtitulo"].strip():
        A("  \\subtitle{%s}" % v["subtitulo"])
    A("  \\foreigntitle{%s}" % v["titulo_en"])
    if v["idioma"] not in ("brazilian", "english") and v["titulo_idioma"].strip():
        A("  \\titlein{%s}{%s}" % (v["idioma"], v["titulo_idioma"]))
    A("  \\author{%s}{%s}" % (v["autor_nome"], v["autor_sobrenome"]))
    A("")
    A("  %% Nome, sobrenome, titulacao e instituicao. O tratamento (\"Prof.\")")
    A("  %% e o argumento OPCIONAL, entre colchetes, e vem vazio por padrao: a")
    A("  %% norma nao pede tratamento nenhum.")
    for i in range(int(v["n_orientadores"])):
        A("  \\advisor{Nome}{Sobrenome do Orientador %d}{D.Sc.}{UFRJ}" % (i + 1))
    for i in range(int(v["n_coorientadores"])):
        A("  \\coadvisor{Nome}{Sobrenome do Coorientador %d}{D.Sc.}{UFRJ}"
          % (i + 1))
    if int(v["n_examinadores"]):
        A("")
        for i in range(int(v["n_examinadores"])):
            A("  \\examiner{Nome Sobrenome do Examinador %d}{D.Sc.}{UFRJ}"
              % (i + 1))
    A("")
    A("  \\department{%s}" % v["programa"])
    A("  \\date{%s}{%s}" % (v["mes"], v["ano"]))
    if v["dataaprovacao"].strip():
        A("  \\dataaprovacao{%s}" % v["dataaprovacao"])
    else:
        A("  %% Sem \\dataaprovacao a folha escreve \"a ser determinada\".")
        A("  %% \\dataaprovacao{15 de setembro de %s}" % v["ano"])
    A("")
    A("  \\keyword{Primeira palavra-chave}")
    A("  \\keyword{Segunda palavra-chave}")
    A("  \\keyword{Terceira palavra-chave}")
    A("  \\foreignkeyword{First keyword}")
    A("  \\foreignkeyword{Second keyword}")
    A("  \\foreignkeyword{Third keyword}")
    if v["resumo_terceiro"]:
        A("  \\braziliankeyword{Primeira palavra-chave}")
        A("  \\braziliankeyword{Segunda palavra-chave}")
    A("")
    A("  %% Folha adicional da Coleta CAPES, obrigatoria desde agosto de 2026.")
    if v["areaconcentracao"].strip():
        A("  \\areaconcentracao{%s}" % v["areaconcentracao"])
    if v["linhapesquisa"].strip():
        A("  \\linhapesquisa{%s}" % v["linhapesquisa"])
    A("  \\tipoproducao{%s}" % v["tipoproducao"])
    A("  \\projetovinculado{%s}" % v["projetovinculado"])
    if v["nomeprojeto"].strip():
        A("  \\nomeprojeto{%s}" % v["nomeprojeto"])
    for i in range(int(v["n_agencias"])):
        A("  \\agenciafomento{Nome por extenso da agencia %d}{SIGLA}" % (i + 1))
    if v["ficha"].strip():
        A("  \\fichacatalografica{%s}" % v["ficha"])
    else:
        A("  %% A ficha vem de fichacatalografica.sibi.ufrj.br. Tendo o arquivo:")
        A("  %% \\fichacatalografica{ficha.pdf}")
    A("")
    A("  \\maketitle")
    A("")
    A("  \\frontmatter")
    if v["dedicatoria"]:
        A("  \\dedication{A quem voce quiser dedicar este trabalho.}")
        A("")
    if v["agradecimentos"]:
        A("  \\chapter*{Agradecimentos}")
        A("")
        A("  " + FILLER)
        A("")
    if v["resumo_pt"]:
        A("  \\begin{abstract}")
        A("")
        A("  " + FILLER)
        A("")
        A("  \\end{abstract}")
        A("")
    A("  \\begin{foreignabstract}")
    A("")
    A("  " + FILLER)
    A("")
    A("  \\end{foreignabstract}")
    A("")
    if v["resumo_terceiro"]:
        A("  \\begin{brazilianabstract}")
        A("")
        A("  " + FILLER)
        A("")
        A("  \\end{brazilianabstract}")
        A("")
    marcadas = [cmd for chave, cmd in LISTAS if v.get(chave)]
    if marcadas:
        A("  %% As listas vem ANTES do sumario (3.1.2.1.6).")
        for cmd in marcadas:
            A("  " + cmd)
    A("  \\tableofcontents")
    A("")
    A("  \\mainmatter")
    A("")
    for chave, titulo in CAPITULOS:
        if v["conteudo"]:
            A("  \\input{conteudo/%s}" % chave)
        else:
            A("  \\chapter{%s}" % titulo)
            A("")
            A("  " + FILLER)
            A("")
            if chave == "introducao":
                A("  " + EXEMPLO_CITACAO)
                A("")
    if v["glossario"] or v["indice"] or int(v["n_apendices"]) or \
            int(v["n_anexos"]):
        A("  \\backmatter")
        A("")
    A("  \\printbibliography")
    A("")
    if v["glossario"]:
        A("  \\begin{theglossary}")
        A("    \\item[Termo] a definicao do termo, em uma linha.")
        A("  \\end{theglossary}")
        A("")
    if int(v["n_apendices"]):
        A("  %% Apendice: texto SEU, que complementa a argumentacao.")
        A("  \\appendix")
        for i in range(int(v["n_apendices"])):
            A("  \\chapter{T\u00edtulo do Ap\u00eandice %d}" % (i + 1))
            A("  " + FILLER)
        A("")
    if int(v["n_anexos"]):
        A("  %% Anexo: documento de TERCEIRO, que fundamenta ou comprova.")
        A("  \\annex")
        for i in range(int(v["n_anexos"])):
            A("  \\chapter{T\u00edtulo do Anexo %d}" % (i + 1))
            A("  " + FILLER)
        A("")
    if v["indice"]:
        A("  \\printindex")
        A("")
    if v["colofao"]:
        A("  \\coppetexfinalpage")
        A("")
    A("\\end{document}")
    return "\n".join(L) + "\n"


def monta_capitulo(chave, titulo):
    corpo = FILLER
    if chave == "introducao":
        corpo += "\n\n" + EXEMPLO_CITACAO
    return ("%% Capitulo gerado por tools/geradocvazio.py.\n"
            "\\chapter{%s}\n\n%s\n" % (titulo, corpo))


def monta_bib(v):
    return """%% Base de referencias gerada por tools/geradocvazio.py.
%%
%% Uma entrada de cada tipo mais comum, para copiar e trocar. A entrega traz,
%% em tipos.bib, um exemplo de CADA categoria da secao 4.2 do Manual -- olhe la
%% quando precisar de um tipo que nao esteja aqui.
%%
%% Os nomes de campo podem ser os do biblatex (author, title, year) ou os
%% sinonimos em portugues que a classe declara (autor, titulo, ano).

@book{sobrenome2026livro,
  author    = "Sobrenome, Nome do Autor",
  title     = "T{\\'i}tulo do livro",
  subtitle  = "subt{\\'i}tulo, se houver",
  edition   = "2",
  location  = "Rio de Janeiro",
  publisher = "Nome da Editora",
  year      = "2026",
}

@article{sobrenome2026artigo,
  author  = "Sobrenome, Nome do Autor and Outro, Nome do",
  title   = "T{\\'i}tulo do artigo",
  journal = "Nome do Peri{\\'o}dico",
  volume  = "12",
  number  = "3",
  pages   = "45--67",
  year    = "2026",
}

@inproceedings{sobrenome2026evento,
  author       = "Sobrenome, Nome do Autor",
  title        = "T{\\'i}tulo do trabalho apresentado",
  eventtitle   = "Nome do Congresso",
  eventdate    = "2026",
  venue        = "Rio de Janeiro",
  booktitle    = "Anais",
  location     = "Rio de Janeiro",
  publisher    = "Nome da Entidade",
  pages        = "1--10",
  year         = "2026",
}

@thesis{sobrenome2026tese,
  author      = "Sobrenome, Nome do Autor",
  title       = "T{\\'i}tulo da tese",
  type        = "Tese (Doutorado em %s)",
  institution = "Universidade Federal do Rio de Janeiro",
  location    = "Rio de Janeiro",
  year        = "2026",
}

@online{sobrenome2026online,
  author      = "Sobrenome, Nome do Autor",
  title       = "T{\\'i}tulo da p{\\'a}gina",
  location    = "Rio de Janeiro",
  year        = "2026",
  url         = "https://exemplo.ufrj.br/pagina",
  urldate     = "2026-09-11",
}
""" % dict(PROGRAMAS)[v["programa"]]


# ---------------------------------------------------------------------------
# Trazer a classe do GitHub
# ---------------------------------------------------------------------------
REPO = "COPPE-UFRJ/CoppeTeX"

# O que e preciso para COMPILAR, e so isso. Os exemplos e os manuais ficam de
# fora de proposito: voce pediu um documento em branco, e um exemplo ao lado e
# justamente o que se queria evitar. Os manuais estao em manuais/ na entrega e
# na pagina do repositorio.
def _serve_para_compilar(relativo):
    nome = relativo.replace("\\", "/").split("/")[-1]
    if nome.startswith("example") or nome in ("tipos.bib", "coppe.bib",
                                              "README.md"):
        return False
    if nome in ("coppe.dtx", "coppe.ins", "manual.tex"):
        return False   # sao FONTES dos manuais, nao servem para compilar a tese
    return True


def baixar_entrega(pasta, idioma, aviso):
    """Traz a entrega do GitHub e a espalha na pasta, ja no idioma escolhido.

    Faz de uma vez o que o README manda fazer a mao: baixa, poe a classe e os
    estilos na raiz, a pasta logos junto, e -- se o trabalho nao for em
    portugues -- TRAZ PARA A RAIZ o conteudo da pasta daquele idioma, que e o
    passo que todo mundo esquece e que faz o LaTeX reclamar de arquivo que
    esta ali do lado.

    Tenta o release mais recente; se nao houver, o zip do ramo master.
    """
    import json
    import tempfile
    import urllib.request
    import zipfile

    def pega(url, binario=True):
        pedido = urllib.request.Request(
            url, headers={"User-Agent": "CoppeTeX-geradocvazio"})
        with urllib.request.urlopen(pedido, timeout=60) as r:
            return r.read() if binario else r.read().decode("utf-8")

    aviso("")
    aviso("baixando a classe do GitHub...")
    dados = None
    try:
        meta = json.loads(pega(
            "https://api.github.com/repos/%s/releases/latest" % REPO, False))
        for a in meta.get("assets", []):
            if a["name"].lower().endswith(".zip"):
                aviso("   release %s, anexo %s" % (meta.get("tag_name", "?"),
                                                   a["name"]))
                dados = pega(a["browser_download_url"])
                break
    except Exception as e:                      # rede, proxy, API fora do ar
        aviso("   nao consegui ler o release (%s)" % e)

    de_dentro_do_repo = False
    if dados is None:
        try:
            aviso("   tentando o ramo master...")
            dados = pega("https://codeload.github.com/%s/zip/refs/heads/master"
                         % REPO)
            de_dentro_do_repo = True
        except Exception as e:
            aviso("   NAO DEU: %s" % e)
            aviso("   Baixe a entrega a mao em"
                  " https://github.com/%s/releases/latest" % REPO)
            return False

    temp = tempfile.mkdtemp(prefix="coppe-baixa-")
    try:
        caminho = os.path.join(temp, "entrega.zip")
        io.open(caminho, "wb").write(dados)
        with zipfile.ZipFile(caminho) as z:
            z.extractall(temp)

        # Achar a pasta que faz as vezes de dist/: no zip do release e a pasta
        # unica de dentro; no zip do ramo e <repo>-master/dist.
        base = None
        for raiz, pastas, nomes in os.walk(temp):
            if "coppe.cls" in nomes:
                base = raiz
                break
        if base is None:
            aviso("   o arquivo baixado nao tem coppe.cls dentro")
            return False
        if de_dentro_do_repo:
            aviso("   (do ramo master, pasta dist/)")

        trazidos = 0
        for raiz, pastas, nomes in os.walk(base):
            rel_pasta = os.path.relpath(raiz, base)
            # As pastas de OUTROS idiomas nao vem; a do idioma escolhido vem, e
            # vem PARA A RAIZ.
            topo = rel_pasta.split(os.sep)[0]
            if topo in ("en", "es", "outraslinguas", "manuais"):
                continue
            for nome in nomes:
                if not _serve_para_compilar(nome):
                    continue
                destino_pasta = pasta if rel_pasta == "." \
                    else os.path.join(pasta, rel_pasta)
                if not os.path.isdir(destino_pasta):
                    os.makedirs(destino_pasta)
                shutil.copy2(os.path.join(raiz, nome),
                             os.path.join(destino_pasta, nome))
                trazidos += 1

        # O idioma escolhido, direto para a raiz.
        qual = {"english": "en", "spanish": "es"}.get(idioma)
        if idioma in ("french", "italian"):
            qual = "outraslinguas"
        if qual:
            de = os.path.join(base, qual)
            if os.path.isdir(de):
                for nome in os.listdir(de):
                    if not _serve_para_compilar(nome):
                        continue
                    shutil.copy2(os.path.join(de, nome),
                                 os.path.join(pasta, nome))
                    trazidos += 1
                aviso("   %s/ veio para a raiz, que e onde o LaTeX procura"
                      % qual)

        aviso("   %d arquivo(s) trazidos" % trazidos)
        return True
    finally:
        shutil.rmtree(temp, ignore_errors=True)


def gerar(v, aviso=print):
    """Escreve os arquivos. Devolve a lista do que escreveu."""
    pasta = v["pasta"].strip() or "."
    pasta = os.path.abspath(pasta)
    if not os.path.isdir(pasta):
        os.makedirs(pasta)

    nome_tex = v["tex"].strip() or "main.tex"
    nome_bib = v["bib"].strip() or "references.bib"
    if not nome_tex.endswith(".tex"):
        nome_tex += ".tex"
    if not nome_bib.endswith(".bib"):
        nome_bib += ".bib"
    v = dict(v)
    v["tex"] = nome_tex

    escritos = []

    def escreve(caminho, texto):
        io.open(caminho, "w", encoding="utf-8", newline="\n").write(texto)
        escritos.append(caminho)
        aviso("   " + os.path.relpath(caminho, pasta))

    aviso("escrevendo em %s" % pasta)
    escreve(os.path.join(pasta, nome_tex), monta_tex(v, nome_bib))
    subbib = (v.get("pastabib") or "").strip().strip("/\\")
    if subbib:
        alvo = os.path.join(pasta, subbib)
        if not os.path.isdir(alvo):
            os.makedirs(alvo)
        escreve(os.path.join(alvo, nome_bib), monta_bib(v))
    else:
        escreve(os.path.join(pasta, nome_bib), monta_bib(v))
    if v["conteudo"]:
        sub = os.path.join(pasta, "conteudo")
        if not os.path.isdir(sub):
            os.makedirs(sub)
        for chave, titulo in CAPITULOS:
            escreve(os.path.join(sub, chave + ".tex"),
                    monta_capitulo(chave, titulo))
    baixou = False
    if v.get("baixar"):
        baixou = baixar_entrega(pasta, v["idioma"], aviso)

    aviso("")
    if baixou:
        aviso("%d arquivo(s) escritos, e a classe ja esta na pasta."
              % len(escritos))
        aviso("Compile com:  latexmk -pdf %s" % nome_tex[:-4])
    else:
        aviso("%d arquivo(s). Copie para esta pasta a raiz da entrega e a"
              % len(escritos))
        aviso("pasta logos/, e compile. A entrega esta em")
        aviso("https://github.com/%s/releases/latest" % REPO)
    return escritos


# ---------------------------------------------------------------------------
# Linha de comando
# ---------------------------------------------------------------------------
def ajuda():
    print(__doc__.strip())
    print("")
    print("Campos (--chave=valor):")
    aba_atual = None
    for chave, aba, rotulo, tipo, padrao, opcoes, explica in CAMPOS:
        if aba != aba_atual:
            print("")
            print("  [%s]" % aba)
            aba_atual = aba
        if tipo == "escolha":
            valores = "|".join(o[0] for o in opcoes)
        elif tipo == "sim/nao":
            valores = "sim|nao"
        elif tipo == "inteiro":
            valores = "%d..%d" % opcoes
        else:
            valores = "texto"
        print("    --%-20s %-28s padrao: %s" % (chave, valores, padrao))
    return 0


def main(argv):
    if "--ajuda" in argv or "-h" in argv or "--help" in argv:
        return ajuda()

    v = padroes()
    for arg in argv:
        if not arg.startswith("--") or "=" not in arg:
            continue
        chave, _, valor = arg[2:].partition("=")
        if chave not in v:
            print("campo desconhecido: %s (veja --ajuda)" % chave)
            return 2
        tipo = campo(chave)[3]
        if tipo == "sim/nao":
            v[chave] = valor.lower() in ("sim", "s", "1", "true", "yes")
        elif tipo == "inteiro":
            v[chave] = int(valor)
        else:
            v[chave] = valor

    if "--gerar" in argv or any(a.startswith("--") and "=" in a for a in argv):
        gerar(v)
        return 0
    return abrir_janela(v)


# ---------------------------------------------------------------------------
# Janela
# ---------------------------------------------------------------------------
def abrir_janela(valores=None):
    try:
        import tkinter as tk
        from tkinter import ttk, filedialog, messagebox, scrolledtext
    except ImportError:
        print("Este Python nao tem Tkinter, entao nao da para abrir a janela.")
        print("Tudo funciona pela linha de comando: --ajuda lista os campos,")
        print("e --gerar escreve os arquivos com os padroes da COPPE.")
        return 1

    v = valores or padroes()
    janela = tk.Tk()
    janela.title("CoppeTeX - novo documento")
    janela.geometry("880x680")

    vars_ = {}

    def valor_atual():
        d = {}
        for chave, _, _, tipo, _, _, _ in CAMPOS:
            bruto = vars_[chave].get()
            if tipo == "inteiro":
                d[chave] = int(bruto)
            else:
                d[chave] = bruto
        return d

    # --- menus --------------------------------------------------------------
    menu = tk.Menu(janela)
    arquivo = tk.Menu(menu, tearoff=0)

    def escolher_pasta():
        p = filedialog.askdirectory(title="Pasta onde gerar")
        if p:
            vars_["pasta"].set(p)

    def acao_gerar():
        try:
            d = valor_atual()
        except ValueError:
            messagebox.showerror("CoppeTeX", "Ha um numero invalido num campo.")
            return
        registro.delete("1.0", "end")
        try:
            gerar(d, aviso=lambda s: (registro.insert("end", s + "\n"),
                                      registro.see("end")))
        except OSError as e:
            messagebox.showerror("CoppeTeX", "Nao consegui escrever: %s" % e)
            return
        messagebox.showinfo("CoppeTeX", "Arquivos gerados.")

    def repor():
        for chave, valor in padroes().items():
            vars_[chave].set(valor)

    arquivo.add_command(label="Escolher pasta...", command=escolher_pasta)
    arquivo.add_command(label="Gerar", command=acao_gerar)
    arquivo.add_separator()
    arquivo.add_command(label="Voltar aos padroes da COPPE", command=repor)
    arquivo.add_separator()
    arquivo.add_command(label="Sair", command=janela.destroy)
    menu.add_cascade(label="Arquivo", menu=arquivo)

    ajudam = tk.Menu(menu, tearoff=0)
    ajudam.add_command(
        label="Sobre",
        command=lambda: messagebox.showinfo(
            "CoppeTeX",
            "Gerador de documento vazio da CoppeTeX.\n\n"
            "Escreve o .tex e o .bib com que um trabalho comeca, ja com a\n"
            "estrutura que a norma pede e os cinco capitulos de sempre.\n\n"
            "Os manuais estao em manuais/ na entrega: coppe.pdf ensina os\n"
            "comandos, manual.pdf diz o que o trabalho tem de ser."))
    menu.add_cascade(label="Ajuda", menu=ajudam)
    janela.config(menu=menu)

    # --- abas ---------------------------------------------------------------
    abas = ttk.Notebook(janela)
    abas.pack(fill="both", expand=True, padx=10, pady=(10, 0))

    quadros = {}
    for nome in ABAS:
        q = ttk.Frame(abas, padding=12)
        abas.add(q, text=nome)
        quadros[nome] = q

    for chave, aba, rotulo, tipo, padrao, opcoes, explica in CAMPOS:
        pai = quadros[aba]
        linha = ttk.Frame(pai)
        linha.pack(fill="x", pady=2)
        if tipo == "sim/nao":
            var = tk.BooleanVar(value=bool(v.get(chave, padrao)))
            ttk.Checkbutton(linha, text=rotulo, variable=var,
                            width=48).pack(side="left")
        else:
            ttk.Label(linha, text=rotulo, width=40).pack(side="left")
            if tipo == "escolha":
                var = tk.StringVar(value=v.get(chave, padrao))
                rotulos = ["%s  (%s)" % (o[1], o[0]) for o in opcoes]
                caixa = ttk.Combobox(linha, values=rotulos, width=34,
                                     state="readonly")
                caixa.pack(side="left")
                # A caixa MOSTRA o rotulo em portugues e GUARDA a chave que vai
                # para o .tex. Os dois nao sao a mesma coisa: ninguem escolhe
                # "dsc" numa lista, mas e "dsc" que a classe entende.
                def ao_escolher(evento, var=var, opcoes=opcoes, caixa=caixa):
                    var.set(opcoes[caixa.current()][0])
                caixa.bind("<<ComboboxSelected>>", ao_escolher)
                atual = v.get(chave, padrao)
                for i, o in enumerate(opcoes):
                    if o[0] == atual:
                        caixa.current(i)
                        break
            elif tipo == "inteiro":
                var = tk.IntVar(value=int(v.get(chave, padrao)))
                ttk.Spinbox(linha, from_=opcoes[0], to=opcoes[1],
                            textvariable=var, width=6).pack(side="left")
            else:
                var = tk.StringVar(value=v.get(chave, padrao))
                ttk.Entry(linha, textvariable=var, width=36).pack(side="left")
        vars_[chave] = var
        if explica:
            ttk.Label(linha, text="  " + explica,
                      foreground="#666").pack(side="left")

    # --- rodape -------------------------------------------------------------
    registro = scrolledtext.ScrolledText(janela, height=8, wrap="none",
                                         font=("Consolas", 9))
    registro.pack(fill="both", expand=False, padx=10, pady=10)

    rodape = ttk.Frame(janela, padding=(10, 0, 10, 10))
    rodape.pack(fill="x")
    ttk.Label(rodape, text="Os padroes sao os da COPPE, como no exemplo "
                           "completo.").pack(side="left")
    ttk.Button(rodape, text="Gerar", command=acao_gerar).pack(side="right")
    ttk.Button(rodape, text="Pasta...",
               command=escolher_pasta).pack(side="right", padx=6)

    janela.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
