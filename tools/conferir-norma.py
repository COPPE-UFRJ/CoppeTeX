#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Confere PDFs gerados pela classe coppe contra o Manual UFRJ/SiBI 2026.

Le o PDF pronto e mede o que a norma fixa em centimetros e em ordem, que e o
que nenhuma compilacao bem-sucedida garante: uma tese compila perfeitamente com
a margem errada.

Precisa de python3, poppler (pdftotext, pdftoppm, pdfinfo) e pypdf. Roda em
qualquer sistema; no Windows, instale poppler e `pip install pypdf'.

    python3 tools/conferir-norma.py adversativa/adv_*.pdf
    python3 tools/conferir-norma.py src/example.pdf
"""
import sys, re, subprocess, os, tempfile, io

PT = 28.3464567          # pontos por centimetro
A4 = (595.276, 841.89)
MANCHA_CENTRO = 11.0     # (3 + 19) / 2, em cm
VIES = 0.02              # vies medido da regua de tinta, em cm

# O que a 3.1.2.1.6 exige no sumario, no idioma em que a classe grafa cada um.
POSTEXTUAIS = {"pt": ("REFER", "AP\u00caNDICE", "ANEXO"),
               "en": ("REFER", "APPENDIX", "ANNEX"),
               "es": ("REFER", "AP\u00c9NDICE", "ANEXO"),
               "fr": ("R\u00c9F\u00c9R", "ANNEXE"),
               "it": ("RIFERIMENTI", "APPENDICE", "ALLEGATO")}
APROVACAO = re.compile(r"APROVAD[AO] POR|APPROVED BY|APROBAD[AO] POR")


def opcoes_da_classe(pdf):
    """As opcoes de \documentclass do .tex que gerou este PDF, se estiver ao lado.

    Uma opcao muda o que a norma pede: `listasnosumario' devolve as listas
    pre-textuais ao sumario, e entao abrir na lista de figuras e o pedido, nao
    um defeito. Sem o .tex ao lado, a conferencia segue pelo padrao da classe.
    """
    base = os.path.splitext(pdf)[0]
    if base.endswith("_lua"): base = base[:-4]     # o gemeo LuaLaTeX
    try:
        fonte = io.open(base + ".tex", encoding="utf-8", errors="replace").read()
    except OSError:
        return []
    m = re.search(r"\\documentclass\[([^\]]*)\]", fonte)
    return [o.strip() for o in m.group(1).split(",")] if m else []

def texto_bbox(pdf):
    out = subprocess.run(["pdftotext", "-bbox", pdf, "-"], capture_output=True, text=True)
    paginas = re.split(r"<page ", out.stdout)[1:]
    res = []
    for p in paginas:
        ws = [(float(a), float(b), float(c), float(d), e) for a, b, c, d, e in
              re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', p)]
        res.append(ws)
    return res

def texto(pdf, p):
    return subprocess.run(["pdftotext", "-f", str(p), "-l", str(p), pdf, "-"],
                          capture_output=True, text=True).stdout

def tinta_folio(pdf, pagina, dpi=300):
    """Topo e borda direita do folio, em cm, medidos na tinta."""
    with tempfile.TemporaryDirectory() as d:
        base = os.path.join(d, "p")
        subprocess.run(["pdftoppm", "-gray", "-r", str(dpi), "-f", str(pagina),
                        "-l", str(pagina), "-singlefile", pdf, base],
                       capture_output=True)
        f = base + ".pgm"
        if not os.path.exists(f): return None
        data = open(f, "rb").read()
        m = re.match(rb"P5\s+(?:#[^\n]*\n)?\s*(\d+)\s+(\d+)\s+(\d+)\s", data)
        w, h = int(m.group(1)), int(m.group(2))
        px = data[m.end():]
        # o folio fica no canto superior EXTERNO: direita nas folhas impares,
        # esquerda nas pares quando o documento e twoside. Varre os dois.
        topo = esq = dir_ = None
        for row in range(int(h * 0.12)):
            b = row * w
            for col in range(w):
                if px[b + col] < 128:
                    if topo is None: topo = row
                    if esq is None or col < esq: esq = col
                    if dir_ is None or col > dir_: dir_ = col
        if topo is None: return None
        # a borda que conta e a mais proxima do folio
        d_dir, d_esq = (w - 1 - dir_) / dpi * 2.54, esq / dpi * 2.54
        return (topo / dpi * 2.54, min(d_dir, d_esq))

def confere(pdf):
    nome = os.path.basename(pdf)
    achados = []
    def erro(m): achados.append(("ERRO ", m))
    def ok(m):   achados.append(("ok   ", m))

    opts = opcoes_da_classe(pdf)
    info = subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout
    npag = int(re.search(r"^Pages:\s+(\d+)", info, re.M).group(1))
    if re.search(r"595\.\d+ x 841\.\d+", info): ok("A4 retrato (2.2a)")
    else: erro("nao e A4 retrato (2.2a)")

    bb = texto_bbox(pdf)

    # --- ordem pre-textual e primeira folha numerada -------------------------
    prim_num = None
    for i, ws in enumerate(bb, 1):
        alto = [w for w in ws if w[1] < 80 and re.fullmatch(r"\d+", w[4].strip())]
        if alto:
            prim_num = i
            break
    if prim_num is None:
        erro("nenhuma folha numerada")
    else:
        ok("numeracao comeca na folha %d, na parte textual (2.7)" % prim_num)
        for j in range(1, prim_num):
            alto = [w for w in bb[j-1] if w[1] < 80 and re.fullmatch(r"\d+", w[4].strip())]
            if alto:
                erro("folha %d, pre-textual, esta numerada (2.7)" % j)

    # --- folio: 2 cm dos dois lados -----------------------------------------
    if prim_num:
        med = tinta_folio(pdf, prim_num)
        if med is None:
            erro("nao consegui medir o folio na folha %d" % prim_num)
        else:
            t, r = med
            if abs(t - 2.0) <= VIES + 0.01: ok("folio a %.3f cm do topo (2.7)" % t)
            else: erro("folio a %.3f cm do topo, deveria ser 2 cm (2.7)" % t)
            if abs(r - 2.0) <= VIES + 0.01: ok("ultimo algarismo a %.3f cm da direita (2.7)" % r)
            else: erro("ultimo algarismo a %.3f cm da direita (2.7)" % r)

    # --- margem esquerda do corpo -------------------------------------------
    if prim_num:
        corpo = [w for w in bb[prim_num - 1] if w[1] > 100]
        if corpo:
            x0 = min(w[0] for w in corpo) / PT
            if abs(x0 - 3.0) < 0.05 or abs(x0 - 3.62) < 0.1:
                ok("margem esquerda em %.3f cm (2.3)" % x0)
            else:
                erro("margem esquerda em %.3f cm, deveria ser 3 cm (2.3)" % x0)

    # o texto de cada folha, lido uma vez so
    pags = [texto(pdf, i) for i in range(1, npag + 1)]

    # --- sumario -------------------------------------------------------------
    sumario, idioma = None, "pt"
    for i, ws in enumerate(bb, 1):
        t = " ".join(w[4] for w in ws[:3]).upper()
        # "ÍNDICE GENERAL" e o sumario espanhol; "ÍNDICE DE FIGURAS" e a lista de
        # figuras, que vem antes -- por isso o espanhol exige as duas palavras.
        for cabeca, lang in (("SUMÁRIO", "pt"), ("SUMARIO", "pt"), ("CONTENTS", "en"),
                             ("ÍNDICE GENERAL", "es"), ("INDICE GENERAL", "es"),
                             ("TABLE DES MATIÈRES", "fr"), ("TABLE DES MATIERES", "fr"),
                             ("INDICE", "it")):
            if t.startswith(cabeca):
                sumario, idioma = i, lang; break
        if sumario: break
    if sumario is None:
        erro("sem sumario")
    else:
        corpo_sum = pags[sumario - 1]
        prim = [l for l in corpo_sum.split("\n")[1:] if l.strip()]
        if "listasnosumario" in opts:
            ok("sumario abre nas listas pre-textuais, pedido por `listasnosumario'")
        elif prim and re.match(r"^\s*1([.\s]|$)", prim[0]):
            # Duas licencas na expressao. O ponto: o babel espanhol grafa
            # "1. INTRODUCCION", e o ponto e dele, nao da norma. O fim de
            # linha: desde que o indicativo e o titulo passaram a ficar em
            # colunas separadas (3.1.2.1.6), o vao entre os dois e largo o
            # bastante para o pdftotext quebrar a linha ali, e a primeira
            # linha do sumario vem a ser o indicativo sozinho.
            ok("sumario abre na primeira secao numerada (3.1.2.1.6)")
        else:
            erro("sumario abre com %r -- elementos pre-textuais nao entram (3.1.2.1.6)"
                 % (prim[0][:40] if prim else ""))
        todo = "".join(pags[sumario - 1:min(sumario + 3, npag)]).upper()

        def tem_secao(termo):
            """O documento tem mesmo essa parte pos-textual?

            A 3.1.2.1.6 manda listar no sumario os elementos pos-textuais que o
            trabalho tiver. Um demonstrativo de nove folhas sem apendice nao
            esta em falta por nao trazer 'APENDICE' no sumario -- so estaria se
            tivesse o apendice e o omitisse. A folha e reconhecida pelo titulo
            no alto: e assim que a classe compoe os pos-textuais.
            """
            for t in pags[sumario:]:
                for linha in t.split("\n")[:6]:
                    if linha.strip().upper().startswith(termo): return True
            return False

        for termo in POSTEXTUAIS[idioma]:
            if termo in todo: ok("sumario traz %s (3.1.2.1.6)" % termo)
            elif not tem_secao(termo): ok("sem %s -- nada a listar (3.1.2.1.6)" % termo)
            else: erro("sumario nao traz %s (3.1.2.1.6)" % termo)

    # --- titulos sem indicativo numerico: centralizados na mancha ------------
    for i, ws in enumerate(bb, 1):
        cand = [w for w in ws if w[1] > 90]
        if not cand: continue
        cand.sort(key=lambda t: t[1])
        y0 = cand[0][1]
        linha = [w for w in cand if abs(w[1] - y0) < 3]
        txt = " ".join(w[4] for w in linha).upper()
        if txt.startswith(("APÊNDICE", "APENDICE", "APÉNDICE", "ANEXO", "APPENDIX", "ANNEX")):
            c = (min(w[0] for w in linha) + max(w[2] for w in linha)) / 2 / PT
            if abs(c - MANCHA_CENTRO) < 0.35:
                ok("'%s' centralizado na mancha (2.6)" % txt[:22])
            else:
                erro("'%s' fora do centro da mancha, em %.2f cm (2.6)" % (txt[:22], c))

    # --- folha de aprovacao em uma folha so ---------------------------------
    for i, ws in enumerate(bb, 1):
        t = " ".join(w[4] for w in ws).upper()
        if APROVACAO.search(t):
            seg = " ".join(w[4] for w in bb[i]).upper() if i < len(bb) else ""
            if seg.startswith(("PROF", "DR", "D.SC")):
                erro("folha de aprovacao transbordou para a folha seguinte")
            else:
                ok("folha de aprovacao cabe em uma folha (3.1.2.1.3)")
            break

    # --- resumos: orientador, programa e palavras-chave ---------------------
    nres = 0
    for i in range(1, npag + 1):
        t = pags[i - 1]
        if re.search(r"(Resumo|Abstract|Resumen)\s+d[ao]|(Abstract of)", t[:200]):
            nres += 1
            if re.search(r"(Orientador|Advisor|Director)", t): pass
            else: erro("pagina de resumo %d sem orientador" % i)
            if re.search(r"(Palavras-chave|Keywords|Palabras clave|Mots-clés|Parole chiave)", t): pass
            else: erro("pagina de resumo %d sem palavras-chave (3.1.2.1.4)" % i)
    if nres: ok("%d pagina(s) de resumo, com orientador e palavras-chave" % nres)
    return nome, npag, achados

if __name__ == "__main__":
    alvos = sys.argv[1:]
    if not alvos:
        print(__doc__); sys.exit(2)
    total_erros = 0
    for pdf in alvos:
        nome, npag, achados = confere(pdf)
        erros = [a for a in achados if a[0].strip() == "ERRO"]
        total_erros += len(erros)
        print("\n=== %s (%d folhas) -- %d conferencia(s), %d erro(s)"
              % (nome, npag, len(achados), len(erros)))
        for tag, m in achados:
            if tag.strip() == "ERRO" or "-v" in os.environ.get("CONFERIR", ""):
                print("   %s %s" % (tag, m))
    print("\n=== TOTAL: %d erro(s) em %d arquivo(s) ===" % (total_erros, len(alvos)))
    sys.exit(1 if total_erros else 0)
