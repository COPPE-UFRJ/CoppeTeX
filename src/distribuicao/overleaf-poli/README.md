# CoppeTeX no Overleaf — Projeto de Graduação da Escola Politécnica

**Este `.zip` é um projeto do Overleaf pronto.** Ele tem a classe, o estilo da
Escola Politécnica, os estilos de bibliografia, os logotipos, uma base de
referências e um Projeto de Graduação mínimo para você começar a escrever por
cima.

> A norma da Escola em vigor ainda é o Anexo da Resolução n.º 05/2012. Este
> projeto segue o Manual da UFRJ/SiBI (2026) e a proposta de Norma 2026 da
> Escola. Confirme com a coordenação do seu Curso antes de depositar.

> Esta pasta é gerada. A fonte está em `src/`, no repositório
> <https://github.com/COPPE-UFRJ/CoppeTeX>, e a próxima geração apaga o que
> tiver sido mudado à mão aqui dentro. Versão @VERSAO@.

## Em 30 segundos

1. No Overleaf: **New Project → Upload Project** e solte este `.zip`.
2. Abra o `poli-min-exemplo.tex` e confira, em *Menu → Main document*, que é
   ele o documento principal (o projeto traz também o exemplo completo).
3. Troque o conteúdo pelo seu e compile.

As primeiras linhas de todo Projeto de Graduação da Escola são:

```latex
\documentclass[grad]{ufrj}
\usepackage{ufrj-poli}          % ou [times] / [arial] para fixar a letra
...
\department{ECI}                % a sigla do seu Curso
```

A classe `ufrj` implementa o Manual da UFRJ/SiBI; o estilo `ufrj-poli` traz o
que é da Escola — a marca, os Cursos com o título que cada um confere e as
frases da norma. A lista das siglas aceitas por `\department` está no
`manuais/ufrj-poli.pdf` e no `manuais/poli-quickref.pdf`.

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

- `poli-min-exemplo.tex` — **o ponto de partida**, só o que a norma exige;
- `poli-max-exemplo.tex` — tudo o que a classe oferece num Projeto de
  Graduação — listas, glossário, índice, quadro, tabela, programa —,
  comentado, para consultar.

O Overleaf compila **um** deles, o *documento principal*. Confira em
*Menu → Main document* que é o `poli-min-exemplo.tex` (ou o seu trabalho, se
você renomeá-lo); para ver o exemplo completo, troque ali e compile.

## Outros idiomas

Os arquivos de todo idioma já estão em `coppetex/`. Escrever em outro idioma é
só trocar a opção da classe:

```latex
\documentclass[grad,english]{ufrj}
```

## Os manuais

Os manuais em PDF estão na pasta `manuais/` deste projeto: o `ufrj.pdf` (o
manual da classe, com toda opção e todo comando), o `ufrj-poli.pdf` (o que é
da Escola), as duas folhas de consulta rápida (`ufrj-quickref.pdf` e
`poli-quickref.pdf`) e os dois exemplos já compilados. Nenhum documento
depende dessa pasta; apague-a se quiser um projeto mais leve.

## Pedidos e defeitos

O projeto mora no GitHub: <https://github.com/COPPE-UFRJ/CoppeTeX>.

Para **pedir uma melhoria** ou **avisar de um defeito**, abra uma *issue* em
<https://github.com/COPPE-UFRJ/CoppeTeX/issues>. Num defeito, diga a versão
da classe (a linha `Document Class: ufrj` do `.log`), mande o menor `.tex` que o
reproduz e, se houver, o `.log` da compilação.

## Licença

GNU General Public License versão 3 — veja o `COPYING.txt`.
