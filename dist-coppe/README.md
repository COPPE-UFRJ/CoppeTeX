<!-- AVISO-CPGP:INICIO — apagar deste comentário até AVISO-CPGP:FIM depois da aprovação -->
> ## ⚠️ Versão nova, ainda não aprovada
>
> **Esta é a CoppeTeX 5.0, e ela ainda não foi aprovada** pela Comissão de
> Programas de Pós-Graduação (CPGP) da COPPE/UFRJ. Use-a para escrever e para
> experimentar, mas confirme com a secretaria do seu Programa antes de depositar
> um trabalho com ela.
<!-- AVISO-CPGP:FIM -->

# CoppeTeX para a COPPE — teses e dissertações

**Esta pasta é tudo o que você precisa para escrever uma tese ou dissertação da
COPPE/UFRJ em LaTeX.** Baixe só ela — ou o `.zip` do *release*, que é a mesma
coisa — e ignore o resto do repositório.

> Esta pasta é gerada. Não edite nada aqui dentro: a fonte está em `src/` no
> repositório <https://github.com/COPPE-UFRJ/CoppeTeX>, e a próxima geração
> apaga o que tiver sido mudado à mão.

## Em 30 segundos

1. Copie **todos os arquivos da raiz desta pasta, mais a pasta `logos/`**, para
   a pasta do seu trabalho.
2. Abra o `coppe-min-exemplo.tex` e troque o conteúdo pelo seu.
3. Compile com `latexmk -pdf coppe-min-exemplo` (ou pdflatex → biber → pdflatex
   → pdflatex).

As duas primeiras linhas de todo trabalho da COPPE são:

```latex
\documentclass[dsc]{ufrj}   % dsc = tese; msc = dissertação
\usepackage{ufrj-coppe}
```

A classe `ufrj` implementa o Manual da UFRJ/SiBI; o estilo `ufrj-coppe` traz o
que é da COPPE — o nome do Instituto, os treze Programas, o logotipo e as frases
da Norma COPPE.

## A regra da arrumação

**O que está na raiz funciona sem você mexer em nada. O que está numa subpasta
de idioma só funciona depois de você trazer o conteúdo dela para a raiz.** O
LaTeX procura a classe, os estilos e os `.lbx` ao lado do documento, e não
dentro de subpastas.

| Pasta | O que é | O que fazer |
|---|---|---|
| **raiz** | Classe, estilo da COPPE, biblatex, exemplos em português | Nada. Já funciona. |
| `logos/` | Logotipos da UFRJ e da COPPE | Copie junto. A classe procura aqui. |
| `manuais/` | Os PDFs para ler | Nada. |
| `norma/` | A Norma COPPE 2026, em PDF | Leitura. |
| `en/` | Exemplo em **inglês** | Copie o conteúdo para a raiz |
| `es/` | Exemplo em **espanhol** e os dois arquivos que ele exige | Copie o conteúdo para a raiz |
| `outraslinguas/` | Francês e italiano | Copie para a raiz; não são idiomas admitidos para redigir tese |
| `gerador/` | Gerador de trabalho novo (`coppetex-novo.bat`) | Rode se quiser começar de uma folha em branco |
| `migracao/` | Guias para quem começou com a versão 3 ou 4 | Leitura |

## Os arquivos da raiz

| Arquivo | Para que serve |
|---|---|
| `ufrj.cls` | A classe. |
| `ufrj-coppe.sty` | O estilo da COPPE, carregado logo depois da classe. |
| `coppe.cls` | Só para trabalho começado com `\documentclass{coppe}` (versão 4.1 ou anterior): carrega a `ufrj` e o `ufrj-coppe`. Trabalho novo não precisa dela. |
| `ufrj.dbx`, `ufrj.bbx`, `ufrj.cbx` | Estilos biblatex de bibliografia e citação, autor-data (ABNT, conforme o Manual). |
| `ufrj-numeric.bbx`, `ufrj-numeric.cbx` | O mesmo no sistema numérico (opção `numbers` da classe). |
| `brazilian-ufrj.lbx`, `english-ufrj.lbx` | Termos de bibliografia em português e inglês. Os dois são necessários em qualquer trabalho, por causa do *abstract*. |
| `ufrj.ist` | Ordenação das listas de siglas, abreviaturas e símbolos e do glossário. |
| `latexmkrc` | Receita de compilação para `latexmk` e Overleaf. |
| `coppe-min-exemplo.tex` | **Ponto de partida**: só o que a norma exige. |
| `coppe-max-exemplo.tex` | Tudo o que a classe oferece, comentado linha a linha. |
| `exemplo.bib` | Base de referências dos exemplos, com uma entrada de cada tipo do Manual. |
| `COPYING.txt` | Licença GNU GPL v3. |

