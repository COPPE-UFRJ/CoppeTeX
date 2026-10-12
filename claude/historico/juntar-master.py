# -*- coding: utf-8 -*-
"""Junta ao goufrj (CoppeTeX 5.0) o que o master (4.1) fez depois que o goufrj nasceu.

    python tools/juntar-master.py juntar origin/master
    python tools/juntar-master.py resolver
    (regerar: em src/, pdflatex ufrj.ins e pdflatex ufrj-coppe.ins)
    python tools/juntar-master.py testes
    python tools/juntar-master.py sobras
    python tools/juntar-master.py traduzir ARQUIVO... [--aplicar]

O passo a passo, com o porque de cada comando, esta em JUNTAR_MASTER_GOUFRJ.md,
na raiz. Roda na raiz de qualquer worktree do repositorio, num ramo que nao seja
o master.

Por que existe
--------------
O goufrj renomeou coppe -> ufrj e tirou da classe o que e da COPPE, que foi para
o ufrj-coppe.dtx. O master, enquanto isso, recebeu a conferencia contra o Manual
UFRJ/SiBI 2026 (issue #112): testes novos r33..r70 e r89, e correcoes no
coppe.dtx. Um `git merge` puro erra de tres jeitos, todos vistos numa simulacao:

1. O src/coppe.dtx e o dist/coppe.dtx eram identicos na base, e o git pareia o
   src/coppe.dtx do master com o dist/ufrj.dtx do goufrj. As correcoes vao parar,
   em silencio, na COPIA da dist, e o src/ufrj.dtx nao recebe nada. O `juntar`
   tira da dist as copias das fontes antes do merge (o painel --dist as poe de
   volta), e o pareamento passa a ser src com src.
2. Linha que o master mudou e o goufrj renomeou da conflito, e o lado do master
   traz os nomes da 4.1 (\\coppe@...). O `resolver` traduz os nomes da base e do
   master e refaz a comparacao de tres vias: conflito que so existia por causa
   do nome se resolve sozinho.
3. O que o master mudou num trecho que o goufrj levou para o ufrj-coppe.dtx (os
   exemplos) conflita com o trecho apagado. O `resolver` aplica essas mudancas,
   traduzidas e em pedacos pequenos, no ufrj-coppe.dtx, e diz o que nao achou.

Arquivos gerados e PDFs ficam com a versao do goufrj: saem de novo do .dtx.
"""
import difflib
import io
import os
import re
import subprocess
import sys

BASE = "b8103c7"   # o commit do master de onde o goufrj saiu

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(errors="replace")
    except (ValueError, OSError):
        pass


def git(*args, check=True):
    r = subprocess.run(["git"] + list(args), capture_output=True)
    saida = r.stdout.decode("utf-8", "replace")
    if check and r.returncode != 0:
        raise SystemExit("git %s falhou:\n%s%s" % (" ".join(args), saida,
                                                     r.stderr.decode("utf-8", "replace")))
    return saida


def git_ok(*args):
    return subprocess.run(["git"] + list(args), capture_output=True).returncode == 0


RAIZ = git("rev-parse", "--show-toplevel").strip()


def ler(rel):
    d = io.open(os.path.join(RAIZ, rel), "rb").read()
    return d.decode("utf-8").replace("\r\n", "\n"), b"\r\n" in d


def gravar(rel, texto, crlf):
    texto = texto.replace("\r\n", "\n")
    if crlf:
        texto = texto.replace("\n", "\r\n")
    io.open(os.path.join(RAIZ, rel), "wb").write(texto.encode("utf-8"))


