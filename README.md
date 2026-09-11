<!-- AVISO-CPGP:INICIO — apagar deste comentário até AVISO-CPGP:FIM depois da aprovação -->
> ## ⚠️ Versão nova, ainda não aprovada
>
> **Esta é a CoppeTeX 4.1, e ela ainda não foi aprovada.** Vai à próxima reunião
> da Comissão de Programas de Pós-Graduação (CPGP) da COPPE/UFRJ.
>
> Enquanto isso: use-a para escrever e para experimentar, mas confirme com a
> secretaria do seu Programa antes de depositar um trabalho com ela.
>
> **O `master` carrega esta versão, e não a aprovada.** A decisão de trazê-la
> para o `master` antes da votação foi deliberada: é assim que os Programas e os
> alunos conseguem experimentar a proposta, e é daqui que sai a entrega em
> [`dist/`](./dist). O último estado que a CPGP aprovou é a tag
> [`coppetex-3.5.1`](https://github.com/COPPE-UFRJ/CoppeTeX/tree/coppetex-3.5.1),
> que continua onde sempre esteve e não se move.
>
> Depois da aprovação, apague o bloco entre os comentários `AVISO-CPGP:INICIO`
> e `AVISO-CPGP:FIM` no começo deste arquivo. Não há nada mais a mexer.
>
> ---
>
> **New version, not yet approved.** This is CoppeTeX 4.1, going to the next
> meeting of COPPE/UFRJ's graduate programme committee (CPGP). Write and
> experiment with it, but check with your Programa's office before depositing a
> thesis. **`master` carries this version, not the approved one**; the last
> state the CPGP approved is the tag `coppetex-3.5.1`.
<!-- AVISO-CPGP:FIM -->

# CoppeTeX

## Vou escrever uma tese. O que eu baixo?

**Baixe o arquivo .zip no release e só ele.** ou **aixe a pasta [`dist/`](./dist), e só ela.** 
Lá está tudo o que é preciso para escrever e depositar: a classe, os estilos de bibliografia, os logotipos, os
dois manuais e um exemplo completo em cada idioma que a UFRJ admite. O
[`dist/README.md`](./dist/README.md) diz como instalar e por onde começar.

Todo o resto deste repositório é para **quem mexe na classe**: a fonte
comentada, os testes, os documentos normativos e as ferramentas. Se é o seu
caso, clone o repositório inteiro e comece pelo [`PAINEL.md`](./PAINEL.md).

*Writing a thesis? Download only [`dist/`](./dist) — it has the class, the
styles, the logos, both manuals and one complete example per language. Working
**on** the class? Clone everything and start from [`PAINEL.md`](./PAINEL.md).*

---

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


## The proposal for CPGP (v4.1)

`master` carries CoppeTeX **4.1**, submitted for evaluation by the Comissão de
Programas de Pós-Graduação (CPGP) of COPPE/UFRJ. Subject to CPGP review and
approval, it becomes the next official release of the `coppe` class. It was
developed on the `nlinguas` branch and merged so that Programas and students can
try it and so that the delivery in [`dist/`](./dist) comes from one place.

**Until the vote, `master` is a proposal, not an approved norm.** The last state
the CPGP approved is the tag
[`coppetex-3.5.1`](https://github.com/COPPE-UFRJ/CoppeTeX/tree/coppetex-3.5.1),
which does not move.

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
- **the work's own reference opening each abstract**, as Annexes E and F show
  it, composed by the class from the folha de rosto data. `resumosemreferencia`
  takes it back out;
- Latin Modern instead of bitmap fonts, and **PDF/A-2b** under the `pdfa`
  option, validated by veraPDF;
- `\coadvisor`, plus the `coorientador` option for the abstract pages;
- the CAPES sheet drawn as the framed table Annex H shows, one cell per field
  and nothing to write on;
- **no signature rules on the approval sheet** — the deposit is digital only,
  so there is nothing to sign by hand. The `assinaturas` option survives as a
  no-op that warns;
- **the approval sheet lists only the examiners** — it records who examined the
  work, and the advisor conducted it. `orientadorexamina` puts the advisors and
  coadvisors back, ahead of the examiners, where the Programa seats the advisor
  on the board;
- **no blank rule for the date** — without `\dataaprovacao` the sheet reads
  "a ser determinada", in the main language;
- **sans-serif by default**, with `comserifa` for the serif face. Neither the
  Manual nor the COPPE norm prescribes a family, and the Manual itself is set
  in Arial.

**Two breaking changes**, both in how the board is declared. The treatment
(`Prof.`) became the optional argument and is empty by default; the institution
became the last mandatory argument and may be left blank:

```latex
\advisor{Ana}{Lima}{D.Sc.}{UFRJ}        % was \advisor[UFRJ]{Prof.}{Ana}{Lima}{D.Sc.}
\examiner{Bia Sousa}{Ph.D.}{UFF}        % was \examiner[UFF]{Prof.}{Bia Sousa}{Ph.D.}
```

`\coadvisor` takes the same four arguments as `\advisor`. See
[`MIGRATION_v3_to_v4.md`](./MIGRATION_v3_to_v4.md).

### What each folder is for

Every directory explains itself in its own README; start with the one you are
about to touch. Only one of them is meant for people writing a thesis.

| Folder | For whom | What it is |
|---|---|---|
| **`dist/`** | **Anyone writing a thesis** | **The delivery — download this and nothing else.** The class, the bibliography styles, the logos, both manuals and one complete example per admitted language. 31 files plus its own README, which is the installation guide. → [dist/README.md](./dist/README.md) |
| `src/` | Whoever changes the class | The source, and the **programming guide**. `coppe.dtx` is the single source: everything distributed is generated from it, and a hand edit to a generated file is lost at the next generation. Also holds the norm manual and the five per-language demos. → [src/README.md](./src/README.md) |
| `tools/` | Whoever changes the class | The build and verification harness, and the developer panel behind `coppetex.bat`. → [tools/README.md](./tools/README.md) |
| `tests/` | Whoever changes the class | Three layers of testing, each asking a different question. No PDF here is versioned. → [tests/README.md](./tests/README.md) |
| `tests/adversativa/` | Whoever changes the class | Six documents that fire everything at once, under both engines. → [tests/adversativa/README.md](./tests/adversativa/README.md) |
| `tests/regressivo/` | Whoever changes the class | One minimal test per defect already fixed. Opt-in. → [tests/regressivo/README.md](./tests/regressivo/README.md) |
| `specs/` | Whoever changes the class | The normative documents the class implements, as PDFs. → [specs/README.md](./specs/README.md) |

The root also carries the documents *about* the release rather than the code:
[`PAINEL.md`](./PAINEL.md) (how to build and test), [`CHANGELOG.md`](./CHANGELOG.md),
[`NORMA_COPPE_2026.md`](./NORMA_COPPE_2026.md) (what COPPE decides on top of the
UFRJ Manual), [`REVISAO_SIBI.md`](./REVISAO_SIBI.md) (the item-by-item check
against it), [`MIGRATION_v3_to_v4.md`](./MIGRATION_v3_to_v4.md) and
[`CONTRIBUTING.md`](./CONTRIBUTING.md).

### Single source, and proving a release

> **`src/coppe.dtx` is the single source.** Everything the project distributes
> is generated from it; a hand edit to a generated file is lost at the next
> generation, without warning. If you want to change the class, change the
> `.dtx`. `tools\prova.ps1` checks this by git and refuses to close a release
> when a derived file has diverged.

`pdflatex coppe.ins` in `src/` generates **everything that is distributed** —
the class, the biblatex styles, the language packs, the `.bib` bases, the
`.ist`, the five per-language examples, `example_pdfa`, the cover montage and
the `latexmkrc`. No derived file is edited by hand.

What exists only to *prove* the class works is not distributed and is not in
the `.dtx`: everything under `tests/` and the harness in `tools/`. One command
does the lot, and asks you what to do:

```bat
coppetex.bat
```

That is the **developer panel** — a window with everything it can do, and the
same set of actions on the command line. Its manual is
[PAINEL.md](./PAINEL.md). To go straight to what a release needs:

```bat
coppetex.bat --tudo --regressivo --conferir --dist
```

It regenerates the distribution and checks by git that no derived file
diverged, compiles everything under both pdfLaTeX and LuaLaTeX, runs veraPDF
over every PDF/A, runs the three layers of tests, and prints a verdict.
`python3 tools/conferir-norma.py src/*.pdf` then measures the finished PDFs
against the Manual — paper size, margins, folio position on the rendered ink,
pagination order, sumário contents, approval sheet, abstract pages.


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

The development of this class follows the Comprehensive TeX Archive Network
(CTAN) standards. **Two files are the whole source**: `src/coppe.dtx`, which
carries the code, the documentation and the demonstration documents, and
`src/coppe.ins`, the docstrip script. One run,

```bash
cd src && pdflatex coppe.ins
```

writes every file that is distributed:

| File(s) | Role |
| --- | --- |
| `coppe.cls` | the document class |
| `coppe.bbx`, `coppe.cbx`, `coppe.dbx` | ABNT author--date biblatex style and data model |
| `coppe-numeric.bbx`, `coppe-numeric.cbx` | the numeric variant (class option `numbers`) |
| `brazilian-coppe.lbx`, `english-coppe.lbx`, `spanish-coppe.lbx`, `french-coppe.lbx`, `italian-coppe.lbx` | biblatex localization strings |
| `coppe-lang-spanish.def`, `coppe-lang-french.def`, `coppe-lang-italian.def` | class-level string packs |
| `coppe.ist` | makeindex style for the lists of symbols and abbreviations |
| `coppe.bib`, `example.bib` | the bibliography of the manual and the example's sample database |
| `example.tex` | the full sample thesis |
| `example_pt.tex`, `example_en.tex`, `example_es.tex`, `example_fr.tex`, `example_it.tex` | one short demonstration per main language |
| `example_pdfa.tex` | the full example compiled as PDF/A-2b |
| `covers_5languages.tex` | the side-by-side cover sheet |
| `latexmkrc` | latexmk configuration (biber + the makeindex runs) |

No derived file is edited by hand. The bundle ships two logos,
`coppe-logo.[eps,pdf]` and `ufrj-logo.pdf`, and `COPYING`.

The BibTeX `.bst` styles of the 3.x series are gone: the bibliography engine
is **biblatex with biber**.

`dist/` holds a built copy of all of the above plus the compiled PDFs, so the
package can be read and installed without running LaTeX at all.

## Installing

If you have some experience with LaTeX classes and packages, you won't have any
difficulty when installing CoppeTeX. It should be installed as any other LaTeX
package you have ever used.

The simplest install is no install: copy the contents of `dist/` next to your
thesis `.tex` and compile. LaTeX finds a class in the current directory first.

### Into your local TeX tree

Suppose `TEXMF` is your local LaTeX tree. Then:

| From `dist/` | Goes to |
| --- | --- |
| `coppe.cls`, the `.bbx`/`.cbx`/`.dbx`, the `.lbx`, the `coppe-lang-*.def`, `coppe-logo.[eps,pdf]`, `ufrj-logo.pdf` | `$TEXMF/tex/latex/coppe` |
| `coppe.ist` | `$TEXMF/makeindex/coppe` |

Then run `texhash` (or `initexmf --update-fndb` on MiKTeX) so the class becomes
visible to your compiler.

### From sources

```bash
cd src && pdflatex coppe.ins
```

gives you the same files, freshly generated from `coppe.dtx`. Then follow the
section above.

### Compiling a thesis

`latexmkrc` ships with the bundle and already knows about biber and the two
makeindex runs, so `latexmk -pdf yourthesis` is enough. By hand it is
pdflatex, biber, pdflatex, pdflatex.

## Help & Support

Please, send any comments, suggestions, questions and bugs to our [mailing list](http://coppetex.sourceforge.net/mailing-list.html).


## Add-ons

Now there is also Beamer template providade by prof. Jean-David Caprace