## A bibliografia (biblatex)

A classe já carrega o biblatex com os estilos `ufrj` — você **não** escreve
`\usepackage{biblatex}`. Basta declarar a base e imprimir:

```latex
\addbibresource{referencias/minha-tese.bib}   % pode ficar numa subpasta
...
\printbibliography
```

- **Autor-data** é o padrão: `\citet{chave}` → Silva (2020);
  `\citep{chave}` → (SILVA, 2020). Para o *apud*, `\citetapud` e `\citepapud`.
- **Numérico**: passe a opção `numbers` à classe, `\documentclass[dsc,numbers]{ufrj}`.
  O Manual não admite o sistema numérico em trabalho com notas de rodapé.
- **Tipos de entrada**: além dos do biblatex, há os do Manual — `@dscthesis`,
  `@mscthesis`, `@tcc`, patentes, documentos jurídicos, audiovisuais etc. — e
  os campos podem ser escritos em português (`@livro`, `autor`, `titulo`,
  `edicao`). O `exemplo.bib` traz um de cada, com a referência como o Manual a
  imprime.
- **Compilação**: o backend é o **biber** (não o BibTeX). Sem rodar o biber, as
  citações saem em negrito com a chave.
- Os `.bib` podem morar numa subpasta (`referencias/`), e é o recomendado: com o
  caminho escrito, o biber não pega por engano um arquivo de mesmo nome da
  instalação do TeX.

O capítulo de bibliografia do `manuais/ufrj.pdf` tem todos os tipos, campos e
comandos de citação.

## Outros idiomas

- **Inglês**: copie o conteúdo de `en/` para a raiz; o documento é o
  `example_en.tex`.
- **Espanhol**: copie o conteúdo de `es/` para a raiz (exemplo, `spanish-ufrj.lbx`
  e `ufrj-lang-spanish.def`). O trabalho tem três resumos: português, inglês e
  espanhol.
- **Francês e italiano** compõem, mas não são admitidos pelo art. 57 da Resolução
  CEPG n.º 302/2024; os pacotes existem como demonstração.

## Como compilar

```
latexmk -pdf coppe-max-exemplo
```

ou, à mão: `pdflatex` → `biber` → `pdflatex` → `pdflatex`. As listas de siglas,
símbolos, o glossário e o índice passam pelo `makeindex`, que a classe roda
sozinha. Se o pdfTeX reclamar de *No room for a new \write*, instale o pacote
`morewrites` ou compile com `lualatex`.

No **Overleaf**, suba os arquivos da raiz e a pasta `logos/` junto com o seu
`.tex`; o `latexmkrc` já diz o que fazer.

Para **instalar de vez**, ponha os arquivos em `tex/latex/ufrj` da sua árvore
local do TeX e rode `texhash` (TeX Live) ou `initexmf --update-fndb` (MiKTeX).

## Antes de depositar

- O PDF sai em **PDF/A-2b** por padrão, como exige o item 2.2(d) do Manual.
- Inclua a ficha catalográfica real, gerada em
  <http://fichacatalografica.sibi.ufrj.br/> ou pedida à biblioteca do Programa:
  `\catalogcard{ficha.pdf}`.
- Confira a `norma/NORMA_COPPE_2026.pdf` e a lista de verificação no fim do
  `manuais/manual.pdf`.

## Se der problema

| Sintoma | Causa |
|---|---|
| `File 'ufrj-lang-spanish.def' not found` | Faltou trazer `es/` para a raiz. |
| `Programa 'PESC' nao declarado` | Faltou `\usepackage{ufrj-coppe}` depois do `\documentclass`. |
| Citações em negrito com a chave | Não rodou o biber. |
| `Cannot find 'exemplo.bib'` | O `.bib` não está onde o `\addbibresource` diz. |

Versão mais nova e *issues*: <https://github.com/COPPE-UFRJ/CoppeTeX>.

## Licença

GNU General Public License, versão 3 (`COPYING.txt`). As fontes comentadas
(`.dtx`) de tudo o que está aqui estão em `src/` no repositório.
