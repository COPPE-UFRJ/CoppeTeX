# CoppeTeX para a Escola Politécnica — Projeto de Graduação

**Esta pasta é tudo o que você precisa para escrever o Projeto de Graduação da
Escola Politécnica/UFRJ em LaTeX.** Baixe só ela — ou o `.zip` do *release* — e
ignore o resto do repositório.

> A norma da Escola em vigor ainda é o Anexo da Resolução n.º 05/2012. Esta
> distribuição segue o Manual da UFRJ/SiBI (2026) e a proposta de Norma 2026 da
> Escola, em `norma/`. Confirme com a coordenação do seu Curso antes de
> depositar.

> Esta pasta é gerada. Não edite nada aqui dentro: a fonte está em `src/` no
> repositório <https://github.com/COPPE-UFRJ/CoppeTeX>.

## Em 30 segundos

1. Copie **todos os arquivos da raiz desta pasta, mais a pasta `logos/`**, para
   a pasta do seu trabalho.
2. Abra o `poli-min-exemplo.tex` e troque o conteúdo pelo seu.
3. Compile com `latexmk -pdf poli-min-exemplo` (ou pdflatex → biber → pdflatex
   → pdflatex).

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

Se o seu trabalho começou com `\documentclass{poli}`, ele continua compilando: a
`poli.cls` desta pasta carrega a `ufrj` com o estilo `ufrj-poli`.

## A regra da arrumação

**O que está na raiz funciona sem você mexer em nada. O que está numa subpasta
de idioma só funciona depois de você trazer o conteúdo dela para a raiz.**

| Pasta | O que é | O que fazer |
|---|---|---|
| **raiz** | Classe, estilo da Escola, biblatex, exemplos | Nada. Já funciona. |
| `logos/` | Logotipos da UFRJ e da Escola Politécnica | Copie junto. |
| `manuais/` | Os PDFs para ler | Nada. |
| `norma/` | A proposta de Norma 2026 da Escola, em PDF | Leitura. |
| `es/` | Os dois arquivos para escrever em espanhol | Copie para a raiz |
| `outraslinguas/` | Francês e italiano | Copie para a raiz; não são idiomas admitidos |

## Os arquivos da raiz

| Arquivo | Para que serve |
|---|---|
| `ufrj.cls` | A classe. |
| `ufrj-poli.sty` | O estilo da Escola Politécnica. |
| `poli.cls` | Só para trabalho começado com `\documentclass{poli}`. |
| `ufrj.dbx`, `ufrj.bbx`, `ufrj.cbx` | Estilos biblatex autor-data (ABNT, conforme o Manual). |
| `ufrj-numeric.bbx`, `ufrj-numeric.cbx` | O mesmo no sistema numérico (opção `numbers` da classe). |
| `brazilian-ufrj.lbx`, `english-ufrj.lbx` | Termos de bibliografia em português e inglês; os dois são necessários, por causa do *abstract*. |
| `ufrj.ist` | Ordenação das listas de siglas, abreviaturas e símbolos. |
| `latexmkrc` | Receita de compilação para `latexmk` e Overleaf. |
| `poli-min-exemplo.tex` | **Ponto de partida**: só o que a norma exige. |
| `poli-max-exemplo.tex` | Tudo o que a classe oferece, comentado. |
| `exemplo.bib` | Base de referências dos exemplos, com uma entrada de cada tipo do Manual. |
| `COPYING.txt` | Licença GNU GPL v3. |

## A bibliografia (biblatex)

A classe já carrega o biblatex com os estilos `ufrj` — não escreva
`\usepackage{biblatex}`. Basta declarar a base e imprimir:

```latex
\addbibresource{referencias/meu-projeto.bib}
...
\printbibliography
```

- **Autor-data** é o padrão: `\citet{chave}` → Silva (2020); `\citep{chave}` →
  (SILVA, 2020). Para o *apud*, `\citetapud` e `\citepapud`.
- **Numérico**: `\documentclass[grad,numbers]{ufrj}`. Não use com notas de rodapé.
- **Tipos de entrada** do Manual (`@tcc`, `@mscthesis`, patentes, documentos
  jurídicos…) e campos em português (`@livro`, `autor`, `titulo`). Veja o
  `exemplo.bib`.
- O backend é o **biber**, não o BibTeX.

## Como compilar

```
latexmk -pdf poli-max-exemplo
```

ou `pdflatex` → `biber` → `pdflatex` → `pdflatex`. No **Overleaf**, suba os
arquivos da raiz e a pasta `logos/` junto com o seu `.tex`.

## Antes de depositar

- O PDF sai em **PDF/A-2b** por padrão (item 2.2(d) do Manual).
- Inclua a ficha catalográfica real, de <http://fichacatalografica.sibi.ufrj.br/>:
  `\catalogcard{ficha.pdf}`.

## Licença

GNU General Public License, versão 3 (`COPYING.txt`). As fontes comentadas
(`.dtx`) estão em `src/` no repositório.
