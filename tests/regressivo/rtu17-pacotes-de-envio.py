# -*- coding: utf-8 -*-
"""Teste de conformidade da CoppeTeX.

BUG: nao havia defeito antigo aqui -- este teste guarda os dois pacotes de ENVIO, o do CTAN e o do Overleaf, que nasceram em outubro de 2026. Os dois sao da COPPE so, saem em build/ e nao sao versionados: sao feitos na hora de enviar, e um arquivo que faltasse na lista so apareceria como erro de compilacao na maquina de quem recebeu.

Cobra-se, sem compilar nada:
  1. todo arquivo das duas listas ou e fonte de src/, ou esta na raiz, ou e
     gerado por um dos .ins -- nenhum nome que nao possa existir nunca;
  2. o projeto do Overleaf basta sozinho e tem a arrumacao da dist-coppe: na
     raiz a classe, o estilo da unidade, o ufrj.ist, o latexmkrc e a base; em
     coppetex/ os estilos de bibliografia, os .lbx e .def de TODO idioma e os
     logotipos, e nenhuma outra subpasta -- o aluno nao tem de mover arquivo
     nenhum, porque a classe poe coppetex/ no \\input@path;
  3. o projeto do Overleaf tem os dois exemplos, o minimo e o maximo, e nenhum
     outro documento principal;
  4. o pacote do CTAN leva o README e a licenca, as quatro fontes (.dtx e .ins)
     e os manuais, e a arvore TDS poe cada arquivo no lugar que o TDS manda;
  5. nenhum dos dois leva nada da Poli: sao da COPPE;
  6. nada dos dois esta versionado -- eles moram em build/, que o git ignora.
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

# 2. O Overleaf e plano e basta sozinho.
over = D.PACOTES["overleaf"]["arquivos"]
na_raiz = set(n for sub, n, _ in over if not sub)
for n in ["ufrj.cls", "ufrj-coppe.sty", "ufrj.ist", "latexmkrc",
          "exemplo.bib", "README.md", "COPYING.txt"]:
    if n not in na_raiz:
        problemas.append("overleaf: falta %s na raiz do projeto" % n)
na_pasta = set(n for sub, n, _ in over if sub == D.PASTA)
for n in D.BIBLATEX + D.IDIOMAS:
    if n not in na_pasta:
        problemas.append("overleaf: falta %s em %s/" % (n, D.PASTA))
subpastas = set(sub for sub, _, _ in over if sub)
if subpastas - {D.PASTA, D.PASTA + "/logos"}:
    problemas.append("overleaf: o projeto tem subpasta alem de %s/ (%s); "
                     "no Overleaf o aluno nao deve ter de mover arquivo"
                     % (D.PASTA, ", ".join(sorted(subpastas - {D.PASTA, D.PASTA + "/logos"}))))
if not any(n.endswith("logo.pdf") for s, n, _ in over if s == D.PASTA + "/logos"):
    problemas.append("overleaf: faltam os logotipos em %s/logos/" % D.PASTA)

# 3. Os dois exemplos, e nenhum outro documento principal.
principais = sorted(n for _, n, _ in over if n.endswith(".tex"))
if principais != ["coppe-max-exemplo.tex", "coppe-min-exemplo.tex"]:
    problemas.append("overleaf: o projeto devia ter o exemplo minimo e o maximo, "
                     "e tem %s" % (", ".join(principais) or "nenhum"))

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

# 5. Nada da Poli nos dois: sao da COPPE.
for pacote, (sub, nome, (origem, caminho)) in entradas:
    if "poli" in nome.lower() or "poli" in caminho.lower():
        problemas.append("%s: %s e da Poli, e estes pacotes sao da COPPE" % (pacote, nome))

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
