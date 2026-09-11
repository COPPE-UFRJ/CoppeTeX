# -*- coding: utf-8 -*-
"""Confere e sobe o numero de versao da CoppeTeX.

    python tools/versao.py                 # confere; sai 1 se algo divergir
    python tools/versao.py --detalhe       # confere e lista as mencoes historicas
    python tools/versao.py --subir 2       # 4.1 -> 4.2
    python tools/versao.py --subir 3       # 4.1 -> 4.1.1

A versao canonica e a do `\\def\\fileversion` em src/coppe.dtx. Tudo o mais e
conferido contra ela.

Por que existe, e por que o nivel 1 nao existe
----------------------------------------------
O numero aparece em uma duzia de lugares -- no .dtx, em cada arquivo que o
docstrip gera a partir dele, nos avisos dos dois README e no topo do CHANGELOG
-- e basta um deles ficar para tras para que a distribuicao se contradiga: o
usuario le 4.1 no README e o LaTeX escreve v4.0 no log.

Subir o primeiro nivel (de 4 para 5) NAO e oferecido de proposito. A troca de
major na CoppeTeX significou, historicamente, mudanca de modelo: a 4.0 trouxe o
modelo multilingue e a 3.0 a reescrita da classe. Isso e decisao de quem
mantem o projeto e da CPGP, nao de um script -- e um clique errado num painel
nao pode anunciar uma versao que nao existe.
"""
import io
import os
import re
import sys
import datetime

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DTX = os.path.join(RAIZ, "src", "coppe.dtx")

# O console do Windows e cp1252 e nao sabe escrever uma seta, um travessao nem
# um til combinante. Sem isto, o script MORRE no meio ao imprimir uma linha de
# arquivo que tenha um desses -- e o que ele estava imprimindo era justamente o
# relatorio. Substituir o caractere e feio; interromper o relatorio e pior.
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(errors="replace")
    except (ValueError, OSError):
        pass

# Arquivos gerados pelo docstrip que carimbam a versao num \ProvidesFile ou
# \ProvidesClass. Divergencia aqui quase sempre quer dizer a mesma coisa: o
# coppe.ins nao foi rodado depois da ultima mudanca no .dtx.
#
# Os de src/ estao escritos aqui; os de dist/ NAO, e sao deduzidos da lista do
# painel. A razao: dist/ tem subpastas -- es/, outraslinguas/ --, e a lista de
# quem vai para onde ja existe em tools/painel.py. Escrever os caminhos aqui de
# novo criaria a segunda copia da mesma lista, e ela divergiu no dia seguinte a
# reorganizacao: este verificador cobrava dist/spanish-coppe.lbx, que tinha
# passado a ser dist/es/spanish-coppe.lbx.
ESTILOS = [
    "coppe.cls", "coppe.dbx", "coppe.bbx", "coppe.cbx",
    "coppe-numeric.bbx", "coppe-numeric.cbx",
    "brazilian-coppe.lbx", "english-coppe.lbx", "spanish-coppe.lbx",
    "french-coppe.lbx", "italian-coppe.lbx",
    "coppe-lang-spanish.def", "coppe-lang-french.def", "coppe-lang-italian.def",
]

GERADOS = ["src/" + n for n in ESTILOS]

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from painel import PARA_DIST
except ImportError:                      # sem o painel, confere so o src/
    PARA_DIST = []
for subpasta, nome in PARA_DIST:
    if nome in ESTILOS:
        GERADOS.append("dist/" + (subpasta + "/" + nome if subpasta else nome))

# Lugares em prosa que TEM de trazer a versao corrente. A lista e explicita, e
# nao uma varredura, porque o repositorio esta cheio de mencoes historicas
# legitimas -- o CHANGELOG fala da 4.0 e da 3.8, o guia de migracao fala da v3 --
# e reprova-las seria pedir para que o verificador fosse desligado.
PROSA = [
    ("README.md", r"Esta é a CoppeTeX (\d+\.\d+(?:\.\d+)?)"),
    ("README.md", r"This is CoppeTeX (\d+\.\d+(?:\.\d+)?)"),
    ("README.md", r"proposal for CPGP \(v(\d+\.\d+(?:\.\d+)?)\)"),
    ("README.md", r"carries CoppeTeX \*\*(\d+\.\d+(?:\.\d+)?)\*\*"),
    ("dist/README.md", r"Esta é a CoppeTeX (\d+\.\d+(?:\.\d+)?)"),
    # O CHANGELOG e o mais novo primeiro, entao o primeiro "## [x.y]" do arquivo
    # e o da versao corrente.
    ("CHANGELOG.md", r"^## \[(\d+\.\d+(?:\.\d+)?)\]"),
]

