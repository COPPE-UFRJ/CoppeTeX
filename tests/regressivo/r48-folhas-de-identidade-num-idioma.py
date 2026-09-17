# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX. NAO roda na suite normal.

BUG: (inconsistencia, Norma COPPE 4 e 7) num trabalho em ingles ou espanhol, a folha de rosto e a folha de aprovacao misturavam idiomas: a frase de natureza em portugues, o rotulo do orientador em portugues e o da linha de pesquisa -- ou o "Aprobada por" -- no idioma principal (#128).
ABERTO: #128

A Norma COPPE 2026 se contradiz: a secao 4 diz que natureza, objetivo e area de
concentracao acompanham o idioma principal; a secao 7 diz que capa, folha de
rosto e folha de aprovacao sao identidade institucional e continuam em
portugues. A classe nao seguiu nenhuma das duas inteira. A decisao de QUAL
idioma e da issue; este teste cobra so o que as duas leituras tem em comum, e
que a secao 7 diz com todas as letras sobre as paginas de resumo: uma pagina com
metade do texto em um idioma e metade em outro nao serve a nenhum leitor.

Cobra-se, em trabalhos em ingles e em espanhol, que o texto que a CLASSE escreve
na folha de rosto e na folha de aprovacao esteja todo num idioma so.
"""
from medidas import Documento, relatar, normaliza

MARCAS = {
    "pt": ["Orientador", "Coorientador", "Linha de pesquisa", "Aprovada em",
           "Aprovada por", "apresentada ao Programa", "Area de concentracao"],
    "en": ["Advisor", "Co-advisor", "Research line", "Approved on", "Approved by",
           "presented to", "Concentration area"],
    "es": ["Director", "Codirector", "Linea de investigacion", "Aprobada el",
           "Aprobada por", "presentada al", "Area de concentracion"],
}

PREAMBULO = r"""\title{Documento de prova}
\foreigntitle{Proof document}
\titlein{spanish}{Documento de prueba}
\author{Nome}{Sobrenome}
\advisor{Ana}{Silva}{D.Sc.}{UFRJ}
\coadvisor{Bruno}{Souza}{D.Sc.}{UFF}
\examiner{Carla Lima}{D.Sc.}{UFRJ}
\department{PESC}
\date{09}{2026}
\dataaprovacao{1 de setembro de 2026}
\areaconcentracao{Engenharia}
\linhapesquisa{Engenharia de Dados}
\keyword{regressao}
\foreignkeyword{regression}
\braziliankeyword{regressao}
"""

problemas = []
for lingua in ("english", "spanish"):
    pre = r"\begin{abstract}Um.\end{abstract}\begin{foreignabstract}Dois.\end{foreignabstract}"
    if lingua == "spanish":
        pre += r"\begin{brazilianabstract}Tres.\end{brazilianabstract}"
    with Documento(opcoes="dsc," + lingua, preambulo=PREAMBULO, pre=pre,
                   corpo=r"\chapter{Um}Texto.") as d:
        if not d.ok:
            problemas.append("%s: nao compilou: %s" % (lingua, d.erros_do_log()))
            continue
        for folha, nome in ((2, "folha de rosto"), (4, "folha de aprovacao")):
            t = normaliza(d.texto(folha))
            achadas = {}
            for idioma, marcas in MARCAS.items():
                for m in marcas:
                    if normaliza(m) in t:
                        achadas.setdefault(idioma, []).append(m)
            # "Director" (es) contem "Director" -- e "Codirector" contem "director";
            # "Advisor" contem "advisor" de "Co-advisor". Essas colisoes so
            # acontecem DENTRO do mesmo idioma, e nao misturam idiomas.
            if len(achadas) > 1:
                problemas.append("%s, %s: idiomas misturados -- %s"
                                 % (lingua, nome, "; ".join("%s: %s" % (k, ", ".join(v))
                                                            for k, v in sorted(achadas.items()))))

relatar(problemas)
