# Changelog

Project changes worth noting, newest first. Follows
[Keep a Changelog](https://keepachangelog.com/) loosely; dates are
ISO-8601.

## [Unreleased] — Full check against the UFRJ/SiBI Manual (2026)

On 2026-09-16, version 4.1 was checked in full against the Manual (9th ed.
rev., 2026) and the CAPES additional-sheet model. Each defect found has one
issue (#113–#152, umbrella #112) and a minimal test in `tests/regressivo/`
(`rt33`–`rt70`, `rt89`) that fails until the fix lands. The fix plan is
`CORRECOES_MANUAL_2026.md`. A test still waiting for its fix carries an
`ABERTO: #<issue>` mark: the unfiltered regression run lists it but does not
run it, and the fix removes the mark.

### Verification

- **The proof now runs the two checkers that compare the finished PDF with the
  Manual** (#151). `conferir-norma.py` (sheet, folio, margins, sumário) and
  `conferir-referencias.py` (each reference against the Manual's own
  examples) were in neither `coppetex.bat --conferir` nor `build-check.ps1`,
  so the m-diss reference shipped wrong in 4.1 while the checker reported the
  divergence to no one. Both now run in `--conferir`, and in `build-check.ps1`
  right after the examples and the adversarial documents are compiled.
  Without arguments, each knows which PDFs to read. Each reads a document with
  one `pdftotext` call instead of one per page, which cuts 174 s to about 20 s.
  On their first run they found the m-diss divergence (#147) and a LuaLaTeX
  defect (#152).
- **The Portuguese field names are checked again** (#147). The 34 Manual
  references exist in two databases: `exemplo.bib`, with English field names,
  and the adversarial `referencias-manual.bib`, with the Portuguese synonyms
  (`@livro`, `autor`, `curso`…). They shared their keys. Biber found every
  citation in the first file and never opened the second, so the Portuguese
  form was never composed. The keys are now `m-<item>` and `pt-<item>`, and
  the Portuguese adversarial documents cite both. `conferir-referencias.py`
  reads the expected text from both databases and ties each `[n]` to its key
  through the `.bbl`, instead of guessing from the start of the text. The
  result: 68 checks, no divergence, and the same three accepted ones in each
  form.

### Changed

- **The area de concentracao leaves the folha de rosto and the folha de
  aprovacao** (#155). The class used to append "Área de concentração: …" to the
  natureza block of both identity sheets, on the strength of the prose in
  3.1.2.1.1(e) and 3.1.2.1.3(c). The SiBI's own model — the two sheets that
  3.1.2.1.2 links to, kept in `specs/` — carries the area on the **folha
  adicional**, as the Coleta CAPES field "Área de concentração da produção
  intelectual", and shows a folha de rosto without it; Annexes B and D end the
  natureza block at the degree. The model wins. The new option
  `areanafolhaderosto` brings the sentence back to both sheets for a Programa
  that requires it, and `ufrj-coppe` does not set it. `\concentrationarea` is
  unchanged and still mandatory for the folha adicional.
- **Headings are set in the body size** (#113). 2.2(b) of the UFRJ Manual fixes
  size 12 for the work and allows only smaller sizes (long quotations, notes,
  folio, captions and sources, catalogue card). 2.6 builds the gradual emphasis
  from bold, italic and capitals, not from size. Chapters and unnumbered
  headings (RESUMO, SUMÁRIO, REFERÊNCIAS…) were `\Large` (17.28 pt), sections
  `\large` (14.4 pt), and the two headings of the CAPES additional sheet
  `\large`. The gradation is unchanged: chapter bold capitals, section
  capitals, subsection bold, subsubsection bold italic, paragraph italic.
- **One blank line before and after section headings** (#122), as 2.4 asks,
  for section, subsection, subsubsection and paragraph. titlesec's default
  left 2.3 ex after the heading, about two thirds of a line at 1.5 spacing.
  Documents get a little longer, and page breaks move.
- **Post-textual entries line up with the titles in the sumário** (#115).
  REFERÊNCIAS, APÊNDICE A – …, ANEXO A – …, the glossary, the index and, under
  `listasnosumario`, the pre-textual lists started at the left margin. They now
  start in the column of the numbered titles. 3.1.2.1.6 aligns titles by the
  longest indicative, post-textual elements included, and the Manual's own
  sumário does so. Section 14 of the COPPE norm already stated it as a rule.
- **The em dash (—) between number and title, everywhere** (#150): captions
  ("Figura 4.1 — Título"), algorithm captions, appendix and annex headings
  ("APÊNDICE A — Título"), their sumário entries and the lists of
  illustrations. The Manual calls the sign *travessão* (2.10, 3.1.2.2.4,
  3.1.4.3, 3.1.4.4), and section 12 of the COPPE norm shows the em dash. The
  class used the en dash almost everywhere and the em dash in the thesis
  reference. This was a maintainer's decision recorded in the issue, and it is
  easy to revert.
- **Lists of illustrations and of tables name each item** (#116): "Figura 4.1
  — Título ….. 27" instead of "4.1 Título ….. 27", as 3.1.2.2.4 and 3.1.2.2.5
  ask, for figures, tables, quadros, programs, algorithms and every float made
  with `\newufrjfloat`. A long title continues at the left margin, as in the
  Manual's example.
- **The lists come in the order of 3.1.2** (#148): every list of illustrations
  (figures, quadros, maps, programs, algorithms) first, then the list of
  tables. `max-exemplo.tex`, `manual.tex`, the document generator, the
  adversarial documents, the class manual and the quick reference had the list
  of tables second. Section 10 of the COPPE norm placed its three lists between
  tables and abbreviations; it now places them with the other illustrations,
  since 2.10 counts quadros, programs and algorithms as illustrations. The class
  imposes no order, so an existing document keeps the order its author wrote.
- **Abstract sheets have a heading** (#114): RESUMO, ABSTRACT or RESUMEN, in the
  language of each sheet, centred in bold capitals like every heading without a
  numeric indicative (2.6). The sheets used to open straight on "Resumo da Tese
  apresentada à COPPE/UFRJ…". The heading cannot be switched off; the four
  optional elements below it still can.

### Fixed

- **LuaLaTeX printed "nº" as "nž"** (#152). The class loaded `fontenc` with T1
  under every engine. A Unicode engine sends each input character straight to
  the font, and in T1 the slot of `º` holds `ž`. So under LuaLaTeX, `º ª § ° « »
  ± × µ · ² ½ ¿ ¡` printed as other letters (`ž ł ğ ř ń ż ś Œ ţ ů š ¡ £ ą`), and
  `— – “ ” ‘ ’ … € œ Ł ő` vanished, with only a "Missing character" line in the
  log. Portuguese accented letters were right, because T1 matches Latin-1
  there, so nobody saw it. Unicode engines now keep TU, LaTeX's default for
  them, with the same Latin Modern in OpenType. The shape declarations that
  keep substitution messages out of the log exist for TU too. The fixed
  typewriter fonts of the language listing styles (`\pythonstyle`,
  `\xmlstyle`…) use Latin Modern Mono under LuaLaTeX, because txtt has no
  OpenType version. pdfLaTeX output does not change. The LuaLaTeX adversarial
  twin now matches the Manual's references with no divergence and is still
  PDF/A-2b.
- **`exemplo.bib`: the master's dissertation example** (`m-diss`) printed
  "1997. 203 f. Memória Social e Documento Centro de Ciências Humanas…",
  without "Dissertação (Mestrado em …)" or the dash (4.2.1.1). The course was
  in `type`, and the `mscdiss` type was missing (#147). The comments in
  `exemplo.bib` and the class manual also said half the entries used the
  Portuguese synonyms, but none has since the database moved to English names.

### Documentation

- **The abstract does not have to fit on one sheet** (#153). The class manual,
  `manual.tex`, a regression test and section 8 of the COPPE norm said that
  3.1.2.1.4 of the UFRJ Manual requires it. The 2026 Manual asks for 1.5
  spacing, a single paragraph and 150 to 500 words, and says nothing about the
  number of sheets. A 500-word abstract with all five elements takes more than
  one A4 sheet anyway. `resumosemreferencia` and `\setupabstracts` remain for
  whoever prefers a single sheet.

## [5.0] — 2026-09-15 — The UFRJ class and the COPPE unit style

The class that was `coppe` is now **`ufrj`**, and implements the UFRJ/SiBI
Manual only. Everything that belongs to COPPE — the institute's name, the
thirteen Programas, the right-hand logo, the phrases the Norma COPPE fixes, the
norm the colophon cites — moved out of the class into the **unit style
`ufrj-coppe`**. Another unit of UFRJ gets its own style and the class does not
change. A COPPE document keeps its pages except for the colophon sentence that
names the class, and a work begun with `\documentclass{coppe}` compiles as it
is. What to change, and when, is in
[`MIGRATION_v4_to_v5.md`](./MIGRATION_v4_to_v5.md).

### Breaking changes

- **The class is `ufrj`, and so is every file generated from it**: `ufrj.cls`,
  `ufrj.bbx`, `ufrj.cbx`, `ufrj.dbx`, `ufrj-numeric.bbx`/`.cbx`,
  `brazilian-ufrj.lbx` and the other language packs, `ufrj-lang-spanish.def`
  and the other two, `ufrj.ist`, `ufrj.bib`, and the manuals `ufrj.pdf` and
  `ufrj-quickref.pdf`. The sources are `src/ufrj.dtx` and `src/ufrj.ins`.
- **A COPPE work starts with two lines**:

  ```latex
  \documentclass[dsc]{ufrj}
  \usepackage{ufrj-coppe}
  ```

  Without the style, `\department{PESC}` stops with
  ``Class ufrj Error: Programa `PESC' nao declarado``: a department code that no
  unit declared is now an error, where 4.1 printed a cover without the Programa.
- **`coppe.cls` is now a compatibility class** of a few lines. A 4.1
  `coppe.cls` left in the work's folder keeps loading 4.1, and must be replaced;
  so must a 4.1 `latexmkrc`, which runs makeindex with `coppe.ist`.
- **A language pack written by an author** must be renamed
  (`ufrj-lang-<language>.def`, `<language>-ufrj.lbx`) and loses what is
  institutional: the keys `universityname`, `cityname`, `statename` and
  `countryname`, which no code ever read, are gone, and the start of
  `abstracttail` ("à COPPE/UFRJ") is the new key `tounit`.

### Added

- **The unit interface**, public and documented in `ufrj.pdf`, section "A
  instituição e a unidade": `\ufrjdeclareunit`, `\ufrjdeclareprogram`,
  `\ufrjdeclarelogos`, `\ufrjdeclarenorm` and `\ufrjdefunitstring`. The texts of
  a unit live in their own table, which wins over the class's and the language
  packs' whichever was loaded first.
- **`src/ufrj-coppe.dtx` and `src/ufrj-coppe.ins`**: the COPPE style, the
  compatibility class, and every example document — `min-exemplo.tex`,
  `max-exemplo.tex`, the five per-language examples and the covers sheet —,
  with their own manual, `ufrj-coppe.pdf`. `ufrj.ins` generates no document.
- **The class alone composes a work of UFRJ**: the cover reads "Programa de
  Pós-Graduação em …", the abstract says the work was presented "à UFRJ", the
  colophon cites the SiBI Manual, and the Programa is declared in the preamble
  with `\ufrjdeclareprogram`. It is the way for a unit that has no style yet.
- **The old names keep working** while `ufrj-coppe` is loaded:
  `\copperdefstring`, `\coppestring`, `\coppemainstring`,
  `\coppeforeignstring`, `\usecoppelanguage`, `\newcoppefloat`,
  `\coppetexfinalpage`, the six colophon pieces `\coppefinal…` (a
  `\renewcommand` by the old name still changes the colophon), the page style
  `coppe`, the `.bib` field `coppedegree`, and the internal names that `.toc`,
  `.lab` and the list files written by 4.1 contain, so the first compilation
  after the update reads them without error.
- **Four regression tests of the split.** `rtu01` composes a work with the class
  alone and forbids every COPPE phrase in the PDF; `rtu02` composes one with a
  made-up unit style that uses only the public interface; `rtu03` compiles a 4.1
  work — `\documentclass{coppe}`, old names, a `.toc` written by the old class;
  `rtu04` reads the class, the bibliography styles, the language packs and the
  glossary style that `ufrj.ins` generates, and fails if one names COPPE or any
  of its data.

### Changed

- **The colophon names the class and the project apart**: "Foi utilizada a
  classe ufrj, do projeto CoppeTeX, versão v5.0". It said "a classe CoppeTeX",
  and CoppeTeX is the name of the project, not of a class. `manual.pdf` and
  `max-exemplo.pdf`, which also said "classe CoppeTeX", say the same.
- **The norm the colophon cites is the unit's**, declared with
  `\ufrjdeclarenorm`: the Norma COPPE under `ufrj-coppe`, the UFRJ/SiBI Manual
  with no unit.
- **The documentation follows the split.** `ufrj.pdf` is the class and the
  interface a unit style uses; `ufrj-coppe.pdf` is only what COPPE declares, the
  table of the thirteen Programas, the old names and how to start a new unit;
  `manual.pdf` is the norm of UFRJ with COPPE as the example, with a new chapter,
  "O que é de cada unidade". `CONTRIBUTING.md` has a section on adding a unit
  style.
- **`NORMA_COPPE_2026`**, section 16, names the class `ufrj` with the style
  `ufrj-coppe` as the implementation of reference from 5.0 on.
- **The tools know both sources**: `tools/build-check.ps1` runs both `.ins` and
  composes both manuals, and `painel.py`, `versao.py`, `conferir-manual.py`,
  `geradocvazio.py` and `mk-adversativa.py` handle the style, the compatibility
  class and the second `.dtx`. The empty-document generator writes
  `\usepackage{ufrj-coppe}`.

### How it was checked

Three steps, each compared with the state before it through an image of every
page of the 33 documents built: COPPE isolated in one block of the `.dtx`
(`22e7dc9`, all 33 identical, and also word by word, with coordinates, and in
the XMP), the rename (`fc0eb20`, the differences only in text that names the
class) and the two sources (`547bf45`, only `max-exemplo` differs: the code it
shows gained the line `\usepackage{ufrj-coppe}`).

## [4.1] — 2026-09-14 — Revision of the 4.1 release

Still version 4.1: these are corrections to the release published on
2026-09-10, and the release archive was rebuilt from `dist/`.

### Breaking changes

- **The class no longer loads a math font.** `amssymb` used to come with the
  class under pdfLaTeX, and the class warned under LuaLaTeX when neither
  `amssymb` nor `unicode-math` was loaded. The math font is now the author's
  choice. A document that uses `\mathbb`, `\hbar`, `\varnothing` and friends must
  load it in the preamble; `example.tex` and the empty-document generator carry
  the block that picks by engine (#90):

  ```latex
  \ifPDFTeX
    \usepackage{amssymb}
  \else
    \usepackage{unicode-math}
    \setmathfont{Latin Modern Math}
  \fi
  ```

- **The licence file is `COPYING.txt`.** Overleaf does not open a file without
  an extension.

- **The advisors head the board on the approval sheet by default.** 3.1.2.1.3(e)
  of the UFRJ Manual says "o orientador deve aparecer em primeiro lugar, por ser o
  presidente da banca", and the class used to leave the advisor out unless
  `orientadorexamina` was given. The new option `semorientadornabanca` lists
  the examiners only; `orientadorexamina` is still accepted and does nothing.

- **Links have no highlight by default.** hyperref's own default drew a frame
  around every link (red, green, cyan), which TeXstudio and Foxit show, and
  2.1(b) of the UFRJ Manual wants the text in black. Links stay clickable. New
  options: `linkscommoldura` (on-screen frame, not printed) and
  `linkscoloridos` (coloured link text, against 2.1(b)). `semlinks` is still
  accepted and now confirms the default. A `\hypersetup` in the preamble wins
  over all of them.

- **`listasnosumario` is documented as against the norm.** NBR 6027 keeps the
  pre-textual elements out of the sumário, and the UFRJ Manual's model
  sumário (3.1.2.1.6) opens at "1 INTRODUÇÃO". The option stays, off by
  default, for a Programa that requires the opposite; `coppe.pdf`,
  `manual.tex`, `max-exemplo.tex` and the document generator now say so. The
  generator also offers `semorientadornabanca` instead of the no-op
  `orientadorexamina`.

- **`example.tex`, `example.bib` and `tipos.bib` are gone.** In their place:
  `min-exemplo.tex` (only what the norm makes mandatory), `max-exemplo.tex`
  (everything the class offers) and one database, `exemplo.bib`. `manual.tex`
  has its own `manual.bib`, with the same entries it always printed (#102).

### Added

- **Automatic glossary** (3.1.4.2): `\makeglossarylist` in the preamble,
  `\glossaryterm[key]{term}{definition}` where the term appears,
  `\printglossarylist` after the references. Alphabetical, accents included,
  same look as the hand-written `theglossary`, which keeps working. The
  document generator offers both forms.
- **The class runs makeindex by itself** at the end of every compilation
  (restricted shell escape, on by default in MiKTeX and TeX Live), so the lists
  of abbreviations, acronyms and symbols, the glossary and the index appear in
  TeXstudio, TeXworks or any editor that runs only pdflatex. Before, they came
  out empty without `latexmk`. Option `semmakeindex` turns it off.
- **Index entries sort alphabetically with accents.** makeindex sorts by byte,
  and every accented word landed after "z". The class gives each accented
  level of an entry an unaccented sort key; an author's own `key@entry` always
  wins. Works with `makeidx` and `imakeidx`, pdfLaTeX and LuaLaTeX. The index
  cross-references read "ver" / "ver também" (NBR 6034) instead of babel's
  "veja".
- **`max-exemplo.tex`** explains the glossary and the index in both forms
  (automatic and manual), several indexes with `imakeidx`, and titles the
  index by its function as NBR 6034 asks ("Índice de Assuntos"). It gains a
  section with a definition, a lemma, a theorem, a corollary, an example and a
  remark (`amsthm`, Cauchy–Schwarz), and text in the chapters, appendices and
  annexes that were empty. `manual.tex` has a new chapter, "Glossário e
  índice"; `coppe.pdf`, a new section.

### Changed

- **The examples are titled by what they are**: "TÍTULO DO TRABALHO: um
  exemplo mínimo de uso do CoppeTeX", "…máximo…", "…em inglês", "…en
  español", with the second half as the subtitle.
- **Every listing breaks long lines**, not only the language styles: a plain
  `lstlisting` wraps too, and the continuation starts after a curved arrow
  (↪). The arrow is black by default; the new option `setavermelha` makes it
  red, as it always was before.
- **The long table's last page says "(conclusão)"**, not "Continua na próxima
  página"; intermediate pages say "(continua)" and "(continuação)", the IBGE
  tabular terms the Manual follows.
- **Every command has an English name**, and the shipped documents use them:
  `\defineacronym`, `\useacronym`, `\makeloacronyms`, `\printloacronyms`,
  `\approvaldate`, `\concentrationarea`, `\researchline`, `\productiontype`,
  `\linkedproject`, `\projectname`, `\fundingagency`, `\catalogcard`,
  `\setupabstracts`, `\epigraph`, `\listofframes`, `\listofprograms` and the
  `framefloat` environment. Values too: `\productiontype{bibliographic}`,
  `\linkedproject{no}`; and the bibliography field `newspapersection`. The
  Portuguese names keep working. algorithm2e runs with `onelanguage`, so
  `\For`, `\While`, `\KwData` print Portuguese words in a Portuguese work
  (#102).
- **The databases use biblatex names** for every entry type and field; the
  reference lists come out identical (#102).
- **The minimal and the maximal example** (#102). `max-exemplo.tex` adds to
  the former example a subtitle, an epigraph (new command `\epigrafe`), XML,
  HTML and Prolog listings, a glossary and an index.
- **The class manual discusses** compile time on Overleaf and the
  alternatives (paid plans, compiling on Windows, Linux and macOS), LaTeX
  editors, and the reference managers JabRef, Zotero and Mendeley with their
  Overleaf integration.
- **The list of symbols follows the order of appearance** in the text, as
  3.1.2.2.7 of the UFRJ Manual asks: each symbol takes the position of the first
  time it is registered, and registering it again does not repeat it. The new
  option `simbolosalfabeticos` restores the alphabetical order, with the
  optional sort key of `\symbl` (#100).
- **A separate list of acronyms**, as 3.1.2.2.6 recommends: `\makelosiglas` in
  the preamble and `\printlosiglas` among the lists. Acronyms from `\sigla` and
  from the new `\acron[key]{ACRONYM}{meaning}` go there, and the other list is
  titled "Lista de Abreviaturas". Without `\makelosiglas` nothing changes: the
  acronyms stay in the list of abbreviations, titled "Abreviaturas e Siglas".
  latexmkrc, the build scripts and the empty-document generator know the new
  `.sgx`/`.lsg` pair. `example.tex` uses the separate list, and with it needs
  `morewrites` (seventeen write streams) (#101).
- **`example_pdfa.tex` is gone**: `example.tex` itself compiles with `pdfa`, and
  the PDF/A scope of the build validates it (#99).
- **`morewrites` gets the free real write streams** (`allocate`). Every stream
  it managed used to be virtual, so each write went through `\jobname.mw`:
  `example.tex` opened that file 772 times per pass. Now only what exceeds
  sixteen goes through it: 118 opens, the same PDF, about 2 s (a quarter) less
  per pdfLaTeX pass. The package stays — a work with an index and a glossary
  overflows the sixteen streams without it (#95, #96).
- **`example.tex` compiles as PDF/A-2b** (`\documentclass[dsc,pdfa]{coppe}`) and
  explains why in a section of its own; the five per-language examples explain
  it in their own language, and the class manual has a new section *Por que
  PDF/A* (#86).
- **UTF-8 everywhere.** TeX accent sequences (`\'a`, `\c c`, `{\~ a}`) became
  UTF-8 characters in the `.dtx` — manual, class strings, language packs, `.bib`
  databases, examples — in the COPPE norm and in the tests. The `listings`
  `literate` table keeps its escapes on purpose (#88).
- **Copyright** unified as 2008–2026 and the four authors in every header, and
  the AI-support note names the models the commits record (#92, #93).
- No `\paragraph` in the class manual; `example.tex` shows the five section
  levels, with the one `\paragraph` there is.
- **No more `\CharacterTable` and `\CheckSum`.** The current `doc`
  documentation lists both as obsolete ("neither should be used in new
  developments"): they guarded against mail gateways that mangled files. The
  table was written with `%%`, which docstrip copies into the header of every
  generated file — class, styles, `.bib` databases, examples — where it was a
  dead comment. Both are gone from `coppe.dtx`, and the manual build no longer
  logs "This macro file has no checksum!". Regression test r94 keeps them out.

### Fixed

- **latexmk (and so Overleaf) ran pdfLaTeX five times and then failed** with
  "pdflatex needed too many passes", on every document made with the class. The
  measured width of the table-of-contents number column alternated between
  42.4 pt and 13.2 pt on each run, so the `.aux` never settled: the measuring
  macro was not protected, and chapter entries go through `\MakeUppercase`,
  which expanded it. With `\protected` the build of `example.tex` stops at four
  passes and finishes cleanly — 75 s to 58 s together with the `morewrites`
  change (#98, #95).
- **`example.tex` compiles with no warning at all**: 0 LaTeX/package warnings,
  0 Underfull/Overfull boxes, 0 font substitutions (#94). On the way:
  - no more "Although slower, you should try compiling with LuaLaTeX" (#89);
  - `lmss/m/it`, `lmss/bx/it`, `lmtt/bx/n` and neighbours are declared directly,
    so no "Font shape … not available" (#87);
  - duplicate PDF destinations `page.2` (folha adicional and approval sheet) and
    `chapter.A`/`chapter.B` (appendix and annex with the same letter — a table of
    contents link to an annex could land on the appendix);
  - under `pdfa`, the five hyperref "already been used" warnings and the pdfx
    colour-model warning.
- The TikZ example has its caption above the figure, as the class's own rule
  says (#91).
- **The subtitle appears on the abstract sheets**, in the language of each
  sheet. `\foreignsubtitle` was stored and never printed anywhere (#102).
- **Column-one comments in the examples reached the student.** docstrip
  removes lines starting with a single `%`, and the explanatory comments of
  the examples' preambles never made it into the generated files.
- `tools/versao.py` no longer reports line-ending differences between `dist/`
  and `src/` as divergences (#85).
- `tools/conferir-referencias-cruzadas.py` no longer crashes when the log is on
  a different Windows drive from the repository (regression test r90).

### Documentation

- When to turn `morewrites` off, and when not to, with the stream cost of each
  list, index and glossary (#96).
- Which front-matter lists the UFRJ Manual makes mandatory (only the table of
  contents) and which are optional, in the manual, the quick reference, the norm
  manual and before the lists in `example.tex` (#97).

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

- **The approval sheet lists only the examiners.** It records who examined the
  work, and the advisor conducted it. The new `orientadorexamina` option puts
  the advisors and coadvisors back, ahead of the examiners, for the Programas
  that seat the advisor on the board. Before this there was no choice, and the
  only way out was not to declare the advisor at all — which also removed them
  from the capa and the folha de rosto, where they belong.

- **No page numbers in the abbreviation and symbol lists.** 4.1.1 describes both
  as an alphabetical list of the term and its MEANING, and asks for no location;
  the folio was inherited from building the two lists with the index machinery,
  where the page is the point. The dot leaders went with it, which also fixes the
  long description that used to break awkwardly before a trailing number.

- **No date given, no blank rule.** Without `\dataaprovacao` the approval sheet
  now reads "a ser determinada", in the main language of the work, instead of
  drawing a rule to fill in by hand. Nobody writes on a PDF.

### Added

- **`\configuraresumos{…}{…}{…}{…}` — the abstract sheet is five elements, and
  four of them are optional.** The five are page identification (the "Resumo da
  Tese apresentada à COPPE/UFRJ…" sentence), title and author, advising, the
  work's own bibliographic reference, and the abstract itself. **Only the
  abstract itself is mandatory.** The command takes four booleans, in that
  order, and applies to **every abstract and every language** in the document —
  three abstract sheets with different layouts in one work are not a choice,
  they are an oversight. All four are on by default, which is the sheet of
  Annexes E and F. A value that is neither `true` nor `false` is a class error:
  a switch that silently keeps the previous state is discovered in the
  deposited PDF.

  ```latex
  \configuraresumos{true}{true}{true}{false}   % sem a referência
  \configuraresumos{false}{false}{false}{false} % só o texto do resumo
  ```

- **The colophon reports the engine and the machine, and nothing in it is
  written by hand.** `\coppetexfinalpage` now prints the engine and its
  version, the engine's own banner (which names MiKTeX or TeX Live), the LaTeX
  format date, the font family and encoding **in force**, the biblatex version,
  the date, the hour, and the operating system and machine. Every item is asked
  of the engine at composition time. Under LuaLaTeX the machine name comes from
  `os.uname()`; pdfLaTeX and XeLaTeX can only tell whether the system is
  Windows, and when even that is unknown the sentence omits the system rather
  than inventing one. If you would rather not publish the machine name,
  `\renewcommand{\coppefinalsystem}{}` removes that clause.

- **The `.bib` files may live in a subfolder.** `\addbibresource{referencias/
  minha-tese.bib}` works on a local machine and on Overleaf, because biber
  opens the path relative to the document. It is also **safer** than the bare
  name: a bare name goes through the kpathsea search, and when the file is
  absent from the work's folder biber silently resolves it to the `.bib` of the
  same name shipped with the TeX distribution — and the thesis comes out with
  someone else's bibliography. With a path there is no search: either the file
  is there or biber stops. The empty-document generator writes the subfolder by
  default, and `tests/regressivo/r31` proves both halves.

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
- **The work's own reference at the top of each abstract** (3.1.2.1.4, Annexes
  E and F). The Manual says "sugere-se que o resumo venha antecedido por uma
  referência conforme apresentado no ANEXO E", and both model annexes show the
  resumo and the abstract opening with it; the class printed none. It is now
  composed by the class from the folha de rosto data — author, title, subtitle,
  city, year, work type, degree and Programa — so nobody types it. The same
  reference appears on all three abstract pages and always in Portuguese,
  because a reference describes a document and is not translated; only the title
  follows the language of the work. An exame de qualificação gets none: it is
  not deposited. `resumosemreferencia` turns it off for an abstract already at
  the 500-word ceiling, which the three added lines could push onto a second
  sheet.
- **Each abstract sheet is now entirely in its own language.** Everything the
  *class* writes on it — the opening sentence, the title, the month, the
  advisor and department labels, the keywords — follows the language of the
  abstract below it. It used to be pinned to Portuguese on the `abstract` page
  and to English on the `foreignabstract` page, whatever the languages of the
  work, so an English-written thesis came out with its English text under
  "Resumo da Tese apresentada à COPPE/UFRJ", the Portuguese title, "Maio/2026"
  and "Orientador:", and its Portuguese text under the English heading. A
  Spanish-written thesis was worse: with only two shapes available, the Spanish
  abstract and the Portuguese one came out under the **same** Portuguese
  heading, and no Spanish heading existed anywhere — in a language art. 57 of
  CEPG Res. 302/2024 admits for writing a thesis.

  The one thing that does not translate is the **Programa's name**: COPPE has an
  official name for each Programa in Portuguese and in English, and no other.
  On a Spanish, French or Italian sheet the Portuguese name is used, as a proper
  noun — the same rule as section 4 of the COPPE norm. The cover, the title page
  and the approval sheet are institutional identity and stay in Portuguese.

  Portuguese output is unchanged, character for character, which is how the
  change was verified. Guarded by `tests/regressivo/r25`, which compiles a work
  in each main language and checks, sheet by sheet, that every piece is in the
  right language *and* that no piece of another language is there.
- **`mscsem` — the Seminário de Mestrado**, a fifth work type. Some Programas
  require it — Mechanical Engineering among them — and it is technically *not* a
  qualifying exam: they are different moments of the course, with different
  boards and different purposes. Until now, whoever needed one typeset it as an
  `mscexam` and changed the title by hand, which comes out wrong on four sheets
  at once: cover, title page, approval sheet and the top of the abstracts. Like
  the two exams, it carries no CAPES sheet, no catalogue card and no reference
  above the abstract — it is not deposited in the library.

  The request came from outside, as [PR
  #61](https://github.com/COPPE-UFRJ/CoppeTeX/pull/61). That implementation
  edited the generated `src/coppe.cls`, which is overwritten at the next
  generation, and left out the flag that marks a work as undeposited — so the
  seminar would have come out with all three. Implemented here in
  `src/coppe.dtx`, where it survives, and guarded by
  `tests/regressivo/r24`, which exercises it in all five languages.
- **Fifth heading level** numbered and formatted (2.6).
- **`listasnosumario`** — restores the pre-textual lists to the sumário, which
  3.1.2.1.6 keeps out of it.
- **`semlinks`** — drops the colour and the frame from every hyperlink, for
  anyone who is going to print. The links stay clickable and the bookmarks stay
  in the reader's panel. It used to take a `\hypersetup` in the preamble, which
  worked but required knowing that the class loads `hyperref` and in what order.
- **A real message when a cover logo is missing.** `\includegraphics` finds the
  logos through the same search that found the class, so a logo installed beside
  `coppe.cls` needs nothing. What broke was copying `coppe.cls` alone into a
  project folder: TeX said "File `coppe-logo' not found" with no hint that the
  file ships with the class. It now says so, and names where to get it.
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
- **`tests/adversativa/`** (not distributed) — six complete documents, four in
  Portuguese, one per work type, plus one in English and one in Spanish of
  different types, each exercising everything the class offers at once,
  compiled under both engines. See *Verification* below for why six and not
  twelve.
- **`NORMA_COPPE_2026`** rewritten as a *differences* document against the
  UFRJ Manual, and **`PROPOSTA_CPGP.md`**, the text put to the CPGP for a vote.

### Changed

- **The abstract sheet is composed from the top, and its vertical spaces went
  from 44 mm to 30 mm.** A 500-word abstract — the limit of 3.1.2.1.4 — did not
  fit on one sheet with the five elements on, and one sheet is what the same
  item requires. The Manual prescribes none of those measures.
- **The three abstract environments now share one macro.** Each of them carried
  the whole leading block copied byte for byte, and that copy is what produced
  the two worst defects those sheets ever had: a fix landed in two of them and
  was missing from the third, and the third was always `brazilianabstract`,
  which only appears in a work written in Spanish.
- **The type of work is now demanded.** It is the only class option with no
  default, and nothing was checking for it: without it the class loaded in
  silence and died later, inside `\maketitle`, with `Undefined control sequence
  \local@doctype` pointing at a line of the class itself. It now stops with a
  message naming the five options.
- **The implementation section of `coppe.pdf` is navigable.** It was a single
  60-page subsection with seven subsubsections, five of them in the first ten
  pages; it is now eleven subsections and twenty-four subsubsections, grouped
  by subject.
- **The options section of `coppe.pdf` opens with a table of what is default,**
  and every entry states its own default. Three were wrong or missing:
  `resumosemreferencia` was described as on by default when it is the
  *reference* that is on and the option that is off, and `rascunhoficha` and
  the `morewrites` loading stated no default at all.
- **The files and developer sections of `coppe.pdf` describe the project as it
  is.** They still showed the logos loose in the root, knew nothing of
  `logos/`, `manuais/` or the language folders, told the reader not to copy
  `coppe.dtx` and `coppe.ins` (which the delivery now ships on purpose), spoke
  of twelve adversarial documents outside `tests/` (there are six, inside), and
  had never heard of `tests/regressivo/` or of the panel.
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

- **Sixty lines of documentation were printed as verbatim code in
  `coppe.pdf`,** and had been for several versions. Two `macrocode` guards in
  the `.dtx` were written with three spaces instead of four, and `doc.sty` only
  closes a code block on a percent sign followed by **exactly** four spaces; a
  dead `\@wrlab` block commented out with four percent signs had the same
  effect for the opposite reason, because `doc.sty` ignores *every* percent
  sign in the documentation part, so that line opened a real code block.
  Neither broke the compilation, which is why neither was seen.
  `tools/conferir-manual.py` now checks every guard.
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

`tests/adversativa/referencias-manual.bib` carries one entry for **each of the 34
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

### Fixed (found while writing the regression suite)

- **The third abstract came out with no title.** On the way out,
  `foreignabstract` cleared `\local@title`, `\foreign@title`, `\@author` and
  `\@date` with `\global\let ... \relax` — housekeeping from when it was the
  last pre-textual sheet. Since v4.0 it is not: `brazilianabstract`, the third
  abstract of a Spanish-written work, comes after it and sets its title from
  the macro that had just been erased. A sheet of the deposit was going out
  titleless, and only in Spanish theses, which are few and had never been read
  sheet by sheet. Guarded by `tests/regressivo/r23`.

### Fixed (found by the extended adversarial document)

- **`\glossaryname` leaked out of `\printlosymbols`.** The `\renewcommand`
  sat outside the `\begingroup`, so after the list of symbols every later use
  of `\glossaryname` — the post-textual Glossário of 3.1.4.2 and its sumário
  entry — came out titled "Lista de Símbolos". Only a document carrying both
  the pre-textual lists and the glossary can show it, and none did until one
  was built for it.

### Verification

Everything above is proved by one command — `coppetex.bat`, the developer
panel, or `tools/prova.ps1` under it — which regenerates the distribution from
the `.dtx`, checks by git that no derived file diverged, compiles the whole
distribution and the test documents under **both engines**, and runs veraPDF
over every PDF/A. `tools/conferir-norma.py` then measures the finished PDFs
against the Manual. See the release notes in the pull request for the run of
record.

Testing is now **three layers**, each asking a different question:

- `tests/*.tex` — *does the class compile?* The verdict is pdflatex's exit
  code. Runs in every build.
- `tests/adversativa/` — *does it survive everything at once?* Cut from twelve
  documents to **six**, because a proof that takes too long is a proof that
  stops being run. The cut was not uniform: Portuguese keeps four, one per work
  type, and English and Spanish keep one each, of *different* types, so the
  sample crosses language with type instead of repeating the same pair. The
  option matrix became explicit in `tools/mk-adversativa.py` so that one can
  check by eye that no option lost its proof and that all three spacing steps
  of the approval sheet — five names, six, seven or more — are still there,
  the ceiling of eight included.
- `tests/regressivo/` — *did an old defect come back?* **New.** One minimal
  test per defect already fixed, 36 of them, each declaring in its own header
  what must and must not appear in the PDF, in the log, in an auxiliary file or
  in the raw bytes. It is opt-in: it answers a different question and does not
  belong in every build. It exists because nearly every bug this class ever had
  **compiled with exit code zero** and came out wrong — the first layer could
  never have caught them.

**No PDF under `tests/` is versioned any more.** The versioned PDFs are the
ones in `src/` and `dist/`, which are the deliverable and let anyone read the
manual on GitHub without installing TeX. The test PDFs are proof of work: they
change on every compile, and versioning them filled the history with binary
nobody reads.

### Fixed in the harness itself

Defects in the tools that check the class are worth the same attention, because
a checker that approves everything is worse than no checker: it looks as though
someone checked.

- **The checkers were reading ten lines of each log.** Both
  `tools/conferir-referencias-cruzadas.py` and the reference verdict in
  `tools/build-check.ps1` cut the `.log` at the **last** `LaTeX2e <`, believing
  the file held several passes and that the last banner marked the last one. It
  does not: pdflatex rewrites the log on every pass, and what appears twice is
  the banner, which LaTeX repeats at the end of the log just before the warning
  summary. The cut threw away the body of the pass — which is exactly where the
  named warnings are — and the reference verdict had stopped finding anything
  at all. Guarded by `tests/regressivo/r90`.
- **A locked PDF failed the whole run.** "I can't write on file X.pdf" is not a
  defect of the document: it is someone holding the file, usually a PDF reader
  on the desk, or veraPDF itself, which validates a PDF and has not let go of it
  when the next step tries to rewrite it. The step now retries up to three
  times and says how many attempts it took; if the file is still locked, it
  still fails.
- **The test suite died mid-run over a banner.** `makeindex` writes its own
  banner to stderr and exits zero; under `$ErrorActionPreference = "Stop"` that
  banner became a terminating error in PowerShell 5.1 and aborted the suite as
  if a test had failed.
- **`tools/conferir-norma.py` blamed the document for a missing tool.** There
  are two programs called `pdftotext`; only poppler's has `-bbox`, which is how
  the script measures position on the finished PDF. With Xpdf's first on the
  PATH the check ran with zero words and accused the document of having no
  numbered folio and no sumário. It now picks a `pdftotext` that has `-bbox`,
  whatever the PATH order.

### Developer panel

`coppetex.bat`, at the root, is the single entry point: with no argument it
opens a window and asks what to do; with arguments it does exactly that and asks
nothing. Every action exists both ways — the window has no path of its own, so
the two cannot drift apart. It can regenerate `src/` from the `.dtx`, compile
the deliverable PDFs, run each of the three test layers, validate PDF/A, run the
checkers, copy to `dist/` and raise the version. Manual in
[`PAINEL.md`](./PAINEL.md).

`tools/versao.py` checks that the version is in step across 28 generated files
and 6 places in prose, and compares `dist/` with `src/` byte for byte — the
version number is the same in both even when the copy fell behind, which is
precisely the case nobody notices. It raises the second or the third level;
**the first is deliberately not offered**, because changing major on this class
has always meant changing the model, and that is a decision of the project and
of the CPGP, not of a script.

`src/doall.bat` became a shortcut for `coppetex.bat --regerar --docs --dist`.
It had a copy list of its own, and that list had already drifted from the
`Makefile`'s: one of the two overwrote `dist/README.md` — the installation
guide — with the root README on every run.

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
