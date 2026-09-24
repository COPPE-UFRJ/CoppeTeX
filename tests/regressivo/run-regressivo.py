# -*- coding: utf-8 -*-
"""Suite de regressao da CoppeTeX: um teste minimo para cada defeito ja corrigido.

    python tests/regressivo/run-regressivo.py
    python tests/regressivo/run-regressivo.py r04
    python tests/regressivo/run-regressivo.py --manter
    python tests/regressivo/run-regressivo.py --tarefas 1   (um de cada vez)
    python tests/regressivo/run-regressivo.py --sem-cache   (recompila tudo)

Compilar e o que custa: sao quase cem chamadas do motor numa rodada completa,
e em quase todas a classe e a mesma. Duas coisas cortam esse custo, e nenhuma
delas muda o que um teste cobra (#154):

  - CACHE. O resultado de cada compilacao fica em _scratch/cache-regressivo,
    com a chave do que entra nela -- o documento, a base, o motor, as passadas
    -- mais o hash dos arquivos GERADOS da classe. Mexeu no .dtx, so os
    documentos afetados voltam ao motor; nao mexeu, a segunda rodada nao chama
    o motor nenhuma vez. `--sem-cache' desliga, e a linha do teste diz
    "(cache)" quando o resultado veio de la.
  - PARALELISMO. Um processo do motor por teste, ate o numero de nucleos.
    `--tarefas <n>' escolhe quantos; `--tarefas 1' volta ao de antes, que e o
    que se quer quando se esta olhando uma falha.

NAO roda na suite normal. A primeira camada (tests/*.tex) pergunta "a classe
compila?"; esta pergunta "aquele defeito voltou?", e cada arquivo aqui e a menor
reproducao possivel de UM defeito que ja aconteceu de verdade. Rode antes de
marcar uma versao, ou quando mexer na parte da classe que o teste cobre.

A diferenca para a primeira camada nao e so o que se testa, e o que se cobra:
la o veredito e o codigo de saida do pdflatex; aqui cada arquivo declara, no
proprio cabecalho, o que tem de aparecer e o que NAO pode aparecer no PDF, no
log ou nos arquivos auxiliares. Um teste que compila e sai errado FALHA.

Diretivas aceitas no cabecalho do .tex (uma por linha, comecando com %%):

    %% BUG: <uma linha dizendo qual defeito este arquivo cobre>
    %% MOTOR: pdflatex | lualatex          (padrao: pdflatex)
    %% PASSADAS: <n>                       (padrao: 2)
    %% BIBER: sim                          (roda o biber entre as passadas)
    %% MAKEINDEX: sim                      (roda o makeindex das listas)
    %% ESPERA-FALHA: sim                   (a compilacao TEM de falhar)
    %% ESPERA-TEXTO: <texto>               (tem de sair no PDF)
    %% NAO-ESPERA-TEXTO: <texto>           (nao pode sair no PDF)
    %% ESPERA-TEXTO-PAGINA: <n>::<texto>   (tem de sair NAQUELA folha)
    %% NAO-ESPERA-TEXTO-PAGINA: <n>::<texto>
    %% ESPERA-LOG: <texto>                 (tem de estar no .log)
    %% NAO-ESPERA-LOG: <texto>             (nao pode estar no .log)
    %% ESPERA-PAGINAS: <n>                 (o PDF tem exatamente n folhas)
    %% ESPERA-ARQUIVO: <ext>::<texto>      (o .<ext> gerado contem o texto)
    %% NAO-ESPERA-ARQUIVO: <ext>::<texto>  (o .<ext> gerado NAO contem)
    %% ESPERA-BYTES: <texto>               (os bytes crus do PDF contem)
    %% ABERTO: #<issue>                    (defeito ainda aberto; ver abaixo)

ABERTO marca um teste que MOSTRA um defeito que ainda nao foi corrigido -- os da
conferencia contra o Manual 2026 (r33 em diante) nasceram assim. Ele falha, e
de proposito. Na rodada sem filtro ele NAO roda: a suite normal continua
dizendo se algum defeito CORRIGIDO voltou, e nao se enche de falhas conhecidas
nem do tempo delas. Rode-o pelo nome (`run-regressivo.py r38`), aos poucos,
enquanto a correcao e feita; a correcao tira a linha ABERTO no mesmo commit, e
dali em diante o teste entra na rodada normal. Nos .py a marca e uma linha
`ABERTO: #<issue>` no docstring, logo depois da linha BUG.

O texto do PDF sai do pdftotext, que vem com o MiKTeX e com o TeX Live. Sem ele
as cobrancas de texto sao PULADAS, e o teste avisa -- nao passa calado.

As cobrancas de texto comparam SEM acento, SEM maiuscula e com o espaco em
branco reduzido a um espaco. Nao e desleixo: e que a mesma frase sai com quebra
de linha num PDF e com espaco em outro, o travessao vira '-' ou '--' conforme a
fonte, e o pdftotext do Xpdf e o do poppler discordam nos dois. Cobrar o
conteudo, e nao a tipografia, e o que faz o teste falhar so quando o defeito
volta. Quem precisar cobrar caixa alta cobra pelo .log ou por um arquivo
auxiliar, onde o texto esta como o LaTeX o escreveu.
"""
import concurrent.futures
import io
import os
import re
import shutil
import subprocess
import sys
import unicodedata