# ---------------------------------------------------------------------------
# A traducao de nomes 4.1 -> 5.0. Sao as regras da troca de nome do goufrj
# (commit fc0eb20), com as duas correcoes que aquela troca precisou fazer a mao:
# {coppe} so vira {ufrj} quando e nome de CLASSE (a sigla \useacronym{coppe} e da
# unidade e fica), e "-coppe" nao mexe em "ufrj-coppe". Ficam: COPPE (a unidade),
# CoppeTeX (o projeto), coppe-logo, coppetex.bat e COPPE_SRC.
REGRAS = [
    (r"copperdefstring", "ufrjdefstring"),
    (r"coppedefunitstring", "ufrjdefunitstring"),
    (r"coppedeclare(unit|program|logos|norm)", r"ufrjdeclare\1"),
    (r"coppe(main|foreign|)string", r"ufrj\1string"),
    (r"usecoppelanguage", "useufrjlanguage"),
    (r"newcoppefloat", "newufrjfloat"),
    (r"coppetexfinalpage", "ufrjfinalpage"),
    (r"coppefinal(engine|texsystem|font|system|time|manual)", r"ufrjfinal\1"),
    (r"coppe-lang-", "ufrj-lang-"),
    (r"(?<!ufrj)(?<=[A-Za-z>])-coppe\b(?!-)", "-ufrj"),
    (r"coppe-numeric", "ufrj-numeric"),
    (r"coppe-quickref", "ufrj-quickref"),
    (r"coppe@", "ufrj@"),
    (r"@coppe", "@ufrj"),
    (r"__coppe_", "__ufrj_"),
    (r"(?<![\w-])coppe:(?=[A-Za-z])", "ufrj:"),
    (r"Coppe(?!TeX)(?=[A-Z])", "Ufrj"),
    (r"\bcoppe\.(cls|dtx|ins|ist|bbx|cbx|dbx|pdf|bib|ind|gls|idx|glo|log|aux|toc|out)\b", r"ufrj.\1"),
    (r"(\\(?:documentclass|LoadClass|LoadClassWithOptions|ProvidesClass|@ifclassloaded|PassOptionsToClass)"
     r"\s*(?:\[[^\]]*\])?\s*)\{coppe\}", r"\1{ufrj}"),
    (r"=coppe\b(?![-.])", "=ufrj"),
    (r"\bcoppe(scale|mscdeg|dscdeg|phddeg|tccdeg|filing|grant|degree|agencias|version|bib)\b", r"ufrj\1"),
    (r"coppeUC", "ufrjUC"),
    (r"\|coppe\|", "|ufrj|"),
    (r"tex/latex/coppe\b", "tex/latex/ufrj"),
    (r"coppe_make_", "ufrj_make_"),
    # O nome da classe nas mensagens, no estilo de pagina e na prosa.
    (r"(\\(?:Class|Package)(?:Error|Warning|WarningNoLine|Info|InfoNoLine))\{coppe\}", r"\1{ufrj}"),
    (r"(\\(?:fancypagestyle|pagestyle|thispagestyle))\{coppe\}", r"\1{ufrj}"),
    (r"(documentclass\s*(?:\[[^\]]*\])?\s*)\\\{coppe\\\}", r"\1\\{ufrj\\}"),
    (r"\\string\{coppe\\string\}", r"\\string{ufrj\\string}"),
    (r"([`'])coppe'", r"\1ufrj'"),
    (r"((?:[Cc]lasse|[Cc]lass)\s+(?:\\texttt\{|\\verb\||))coppe(?=[}|\s,.;:])", r"\1ufrj"),
    (r"\bcoppe(\s+(?:document\s+)?class)\b", r"ufrj\1"),
]
REGRAS = [(re.compile(p), s) for p, s in REGRAS]
RE_DOCCLASS = re.compile(r"(\\\\?documentclass\s*(?:\[[^\]]*\])?\s*)\{coppe\}")
RE_ARQ_CLASSE = re.compile(r"coppe\.(cls|bbx|cbx|dbx)|coppe-numeric")


def traduzir(texto):
    for rx, subst in REGRAS:
        texto = rx.sub(subst, texto)
    return texto


def escapar_strings_python(texto):
    r"""Numa string Python que nao e crua, "\coppe@x" e uma barra seguida de c --
    escape invalido, que o Python deixa passar. Traduzido, vira "\ufrj@x", e \u e
    escape Unicode: o arquivo nao compila mais. Antes de traduzir, a barra dessas
    strings passa a ser escrita escapada ("\\coppe@x"), que e o mesmo valor."""
    import tokenize
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(texto).readline))
    except (tokenize.TokenError, SyntaxError, IndentationError):
        return texto
    linhas = texto.split("\n")
    trocas = []
    for tok in tokens:
        if tok.type != tokenize.STRING:
            continue
        prefixo = re.match(r"^[A-Za-z]*", tok.string).group(0).lower()
        if "r" in prefixo:
            continue
        novo = re.sub(r"(?<!\\)\\(?=[Cc]oppe)", r"\\\\", tok.string)
        if novo != tok.string:
            trocas.append((tok.start, tok.end, novo))
    for (l1, c1), (l2, c2), novo in reversed(trocas):
        if l1 == l2:
            linha = linhas[l1 - 1]
            linhas[l1 - 1] = linha[:c1] + novo + linha[c2:]
        else:
            inicio = linhas[l1 - 1][:c1]
            fim = linhas[l2 - 1][c2:]
            linhas[l1 - 1:l2] = (inicio + novo + fim).split("\n")
    return "\n".join(linhas)


