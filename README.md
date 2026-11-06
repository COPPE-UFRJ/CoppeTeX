# CoppeTeX

Classe LaTeX para teses, dissertações e Projetos de Graduação da UFRJ, conforme
o *Manual para Elaboração e Normalização de Trabalhos Acadêmicos* da UFRJ/SiBI
(9.ª ed. rev., 2026), com os estilos da COPPE e da Escola Politécnica e estilos
biblatex ABNT.

## O que eu baixo?

Pegue **só a sua distribuição** — e ignore o resto do repositório. Cada uma vem
de dois jeitos, com o mesmo conteúdo: a **pasta** `dist-…/` (para navegar e ler
no GitHub) e o **arquivo** `dist-….zip` no raiz (um download só, e já pronto
para subir no Overleaf).

| Você é | Baixe a pasta **ou** o `.zip` | Comece por |
|---|---|---|
| Aluno da **COPPE** (tese ou dissertação) | [`dist-coppe/`](./dist-coppe) ou [`dist-coppe.zip`](./dist-coppe.zip) | [`dist-coppe/README.md`](./dist-coppe/README.md) |
| Aluno da **Escola Politécnica** (Projeto de Graduação) | [`dist-poli/`](./dist-poli) ou [`dist-poli.zip`](./dist-poli.zip) | [`dist-poli/README.md`](./dist-poli/README.md) |
| Quem só quer **referências ABNT com biblatex** em outro documento | [`dist-biblatex/`](./dist-biblatex) ou [`dist-biblatex.zip`](./dist-biblatex.zip) | [`dist-biblatex/README.md`](./dist-biblatex/README.md) |

A **norma** de cada unidade não vai na distribuição; ela está no repositório, em
`specs/` e na fonte `src/normas/`.

Cada distribuição basta sozinha: tem a classe, os estilos, o biblatex, os
logotipos, os exemplos, os manuais em PDF e um README com as instruções de uso.

Há duas formas de usar, e as duas próximas seções são o passo a passo de cada
uma: **no Overleaf**, suba o `.zip`; **no seu computador** (Windows, Mac ou
Linux), extraia o `.zip` (ou copie a pasta) e compile.

*Writing a thesis? Download only `dist-coppe` (COPPE) or `dist-poli` (Escola
Politécnica) — the folder or the `.zip`. Only want the ABNT biblatex styles?
Take `dist-biblatex`.*

## Usando no Overleaf

O Overleaf abre um `.zip` como um projeto pronto. É o caminho mais simples, e
não exige instalar nada.

1. Baixe o `.zip` da sua distribuição no raiz deste repositório — por exemplo
   **[`dist-coppe.zip`](./dist-coppe.zip)** para a COPPE (ou
   [`dist-poli.zip`](./dist-poli.zip) para a Poli).
2. No Overleaf, clique em **New Project → Upload Project** e solte o `.zip`. O
   que estiver na raiz do `.zip` vira a raiz do projeto.
3. Em **Menu → Compiler**, confirme **pdfLaTeX**; em **Menu → TeX Live version**,
   use a mais recente.
4. Abra o `coppe-min-exemplo.tex` (o ponto de partida) e, em
   **Menu → Main document**, confirme que é ele o documento principal — o
   projeto traz também o `coppe-max-exemplo.tex`, com tudo o que a classe
   oferece. Troque o conteúdo pelo seu e compile.

As duas primeiras linhas de todo trabalho da COPPE são:

```latex
\documentclass[dsc]{ufrj}   % dsc = tese; msc = dissertação
\usepackage{ufrj-coppe}
```

**Não apague o `latexmkrc`** nem a pasta `coppetex/`: o `latexmkrc` é quem faz
as listas de siglas, de símbolos, o glossário e o índice passarem pelo
`makeindex` (sem ele saem vazias), e a pasta `coppetex/` tem os estilos de
bibliografia, os arquivos de todo idioma e os logotipos, que a classe sabe
procurar ali. A bibliografia é biblatex com **biber**, que o Overleaf escolhe
sozinho quando vê o `\addbibresource`.