# O cache mora no medidas.py, que e o outro lugar que compila -- os testes .py
# de medida --, para que a chave seja a mesma nos dois.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from medidas import cache_gravar, cache_ler, chave_de_compilacao  # noqa: E402

# O console do Windows e cp1252, e as cobrancas que este rodador imprime saem
# do texto do PDF, que tem acento, travessao e aspas tipograficas. Sem isto o
# rodador morre ao IMPRIMIR a falha que acabou de achar.
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(errors="replace")
    except (ValueError, OSError):
        pass

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
SRC = os.path.join(RAIZ, "src")

DIRETIVA = re.compile(r"^%%\s*([A-Z-]+):\s*(.*?)\s*$")
# <prefixo><numero>-<apelido>.tex ou .py. Ver o comentario em main(). Os
# prefixos dizem de onde o teste veio: r, os defeitos da classe ate a 4.1; rt, os
# da conferencia contra o Manual UFRJ/SiBI 2026 (issue #112), feita no master;
# rtu, os da classe ufrj e do estilo de unidade, da 5.0.
RE_NOME = re.compile(r"^r(?:tu?)?\d+-.*\.(tex|py)$")


def ler_diretivas(caminho):
    d = {"ESPERA-TEXTO": [], "NAO-ESPERA-TEXTO": [], "ESPERA-LOG": [],
         "NAO-ESPERA-LOG": [], "ESPERA-ARQUIVO": [], "NAO-ESPERA-ARQUIVO": [],
         "ESPERA-BYTES": [], "ESPERA-TEXTO-PAGINA": [],
         "NAO-ESPERA-TEXTO-PAGINA": []}
    for linha in io.open(caminho, encoding="utf-8").read().splitlines():
        if linha.startswith("\\documentclass"):
            break
        m = DIRETIVA.match(linha)
        if not m:
            continue
        chave, valor = m.group(1), m.group(2)
        if chave in d and isinstance(d[chave], list):
            d[chave].append(valor)
        else:
            d[chave] = valor
    return d


def rodar(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT)


def texto_do_pdf(pdf, primeira=None, ultima=None):
    cmd = ["pdftotext", "-enc", "UTF-8"]
    if primeira:
        cmd += ["-f", str(primeira), "-l", str(ultima or primeira)]
    cmd += [pdf, "-"]
    try:
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError:
        return None
    if p.returncode != 0:
        return None
    return p.stdout.decode("utf-8", "replace")


def paginas_do_pdf(pdf):
    try:
        p = subprocess.run(["pdfinfo", pdf], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    except OSError:
        return None
    if p.returncode != 0:
        return None
    m = re.search(r"Pages:\s+(\d+)", p.stdout.decode("utf-8", "replace"))
    return int(m.group(1)) if m else None


def normaliza(s):
    """Reduz o texto ao conteudo: sem acento, sem caixa, sem tipografia.

    Traco de qualquer largura vira '-', ligadura vira as letras, hifen de
    separacao some, espaco de qualquer tipo vira um espaco so, e o acento sai
    pela decomposicao Unicode. O que sobra e o que o teste cobra.
    """
    s = s.replace("­", "").replace("‐", "-").replace("‑", "-")
    s = s.replace("–", "-").replace("—", "-").replace("−", "-")
    s = s.replace(" ", " ").replace("ﬁ", "fi").replace("ﬂ", "fl")
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s).strip().lower()


class _Retorno(object):
    """O que sobrou de uma compilacao que veio do cache: o codigo de saida."""

    def __init__(self, returncode):
        self.returncode = returncode