def traduzir_documento(rel, texto):
    """Traducao de um arquivo inteiro (teste, apoio, roteiro): os nomes, e
    \\documentclass{coppe} vira a forma da 5.0, com \\usepackage{ufrj-coppe} logo
    depois. Devolve o texto e a lista do que conferir a mao."""
    avisos = []
    saida = []
    if rel.endswith(".py"):
        texto = escapar_strings_python(texto)
    for linha in texto.split("\n"):
        if rel.endswith(".py") and RE_ARQ_CLASSE.search(linha):
            avisos.append("%s: cita arquivo da classe 4.1; a 5.0 compila com ufrj.cls, ufrj-coppe.sty "
                          "(e coppe.cls, se o teste usar a forma antiga): %s" % (rel, linha.strip()[:90]))
        m = RE_DOCCLASS.search(linha)
        if not m:
            saida.append(traduzir(linha))
            continue
        barra = "\\\\" if m.group(1).startswith("\\\\") else "\\"
        resto = linha[m.end():]
        nova = traduzir(linha[:m.start()]) + m.group(1) + "{ufrj}"
        if resto.strip() in ("", "%"):
            saida.append(nova + resto)
            saida.append(barra + "usepackage{ufrj-coppe}")
        elif resto.startswith("\\n"):
            saida.append(nova + "\\n" + barra + "usepackage{ufrj-coppe}" + traduzir(resto))
        else:
            saida.append(traduzir(linha))
            avisos.append("%s: \\documentclass{coppe} no meio da linha; acrescente "
                          "\\usepackage{ufrj-coppe} a mao: %s" % (rel, linha.strip()[:90]))
            continue
        if rel.endswith(".py"):
            avisos.append("%s: \\usepackage{ufrj-coppe} acrescentado dentro de uma string Python; "
                          "confira: %s" % (rel, linha.strip()[:90]))
    resultado = "\n".join(saida)
    if rel.endswith(".py"):
        try:
            compile(resultado, rel, "exec")
        except SyntaxError as e:
            avisos.append("%s: NAO COMPILA depois da traducao (linha %s: %s); corrija a mao"
                          % (rel, e.lineno, e.msg))
    return resultado, avisos


# ---------------------------------------------------------------------------
def cmd_juntar(ref):
    ramo = git("rev-parse", "--abbrev-ref", "HEAD").strip()
    if ramo == "master":
        raise SystemExit("rode num ramo da 5.0 (goufrj ou o de integracao), nunca no master")
    if git("status", "--porcelain", "--untracked-files=no").strip():
        raise SystemExit("ha mudancas nao commitadas; faca commit ou stash antes de juntar")
    copias = [c for c in ("dist/ufrj.dtx", "dist/ufrj.ins", "dist/ufrj-coppe.dtx", "dist/ufrj-coppe.ins")
              if os.path.exists(os.path.join(RAIZ, c))]
    if copias:
        git("rm", "-q", *copias)
        git("commit", "-q", "-m",
            "juntar: tira da dist as copias das fontes antes do merge\n\n"
            "O src/coppe.dtx e o dist/coppe.dtx eram identicos na base, e o git\n"
            "pareava o src/coppe.dtx do master com o dist/ufrj.dtx. Sem as copias, o\n"
            "pareamento e src com src. O painel --dist as poe de volta.")
        print("commit: tiradas da dist %s" % ", ".join(copias))
    r = subprocess.run(["git", "-c", "merge.conflictStyle=diff3", "-c", "merge.renameLimit=20000",
                        "merge", "--no-ff", "--no-commit", ref], capture_output=True)
    print(r.stdout.decode("utf-8", "replace").strip())
    print(r.stderr.decode("utf-8", "replace").strip())
    print("\nProximo passo: python tools/juntar-master.py resolver")
    return 0


# ---------------------------------------------------------------------------
def gerados():
    """Os nomes que o docstrip escreve, lidos dos dois .ins, e os da 4.1 que
    deixaram de existir."""
    nomes = {"latexmkrc"}
    for ins in ("src/ufrj.ins", "src/ufrj-coppe.ins"):
        if os.path.exists(os.path.join(RAIZ, ins)):
            nomes.update(re.findall(r"\\file\{([^}]+)\}", ler(ins)[0]))
    nomes.update(["coppe.bbx", "coppe.cbx", "coppe.dbx", "coppe.ist", "coppe.bib",
                  "coppe-numeric.bbx", "coppe-numeric.cbx", "coppe-quickref.tex",
                  "coppe-lang-spanish.def", "coppe-lang-french.def", "coppe-lang-italian.def",
                  "brazilian-coppe.lbx", "english-coppe.lbx", "spanish-coppe.lbx",
                  "french-coppe.lbx", "italian-coppe.lbx"])
    return nomes


