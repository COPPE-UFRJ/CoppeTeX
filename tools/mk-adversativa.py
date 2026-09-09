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

def doc(i, tipo, tiponome, lang):
    d = L[lang]
    opts = [tipo]
    if d["opt"]: opts.append(d["opt"])
    # Nenhuma opcao de fluxo aqui, de proposito: estes documentos acionam TODAS
    # as listas ao mesmo tempo, que e o caso em que o pdfTeX estoura os 16
    # fluxos, e o ponto e verificar que a classe resolve isso SOZINHA, no
    # caminho padrao, sem o autor saber que o problema existe.
    opts += ["pdfa","assinaturas","coorientador"]
    if i % 2 == 1: opts.append("numbers")
    if i % 3 == 0: opts.append("twoside")
    if i % 4 == 0: opts.append("doublespacing")
    if i % 2 == 0: opts.append("rascunhoficha")
    if i == 7:     opts.append("listasnosumario")
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
    A("\\addbibresource{example.bib}")
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
    for k in range(nadv):
        inst = "[UFRJ]" if k == 0 else ""
        A("  \\advisor%s{Prof.}{Orientador}{Numero %d}{D.Sc.}" % (inst, k+1))
    A("  \\coadvisor[UFF]{Prof.}{Coorientador}{Primeiro}{Ph.D.}")
    for k in range(nexam):
        inst = ["[UFRJ]","","[UFF]","[UNIRIO]","[USP]"][k % 5]
        A("  \\examiner%s{Prof.}{Examinador Numero %d}{D.Sc.}" % (inst, k+1))
    A("  \\department{%s}" % dept)
    A("  \\date{09}{2026}")
    A("  \\dataaprovacao{15 de setembro de 2026}")
    A("  \\areaconcentracao{Engenharia de Sistemas e Computação}")
    A("  \\linhapesquisa{Engenharia de Dados e Conhecimento}")
    A("  \\tipoproducao{bibliografica}")
    A("  \\projetovinculado{sim}")
    A("  \\nomeprojeto{Projeto Adversativo}")
    A("  \\agenciafomento{Conselho Nacional de Desenvolvimento Científico e Tecnológico}{CNPq}")
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
    A("")
    A("  \\chapter{%s}" % d["ch"][4])
    A("  %s" % d["body"])
    A("")
    A("  \\backmatter")
    A("  \\nocite{article-example,manualbib}")
    A("  \\printbibliography")
    A("")
    A("  \\appendix")
    for k, tt in enumerate(d["app"]):
        A("  \\chapter{%s}" % tt)
        A("  %s" % (d["appt"] if k == 0 else d["body"]))
    A("")
    A("  \\annex")
    for k, tt in enumerate(d["anx"]):
        A("  \\chapter{%s}" % tt)
        A("  %s" % (d["anxt"] if k == 0 else d["body"]))
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