def um_teste(tex, manter):
    nome = os.path.splitext(os.path.basename(tex))[0]
    d = ler_diretivas(tex)
    motor = d.get("MOTOR", "pdflatex")
    passadas = int(d.get("PASSADAS", "2"))
    falhas = []
    pulados = []

    def compilar():
        return rodar([motor, "-interaction=nonstopmode", os.path.basename(tex)],
                     AQUI)

    # O mesmo documento, com a mesma classe, ja compilado antes (#154). A chave
    # leva o texto do teste e os gerados da classe: o cache nao sobrevive a uma
    # mudanca no .dtx.
    fonte = io.open(tex, encoding="utf-8").read()
    chave = chave_de_compilacao([fonte, motor, passadas, d.get("BIBER", ""),
                                 d.get("MAKEINDEX", "")])
    achou, retorno = cache_ler(chave, AQUI, nome)
    if achou:
        p = _Retorno(retorno)
    else:
        p = compilar()
        if d.get("BIBER", "").lower() in ("sim", "yes", "1"):
            rodar(["biber", nome], AQUI)
        if d.get("MAKEINDEX", "").lower() in ("sim", "yes", "1"):
            ist = os.path.join(SRC, "ufrj.ist")
            for ext, saida in (("abx", "lab"), ("syx", "los"), ("sgx", "lsg"), ("gsx", "lgs")):
                if os.path.exists(os.path.join(AQUI, nome + "." + ext)):
                    rodar(["makeindex", "-s", ist, "-o", nome + "." + saida,
                           nome + "." + ext], AQUI)
        for _ in range(passadas - 1):
            p = compilar()
        cache_gravar(chave, AQUI, nome, p.returncode)

    log = os.path.join(AQUI, nome + ".log")
    texto_log = ""
    if os.path.exists(log):
        texto_log = io.open(log, encoding="utf-8", errors="replace").read()

    esperava_falha = d.get("ESPERA-FALHA", "").lower() in ("sim", "yes", "1")
    if esperava_falha:
        if p.returncode == 0:
            falhas.append("compilou, e o esperado era falhar")
    elif p.returncode != 0:
        erros = [l for l in texto_log.splitlines() if l.startswith("!")][:2]
        falhas.append("nao compilou (exit %d) %s" % (p.returncode, "; ".join(erros)))

    pdf = os.path.join(AQUI, nome + ".pdf")
    texto = None
    if os.path.exists(pdf) and (d["ESPERA-TEXTO"] or d["NAO-ESPERA-TEXTO"]):
        texto = texto_do_pdf(pdf)
        if texto is None:
            pulados.append("pdftotext nao disponivel: cobrancas de texto puladas")
    if texto is not None:
        alvo = normaliza(texto)
        for esperado in d["ESPERA-TEXTO"]:
            if normaliza(esperado) not in alvo:
                falhas.append("faltou no PDF: %s" % esperado)
        for proibido in d["NAO-ESPERA-TEXTO"]:
            if normaliza(proibido) in alvo:
                falhas.append("apareceu no PDF e nao devia: %s" % proibido)

    for item in d["ESPERA-TEXTO-PAGINA"]:
        num, _, esperado = item.partition("::")
        t = texto_do_pdf(pdf, int(num)) if os.path.exists(pdf) else None
        if t is None:
            pulados.append("pdftotext nao disponivel: folha %s pulada" % num)
        elif normaliza(esperado) not in normaliza(t):
            falhas.append("faltou na folha %s: %s" % (num, esperado))

    for item in d["NAO-ESPERA-TEXTO-PAGINA"]:
        num, _, proibido = item.partition("::")
        t = texto_do_pdf(pdf, int(num)) if os.path.exists(pdf) else None
        if t is None:
            pulados.append("pdftotext nao disponivel: folha %s pulada" % num)
        elif normaliza(proibido) in normaliza(t):
            falhas.append("apareceu na folha %s e nao devia: %s" % (num, proibido))

    for esperado in d["ESPERA-LOG"]:
        if esperado not in texto_log:
            falhas.append("faltou no log: %s" % esperado)
    for proibido in d["NAO-ESPERA-LOG"]:
        if proibido in texto_log:
            falhas.append("apareceu no log e nao devia: %s" % proibido)

    if "ESPERA-PAGINAS" in d and os.path.exists(pdf):
        n = paginas_do_pdf(pdf)
        if n is None:
            pulados.append("pdfinfo nao disponivel: contagem de folhas pulada")
        elif n != int(d["ESPERA-PAGINAS"]):
            falhas.append("o PDF tem %d folha(s) e devia ter %s" % (n, d["ESPERA-PAGINAS"]))

    for item in d["ESPERA-ARQUIVO"]:
        ext, _, esperado = item.partition("::")
        caminho = os.path.join(AQUI, nome + "." + ext.lstrip("."))
        if not os.path.exists(caminho):
            falhas.append("nao saiu o arquivo .%s" % ext)
        else:
            conteudo = io.open(caminho, encoding="utf-8", errors="replace").read()
            if esperado not in conteudo:
                falhas.append("faltou no .%s: %s" % (ext, esperado))

    for item in d["NAO-ESPERA-ARQUIVO"]:
        ext, _, proibido = item.partition("::")
        caminho = os.path.join(AQUI, nome + "." + ext.lstrip("."))
        if not os.path.exists(caminho):
            falhas.append("nao saiu o arquivo .%s" % ext)
        else:
            conteudo = io.open(caminho, encoding="utf-8", errors="replace").read()
            if proibido in conteudo:
                falhas.append("apareceu no .%s e nao devia: %s" % (ext, proibido))

    for esperado in d["ESPERA-BYTES"]:
        if not os.path.exists(pdf):
            falhas.append("nao saiu o PDF para conferir os bytes")
        else:
            crus = io.open(pdf, "rb").read()
            if esperado.encode("latin-1") not in crus:
                falhas.append("faltou nos bytes do PDF: %s" % esperado)

    if not manter:
        limpar(nome)
    return d.get("BUG", "(sem descricao)"), falhas, pulados, achou


