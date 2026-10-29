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

1. Copie **os arquivos da raiz desta pasta e a pasta `coppetex/`** para a
   pasta do seu trabalho.
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

Se o seu trabalho começou com `\documentclass{poli}`, ele continua compilando:
traga a `migracao/poli.cls` para a raiz, e ela carrega a `ufrj` com o estilo
`ufrj-poli`.

## A regra da arrumação

**Ao lado do seu `.tex` ficam só a classe, o estilo da Escola e os exemplos; o
resto da classe mora em `coppetex/`, e a própria classe sabe procurar lá.**
Não há nada a mover, nem para escrever em outro idioma, e compila de qualquer
jeito: `pdflatex` à mão, o botão do seu editor, `latexmk` ou Overleaf.

| Pasta | O que é | O que fazer |
|---|---|---|
| **raiz** | Classe, estilo da Escola, exemplos, base de referências | Copie para a pasta do trabalho. |
| `coppetex/` | Estilos de bibliografia, os arquivos de **todo** idioma e os logotipos | Copie junto, sem abrir. |
| `manuais/` | Os PDFs para ler | Nada. |
| `norma/` | A proposta de Norma 2026 da Escola, em PDF | Leitura. |
| `migracao/` | A `poli.cls` | Traga para a raiz só se o seu trabalho começa com `\documentclass{poli}` |

## Os arquivos da raiz

| Arquivo | Para que serve |
|---|---|
| `ufrj.cls` | A classe. |
| `ufrj-poli.sty` | O estilo da Escola Politécnica. |
| `ufrj.ist` | Ordenação das listas de siglas, abreviaturas e símbolos. Fica na raiz porque quem o lê é o `makeindex`, e não o LaTeX. |
| `latexmkrc` | Receita de compilação para `latexmk` e Overleaf: monta as listas sozinho. |
| `poli-min-exemplo.tex` | **Ponto de partida**: só o que a norma exige. |
| `poli-max-exemplo.tex` | Tudo o que a classe oferece, comentado. |
| `exemplo.bib` | Base de referências dos exemplos, com uma entrada de cada tipo do Manual. |
| `COPYING.txt` | Licença GNU GPL v3. |

Em `coppetex/` estão os estilos biblatex (`ufrj.dbx`, `ufrj.bbx`, `ufrj.cbx` e
os `ufrj-numeric`), os termos de bibliografia de cada idioma (`*-ufrj.lbx`),
os pacotes de idioma da classe (`ufrj-lang-*.def`) e, em `coppetex/logos/`, os
logotipos da UFRJ e da Escola.

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
arquivos da raiz e a pasta `coppetex/` junto com o seu `.tex`.

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
