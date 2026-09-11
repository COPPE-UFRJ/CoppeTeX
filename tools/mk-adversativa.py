# -*- coding: utf-8 -*-
"""Gera os 12 documentos da revisao adversativa em src/adversativa/."""
import os
OUT = "adversativa"

L = {
 "pt": dict(babel="brazilian", opt=None,
   ack="Agradecimentos",
   ded="A quem soube esperar.",
   abs_="Este documento existe para ser difícil. Ele aciona, de propósito e ao mesmo tempo, tudo o que a classe oferece: os cinco níveis de seção, os cinco tipos de ilustração, as três listas próprias da COPPE, a citação longa, as siglas, os símbolos, as abreviaturas, o índice remissivo, os apêndices e os anexos. Se alguma coisa quebra, quebra aqui.",
   ch=["Introdução","Todos os níveis de seção","Todas as ilustrações","Citações, símbolos e siglas","Conclusões"],
   sec=["Seção secundária","Subseção terciária","Subsubseção quaternária","Nível quinário"],
   fig="Figura de teste", tab="Tabela de teste", qua="Quadro de teste",
   prog="Programa de teste", alg="Algoritmo de teste",
   src="Elaboração própria.",
   quote="Uma citação com mais de três linhas é recuada em quatro centímetros a partir da margem esquerda, composta em corpo menor e em espaço simples, e não leva aspas. É o que a norma pede e é o que este parágrafo verifica, ocupando linhas suficientes para que o recuo se veja.",
   app=["Um apêndice","Outro apêndice"], anx=["Um anexo","Outro anexo"],
   appt="Apêndice é texto elaborado pelo próprio autor, para complementar a argumentação sem ser essencial à compreensão do texto principal.",
   anxt="Anexo é documento não elaborado pelo autor, que serve de fundamentação, comprovação ou ilustração.",
   body="Parágrafo de corpo, para conferir o recuo da primeira linha, o espaçamento de uma linha e meia e a mancha gráfica.",
   ),
 "en": dict(babel="english", opt="english",
   ack="Acknowledgements",
   ded="To those who waited.",
   abs_="This document exists to be difficult. It deliberately exercises everything the class offers at once: the five section levels, the five kinds of illustration, the three COPPE-specific lists, the long quotation, the acronyms, the symbols, the abbreviations, the index, the appendices and the annexes. If anything breaks, it breaks here.",
   ch=["Introduction","Every section level","Every illustration","Quotations, symbols and acronyms","Conclusions"],
   sec=["Secondary section","Tertiary subsection","Quaternary subsubsection","Quinary level"],
   fig="Test figure", tab="Test table", qua="Test frame",
   prog="Test program", alg="Test algorithm",
   src="Prepared by the author.",
   quote="A quotation longer than three lines is indented four centimetres from the left margin, set in the smaller font and single spaced, and carries no quotation marks. That is what the norm asks for and what this paragraph checks, running long enough for the indentation to be visible.",
   app=["An appendix","Another appendix"], anx=["An annex","Another annex"],
   appt="An appendix is a text written by the author to complement the argument without being essential to understanding the main text.",
   anxt="An annex is a document not written by the author, serving as grounding, evidence or illustration.",
   body="A body paragraph, to check the first-line indentation, the one-and-a-half spacing and the text block.",
   ),
 "es": dict(babel="spanish", opt="spanish",
   ack="Agradecimientos",
   ded="A quienes supieron esperar.",
   abs_="Este documento existe para ser difícil. Ejercita a propósito y al mismo tiempo todo lo que ofrece la clase: los cinco niveles de sección, los cinco tipos de ilustración, las tres listas propias de la COPPE, la cita larga, las siglas, los símbolos, las abreviaturas, el índice, los apéndices y los anexos. Si algo se rompe, se rompe aquí.",
   ch=["Introducción","Todos los niveles de sección","Todas las ilustraciones","Citas, símbolos y siglas","Conclusiones"],
   sec=["Sección secundaria","Subsección terciaria","Subsubsección cuaternaria","Nivel quinario"],
   fig="Figura de prueba", tab="Tabla de prueba", qua="Cuadro de prueba",
   prog="Programa de prueba", alg="Algoritmo de prueba",
   src="Elaboración propia.",
   quote="Una cita de más de tres líneas se sangra cuatro centímetros desde el margen izquierdo, se compone en cuerpo menor y a espacio simple, y no lleva comillas. Es lo que pide la norma y lo que verifica este párrafo, ocupando líneas suficientes para que la sangría se vea.",
   app=["Un apéndice","Otro apéndice"], anx=["Un anexo","Otro anexo"],
   appt="El apéndice es un texto elaborado por el propio autor para complementar su argumentación sin ser esencial para comprender el texto principal.",
   anxt="El anexo es un documento no elaborado por el autor, que sirve de fundamentación, comprobación o ilustración.",
   body="Párrafo de cuerpo, para comprobar la sangría de primera línea, el interlineado de uno y medio y la mancha gráfica.",
   ),
}