# O PDF fica, porque e ele que se olha quando um teste falha; o resto sai. Os
# .pdf daqui NAO vao para o git: ver o .gitignore de tests/.
RESTOS = ("aux bbl bcf blg idx ilg ind lab lof log lol loq lot los mw out "
          "run.xml syx abx sgx lsg gsx lgs toc xmpdata glo gls").split()


def limpar(nome):
    for ext in RESTOS:
        f = os.path.join(AQUI, nome + "." + ext)
        if os.path.exists(f):
            try:
                os.remove(f)
            except OSError:
                pass


def um_teste_python(caminho):
    """Um defeito que nao esta na classe, e sim na ferramenta que a confere.

    Vale teste igual: um verificador que aprova tudo e pior que verificador
    nenhum, porque parece que alguem conferiu. O arquivo .py roda sozinho e
    passa quando sai com zero; a primeira linha do docstring que comeca por
    "BUG:" e a descricao.
    """
    bug = "(sem descricao)"
    for linha in io.open(caminho, encoding="utf-8").read().splitlines()[:20]:
        if linha.strip().startswith("BUG:"):
            bug = linha.strip()[4:].strip()
            break
    p = rodar([sys.executable, caminho], AQUI)
    if p.returncode == 0:
        return bug, [], [], False
    saida = p.stdout.decode("utf-8", "replace").strip().splitlines()
    return bug, ["saiu com codigo %d" % p.returncode] + saida[-6:], [], False


def aberto(caminho):
    """A issue de um teste que ainda mostra defeito aberto (marca ABERTO), ou None."""
    with io.open(caminho, encoding="utf-8") as f:
        for i, linha in enumerate(f):
            if i > 40 or linha.startswith("\\documentclass"):
                break
            m = re.match(r"^(?:%%\s*)?ABERTO:\s*(.*?)\s*$", linha)
            if m:
                return m.group(1) or "?"
    return None


