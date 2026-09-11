# CoppeTeX Examples Registry

Documents each `example#.pdf` / `example#.tex` used to demonstrate and prove the
CoppeTeX bibliography (and later, float/caption) features.

**Convention:** `example<N>.tex` compiles to `example<N>.pdf`; `N` is the example
number described in the table below.

| # | File | Demonstrates | Status |
|---|------|--------------|--------|
| 0 | `example0.pdf` | **Baseline.** Current (pre-change) build of the original `example.tex`, using the legacy BibTeX + natbib bibliography (`coppe-unsrt`). Captured before any CoppeTeX 4.0 bibliography change so later builds can be diffed to prove *only* the bibliography changed (todo §20). | baseline captured |
| 1 | `example1.pdf` | **Engine proof (author-date).** Standalone document (article class, while the `coppe` class integration is in progress) exercising the new BibLaTeX/biber ABNT engine: core types (`book`, `article`, `incollection`, `inproceedings`, `thesis`, `report`, `misc`), the thesis family (`@dscthesis` → "Tese de Doutorado"), English+Portuguese field synonyms (`@livro` with `autor`/`titulo`/`edicao`/…), a custom `@videogame` with corporate author, entry-by-title, `natbib` `\citet`/`\citep`, and *apud* citation-of-citation (`\citetapud`/`\citepapud`, ABNT §4.1.2.2.1). Build: `pdflatex example1 ; biber example1 ; pdflatex example1 ; pdflatex example1`. | working |
| 2 | `example2.pdf` | **Engine proof (numeric, unsorted).** Same data as `example1.bib`, rebuilt with the numeric citation style (`bibstyle`/`citestyle=coppe-numeric`): bracketed `[n]` in-text labels, `numeric-comp` range compression (`[1--3]`), `natbib` `\citet`→"Author [n]" / `\citep`→"[n]", and the reference list in **citation order** (ABNT NBR 10520, `sorting=none`) — cited deliberately out of alphabetical order so the unsorted numbering is visible. All `coppe.bbx` ABNT list formatting carries over. Build: `pdflatex example2 ; biber example2 ; pdflatex example2 ; pdflatex example2`. | working |

_The `coppe` class integration and exotic-type drivers are the next examples. The
engine files are `src/coppe.{dbx,bbx,cbx}`, `src/coppe-numeric.{bbx,cbx}` (numeric
opt-in) and `src/{brazilian,english}-coppe.lbx` (to be generated from `coppe.dtx`)._