RE_PROVIDES = re.compile(
    r"(\\Provides(?:File|Class)\{[^}]+\}\[)(\d{4}/\d{2}/\d{2})( v)(\d+\.\d+(?:\.\d+)?)")
RE_FILEVERSION = re.compile(r"(\\def\\fileversion\{v)(\d+\.\d+(?:\.\d+)?)(\})")
RE_FILEDATE = re.compile(r"(\\def\\filedate\{)(\d{4}/\d{2}/\d{2})(\})")


def ler(caminho):
    return io.open(caminho, encoding="utf-8", errors="replace").read()


def canonica():
    m = RE_FILEVERSION.search(ler(DTX))
    if not m:
        raise SystemExit("nao achei \\def\\fileversion em src/coppe.dtx")
    return m.group(2)


def conferir(detalhe=False):
    alvo = canonica()
    print("versao canonica (src/coppe.dtx): %s" % alvo)
    problemas = []

    # 1. O proprio .dtx: todo \ProvidesFile/\ProvidesClass, inclusive o que fica
    #    em comentario e alimenta o \GetFileInfo do manual.
    texto = ler(DTX)
    for m in RE_PROVIDES.finditer(texto):
        if m.group(4) != alvo:
            linha = texto[:m.start()].count("\n") + 1
            problemas.append("src/coppe.dtx:%d  %s (esperado %s)"
                             % (linha, m.group(0).strip(), alvo))

    # 2. Os gerados. Divergir aqui costuma ser o coppe.ins nao rodado.
    for rel in GERADOS:
        caminho = os.path.join(RAIZ, rel.replace("/", os.sep))
        if not os.path.exists(caminho):
            problemas.append("%s  nao existe" % rel)
            continue
        conteudo = ler(caminho)
        # O coppe.cls nao carimba a versao literalmente: o \ProvidesClass dele
        # usa \filedate e \fileversion, que sao definidos duas linhas acima. Por
        # isso os dois padroes, e nao so o \ProvidesFile.
        achou = None
        m = RE_FILEVERSION.search(conteudo)
        if m:
            achou = m.group(2)
        else:
            m = RE_PROVIDES.search(conteudo)
            if m:
                achou = m.group(4)
        if achou is None:
            problemas.append("%s  nao carimba versao nenhuma" % rel)
        elif achou != alvo:
            problemas.append("%s  diz v%s (esperado %s)" % (rel, achou, alvo))

    # 3. A prosa que tem de acompanhar.
    for rel, padrao in PROSA:
        caminho = os.path.join(RAIZ, rel.replace("/", os.sep))
        if not os.path.exists(caminho):
            problemas.append("%s  nao existe" % rel)
            continue
        m = re.search(padrao, ler(caminho), re.M)
        if not m:
            problemas.append("%s  nao casou com o padrao %r" % (rel, padrao))
        elif m.group(1) != alvo:
            problemas.append("%s  diz %s (esperado %s)" % (rel, m.group(1), alvo))

    # 4. dist/ e COPIA de src/. Se um arquivo divergir, a distribuicao nao e
    #    mais a classe que acabou de ser provada -- e o numero de versao, que e
    #    o mesmo nos dois, nao denuncia isso.
    for rel in GERADOS:
        if not rel.startswith("dist/"):
            continue
        emdist = os.path.join(RAIZ, rel.replace("/", os.sep))
        emsrc = os.path.join(RAIZ, "src", os.path.basename(rel))
        if os.path.exists(emdist) and os.path.exists(emsrc):
            if io.open(emdist, "rb").read() != io.open(emsrc, "rb").read():
                problemas.append("%s  difere de src/%s -- falta copiar para dist"
                                 % (rel, os.path.basename(rel)))

    if detalhe:
        print("")
        print("mencoes a OUTRA versao (informativo, nao sao erro):")
        # O padrao exige contexto de versao -- "v4.0", "CoppeTeX 4.0", "versao
        # 3.8". Sem isso a lista vinha cheia de numeros de item do Manual, que
        # se parecem com versao e nao sao: 3.1.2.1.4, 4.2, 2.6. Uma lista que e
        # quase toda ruido nao e lida, e deixa de servir para alguma coisa.
        contexto = re.compile(
            r"(?:\bv(\d+\.\d+(?:\.\d+)?)\b"
            r"|CoppeTeX\s+(\d+\.\d+(?:\.\d+)?)\b"
            r"|[Vv]ers[aã]o\D{0,12}?(\d+\.\d+(?:\.\d+)?)\b)")
        for raiz, _, arquivos in os.walk(RAIZ):
            if any(p in raiz for p in (".git", "_scratch", "specs", "dist")):
                continue
            for a in sorted(arquivos):
                if not a.endswith(".md"):
                    continue
                caminho = os.path.join(raiz, a)
                rel = os.path.relpath(caminho, RAIZ)
                for n, linha in enumerate(ler(caminho).splitlines(), 1):
                    achados = [g for m in contexto.finditer(linha)
                               for g in m.groups() if g]
                    if achados and all(v != alvo for v in achados):
                        print("   %s:%d  %s" % (rel, n, linha.strip()[:88]))

    print("")
    if problemas:
        for p in problemas:
            print("DIVERGE  %s" % p)
        print("")
        print("=== %d divergencia(s) ===" % len(problemas))
        return 1
    print("ok  versao %s sincronizada em %d gerado(s) e %d lugar(es) em prosa"
          % (alvo, len(GERADOS), len(PROSA)))
    return 0


