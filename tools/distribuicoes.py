# -*- coding: utf-8 -*-
"""Gera as distribuicoes da CoppeTeX a partir de src/.

    python tools/distribuicoes.py              regera build/, as normas e as tres dist-*
    python tools/distribuicoes.py --regerar    so prepara build/ e roda os tres .ins
    python tools/distribuicoes.py --normas     so converte as normas de src/normas
    python tools/distribuicoes.py --montar     so monta dist-coppe, dist-poli e dist-biblatex
    python tools/distribuicoes.py --pacote     fecha cada dist-* num .zip em build/pacotes
    python tools/distribuicoes.py --conferir   so diz o que falta em build/ para montar

O caminho inteiro, do .dtx ao que se baixa, e:

    src/  --(copia das fontes)-->  build/  --(.ins)-->  build/ com os gerados
          build/  --(compilacao: build-check.ps1 / coppetex.bat --docs)-->  PDFs
          build/ + src/distribuicao + src/normas  --(--montar)-->  dist-*/ e normas/

src/ so tem fonte. build/ e a pasta de trabalho: recebe uma copia das fontes,
os arquivos que os .ins geram e os PDFs que a compilacao produz, e fica fora do
git. As dist-* e normas/ sao versionadas: sao o que se baixa.

Este arquivo e o UNICO lugar que sabe o que vai em cada distribuicao. O painel
(coppetex.bat), o build-check.ps1, o versao.py e os testes r92/r93/rtu14 leem
as listas daqui.

Nao compila nada que precise de biber: isso continua com o build-check.ps1, que
e quem sabe o ciclo de cada documento. Aqui se roda so o docstrip (os .ins) e a
conversao das normas, de Word para PDF, pelo LibreOffice.
"""
from __future__ import print_function

import io
import os
import shutil
import subprocess
import sys
import zipfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(RAIZ, "src")
BUILD = os.path.join(RAIZ, "build")
NORMAS = os.path.join(RAIZ, "normas")

# ---------------------------------------------------------------------------
# Fontes: o que de src/ e copiado para build/ antes de rodar os .ins
# ---------------------------------------------------------------------------
FONTES = ["ufrj.dtx", "ufrj.ins", "ufrj-coppe.dtx", "ufrj-coppe.ins",
          "ufrj-poli.dtx", "ufrj-poli.ins", "manual.tex"]
PASTAS_FONTE = ["logos"]
INS = ["ufrj.ins", "ufrj-coppe.ins", "ufrj-poli.ins"]

# ---------------------------------------------------------------------------
# Blocos que se repetem entre as distribuicoes. A repeticao e de proposito:
# cada dist-* tem de bastar sozinha.
# ---------------------------------------------------------------------------
# O biblatex inteiro. O english-ufrj.lbx vai sempre: todo trabalho tem resumo
# em ingles, e o biblatex carrega o .lbx de cada idioma que o documento usa.
BIBLATEX = ["ufrj.dbx", "ufrj.bbx", "ufrj.cbx",
            "ufrj-numeric.bbx", "ufrj-numeric.cbx",
            "brazilian-ufrj.lbx", "english-ufrj.lbx"]
CLASSE = ["ufrj.cls", "ufrj.ist", "latexmkrc"]
ESPANHOL = ["spanish-ufrj.lbx", "ufrj-lang-spanish.def"]
OUTRAS = ["french-ufrj.lbx", "italian-ufrj.lbx",
          "ufrj-lang-french.def", "ufrj-lang-italian.def"]


def _b(nome, destino=""):
    """Um arquivo de build/ (gerado ou compilado)."""
    return (destino, nome, ("build", nome))


def _s(caminho, destino="", nome=None):
    """Um arquivo de src/ copiado como esta."""
    return (destino, nome or os.path.basename(caminho), ("src", caminho))


def _r(caminho, destino=""):
    """Um arquivo da raiz do repositorio."""
    return (destino, os.path.basename(caminho), ("raiz", caminho))


def _n(caminho, destino="norma"):
    """Um arquivo de normas/ (ja convertido por --normas)."""
    return (destino, os.path.basename(caminho), ("normas", caminho))