TIPOS = [("mscexam","Exame de Qualificação de Mestrado"),
         ("dscexam","Exame de Qualificação de Doutorado"),
         ("msc","Dissertação de Mestrado"),
         ("dsc","Tese de Doutorado")]

DEPTS = ["PESC","PEB","PEC","PEE","PEM","PEMM","PEN","PENO","PEP","PEQ","PET","PPE"]

TIT = {"pt":"Um documento adversativo para a classe CoppeTeX",
       "en":"An adversarial document for the CoppeTeX class",
       "es":"Un documento adversativo para la clase CoppeTeX"}
SUB = {"pt":"tudo o que a classe oferece, ao mesmo tempo",
       "en":"everything the class offers, all at once",
       "es":"todo lo que ofrece la clase, a la vez"}

# As categorias de referencia da secao 4.2 do Manual UFRJ/SiBI 2026, na ordem
# do Manual, e a chave da entrada correspondente em referencias-manual.bib.
PROVA_REFS = [
    ("m-4211",  "4.2.1.1 monografia no todo"),
    ("m-4212",  "4.2.1.2 monografia em meio eletrônico"),
    ("m-4213",  "4.2.1.3 parte de monografia"),
    ("m-422",   "4.2.2 correspondência"),
    ("m-4221",  "4.2.2.1 correspondência em meio eletrônico"),
    ("m-4231",  "4.2.3.1 publicação periódica no todo"),
    ("m-4233",  "4.2.3.3 parte de revista"),
    ("m-4234",  "4.2.3.4 artigo de revista"),
    ("m-4235",  "4.2.3.5 artigo de revista em meio eletrônico"),
    ("m-4236",  "4.2.3.6 matéria de jornal"),
    ("m-4237",  "4.2.3.7 matéria de jornal assinada em meio eletrônico"),
    ("m-4238",  "4.2.3.8 matéria de jornal não assinada em meio eletrônico"),
    ("m-4241",  "4.2.4.1 evento no todo"),
    ("m-4243",  "4.2.4.3 evento no todo em meio eletrônico"),
    ("m-4245",  "4.2.4.5 trabalho apresentado em evento"),
    ("m-4246",  "4.2.4.6 trabalho em evento em meio eletrônico"),
    ("m-425",   "4.2.5 patente"),
    ("m-4251",  "4.2.5.1 patente em meio eletrônico"),
    ("m-4261",  "4.2.6.1 legislação"),
    ("m-4262",  "4.2.6.2 jurisprudência"),
    ("m-4263",  "4.2.6.3 ato administrativo normativo"),
    ("m-427",   "4.2.7 documento jurídico em meio eletrônico"),
    ("m-428",   "4.2.8 documento civil e de cartório"),
    ("m-429",   "4.2.9 documento audiovisual"),
    ("m-42101", "4.2.10 partitura"),
    ("m-42102", "4.2.10.1 partitura em meio eletrônico"),
    ("m-42111", "4.2.11 documento iconográfico"),
    ("m-42112", "4.2.11.1 documento iconográfico em meio eletrônico"),
    ("m-42121", "4.2.12 documento cartográfico"),
    ("m-42122", "4.2.12.1 documento cartográfico em meio eletrônico"),
    ("m-42131", "4.2.13 documento tridimensional"),
    ("m-4214",  "4.2.14 documento de acesso exclusivo em meio eletrônico"),
    ("m-diss",  "dissertação de mestrado"),
    ("m-norma", "norma técnica"),
]

