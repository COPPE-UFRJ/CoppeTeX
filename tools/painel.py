# -*- coding: utf-8 -*-
"""Painel de controle do desenvolvedor da CoppeTeX.

    coppetex.bat                      abre a janela
    coppetex.bat --regerar --dist     faz so isso, sem janela
    coppetex.bat --tudo               a prova inteira
    coppetex.bat --ajuda              a lista completa

Tudo o que a janela faz, a linha de comando faz -- e o contrario tambem. A
janela nao tem nenhum caminho proprio: cada botao dela chama a mesma funcao que
a opcao de linha de comando chama, para que nao existam duas implementacoes da
mesma coisa, uma delas sempre um pouco atras da outra.

O trabalho pesado nao esta aqui. Compilar, rodar a suite e validar PDF/A e com o
tools/build-check.ps1, que ja existia, ja e usado no lugar certo e ja sabe o
ciclo completo de cada documento. Este arquivo orquestra: decide o que rodar, em
que ordem, e mostra a saida enquanto ela acontece.
"""
import io
import os
import shutil
import subprocess
import sys
import threading

# O console do Windows e cp1252 e nao sabe escrever uma seta nem um travessao.
# Como o painel repassa a saida de programas que escrevem os dois, sem isto ele
# morre no meio de um build por causa de um caractere de mensagem.
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(errors="replace")
    except (ValueError, OSError):
        pass

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(RAIZ, "src")
DIST = os.path.join(RAIZ, "dist")
TESTES = os.path.join(RAIZ, "tests")
TOOLS = os.path.join(RAIZ, "tools")

# O que o aluno precisa para escrever e depositar, e nada alem disso.
#
# A lista existe em UM lugar -- aqui -- e o src/doall.bat e o alvo `build' do
# Makefile chamam este passo. Ela ja esteve escrita em tres lugares, e os tres
# divergiram; tests/regressivo/r92 cobra que nao volte a acontecer.
#
# Duas ausencias sao deliberadas:
#
#   * o README.md. O de dist/ e um guia de instalacao e NAO vem da raiz -- uma
#     versao antiga deste passo copiava o da raiz por cima dele a cada
#     execucao, apagando o guia (issue #75);
#   * os exemplos em frances e italiano. Os pacotes desses dois idiomas vao,
#     porque sao demonstracao do mecanismo de extensao e alguem pode querer
#     usa-los; os documentos de exemplo, nao. O art. 57 da Resolucao CEPG
#     n. 302/2024 admite portugues, ingles e espanhol para redigir uma tese, e
#     e para esses tres que ha exemplo aqui.
PARA_DIST = [
    # A classe e o que ela carrega
    "coppe.cls", "coppe.dbx", "coppe.bbx", "coppe.cbx",
    "coppe-numeric.bbx", "coppe-numeric.cbx",
    "brazilian-coppe.lbx", "english-coppe.lbx", "spanish-coppe.lbx",
    "french-coppe.lbx", "italian-coppe.lbx",
    "coppe-lang-spanish.def", "coppe-lang-french.def", "coppe-lang-italian.def",
    "coppe.ist", "latexmkrc",
    "coppe-logo.eps", "coppe-logo.pdf", "ufrj-logo.pdf",
    # Os manuais: o da classe, o guia rapido em ingles e o da NORMA
    "coppe.pdf", "coppe-quickref.pdf", "manual.pdf",
    # Um exemplo por idioma admitido para redacao
    "example.tex", "example.bib", "coppe.bib", "example.pdf",
    "example_en.tex", "example_en.pdf",
    "example_es.tex", "example_es.pdf",
]

# Restos de compilacao. O .pdf nunca entra nesta lista: e o produto.
RESTOS = """aux bbl bcf blg fdb_latexmk fls glo gls idx ilg ind lab loa lof
lol lomapa loq los lot mw out run.xml syx toc xmpdata xmpi synctex.gz""".split()


# --------------------------------------------------------------------------
# Saida
# --------------------------------------------------------------------------
class Saida(object):
    """Para onde vao as linhas: o terminal, a janela, ou os dois."""

    def __init__(self, escrever=None):
        self.escrever = escrever or (lambda s: None)

    def __call__(self, linha=""):
        print(linha)
        sys.stdout.flush()
        self.escrever(linha)


