#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Confere o manual contra a classe: nenhum comando publico pode ficar de fora.

O manual e o exemplo envelhecem em silencio. Um comando novo entra na classe e
ninguem o documenta; uma linha do max-exemplo.tex se desloca e a tabela "onde ver
cada coisa funcionando" passa a apontar para o lugar errado. Nenhuma das duas
coisas quebra a compilacao, e por isso nenhuma das duas aparece sozinha.

Este script olha cinco coisas:

  1. Todo comando e ambiente PUBLICO que a classe define aparece no manual,
     marcado com \\DescribeMacro ou \\DescribeEnv?
  2. Toda opcao de classe aparece na secao de opcoes?
  3. Os numeros de linha da tabela "onde ver" ainda batem com o max-exemplo.tex?
  4. Os guardas de macrocode do .dtx estao bem escritos? Um guarda torto nao
     quebra nada: so faz o manual imprimir documentacao como se fosse codigo.
  5. Todo comando publico tem os DOIS NOMES -- o ingles, que tem o codigo, e o
     apelido em portugues --, e o par esta declarado no bloco unico de apelidos
     do fim da classe? Espalhados pelo codigo, um comando novo nascia com um
     nome so e ninguem percebia.

O que NAO e cobrado: comandos internos (os que levam @ no nome), os quatro
comandos de montagem de folha que o manual lista de proposito na secao
"Comandos que voce nao deve chamar", e os logotipos da familia TeX, que sao
enfeite tipografico e nao API.

    python3 tools/conferir-manual.py

