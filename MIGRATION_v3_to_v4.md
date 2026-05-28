# Migration guide — CoppeTeX v3.x → v4.0

Short guide for thesis authors currently using CoppeTeX v3.x who want to
move to v4.0. Read once, do at most one of the three sections below
depending on your situation, and you are done.

---

## TL;DR

| Your situation                                                          | Action required                          |
| ----------------------------------------------------------------------- | ---------------------------------------- |
| Portuguese-main thesis (`\documentclass[dsc]{coppe}`)                   | **None.** Just replace `coppe.cls`.       |
| English-main thesis (`\documentclass[english,dsc]{coppe}`)              | **None.** Just replace `coppe.cls`.       |
| You want to write the thesis in Spanish, French or Italian              | See Section 3 below.                     |

---

## 1. Portuguese-main thesis: nothing to do

If your `\documentclass` line is one of:

```latex
\documentclass[dsc]{coppe}
\documentclass[msc]{coppe}
\documentclass[brazilian,dsc]{coppe}
\documentclass[dscexam]{coppe}
\documentclass[mscexam]{coppe}
```

— or any combination of these with `numbers`, `doublespacing`,
`numeraisromanos`, etc. — **your document compiles bit-for-bit
identically under v4.0**. We have verified this with a
page-by-page rendered-image diff against a v3.8 build.

What to do:

1. Replace `coppe.cls`, `coppe.bbx`, `coppe.cbx`, `coppe.dbx`,
   `brazilian-coppe.lbx`, `english-coppe.lbx`, `coppe-numeric.bbx`,
   `coppe-numeric.cbx` and `coppe.ist` in your project (or local TEXMF)
   with the v4.0 versions from
   <https://github.com/COPPE-UFRJ/CoppeTeX/tree/master/dist>.
2. Recompile. Output should be visually identical.

Nothing in your `.tex` source changes.

---

## 2. English-main thesis: nothing to do

If your `\documentclass` line includes `english`:

```latex
\documentclass[english,dsc]{coppe}
```

— same story as Section 1. The `english` option keeps the exact same
semantics, the cover keeps the same institutional Portuguese template
with your English title on it, `\title{...}` and `\foreigntitle{...}`
keep their historical meaning (`\title` = Portuguese version of the
title, `\foreigntitle` = English version), and `\begin{foreignabstract}`
still produces the Brazilian-Portuguese abstract page. We have verified
byte-identical output.

What to do: same as Section 1 — replace the class files, recompile.

---

## 3. Writing in Spanish, French or Italian: three small additions

This is the new capability in v4.0. Suppose you want to write your
thesis in Spanish. Then:

### 3.1 Change the class option

```latex
\documentclass[spanish,dsc]{coppe}
```

Replace `spanish` with `french` or `italian` as appropriate.

### 3.2 Install the language pack files

Two files must sit next to `coppe.cls` (in your project directory, or in
a `TEXMF` location), both shipped in `dist/`:

- `coppe-lang-spanish.def` (class-level strings)
- `spanish-coppe.lbx` (bibliography strings)

(Use `french` or `italian` in the file names accordingly.)

If you forget either, the class will tell you so with a clear error.

### 3.3 Add a Spanish title via `\titlein`

The historical `\title{...}` still expects the Portuguese title and
`\foreigntitle{...}` still expects the English title. For a Spanish-main
thesis, the title shown on the cover is read from a new slot — set with:

```latex
\title{Título em portugu\^es}                % traditional
\foreigntitle{English title}                  % traditional
\titlein{spanish}{T\'itulo en espa\~nol}      % NEW -- the cover prints this
```

For French use `\titlein{french}{...}`; for Italian, `\titlein{italian}{...}`.

### 3.4 (Optional) Add a Portuguese abstract for the banca

When your main language is not Portuguese and you want a Portuguese
resumo for the Brazilian examiners (in addition to the abstract in the
main language and the foreign English abstract), use the new
`brazilianabstract` environment:

```latex
\begin{abstract}        ... main-language abstract ...    \end{abstract}
\begin{foreignabstract} ... English abstract ...          \end{foreignabstract}
\begin{brazilianabstract} ... Resumo em portugu\^es ...   \end{brazilianabstract}
```

This is the only place where the abstract layout is genuinely new.

### 3.5 Done.

The full layout, the cover, the folha de rosto, the ficha catalográfica,
the running heads, the references list — everything else is automatic
and respects the main language.

---

## Frequently asked

> **Will my v3.x tese-em-andamento break if I switch now?**
>
> No, as long as you are not using Spanish/French/Italian. pt/en
> documents are byte-identical.

> **Can I keep v3.x files in some directories and v4.0 in others?**
>
> Yes — each project picks up the `coppe.cls` (and friends) it finds
> first on its TEXMF path. Most students will simply put the v4.0 files
> in their project directory and forget about the global tree.

> **What if I want to use a language not in the built-in five?**
>
> Write a `coppe-lang-<lang>.def` and a `<lang>-coppe.lbx` (use any of
> the shipped Spanish/French/Italian as a template). See
> [`CONTRIBUTING.md`](./CONTRIBUTING.md) for the step-by-step.

> **Do I need to update my `latexmkrc` / Overleaf setup?**
>
> No. The build chain (pdflatex / biber / makeindex) is unchanged.

> **Where is the full reference?**
>
> Section 5.2 "Multilingual support" of the manual
> (`dist/coppe.pdf`).
