# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX. NAO roda na suite normal.

BUG: (conteudo dos exemplos) o max-exemplo.tex e o exemplo.bib -- os modelos que o aluno copia -- contrariavam o Manual em pontos de conteudo: algoritmos sem fonte, nomes de agencia sem acento, capitulo com titulo em ingles, palavras-chave com inicial maiuscula, edicao digitada como ordinal, referencias repetidas e o proprio Manual citado na edicao de 2025 (#149).
ABERTO: #149

Um por um, com a regra:
  * 2.10 -- a fonte e obrigatoria abaixo de TODA ilustracao; os dois algoritmos
    do max-exemplo nao tinham \\source;
  * a folha adicional mostrava "Cientifico", "Tecnologico", "Fundacao" e
    "Amparo a Pesquisa" sem acento (convencao do projeto: UTF-8 em toda parte);
  * 2.1 -- o trabalho em portugues tinha um capitulo "Using BibLaTeX", e outro
    "Alguns outros exemplo uteis";
  * 3.1.2.1.4 -- palavras-chave comecam por letra minuscula, salvo nome proprio
    ou cientifico; o exemplo tinha "Primeira palavra-chave";
  * 4.3.4 -- edicao e numero seguido de ponto ("2. ed."); o exemplo.bib trazia
    edicoes digitadas como "2ª" e "9ª";
  * 4.4 -- a lista de referencias do exemplo repetia entradas identicas (mesmo
    autor, titulo e ano em duas chaves);
  * specs/README.md -- a norma vigente e a 9. ed. rev., 2026; o exemplo.bib
    citava o Manual como 9. ed., 2025;
  * 4.3.2.13 -- "Brasil. Supremo Tribunal Federal" digitado sem a entidade
    superior em caixa alta, que a classe (por decisao registrada junto de
    \\coppe@ucfamily) imprime como foi digitado.

Cobra-se tudo isso sem compilar, lendo src/max-exemplo.tex e src/exemplo.bib
(os dois saem do coppe.dtx: a correcao vai nos modulos maxexemplo, examplebib e
tiposbib).
"""
import io
import os
import re
import unicodedata
from medidas import relatar, RAIZ

tex = io.open(os.path.join(RAIZ, "src", "max-exemplo.tex"), encoding="utf-8").read()
bib = io.open(os.path.join(RAIZ, "src", "exemplo.bib"), encoding="utf-8").read()
problemas = []

# 2.10: fonte abaixo de todo algoritmo
for m in re.finditer(r"\\end\{algorithm\}", tex):
    seguinte = tex[m.end():m.end() + 200].lstrip()
    if not seguinte.startswith((r"\source", r"\fonte", r"\cpsource", r"\cpfonte")):
        linha = tex.count("\n", 0, m.start()) + 1
        problemas.append("max-exemplo.tex, linha %d: algoritmo sem \\source logo depois" % linha)

# acentos na folha adicional
for errado in ("Cientifico", "Tecnologico", "Fundacao Carlos", "Amparo a Pesquisa"):
    if errado in tex:
        problemas.append("max-exemplo.tex: %r sem acento" % errado)

# titulos de capitulo
for errado in (r"\chapter{Using BibLaTeX}", "exemplo úteis"):
    if errado in tex:
        problemas.append("max-exemplo.tex: titulo %r" % errado)

# palavras-chave em minuscula -- so as de trabalho em portugues: \keyword e a do
# idioma principal. (O Anexo E do Manual traz as iniciais maiusculas, contra o
# texto da 3.1.2.1.4 e da NBR 6028:2021; vale o texto.)
modelos = [("max-exemplo.tex", tex),
           ("min-exemplo.tex", io.open(os.path.join(RAIZ, "src", "min-exemplo.tex"), encoding="utf-8").read()),
           ("example_pt.tex", io.open(os.path.join(RAIZ, "src", "example_pt.tex"), encoding="utf-8").read()),
           ("tools/geradocvazio.py", io.open(os.path.join(RAIZ, "tools", "geradocvazio.py"), encoding="utf-8").read())]
for nome, fonte in modelos:
    for kw in re.findall(r"\\\\?keyword\{([^}]*)\}", fonte):
        if kw[:1].isupper():
            problemas.append("%s: palavra-chave %r comeca por maiuscula (3.1.2.1.4)" % (nome, kw))

# edicao como ordinal
for m in re.finditer(r"(edition|edicao)\s*=\s*[\"{]([^\"}]*)[\"}]", bib):
    if re.search("[ªº]", m.group(2)):
        problemas.append("exemplo.bib: %s = %r (4.3.4 pede '2. ed.')" % (m.group(1), m.group(2)))

# entradas repetidas: mesmo autor, titulo e ano (com os sinonimos em portugues)
def campo(corpo, *nomes):
    for n in nomes:
        m = re.search(r"\b%s\s*=\s*(\"(?:[^\"]*)\"|\{(?:[^{}]|\{[^{}]*\})*\}|\d+)" % n, corpo)
        if m:
            v = m.group(1).strip("\"{}")
            v = unicodedata.normalize("NFD", v)
            v = "".join(c for c in v if not unicodedata.combining(c))
            return re.sub(r"[\s{}]+", " ", v).strip().lower()
    return ""

def nomes(valor):
    """'J. Byrne' e 'Byrne, J.' viram o mesmo: sobrenome e iniciais."""
    saida = []
    for nome in re.split(r"\s+and\s+", valor):
        nome = nome.strip()
        if not nome:
            continue
        if "," in nome:
            familia, dado = nome.split(",", 1)
        else:
            partes = nome.split()
            familia, dado = partes[-1], " ".join(partes[:-1])
        iniciais = "".join(p[0] for p in re.split(r"[\s.\-]+", dado) if p)
        saida.append(familia.strip() + " " + iniciais)
    return "; ".join(saida)


def entradas_do_bib(texto):
    """(tipo, chave, corpo) de cada entrada, contando chaves -- um @Comment{...}
    que termina no meio da linha nao pode engolir a entrada seguinte."""
    i = 0
    while True:
        m = re.compile(r"@(\w+)\s*\{").search(texto, i)
        if not m:
            return
        nivel, j = 1, m.end()
        while j < len(texto) and nivel:
            if texto[j] == "{":
                nivel += 1
            elif texto[j] == "}":
                nivel -= 1
            j += 1
        bloco = texto[m.end():j - 1]
        i = j
        if m.group(1).lower() in ("comment", "preamble", "string"):
            continue
        chave, _, corpo = bloco.partition(",")
        yield m.group(1).lower(), chave.strip(), corpo


vistas = {}
for tipo, chave, corpo in entradas_do_bib(bib):
    ano = re.search(r"\d{4}", campo(corpo, "year", "ano", "date", "data"))
    ident = (nomes(campo(corpo, "author", "autor", "editor", "organizador")),
             campo(corpo, "title", "titulo"),
             ano.group(0) if ano else "")
    if not ident[1]:
        continue
    if ident in vistas:
        problemas.append("exemplo.bib: %s e %s sao a mesma referencia (%s)"
                         % (vistas[ident], chave, ident[1][:40]))
    else:
        vistas[ident] = chave

# 4.3.2.13 e a regra da classe (\coppe@ucfamily): entidade com orgao subordinado
# e digitada com a entidade superior em caixa alta -- a classe nao converte nome
# que tenha ponto
for tipo, chave, corpo in entradas_do_bib(bib):
    for m in re.finditer(r"\b(author|autor)\s*=\s*\"\{([^{}]*)\}\"", corpo):
        nome = m.group(2)
        if ". " in nome:
            superior = nome.split(". ", 1)[0]
            if superior != superior.upper():
                problemas.append("exemplo.bib: %s: entidade %r com a superior fora da caixa alta"
                                 % (chave, nome[:45]))

# o Manual na edicao vigente
m = re.search(r"@\w+\{manualbib,(.*?)\n\}", bib, re.S)
if m:
    ano = campo(m.group(1), "date", "year", "data", "ano")
    edicao = campo(m.group(1), "edition", "edicao")
    if not ano.startswith("2026") or "rev" not in edicao:
        problemas.append("exemplo.bib: manualbib cita o Manual do SiBI como edicao %r de %r; "
                         "a vigente e a 9. ed. rev., 2026" % (edicao, ano))

relatar(problemas)
