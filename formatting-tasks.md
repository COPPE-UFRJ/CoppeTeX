# Formatting tasks — unified list (TODO2 steps 0–2)

Single, actionable list for **Phase 2 (formatting)**, reconciling:
- `rules.md` — rules extracted from `manual2024.pdf` ch. 1–3 (`R#`);
- `specs/propostaregrasmanual2024.txt` — the user's LaTeX-implementation proposal (`P#`);
- the **current `src/coppe.cls`** state (audited).

Guiding rule (proposta P0): **keep the original behaviour; change only where the new rule differs.** Each task is marked **KEEP** (already compliant), **CHANGE** (modify existing), or **ADD** (new), with the target value and where it lives in `coppe.cls`.

Legend for "side" math: proposta uses `geometry` `left=right=2cm` + `bindingoffset=1cm` + `twoside`, which yields **inner = 3 cm, outer = 2 cm** — exactly the manual's mirrored anverso/verso margins (R13/R14).

---

## A. Page geometry & sides

| # | Task | Now (coppe.cls) | Action | Source |
|---|------|------|--------|--------|
| F1 | A4 paper | `a4paper` (l.58, l.69) | **KEEP** | P1, R5 |
| F2 | Top margin 3 cm | `top=2.5cm` | **CHANGE** → `top=3cm` | P12, R13 |
| F3 | Bottom margin 2 cm | `bottom=2.5cm` | **CHANGE** → `bottom=2cm` | P13, R13 |
| F4 | Left/right 2 cm | `left=3cm,right=3cm` | **CHANGE** → `left=2cm,right=2cm` | P13 |
| F5 | Binding offset 1 cm | `bindingoffset=0cm` | **CHANGE** → `bindingoffset=1cm` | P14, R14 |
| F6 | Drop vertical centering | `vcentering=true` | **CHANGE** → remove | P12–15 |
| F7 | Use `geometry` | loaded (l.69) | **KEEP** | P15 |
| F8 | Two-sided body (anverso+verso) | `\LoadClass[...,oneside]{book}` | **CHANGE** → `twoside`; keep pre-textual front-only (blank versos via `\cleardoublepage`) | P8–11, R10–11 |

## B. Line spacing

| # | Task | Now | Action | Source |
|---|------|-----|--------|--------|
| F9 | 1.5 spacing (textual), `setspace` | `setspace` + `\onehalfspacing` (l.63,114) | **KEEP** | P17, R15 |
| F10 | Single spacing: long quotes, footnotes | `longquote`→`\singlespacing` (l.701); footnotes default `\footnotesize`+single | **KEEP** (verify footnotes) | P18, R16 |
| F11 | Single spacing: references, captions, fontes, ficha, folha-de-rosto data | partial | **CHANGE/ADD** per element | P19, R17 |
| F12 | References separated by one blank line | bib `\bibitemsep=\baselineskip` (coppe.bbx l.159) | **KEEP** | P20, R17 |

## C. Fonts

| # | Task | Now | Action | Source |
|---|------|-----|--------|--------|
| F13 | Base 12 pt | `12pt` (l.58) | **KEEP** | P2, R7 |
| F14 | Long quotes (>3 lines) `\footnotesize` | `longquote`→`\footnotesize` (l.698) | **KEEP** | P4, R8 |
| F15 | Footnotes `\footnotesize` | book 12pt default | **KEEP** (verify) | P5, R8 |
| F16 | Captions / sources / legends `\footnotesize` | default size | **CHANGE** → smaller caption font (e.g. `caption` pkg `font=footnotesize`) | P6, R8 |

## D. Citations & quotes

| # | Task | Now | Action | Source |
|---|------|-----|--------|--------|
| F17 | `\enquote` for quotes | csquotes not loaded | **ADD** → load `csquotes` | P3 |
| F18 | `\citacao` PT command (short, inline quote) | none | **ADD** → map to `\enquote` (+ cite) | P3 |
| F19 | Long quote = >3 lines, 4 cm indent | `longquote`, `\recuolongquote=4cm` (l.694–703) | **KEEP** (4 cm now *recommended* by NBR 10520:2023) | P7, R9 |

## E. Section / heading formats (TOC + body) — proposta P22–23

Target levels (define down to **subsubsubsection**, P23):
| Level | Format |
|-------|--------|
| chapter | ALL CAPS, **bold** |
| section | ALL CAPS, normal weight |
| subsection | Title Case, **bold** |
| subsubsection | Title Case, ***bold italic*** |
| subsubsubsection | *italic*, only first word capitalised |

| # | Task | Now | Action | Source |
|---|------|-----|--------|--------|
| F20 | Heading formats per level (above) | book defaults (no custom) | **CHANGE/ADD** → `titlesec` (and ToC via `tocloft`/`titletoc`) | P22 |
| F21 | Define `subsubsubsection` | not defined (book stops at subsubsection) | **ADD** | P23 |
| F22 | Numeric indicative left-aligned; unnumbered headings centred | mixed (`\chapter*` used for unnumbered) | **CHANGE** → ensure centred unnumbered + left-aligned numbered | P29, R25–26 |
| F23 | Unnumbered (centred) headings: errata, agradecimentos, lists, resumo, sumário, referências, glossário, apêndice, anexo, índice | partly `\chapter*` | **KEEP/CHANGE** as needed | P30, R26 |

