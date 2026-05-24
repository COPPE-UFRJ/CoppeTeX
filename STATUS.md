# CoppeTeX 4.0 — Phase 1 (Bibliography) status

_Last updated: 2026-05-24. Migration of the COPPE thesis bibliography from
BibTeX/natbib to a custom **BibLaTeX + biber** style implementing **post-2020 ABNT
NBR 6023** (per `specs/manual2024.pdf`)._

## Done

- **Stage 0 — baseline:** `src/example0.pdf` (old bibtex build, for diffing).
- **Stage 1 — extraction:** `howto.md` (full citation/reference/element spec +
  2018→post-2020 deltas), `desiredreferences.md`, `desiredelements.md`.
- **Stage 2 — mapping:** `mapping.csv` (ABNT→biblatex, EN + PT synonyms). NOTE: the
  thesis-family + games/report rows are reflected in the `.md` files but `mapping.csv`
  itself still shows the old single `thesis` row — it was locked (open in Excel) when
  the update ran. The replacement rows are in the chat; re-apply when it's closed.
- **Stage 3 (engine) — validated & working** as standalone files in `src/`:
  - `coppe.dbx` — datamodel: custom types `game/videogame/boardgame/tvshow`, custom
    fields `course/coppedegree/platform/artist/director/producer`.
  - `coppe.bbx` — ABNT bibliography style (derives from biblatex `standard`):
    surname CAPS, bold titles, `In:` for parts, `p.`/`f.`, article `v./n./p.` with
    no "In:", entry-by-title, plus a **biber source map** (PT→EN type/field synonyms
    and the thesis family) and the `type` bibstring resolver.
  - `coppe.cbx` — author-date citations (`authoryear-comp`, normal-caps names),
    plus `\citetapud`/`\citepapud` for *apud* citation-of-citation (§4.1.2.2.1).
  - `brazilian-coppe.lbx` / `english-coppe.lbx` — strings (Disponível em / Acesso em,
    thesis type words mscdiss/dscthesis/phdthesis/tcc, In).
- **Proof:** `src/example1.pdf` (see `src/examples.md`) compiles cleanly and renders
  correct ABNT for book, article, incollection, inproceedings, thesis, report, misc,
  the thesis family, PT-synonym entries, a corporate-author videogame, entry-by-title,
  and natbib `\citet`/`\citep`.

## What works (verified by compiling `src/example1.tex`)

author-date citations with normal-caps names · EN + PT entry-type/field synonyms ·
thesis family (generic `@thesis`/`@dissertation` need `type`; specific
`@masterdissertation`/`@dscthesis`/`@phdthesis`/`@tcc` preset a babel-aware type) ·
`@report` · custom `@videogame` + corporate author · ABNT list layout ·
*apud* citation-of-citation (`\citetapud`/`\citepapud`, §4.1.2.2.1).

## Remaining (next steps)

1. **`coppe.cls` integration (Stage 3a):** replace natbib with
   `\RequirePackage[backend=biber,datamodel=coppe,bibstyle=coppe,citestyle=coppe,natbib=true]{biblatex}`;
   reproduce the `bib:begin`/`bib:end` catalog labels via `\AtBeginBibliography` /
   `\AtEndBibliography` (the old `\thebibliography` redef is unused by biblatex).
   *Left for review because it changes the thesis-template build.*
2. **Migrate the thesis template** (`<example>` module) from `\bibliographystyle`+
   `\bibliography` to `\addbibresource`+`\printbibliography`; rebuild and diff against
   `example0.pdf` (todo §20).
3. **Embed the style files into `coppe.dtx`** as docstrip modules + update `coppe.ins`
   (todo §39–42: "generated from coppe.dtx"). Currently they live as direct `src/`
   files.
4. **Build scripts** `doall.bat` / `Makefile` / `latexmkrc`: bibtex → biber.
5. **Numeric + unsorted citation styles** (todo §21–22): add `coppe-numeric.cbx`
   (+ number labels in the bbx), selected by the existing `numbers` class option.
6. **Formatting refinements:** entry-by-title first-word CAPS; incollection editor
   `(org.)`; exact thesis `(Mestrado em <course>)` parenthetical using the `course`
   field; custom drivers for game/videogame/movie/tvshow (render `platform`/`artist`/
   `director`); the deferred exotic ABNT types (legal, scores, maps, 3D, etc.).

## Decisions taken autonomously (review/override welcome)

- `masterdissertation` primary + `mscdissertation` synonym; `dscthesis`≠`phdthesis`
  (D.Sc. vs Ph.D.); dedicated `course` field for "(… em <course>)"; PT synonyms as in
  `mapping.csv`/`desiredreferences.md`.
- Build on biblatex's stock `standard`/`authoryear-comp` (core biblatex, **not**
  `biblatex-abnt`), per your instruction.
