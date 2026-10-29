# ufrj — LaTeX class for theses and dissertations at UFRJ

Version @VERSAO@. Licence: GNU General Public License version 3 (see
`COPYING.txt`). Maintainers: Geraldo Xexéo and Eduardo Mangeli; originally
written by Vicente Helano F. Batista and George O. Ainsworth Jr.

The package is named after the class it provides, `ufrj`. It is the work of
the **CoppeTeX** project, which is the name the colophon of every thesis
carries and the name of the repository where it is developed.

Development, issues and the full repository:
<https://github.com/COPPE-UFRJ/CoppeTeX>

## What this is

`ufrj` is a document class for the academic works deposited at the Federal
University of Rio de Janeiro (UFRJ): master's dissertations, doctoral theses,
qualifying exams and master's seminars. It implements the *Manual para
elaboração e normalização de trabalhos acadêmicos* of the UFRJ Library System
(SiBI), 9th edition revised, 2026, which is the binding norm for every unit of
the university.

The class knows **no academic unit**. What belongs to a unit — the name of the
institute on the cover, its graduate programmes, its logo, the phrases its own
norm fixes — comes from a **unit style** loaded right after the class:

```latex
\documentclass[dsc]{ufrj}
\usepackage{ufrj-coppe}
```

`ufrj-coppe` is the style of COPPE, the Alberto Luiz Coimbra Institute for
Graduate Studies and Research in Engineering, where the project was born, and
it is the model for any other unit. A work begun with the older `coppe` class
still compiles: `coppe.cls` loads the pair above and warns once.

The bibliography follows ABNT NBR 6023:2018 and NBR 10520:2023 through
biblatex and biber, with author-date citations by default and a numeric
alternative. Documents may be written in Portuguese, English or Spanish, the
three languages UFRJ admits; French and Italian ship as demonstrations of the
plug-in mechanism for any other Babel language.

## What is in this package

| File | What it is |
|---|---|
| `ufrj.dtx`, `ufrj.ins` | The class, the biblatex styles, the language packs, the bibliographic databases, the makeindex style and the `latexmkrc`. |
| `ufrj-coppe.dtx`, `ufrj-coppe.ins` | The COPPE unit style, the `coppe` compatibility class and the example documents. |
| `ufrj.pdf` | The manual of the class: every option, command and environment, and the interface a unit style uses. |
| `ufrj-coppe.pdf` | The manual of the COPPE style: what it declares, and how to write the style of another unit. |
| `ufrj-quickref.pdf`, `coppe-quickref.pdf` | One-page references, in English. |
| `manual.pdf` | The norm itself, as a document that obeys it: every rule is stated and then demonstrated. |
| `coppe-min-exemplo.tex`, `coppe-max-exemplo.tex`, `exemplo.bib` | A minimal work and a work that uses everything the class offers. |
| `logos/` | The logos the cover may carry. |
| `ufrj.tds.zip` | The same files in a TDS tree, ready to unzip into a `texmf` root. |

To generate the class and the styles from source:

```
pdflatex ufrj.ins
pdflatex ufrj-coppe.ins
```

One of the generated files comes out as `latexmkrc.tex` and has to be renamed
to `latexmkrc`: TeX's `\openout` appends `.tex` to a name without an extension
and refuses a name beginning with a dot, so docstrip cannot write it under its
own name. It is the recipe that makes `latexmk` — and Overleaf — run biber and
the four makeindex passes that the lists of abbreviations, of symbols, the
glossary and the index need. In the TDS tree it is already installed as
`doc/latex/ufrj/latexmkrc`.

## Installation

Unzip `ufrj.tds.zip` into a local `texmf` tree and refresh the filename
database (`mktexlsr`, or `initexmf --update-fndb` on MiKTeX). The logos are
installed next to the class, so a document finds them without copying anything.

To use the class in a single folder instead, run the two `.ins` above and keep
the generated files beside your document, together with `logos/`.

## Requests and bugs

The project lives on GitHub: <https://github.com/COPPE-UFRJ/CoppeTeX>.

To **request a feature** or **report a bug**, open an issue at
<https://github.com/COPPE-UFRJ/CoppeTeX/issues>. For a bug, give the class
version (the `Document Class: ufrj` line of the `.log`), the smallest `.tex` that reproduces
it and, if there is one, the `.log` of the run.

## The documentation is in Portuguese

The manuals, the examples and the error messages are written in Portuguese:
the readers are students of a Brazilian university writing to a Brazilian
norm. The quick references (`ufrj-quickref.pdf` and `coppe-quickref.pdf`) are
in English, and so are the comments in the source, so that the class can be
read and adapted by anyone.