RE_CONFLITO = re.compile(r"^<<<<<<< [^\n]*\n(.*?)^\|\|\|\|\|\|\| [^\n]*\n(.*?)^=======\n(.*?)^>>>>>>> [^\n]*\n",
                         re.M | re.S)


def mesmas_linhas(a, b):
    return [l.rstrip() for l in a.split("\n")] == [l.rstrip() for l in b.split("\n")]


def pedacos(antes, depois):
    """(pre, velho, novo, pos) para cada mudanca entre duas listas de linhas, com
    ate tres linhas de contexto de cada lado."""
    sm = difflib.SequenceMatcher(None, antes, depois, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag != "equal":
            yield antes[max(0, i1 - 3):i1], antes[i1:i2], depois[j1:j2], antes[i2:i2 + 3]


def trocar_unico(alvo, velho, novo):
    norm = [l.rstrip() for l in alvo]
    v = [l.rstrip() for l in velho]
    achados = [i for i in range(len(norm) - len(v) + 1) if norm[i:i + len(v)] == v]
    if len(achados) != 1:
        return None
    i = achados[0]
    return alvo[:i] + novo + alvo[i + len(v):]


def portar_para_estilo(base_t, theirs_t, relatorio):
    """Aplica no ufrj-coppe.dtx as mudancas de um trecho que o goufrj tirou do
    ufrj.dtx. Devolve True se todas entraram."""
    rel = "src/ufrj-coppe.dtx"
    texto, crlf = ler(rel)
    alvo = texto.split("\n")
    tudo = True
    for pre, velho, novo, pos in pedacos(base_t.split("\n"), theirs_t.split("\n")):
        feito = None
        for ctx in (3, 2, 1, 0):
            p = pre[len(pre) - ctx:] if ctx else []
            q = pos[:ctx]
            v = p + velho + q
            if not [l for l in v if l.strip()]:
                continue
            feito = trocar_unico(alvo, v, p + novo + q)
            if feito is not None:
                break
        if feito is None:
            tudo = False
            relatorio.append("  NAO ACHEI no %s este trecho; aplique a mao:\n%s\n%s" % (
                rel, "\n".join("    - " + l for l in pre + velho + pos),
                "\n".join("    + " + l for l in pre + novo + pos)))
        else:
            alvo = feito
    gravar(rel, "\n".join(alvo), crlf)
    return tudo


def cmd_resolver():
    conflitos = [l for l in git("diff", "--name-only", "--diff-filter=U").split("\n") if l]
    if not conflitos:
        print("nenhum arquivo em conflito")
        return 0
    nomes_gerados = gerados()
    relatorio = []
    pendentes = []
    estilo_mudou = False
    for rel in conflitos:
        nome = os.path.basename(rel)
        ours_existe = git_ok("cat-file", "-e", "HEAD:" + rel)
        if rel.startswith("dist/") or nome in nomes_gerados or rel.endswith(".pdf"):
            if ours_existe:
                git("checkout", "--ours", "--", rel)
                git("add", "--", rel)
                relatorio.append("gerado: fica o do goufrj, que sai de novo do .dtx: %s" % rel)
            else:
                git("rm", "-q", "--cached", "--", rel, check=False)
                if os.path.exists(os.path.join(RAIZ, rel)):
                    os.remove(os.path.join(RAIZ, rel))
                relatorio.append("gerado da 4.1 que a 5.0 nao tem: removido: %s" % rel)
            continue
        if not ours_existe or not os.path.exists(os.path.join(RAIZ, rel)):
            pendentes.append(rel)
            relatorio.append("PENDENTE, apagado de um dos lados: %s" % rel)
            continue
        git("checkout", "--conflict=diff3", "--", rel)
        texto, crlf = ler(rel)
        conta = {"traducao": 0, "estilo": 0, "mao": 0}

        def resolve(m):
            ours, base, theirs = m.group(1), m.group(2), m.group(3)
            base_t, theirs_t = traduzir(base), traduzir(theirs)
            if mesmas_linhas(ours, base_t):
                conta["traducao"] += 1
                return theirs_t
            if mesmas_linhas(theirs_t, base_t) or mesmas_linhas(ours, theirs_t):
                conta["traducao"] += 1
                return ours
            if not ours.strip() and rel == "src/ufrj.dtx":
                if portar_para_estilo(base_t.rstrip("\n"), theirs_t.rstrip("\n"), relatorio):
                    conta["estilo"] += 1
                    return ours
            conta["mao"] += 1
            return m.group(0)

        novo = RE_CONFLITO.sub(resolve, texto)
        estilo_mudou = estilo_mudou or conta["estilo"] > 0
        gravar(rel, novo, crlf)
        if conta["mao"] == 0 and "<<<<<<< " not in novo:
            git("add", "--", rel)
            relatorio.append("%s: %d conflito(s) resolvido(s) pela traducao dos nomes, %d levado(s) ao ufrj-coppe.dtx"
                             % (rel, conta["traducao"], conta["estilo"]))
        else:
            pendentes.append(rel)
            relatorio.append("PENDENTE %s: %d pela traducao, %d ao estilo, %d a mao (procure <<<<<<< no arquivo)"
                             % (rel, conta["traducao"], conta["estilo"], conta["mao"]))
    if estilo_mudou:
        git("add", "--", "src/ufrj-coppe.dtx")
    print("\n".join(relatorio))
    print("\n%d arquivo(s) pendente(s)%s" % (len(pendentes), (": " + ", ".join(pendentes)) if pendentes else "."))
    print("Depois: regere (em src/: pdflatex ufrj.ins; pdflatex ufrj-coppe.ins), e rode\n"
          "`python tools/juntar-master.py testes` e `python tools/juntar-master.py sobras`.")
    return 1 if pendentes else 0


# ---------------------------------------------------------------------------
def cmd_testes(ref):
    """Os testes que o master criou desde a base viram rt<numero>, com os nomes
    traduzidos; o README do regressivo ganha a secao deles."""
    if ref is None:
        ref = "MERGE_HEAD" if git_ok("rev-parse", "-q", "--verify", "MERGE_HEAD") else "origin/master"
    novos = [l for l in git("diff", "--name-only", "--diff-filter=A", BASE, ref, "--",
                            "tests/regressivo/").split("\n") if l]
    re_teste = re.compile(r"^tests/regressivo/r(\d+)-(.+\.(?:tex|py))$")
    numeros = {}
    for rel in novos:
        m = re_teste.match(rel)
        if m and os.path.exists(os.path.join(RAIZ, rel)):
            git("mv", rel, "tests/regressivo/rt%s-%s" % (m.group(1), m.group(2)))
            numeros[m.group(1)] = True
    apoio = [l for l in novos if not re_teste.match(l) and os.path.exists(os.path.join(RAIZ, l))
             and l.endswith((".py", ".tex", ".bib", ".sty", ".md"))]
    alvos = [l for l in git("ls-files", "tests/regressivo").split("\n")
             if re.match(r"tests/regressivo/rt\d+-", l)] + apoio
    for extra in ("CORRECOES_MANUAL_2026.md", "tests/regressivo/README.md"):
        if os.path.exists(os.path.join(RAIZ, extra)):
            alvos.append(extra)
    re_num = re.compile(r"(?<![\w-])r(%s)(?!\d)" % "|".join(sorted(numeros, key=len, reverse=True))) \
        if numeros else None
    avisos = []
    for rel in alvos:
        texto, crlf = ler(rel)
        novo = re_num.sub(lambda m: "rt" + m.group(1), texto) if re_num else texto
        if rel != "tests/regressivo/README.md":
            novo, av = traduzir_documento(rel, novo)
            avisos.extend(av)
        else:
            novo = mover_linhas_rt(novo)
        if novo != texto:
            gravar(rel, novo, crlf)
            git("add", "--", rel)
    print("%d teste(s) renomeado(s) de r para rt: %s" % (len(numeros), ", ".join(
        "rt" + n for n in sorted(numeros, key=int))))
    print("%d arquivo(s) de apoio traduzido(s): %s" % (len(apoio), ", ".join(apoio) or "-"))
    for a in avisos:
        print("  CONFERIR " + a)
    return 0


def mover_linhas_rt(texto):
    linhas = texto.split("\n")
    rt = [l for l in linhas if re.match(r"^\| `rt\d+-", l)]
    if not rt:
        return texto
    linhas = [l for l in linhas if not re.match(r"^\| `rt\d+-", l)]
    titulo = "### A conferência contra o Manual UFRJ/SiBI 2026 (`rt`)"
    bloco = [titulo, "",
             "Os testes da conferência de 16/09/2026 (issue #112). Cada um falha até a",
             "issue dele ser corrigida.", "",
             "| Arquivo | O defeito |", "|---|---|"] + rt + [""]
    alvo = next((i for i, l in enumerate(linhas) if l.startswith("### A classe da UFRJ e o estilo")), None)
    if alvo is None:
        alvo = next((i for i, l in enumerate(linhas) if l.startswith("### As ferramentas")), len(linhas))
    linhas[alvo:alvo] = bloco
    return "\n".join(linhas)


# ---------------------------------------------------------------------------
MODULOS_CODIGO = {"class", "bbx", "cbx", "dbx", "numbbx", "numcbx", "glossary",
                  "lbxbr", "lbxen", "lbxes", "lbxfr", "lbxit", "langes", "langfr", "langit"}
RE_41 = re.compile(r"coppe@|@coppe|newcoppefloat|(?<![\w-])coppe:[A-Za-z]|copperdefstring|coppe(main|foreign)?string|"
                   r"documentclass\s*(\[[^\]]*\])?\s*\{coppe\}|(?<![\w-])coppe\.(cls|dtx|bbx|cbx|dbx|ist)|"
                   r"(?<!ufrj)-coppe\.lbx|coppe-lang-|coppe-numeric")


def cmd_sobras():
    problemas = []
    for rel in git("ls-files").split("\n"):
        if not rel or rel.startswith(("LIXO/", "specs/")) or \
                rel.endswith((".pdf", ".png", ".jpg", ".eps", ".zip", ".xmpi", ".ico")):
            continue
        caminho = os.path.join(RAIZ, rel)
        if not os.path.isfile(caminho):
            continue
        try:
            linhas = io.open(caminho, encoding="utf-8").read().split("\n")
        except (UnicodeDecodeError, OSError):
            continue
        if any(l.startswith("<<<<<<< ") for l in linhas):
            problemas.extend("%s:%d marca de conflito" % (rel, n) for n, l in enumerate(linhas, 1)
                             if l.startswith(("<<<<<<< ", "||||||| ", ">>>>>>> ")) or l.rstrip("\r") == "=======")
    pilha = []
    for n, l in enumerate(ler("src/ufrj.dtx")[0].split("\n"), 1):
        for m in re.finditer(r"^%<([*/])([^>]+)>", l):
            if m.group(1) == "*":
                pilha.append(m.group(2))
            elif pilha:
                pilha.pop()
        if pilha and pilha[-1] in MODULOS_CODIGO and RE_41.search(l):
            onde = "num comentario" if l.lstrip().startswith("%") else "no codigo"
            problemas.append("src/ufrj.dtx:%d nome da 4.1 %s [%s]: %s" % (n, onde, pilha[-1], l.strip()[:100]))
    for rel in git("ls-files", "tests/regressivo").split("\n"):
        if re.match(r"tests/regressivo/rt\d+-", rel):
            for n, l in enumerate(ler(rel)[0].split("\n"), 1):
                if RE_41.search(l):
                    problemas.append("%s:%d nome da 4.1: %s" % (rel, n, l.strip()[:100]))
    print("\n".join(problemas) if problemas else "nenhuma sobra: sem marca de conflito e sem nome da 4.1 no codigo")
    return 1 if problemas else 0


def cmd_traduzir(arquivos, aplicar):
    for rel in arquivos:
        texto, crlf = ler(rel)
        novo, avisos = traduzir_documento(rel, texto)
        diff = list(difflib.unified_diff(texto.split("\n"), novo.split("\n"),
                                         rel, rel + " (5.0)", lineterm="", n=0))
        print("\n".join(diff) if diff else "%s: nada a traduzir" % rel)
        for a in avisos:
            print("  CONFERIR " + a)
        if aplicar and diff:
            gravar(rel, novo, crlf)
    return 0


def main():
    a = sys.argv[1:]
    if a[:1] == ["juntar"] and len(a) == 2:
        return cmd_juntar(a[1])
    if a[:1] == ["resolver"]:
        return cmd_resolver()
    if a[:1] == ["testes"]:
        return cmd_testes(a[1] if len(a) > 1 else None)
    if a[:1] == ["sobras"]:
        return cmd_sobras()
    if a[:1] == ["traduzir"] and len(a) > 1:
        return cmd_traduzir([x for x in a[1:] if x != "--aplicar"], "--aplicar" in a)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main() or 0)
