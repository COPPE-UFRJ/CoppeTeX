# -*- coding: utf-8 -*-
"""Apoio aos testes de conformidade de tests/regressivo/ (rt33 em diante).

NAO e teste: o rodador so pega arquivos r<numero>-<apelido>, e este nome nao
casa. Existe porque os defeitos achados na conferencia contra o Manual UFRJ/SiBI
(9.a ed. rev., 2026) sao, na maioria, TIPOGRAFICOS -- italico, negrito, corpo,
posicao na folha -- e as cobrancas de texto do run-regressivo.py tiram acento,
caixa e largura de traco de proposito. Para cobrar tipografia e preciso ler o
PDF com a fonte e a posicao de cada pedaco de texto, e isso e o que este modulo
faz, com o que ja vem no MiKTeX e no TeX Live:

  * pdftohtml -xml   -> cada pedaco de texto com a FONTE (nome e corpo) e a posicao;
  * pdftotext -bbox  -> cada PALAVRA com a caixa exata, em pontos.

Unidades: tudo em pontos PostScript (1/72 pol.), origem no canto SUPERIOR
esquerdo da folha, como o pdftotext e o pdftohtml entregam.

Uso tipico:

    from medidas import Documento, cm
    with Documento(corpo=r"\\chapter{Um}Texto.") as d:
        for pal in d.palavras(9): ...
        for frag in d.fragmentos(9): ...
"""
import glob
import hashlib
import html
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unicodedata
import xml.etree.ElementTree as ET

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
# COPPE_SRC aponta para outra copia da classe -- serve para provar uma correcao
# numa pasta de rascunho antes de leva-la ao .dtx.
SRC = os.environ.get("COPPE_SRC") or os.path.join(RAIZ, "src")


# ---------------------------------------------------------------- cache -----
# Compilar e o que custa. Uma rodada completa do regressivo chama o motor perto
# de cem vezes, e em quase todas a classe e a MESMA: o que muda e o documento
# de dez linhas em volta. O cache guarda o resultado de cada compilacao pela
# chave do que ENTRA nela -- o .tex, a base, os arquivos ao lado, o motor, as
# passadas -- mais o hash dos arquivos GERADOS da classe. Mexeu no .dtx, so os
# documentos afetados voltam ao motor; nao mexeu, a segunda rodada nao chama o
# motor nenhuma vez (#154).
#
# A chave inclui os gerados da classe justamente para o cache nao mascarar uma
# mudanca: e o risco que a issue aponta, e e por isso que a chave nao e so a do
# .tex do teste.
CACHE = os.path.join(RAIZ, "_scratch", "cache-regressivo")
SEM_CACHE = bool(os.environ.get("COPPE_SEM_CACHE"))
# Sete dias: o bastante para uma semana de trabalho na mesma issue, e pouco o
# bastante para a pasta nao crescer sem fim.
CACHE_DIAS = 7
_HASH_CLASSE = None
_PODADO = False


def hash_da_classe():
    """O hash dos arquivos gerados da classe, calculado uma vez por processo."""
    global _HASH_CLASSE
    if _HASH_CLASSE is None:
        h = hashlib.sha256()
        alvos = []
        for padrao in ("*.cls", "*.sty", "*.bbx", "*.cbx", "*.dbx", "*.lbx",
                       "*.def", "*.ist", "*.bib"):
            alvos += glob.glob(os.path.join(SRC, padrao))
        alvos += glob.glob(os.path.join(SRC, "logos", "*.pdf"))
        for caminho in sorted(alvos):
            h.update(os.path.basename(caminho).encode("utf-8"))
            try:
                h.update(io.open(caminho, "rb").read())
            except OSError:
                h.update(b"?")
        _HASH_CLASSE = h.hexdigest()
    return _HASH_CLASSE


def chave_de_compilacao(partes, arquivos=None):
    """A chave do cache: o que entra na compilacao, e a classe."""
    h = hashlib.sha256()
    for parte in partes:
        h.update(("%s\0" % parte).encode("utf-8"))
    for nome in sorted(arquivos or {}):
        h.update(("%s\0" % nome).encode("utf-8"))
        h.update(("%s\0" % (arquivos[nome],)).encode("utf-8"))
    h.update(hash_da_classe().encode("ascii"))
    return h.hexdigest()[:32]