Sai com codigo 1 se algo estiver fora do lugar, para poder entrar no harness.
"""
import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DTX = os.path.join(RAIZ, "src", "ufrj.dtx")
CLS = os.path.join(RAIZ, "src", "ufrj.cls")
EXEMPLO = os.path.join(RAIZ, "src", "max-exemplo.tex")
# O estilo da COPPE tem fonte e manual proprios. Um comando publico dele pode
# estar documentado em qualquer dos dois manuais -- os que o estilo redefine sao
# da classe, e e la que estao descritos --, e os guardas de macrocode dos dois
# .dtx sao conferidos.
STY = os.path.join(RAIZ, "src", "ufrj-coppe.sty")
DTX_COPPE = os.path.join(RAIZ, "src", "ufrj-coppe.dtx")
# O estilo da Escola Politecnica entra pela mesma razao: hoje ele nao cria
# comando publico nenhum -- so declara dados pela interface da classe --, e e
# justamente isso que a conferencia mantem verdadeiro.
STY_POLI = os.path.join(RAIZ, "src", "ufrj-poli.sty")
DTX_POLI = os.path.join(RAIZ, "src", "ufrj-poli.dtx")

# Logotipos da familia TeX e afins: a classe os define para uso tipografico,
# nao sao interface de quem escreve uma tese.
ENFEITE = {
    "TeX", "LaTeX", "LaTeXe", "BibTeX", "pdfTeX", "pdfLaTeX", "LuaLaTeX",
    "XeLaTeX", "MiKTeX", "CoppeTeX",
}

# Redefinicoes de comandos do proprio LaTeX, documentadas onde fazem sentido
# (ou nao documentadas de proposito, por serem o comando padrao inalterado).
PADRAO_LATEX = {
    "and", "appendixname", "cleardoublepage", "csname", "familydefault",
    "filedate", "filename", "fileversion", "footnoterule", "headrulewidth",
    "item", "numberline", "protect", "theFancyVerbLine", "glossaryname",
    "listabbreviationname", "listsymbolname", "listsiglaname", "lstlistingname",
    "lstlistlistingname", "quadroname", "listquadroname",
    "quadroautorefname", "cpsourcename",
    # o do algorithm2e, com o nome da legenda no lugar do minusculo (#149)
    "algorithmautorefname",
    # redefinidos localmente: \PackageWarning so durante o carregamento do
    # pdfx, \thepage so na folha adicional, \theHchapter so nos anexos, e o
    # \contentsline so na leitura do .toc de OUTRO volume, para a linha sair
    # sem o destino do hyperref (#126)
    "PackageWarning", "thepage", "theHchapter", "contentsline",
    # nomes do babel: "ver"/"ver tambem" nas remissivas do indice (NBR 6034)
    "seename", "alsoname",
}

# Ambientes internos do mecanismo de listas, nunca escritos a mao.
ENV_INTERNO = {"theglossary", "theindex"}


# Os comandos que a classe cria e que NAO tem par, com a razao. Sao poucos, e
# cada um esta explicado na secao "Os dois nomes de cada comando" do manual.
SEM_PAR = {
    # iguais nos dois idiomas
    "volume", "volumes",
    # o nome e o da familia do biblatex mais o latim `apud'
    "citepapud", "citetapud",
    # ja e o nome portugues de um comando do csquotes (\enquote)
    "citacao",
    # do proprio LaTeX ou de um pacote: a classe os REDEFINE, e o nome nao e
    # nosso para traduzir
    "title", "author", "date", "appendix", "frontmatter", "mainmatter",
    "backmatter", "listoffigures", "listoftables", "printbibliography",
    # o par traduz os VALORES do argumento, e por isso e um comando proprio e
    # nao um \let: \productiontype{technical} e \tipoproducao{tecnica}
    "productiontype", "tipoproducao", "linkedproject", "projetovinculado",
    # o estilo ufrj-coppe guarda os nomes da v4.1 para o trabalho escrito ate
    # la: sao apelidos de COMPATIBILIDADE, de um nome velho para um novo, e nao
    # o par de idiomas -- o par deles e o do comando da classe que apelidam
    "coppefinalengine", "coppefinalfont", "coppefinalmanual",
    "coppefinalsystem", "coppefinaltexsystem", "coppefinaltime",
    "coppeforeignstring", "coppemainstring", "copperdefstring", "coppestring",
    "coppetexfinalpage", "newcoppefloat", "usecoppelanguage",
    # os quatro de montagem de folha que o manual manda nao chamar entram pela
    # lista `naochame', e os enfeites tipograficos pela ENFEITE
}

# O bloco unico: comeca no cabecalho e termina na linha de tracos seguinte.
INICIO_APELIDOS = "% OS APELIDOS EM PORTUGUES."
FIM_APELIDOS = "% FIM DOS APELIDOS"


def ler(caminho):
    return io.open(caminho, encoding="utf-8", errors="replace").read()


def bloco_de_apelidos(dtx):
    """O texto do bloco unico de apelidos, tal como esta no .dtx."""
    i = dtx.find(INICIO_APELIDOS)
    if i < 0:
        return None
    f = dtx.find(FIM_APELIDOS, i)
    return dtx[i:f if f > 0 else len(dtx)]


def pares(bloco):
    """{nome: parceiro} dos dois lados de cada apelido do bloco."""
    tabela = {}
    if not bloco:
        return tabela
    for apelido, original in re.findall(r"\\let\\([A-Za-z]+)\\([A-Za-z]+)", bloco):
        tabela[apelido] = original
        tabela[original] = apelido
    for apelido, original in re.findall(
            r"\\@ifundefined\{([A-Za-z]+)\}\{\}\{\\let\\([A-Za-z]+)\\[A-Za-z]+\}", bloco):
        tabela[apelido] = original
        tabela[original] = apelido
    for apelido, original in re.findall(
            r"\\@ifundefined\{([A-Za-z]+)\}\{\\let\\[A-Za-z]+\\([A-Za-z]+)\}", bloco):
        tabela[apelido] = original
        tabela[original] = apelido
    # \epigraph nao pode ser um \let: o pacote epigraph tem um comando com o
    # mesmo nome, e quem o carrega fica com o dele.
    for apelido, original in re.findall(
            r"\\providecommand\\([A-Za-z]+)\{\\([A-Za-z]+)\}", bloco):
        tabela[apelido] = original
        tabela[original] = apelido
    return tabela


def definidos(cls):
    cmds = set()
    cmds |= set(re.findall(r"\\(?:new|renew|provide)command\*?\s*\{?\\([A-Za-z@]+)", cls))
    cmds |= set(re.findall(r"\\let\\([A-Za-z@]+)\s*\\", cls))
    cmds |= set(re.findall(r"\\def\\([A-Za-z@]+)", cls))
    envs = set(re.findall(r"\\(?:new|renew)environment\*?\s*\{([A-Za-z@]+)\}", cls))
    envs |= set(re.findall(r"\\lstnewenvironment\{([A-Za-z@]+)\}", cls))
    envs |= set(re.findall(r"\\newfloat\{([A-Za-z@]+)\}", cls))
    opts = set(re.findall(r"\\DeclareOption\{([^}]*)\}", cls))
    publicos = {c for c in cmds if "@" not in c}
    return publicos, envs, opts


def documentados(dtx):
    macros = set(re.findall(r"\\DescribeMacro\{\\([A-Za-z@]+)\}", dtx))
    envs = set(re.findall(r"\\DescribeEnv\{([A-Za-z@]+)\}", dtx))
    # A secao "Comandos que voce nao deve chamar" lista os de montagem de folha.
    naochame = set(re.findall(r"\|\\(make[A-Za-z]+)\|", dtx))
    naochame |= set(re.findall(r"\|\\(ufrjfinal[a-z]+)\|", dtx))
    return macros, envs, naochame


def onde_ver(dtx, exemplo):
    """Confere a tabela de linhas do max-exemplo.tex."""
    linhas_ex = exemplo.split("\n")
    problemas = []
    # linhas da tabela: ... & |\comando| & 123 \\
    for cmd, num in re.findall(r"&\s*\|\\([A-Za-z@]+)\|\s*&\s*(\d+)\s*\\\\", dtx):
        n = int(num)
        if n < 1 or n > len(linhas_ex):
            problemas.append((cmd, n, "fora do arquivo"))
            continue
        if not re.search(r"\\" + cmd + r"(?![A-Za-z])", linhas_ex[n - 1]):
            real = None
            for i, l in enumerate(linhas_ex, 1):
                if re.search(r"\\" + cmd + r"(?![A-Za-z])", l):
                    real = i
                    break
            problemas.append((cmd, n, "esta na linha %s" % (real or "nenhuma")))
    return problemas


GUARDA_BOA = re.compile(r"^%    \\(begin|end)\{macrocode\*?\}$")
GUARDA_QUALQUER = re.compile(r"\\(begin|end)\{macrocode\*?\}")


def guardas(dtx):
    """Confere os guardas de macrocode do .dtx.

    O doc.sty so fecha um bloco de codigo quando a linha e, EXATAMENTE, um '%'
    seguido de QUATRO espacos e do \\end{macrocode}. Com tres espacos o bloco
    nao fecha, e tudo o que vem depois -- documentacao inclusive -- sai
    impresso como codigo, verbatim, no ufrj.pdf. Nada quebra a compilacao, e
    por isso ninguem ve: foi assim que sessenta linhas do manual passaram
    quatro versoes impressas como se fossem codigo.

    O sinal de porcentagem tambem merece cuidado na parte de documentacao: o
    doc.sty ignora TODOS eles, e nao apenas o primeiro de cada linha, de modo
    que uma linha comecada por '%%%%' abre um bloco de codigo de verdade.
    """
    problemas = []
    aberto = False
    for n, linha in enumerate(dtx.split("\n"), 1):
        if not GUARDA_QUALQUER.search(linha):
            continue
        m = GUARDA_BOA.match(linha)
        if not m:
            problemas.append((n, "guarda fora do padrao: %s" % linha.strip()))
            continue
        if m.group(1) == "begin":
            if aberto:
                problemas.append((n, "abriu macrocode com bloco ja aberto"))
            aberto = True
        else:
            if not aberto:
                problemas.append((n, "fechou macrocode sem bloco aberto"))
            aberto = False
    if aberto:
        problemas.append((0, "o .dtx termina com um bloco macrocode aberto"))
    return problemas


def main():
    cls, dtx, exemplo = ler(CLS), ler(DTX), ler(EXEMPLO)
    sty, dtx_coppe = ler(STY), ler(DTX_COPPE)
    sty_poli, dtx_poli = ler(STY_POLI), ler(DTX_POLI)
    cmds, envs, opts = definidos(cls)
    for outro in (sty, sty_poli):
        cmds_sty, envs_sty, _ = definidos(outro)
        cmds |= cmds_sty
        envs |= envs_sty
    docmac, docenv, naochame = documentados(
        dtx + "\n" + dtx_coppe + "\n" + dtx_poli)

    faltam_cmd = sorted(
        c for c in cmds
        if c not in docmac and c not in ENFEITE and c not in PADRAO_LATEX
        and c not in naochame
    )
    faltam_env = sorted(e for e in envs if e not in docenv and e not in ENV_INTERNO)
    faltam_opt = sorted(o for o in opts if ("texttt{%s}" % o) not in dtx)
    bloco = bloco_de_apelidos(dtx)
    dupla = pares(bloco)
    sem_par = sorted(
        c for c in cmds
        if c not in dupla and c not in SEM_PAR and c not in ENFEITE
        and c not in PADRAO_LATEX and c not in naochame
    )
    # Um apelido declarado FORA do bloco e o defeito que a regra existe para
    # impedir: ele funciona, e some da tabela do manual.
    fora = []
    if bloco:
        resto = dtx.replace(bloco, "")
        for apelido, original in re.findall(r"\n\\let\\([A-Za-z]+)\\([A-Za-z]+)", resto):
            if apelido in cmds and original in cmds and apelido not in dupla:
                fora.append(apelido)
    desalinhadas = onde_ver(dtx, exemplo)
    tortos = guardas(dtx) + [(n, "ufrj-coppe.dtx: " + obs)
                             for n, obs in guardas(dtx_coppe)] \
        + [(n, "ufrj-poli.dtx: " + obs) for n, obs in guardas(dtx_poli)]

    erros = 0
    print("=== conferir-manual: %d comandos publicos, %d ambientes, %d opcoes"
          % (len(cmds), len(envs), len(opts)))

    if faltam_cmd:
        erros += len(faltam_cmd)
        print("\nERRO  %d comando(s) publico(s) sem \\DescribeMacro no manual:"
              % len(faltam_cmd))
        for c in faltam_cmd:
            print("        \\%s" % c)
    else:
        print("ok    todo comando publico esta documentado")

    if faltam_env:
        erros += len(faltam_env)
        print("\nERRO  %d ambiente(s) sem \\DescribeEnv no manual:" % len(faltam_env))
        for e in faltam_env:
            print("        %s" % e)
    else:
        print("ok    todo ambiente esta documentado")

    if faltam_opt:
        erros += len(faltam_opt)
        print("\nERRO  %d opcao(oes) de classe nao citada(s) no manual:" % len(faltam_opt))
        for o in faltam_opt:
            print("        %s" % o)
    else:
        print("ok    toda opcao de classe esta documentada")

    if bloco is None:
        erros += 1
        print("\nERRO  nao achei o bloco unico de apelidos no ufrj.dtx"
              " (procurei por '%s')" % INICIO_APELIDOS)
    elif sem_par:
        erros += len(sem_par)
        print("\nERRO  %d comando(s) publico(s) com um nome so:" % len(sem_par))
        for c in sorted(sem_par):
            print("        \\%s -- declare o par no bloco de apelidos, ou"
                  " justifique a excecao em SEM_PAR" % c)
    elif fora:
        erros += len(fora)
        print("\nERRO  %d apelido(s) declarado(s) fora do bloco unico:" % len(fora))
        for c in sorted(set(fora)):
            print("        \\%s" % c)
    else:
        print("ok    todo comando publico tem os dois nomes, no bloco unico"
              " (%d nomes)" % len(dupla))

    if desalinhadas:
        erros += len(desalinhadas)
        print("\nERRO  %d linha(s) da tabela 'onde ver' nao batem com o max-exemplo.tex:"
              % len(desalinhadas))
        for cmd, n, obs in desalinhadas:
            print("        \\%-22s manual diz %-5d %s" % (cmd, n, obs))
    else:
        print("ok    a tabela 'onde ver' bate com o max-exemplo.tex")

    if tortos:
        erros += len(tortos)
        print("\nERRO  %d guarda(s) de macrocode mal escrito(s) no ufrj.dtx:"
              % len(tortos))
        for n, obs in tortos:
            print("        linha %-6s %s" % (n or "?", obs))
    else:
        print("ok    os guardas de macrocode estao bem escritos")

    print("\n=== %d problema(s) ===" % erros)
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