## F. Pagination — proposta P25–26

| # | Task | Now | Action | Source |
|---|------|-----|--------|--------|
| F24 | Count from folha de rosto, not numbered until textual | `\pagenumbering{alph/roman}` front; ficha not numbered | **KEEP** | R38–39 |
| F25 | Arabic numbers from first textual leaf | `\pagenumbering{arabic}` in `\mainmatter` (l.255) | **KEEP** | P25, R40 |
| F26 | Number at **top-right, 2 cm from top & right** (anverso); top-**outer** when two-sided | `\pagestyle{plain}` = bottom-centre | **CHANGE** → custom page style (top-outer), e.g. `fancyhdr`/`geometry` headsep | P25–26, R40–41 |

## G. Front matter (title page, ficha, order)

| # | Task | Now | Action | Source |
|---|------|-----|--------|--------|
| F27 | **Two logos** on title page (UFRJ + COPPE) | one logo `coppe-logo` (l.270) | **CHANGE** → add `ufrj-logo` (`specs/ufrj-logo.pdf` → copy to src) | P28 |
| F28 | Ficha catalográfica on verso of folha de rosto | `\makecatalog` (l.415) | **KEEP/verify placement** | P10, R57 |
| F29 | Pre-textual order: capa, folha de rosto, errata, aprovação, dedicatória, agradecimentos, epígrafe, resumo, abstract, listas, sumário | provided piecemeal; order set by `example.tex` | **CHANGE** → align `example.tex`; ensure all pieces exist | proposta §order, R55 |

## H. Lists & special commands

| # | Task | Now | Action | Source |
|---|------|-----|--------|--------|
| F30 | `alíneas` environment: a) b) c) lowercase letters | none | **ADD** → `enumerate`-based env | P24, R33–34 |
| F31 | `\sigla` command: first use prints "full form (ACRONYM)" **and** registers in list of abbreviations | `\abbrev`/`\makeloabbreviations` register only (l.629) | **ADD/EXTEND** → first-use expansion + auto-register | P27, R43 |
| F32 | Lists of illustrations/tables/abbreviations/symbols | `\listoffigures`,`\listoftables`,`\printlosymbols`,`\printloabbreviations` (l.572–651) | **KEEP** | R67–70 |

## I. Floats & source ("Fonte:")  — manual §2.10–2.11 (R46–53)

| # | Task | Now | Action | Source |
|---|------|-----|--------|--------|
| F33 | Caption **above** float | default `book` (caption follows author placement) | **CHANGE** → enforce caption-on-top for figure/table/quadro | R46, R51 |
| F34 | `\source{}` / `\fonte{}` line **below** float, not numbered, doesn't advance counter; `\abntsource` if clash | none | **ADD** | R48, R52 (TODO2 phase-2 feature) |
| F35 | `quadro` float ("Quadro") + `\quadro` BR alias; long tables via `longtable` with `\source` | none | **ADD** | R53 |

## J. Post-textual

| # | Task | Now | Action | Source |
|---|------|-----|--------|--------|
| F36 | Reference list titled **"Referências"** (not "Bibliografia") | brazilian `\bibname` = "Bibliografia" (babel default); english="References" (l.125) | **CHANGE** → brazilian `\bibname`="Referências" | R73 |
| F37 | Apêndice / Anexo: consecutive UPPERCASE letters + travessão + title | `\appendix`, `\annex` (l.797) | **KEEP/verify** lettering & title format | proposta §pós, R75–76 |
| F38 | Chapter/appendix/annex title formats identical | n/a | **KEEP** (follows F20) | proposta §pós |

## K. Languages & meta

| # | Task | Now | Action | Source |
|---|------|-----|--------|--------|
| F39 | babel; PT ⇒ `brazilian` | `[english,brazilian]`/`[brazilian,english]` (l.119–123) | **KEEP** | P16 |
| F40 | Allow Portuguese/English (Spanish noted by manual, not required now) | PT+EN | **KEEP** | R4 |
| F41 | Bump class version to **3.8** | `\fileversion{v3.4}` (l.54) | **CHANGE** (end of phase) | TODO2 |

---

## Significant / opinionated changes to confirm before implementing
These change the document layout substantially (large diff vs `baseline.pdf`):
1. **F8 twoside + F2–F6 margins/bindingoffset** — switches the whole document to mirrored two-sided layout.
2. **F26 page-number position** — moves numbers from bottom-centre to top-outer on every page.
3. **F20–F22 heading formats** — restyles all chapter/section headings and the ToC.
4. **F27 second logo**, **F34 `\source`**, **F36 "Referências"**.

Everything else is either already compliant (KEEP) or a localized addition.