def roda(cmd, cwd, saida):
    """Roda um programa e vai mostrando a saida dele linha a linha.

    Linha a linha, e nao no fim: a prova inteira leva minutos, e um painel que
    fica mudo durante minutos parece travado.
    """
    saida("$ " + " ".join(str(c) for c in cmd))
    try:
        p = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT, bufsize=1,
                             universal_newlines=True, errors="replace")
    except OSError as e:
        saida("   NAO RODOU: %s" % e)
        return False
    for linha in p.stdout:
        saida(linha.rstrip("\r\n"))
    p.wait()
    return p.returncode == 0


def powershell(script, saida, *args):
    cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
           "-File", os.path.join(TOOLS, script)] + list(args)
    return roda(cmd, RAIZ, saida)


# --------------------------------------------------------------------------
# As acoes
# --------------------------------------------------------------------------
def acao_regerar(saida):
    """O src inteiro sai do coppe.dtx e do coppe.ins. So isso, e e rapido."""
    return powershell("build-check.ps1", saida, "-Scope", "class")


def acao_docs(saida):
    """Os PDFs que sao a entrega: manual, exemplo, os cinco idiomas, a norma."""
    ok = powershell("build-check.ps1", saida, "-Scope", "example")
    ok = powershell("build-check.ps1", saida, "-Scope", "langs") and ok
    ok = powershell("build-check.ps1", saida, "-Scope", "docs") and ok
    return ok


def acao_testes(saida):
    """Primeira camada: a classe compila?"""
    return powershell("build-check.ps1", saida, "-Scope", "tests")


def acao_adversativo(saida):
    """Segunda camada: ela sobrevive a tudo ao mesmo tempo?"""
    return powershell("build-check.ps1", saida, "-Scope", "adversativa")


def acao_regressivo(saida):
    """Terceira camada: algum defeito ja corrigido voltou?"""
    return roda([sys.executable,
                 os.path.join(TESTES, "regressivo", "run-regressivo.py")],
                RAIZ, saida)


def acao_pdfa(saida):
    """PDF/A-2b pelo veraPDF. Sem o veraPDF instalado o passo e PULADO."""
    return powershell("build-check.ps1", saida, "-Scope", "pdfa")


def acao_prova(saida):
    """Tudo, com o veredito no fim. E o que tem de sair limpo antes de marcar."""
    return powershell("build-check.ps1", saida, "-Scope", "prova")


def acao_conferir(saida):
    """Os verificadores que nao compilam nada: so leem o que foi produzido."""
    ok = True
    for script in ("conferir-referencias-cruzadas.py", "conferir-manual.py",
                   "versao.py"):
        saida("")
        ok = roda([sys.executable, os.path.join(TOOLS, script)], RAIZ, saida) and ok
    return ok


def acao_dist(saida):
    """dist/ recebe COPIA do que esta em src/. Nunca compila nada por conta."""
    saida("")
    saida("copiando para dist/")
    faltando = []
    for nome in PARA_DIST:
        de = os.path.join(SRC, nome)
        if not os.path.exists(de):
            faltando.append(nome)
            continue
        shutil.copy2(de, os.path.join(DIST, nome))
        saida("   %s" % nome)
    # A licenca vem da RAIZ, e nao de src/, e por isso esta fora da lista. Ela
    # tem de ir junto: a GPL exige que o texto acompanhe o que se distribui.
    licenca = os.path.join(RAIZ, "COPYING")
    if os.path.exists(licenca):
        shutil.copy2(licenca, os.path.join(DIST, "COPYING"))
        saida("   COPYING")
    else:
        faltando.append("COPYING")
    if faltando:
        saida("")
        for nome in faltando:
            saida("   FALTOU  %s -- compile antes" % nome)
        return False
    saida("   %d arquivo(s) copiado(s)" % (len(PARA_DIST) + 1))
    saida("   (dist/ fica com esses mais o README.md dela, que nao e copiado)")
    return True