# Cada entrada: (subpasta dentro da dist, nome final, (origem, caminho)).
# O que esta na RAIZ de cada dist e o que funciona sem mexer em nada: o LaTeX
# procura classe, estilos e .lbx ao lado do documento, e nao em subpastas.
DISTRIBUICOES = {
    "dist-coppe": (
        [_s("distribuicao/coppe/README.md"), _r("COPYING.txt")]
        + [_b(n) for n in CLASSE + BIBLATEX]
        + [_b("ufrj-coppe.sty"), _b("coppe.cls"),
           _b("coppe-min-exemplo.tex"), _b("coppe-max-exemplo.tex"),
           _b("exemplo.bib")]
        + [_s("logos/coppe-logo.pdf", "logos"), _s("logos/coppe-logo.eps", "logos"),
           _s("logos/ufrj-logo.pdf", "logos")]
        + [_b(n, "manuais") for n in (
            "ufrj.pdf", "ufrj-coppe.pdf", "ufrj-quickref.pdf", "coppe-quickref.pdf",
            "manual.pdf", "coppe-min-exemplo.pdf", "coppe-max-exemplo.pdf")]
        + [_b("example_en.tex", "en"), _b("example_en.pdf", "en"),
           _b("example_es.tex", "es"), _b("example_es.pdf", "es")]
        + [_b(n, "es") for n in ESPANHOL]
        + [_b(n, "outraslinguas") for n in OUTRAS]
        + [_s("gerador/coppetex-novo.bat", "gerador"),
           _s("gerador/geradocvazio.py", "gerador")]
        + [_s("distribuicao/coppe/MIGRATION_v3_to_v4.md", "migracao"),
           _s("distribuicao/coppe/MIGRATION_v4_to_v5.md", "migracao")]
        + [_n("norma-coppe/NORMA_COPPE_2026.pdf")]
    ),
    "dist-poli": (
        [_s("distribuicao/poli/README.md"), _r("COPYING.txt")]
        + [_b(n) for n in CLASSE + BIBLATEX]
        + [_b("ufrj-poli.sty"), _b("poli.cls"),
           _b("poli-min-exemplo.tex"), _b("poli-max-exemplo.tex"),
           _b("exemplo.bib")]
        + [_s("logos/poli-logo.pdf", "logos"), _s("logos/ufrj-logo.pdf", "logos")]
        + [_b(n, "manuais") for n in (
            "ufrj.pdf", "ufrj-poli.pdf", "ufrj-quickref.pdf", "poli-quickref.pdf",
            "poli-min-exemplo.pdf", "poli-max-exemplo.pdf")]
        + [_b(n, "es") for n in ESPANHOL]
        + [_b(n, "outraslinguas") for n in OUTRAS]
        + [_n("norma-poli/NORMA_POLI_2026.pdf")]
    ),
    "dist-biblatex": (
        [_s("distribuicao/biblatex/README.md"), _r("COPYING.txt"),
         _s("distribuicao/biblatex/exemplo-biblatex.tex")]
        + [_b(n) for n in BIBLATEX]
        + [_b("exemplo.bib")]
        + [_b("spanish-ufrj.lbx"), _b("french-ufrj.lbx"), _b("italian-ufrj.lbx")]
    ),
}

# As normas: a fonte e o .docx em src/normas; em normas/ vao o .docx e o .pdf.
NORMAS_FONTE = [
    ("norma-coppe", "NORMA_COPPE_2026.docx"),
    ("norma-poli", "NORMA_POLI_2026.docx"),
]


# ---------------------------------------------------------------------------
def _diz(*a):
    print(*a)
    sys.stdout.flush()


def _origem(o):
    tipo, caminho = o
    base = {"build": BUILD, "src": SRC, "raiz": RAIZ, "normas": NORMAS}[tipo]
    return os.path.join(base, *caminho.split("/"))


def esperado(nome):
    """Os caminhos relativos ('/') que a dist `nome' tem de ter, e so eles."""
    return sorted(("%s/%s" % (sub, n)) if sub else n
                  for sub, n, _ in DISTRIBUICOES[nome])