Para escrever em inglês ou espanhol, basta a opção da classe
(`\documentclass[dsc,english]{ufrj}`); nada a mover.

## Usando no Windows, Mac e Linux

Para compilar na sua máquina você precisa de uma distribuição TeX instalada:

- **Windows** — [MiKTeX](https://miktex.org) (ou TeX Live). O `latexmk` pede o
  **Perl**: no Windows, instale o [Strawberry Perl](https://strawberryperl.com)
  se for usá-lo.
- **macOS** — [MacTeX](https://tug.org/mactex/).
- **Linux** — TeX Live, pelo gerenciador de pacotes da distribuição
  (`texlive-full` cobre tudo) ou do instalador oficial.

Passo a passo:

1. **Extraia** o `.zip` da sua distribuição (ou copie a pasta `dist-…/` inteira)
   para a pasta onde vai escrever o trabalho. Mantenha **os arquivos da raiz e a
   pasta `coppetex/` juntos** — a classe procura os estilos e os logotipos ali
   ao lado do documento; não mova nada para dentro de subpastas.
2. **Abra o `coppe-min-exemplo.tex`** (o ponto de partida, só o que a norma
   exige) e troque o conteúdo pelo seu. O `coppe-max-exemplo.tex` mostra tudo o
   que a classe oferece, comentado linha a linha.
3. **Compile.** O jeito recomendado, que resolve bibliografia, listas, glossário
   e índice sozinho:

   ```
   latexmk -pdf coppe-min-exemplo
   ```

   À mão, a sequência é: `pdflatex` → `biber` → `pdflatex` → `pdflatex`. O
   compilador é o **pdfLaTeX** e o backend da bibliografia é o **biber** (não o
   BibTeX) — sem rodar o biber, as citações saem em negrito com a chave.

O PDF sai em **PDF/A-2b** por padrão, que é o formato que o depósito exige
(Manual 2.2d). Antes de depositar, inclua a ficha catalográfica real, gerada em
<http://fichacatalografica.sibi.ufrj.br/>, com `\catalogcard{ficha.pdf}`.

Problemas comuns (erro de `coppetex/` não copiada, `\usepackage{ufrj-coppe}`
esquecido, biber não rodado) estão na tabela "Se der problema" do
[`dist-coppe/README.md`](./dist-coppe/README.md). Se o pdfTeX reclamar de
*No room for a new \write*, instale o pacote `morewrites` ou compile com
`lualatex`.

## Os manuais

Cada distribuição traz, na pasta `manuais/` (e no projeto do Overleaf), os PDFs
abaixo. Para quem está começando, **comece pelo guia**.

| Manual | O que é | Para quem |
|---|---|---|
| **`coppe-guia.pdf`** / **`poli-guia.pdf`** | **Guia Passo a Passo para Usar o CoppeTeX**: como montar o trabalho (estrutura de pastas e arquivos, um capítulo por arquivo) e o que preencher no `.tex`. **Comece por aqui.** | Quem vai escrever |
| `manual.pdf` | A **norma** da UFRJ/SiBI (9.ª ed., 2026) demonstrada: um documento que obedece a tudo o que enuncia — margens, paginação, legendas, citações, referências. | Quem quer saber como o trabalho tem de sair |
| `ufrj.pdf` | O **manual da classe**: todo comando e toda opção, um a um. | Consulta e referência |
| `ufrj-coppe.pdf` / `ufrj-poli.pdf` | O **manual do estilo da unidade**: o que é da COPPE (ou da Escola Politécnica) — Programas/cursos, logotipo, frases da norma. | Consulta da unidade |
| `ufrj-quickref.pdf` + `coppe-quickref.pdf` / `poli-quickref.pdf` | As **folhas de consulta rápida**, de uma página: a da classe e a de cada unidade. | Consulta rápida |
| `coppe-min-exemplo.pdf` / `coppe-max-exemplo.pdf` (e os da Poli) | Os **exemplos já compilados**: o mínimo que a norma exige e tudo o que a classe oferece. | Ver o resultado pronto |

O guia, o manual da norma e os exemplos são, eles mesmos, trabalhos compostos
com a classe: o que ensinam, fazem.

## O repositório

Para quem **mantém a classe** (o aluno não precisa disto):

| Pasta | O que é | Quem mexe |
|---|---|---|
| [`src/`](./src) | **Toda a fonte**: os três `.dtx`/`.ins`, o `manual.tex`, os logotipos, as normas em Word (`src/normas`), os READMEs e extras de cada distribuição (`src/distribuicao`) e o gerador de trabalho novo (`src/gerador`). Guia do programador em [`src/README.md`](./src/README.md). | Quem muda a classe |
| `build/` | Pasta de trabalho, fora do git: cópia das fontes, os arquivos que os `.ins` geram e os PDFs compilados. | Ninguém: é gerada |
| [`dist-coppe/`](./dist-coppe), [`dist-poli/`](./dist-poli), [`dist-biblatex/`](./dist-biblatex) e os `dist-*.zip` do raiz | As distribuições, abertas (pasta) e fechadas (`.zip`). Geradas, versionadas, com arquivos repetidos entre elas de propósito. | Ninguém: são geradas |
| `src/normas/` | A **fonte** das normas (Word). A classe gera delas a norma em PDF, que vai só dentro de cada `dist-*/norma/`; não há `normas/` versionada no raiz. | Quem atualiza a norma |
| [`specs/`](./specs) | As especificações que a classe implementa: Manual UFRJ/SiBI, normas ABNT, modelos do SiBI/CAPES, Resolução 05/2012 da Poli. | Só se a especificação mudar |
| [`tests/`](./tests) | As três camadas de teste. | Quem muda a classe |
| [`tools/`](./tools) | O harness: gerador, painel, verificadores. Manual em [`tools/PAINEL.md`](./tools/PAINEL.md). | Quem muda a classe |
| [`claude/`](./claude) | Notas de trabalho, roteiros e histórico do desenvolvimento com o Claude. Nada aqui é distribuído. | — |
| `Beamer Template/` | Modelo de apresentação da COPPE (prof. Jean-David Caprace), iniciativa à parte. | — |

## Gerar tudo

Um comando, na raiz, refaz as três distribuições (a pasta `dist-*/` **e** o
`dist-*.zip` no raiz) e as normas a partir de `src/`:

```bat
coppetex.bat --distribuir
```

Ele roda, nesta ordem: o docstrip dos três `.ins` em `build/`, a compilação dos
PDFs (`tools/build-check.ps1`), a conversão das normas de Word para PDF, a
montagem das `dist-*` e o fechamento dos `dist-*.zip` no raiz. As listas do que
vai em cada distribuição estão num lugar só,
[`tools/distribuicoes.py`](./tools/distribuicoes.py), que também roda sozinho em
qualquer sistema:

```
python tools/distribuicoes.py              # docstrip + normas + montagem + zips no raiz
python tools/distribuicoes.py --zip        # só refaz os dist-*.zip do raiz
python tools/distribuicoes.py --pacote     # os zips de release, versionados, em build/pacotes
```

Sem argumento, `coppetex.bat` abre o painel do desenvolvedor, com testes,
verificadores e versão. Antes de marcar uma versão: `coppetex.bat --tudo`.

> **A fonte é `src/`, e só ela.** Nada em `build/`, `dist-*` ou `normas/` é
> editado à mão: a próxima geração apaga a edição.

## Required LaTeX packages

`ufrj.cls` is built on the standard **`book`** class (`12pt, a4paper,
twoside`) and loads the stock CTAN packages below with `\RequirePackage`.
A full TeX Live or MiKTeX install already has every one of them, so the
list matters only for a minimal install — or when you want to know which
commands are already in scope (you do **not** need to `\usepackage` any of
these in your thesis). Bracketed text is the options the class passes.

**Engine & encoding**

- `iftex` — detect the engine (pdfTeX / LuaTeX / XeTeX) to branch setup.
- `inputenc` [`utf8`] — UTF-8 input; loaded **only under pdfTeX** (Unicode
  engines read UTF-8 natively).
- `fontenc` [`T1`] — T1 font encoding (accented glyphs, correct hyphenation).

**Math & symbols**

- `amsmath` — AMS math environments.
- **No math fonts.** Since 4.1 the math font is the author's choice: load
  `amssymb` under pdfTeX, or `unicode-math` with an OpenType math font under
  LuaTeX, in your preamble. The examples and the empty-document generator
  carry a block that picks by engine.

**Page layout & spacing**

- `geometry` — A4 two-side margins, binding offset, header height.
- `fancyhdr` — running headers and footers.
- `titlesec` — chapter and section title formatting.
- `setspace` — one-and-a-half (or, with `doublespacing`, double) line spacing.

**Lists, tables & rules**

- `enumitem` — customizable list spacing and labels.
- `tabularx` — tables with auto-width columns.
- `booktabs` — professional horizontal rules (`\toprule`, `\midrule`, …).
- `longtable` — tables that break across pages.

**Floats, graphics & captions**

- `graphicx` — include images.
- `float` — float placement control (e.g. `[H]`).
- `caption` — caption typography (ABNT caption-on-top).
- `subcaption` — subfigures and subtables.

**Code, verbatim & algorithms**

- `listings` — source-code listings.
- `fancyvrb` — extended verbatim.
- `algorithm2e` [`linesnumbered, lined, algochapter, ruled`] — typeset
  algorithms; the natural-language option follows the main language.

**Bibliography, quotations & language**

- `babel` — multilingual typesetting; the language options are computed
  from the main/foreign language slots.
- `csquotes` — context-sensitive quotation marks (recommended companion of
  biblatex).
- `biblatex` [`backend=biber`] — bibliography engine and the ABNT `ufrj`
  styles (`ufrj` / `ufrj-numeric`). The backend is **biber**, not bibtex.

**Hyperlinks**

- `hyperref` — clickable cross-references, PDF bookmarks and metadata.

**Low-level utilities**

- `etoolbox` — e-TeX programming toolkit.
- `ltxcmds` — low-level command helpers (`\ltx@ifpackageloaded`, …).
- `ifthen` — `\ifthenelse` conditionals.
- `hyphenat` — hyphenation control (`\nohyphens`, used on the cover).
- `lastpage` — `\pageref{LastPage}` for the cataloging page count.
- `hologo` — TeX-family logos (`\hologo{LaTeX}`, …).
- `xcolor` — colour support (used by `listings` and `hyperref`).

Everything is loaded unconditionally except `inputenc` (pdfTeX
only) and the option-driven `biblatex` style choice (`numbers` selects the
numeric `ufrj-numeric` style). The language packs add no packages — only
the string files described above.

## Pedidos e defeitos

O projeto mora no GitHub: <https://github.com/COPPE-UFRJ/CoppeTeX>.

Para **pedir uma melhoria** ou **avisar de um defeito**, abra uma *issue* em
<https://github.com/COPPE-UFRJ/CoppeTeX/issues>. Num defeito, diga a versão
da classe (a linha `Document Class: ufrj` do `.log`), mande o menor `.tex` que o
reproduz e, se houver, o `.log` da compilação.

## Licença

GNU General Public License, versão 3 (`COPYING.txt`).

<!-- registro de build -->
_Último build exportado: 06/11/2026 — versão 5.0 (build/, dist-coppe, dist-poli, dist-biblatex, os `.zip` do raiz, o site `docs/` e o pacote CTAN)._
