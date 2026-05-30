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


## `nlinguas` branch — new proposal for CPGP

This branch (`nlinguas`) is the proposed multilingual extension of CoppeTeX 4.x
submitted for evaluation by the Comissão de Programas de Pós-Graduação (CPGP)
of COPPE/UFRJ. Subject to CPGP review and approval, it will become the next
official release of the `coppe` class.

The accompanying draft of the updated COPPE norm — short, in Portuguese, and
written to delegate to the UFRJ 2025 *Manual para Elaboração e Normalização
de Trabalhos Acadêmicos* — is in [`NORMA_COPPE_2026.md`](./NORMA_COPPE_2026.md).
It lists only the COPPE-specific deltas (institutional identity, three-abstract
structure, main-language choice, COPPE lists, apêndice/anexo layout,
pre-textual numbering, ABNT post-2020 adoption) and cites CoppeTeX 4.x as the
implementation of reference.

### What it changes

The class gains a three-slot multilingual model — *main* / *foreign* /
optional *third* — with five built-in language options and a plug-in
mechanism for any other Babel language:

- **`brazilian`** (default) and **`english`** — strings shipped inside
  `coppe.cls`; no extra file needed; identical output to previous releases.
- **`spanish`**, **`french`**, **`italian`** — language packs auto-loaded
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

### Implementation history on this branch

Four commits, each independently verifiable, each rebuilt with the
existing pt/en regression baseline:

1. **`775db80`** — *scaffolding (no behavior change)*: language registers,
   dispatcher (`\copperdefstring`, `\coppestring`, `\coppemainstring`,
   `\coppeforeignstring`), Brazilian + English string tables, new class
   options, language-pack loader.
2. **`a363bc6`** — *migrate every site*: every `\iflanguage{brazilian}{x}{y}`
   and every `\if@english` design-time switch in `coppe.cls`, `coppe.bbx`
   and the bibliography drivers now reads from the dispatcher. Adds
   `\coppe@selecttitle`, `\titlein`, the `brazilianabstract` environment,
   and routes `foreignabstract` through `\coppe@foreignlang`.
3. **`466302a`** — *Spanish / French / Italian language packs*: six new
   docstrip modules in `coppe.dtx`, matching `\file{...}` entries in
   `coppe.ins`, sync rules in `doall.bat`, smoke-tested with full
   cover + abstract + foreignabstract + brazilianabstract documents.
4. **`bfd0b5d`** — *documentation*: §5.2 "Multilingual support" added to
   the manual; the class-option list and the `\title` paragraph in the
   pre-existing "Document identification" section updated to point at it.





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