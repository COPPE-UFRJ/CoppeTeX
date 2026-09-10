# Changelog

Project changes worth noting, newest first. Follows
[Keep a Changelog](https://keepachangelog.com/) loosely; dates are
ISO-8601.

## [4.1] — 2026-09-10 — Conformance with the revised UFRJ/SiBI Manual (2026)

The September series aligned the class with the **9th edition, revised
(2026)** of the UFRJ/SiBI *Manual para Elaboração e Normalização de Trabalhos
Acadêmicos*, against which it had never been checked. That edition absorbs
three institutional decisions: exclusively digital deposit (CEPG Res.
246/2023), the writing languages of art. 57 of CEPG Res. 302/2024, and the new
CAPES data-collection sheet.

The item-by-item verification that produced this release is in
[`REVISAO_SIBI.md`](./REVISAO_SIBI.md); what changed for thesis authors is in
[`MIGRATION_v3_to_v4.md`](./MIGRATION_v3_to_v4.md), section 4; the proposal put
to the CPGP is [`PROPOSTA_CPGP.md`](./PROPOSTA_CPGP.md).

### Breaking changes

- **`\advisor`, `\coadvisor` and `\examiner` changed argument order.** The
  treatment (`Prof.`) was the first mandatory argument and the institution an
  optional one; now the treatment is the OPTIONAL argument and comes empty by
  default, and the institution is the last mandatory argument and may be left
  blank. 3.1.2.1.3(e) asks for name, titulação and institution, and asks for no
  treatment at all.

  ```latex
  \advisor{Ana}{Lima}{D.Sc.}{UFRJ}   % was \advisor[UFRJ]{Prof.}{Ana}{Lima}{D.Sc.}
  \examiner{Bia Sousa}{Ph.D.}{UFF}   % was \examiner[UFF]{Prof.}{Bia Sousa}{Ph.D.}
  ```

  To convert a document: drop the treatment from the front, drop the brackets
  from the institution, move the institution to the end. `MIGRATION_v3_to_v4.md`
  §4.4 has the rule and the two questions everyone asks.

- **Sans-serif is now the default.** `comserifa` restores the serif family.
  `semserifa` is still accepted and now does nothing, so a pre-4.1 document
  still compiles. Neither the Manual nor the COPPE norm prescribes a family,
  and the Manual itself is set in Arial.

- **No signature rules on the approval sheet.** The deposit has been digital
  only since CEPG Res. 246/2023, so there is nothing to sign by hand. The
  `assinaturas` option is still accepted and only warns.

### Added

- **`pdfa` class option** — PDF/A-2b output through `pdfx`, with the XMP
  metadata built from the document's own fields (Manual 2.2d). Validated by
  veraPDF 1.30.2, 144 rules.
- **Additional sheet with the catalog card** and the CAPES collection fields
  (3.1.2.1.2), mandatory since August 2026: `\fichacatalografica`, and
  `rascunhoficha` for a placeholder while the card is not yet issued.
- **`\coadvisor`** — the class had no coadvisor at all. The `coorientador`
  option additionally prints them on the abstract pages (off by default;
  the norm leaves it to each Programa).
- **Front page fields** — área de concentração, linha de pesquisa, subtitle,
  number of volumes, year of deposit.
- **Approval sheet** in the order of 3.1.2.1.3: date of approval, degree and
  institution of every member, advisor as president.
- **Keywords** at the end of all three abstracts (3.1.2.1.4).
- **Fifth heading level** numbered and formatted (2.6).
- **`listasnosumario`** — restores the pre-textual lists to the sumário, which
  3.1.2.1.6 keeps out of it.
- **`comserifa`** — restores the serif family, now that sans is the default.
  Neither the manual nor the COPPE norm prescribes a typeface: 2.2(b) fixes the
  colour, the body size 12 and the smaller uniform size of the four items it
  lists, and says nothing about the family — the SiBI manual that carries the
  rule is itself set in Arial. `lmodern` brings both families as vector fonts,
  so either way the document is PDF/A material, which `tests/test_comserifa.tex`
  proves by asking for `comserifa` and `pdfa` at once and going through veraPDF.
- **The CAPES sheet as a framed table** — Annex H draws the five fields inside
  a closed frame, one cell each, with nothing to write on. The class did loose
  paragraphs with dotted fill rules; it now draws the frame.
- **`\newcoppefloat` usable in practice** — it wrapped `\newfloat` in a group,
  and since `\newfloat` defines the environment locally the author's new float
  vanished as soon as the group closed. Its list also came out unnumbered and
  without leaders. Author-declared floats are now numbered within the chapter
  like every other illustration, and `example.tex` declares one (`mapa`) and
  uses it twice.
- **`morewrites` / `semmorewrites`** — under pdfTeX the class now loads
  `morewrites` on its own when it is installed; a document that uses every
  list needs seventeen of TeX's sixteen output streams.
- **Single source.** `pdflatex coppe.ins` generates *everything distributed*:
  the class, the biblatex styles, the language packs, the `.bib` bases, the
  `.ist`, the five per-language examples, `example_pdfa`, the cover montage
  and the `latexmkrc`. No derived file is maintained by hand.
- **Verification harness** (not distributed): `tools/build-check.ps1` with
  scopes, `tools/watch-build.ps1`, `tools/prova.ps1` (the release proof),
  `tools/mk-adversativa.py`, and `tools/conferir-norma.py`, which measures the
  finished PDF against the Manual in centimetres and in order.
- **`adversativa/`** (not distributed) — twelve complete documents, four work
  types × three languages, each exercising everything the class offers at
  once, compiled under both engines.
- **`NORMA_COPPE_2026`** rewritten as a *differences* document against the
  UFRJ Manual, and **`PROPOSTA_CPGP.md`**, the text put to the CPGP for a vote.

### Changed

- **One-sided layout, 3 cm left margin** (2.3) — mirrored margins lost their
  normative basis when the 2026 edition dropped the verso margins.
- **Continuous pagination from the folha de rosto**; the Introduction is no
  longer folha 1 (2.7).
- **Folio in 10 pt** (2.2b) and positioned 2 cm from the top and right edges —
  measured on the rendered ink, not on font metrics.
- **Pre-textual lists out of the sumário** (3.1.2.1.6), which now opens at the
  first numbered section.
- **The sumário is the manual's, not `book`'s** (2.6 and 3.1.2.1.6). Every
  indicative starts at the left margin and every title in a single column,
  whose position is measured from the document's own widest indicative and
  carried through the `.aux` — literally "a margem do título do indicativo mais
  extenso". Dotted leaders on every level, uniform line spacing, and the
  per-level graphic treatment of the body reproduced: primary in bold caps,
  secondary in caps, tertiary bold, quaternary bold italic, quinary italic.
  Only the first two levels had been reproduced before.
- **Apêndice and Anexo headings centred** (2.6) — a letter is not a numeric
  indicative.
- **Latin Modern** instead of the bitmap fonts: the whole document was coming
  out in Type 3, which made PDF/A impossible.
- **Typography** — first-paragraph indent, `section` titles no longer bold,
  sumário typeset like the body, algorithm captions with an em dash, one
  caption alignment throughout, and the end of the example's 17 overfull
  boxes.
- **Approval-sheet spacing scales with the board**, from five members up to
  eight, so a large board still fits on one sheet.
- **Documentation** — every class option is now documented (half of them were
  not, `pdfa` and `assinaturas` included), and an error by a factor of four
  was removed: the long quotation is indented 4 cm *beyond* the margin, not
  set with a 4 cm margin.

### Fixed

- **The `pdfa` option had never been compiled in a real document** and worked
  in none: it wrote the `.xmpdata` before `\title` and `\author` existed, it
  exhausted TeX's sixteen output streams in `example.tex`, a bad pass recorded
  a control-sequence name into the `.xmpdata` and left the file unusable until
  someone deleted it by hand, and every code listing died because `pdfx` puts
  `xcolor` in conversion mode and the `\textcolor` in `postbreak` failed on the
  first broken line.
- **`\pdfsuppressptexinfo` under LuaTeX** — the primitive does not exist
  there; `\pdfvariable suppressoptionalinfo` takes its place, with the bit
  value that keeps the trailer `/ID` that PDF/A requires.
- **Cover overflowing under `doublespacing`**, and the overflow sheets
  printing a folio in the pre-textual part, which 2.7 forbids. The cover and
  the folha de rosto are institutional templates and now compose in single
  spacing whatever the body uses.
- **`\thispagestyle` covering only one page** — when the approval sheet
  overflowed, the extra sheet inherited the current style and came out
  numbered.
- **The indicative printed over the title in the sumário.** `\@dottedtocline`
  gives each level a fixed-width box for the number; a thesis with ten chapters
  reaches indicatives such as `10.10.10.10`, which overflowed the box by up to
  4.6 mm and ran across the title — the opposite of 2.6's "separado por um
  espaço". The measured column removes the ceiling. Covered by the new
  `tests/test_sumario.tex`, which forces two-digit numbering at all five
  levels; no sample document had ever produced the shape.
- **Period in the Spanish sumário indicative** — with Spanish as the main
  language, babel redefines `\numberline` and the sumário read "2.1. SECCIÓN"
  while the heading read "2.1 SECCIÓN". `es-nosectiondot`, applied through the
  new `\coppe@babelextra@<lang>` hook, turns off that one adjustment.

### Bibliography styles checked against the manual's own examples

`adversativa/referencias-manual.bib` carries one entry for **each of the 34
reference categories of section 4.2** of the manual, with the manual's own
example data, and the `%%` comment above each entry is the reference **as the
manual prints it**. `tools/conferir-referencias.py` compares the two. The first
measurement found **31 divergences in 34 categories**; the styles had never
been checked against anything but their author's memory. The run of record now
reads **0 divergences, 3 accepted** — each accepted one marked `%%!` in the
`.bib` with its reason.

What that took:

- `Disponível em: <url>. Acesso em: <data>.` — biblatex parenthesises the
  access date and drops the colon; the manual does neither. Physical
  description ("1 carta") moved ahead of the electronic block.
- A final period on `standard`, `music`, `audio`, `video`, `software`, `image`,
  `artwork`, `performance` and `dataset`: all nine are `\usedriver` aliases,
  and `\usedriver` disables the called driver's `\finentry` expecting the
  caller to close the entry — nobody did.
- "maio" is not abbreviated (4.3), and a month range takes a slash.
- The period after "Anais [...]" and the comma after an abbreviated journal
  title: biblatex's punctuation tracker swallowed both.
- **New drivers**: `periodical` (whose title printed as *nothing*, because the
  `title` bibmacro goes through the `titlecase` format and an author-less
  periodical produced no output), `proceedings` and `inproceedings` (with
  `eventtitle`/`venue`/`eventdate` so the event name is set in capitals ahead
  of the proceedings title), and `online` (which never printed the location).
- **Corporate authors** now follow 4.3.2.13: a name containing a period or a
  parenthesis prints as the author typed it, everything else goes to capitals.
  The style cannot know whether "Associação Brasileira de Normas Técnicas" is
  one entity or "Brasil. Supremo Tribunal Federal" has a subordinate organ —
  the author can.
- Theses in the shape of 4.2.1.1, patents with filing and grant dates,
  legislation with the volume, number and pages of its vehicle, maps without
  the stray colon when there is no publisher.

### Fixed (found by the extended adversarial document)

- **`\glossaryname` leaked out of `\printlosymbols`.** The `\renewcommand`
  sat outside the `\begingroup`, so after the list of symbols every later use
  of `\glossaryname` — the post-textual Glossário of 3.1.4.2 and its sumário
  entry — came out titled "Lista de Símbolos". Only a document carrying both
  the pre-textual lists and the glossary can show it, and none did until one
  was built for it.

### Verification

Everything above is proved by one command, `tools/prova.ps1`, which regenerates
the distribution from the `.dtx`, checks by git that no derived file diverged,
compiles the whole distribution, the regression suite and the twelve
adversarial documents under **both engines**, and runs veraPDF over every
PDF/A. `tools/conferir-norma.py` then measures the finished PDFs against the
Manual. See the release notes in the pull request for the run of record.

### Backward compatibility

- The user-facing API of v4.0 is unchanged; every new element is a new command
  or an option that is off by default.
- Documents written for v3.x/v4.0 keep compiling. What changes is the
  *rendering* of the pre-textual pages, which is the point of the release: the
  pagination now starts at the folha de rosto, the sumário no longer lists the
  pre-textual lists, and the approval sheet carries the fields 3.1.2.1.3
  requires. Authors who need the previous sumário can pass `listasnosumario`.

---

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

### Fixed

- **Catalog-label writers crashed every Spanish-main document** with
  `! Emergency stop. <inserted text> }\endwrite` at `\mainmatter`.
  `\coppe@mainBegin` / `\coppe@bibBegin` / `\coppe@bibEnd` / `\coppe@hasLof`
  used `\roman{page}` inside `\immediate\write\@auxout{...}`, which
  Spanish babel redefines (via `\@roman` → `\es@scroman` →
  `\es@xlsc\uppercase\@firstofone`) to produce small-caps roman; that
  expansion contains an `\uppercase` group that is unbalanced inside
  `\write` and aborts pdfTeX. Fixed by switching the four writers to
  the raw e-TeX primitives `\romannumeral` and `\number` operating on
  `\c@page` (language-agnostic) and by wrapping the label names
  themselves in `\detokenize{...}` so the `:` and `.` they contain
  survive any future babel that activates them. `example_es.pdf` and
  the historical pt-main `example.pdf` now build cleanly again.

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
