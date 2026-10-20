# CoppeTeX no Overleaf — tese ou dissertação da COPPE

**Este `.zip` é um projeto do Overleaf pronto.** Ele tem a classe, o estilo da
COPPE, os estilos de bibliografia, os logotipos, uma base de referências e um
trabalho mínimo para você começar a escrever por cima.

> Esta pasta é gerada. A fonte está em `src/`, no repositório
> <https://github.com/COPPE-UFRJ/CoppeTeX>, e a próxima geração apaga o que
> tiver sido mudado à mão aqui dentro. Versão @VERSAO@.

## Em 30 segundos

1. No Overleaf: **New Project → Upload Project** e solte este `.zip`.
2. Abra o `coppe-min-exemplo.tex` — é o único documento do projeto, e o
   Overleaf já o escolhe como principal.
3. Troque o conteúdo pelo seu e compile.

As duas primeiras linhas de todo trabalho da COPPE são:

```latex
\documentclass[dsc]{ufrj}   % dsc = tese; msc = dissertação
\usepackage{ufrj-coppe}
```

A classe `ufrj` implementa o Manual da UFRJ/SiBI; o estilo `ufrj-coppe` traz o
que é da COPPE — o nome do Instituto, os treze Programas, o logotipo e as
frases da Norma COPPE.

## O que o Overleaf precisa saber

**O compilador é o pdfLaTeX**, que já é o padrão. Em *Menu → Compiler*,
confirme `pdfLaTeX`; em *Menu → TeX Live version*, use a mais recente.

**A bibliografia é biblatex com biber**, e o Overleaf escolhe o biber sozinho
quando vê o `\addbibresource`. O `latexmkrc` deste projeto é quem manda as
listas de siglas, de símbolos, o glossário e o índice passarem pelo
`makeindex` — sem ele essas listas saem vazias. Não apague esse arquivo.

**Os logotipos estão em `logos/`**, e a classe sabe procurar ali.

## Diferente da pasta que se baixa do GitHub

Na distribuição comum (`dist-coppe`) os arquivos dos outros idiomas ficam em
subpastas, e quem escreve em inglês ou espanhol tem de trazê-los para a raiz.
**Aqui não**: todos os arquivos de idioma já estão na raiz do projeto, porque
no Overleaf não há razão para mexer em pastas. Escrever em outro idioma é só
trocar a opção da classe:

```latex
\documentclass[dsc,english]{ufrj}
```

## O exemplo completo e os manuais

Este projeto traz só o exemplo mínimo, para o Overleaf não ter dois documentos
principais e ficar em dúvida sobre qual compilar. O exemplo que usa **tudo** o
que a classe oferece — listas, glossário, índice, PDF/A, folha adicional da
CAPES, os cinco idiomas — e os manuais em PDF estão na distribuição completa:

<https://github.com/COPPE-UFRJ/CoppeTeX/tree/master/dist-coppe>

Lá estão também o `ufrj.pdf` (o manual da classe, com toda opção e todo
comando), o `ufrj-coppe.pdf` (o que é da COPPE) e o `manual.pdf` (a norma
demonstrada por um documento que a obedece).

## Licença

GNU General Public License versão 3 — veja o `COPYING.txt`.
