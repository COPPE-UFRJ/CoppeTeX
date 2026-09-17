# Contributing to CoppeTeX

Thanks for your interest in CoppeTeX. This guide covers the three most
common contributions:

1. [Adding a new language pack](#adding-a-new-language-pack) — by far the
   most likely contribution path for users, especially since v4.0.
2. [Adding a unit style](#adding-a-unit-style) — for an academic unit of
   UFRJ other than COPPE, since v5.0.
3. [Fixing or improving the class / manual](#fixing-the-class-or-the-manual)
   — for changes to `ufrj.dtx`, `ufrj-coppe.dtx`, the manuals, etc.

A last section briefly covers [reporting bugs and asking
questions](#reporting-bugs-or-asking-questions).

---

## Adding a new language pack

CoppeTeX ships with five built-in main languages: `brazilian`,
`english`, `spanish`, `french`, `italian`. Adding a new one — say
**`german`** — is a self-contained, ~5-minute task. You need to write
two small files and either drop them next to your `ufrj.cls` or open a
pull request to add them to the official distribution.

### 1. Pick the language name

Use the **exact name Babel uses** for the language (`german`, `dutch`,
`catalan`, etc.). The class option name, the `.def` and `.lbx` file
names, and the table keys all use this single string.

### 2. Write `ufrj-lang-<lang>.def`

Take an existing pack as your template. The simplest reference is
[`dist/es/ufrj-lang-spanish.def`](./dist/es/ufrj-lang-spanish.def).

The file consists of:

- One `\ProvidesFile{ufrj-lang-<lang>.def}[date version description]`
  header line.
- One `\ufrjdefstring{<lang>}{<key>}{<value>}` line per string. The
  full list of keys you must populate is the same one populated for
  `brazilian` and `english` in `ufrj.cls`:
  - **TOC / list labels:** `appendix`, `annex`, `frame`, `listframe`,
    `source`, `program`, `listprogram`, `references`, `in:`, `art`,
    `platform`, `directedby`, `producedby`, `listabbreviation`,
    `listabbreviationonly`, `listsigla`, `listsymbol`, `glossary`
  - **Folha de rosto and approval sheet:** `advisor`, `advisors`,
    `coadvisor`, `coadvisors`, `dept`, `approvedmale`, `approvedfemale`,
    `approvedonmale`, `approvedonfemale`, `keywordsname`, `volumename`,
    `ofname`, `researchline`, `tbddate`
  - **The opening sentence of the abstract sheet:** `abstractname`,
    `abstractofmale`, `abstractoffemale`, `presentedmale`,
    `presentedfemale`, `tounit`, `abstracttail`, `doctypemsc`,
    `doctypedsc`, `doctypeexam`, `doctypesem`, `degnamemsc`, `degnamedsc`.
    `tounit` is the class's value with no unit, *to UFRJ* in your language
    with the right article (`a la UFRJ`, `à l'UFRJ`); a unit style replaces
    it with its own.
  - **Months:** `monthname1` through `monthname12`
  - **Engine-specific:** `algorithm2eopt` (the language name that
    `algorithm2e` expects — careful: not always the same Babel calls it,
    e.g. for Italian it is `italiano`), `babelname` (the Babel language
    name itself, kept for clarity).
- One **deferred** `\AtBeginDocument{\DeclareLanguageMapping{<lang>}{<lang>-ufrj}}`
  line at the end. Don't call `\DeclareLanguageMapping` directly — at
  the moment the pack is read, biblatex is not yet loaded.

**Nothing institutional goes in a language pack.** The names of the
university, of the unit and of the Programa do not translate, and whatever
belongs to a unit — the name it gives the degree (`sciencename`), the
institution the work was presented to — comes from the unit style.

### 3. Write `<lang>-ufrj.lbx`

This is the biblatex localization file. Template:
[`dist/es/spanish-ufrj.lbx`](./dist/es/spanish-ufrj.lbx).

It consists of:

- `\ProvidesFile{<lang>-ufrj.lbx}[date version description]`
- `\InheritBibliographyExtras{<lang>}` — inherits from biblatex's own
  `<lang>.lbx` (so the language must be one of those biblatex ships, or
  you must also write the inherited extras yourself).
- `\NewBibliographyString{availablefrom,mscdiss,dscthesis,tcc,depositor,ufrjscale,ufrjmscdeg,ufrjdscdeg,ufrjphddeg,ufrjtccdeg,ufrjfiling,ufrjgrant}`
- `\DeclareBibliographyStrings{...}` with translations for each of the
  CoppeTeX-specific keys: `availablefrom`, `urlseen`, `in`, `editor`,
  `editors`, `depositor`, `ufrjscale`, `mscdiss`, `dscthesis`,
  `phdthesis`, `tcc`, `ufrjmscdeg`, `ufrjdscdeg`, `ufrjphddeg`,
  `ufrjtccdeg`, `ufrjfiling`, `ufrjgrant`.

### 4. Test

Copy `example_pt.tex` (or any of `example_{en,es,fr,it}.tex`) to
`example_<lang>.tex`, change the `\documentclass` option, add a
`\titlein{<lang>}{...}`, and translate the body to the new language.
Build it with the same chain (`pdflatex` → `biber` → `makeindex` →
`pdflatex` → `pdflatex`). The cover should render with Portuguese
institutional names and your translated title. The COPPE style does not
know your language, so the abstract sheet says the work was presented *to
UFRJ*, from your pack; a line `\ufrjdefunitstring{<lang>}{tounit}{...}` in
`ufrj-coppe.dtx` would make it say *to COPPE/UFRJ*.

### 5. Submit (optional)

If you would like the pack to ship with the official CoppeTeX:

1. Open a pull request adding the two new docstrip modules
   (`<*lang<xx>>...</lang<xx>>` and `<*lbx<xx>>...</lbx<xx>>`) inside
   `src/ufrj.dtx`, plus the matching `\file{...}` entries in
   `src/ufrj.ins` and the `PARA_DIST` list in `tools/painel.py`.
2. Run `pdflatex ufrj.ins` once to regenerate everything.
3. Include the example file. The examples use the COPPE style, so they live in
   `src/ufrj-coppe.dtx`, with a `\file{...}` entry in `src/ufrj-coppe.ins`.
   It goes to `dist/` only for a language art. 57 of CEPG Res. 302/2024
   admits for writing a thesis — Portuguese, English and Spanish. A new
   language pack is a demonstration of the extension mechanism until that
   changes.
4. Submit. The maintainers will review the translations (preferably
   with help from a native speaker) before merging.

---

## Adding a unit style

The `ufrj` class implements the UFRJ Library System's manual and knows no
academic unit. Whatever a unit fixes on its own — its name on the cover, its
Programas, the right-hand logo, the phrases of its norm — comes from a
**unit style**, loaded right after the class:

```latex
\documentclass[dsc]{ufrj}
\usepackage{ufrj-coppe}
```

A new unit — say the Escola Politécnica — writes its own style. The class
does not change. Step by step:

### 1. Copy the COPPE style

Copy `src/ufrj-coppe.dtx` and `src/ufrj-coppe.ins` to `src/ufrj-poli.dtx` and
`src/ufrj-poli.ins`, and rename inside them. Keep the `ufrj-` prefix: every
file of a TeX distribution must have a unique name, and `poli.sty` is a name
someone else may want.

### 2. Change the declarations

The implementation section of the `.dtx` is a short list of declarations,
all documented in the class manual (`ufrj.pdf`, section *A instituição e a
unidade*):

| Command | What it declares |
|---|---|
| `\ufrjdeclareunit{full name}{cover form}{acronym}` | the unit, in the reference line, on the cover (with `\\` breaks) and as an acronym |
| `\ufrjdeclareprogram{code}{Portuguese name}{English name}` | one Programa, chosen by the author with `\department{code}` |
| `\ufrjdeclarelogos[height]{left}{right}` | the logos on the cover and title page; an empty name removes one |
| `\ufrjdeclarenorm{article}{title}` | the norm the colophon says the document follows |
| `\ufrjdefunitstring{language}{key}{text}` | a unit text: `tounit` (*à COPPE/UFRJ*), `sciencename` (*em Ciências*), `coverprogram`, `natureza` |

The smallest complete example is the test fixture
[`tests/regressivo/ufrj-ficticia.sty`](./tests/regressivo/ufrj-ficticia.sty),
a made-up unit in twenty lines.

### 3. Remove what only COPPE has

The old command names of the `coppe` class, the `coppe` compatibility class
(module `compat`) and the COPPE examples belong to COPPE. A new unit writes
its own examples, or none.

### 4. Add the logo and test

Put the unit's logo in `src/logos/` as a PDF. Build a document with the new
style and check the cover, the folha de rosto, the abstract sheets and the
colophon. `tests/regressivo/rtu02-unidade-ficticia.tex` shows what to check.

### 5. Submit (optional)

Add the new `.ins` to `tools/build-check.ps1`, the new files to the
`PARA_DIST` list in `tools/painel.py`, and open a pull request. The review
checks the data against the unit's own norm, the way `ufrj-coppe.dtx`
cites the COPPE norm section by section.

---

## Fixing the class or the manual

The class lives in `src/ufrj.dtx` and the COPPE unit style in
`src/ufrj-coppe.dtx` — two documented `.dtx` files. Run `pdflatex ufrj.ins`
and `pdflatex ufrj-coppe.ins` (or `coppetex.bat --regerar` on Windows, which
runs both) to regenerate `ufrj.cls`, the `.bbx/.cbx/.dbx`, the `.lbx` files
and the `.def` files from the first, and `ufrj-coppe.sty`, `coppe.cls` and
the examples (`min-exemplo.tex`, `max-exemplo.tex`, the language demos) from
the second. The manuals `ufrj.pdf` and `ufrj-coppe.pdf` are also rebuilt from
the `.dtx` files by running `pdflatex` on them three times with `makeindex`
in between.

**The class never names a unit.** Nothing generated from `ufrj.dtx` may
mention COPPE, its institute, its logo or its Programas;
`tests/regressivo/rtu04` checks the generated code and `rtu01` checks a PDF
composed without any unit style. If a change needs unit data, it needs a new
declaration in the class interface, filled by the unit style.

When you edit a `.dtx`:

- **Behavior changes for pt or en?** Compare a rebuilt `dist/manuais/max-exemplo.pdf`
  against the previous version page-by-page (`pdftoppm` + `md5sum`).
  Unless you intend a visible change, the diff should be empty.
- **New macros?** Add a `\changes{vX.Y}{date}{description}` entry near
  the macro's `\begin{macro}` block — these become the change history
  in `ufrj.pdf` or `ufrj-coppe.pdf`.
- **Anything affecting documentation?** Update the relevant section of
  the documentation prose in the `.dtx` (the lines starting with `%`).
- **dist/ in sync?** When you finalise, copy the generated files to
  `dist/` (or run `coppetex.bat --dist` on Windows, which does it).

For larger restructurings, see how the v4.0 multilingual refactor was
sequenced (commits `775db80`, `a363bc6`, `466302a`, `bfd0b5d`) — three
small, individually-verifiable steps each preserving the pt/en
baseline — and how the v5.0 split between the class and the unit style was
(commits `22e7dc9`, `fc0eb20`, `547bf45`), each proved against page renders of
the previous state.

---

## Reporting bugs or asking questions

Open an issue on the GitHub repository
<https://github.com/COPPE-UFRJ/CoppeTeX/issues>.

When reporting a bug:

- The class option(s) you used (`brazilian`, `english`, `spanish`, …).
- The unit style you load (`ufrj-coppe`, another one, or none).
- A **minimal `example_bug.tex`** that reproduces the issue (15 lines
  is enough in most cases).
- The version of CoppeTeX (look for the `\ProvidesClass{ufrj}[...]`
  line in your build log, or the first line of `ufrj.cls`).
- The TeX engine and distribution (`pdfLaTeX`/`LuaLaTeX`/`XeLaTeX`,
  MiKTeX/TeX Live, year).

For language-pack issues specifically, mention also which `.def`/`.lbx`
files you have installed and where.
