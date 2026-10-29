# CoppeTeX no Overleaf — tese ou dissertação da COPPE

**Este `.zip` é um projeto do Overleaf pronto.** Ele tem a classe, o estilo da
COPPE, os estilos de bibliografia, os logotipos, uma base de referências e um
trabalho mínimo para você começar a escrever por cima.

> Esta pasta é gerada. A fonte está em `src/`, no repositório
> <https://github.com/COPPE-UFRJ/CoppeTeX>, e a próxima geração apaga o que
> tiver sido mudado à mão aqui dentro. Versão @VERSAO@.

## Em 30 segundos

1. No Overleaf: **New Project → Upload Project** e solte este `.zip`.
2. Abra o `coppe-min-exemplo.tex` e confira, em *Menu → Main document*, que
   é ele o documento principal (o projeto traz também o exemplo completo).
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

**O que é da classe está em `coppetex/`** — estilos de bibliografia, os
arquivos de todo idioma e os logotipos —, e a classe sabe procurar ali. Não
mexa nessa pasta; o seu trabalho e as suas figuras ficam fora dela.

## Os dois exemplos

O projeto traz dois documentos:

- `coppe-min-exemplo.tex` — **o ponto de partida**, só o que a norma exige;
- `coppe-max-exemplo.tex` — tudo o que a classe oferece — listas, glossário,
  índice, PDF/A, folha adicional da CAPES —, comentado linha a linha, para
  consultar.

O Overleaf compila **um** deles, o *documento principal*. Confira em
*Menu → Main document* que é o `coppe-min-exemplo.tex` (ou o seu trabalho, se
você renomeá-lo); para ver o exemplo completo, troque ali e compile.

## Outros idiomas

Os arquivos de todo idioma já estão em `coppetex/`. Escrever em outro idioma é
só trocar a opção da classe:

```latex
\documentclass[dsc,english]{ufrj}
```

## Os manuais

Os manuais em PDF estão na pasta `manuais/` deste projeto: o `ufrj.pdf` (o
manual da classe, com toda opção e todo comando), o `ufrj-coppe.pdf` (o que é
da COPPE), o `manual.pdf` (a norma demonstrada por um documento que a
obedece), as duas folhas de consulta rápida (`ufrj-quickref.pdf` e
`coppe-quickref.pdf`) e os dois exemplos já compilados. Nenhum documento
depende dessa pasta; apague-a se quiser um projeto mais leve.

## Pedidos e defeitos

O projeto mora no GitHub: <https://github.com/COPPE-UFRJ/CoppeTeX>.

Para **pedir uma melhoria** ou **avisar de um defeito**, abra uma *issue* em
<https://github.com/COPPE-UFRJ/CoppeTeX/issues>. Num defeito, diga a versão
da classe (a linha `Document Class: ufrj` do `.log`), mande o menor `.tex` que o
reproduz e, se houver, o `.log` da compilação.

## Licença

GNU General Public License versão 3 — veja o `COPYING.txt`.