def conferir_ferramentas():
    """As ferramentas que os testes usam para ler o PDF, conferidas uma vez.

    O -bbox e do poppler. O pdftotext do Xpdf -- o que vem com o Git for
    Windows -- nao o tem, e quando ele esta na frente do PATH os testes de
    medida recebem lista vazia e passam SEM MEDIR NADA (#156). Aqui isso vira
    uma linha no cabecalho da rodada, e nao um `ok' mentiroso trinta vezes."""
    linhas = []
    problema = False
    for nome, args, marca in (("pdftotext", ["-v"], "poppler"),
                              ("pdftohtml", ["-v"], "poppler"),
                              ("pdfinfo", ["-v"], "poppler")):
        caminho = shutil.which(nome)
        if caminho is None:
            linhas.append("%-10s NAO ACHEI no PATH" % nome)
            problema = True
            continue
        p = subprocess.run([nome] + args, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
        saida = p.stdout.decode("utf-8", "replace").strip().split("\n")
        versao = saida[0] if saida else ""
        eh_poppler = any(marca in l.lower() for l in saida)
        linhas.append("%-10s %s%s" % (nome, versao, "" if eh_poppler else
                                      "   <- NAO e o do poppler: %s" % caminho))
        if not eh_poppler:
            problema = True
    print("\n".join(linhas))
    if problema:
        print("ATENCAO: os testes de medida precisam do poppler (pdftotext -bbox).\n"
              "         No Windows com Git instalado, rode pelo PowerShell.")
    print()
    return not problema


def tarefas_pedidas():
    """Quantos testes de cada vez. O motor e monotarefa, entao vale um por
    nucleo; mais do que isso so disputa disco."""
    for i, a in enumerate(sys.argv):
        if a == "--tarefas" and i + 1 < len(sys.argv):
            return max(1, int(sys.argv[i + 1]))
        if a.startswith("--tarefas="):
            return max(1, int(a.split("=", 1)[1]))
    return max(1, min(8, os.cpu_count() or 4))


def main():
    argv = [a for a in sys.argv[1:]
            if not a.startswith("-") and not a.isdigit()]
    manter = "--manter" in sys.argv
    tarefas = tarefas_pedidas()
    if "--sem-cache" in sys.argv:
        os.environ["COPPE_SEM_CACHE"] = "1"
        import medidas
        medidas.SEM_CACHE = True
    # O nome de um teste e r, rt ou rtu, um numero e um apelido. O numero nao e
    # enfeite: sem ele,
    # "r" no comeco do nome bastava, e este proprio arquivo -- run-regressivo.py
    # -- se enquadrava. O rodador achava a si mesmo, rodava a si mesmo, e cada
    # copia achava a si mesma outra vez: uma recursao que so parou quando alguem
    # foi matar os processos na mao.
    testes = sorted(f for f in os.listdir(AQUI)
                    if RE_NOME.match(f))
    abertos = []
    if argv:
        testes = [t for t in testes if any(a in t for a in argv)]
    else:
        # sem filtro, os testes de defeito ABERTO ficam de fora: ver o docstring
        todos, testes = testes, []
        for t in todos:
            issue = aberto(os.path.join(AQUI, t))
            if issue:
                abertos.append((t, issue))
            else:
                testes.append(t)
    if not testes:
        print("nenhum teste casou com o filtro")
        return 1
    conferir_ferramentas()

    # O pdflatex precisa achar a classe em src/ e as bases .bib de la.
    for var in ("TEXINPUTS", "BIBINPUTS"):
        os.environ[var] = ".;" + SRC + ";" + os.environ.get(var, "")

    ruins = 0
    avisos = 0
    docache = 0

    def rodar_um(t):
        if t.endswith(".py"):
            return t, um_teste_python(os.path.join(AQUI, t))
        return t, um_teste(os.path.join(AQUI, t), manter)

    def relatar(t, resultado):
        """Uma linha por teste, na ordem em que cada um termina."""
        bug, falhas, pulados, veio_do_cache = resultado
        nome = os.path.splitext(t)[0]
        marca = " (cache)" if veio_do_cache else ""
        if falhas:
            print("FALHOU  %s%s  -- %s" % (nome, marca, bug))
            for f in falhas:
                print("        %s" % f)
        else:
            print("ok      %s%s  -- %s" % (nome, marca, bug))
        for a in pulados:
            print("        aviso: %s" % a)
        return len(falhas) > 0, len(pulados), veio_do_cache

    if tarefas == 1:
        for t in testes:
            _, resultado = rodar_um(t)
            falhou, n_avisos, veio = relatar(t, resultado)
            ruins += falhou
            avisos += n_avisos
            docache += veio
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=tarefas) as piscina:
            for t, resultado in piscina.map(rodar_um, testes):
                falhou, n_avisos, veio = relatar(t, resultado)
                ruins += falhou
                avisos += n_avisos
                docache += veio

    print("")
    if abertos:
        print("%d teste(s) de defeito ABERTO fora desta rodada; rode pelo nome: %s"
              % (len(abertos), " ".join("%s(%s)" % (t.split("-")[0], i) for t, i in abertos)))
    print("=== %d teste(s), %d falha(s), %d aviso(s), %d do cache, %d tarefa(s) ==="
          % (len(testes), ruins, avisos, docache, tarefas))
    return 1 if ruins else 0


if __name__ == "__main__":
    sys.exit(main())