def acao_limpar(saida):
    """Tira os restos de compilacao de src/ e de tests/. Nao toca em PDF."""
    n = 0
    for pasta in (SRC, TESTES, os.path.join(TESTES, "adversativa"),
                  os.path.join(TESTES, "regressivo")):
        if not os.path.isdir(pasta):
            continue
        for nome in os.listdir(pasta):
            if any(nome.endswith("." + e) for e in RESTOS):
                try:
                    os.remove(os.path.join(pasta, nome))
                    n += 1
                except OSError:
                    pass
    saida("limpou %d arquivo(s) intermediario(s)" % n)
    return True


def acao_versao2(saida):
    return roda([sys.executable, os.path.join(TOOLS, "versao.py"),
                 "--subir", "2"], RAIZ, saida)


def acao_versao3(saida):
    return roda([sys.executable, os.path.join(TOOLS, "versao.py"),
                 "--subir", "3"], RAIZ, saida)


# nome de linha de comando, rotulo na janela, funcao, explicacao de uma linha
ACOES = [
    ("regerar", "Regerar o src a partir do .dtx", acao_regerar,
     "coppe.ins gera a classe, os estilos, os exemplos e o latexmkrc"),
    ("docs", "Compilar os PDFs da entrega", acao_docs,
     "manual da classe, exemplo, os cinco idiomas, manual da norma, capas"),
    ("testes", "Testes - primeira camada", acao_testes,
     "a suite de tests/: a classe compila?"),
    ("adversativo", "Testes - adversativo", acao_adversativo,
     "os seis documentos extremos, nos dois motores, com veraPDF"),
    ("regressivo", "Testes - regressivo", acao_regressivo,
     "um teste minimo para cada defeito ja corrigido"),
    ("pdfa", "Validar PDF/A", acao_pdfa,
     "veraPDF no perfil 2b; pulado se o veraPDF nao estiver instalado"),
    ("conferir", "Conferir sem compilar", acao_conferir,
     "referencias cruzadas, cobertura do manual e versao sincronizada"),
    ("tudo", "TUDO, com veredito", acao_prova,
     "a prova completa; e o que tem de sair limpo antes de marcar uma versao"),
    ("dist", "Copiar para dist/", acao_dist,
     "dist/ e copia do que esta em src/, e nada mais"),
    ("limpar", "Limpar intermediarios", acao_limpar,
     "tira .aux, .log e companhia de src/ e de tests/; nao toca em PDF"),
]

# A ordem em que as acoes rodam quando mais de uma e pedida. Nao e a ordem em
# que o usuario as marcou, e nao e por capricho:
#
#   * `regerar' vem antes de tudo, porque nada faz sentido contra uma classe
#     velha. `tudo' ja regera por dentro, e por isso vem antes das camadas de
#     teste -- rodar o regressivo ANTES dele seria testar a classe que estava
#     em disco, e nao a que acabou de sair do .dtx;
#   * `dist' depois de compilar, porque dist/ nao pode receber o que ainda nao
#     foi provado -- e ANTES de `conferir', porque um dos verificadores compara
#     dist/ com src/ byte a byte. Na ordem contraria ele reprovava uma copia que
#     o passo seguinte ia fazer, e o painel terminava dizendo "houve falha" com
#     tudo certo;
#   * `conferir' por ultimo entre os que leem, porque ele le os .log que a
#     compilacao acabou de escrever e a copia que o dist acabou de fazer;
#   * `limpar' no fim de tudo, senao apaga o que ainda nao foi lido nem copiado.
ORDEM = ["regerar", "tudo", "docs", "testes", "adversativo", "regressivo",
         "pdfa", "dist", "conferir", "limpar"]


def executar(pedidas, versao, saida):
    """Roda o que foi pedido, na ordem certa, e devolve True se tudo passou."""
    tudo_ok = True

    # A versao sobe ANTES de qualquer compilacao: o numero novo tem de entrar
    # nos arquivos gerados na mesma rodada, senao a distribuicao sai com metade
    # de cada versao.
    if versao in (2, 3):
        saida("=== subindo a versao (nivel %d) ===" % versao)
        fn = acao_versao2 if versao == 2 else acao_versao3
        if not fn(saida):
            saida("a versao nao subiu; nada mais foi feito")
            return False
        if "regerar" not in pedidas:
            pedidas = ["regerar"] + list(pedidas)
            saida("(regerar foi acrescentado: o numero novo precisa entrar nos gerados)")
        saida("")

    porordem = [a for a in ORDEM if a in pedidas]
    for nome in porordem:
        fn = dict((n, f) for n, _, f, _ in ACOES)[nome]
        saida("")
        saida("=== %s ===" % nome)
        ok = fn(saida)
        tudo_ok = ok and tudo_ok
        saida("--- %s: %s ---" % (nome, "ok" if ok else "FALHOU"))

    saida("")
    saida("=========================================")
    saida(" RESULTADO: " + ("tudo passou" if tudo_ok else "houve falha"))
    saida("=========================================")
    return tudo_ok


