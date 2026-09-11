# -*- coding: utf-8 -*-
"""Suite de regressao da CoppeTeX: um teste minimo para cada defeito ja corrigido.

    python tests/regressivo/run-regressivo.py
    python tests/regressivo/run-regressivo.py r04
    python tests/regressivo/run-regressivo.py --manter

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
import io
import os
import re
import subprocess
import sys
import unicodedata

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
# r<numero>-<apelido>.tex ou .py. Ver o comentario em main().
RE_NOME = re.compile(r"^r\d+-.*\.(tex|py)$")


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

    p = compilar()
    if d.get("BIBER", "").lower() in ("sim", "yes", "1"):
        rodar(["biber", nome], AQUI)
    if d.get("MAKEINDEX", "").lower() in ("sim", "yes", "1"):
        ist = os.path.join(SRC, "coppe.ist")
        for ext, saida in (("abx", "lab"), ("syx", "los")):
            if os.path.exists(os.path.join(AQUI, nome + "." + ext)):
                rodar(["makeindex", "-s", ist, "-o", nome + "." + saida,
                       nome + "." + ext], AQUI)
    for _ in range(passadas - 1):
        p = compilar()

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
    return d.get("BUG", "(sem descricao)"), falhas, pulados


# O PDF fica, porque e ele que se olha quando um teste falha; o resto sai. Os
# .pdf daqui NAO vao para o git: ver o .gitignore de tests/.
RESTOS = ("aux bbl bcf blg idx ilg ind lab lof log lol loq lot los mw out "
          "run.xml syx abx toc xmpdata glo gls").split()


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
        return bug, [], []
    saida = p.stdout.decode("utf-8", "replace").strip().splitlines()
    return bug, ["saiu com codigo %d" % p.returncode] + saida[-6:], []


def main():
    argv = [a for a in sys.argv[1:] if not a.startswith("-")]
    manter = "--manter" in sys.argv
    # O nome de um teste e r<numero>-<apelido>. O numero nao e enfeite: sem ele,
    # "r" no comeco do nome bastava, e este proprio arquivo -- run-regressivo.py
    # -- se enquadrava. O rodador achava a si mesmo, rodava a si mesmo, e cada
    # copia achava a si mesma outra vez: uma recursao que so parou quando alguem
    # foi matar os processos na mao.
    testes = sorted(f for f in os.listdir(AQUI)
                    if RE_NOME.match(f))
    if argv:
        testes = [t for t in testes if any(a in t for a in argv)]
    if not testes:
        print("nenhum teste casou com o filtro")
        return 1

    # O pdflatex precisa achar a classe em src/ e as bases .bib de la.
    for var in ("TEXINPUTS", "BIBINPUTS"):
        os.environ[var] = ".;" + SRC + ";" + os.environ.get(var, "")

    ruins = 0
    avisos = 0
    for t in testes:
        if t.endswith(".py"):
            bug, falhas, pulados = um_teste_python(os.path.join(AQUI, t))
        else:
            bug, falhas, pulados = um_teste(os.path.join(AQUI, t), manter)
        nome = os.path.splitext(t)[0]
        if falhas:
            ruins += 1
            print("FALHOU  %s  -- %s" % (nome, bug))
            for f in falhas:
                print("        %s" % f)
        else:
            print("ok      %s  -- %s" % (nome, bug))
        for a in pulados:
            avisos += 1
            print("        aviso: %s" % a)

    print("")
    print("=== %d teste(s), %d falha(s), %d aviso(s) ===" % (len(testes), ruins, avisos))
    return 1 if ruins else 0


if __name__ == "__main__":
    sys.exit(main())