def _podar_cache():
    """Apaga o que passou de CACHE_DIAS. Roda uma vez por processo."""
    global _PODADO
    if _PODADO or not os.path.isdir(CACHE):
        _PODADO = True
        return
    _PODADO = True
    limite = time.time() - CACHE_DIAS * 86400
    for nome in os.listdir(CACHE):
        caminho = os.path.join(CACHE, nome)
        try:
            if os.path.isdir(caminho) and os.path.getmtime(caminho) < limite:
                shutil.rmtree(caminho, ignore_errors=True)
        except OSError:
            pass


def cache_ler(chave, destino, nome):
    """Copia o resultado guardado para a pasta de trabalho. Achou? True.

    Devolve tambem o codigo de saida da compilacao guardada, porque ha teste
    que espera FALHA: o cache tem de lembrar disso, e nao so do PDF.
    """
    if SEM_CACHE or not chave:
        return False, None
    pasta = os.path.join(CACHE, chave)
    marca = os.path.join(pasta, "retorno.txt")
    if not os.path.exists(marca):
        return False, None
    try:
        retorno = int(io.open(marca, encoding="utf-8").read().strip())
        for arquivo in os.listdir(pasta):
            if arquivo == "retorno.txt":
                continue
            shutil.copy2(os.path.join(pasta, arquivo), os.path.join(destino, arquivo))
    except (OSError, ValueError):
        return False, None
    # O cache vale por sete dias a contar do ultimo uso, e nao da criacao.
    try:
        os.utime(pasta, None)
    except OSError:
        pass
    return True, retorno


def cache_gravar(chave, origem, nome, retorno):
    """Guarda <nome>.* da pasta de trabalho, e o codigo de saida."""
    if SEM_CACHE or not chave:
        return
    _podar_cache()
    destino = os.path.join(CACHE, chave)
    try:
        os.makedirs(CACHE, exist_ok=True)
        # Pasta provisoria com nome unico: dois testes do mesmo grupo podem
        # gravar a mesma chave ao mesmo tempo, em paralelo.
        provisoria = tempfile.mkdtemp(prefix=chave + ".", dir=CACHE)
        for arquivo in os.listdir(origem):
            if arquivo.startswith(nome + "."):
                shutil.copy2(os.path.join(origem, arquivo),
                             os.path.join(provisoria, arquivo))
        io.open(os.path.join(provisoria, "retorno.txt"), "w",
                encoding="utf-8").write("%d\n" % retorno)
        if os.path.isdir(destino):
            # Outro processo chegou primeiro: o resultado e o mesmo, e o dele
            # serve.
            shutil.rmtree(provisoria, ignore_errors=True)
            return
        os.replace(provisoria, destino)
    except OSError:
        shutil.rmtree(provisoria, ignore_errors=True)


PT_POR_CM = 72.0 / 2.54


def cm(x):
    """Centimetros em pontos."""
    return x * PT_POR_CM


# A mancha da classe: margem esquerda 3 cm, direita 2 cm (2.3 do Manual).
MARGEM_ESQ = cm(3.0)
MARGEM_DIR = cm(19.0)          # x da borda direita da mancha
CENTRO_MANCHA = cm(11.0)       # (3 + 19) / 2
META_FOLHA = cm(29.7) / 2.0

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(errors="replace")
    except (ValueError, OSError):
        pass


PREAMBULO_PADRAO = r"""\title{Documento de prova}
\foreigntitle{Proof document}
\author{Nome}{Sobrenome}
\advisor{Primeiro}{Orientador}{D.Sc.}{UFRJ}
\examiner{Primeiro Examinador}{D.Sc.}{UFRJ}
\department{PESC}
\date{09}{2026}
\dataaprovacao{1 de setembro de 2026}
\keyword{regressao}
\foreignkeyword{regression}
"""

MODELO = r"""\documentclass[%(opcoes)s]{ufrj}
\usepackage{ufrj-coppe}
%(pacotes)s
%(preambulo)s
\begin{document}
\maketitle
\frontmatter
%(pre)s
\mainmatter
%(corpo)s
\end{document}
"""


class Pedaco(object):
    """Um pedaco de texto do pdftohtml: mesma linha, mesma fonte."""

    def __init__(self, texto, esq, topo, larg, alt, fonte, corpo):
        self.texto = texto
        self.esq = esq
        self.topo = topo
        self.larg = larg
        self.alt = alt
        self.dir = esq + larg
        self.fonte = fonte
        self.corpo = corpo

    @property
    def italico(self):
        f = self.fonte.lower()
        return "italic" in f or "oblique" in f or "slant" in f

    @property
    def negrito(self):
        f = self.fonte.lower()
        return "bold" in f or "demi" in f

    def __repr__(self):
        return "<%r esq=%.1f topo=%.1f corpo=%.1f fonte=%s>" % (
            self.texto, self.esq, self.topo, self.corpo, self.fonte)