# --------------------------------------------------------------------------
# Linha de comando
# --------------------------------------------------------------------------
def ajuda():
    print(__doc__.strip())
    print("")
    print("Acoes (pode combinar):")
    for nome, rotulo, _, explica in ACOES:
        print("  --%-14s %s" % (nome, explica))
    print("")
    print("Versao:")
    print("  --versao 2       sobe o segundo nivel (4.1 -> 4.2)")
    print("  --versao 3       sobe o terceiro nivel (4.1 -> 4.1.1)")
    print("                   o primeiro nivel nao e oferecido: ver tools/versao.py")
    print("")
    print("Outras:")
    print("  --janela         forca a janela mesmo com acoes na linha de comando")
    print("  --ajuda          isto")
    return 0


def main(argv):
    if "--ajuda" in argv or "-h" in argv or "--help" in argv:
        return ajuda()

    nomes = [n for n, _, _, _ in ACOES]
    pedidas = [n for n in nomes if "--" + n in argv]

    versao = 0
    if "--versao" in argv:
        i = argv.index("--versao")
        try:
            versao = int(argv[i + 1])
        except (IndexError, ValueError):
            print("uso: --versao 2  ou  --versao 3")
            return 2
        if versao not in (2, 3):
            print("--versao aceita 2 ou 3. O primeiro nivel nao e oferecido:")
            print("trocar de major e decisao do projeto e da CPGP, nao de um script.")
            return 2

    if not pedidas and not versao and "--janela" not in argv:
        return abrir_janela()
    if "--janela" in argv:
        return abrir_janela(pedidas, versao)

    return 0 if executar(pedidas, versao, Saida()) else 1


