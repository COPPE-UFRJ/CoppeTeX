# CoppeTeX

Classe LaTeX para teses, dissertações e Projetos de Graduação da UFRJ, conforme
o *Manual para Elaboração e Normalização de Trabalhos Acadêmicos* da UFRJ/SiBI
(9.ª ed. rev., 2026), com os estilos da COPPE e da Escola Politécnica e estilos
biblatex ABNT. 

## O que eu baixo?

| Você é | Baixe | Comece por |
|---|---|---|
| Aluno da **COPPE** (tese ou dissertação) | [`dist-coppe/`](./dist-coppe) | [`dist-coppe/README.md`](./dist-coppe/README.md) |
| Aluno da **Escola Politécnica** (Projeto de Graduação) | [`dist-poli/`](./dist-poli) | [`dist-poli/README.md`](./dist-poli/README.md) |
| Quem só quer **referências ABNT com biblatex** em outro documento | [`dist-biblatex/`](./dist-biblatex) | [`dist-biblatex/README.md`](./dist-biblatex/README.md) |
| Quem quer ler a **norma** da unidade | [`normas/`](./normas) | `normas/norma-coppe/`, `normas/norma-poli/` |

Cada `dist-*` basta sozinha: tem a classe, os estilos, o biblatex, os logotipos,
os exemplos, os manuais em PDF e um README com as instruções de uso. O `.zip`
de cada uma está nos *releases*.

*Writing a thesis? Download only `dist-coppe/` (COPPE) or `dist-poli/` (Escola
Politécnica). Only want the ABNT biblatex styles? Take `dist-biblatex/`.*

## O repositório

| Pasta | O que é | Quem mexe |
|---|---|---|
| [`src/`](./src) | **Toda a fonte**: os três `.dtx`/`.ins`, o `manual.tex`, os logotipos, as normas em Word (`src/normas`), os READMEs e extras de cada distribuição (`src/distribuicao`) e o gerador de trabalho novo (`src/gerador`). Guia do programador em [`src/README.md`](./src/README.md). | Quem muda a classe |
| `build/` | Pasta de trabalho, fora do git: cópia das fontes, os arquivos que os `.ins` geram e os PDFs compilados. | Ninguém: é gerada |
| [`dist-coppe/`](./dist-coppe), [`dist-poli/`](./dist-poli), [`dist-biblatex/`](./dist-biblatex) | As distribuições. Geradas, versionadas, com arquivos repetidos entre elas de propósito. | Ninguém: são geradas |
| [`normas/`](./normas) | As normas mais recentes de cada unidade, em Word e PDF, geradas de `src/normas`. | Ninguém: é gerada |
| [`specs/`](./specs) | As especificações que a classe implementa: Manual UFRJ/SiBI, normas ABNT, modelos do SiBI/CAPES, Resolução 05/2012 da Poli. | Só se a especificação mudar |
| [`tests/`](./tests) | As três camadas de teste. | Quem muda a classe |
| [`tools/`](./tools) | O harness: gerador, painel, verificadores. Manual em [`tools/PAINEL.md`](./tools/PAINEL.md). | Quem muda a classe |
| [`claude/`](./claude) | Notas de trabalho, roteiros e histórico do desenvolvimento com o Claude. Nada aqui é distribuído. | — |
| `Beamer Template/` | Modelo de apresentação da COPPE (prof. Jean-David Caprace), iniciativa à parte. | — |

## Gerar tudo

Um comando, na raiz, refaz as três distribuições e as normas a partir de `src/`:

```bat
coppetex.bat --distribuir
```

Ele roda, nesta ordem: o docstrip dos três `.ins` em `build/`, a compilação dos
PDFs (`tools/build-check.ps1`), a conversão das normas de Word para PDF e a
montagem das `dist-*`. As listas do que vai em cada distribuição estão num lugar
só, [`tools/distribuicoes.py`](./tools/distribuicoes.py), que também roda
sozinho em qualquer sistema:

```
python tools/distribuicoes.py              # docstrip + normas + montagem
python tools/distribuicoes.py --pacote     # um .zip por distribuição
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
_Último build exportado: 29/10/2026 12:48 (build/, dist-coppe, dist-poli, dist-biblatex, Overleaf e CTAN)._
