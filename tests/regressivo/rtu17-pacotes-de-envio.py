# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: nao havia defeito antigo aqui -- este teste guarda os pacotes de ENVIO, o do CTAN e os do Overleaf, que nasceram em outubro de 2026. O do CTAN e da COPPE; o Overleaf tem um projeto por unidade (COPPE, Poli e IC). Todos saem em build/ e nao sao versionados: sao feitos na hora de enviar, e um arquivo que faltasse na lista so apareceria como erro de compilacao na maquina de quem recebeu.

Cobra-se, sem compilar nada:
  1. todo arquivo das listas ou e fonte de src/, ou esta na raiz, ou e gerado
     por um dos .ins -- nenhum nome que nao possa existir nunca;
  2. cada projeto do Overleaf basta sozinho e tem a arrumacao da dist-* da
     unidade: na raiz a classe, o estilo da unidade, o ufrj.ist, o latexmkrc e
     a base; em coppetex/ os estilos de bibliografia, os .lbx e .def de TODO
     idioma e os logotipos; em manuais/ os PDFs da dist-*, e nenhuma outra
     subpasta -- o aluno nao tem de mover arquivo nenhum, porque a classe poe
     coppetex/ no \\input@path;
  3. cada projeto do Overleaf tem os dois exemplos da unidade, o minimo e o
     maximo, e nenhum outro documento principal;
  4. o pacote do CTAN leva o README e a licenca, as quatro fontes (.dtx e .ins)
     e os manuais, e a arvore TDS poe cada arquivo no lugar que o TDS manda;
  5. nenhum pacote leva nada de outra unidade: o do CTAN e da COPPE, e cada
     Overleaf e so da sua;
  6. nada deles esta versionado -- eles moram em build/, que o git ignora.