class Palavra(object):
    """Uma palavra do pdftotext -bbox."""

    def __init__(self, texto, x0, y0, x1, y1):
        self.texto = texto
        self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1

    def __repr__(self):
        return "<%r x0=%.1f y0=%.1f x1=%.1f y1=%.1f>" % (
            self.texto, self.x0, self.y0, self.x1, self.y1)


def normaliza(s):
    """Mesma normalizacao do run-regressivo.py: sem acento, sem caixa, traco '-'."""
    s = s.replace("­", "").replace("‐", "-").replace("‑", "-")
    s = s.replace("–", "-").replace("—", "-").replace("−", "-")
    s = s.replace(" ", " ").replace("ﬁ", "fi").replace("ﬂ", "fl")
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s).strip().lower()


def compacta(s):
    """So junta espaco; preserva acento, caixa e o traco exato."""
    s = s.replace("­", "").replace(" ", " ")
    s = unicodedata.normalize("NFC", s)
    return re.sub(r"\s+", " ", s).strip()


class Documento(object):
    """Compila um documento numa pasta temporaria, com a classe de src/.

    tex        -- o documento inteiro; se omitido, monta-se pelo MODELO
    bib        -- conteudo de um .bib (gravado como prova.bib e ja carregado)
    arquivos   -- {nome: conteudo} gravados ao lado
    biber      -- roda o biber depois da primeira passada
    makeindex  -- roda o makeindex das listas da classe e do indice remissivo
    passadas   -- passadas do pdflatex depois do biber/makeindex (padrao 2)
    """

    def __init__(self, tex=None, opcoes="dsc", pacotes="", preambulo=None,
                 pre="", corpo="", bib=None, arquivos=None, biber=None,
                 makeindex=False, passadas=2, nome="prova", motor="pdflatex"):
        if preambulo is None:
            preambulo = PREAMBULO_PADRAO
        if bib is not None:
            pacotes = pacotes + "\n\\addbibresource{prova.bib}"
            if biber is None:
                biber = True
        if tex is None:
            tex = MODELO % {"opcoes": opcoes, "pacotes": pacotes,
                            "preambulo": preambulo, "pre": pre, "corpo": corpo}
        self.tex = tex
        self.bib = bib
        self.arquivos = arquivos or {}
        self.biber = bool(biber)
        self.makeindex = makeindex
        self.passadas = passadas
        self.nome = nome
        self.motor = motor
        self.pasta = None
        self._paginas_xml = {}
        self._palavras = {}

    # -- compilacao ---------------------------------------------------------
    def __enter__(self):
        self.pasta = tempfile.mkdtemp(prefix="coppe-conf-")
        self.compila()
        return self

    def __exit__(self, *exc):
        if os.environ.get("MANTER_PROVA"):
            print("pasta mantida: %s" % self.pasta)
        else:
            shutil.rmtree(self.pasta, ignore_errors=True)
        return False

    def _rodar(self, cmd):
        amb = dict(os.environ)
        for var in ("TEXINPUTS", "BIBINPUTS"):
            amb[var] = self.pasta + os.pathsep + SRC + os.pathsep + \
                os.path.join(SRC, "logos") + os.pathsep
        return subprocess.run(cmd, cwd=self.pasta, env=amb,
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def _chave(self):
        return chave_de_compilacao(
            [self.tex, self.bib or "", self.nome, self.motor, self.passadas,
             self.biber, self.makeindex], self.arquivos)

    def compila(self):
        io.open(os.path.join(self.pasta, self.nome + ".tex"), "w",
                encoding="utf-8").write(self.tex)
        if self.bib is not None:
            io.open(os.path.join(self.pasta, "prova.bib"), "w",
                    encoding="utf-8").write(self.bib)
        for nome, conteudo in self.arquivos.items():
            io.open(os.path.join(self.pasta, nome), "w",
                    encoding="utf-8").write(conteudo)
        tex = self.nome + ".tex"
        # O mesmo documento, com a mesma classe, ja foi compilado antes (#154).
        chave = self._chave()
        achou, retorno = cache_ler(chave, self.pasta, self.nome)
        if achou:
            self.doCache = True
            self.retorno = retorno
            self._paginas_xml = {}
            self._palavras = {}
            return
        self.doCache = False
        self.ultima = self._rodar([self.motor, "-interaction=nonstopmode", tex])
        if self.biber:
            self._rodar(["biber", self.nome])
        if self.makeindex:
            ist = os.path.join(SRC, "ufrj.ist")
            for ext, saida in (("abx", "lab"), ("syx", "los"),
                               ("sgx", "lsg"), ("gsx", "lgs")):
                if os.path.exists(os.path.join(self.pasta, self.nome + "." + ext)):
                    self._rodar(["makeindex", "-s", ist, "-o",
                                 self.nome + "." + saida, self.nome + "." + ext])
            if os.path.exists(os.path.join(self.pasta, self.nome + ".idx")):
                self._rodar(["makeindex", self.nome + ".idx"])
        for _ in range(self.passadas):
            self.ultima = self._rodar([self.motor, "-interaction=nonstopmode", tex])
        self.retorno = self.ultima.returncode
        cache_gravar(chave, self.pasta, self.nome, self.retorno)
        self._paginas_xml = {}
        self._palavras = {}

    @property
    def pdf(self):
        return os.path.join(self.pasta, self.nome + ".pdf")

    @property
    def ok(self):
        """O PDF saiu E a ultima passada nao registrou erro (linha "!" no .log).

        So o PDF nao basta: em nonstopmode o TeX segue depois de um erro e
        produz o PDF assim mesmo. Um \\titlespacing com "plus", que o calc nao
        entende, saiu assim -- "Missing number" no log e "plus .2" impresso na
        folha --, e o teste que media o espaco reprovou pela medida, sem dizer
        que o documento tinha erro.
        """
        return os.path.exists(self.pdf) and not self.erros_do_log(1)

    @property
    def log(self):
        f = os.path.join(self.pasta, self.nome + ".log")
        if not os.path.exists(f):
            return ""
        return io.open(f, encoding="utf-8", errors="replace").read()

    def erros_do_log(self, n=3):
        return [l for l in self.log.splitlines() if l.startswith("!")][:n]

    def auxiliar(self, ext):
        f = os.path.join(self.pasta, self.nome + "." + ext)
        if not os.path.exists(f):
            return None
        return io.open(f, encoding="utf-8", errors="replace").read()

    # -- leitura do PDF -----------------------------------------------------
    def n_paginas(self):
        p = subprocess.run(["pdfinfo", self.pdf], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
        m = re.search(r"Pages:\s+(\d+)", p.stdout.decode("utf-8", "replace"))
        return int(m.group(1)) if m else 0

    def texto(self, pagina=None):
        cmd = ["pdftotext", "-enc", "UTF-8"]
        if pagina:
            cmd += ["-f", str(pagina), "-l", str(pagina)]
        cmd += [self.pdf, "-"]
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return p.stdout.decode("utf-8", "replace")

    def texto_layout(self, pagina=None):
        cmd = ["pdftotext", "-enc", "UTF-8", "-layout"]
        if pagina:
            cmd += ["-f", str(pagina), "-l", str(pagina)]
        cmd += [self.pdf, "-"]
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return p.stdout.decode("utf-8", "replace")

    def pagina_com(self, trecho, depois_de=0):
        """Primeira folha (1-based), depois de `depois_de', cujo texto contem o trecho."""
        alvo = normaliza(trecho)
        for i in range(depois_de + 1, self.n_paginas() + 1):
            if alvo in normaliza(self.texto(i)):
                return i
        return None

    def paginas_com(self, trecho):
        alvo = normaliza(trecho)
        return [i for i in range(1, self.n_paginas() + 1)
                if alvo in normaliza(self.texto(i))]

    def fragmentos(self, pagina):
        """Pedacos de texto da folha, com fonte e posicao (pdftohtml -xml, zoom 2)."""
        if pagina in self._paginas_xml:
            return self._paginas_xml[pagina]
        base = os.path.join(self.pasta, "_xml%d" % pagina)
        subprocess.run(["pdftohtml", "-xml", "-i", "-q", "-zoom", "2",
                        "-fontfullname", "-f", str(pagina), "-l", str(pagina),
                        self.pdf, base], stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE)
        caminho = base + ".xml"
        saida = []
        if os.path.exists(caminho):
            bruto = io.open(caminho, encoding="utf-8", errors="replace").read()
            bruto = re.sub(r"<!DOCTYPE[^>]*>", "", bruto)
            raiz = ET.fromstring(bruto.encode("utf-8"))
            fontes = {}
            for pg in raiz.iter("page"):
                for fs in pg.iter("fontspec"):
                    fontes[fs.get("id")] = (fs.get("family", ""),
                                            float(fs.get("size", "0")) / 2.0)
                for t in pg.iter("text"):
                    fam, corpo = fontes.get(t.get("font"), ("", 0.0))
                    texto = "".join(t.itertext())
                    saida.append(Pedaco(texto,
                                        float(t.get("left")) / 2.0,
                                        float(t.get("top")) / 2.0,
                                        float(t.get("width")) / 2.0,
                                        float(t.get("height")) / 2.0,
                                        fam, corpo))
        self._paginas_xml[pagina] = saida
        return saida

    def palavras(self, pagina):
        """Palavras da folha com a caixa exata (pdftotext -bbox)."""
        if pagina in self._palavras:
            return self._palavras[pagina]
        p = subprocess.run(["pdftotext", "-bbox", "-f", str(pagina), "-l",
                            str(pagina), self.pdf, "-"], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
        bruto = p.stdout.decode("utf-8", "replace")
        saida = []
        for m in re.finditer(r'<word xMin="([\d.]+)" yMin="([\d.]+)" '
                             r'xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>', bruto):
            saida.append(Palavra(html.unescape(m.group(5)), float(m.group(1)),
                                 float(m.group(2)), float(m.group(3)),
                                 float(m.group(4))))
        if not saida and self.fragmentos(pagina):
            # A folha tem texto, e o -bbox nao devolveu palavra nenhuma: quase
            # sempre o pdftotext do PATH e o do Xpdf (o que vem com o Git), que
            # nao tem a opcao. Sem esta guarda, o teste de medida PASSA sem
            # medir nada -- e passa em falso.
            onde = shutil.which("pdftotext") or "pdftotext"
            raise SystemExit(
                "medidas: 'pdftotext -bbox' nao devolveu palavra nenhuma na folha %d.\n"
                "  pdftotext em uso: %s\n"
                "  O -bbox e do poppler; o pdftotext do Xpdf (o do Git) nao o tem.\n"
                "  Rode pelo PowerShell, ou ponha o poppler na frente do PATH."
                % (pagina, onde))
        self._palavras[pagina] = saida
        return saida

    def linhas(self, pagina, tolerancia=2.0):
        """Palavras agrupadas por linha (mesma base), de cima para baixo."""
        linhas = []
        for w in sorted(self.palavras(pagina), key=lambda w: (w.y1, w.x0)):
            for ln in linhas:
                if abs(ln[0].y1 - w.y1) <= tolerancia:
                    ln.append(w)
                    break
            else:
                linhas.append([w])
        for ln in linhas:
            ln.sort(key=lambda w: w.x0)
        linhas.sort(key=lambda ln: ln[0].y1)
        return linhas


def texto_da_linha(linha):
    return " ".join(w.texto for w in linha)


# SOBRENOME, / ENTIDADE. / ENTRADA pelo titulo (PALAVRA minuscula...), com ou sem
# rotulo numerico na frente
_INICIO_DE_ENTRADA = re.compile(
    r"^(\[\d+\]\s*|\d+\s+)?[A-ZÀ-Ý][A-ZÀ-Ý'\-]+(\s+[A-ZÀ-Ý][A-ZÀ-Ý'\-]+)*(,|\.|\s+[a-zà-ý])")


def entrada(texto, comeco):
    """A entrada da lista de referencias que comeca por `comeco', numa linha so.

    Vai da linha que comeca por `comeco' ate a linha anterior a proxima entrada
    (uma linha que comeca por SOBRENOME em caixa alta seguido de virgula ou
    ponto). Serve para mostrar, na falha, o que a classe compos.
    """
    linhas = texto.splitlines()
    saida = []
    dentro = False
    for l in linhas:
        s = l.strip()
        if not dentro:
            if normaliza(s).startswith(normaliza(comeco)) or \
                    re.sub(r"^(\[\d+\]\s*|\d+\s+)", "", s).upper().startswith(comeco.upper()):
                dentro = True
                saida.append(s)
            continue
        if not s or _INICIO_DE_ENTRADA.match(s):
            break
        saida.append(s)
    return re.sub(r"-\s+(?=[a-zà-ý])", "", " ".join(saida)) if saida else ""


def relatar(problemas):
    """Imprime os problemas e sai com 1 se houver algum."""
    for p in problemas:
        print(p)
    sys.exit(1 if problemas else 0)