def faltando(nome=None):
    """O que ainda nao existe para montar a dist (ou todas)."""
    nomes = [nome] if nome else sorted(DISTRIBUICOES)
    falta = []
    for d in nomes:
        for sub, n, o in DISTRIBUICOES[d]:
            if not os.path.exists(_origem(o)):
                falta.append("%s: %s (de %s/%s)" % (d, n, o[0], o[1]))
    return falta


# ---------------------------------------------------------------------------
def regerar(diz=_diz):
    """Copia as fontes de src/ para build/ e roda os tres .ins la dentro."""
    if not os.path.isdir(BUILD):
        os.makedirs(BUILD)
    for nome in FONTES:
        shutil.copy2(os.path.join(SRC, nome), os.path.join(BUILD, nome))
    for pasta in PASTAS_FONTE:
        destino = os.path.join(BUILD, pasta)
        if os.path.isdir(destino):
            shutil.rmtree(destino)
        shutil.copytree(os.path.join(SRC, pasta), destino)
    diz("fontes copiadas de src/ para build/")
    ok = True
    for ins in INS:
        diz("   pdflatex %s" % ins)
        r = subprocess.run(["pdflatex", "-interaction=nonstopmode", ins],
                           cwd=BUILD, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
        if r.returncode != 0:
            diz("   FALHOU %s -- veja build/%s" % (ins, ins.replace(".ins", ".log")))
            ok = False
    # O ufrj.ins escreve latexmkrc.tex (o docstrip so escreve com extensao);
    # o nome que o latexmk procura e latexmkrc.
    gerado = os.path.join(BUILD, "latexmkrc.tex")
    if os.path.exists(gerado):
        shutil.copy2(gerado, os.path.join(BUILD, "latexmkrc"))
    return ok


def _soffice():
    for nome in ("soffice", "soffice.exe", "libreoffice"):
        achado = shutil.which(nome)
        if achado:
            return achado
    for candidato in (r"C:\Program Files\LibreOffice\program\soffice.exe",
                      r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
                      "/Applications/LibreOffice.app/Contents/MacOS/soffice"):
        if os.path.exists(candidato):
            return candidato
    return None


def _word_para_pdf(docx, pdf, diz):
    """Word -> PDF: LibreOffice, ou o proprio Word no Windows."""
    soffice = _soffice()
    if soffice:
        r = subprocess.run([soffice, "--headless", "--convert-to", "pdf",
                            "--outdir", os.path.dirname(pdf), docx],
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return r.returncode == 0 and os.path.exists(pdf)
    if os.name == "nt":
        try:
            import win32com.client  # pywin32
            word = win32com.client.Dispatch("Word.Application")
            doc = word.Documents.Open(os.path.abspath(docx))
            doc.SaveAs(os.path.abspath(pdf), FileFormat=17)
            doc.Close()
            word.Quit()
            return os.path.exists(pdf)
        except Exception as e:                       # sem pywin32 ou sem Word
            diz("   Word nao converteu (%s)" % e)
    return False


def normas(diz=_diz):
    """src/normas/<norma>/<arquivo>.docx -> normas/<norma>/ o .docx e o .pdf."""
    ok = True
    for pasta, docx in NORMAS_FONTE:
        fonte = os.path.join(SRC, "normas", pasta, docx)
        destino = os.path.join(NORMAS, pasta)
        if not os.path.isdir(destino):
            os.makedirs(destino)
        shutil.copy2(fonte, os.path.join(destino, docx))
        pdf = os.path.join(destino, docx[:-5] + ".pdf")
        if _word_para_pdf(os.path.join(destino, docx), pdf, diz):
            diz("   normas/%s/%s (e o .pdf)" % (pasta, docx))
        elif os.path.exists(pdf) and os.path.getmtime(pdf) >= os.path.getmtime(fonte):
            diz("   normas/%s: sem LibreOffice nem Word; o PDF que ja estava e "
                "mais novo que o .docx e fica" % pasta)
        else:
            diz("   FALTOU normas/%s/%s -- instale o LibreOffice" %
                (pasta, os.path.basename(pdf)))
            ok = False
    leiame = os.path.join(SRC, "normas", "README.md")
    if os.path.exists(leiame):
        shutil.copy2(leiame, os.path.join(NORMAS, "README.md"))
    return ok


def montar(diz=_diz, nomes=None):
    """Recria cada dist-* do zero, com exatamente o que a lista manda."""
    nomes = nomes or sorted(DISTRIBUICOES)
    falta = []
    for d in nomes:
        falta += faltando(d)
    if falta:
        for f in falta:
            diz("   FALTOU  %s" % f)
        diz("nada foi montado: compile antes (coppetex.bat --docs) e rode de novo")
        return False
    for d in nomes:
        pasta = os.path.join(RAIZ, d)
        # Do zero: o que ja estava e saiu da lista nao pode ficar para o zip.
        # O .gitignore de cada dist e do repositorio e fica.
        if os.path.isdir(pasta):
            for item in os.listdir(pasta):
                if item == ".gitignore":
                    continue
                alvo = os.path.join(pasta, item)
                if os.path.isdir(alvo):
                    shutil.rmtree(alvo)
                else:
                    os.remove(alvo)
        else:
            os.makedirs(pasta)
        for sub, n, o in DISTRIBUICOES[d]:
            destino = os.path.join(pasta, sub) if sub else pasta
            if not os.path.isdir(destino):
                os.makedirs(destino)
            shutil.copy2(_origem(o), os.path.join(destino, n))
        diz("   %s: %d arquivo(s)" % (d, len(DISTRIBUICOES[d])))
    return True


def sobras(nome):
    """O que esta na dist e nao esta na lista (alem do .gitignore)."""
    pasta = os.path.join(RAIZ, nome)
    esp = set(esperado(nome))
    achado = []
    for raiz, pastas, arquivos in os.walk(pasta):
        for a in arquivos:
            rel = os.path.relpath(os.path.join(raiz, a), pasta).replace(os.sep, "/")
            if rel != ".gitignore" and rel not in esp:
                achado.append(rel)
    return sorted(achado)


def versao_atual():
    import re
    texto = io.open(os.path.join(SRC, "ufrj.dtx"), encoding="utf-8").read()
    m = re.search(r"\\def\\fileversion\{v?([^}]+)\}", texto)
    return m.group(1) if m else "x"


def pacote(diz=_diz):
    """Um .zip por distribuicao, em build/pacotes/, com uma pasta dentro."""
    versao = versao_atual()
    saida = os.path.join(BUILD, "pacotes")
    if not os.path.isdir(saida):
        os.makedirs(saida)
    ok = True
    for d in sorted(DISTRIBUICOES):
        if sobras(d):
            diz("   %s tem arquivo fora da lista -- rode --montar" % d)
            ok = False
            continue
        zipado = os.path.join(saida, "CoppeTeX-%s-%s.zip" % (d.replace("dist-", ""), versao))
        pasta = os.path.join(RAIZ, d)
        dentro = "CoppeTeX-%s-%s" % (d.replace("dist-", ""), versao)
        with zipfile.ZipFile(zipado, "w", zipfile.ZIP_DEFLATED) as z:
            for rel in esperado(d):
                z.write(os.path.join(pasta, *rel.split("/")), dentro + "/" + rel)
        diz("   %s" % os.path.relpath(zipado, RAIZ))
    return ok


def main(argv):
    if "--ajuda" in argv or "-h" in argv:
        print(__doc__)
        return 0
    passos = [a for a in argv if a.startswith("--")]
    if "--conferir" in passos:
        falta = faltando()
        for f in falta:
            print("FALTA  " + f)
        return 1 if falta else 0
    tudo = not passos
    ok = True
    if tudo or "--regerar" in passos:
        ok = regerar() and ok
    if tudo or "--normas" in passos:
        ok = normas() and ok
    if tudo or "--montar" in passos:
        ok = montar() and ok
    if "--pacote" in passos:
        ok = pacote() and ok
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
