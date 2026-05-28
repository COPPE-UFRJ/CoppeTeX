# Contributing to CoppeTeX

Thanks for your interest in CoppeTeX. This guide covers the two most
common contributions:

1. [Adding a new language pack](#adding-a-new-language-pack) — by far the
   most likely contribution path for users, especially since v4.0.
2. [Fixing or improving the class / manual](#fixing-the-class-or-the-manual)
   — for changes to `coppe.dtx`, `coppe.bbx`, the manual, etc.

A third section briefly covers [reporting bugs and asking
questions](#reporting-bugs-or-asking-questions).

---

## Adding a new language pack

CoppeTeX 4.0 ships with five built-in main languages: `brazilian`,
`english`, `spanish`, `french`, `italian`. Adding a new one — say
**`german`** — is a self-contained, ~5-minute task. You need to write
two small files and either drop them next to your `coppe.cls` or open a
pull request to add them to the official distribution.

### 1. Pick the language name

Use the **exact name Babel uses** for the language (`german`, `dutch`,
`catalan`, etc.). The class option name, the `.def` and `.lbx` file
names, and the table keys all use this single string.

### 2. Write `coppe-lang-<lang>.def`

Take an existing pack as your template. The simplest reference is
[`dist/coppe-lang-spanish.def`](./dist/coppe-lang-spanish.def).

The file consists of:

- One `\ProvidesFile{coppe-lang-<lang>.def}[date version description]`
  header line.
- One `\copperdefstring{<lang>}{<key>}{<value>}` line per string. The
  full list of keys you must populate is the same one populated for
  `brazilian` and `english` in `coppe.cls`:
  - **TOC / list labels:** `appendix`, `annex`, `frame`, `listframe`,
    `source`, `program`, `listprogram`, `references`, `in:`, `art`,
    `platform`, `directedby`, `producedby`, `listabbreviation`,
    `listsymbol`, `glossary`
  - **Cover / folha / abstract strings:** `advisor`, `advisors`, `dept`,
    `approvedmale`, `approvedfemale`
  - **Institutional (always keep in Portuguese — they are the UFRJ
    institutional template):** `universityname`, `cityname`,
    `statename`, `countryname`
  - **Months:** `monthname1` through `monthname12`
  - **Engine-specific:** `algorithm2eopt` (the language name that
    `algorithm2e` expects — careful: not always the same Babel calls it,
    e.g. for Italian it is `italiano`), `babelname` (the Babel language
    name itself, kept for clarity).
- One **deferred** `\AtBeginDocument{\DeclareLanguageMapping{<lang>}{<lang>-coppe}}`
  line at the end. Don't call `\DeclareLanguageMapping` directly — at
  the moment the pack is read, biblatex is not yet loaded.

### 3. Write `<lang>-coppe.lbx`

This is the biblatex localization file. Template:
[`dist/spanish-coppe.lbx`](./dist/spanish-coppe.lbx).

It consists of:

- `\ProvidesFile{<lang>-coppe.lbx}[date version description]`
- `\InheritBibliographyExtras{<lang>}` — inherits from biblatex's own
  `<lang>.lbx` (so the language must be one of those biblatex ships, or
  you must also write the inherited extras yourself).
- `\NewBibliographyString{availablefrom,mscdiss,dscthesis,tcc,depositor,coppescale}`
- `\DeclareBibliographyStrings{...}` with translations for each of the
  CoppeTeX-specific keys: `availablefrom`, `urlseen`, `in`, `editor`,
  `editors`, `depositor`, `coppescale`, `mscdiss`, `dscthesis`,
  `phdthesis`, `tcc`.

### 4. Test

Copy `example_pt.tex` (or any of `example_{en,es,fr,it}.tex`) to
`example_<lang>.tex`, change the `\documentclass` option, add a
`\titlein{<lang>}{...}`, and translate the body to the new language.
Build it with the same chain (`pdflatex` → `biber` → `makeindex` →
`pdflatex` → `pdflatex`). The cover should render with Portuguese
institutional names and your translated title.

### 5. Submit (optional)

If you would like the pack to ship with the official CoppeTeX:

1. Open a pull request adding the two new docstrip modules
   (`<*lang<xx>>...</lang<xx>>` and `<*lbx<xx>>...</lbx<xx>>`) inside
   `src/coppe.dtx`, plus the matching `\file{...}` entries in
   `src/coppe.ins` and the `copy /Y` lines in `src/doall.bat`.
2. Run `pdflatex coppe.ins` once to regenerate everything.
3. Include the example file (`src/example_<lang>.tex` +
   `dist/example_<lang>.{tex,pdf}`).
4. Submit. The maintainers will review the translations (preferably
   with help from a native speaker) before merging.

---

## Fixing the class or the manual

The class lives in `src/coppe.dtx` — a documented `.dtx` file. Run
`pdflatex coppe.ins` (or `./doall.bat` on Windows) to regenerate
`coppe.cls`, the `.bbx/.cbx/.dbx`, the `.lbx` files, the `.def` files
and `example.tex` from it. The manual `coppe.pdf` is also rebuilt from
the same `.dtx` by running `pdflatex coppe.dtx` three times with
`makeindex` in between.

When you edit `coppe.dtx`:

- **Behavior changes for pt or en?** Compare a rebuilt `dist/example.pdf`
  against the previous version page-by-page (`pdftoppm` + `md5sum`).
  Unless you intend a visible change, the diff should be empty.
- **New macros?** Add a `\changes{vX.Y}{date}{description}` entry near
  the macro's `\begin{macro}` block — these become the change history
  in `coppe.pdf`.
- **Anything affecting documentation?** Update the relevant section of
  the documentation prose in `coppe.dtx` (the lines starting with `%`).
- **dist/ in sync?** When you finalise, copy the generated files to
  `dist/` (or run `./doall.bat` on Windows, which does it).

For larger restructurings, see how the v4.0 multilingual refactor was
sequenced (commits `775db80`, `a363bc6`, `466302a`, `bfd0b5d`) — three
small, individually-verifiable steps each preserving the pt/en
baseline.

---

## Reporting bugs or asking questions

Open an issue on the GitHub repository
<https://github.com/COPPE-UFRJ/CoppeTeX/issues>.

When reporting a bug:

- The class option(s) you used (`brazilian`, `english`, `spanish`, …).
- A **minimal `example_bug.tex`** that reproduces the issue (15 lines
  is enough in most cases).
- The version of CoppeTeX (look for the `\ProvidesClass{coppe}[...]`
  line in your build log, or the first line of `coppe.cls`).
- The TeX engine and distribution (`pdfLaTeX`/`LuaLaTeX`/`XeLaTeX`,
  MiKTeX/TeX Live, year).

For language-pack issues specifically, mention also which `.def`/`.lbx`
files you have installed and where.