# --------------------------------------------------------------------------
# Janela
# --------------------------------------------------------------------------
def abrir_janela(pedidas=(), versao=0):
    try:
        import tkinter as tk
        from tkinter import ttk, scrolledtext
    except ImportError:
        print("Este Python nao tem Tkinter, entao nao da para abrir a janela.")
        print("Tudo funciona pela linha de comando -- veja:")
        print("")
        return menu_de_texto()

    try:
        atual = versao_atual()
    except Exception:
        atual = "?"

    janela = tk.Tk()
    janela.title("CoppeTeX - painel do desenvolvedor")
    janela.geometry("980x720")

    topo = ttk.Frame(janela, padding=10)
    topo.pack(fill="x")
    ttk.Label(topo, text="CoppeTeX %s" % atual,
              font=("Segoe UI", 14, "bold")).pack(side="left")
    ttk.Label(topo, text="   fonte unica: src/coppe.dtx").pack(side="left")

    corpo = ttk.Frame(janela, padding=(10, 0))
    corpo.pack(fill="x")

    caixa = ttk.LabelFrame(corpo, text=" O que fazer ", padding=10)
    caixa.pack(side="left", fill="both", expand=True)
    variaveis = {}
    for nome, rotulo, _, explica in ACOES:
        v = tk.BooleanVar(value=(nome in pedidas))
        variaveis[nome] = v
        linha = ttk.Frame(caixa)
        linha.pack(fill="x", anchor="w")
        ttk.Checkbutton(linha, text=rotulo, variable=v).pack(side="left")
        ttk.Label(linha, text="  " + explica,
                  foreground="#666").pack(side="left")

    lado = ttk.Frame(corpo, padding=(10, 0))
    lado.pack(side="left", fill="y")

    cxv = ttk.LabelFrame(lado, text=" Versao ", padding=10)
    cxv.pack(fill="x")
    vv = tk.IntVar(value=versao)
    ttk.Radiobutton(cxv, text="nao mexer (%s)" % atual,
                    variable=vv, value=0).pack(anchor="w")
    ttk.Radiobutton(cxv, text="subir para %s" % proxima(atual, 2),
                    variable=vv, value=2).pack(anchor="w")
    ttk.Radiobutton(cxv, text="subir para %s" % proxima(atual, 3),
                    variable=vv, value=3).pack(anchor="w")
    ttk.Label(cxv, text="o primeiro nivel (4 -> 5)\nnao e oferecido: e decisao\ndo projeto e da CPGP",
              foreground="#666", justify="left").pack(anchor="w", pady=(6, 0))

    botoes = ttk.Frame(lado, padding=(0, 10))
    botoes.pack(fill="x")

    def marcar_tudo():
        for nome, v in variaveis.items():
            v.set(nome in ("tudo", "conferir", "regressivo", "dist"))

    def desmarcar():
        for v in variaveis.values():
            v.set(False)

    ttk.Button(botoes, text="Antes de marcar uma versao",
               command=marcar_tudo).pack(fill="x")
    ttk.Button(botoes, text="Desmarcar tudo", command=desmarcar).pack(fill="x", pady=4)

    texto = scrolledtext.ScrolledText(janela, wrap="none", height=24,
                                      font=("Consolas", 9))
    texto.pack(fill="both", expand=True, padx=10, pady=10)

    rodape = ttk.Frame(janela, padding=(10, 0, 10, 10))
    rodape.pack(fill="x")
    estado = ttk.Label(rodape, text="parado")
    estado.pack(side="left")

    fila = []
    trava = threading.Lock()

    def escrever(linha):
        with trava:
            fila.append(linha)

    def drenar():
        with trava:
            pendentes, fila[:] = fila[:], []
        if pendentes:
            texto.insert("end", "\n".join(pendentes) + "\n")
            texto.see("end")
        janela.after(100, drenar)

    botao_rodar = ttk.Button(rodape, text="Rodar")
    botao_rodar.pack(side="right")

    def rodar():
        escolhidas = [n for n, v in variaveis.items() if v.get()]
        if not escolhidas and vv.get() == 0:
            escrever("nada marcado")
            return
        botao_rodar.state(["disabled"])
        estado.config(text="rodando...")
        texto.delete("1.0", "end")

        def trabalho():
            ok = executar(escolhidas, vv.get(), Saida(escrever))
            janela.after(0, lambda: (
                botao_rodar.state(["!disabled"]),
                estado.config(text="tudo passou" if ok else "houve falha")))

        threading.Thread(target=trabalho, daemon=True).start()

    botao_rodar.config(command=rodar)
    janela.after(100, drenar)
    janela.mainloop()
    return 0


def versao_atual():
    import re
    texto = io.open(os.path.join(SRC, "coppe.dtx"),
                    encoding="utf-8", errors="replace").read()
    m = re.search(r"\\def\\fileversion\{v([0-9.]+)\}", texto)
    return m.group(1) if m else "?"


def proxima(atual, nivel):
    partes = [int(x) for x in atual.split(".")] if atual != "?" else [4, 0]
    while len(partes) < 3:
        partes.append(0)
    if nivel == 2:
        partes[1] += 1
        partes[2] = 0
    else:
        partes[2] += 1
    if partes[2] == 0:
        return "%d.%d" % (partes[0], partes[1])
    return "%d.%d.%d" % tuple(partes)


def menu_de_texto():
    """Sem Tkinter, a pergunta e feita no terminal mesmo."""
    print("Painel CoppeTeX -- marque o que quer, separado por espaco:")
    print("")
    for i, (nome, rotulo, _, explica) in enumerate(ACOES, 1):
        print("  %2d. %-28s %s" % (i, rotulo, explica))
    print("")
    print("   v2. subir a versao para %s" % proxima(versao_atual(), 2))
    print("   v3. subir a versao para %s" % proxima(versao_atual(), 3))
    print("")
    try:
        resposta = input("numeros (vazio cancela): ").strip()
    except EOFError:
        return 1
    if not resposta:
        return 1
    versao = 0
    escolhidas = []
    for item in resposta.split():
        if item.lower() in ("v2", "v3"):
            versao = int(item[1])
        elif item.isdigit() and 1 <= int(item) <= len(ACOES):
            escolhidas.append(ACOES[int(item) - 1][0])
    return 0 if executar(escolhidas, versao, Saida()) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
