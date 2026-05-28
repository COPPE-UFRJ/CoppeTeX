# Changelog

Project changes worth noting, newest first. Follows
[Keep a Changelog](https://keepachangelog.com/) loosely; dates are
ISO-8601.

## [4.0] — 2026-05-28 — Multilingual release (CPGP proposal)

Introduced on the `nlinguas` branch and submitted for evaluation by the
Comissão de Programas de Pós-Graduação (CPGP) of COPPE/UFRJ. Pending
approval; meant to become the next official release.

### Added

- **Three fixed language slots** — *main*, *foreign*, optional *third*.
- **Five built-in main-language class options**:
  - `brazilian` (default)
  - `english`
  - `spanish` *(NEW)*
  - `french` *(NEW)*
  - `italian` *(NEW)*
- **Plug-in mechanism** for any other Babel language via two files
  installed alongside `coppe.cls`:
  - `coppe-lang-<lang>.def` — class-level string table
  - `<lang>-coppe.lbx` — biblatex localization
- **`\titlein{<lang>}{<text>}`** — register the main title for any
  language. `\title` / `\foreigntitle` keep their pt / en meaning.
- **`brazilianabstract` environment** — optional third abstract, used
  when the main language is neither `brazilian` nor `english` and a
  Portuguese resumo is needed for the banca.
- **`\usecoppelanguage{<lang>}`** — load a language pack at preamble
  time without making it main or foreign (third-slot use).
- **Manual** (`coppe.pdf`): new subsection 5.2 "Multilingual support"
  describing the architecture, the user-facing API, and how to author a
  new language pack.
- **Demo set** in `dist/`: `example_pt.pdf`, `example_en.pdf`,
  `example_es.pdf`, `example_fr.pdf`, `example_it.pdf` (cover + folha
  de rosto + abstracts + one chapter, ~13–15 pages each) and
  `covers_5languages.pdf` (one-page side-by-side montage).
- **Documentation in repository root**:
  `NORMA_COPPE_2026.md` (new draft CPGP norm),
  `MIGRATION_v3_to_v4.md` (existing thesis authors),
  `CONTRIBUTING.md` (guide for new language packs),
  `CARTA_CPGP.md` (cover letter for CPGP submission),
  `TODO.md` (open items toward final release).

### Changed

- **Class-wide string dispatcher** — `\copperdefstring`, `\coppestring`,
  `\coppemainstring`, `\coppeforeignstring` replace the scattered
  `\iflanguage{brazilian}{x}{y}` and `\if@english x \else y \fi`
  switches in `coppe.cls`, `coppe.bbx` and the bibliography drivers.
  Every previously inlined pt/en literal moved into a per-language
  table.
- **Babel load** rewritten to use the new `\coppe@mainlang` and
  `\coppe@foreignlang` registers (`[<foreign>,<main>]{babel}`).
- **`algorithm2e` language option** now read from the dispatcher
  (`algorithm2eopt` key per language).
- **`foreignabstract`** now uses `\begin{otherlanguage}{\coppe@foreignlang}`
  instead of hard-coding `english`.

### Backward compatibility

- `\documentclass[english]{coppe}` and every pre-existing user API
  (`\title`, `\foreigntitle`, `\local@*`, `\foreign@*`, `\if@english`,
  `\iflanguage{brazilian}{...}{...}`, `\selectlanguage`, `\begin{
  foreignabstract}`, `\annex`, …) keeps the same behavior as in v3.x.
- pt-main `example.pdf` rebuild is **byte-identical** to a v3.8 build
  (page-by-page md5 diff is empty across all 75 rendered pages).
- en-main smoke document is byte-identical to the v3.8 rendering.
- The historical `\if@english` boolean is kept declared and mirrors
  "is main = english?" — user code that tested it still works.

### Implementation history on the branch

| Commit  | Subject                                                                  |
| ------- | ------------------------------------------------------------------------ |
| `775db80` | step 1 — multilingual scaffolding (no behavior change)                 |
| `a363bc6` | step 2 — migrate every iflanguage/ifenglish site to the dispatcher     |
| `466302a` | step 3 — Spanish/French/Italian language packs                         |
| `bfd0b5d` | docs — multilingual support section in coppe.pdf                        |
| `ac33c92` | repo hygiene — untrack InstrucoesClaude/ and specs/                    |
| `f6508ff` | README — register the nlinguas multilingual proposal for CPGP          |
| `426e8e7` | norm — NORMA_COPPE_2026.md (minimal new CPGP norm)                     |
| `a01eb63` | version — bump to v4.0 (2026/05/28), changelog entries in the .dtx     |

---

## [3.8] — 2026-05-25

Final v3.x snapshot from the `coppetec-4.0` queue (the "CoppeTeX 4.0
queue" naming preceded the actual v4.0 multilingual release on
`nlinguas`). All ABNT post-2020 review items closed; bibliography
engine fully on biblatex/biber; `coppe.pdf` manual brought to current
state.

For the cumulative pre-4.0 history see the `\changes` entries embedded
in `coppe.dtx` and the git log on the `coppetec-4.0` branch.

---

## [3.x] — 2020 – 2026

Successive ABNT-conformance fixes, the biblatex/biber migration, the
new caption-on-top floats (Quadro / Programa / Algoritmo), the post-
2020 NBR 6023 / NBR 10520 updates, addition of the `english` option,
and minor v3.0–v3.7 maintenance releases. See `coppe.dtx` `\changes`
for entries.

---

## [Pre-3.0] — 2008 – 2019

Original CoppeTeX by Vicente Helano and George Ainsworth Jr., maintained
on the bibtex-based v1.x and v2.x lines. Pre-3.0 history is preserved in
the `coppetex-1.0`, `coppetex-2.0`, `coppetex-2.1` and `coppetex-2.2`
git branches.