"""
import io
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(RAIZ, "tools"))

from medidas import relatar  # noqa: E402
import distribuicoes as D  # noqa: E402

problemas = []

# O que os .ins geram, lido dos proprios .ins.
gerados = set()
for ins in D.INS:
    texto = io.open(os.path.join(D.SRC, ins), encoding="utf-8").read()
    gerados.update(re.findall(r"\\file\{([^}]+)\}", texto))
gerados.add("latexmkrc")          # o ufrj.ins escreve latexmkrc.tex; ver regerar()


def pode_existir(caminho):
    """Um arquivo de build/ so e legitimo se alguma coisa o produz.

    Ou um .ins o gera, ou ele e o PDF de um documento que um .ins gera (o guia
    rapido) ou que e fonte em src/ (o manual da norma, os .dtx). PDF nenhum sai
    de .ins: quem compila e o build-check.ps1.
    """
    if caminho in gerados:
        return True
    base, ext = os.path.splitext(caminho)
    if ext == ".pdf":
        return (base + ".tex" in gerados
                or os.path.exists(os.path.join(D.SRC, base + ".dtx"))
                or os.path.exists(os.path.join(D.SRC, base + ".tex")))
    return False


# 1. Nenhum nome impossivel nas duas listas (nem na arvore TDS).
entradas = [(p, e) for p in sorted(D.PACOTES)
            for e in D.PACOTES[p]["arquivos"]]
entradas += [("ctan (TDS)", e) for _, e in D.TDS]
for pacote, (sub, nome, (origem, caminho)) in entradas:
    if origem == "build":
        if not pode_existir(caminho):
            problemas.append("%s: nada produz build/%s -- nem um .ins, nem a "
                             "compilacao de uma fonte" % (pacote, caminho))
    else:
        base = {"src": D.SRC, "raiz": RAIZ, "normas": D.NORMAS}[origem]
        if not os.path.exists(os.path.join(base, *caminho.split("/"))):
            problemas.append("%s: %s/%s nao existe" % (pacote, origem, caminho))

# 2 e 3. Cada Overleaf e plano, basta sozinho e tem os dois exemplos.
UNIDADES = {
    "overleaf-coppe": ("coppe", "ufrj-coppe.sty", D.MANUAIS_COPPE),
    "overleaf-poli": ("poli", "ufrj-poli.sty", D.MANUAIS_POLI),
    "overleaf-ic": ("ic", "ufrj-ic.sty", D.MANUAIS_IC),
}
if sorted(D.OVERLEAF) != sorted(UNIDADES):
    problemas.append("os projetos do Overleaf sao %s; o teste conhece %s"
                     % (", ".join(sorted(D.OVERLEAF)), ", ".join(sorted(UNIDADES))))
for pac in sorted(UNIDADES):
    if pac not in D.PACOTES:
        problemas.append("%s: o pacote nao existe" % pac)
        continue
    unidade, estilo, manuais = UNIDADES[pac]
    over = D.PACOTES[pac]["arquivos"]
    na_raiz = set(n for sub, n, _ in over if not sub)
    for n in ["ufrj.cls", estilo, "ufrj.ist", "latexmkrc",
              "exemplo.bib", "README.md", "COPYING.txt"]:
        if n not in na_raiz:
            problemas.append("%s: falta %s na raiz do projeto" % (pac, n))
    na_pasta = set(n for sub, n, _ in over if sub == D.PASTA)
    for n in D.BIBLATEX + D.IDIOMAS:
        if n not in na_pasta:
            problemas.append("%s: falta %s em %s/" % (pac, n, D.PASTA))
    # Alem de coppetex/, so manuais/, que se le e de que nenhum documento depende.
    permitidas = {D.PASTA, D.PASTA + "/logos", "manuais"}
    subpastas = set(sub for sub, _, _ in over if sub)
    if subpastas - permitidas:
        problemas.append("%s: o projeto tem subpasta alem de %s/ e manuais/ (%s); "
                         "no Overleaf o aluno nao deve ter de mover arquivo"
                         % (pac, D.PASTA, ", ".join(sorted(subpastas - permitidas))))
    na_manuais = set(n for sub, n, _ in over if sub == "manuais")
    for n in manuais:
        if n not in na_manuais:
            problemas.append("%s: falta manuais/%s" % (pac, n))
    logos = [n for s, n, _ in over if s == D.PASTA + "/logos"]
    if "ufrj-logo.pdf" not in logos or len(logos) < 2:
        problemas.append("%s: faltam os logotipos em %s/logos/ (tem %s)"
                         % (pac, D.PASTA, ", ".join(logos) or "nenhum"))
    principais = sorted(n for _, n, _ in over if n.endswith(".tex"))
    esperados = ["%s-max-exemplo.tex" % unidade, "%s-min-exemplo.tex" % unidade]
    if principais != esperados:
        problemas.append("%s: o projeto devia ter o exemplo minimo e o maximo, "
                         "e tem %s" % (pac, ", ".join(principais) or "nenhum"))

# 4. O CTAN leva fonte, licenca e documentacao, e o TDS poe cada um no lugar.
ctan = set(n for _, n, _ in D.PACOTES["ctan"]["arquivos"])
for n in ("README.md", "COPYING.txt", "ufrj.dtx", "ufrj.ins",
          "ufrj-coppe.dtx", "ufrj-coppe.ins", "ufrj.pdf", "ufrj-coppe.pdf"):
    if n not in ctan:
        problemas.append("ctan: falta %s no pacote" % n)
ONDE = {".cls": "tex/latex/", ".sty": "tex/latex/", ".lbx": "tex/latex/",
        ".def": "tex/latex/", ".bbx": "tex/latex/", ".cbx": "tex/latex/",
        ".dbx": "tex/latex/", ".dtx": "source/latex/", ".ins": "source/latex/",
        ".ist": "makeindex/", ".bib": "bibtex/bib/", ".pdf": None}
for tdsdir, (_, nome, _) in D.TDS:
    esperado = ONDE.get(os.path.splitext(nome)[1])
    if esperado and not tdsdir.startswith(esperado):
        problemas.append("ctan: no TDS, %s esta em %s; o TDS poe esse tipo em %s"
                         % (nome, tdsdir, esperado))
if not any(t.startswith("doc/latex/") for t, _ in D.TDS):
    problemas.append("ctan: a arvore TDS nao tem doc/latex/")

# 5. Cada pacote so com a sua unidade. A marca de cada uma no nome do arquivo:
#    "coppetex" e o nome da pasta da classe, e nao da COPPE.
MARCA = {
    "coppe": re.compile(r"(^|[/-])coppe[-.]"),
    "poli": re.compile(r"poli"),
    "ic": re.compile(r"(^|[/-])(ic|ppgi)[-.]"),
}
DONO = {"ctan": "coppe", "overleaf-coppe": "coppe", "overleaf-poli": "poli",
        "overleaf-ic": "ic"}
for pacote, (sub, nome, (origem, caminho)) in entradas:
    dono = DONO.get(pacote.split(" ")[0])
    for unidade, marca in sorted(MARCA.items()):
        if unidade != dono and (marca.search(nome.lower())
                                or marca.search(caminho.lower())):
            problemas.append("%s: %s e de %s, e este pacote e de %s"
                             % (pacote, nome, unidade, dono))

# 6. O pacote nao e versionado, mas o que ele copia de src/ e da raiz TEM de
#    ser: numa copia limpa do repositorio, o que nao esta no git nao existe, e
#    a montagem pararia no meio na hora de enviar.
p = subprocess.run(["git", "ls-files"], cwd=RAIZ,
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if p.returncode != 0:
    print("aviso: git ls-files falhou; o item 6 nao foi conferido")
else:
    versionados = set(p.stdout.decode("utf-8", "replace").splitlines())
    for pacote, (sub, nome, (origem, caminho)) in entradas:
        if origem == "src" and "src/" + caminho not in versionados:
            problemas.append("%s: src/%s nao esta no git; numa copia limpa o "
                             "pacote nao se monta" % (pacote, caminho))
        if origem == "raiz" and caminho not in versionados:
            problemas.append("%s: %s nao esta no git" % (pacote, caminho))
    nobuild = [v for v in versionados if v.startswith("build/")]
    if nobuild:
        problemas.append("ha arquivo de build/ versionado: os pacotes de envio "
                         "ficam fora do git (%s)" % nobuild[0])

relatar(problemas)
