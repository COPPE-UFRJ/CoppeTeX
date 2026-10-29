# CoppeTeX para o Instituto de Computação — PPGI e Ciência da Computação

**Esta pasta é tudo o que você precisa para escrever, em LaTeX, a dissertação
ou a tese do Programa de Pós-Graduação em Informática (PPGI) ou o trabalho de
conclusão do Bacharelado em Ciência da Computação do Instituto de
Computação/UFRJ.** Baixe só ela — ou o `.zip` do *release* — e ignore o resto
do repositório.

> Os dados do Instituto — os nomes, as siglas, a frase da natureza e o
> logotipo do PPGI — vêm do Projeto Jacurutu, o modelo LaTeX mantido no PPGI
> (<https://github.com/projeto-jacurutu/jacurutu-latex>). A formatação é a do
> Manual da UFRJ/SiBI (2026).

> Esta pasta é gerada. Não edite nada aqui dentro: a fonte está em `src/` no
> repositório <https://github.com/COPPE-UFRJ/CoppeTeX>.

## Em 30 segundos

1. Copie **os arquivos da raiz desta pasta e a pasta `coppetex/`** para a
   pasta do seu trabalho.
2. Abra o `ic-min-exemplo.tex` e troque o conteúdo pelo seu.
3. Compile com `latexmk -pdf ic-min-exemplo` (ou pdflatex → biber → pdflatex
   → pdflatex).

As primeiras linhas de uma dissertação ou tese do PPGI são:

```latex
\documentclass[msc]{ufrj}       % msc = dissertação; dsc = tese
\usepackage{ufrj-ic}
...
\department{PPGI}
```

e as de um trabalho de conclusão do Bacharelado em Ciência da Computação:

```latex
\documentclass[grad]{ufrj}
\usepackage{ufrj-ic}
...
\department{BCC}
```

A classe `ufrj` implementa o Manual da UFRJ/SiBI; o estilo `ufrj-ic` traz o
que é do Instituto. No PPGI, a capa e a natureza nomeiam os dois institutos
que oferecem o Programa — o Instituto de Computação e o Instituto Tércio
Pacitti de Aplicações e Pesquisas Computacionais — e a capa traz o logotipo do
PPGI. Na graduação, o trabalho é apresentado ao Instituto de Computação, e o
logotipo é o do curso: ponha o arquivo `ic-logo.pdf` em `coppetex/logos/` (a
distribuição ainda não o traz; sem ele, a capa sai só com o logotipo da UFRJ).

## A regra da arrumação

**Ao lado do seu `.tex` ficam só a classe, o estilo do Instituto e os
exemplos; o resto da classe mora em `coppetex/`, e a própria classe sabe
procurar lá.** Não há nada a mover, nem para escrever em outro idioma, e
compila de qualquer jeito: `pdflatex` à mão, o botão do seu editor, `latexmk`
ou Overleaf.

| Pasta | O que é | O que fazer |
|---|---|---|
| **raiz** | Classe, estilo do Instituto, exemplos, base de referências | Copie para a pasta do trabalho. |
| `coppetex/` | Estilos de bibliografia, os arquivos de **todo** idioma e os logotipos | Copie junto, sem abrir. |
| `manuais/` | Os PDFs para ler | Nada. |

## Os arquivos da raiz

| Arquivo | Para que serve |
|---|---|
| `ufrj.cls` | A classe. |
| `ufrj-ic.sty` | O estilo do Instituto de Computação. |
| `ufrj.ist` | Ordenação das listas de siglas, abreviaturas e símbolos. Fica na raiz porque quem o lê é o `makeindex`, e não o LaTeX. |
| `latexmkrc` | Receita de compilação para `latexmk` e Overleaf: monta as listas sozinho. |
| `ic-min-exemplo.tex` | **Ponto de partida**: uma dissertação com só o que a norma exige. |
| `ic-max-exemplo.tex` | Uma tese com tudo o que a classe oferece, comentada. |
| `exemplo.bib` | Base de referências dos exemplos, com uma entrada de cada tipo do Manual. |
| `COPYING.txt` | Licença GNU GPL v3. |

Em `coppetex/` estão os estilos biblatex (`ufrj.dbx`, `ufrj.bbx`, `ufrj.cbx` e
os `ufrj-numeric`), os termos de bibliografia de cada idioma (`*-ufrj.lbx`),
os pacotes de idioma da classe (`ufrj-lang-*.def`) e, em `coppetex/logos/`, os
logotipos da UFRJ e do PPGI.

## A bibliografia (biblatex)

A classe já carrega o biblatex com os estilos `ufrj` — não escreva
`\usepackage{biblatex}`. Basta declarar a base e imprimir:

```latex
\addbibresource{referencias/minha-tese.bib}
...
\printbibliography
```

- **Autor-data** é o padrão: `\citet{chave}` → Silva (2020); `\citep{chave}` →
  (SILVA, 2020). Para o *apud*, `\citetapud` e `\citepapud`.
- **Numérico**: `\documentclass[msc,numbers]{ufrj}`. Não use com notas de rodapé.
- **Tipos de entrada** do Manual (`@tcc`, `@mscthesis`, patentes, documentos
  jurídicos…) e campos em português (`@livro`, `autor`, `titulo`). Veja o
  `exemplo.bib`.
- O backend é o **biber**, não o BibTeX.

## Como compilar

```
latexmk -pdf ic-max-exemplo
```

ou `pdflatex` → `biber` → `pdflatex` → `pdflatex`. No **Overleaf**, suba os
arquivos da raiz e a pasta `coppetex/` junto com o seu `.tex` — ou use o
projeto do Overleaf do Instituto, que já vem pronto.

## Antes de depositar

- O PDF sai em **PDF/A-2b** por padrão (item 2.2(d) do Manual).
- Inclua a ficha catalográfica real, de <http://fichacatalografica.sibi.ufrj.br/>:
  `\catalogcard{ficha.pdf}`.

## Pedidos e defeitos

O projeto mora no GitHub: <https://github.com/COPPE-UFRJ/CoppeTeX>.

Para **pedir uma melhoria** ou **avisar de um defeito**, abra uma *issue* em
<https://github.com/COPPE-UFRJ/CoppeTeX/issues>. Num defeito, diga a versão
da classe (a linha `Document Class: ufrj` do `.log`), mande o menor `.tex` que o
reproduz e, se houver, o `.log` da compilação.

## Licença

GNU General Public License, versão 3 (`COPYING.txt`). As fontes comentadas
(`.dtx`) estão em `src/` no repositório.
