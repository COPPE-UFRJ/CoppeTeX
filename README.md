# CoppeTeX

This project provides a LaTeX document class suitable for writing academic
dissertations and thesis according to the formatting rules established by the
Alberto Luiz Coimbra Institute for Graduate Studies and Research in Engineering
(COPPE/UFRJ).

The 'coppe' class contains a minimalist set of macro commands which allows its
users to create the required textual elements following the COPPE/UFRJ
dissertation/thesis guidelines. Among these elements, there are a front cover,
a title page, cataloging details, native and foreign languages abstracts, table
of contents, and list of bibliographic references.

Although it is tied to the COPPE/UFRJ guidelines, it can be easily ported to other institutions.

This version follows the [document](https://registro.daac.coppe.ufrj.br/wp-content/uploads/2020/09/Normas-de-Elaboracao.pdf):

> Original: Norma para a Elaboração Gráfica de Teses/Dissertações COPPE/UFRJ
>  Aprovada pela CPGP em 15 de julho de 2008 
> Com correção no Anexo III, páginas 19 e 20, em 01/10/2009
> (Revisada em 10/09/2010)
> (Revisada em 26/11/2019 – Alteração da Folha Aprovação, Anexo III, páginas 22 e 23) 


## `nlinguas` branch — proposal for CPGP (v4.1)

This branch (`nlinguas`) carries CoppeTeX **4.1**, submitted for evaluation by
the Comissão de Programas de Pós-Graduação (CPGP) of COPPE/UFRJ. Subject to
CPGP review and approval, it becomes the next official release of the `coppe`
class. **`master` holds the state the COPPE has approved and does not move
before that vote.**

Two things are proposed together:

- **The norm.** [`NORMA_COPPE_2026.md`](./NORMA_COPPE_2026.md) stops describing
  the format and adopts the UFRJ/SiBI *Manual para Elaboração e Normalização de
  Trabalhos Acadêmicos*, **9th edition revised (2026)**, in full. What is left
  is thirteen sections recording only where COPPE specializes the Manual —
  each labelled *Escolha*, *Dado próprio*, *Acréscimo* or *Reafirmação* — plus
  the logomarks, the list of the thirteen Programas, and the three-abstract
  structure.
- **The implementation.** The class is verified against that Manual item by
  item ([`REVISAO_SIBI.md`](./REVISAO_SIBI.md)) and the norm cites it as the
  implementation of reference.

The text put to the Comissão for a vote is
[`PROPOSTA_CPGP.md`](./PROPOSTA_CPGP.md); the covering letter is
[`CARTA_CPGP.md`](./CARTA_CPGP.md). What changes for people already writing a
thesis is in [`MIGRATION_v3_to_v4.md`](./MIGRATION_v3_to_v4.md).

### What it changes

The class gains a three-slot multilingual model — *main* / *foreign* /
optional *third*. The languages a thesis may be WRITTEN in are the three
allowed by art. 57 of CEPG Resolution 302/2024 (Portuguese, English,
Spanish); French and Italian ship as demonstrations of the plug-in
mechanism, not as permitted thesis languages. There are five built-in
language options and a plug-in
mechanism for any other Babel language:

- **`brazilian`** (default) and **`english`** — strings shipped inside
  `coppe.cls`; no extra file needed; identical output to previous releases.
- **`spanish`** — language pack auto-loaded
- **`french`**, **`italian`** — demonstration packs, auto-loaded
  from `coppe-lang-<lang>.def` (class strings) and `<lang>-coppe.lbx`
  (biblatex strings), both shipped alongside `coppe.cls` in `dist/`.
- **Any other Babel language** — supply the same two files and pass the
  language name as a class option or call `\usecoppelanguage{<lang>}`.

The *main* language is selected by the class option. The *foreign* slot
defaults to `english` (and to `brazilian` when main = `english`). The
optional *third* slot is loaded on demand for citations or quotations in
a third language.

### New user-facing API

| Macro / environment            | Purpose                                                             |
| ------------------------------ | ------------------------------------------------------------------- |
| `\titlein{<lang>}{<text>}`     | Register the title in any language. `\title` / `\foreigntitle` still write the Brazilian-Portuguese and English titles. The cover/folha-de-rosto prints the title that matches the main language. |
| `\begin{brazilianabstract}`    | Optional third abstract in Portuguese (with the babel typography pinned), for Spanish/French/Italian theses that also need a UFRJ-readable resumo. |
| `\usecoppelanguage{<lang>}`    | Load an extra language pack in the preamble without making it main or foreign. |

### Backward compatibility

`\documentclass[english]{coppe}` and the entire pre-existing user-facing
API (`\if@english`, `\iflanguage{brazilian}{...}{...}`, `\local@*`,
`\foreign@*`, `\title`, `\foreigntitle`, `\begin{foreignabstract}`,
`\selectlanguage`, …) continue to behave exactly as before. The pt-main
`example.pdf` and an en-main smoke document rebuild **byte-identical** to
the previous release at every step of the refactor.

### Institutional template stays Portuguese

The cover, folha-de-rosto and ficha catalográfica are a Brazilian
institutional template (NBR 14724 + COPPE manual). University name,
city, state, country and department titles, plus the surrounding
"apresentada/submetida ao…" wording, remain in Portuguese for every
main language. Only the thesis title (chosen via `\titlein`) follows
the main language.

### What is new in `dist/`

| File                          | Role                                                  |
| ----------------------------- | ----------------------------------------------------- |
| `spanish-coppe.lbx`           | Biblatex localization strings for Spanish.            |
| `french-coppe.lbx`            | Biblatex localization strings for French.             |
| `italian-coppe.lbx`           | Biblatex localization strings for Italian.            |
| `coppe-lang-spanish.def`      | Class-level Spanish string pack (captions, labels, months, advisor, etc.). |
| `coppe-lang-french.def`       | Class-level French string pack.                       |
| `coppe-lang-italian.def`      | Class-level Italian string pack.                      |

The manual (`coppe.pdf`) gains a new "Multilingual support" subsection
(§5.2) covering the architecture, the API, the language-pack recipe (full
key list + the deferred `\DeclareLanguageMapping` idiom) and a complete
Spanish-main worked example.

### Conformance with the 2026 Manual (v4.1)

The revised 9th edition (2026) of the UFRJ/SiBI Manual absorbed three
institutional decisions — exclusively digital deposit (CEPG Res. 246/2023), the
writing languages of art. 57 of CEPG Res. 302/2024, and the new CAPES
data-collection sheet — and the class had never been checked against it. The
September 2026 series did that, item by item. The full list is in
[`CHANGELOG.md`](./CHANGELOG.md); the headline items:

- pagination continuous from the folha de rosto, folio in 10 pt at 2 cm from
  the top and right edges, one-sided layout with a 3 cm left margin;
- the additional sheet with the catalog card and the CAPES collection fields;
- the approval sheet of 3.1.2.1.3, with the date and each member's degree and
  institution, and spacing that keeps a board of up to eight on one sheet;
- keywords closing all three abstracts, pre-textual lists out of the sumário,
  Apêndice and Anexo centred;
- Latin Modern instead of bitmap fonts, and **PDF/A-2b** under the `pdfa`
  option, validated by veraPDF;
- `\coadvisor`, plus the `coorientador` option for the abstract pages.

### Single source, and proving a release

`pdflatex coppe.ins` in `src/` generates **everything that is distributed** —
the class, the biblatex styles, the language packs, the `.bib` bases, the
`.ist`, the five per-language examples, `example_pdfa`, the cover montage and
the `latexmkrc`. No derived file is edited by hand.

What exists only to *prove* the class works is not distributed and is not in
the `.dtx`: the regression suite, the twelve adversarial documents in
`adversativa/`, and the harness in `tools/`. One command runs the lot:

```powershell
.\tools\prova.ps1
```

It regenerates the distribution and checks by git that no derived file
diverged, compiles everything under both pdfLaTeX and LuaLaTeX, runs veraPDF
over every PDF/A, and prints a verdict. `python3 tools/conferir-norma.py
adversativa/adv_*.pdf` then measures the finished PDFs against the Manual —
paper size, margins, folio position on the rendered ink, pagination order,
sumário contents, approval sheet, abstract pages.


## Required LaTeX packages

`coppe.cls` is built on the standard **`book`** class (`12pt, a4paper,
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
- `amssymb` — AMS symbol fonts; loaded **only under pdfTeX** (under a
  Unicode engine load `unicode-math` yourself — the class warns if neither
  is present).

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
- `biblatex` [`backend=biber`] — bibliography engine and the ABNT `coppe`
  styles (`coppe` / `coppe-numeric`). The backend is **biber**, not bibtex.

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

Everything is loaded unconditionally except `inputenc` / `amssymb` (pdfTeX
only) and the option-driven `biblatex` style choice (`numbers` selects the
numeric `coppe-numeric` style). The language packs add no packages — only
the string files described above.



## How Much

> This program is free software; you can redistribute it and/or modify
> it under the terms of the GNU General Public License version 3 as
> published by the Free Software Foundation.


### Content

The development of this class follows the Comprehensive TeX Archive
Network (CTAN) standards. It is basically composed by an installation file ('coppe.ins') and the main source file ('coppe.dtx'). The full sources contain:

  1. COPYING: full text of the GNU General Policy License version 3.

  2. Makefile: used to extract the coppe class and build the
     documentation and a sample thesis.

  3. README.md: describe the CoppeTeX package.

  4. coppe-{plain,unsrt}.bst: alphabetically sorted and unsorted numbered
     BibTeX styles, Natbib compatible.

  5. coppe.dtx: main source file; contains the documentation, a sample
     thesis and a Makeindex style.

  7. coppe.ins: used to strip out the coppe document class from `coppe.dtx'.

  8. coppe-logo.[eps,pdf]: images included in the front cover.

  9. example.bib: sample BibTeX database for being used by example.tex.

Our release packages contain the following files:

  1. COPYING: full text of the GNU General Policy License version 3.

  2. README.md: describe the CoppeTeX package.

  3. coppe.cls: the main file. It is a LaTeX document class.

  4. coppe-{plain,unsrt}.bst: alphabetically sorted and unsorted numbered
     BibTeX styles, Natbib compatible.

  5. coppe.ist: Makeindex style for creating lists of symbols
     and abbreviations.

  6. coppe.pdf: CoppeTeX documentation.

  7. example.{tex,bib}: sample thesis using coppe class.

  8. coppe-logo.[eps, pdf]: images included in the front cover.


## Installing

If you have some experience with LaTeX classes and packages, you won't have any
difficulty when installing CoppeTeX. It should be installed as any other LaTeX
package you have ever used. So, you can save your time skipping this section.

The impatient user should get a thesis template [here](#).

For the enthusiastic newbies, we give here succinct instructions for installing
the CoppeTeX bundle.

There exist two possible ways of obtaining CoppeTeX. You can download a release
or the sources. Each of these has its own installation method. We describe both
in the following sections.

### From releases

Suppose TEXMF is a variable which stores the path of your local LaTeX tree.
Then you should copy the files coppe.cls, coppe.ist and coppe-unsrt.bst to
$TEXMF/tex/latex/coppe, $TEXMF/makeindex/coppe and $TEXMF/bibtex/bst/coppe,
respectively. The image files minerva.eps and minerva.pdf go into the same
directory as coppe.cls. In the end, you have to type 'texhash' to update your
LaTeX tree and to make CoppeTeX visible to your LaTeX compiler.

### From sources

For installing from sources, type:

```bash
  latex coppe.ins
```

and you will get all the files you need. They are all stripped out from
coppe.dtx. Now, you should follow the instructions in the 'From releases'
section.


## Help & Support

Please, send any comments, suggestions, questions and bugs to our [mailing list](http://coppetex.sourceforge.net/mailing-list.html).


## Add-ons

Now there is also Beamer template providade by prof. Jean-David Caprace