def subir(nivel):
    """Sobe o segundo ou o terceiro nivel. O primeiro nunca."""
    if nivel not in (2, 3):
        print("nivel tem de ser 2 (4.1 -> 4.2) ou 3 (4.1 -> 4.1.1).")
        print("O nivel 1 nao e oferecido: trocar de major e decisao do projeto")
        print("e da CPGP, nao de um script.")
        return 2

    velha = canonica()
    partes = [int(x) for x in velha.split(".")]
    while len(partes) < 3:
        partes.append(0)
    if nivel == 2:
        partes[1] += 1
        partes[2] = 0
    else:
        partes[2] += 1
    nova = "%d.%d" % (partes[0], partes[1]) if partes[2] == 0 else \
           "%d.%d.%d" % tuple(partes)
    hoje = datetime.date.today().strftime("%Y/%m/%d")
    print("%s  ->  %s   (data %s)" % (velha, nova, hoje))

    texto = ler(DTX)
    texto = RE_FILEVERSION.sub(lambda m: m.group(1) + nova + m.group(3), texto)
    texto = RE_FILEDATE.sub(lambda m: m.group(1) + hoje + m.group(3), texto)
    texto = RE_PROVIDES.sub(
        lambda m: m.group(1) + hoje + m.group(3) + nova, texto)
    io.open(DTX, "w", encoding="utf-8", newline="\n").write(texto)
    print("src/coppe.dtx atualizado")

    # A prosa NAO e reescrita por conta propria. O aviso do README e o titulo do
    # CHANGELOG nao sao so um numero: sao uma frase sobre o que aquela versao e,
    # e trocar o numero deixando a frase velha e pior do que nao trocar nada.
    print("")
    print("Falta a mao, e de proposito:")
    for rel, _ in PROSA:
        print("   %s" % rel)
    print("")
    print("Depois rode:  coppetex.bat --regerar --dist  e  python tools/versao.py")
    return 0


def main():
    if "--subir" in sys.argv:
        i = sys.argv.index("--subir")
        try:
            return subir(int(sys.argv[i + 1]))
        except (IndexError, ValueError):
            print("uso: python tools/versao.py --subir 2|3")
            return 2
    return conferir(detalhe="--detalhe" in sys.argv)


if __name__ == "__main__":
    sys.exit(main())