def doc(i, tipo, tiponome, lang):
    d = L[lang]
    # UM documento da suite -- a tese de doutorado em portugues -- e levado ao
    # extremo: mais de um exemplo em cada lista, indice remissivo com
    # subentradas e remissivas, glossario pos-textual, apendice com longtable
    # que atravessa folhas e anexo com PDF externo incluido. Os outros onze
    # ficam enxutos de proposito: eles cobrem a matriz de opcoes e de idiomas,
    # e um documento gigante em cada um deles so faria a prova demorar.
    ext = (tipo == "dsc" and lang == "pt")
    opts = [tipo]
    if d["opt"]: opts.append(d["opt"])
    # Nenhuma opcao de fluxo aqui, de proposito: estes documentos acionam TODAS
    # as listas ao mesmo tempo, que e o caso em que o pdfTeX estoura os 16
    # fluxos, e o ponto e verificar que a classe resolve isso SOZINHA, no
    # caminho padrao, sem o autor saber que o problema existe.
    opts += ["pdfa","coorientador"]
    if i % 2 == 1: opts.append("numbers")
    if i % 3 == 0: opts.append("twoside")
    if i % 4 == 0: opts.append("doublespacing")
    if i % 2 == 0: opts.append("rascunhoficha")
    if i == 7:     opts.append("listasnosumario")
    # Um documento leva `comserifa': desde a v4.1 a classe compoe sem serifa por
    # padrao, e a opcao de voltar a serifa precisa de pelo menos uma prova.
    if i == 5:     opts.append("comserifa")
    # Metade leva `orientadorexamina'. Desde a v4.1 a folha de aprovacao lista
    # so os examinadores; os dois caminhos -- com e sem o orientador na banca --
    # precisam de prova, e em bancas de tamanhos diferentes, porque o
    # espacamento da folha depende de quantos nomes ela realmente imprime.
    if i % 2 == 1: opts.append("orientadorexamina")
    # Um documento leva `semlinks': os links continuam existindo, so perdem a
    # cor e a moldura. Precisa de prova em documento grande porque o que se quer
    # verificar e que os bookmarks e os \autoref continuam funcionando.
    if i == 2:     opts.append("semlinks")
    dept = DEPTS[i % len(DEPTS)]
    nadv  = 1 if i % 3 == 0 else 2
    nexam = 2 + (i % 4)

    t = []
    A = t.append
    A("%% Documento da revisao adversativa -- GERADO por tools/mk-adversativa.py.")
    A("%%%% tipo=%s idioma=%s programa=%s" % (tipo, lang, dept))
    A("%% Opcoes: " + ", ".join(opts))
    A("\\documentclass[" + ",".join(opts) + "]{coppe}")
    A("")
    A("\\usepackage[most]{tcolorbox}")
    A("\\usepackage{makeidx}\\makeindex")
    if ext:
        A("\\usepackage{pdfpages}   % anexo com PDF externo")
    A("\\addbibresource{example.bib}")
    # Prova de referencias: so nos documentos em portugues, porque os dados sao
    # os exemplos do proprio Manual UFRJ/SiBI e sao em portugues. Os quatro
    # documentos pt cobrem os dois sistemas de chamada -- autor-data e, com a
    # opcao `numbers', numerico -- sobre a MESMA bibliografia.
    if lang == "pt":
        A("\\addbibresource{referencias-manual.bib}")
    A("\\makelosymbols")
    A("\\makeloabbreviations")
    A("")
    A("\\begin{document}")
    A("")
    A("  \\title{%s}" % TIT["pt"])
    A("  \\subtitle{%s}" % SUB["pt"])
    A("  \\foreigntitle{%s}" % TIT["en"])
    A("  \\foreignsubtitle{%s}" % SUB["en"])
    if lang == "es":
        A("  \\titlein{spanish}{%s}" % TIT["es"])
        A("  \\subtitlein{spanish}{%s}" % SUB["es"])
    A("  \\volumes{2}\\volume{1}")
    A("  \\author{Nome do}{Autor Adversativo}")
    # Ordem dos argumentos desde a v4.1: nome, sobrenome, titulacao e
    # instituicao, com o tratamento no argumento OPCIONAL. O primeiro orientador
    # leva tratamento e o segundo nao, de proposito: os dois caminhos precisam
    # de prova. A instituicao vazia tambem: e obrigatoria, mas aceita ficar em
    # branco.
    for k in range(nadv):
        trat = "[Prof.]" if k == 0 else ""
        A("  \\advisor%s{Orientador}{Numero %d}{D.Sc.}{UFRJ}" % (trat, k+1))
    A("  \\coadvisor{Coorientador}{Primeiro}{Ph.D.}{UFF}")
    for k in range(nexam):
        inst = ["UFRJ","","UFF","UNIRIO","USP"][k % 5]
        A("  \\examiner{Examinador Numero %d}{D.Sc.}{%s}" % (k+1, inst))
    A("  \\department{%s}" % dept)
    A("  \\date{09}{2026}")
    # Um documento fica SEM data de aprovacao, de proposito: e o caso em que a
    # folha tem de escrever "a ser determinada", e ele precisa de prova tanto
    # quanto o caso com data.
    if i != 4:
        A("  \\dataaprovacao{15 de setembro de 2026}")
    A("  \\areaconcentracao{Engenharia de Sistemas e Computação}")
    A("  \\linhapesquisa{Engenharia de Dados e Conhecimento}")
    A("  \\tipoproducao{bibliografica}")
    A("  \\projetovinculado{sim}")
    A("  \\nomeprojeto{Projeto Adversativo}")
    A("  \\agenciafomento{Conselho Nacional de Desenvolvimento Científico e Tecnológico}{CNPq}")
    # Duas agências, e não uma: o Anexo H pede "Agência(s)", e a segunda
    # chamada é a que exercita a acumulação -- uma só nunca a exercitaria.
    A("  \\agenciafomento{Fundação Carlos Chagas Filho de Amparo à Pesquisa do "
      "Estado do Rio de Janeiro}{FAPERJ}")
    if i % 2 == 1:
        A("  \\fichacatalografica{coppe-logo.pdf}")
    A("  \\keyword{Adversativo}\\keyword{Conformidade}")
    A("  \\foreignkeyword{Adversarial}\\foreignkeyword{Conformance}")
    if lang == "es":
        A("  \\braziliankeyword{Adversativo}\\braziliankeyword{Conformidade}")
    A("")
    A("  \\maketitle")
    A("  \\frontmatter")
    A("  \\dedication{%s}" % d["ded"])
    A("")
    A("  \\chapter*{%s}" % d["ack"])
    A("  %s" % d["body"])
    A("")
    A("  \\begin{abstract}")
    A("  %s" % d["abs_"])
    A("  \\end{abstract}")
    A("")
    A("  \\begin{foreignabstract}")
    A("  %s" % (L["pt"]["abs_"] if lang == "en" else L["en"]["abs_"]))
    A("  \\end{foreignabstract}")
    if lang == "es":
        A("")
        A("  \\begin{brazilianabstract}")
        A("  %s" % L["pt"]["abs_"])
        A("  \\end{brazilianabstract}")
    A("")
    A("  \\listoffigures")
    A("  \\listoftables")
    A("  \\listofquadros")
    A("  \\listofprogramas")
    A("  \\listofalgorithms")
    A("  \\printloabbreviations")
    A("  \\printlosymbols")
    A("  \\tableofcontents")
    A("")
    A("  \\mainmatter")
    # cap 1
    A("  \\chapter{%s}\\label{cap:intro}" % d["ch"][0])
    A("  %s\\index{adversativo}" % d["body"])
    A("")
    # cap 2 -- cinco niveis
    A("  \\chapter{%s}" % d["ch"][1])
    A("  %s" % d["body"])
    A("  \\section{%s}" % d["sec"][0])
    A("  %s" % d["body"])
    A("  \\subsection{%s}" % d["sec"][1])
    A("  %s" % d["body"])
    A("  \\subsubsection{%s}" % d["sec"][2])
    A("  %s" % d["body"])
    A("  \\paragraph{%s}" % d["sec"][3])
    A("  %s" % d["body"])
    A("")
    # cap 3 -- ilustracoes
    A("  \\chapter{%s}" % d["ch"][2])
    A("  \\begin{figure}[ht]")
    A("    \\centering\\includegraphics[height=3cm]{coppe-logo}")
    A("    \\caption{%s}\\label{fig:adv}" % d["fig"])
    A("    \\source{%s}" % d["src"])
    A("  \\end{figure}")
    A("  \\begin{table}[ht]")
    A("    \\centering\\caption{%s}\\label{tab:adv}" % d["tab"])
    A("    \\begin{tabular}{lrr}\\hline A & 1 & 2\\\\ B & 3 & 4\\\\ \\hline\\end{tabular}")
    A("    \\source{%s}" % d["src"])
    A("  \\end{table}")
    A("  \\begin{quadro}[ht]")
    A("    \\centering\\caption{%s}\\label{qua:adv}" % d["qua"])
    A("    \\begin{tabular}{|l|l|}\\hline A & B\\\\ \\hline C & D\\\\ \\hline\\end{tabular}")
    A("    \\source{%s}" % d["src"])
    A("  \\end{quadro}")
    A("  \\begin{python}[caption={%s},label=prog:adv]" % d["prog"])
    A("def adversativo(n):")
    A("    # uma linha bastante longa, de proposito, para acionar a quebra do listings e o gancho vermelho do postbreak")
    A("    return sum(i * i for i in range(n))")
    A("  \\end{python}")
    A("  \\source{%s}" % d["src"])
    A("  \\begin{algorithm}[H]")
    A("    \\caption{%s}\\label{alg:adv}" % d["alg"])
    A("    \\KwIn{$n$}")
    A("    \\KwOut{$s$}")
    A("    $s \\leftarrow 0$\\;")
    A("    \\For{$i \\leftarrow 1$ \\KwTo $n$}{$s \\leftarrow s + i$\\;}")
    A("    \\Return $s$\\;")
    A("  \\end{algorithm}")
    A("  \\source{%s}" % d["src"])
    if ext:
        A("")
        A("  \\section{Mais de um exemplo em cada lista}")
        A("  Uma lista com uma entrada só não prova que a lista é uma lista.")
        A("  \\begin{figure}[ht]")
        A("    \\centering")
        A("    \\begin{subfigure}[b]{0.35\\textwidth}")
        A("      \\centering\\includegraphics[height=2cm]{ufrj-logo}")
        A("      \\caption{A marca da Universidade}\\label{fig:sub-ufrj}")
        A("    \\end{subfigure}\\hfill")
        A("    \\begin{subfigure}[b]{0.35\\textwidth}")
        A("      \\centering\\includegraphics[height=2cm]{coppe-logo}")
        A("      \\caption{A marca do Instituto}\\label{fig:sub-coppe}")
        A("    \\end{subfigure}")
        A("    \\caption{Duas subfiguras numa figura só}\\label{fig:subs}")
        A("    \\source{Elaboração própria.}")
        A("  \\end{figure}")
        A("  \\begin{figure}[ht]")
        A("    \\centering\\includegraphics[height=2.5cm]{ufrj-logo}")
        A("    \\caption{Uma terceira figura, com legenda deliberadamente longa para")
        A("      que ela ocupe mais de uma linha e mostre o alinhamento das legendas")
        A("      de várias linhas}\\label{fig:adv3}")
        A("    \\source{Elaboração própria.}")
        A("  \\end{figure}")
        A("  \\begin{table}[ht]")
        A("    \\centering\\caption{Segunda tabela, com \\texttt{booktabs}}\\label{tab:adv2}")
        A("    \\begin{tabular}{lrr}\\toprule")
        A("      Item & Medido & Esperado\\\\ \\midrule")
        A("      Fólio, topo & 2{,}019 cm & 2 cm\\\\")
        A("      Fólio, direita & 2{,}019 cm & 2 cm\\\\")
        A("      Margem esquerda & 3{,}000 cm & 3 cm\\\\ \\bottomrule")
        A("    \\end{tabular}")
        A("    \\source{Medição no PDF composto.}")
        A("  \\end{table}")
        A("  \\begin{table}[ht]")
        A("    \\centering\\caption{Terceira tabela, com \\texttt{tabularx}}\\label{tab:adv3}")
        A("    \\begin{tabularx}{\\textwidth}{lX}\\hline")
        A("      Campo & Descrição\\\\ \\hline")
        A("      \\texttt{evento} & Nome do evento, em caixa alta, antes do título dos anais, como pede a 4.2.4 do Manual.\\\\")
        A("      \\texttt{deposito} & Data de depósito da patente (4.2.5).\\\\ \\hline")
        A("    \\end{tabularx}")
        A("    \\source{Elaboração própria.}")
        A("  \\end{table}")
        A("  \\begin{quadro}[ht]")
        A("    \\centering\\caption{Segundo quadro}\\label{qua:adv2}")
        A("    \\begin{tabular}{|l|l|}\\hline Escolha & A COPPE fixa uma forma\\\\ \\hline")
        A("      Acréscimo & O Manual não prevê\\\\ \\hline\\end{tabular}")
        A("    \\source{NORMA\\_COPPE\\_2026.}")
        A("  \\end{quadro}")
        A("  \\begin{quadro}[ht]")
        A("    \\centering\\caption{Terceiro quadro}\\label{qua:adv3}")
        A("    \\begin{tabular}{|l|l|}\\hline Dado próprio & O valor é da COPPE\\\\ \\hline")
        A("      Reafirmação & Repete-se por ser fonte de erro\\\\ \\hline\\end{tabular}")
        A("    \\source{NORMA\\_COPPE\\_2026.}")
        A("  \\end{quadro}")
        A("  \\begin{xml}[caption={Segundo programa, em XML},label=prog:adv2]")
        A("<norma edicao=\"2026\">")
        A("  <secao tipo=\"Escolha\">Logomarcas</secao>")
        A("</norma>")
        A("  \\end{xml}")
        A("  \\source{Elaboração própria.}")
        A("  \\begin{java}[caption={Terceiro programa, em Java},label=prog:adv3]")
        A("public static int adversativo(int n) {")
        A("    return n * (n + 1) / 2;")
        A("}")
        A("  \\end{java}")
        A("  \\source{Elaboração própria.}")
        A("  \\begin{algorithm}[H]")
        A("    \\caption{Segundo algoritmo}\\label{alg:adv2}")
        A("    \\KwIn{Uma lista $L$}")
        A("    \\KwOut{O maior elemento}")
        A("    $m \\leftarrow -\\infty$\\;")
        A("    \\ForEach{$x \\in L$}{\\lIf{$x > m$}{$m \\leftarrow x$}}")
        A("    \\Return $m$\\;")
        A("  \\end{algorithm}")
        A("  \\source{Elaboração própria.}")
        A("  \\begin{algorithm}[H]")
        A("    \\caption{Terceiro algoritmo}\\label{alg:adv3}")
        A("    \\KwIn{$a$, $b$}")
        A("    \\While{$b \\neq 0$}{$(a,b) \\leftarrow (b, a \\bmod b)$\\;}")
        A("    \\Return $a$\\;")
        A("  \\end{algorithm}")
        A("  \\source{Elaboração própria.}")
    A("")
    # cap 4 -- citacoes, simbolos, siglas, equacoes
    A("  \\chapter{%s}" % d["ch"][3])
    A("  %s \\citep{book-example}" % d["body"])
    A("  \\begin{longquote}")
    A("  %s" % d["quote"])
    A("  \\end{longquote}")
    A("  %s\\footnote{%s}" % (d["body"], d["body"]))
    A("  \\begin{equation}")
    A("    E = mc^{2} \\label{eq:adv}")
    A("  \\end{equation}")
    A("  \\symbl{$\\alpha$}{%s}" % d["body"][:28])
    A("  \\symbl{$\\beta$}{%s}" % d["body"][:28])
    A("  \\abbrev{CoppeTeX}{%s}" % d["body"][:28])
    A("  \\abbrev[ABNT]{ABNT}{Associação Brasileira de Normas Técnicas}")
    A("  \\newsigla{ufrj}{UFRJ}{Universidade Federal do Rio de Janeiro}")
    A("  \\newsigla{cpgp}{CPGP}{Comissão de Programas de Pós-Graduação}")
    A("  \\sigla{ufrj} \\sigla{cpgp} \\sigla{ufrj}")
    if ext:
        A("")
        A("  \\section{Um título de seção deliberadamente longo, para que ele quebre")
        A("    em duas linhas no sumário e mostre onde a segunda linha começa}")
        A("  Mais símbolos e mais abreviaturas, porque uma lista de um item só não")
        A("  prova nada sobre a ordenação:")
        A("  \\symbl{$\\gamma$}{Terceira letra, terceiro símbolo}")
        A("  \\symbl{$\\Delta$}{Variação entre o medido e o esperado}")
        A("  \\symbl{$\\sum$}{Somatório sobre as folhas conferidas}")
        A("  \\symbl{$\\int$}{Integral, para exercitar um símbolo grande}")
        A("  \\abbrev{SiBI}{Sistema de Bibliotecas e Informação da UFRJ}")
        A("  \\abbrev{CAPES}{Coordenação de Aperfeiçoamento de Pessoal de Nível Superior}")
        A("  \\abbrev{PDF/A}{Formato de arquivamento de longo prazo}")
        A("  \\abbrev{CEPG}{Conselho de Ensino para Graduados e Pesquisa}")
        A("  \\newsigla{sibi}{SiBI}{Sistema de Bibliotecas e Informação}")
        A("  \\newsigla{capes}{CAPES}{Coordenação de Aperfeiçoamento de Pessoal de Nível Superior}")
        A("  \\sigla{sibi} \\sigla{capes} \\sigla{sibi} \\sigla{capes}")
        A("")
        A("  \\subsection{Todas as formas de citar}")
        A("  Citação entre parênteses \\citep{book-example}; citação textual, em que")
        A("  \\citet{article-example} é sujeito da frase; só o autor,")
        A("  \\citeauthor{book-example}; só o ano, \\citeyear{book-example}; e a")
        A("  citação direta com página, \\citep[p.~37]{m-4234}. O \\emph{apud}, que a")
        A("  4.1.2.2.1 admite apenas quando o original é inacessível:")
        A("  \\citeauthor{m-4211} \\emph{apud} \\citet{book-example}.")
        A("  \\index{citação!autor-data}\\index{citação!numérica}")
        A("  \\index{referência|see{citação}}")
        A("")
        A("  \\subsection{Todas as formas de equação}")
        A("  Uma equação numerada, a \\autoref{eq:adv}, já apareceu. Um sistema:")
        A("  \\begin{align}")
        A("    a &= b + c \\label{eq:align1}\\\\")
        A("    d &= e - f \\label{eq:align2}")
        A("  \\end{align}")
        A("  Uma definição por casos:")
        A("  \\begin{equation}\\label{eq:cases}")
        A("    \\mathrm{conforme}(x) = \\begin{cases}")
        A("      1, & \\text{se } x \\text{ obedece à norma},\\\\")
        A("      0, & \\text{caso contrário.}")
        A("    \\end{cases}")
        A("  \\end{equation}")
        A("  Uma matriz, e a referência cruzada à \\eqref{eq:cases} na")
        A("  folha~\\pageref{eq:cases}:")
        A("  \\begin{equation}\\label{eq:matriz}")
        A("    M = \\begin{pmatrix} 1 & 0\\\\ 0 & 1 \\end{pmatrix}")
        A("  \\end{equation}")
        A("")
        A("  \\subsection{Todas as formas de lista}")
        A("  \\begin{itemize}")
        A("    \\item Primeiro item, com aninhamento:")
        A("    \\begin{itemize}")
        A("      \\item item de segundo nível;")
        A("      \\item outro item de segundo nível.")
        A("    \\end{itemize}")
        A("    \\item Segundo item.")
        A("  \\end{itemize}")
        A("  \\begin{enumerate}")
        A("    \\item Primeiro, numerado;")
        A("    \\item segundo, também;")
        A("    \\begin{enumerate}")
        A("      \\item e um aninhado dentro dele.")
        A("    \\end{enumerate}")
        A("  \\end{enumerate}")
        A("  \\begin{description}")
        A("    \\item[Escolha] o Manual admite mais de uma forma e a COPPE fixa uma;")
        A("    \\item[Acréscimo] elemento que o Manual não prevê.")
        A("  \\end{description}")
        A("")
        A("  \\subsection{Caixas, verbatim e notas}")
        A("  \\begin{tcolorbox}[title=Uma caixa com título]")
        A("    O \\texttt{tcolorbox} produz transparência, que é justamente o que o")
        A("    PDF/A-1b proibiria e o a-2b admite.")
        A("  \\end{tcolorbox}")
        A("  \\begin{tcolorbox}[colback=white,colframe=black,title=Uma segunda caixa]")
        A("    Duas caixas, porque uma só não mostra que o estilo se repete.")
        A("  \\end{tcolorbox}")
        A("  \\begin{Verbatim}[frame=single]")
        A("  pdflatex coppe.ins   % gera todos os arquivos derivados")
        A("  \\end{Verbatim}")
        A("  Uma nota de rodapé com citação dentro.\\footnote{Como em")
        A("  \\citet{m-norma}, a nota sai em corpo menor, 2.2(b).}")
        A("  \\index{norma!ABNT}\\index{norma!UFRJ}\\index{PDF/A}")
    A("")
    A("  \\chapter{%s}" % d["ch"][4])
    A("  %s" % d["body"])
    A("")
    if lang == "pt":
        A("  \\chapter{Prova de referências}")
        A("  Um exemplo de cada categoria de referência da seção 4.2 do Manual")
        A("  UFRJ/SiBI, 9.\\textsuperscript{a} ed. rev. (2026), com os dados do")
        A("  próprio Manual. A referência composta pela classe está na lista de")
        A("  referências; o gabarito, como o Manual a imprime, está no comentário")
        A("  de cada entrada de \\texttt{referencias-manual.bib}.")
        A("  \\begin{itemize}")
        for chave, rot in PROVA_REFS:
            A("    \\item %s \\citep{%s}" % (rot, chave))
        A("  \\end{itemize}")
        A("")
    A("  \\backmatter")
    A("  \\nocite{article-example,manualbib}")
    A("  \\printbibliography")
    A("")
    if ext:
        # Glossario e POS-textual (3.1.4.2): vem depois das referencias e antes
        # dos apendices. O ambiente theglossary da classe e o mesmo que compoe
        # as listas de simbolos e de abreviaturas, mas fora do bloco
        # pre-textual ele entra no sumario como capitulo proprio.
        A("  \\begin{theglossary}")
        A("    \\item[Adversativo] documento escrito para acionar ao mesmo tempo")
        A("      tudo o que a classe oferece, e assim revelar o que um exemplo")
        A("      bem-comportado esconde.")
        A("    \\item[Fólio] o número da folha, impresso a 2\\,cm da borda superior")
        A("      e da direita, em corpo menor (2.2(b) e 2.7).")
        A("    \\item[Folha adicional] a folha que traz a ficha catalográfica e os")
        A("      campos da Coleta CAPES; não é contada nem numerada (3.1.2.1.2).")
        A("    \\item[Gabarito] a referência como o Manual a imprime, contra a qual")
        A("      se compara a que a classe compôs.")
        A("    \\item[Quadro] ilustração delimitada por linhas em todas as bordas,")
        A("      ao contrário da tabela, fechada só no topo e na base.")
        A("  \\end{theglossary}")
        A("")
    A("  \\appendix")
    for k, tt in enumerate(d["app"]):
        A("  \\chapter{%s}" % tt)
        A("  %s" % (d["appt"] if k == 0 else d["body"]))
    if ext:
        A("  \\chapter{Um apêndice com uma tabela que atravessa folhas}")
        A("  A \\texttt{longtable} quebra em várias folhas e repete o cabeçalho.")
        A("  É o caso em que a legenda, a fonte e o fólio têm de continuar")
        A("  obedecendo à norma folha após folha.")
        A("  \\begin{longtable}{rll}")
        A("    \\caption{Conferências do \\texttt{conferir-norma.py}, uma a uma}")
        A("    \\label{tab:long}\\\\")
        A("    \\hline Nº & Item & Cláusula\\\\ \\hline")
        A("    \\endfirsthead")
        A("    \\hline Nº & Item & Cláusula\\\\ \\hline")
        A("    \\endhead")
        A("    \\hline \\multicolumn{3}{r}{\\footnotesize continua na folha seguinte}\\\\")
        A("    \\endfoot")
        A("    \\hline")
        A("    \\endlastfoot")
        for k in range(1, 41):
            it = ["A4 retrato","Fólio ao topo","Fólio à direita","Margem esquerda",
                  "Primeira folha numerada","Nenhuma pré-textual numerada",
                  "Abertura do sumário","Referências no sumário","Apêndice no sumário",
                  "Anexo no sumário","Apêndice centralizado","Anexo centralizado",
                  "Folha de aprovação numa folha","Resumo com orientador",
                  "Resumo com palavras-chave"][ (k-1) % 15 ]
            cl = ["2.2(a)","2.7","2.7","2.3","2.7","2.7","3.1.2.1.6","3.1.2.1.6",
                  "3.1.2.1.6","3.1.2.1.6","2.6","2.6","3.1.2.1.3","3.1.2.1.4",
                  "3.1.2.1.4"][ (k-1) % 15 ]
            A("    %d & %s & %s\\\\" % (k, it, cl))
        A("  \\end{longtable}")
        A("  \\source{Elaboração própria, a partir do Manual UFRJ/SiBI 2026.}")
    A("")
    A("  \\annex")
    for k, tt in enumerate(d["anx"]):
        A("  \\chapter{%s}" % tt)
        A("  %s" % (d["anxt"] if k == 0 else d["body"]))
    if ext:
        A("  \\chapter{Um anexo que reproduz um PDF externo}")
        A("  Anexo é documento de terceiro, e documento de terceiro costuma chegar")
        A("  como PDF pronto. O \\texttt{pdfpages} insere as folhas do arquivo")
        A("  original; o \\texttt{pagecommand} devolve o estilo da página, senão as")
        A("  folhas inseridas sairiam sem fólio, contrariando a 2.7.")
        A("  \\includepdf[pages=-,scale=0.85,pagecommand={\\thispagestyle{fancy}}]{coppe-logo.pdf}")
    A("")
    A("  \\printindex")
    A("  \\coppetexfinalpage")
    A("\\end{document}")
    return "\n".join(t) + "\n"

os.makedirs(OUT, exist_ok=True)
i = 0
nomes = []
for tipo, tiponome in TIPOS:
    for lang in ("pt","en","es"):
        nome = "adv_%s_%s" % (tipo, lang)
        open(os.path.join(OUT, nome + ".tex"), "w", encoding="utf-8").write(doc(i, tipo, tiponome, lang))
        nomes.append(nome); i += 1
print("\n".join(nomes))
print("total:", len(nomes))
