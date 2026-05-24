# howto.md — ABNT NBR 6023 (post-2020) as implemented for CoppeTeX 4.0

**Purpose.** Working specification, extracted from `specs/manual2024.pdf`, of every
citation rule, reference type, field/element, and formatting block we must support
in the new BibLaTeX/biber bibliography engine. This is the reference document for
implementing `coppe.{bbx,cbx,lbx,dbx}` (generated from `coppe.dtx`).

**Source.** `specs/manual2024.pdf` (COPPE/UFRJ, follows ABNT NBR 6023, edition
citing "ABNT, 2023"). It supersedes `specs/oldmanual.pdf`. Where manual2024 is
silent, oldmanual may still apply.

**Backend / engine.** biber + biblatex only. No bibtex, no `.bst`, no
bibtex-natbib. Default citation style = **author-date (autor-data)**; numeric is
opt-in; unsorted also supported. All formatting is deferred to output (never
pre-format inside `.bib`).

> Section numbers below (§4.1, §4.2, …) refer to manual2024's own numbering.

---

## 0. Key deltas: post-2020 vs the 2018 edition (why a new style is needed)

The installed `biblatex-abnt` implements NBR 6023:2018. manual2024 follows the
post-2020 (2023) revision. Confirmed differences so far (extend as found):

1. **In-text citation names use initial caps, NOT all-caps/small-caps.**
   §4.1.1.2(a): "the call by author surname … must be in initial capitals and the
   rest lowercase." So `Segundo Chartier (2002, p. 23)` and
   `(Chartier, 2002, p. 23)` — never `CHARTIER`. (Reference *list* surnames remain
   ALL CAPS — see §4.2/§4.3.) biblatex's stock `authoryear` already uses normal
   caps in citations, so we must NOT re-impose uppercase the way old abnt did.
2. **Repeated author → repeat the full entry, NOT a `______` dash.** §4.4.1: "as
   entradas subsequentes devem ser repetidas." Old ABNT/`biblatex-abnt` substitute a
   repeated author with a 6-space dash/underscore; post-2020 repeats the name in
   full. biblatex: **`dashed=false`**.
3. `et al.` appears in **italic** in author-date parentheses, and the manual writes
   it without a trailing period in the parenthetical example (`Barbosa et al, 2008,
   p.43`). Confirm exact punctuation during implementation.
4. Brackets for missing data: **`[S. l.]`** (sine loco), **`[s. n.]`** (sine
   nomine), **`[S. l.: s. n.]`**, and the no-date estimate forms (`[1981?]`,
   `[ca. 1977]`, `[197-]`, `[19--?]`, …) — §4.3.5.
5. Title highlight = **bold (negrito)**; italic is explicitly discouraged (reserved
   for foreign words) — §4.3.3. (Old styles often used italic.)
6. "More than three authors" may list **all** authors (recommended for research
   output) or truncate to first + `et al.` — needs configurable `maxbibnames`
   (§4.3.1.3), not a hard 3-name cap.

---

## 1. Citations — §4.1

### 1.1 What a citation is (§4.1.1)
A citation is a mention, in the text, of information taken from another source; may
appear in text or in a footnote. Three kinds:
- **Direta** (direct) — verbatim transcription of part of the consulted work.
- **Indireta** (indirect) — text based on the consulted work.
- **Citação de citação** — direct/indirect citation of a text whose original was
  not accessed (see `apud`, §1.4.2).

### 1.2 Call system (§4.1.1.1)
Citations are indicated by **one** system — numeric **or** author-data — used
consistently throughout the whole work, allowing correlation to the reference list
(or footnotes).

#### Numeric system (§4.1.1.1.1)
- Single, consecutive numbering for the whole work, in arabic numerals; order of
  appearance in text. Numbering does **not** restart per page.
- Indicated either (a) between parentheses, aligned to text: `(15)`; or
  (b) superscript: `…previvendo [...]"`¹⁵.
- **Must not** be used together with footnotes.
- Direct citation: page/locator after the citation number, separated by `, `
  (comma + space). Page preceded by lowercase `p.`. Electronic locator
  (paragraph, minutes, slide, …) preceded by its abbreviation (`local.`, `min.`,
  `slide`, `par.`).
  - `"…direitos territoriais indígenas" (1, p. 30).`
  - `"…no ambiente virtual [...]"`²ʼ ᵖᵃʳ· ³ (superscript "2, par. 3").

#### Author-data system (§4.1.1.1.2) — DEFAULT for CoppeTeX 4.0
- Indicated by the author surname **or** responsible institution **or** title of
  entry, followed by the year of publication, separated by a comma, in parentheses.
- Direct citations: add the page number or location of the excerpt after the year.

### 1.3 General rules (§4.1.1.2)
- **(a) Initial caps, rest lowercase** for the surname/institution/work/title,
  whether inside the sentence or in parentheses (the key post-2020 delta):
  - In sentence: `Segundo Chartier (2002, p. 23), "a leitura diante da tela…"`
  - In parens: `"A leitura diante da tela…" (Chartier, 2002, p. 23).`
  - **2 or 3 authors:** in sentence use `e` between the last two
    (`Barbosa, Paula e Oliveira (2008, p.43)`); in parentheses separate **all** by
    `;` (`(Barbosa; Paula; Oliveira, 2008, p.43)`).
  - **More than 3 authors / "e outros":** in sentence `Barbosa e outros (2008, p.
    43)`; in parentheses `(Barbosa et al, 2008, p.43)` with `et al` in italic.
  - **Legal entity (pessoa jurídica):** `(Organização Mundial da Saúde, 2010, p.
    xi)`, `(IBGE, 2011, p. 3)`.
  - **Government entity:** in text `(Brasil, 1995)`; list entry begins
    `BRASIL. Ministério da Administração Federal e da Reforma do Estado. …`.
  - **Title entry (no author):** `(Inglês, 2012, p. 7)`; list entry
    `INGLÊS: guia de conversação. …`.
- **(b)** Same surname + same year → add prename initials; if still ambiguous, full
  prename: `(Braga, O., 1966)` vs `(Braga, Orlando, 1987)`.
- **(c)** Same author, same year, different works → append lowercase letters to the
  year, no space: `(Carvalho, 1999a) (Carvalho, 1999b)`.
- **(d)** Indirect citations of several works by the *same* author in *different*
  years cited together → years separated by commas: `(Foucault, 1986, 1993, 1996)`.
- **(e)** Several works by *different* authors cited together → separated by `;`:
  `(Derrida, 1980; Guattari, 1986; Deleuze, 1983)`.
- **(f)** Direct quote ≤ 3 lines → double quotes; single quotes for a quote within
  the quote.
- **(g)** Direct quote > 3 lines → block, indented (recommended 4 cm from left
  margin), smaller font, single spacing, no quotes; final period ends the sentence,
  not the citation.
- **(h)** Abbreviated page(s)/location and, if any, volume(s)/section(s); order:
  **author, date, volume or section, page**, separated by commas. In indirect
  citations the page is optional.
- **(i)** Indications:
  - interpolations/additions/comments → square brackets `[ ]`;
  - suppressions → ellipsis in brackets `[...]`;
  - emphasis (grifo, negrito, itálico) → mark with `grifo nosso` in parentheses
    after the citation call; if the author's, `grifo do autor`.
  - data from non-formally-published sources (lectures, speeches, interviews) →
    indicated directly in text or in a note; unpublished oral communications do not
    generate a reference;
  - works in progress (fase de elaboração) → mention the fact, give available data
    in a note.
- **(j)** Author's own translation of the quote → add `tradução nossa` after the
  call: `(Nora, 1989, p. 7, tradução nossa)`.

### 1.4 Notes — §4.1.2
Notes (footnote / margin / end-of-document) are of two kinds: **reference notes**
and **explanatory notes**. Footnotes: separated from text by a single line space and
a 5 cm horizontal rule from the left margin; arabic superscript numbers, consecutive
through the text; aligned from the 2nd line under the first letter; smaller font;
kept on the page where the call appears.

#### 1.4.1 Reference notes (§4.1.2.1)
Indicate consulted sources or refer to other parts of the work. Arabic, single
consecutive numbering per section/part. A note referring to a source cited earlier
may repeat the full reference or indicate the previous note number preceded by the
abbreviation `ref.` (optionally with page/location).

#### 1.4.2 Latin expressions (§4.1.2.2)
Used **only in notes**, except **`apud`** which may also appear in body text. All
latin expressions and their abbreviations are set in **italic**.
- **`apud`** ("cited by") — for citation of a citation (original not accessed). The
  reference is to the citing work (the one actually accessed):
  `Segundo Massarani (apud Werneck, 2002, p. 80)`, `(Silva, 1955 apud Pessoa,
  1965)`.
- Notes-only expressions: **`Ibidem`/`ibid.`** (same work), **`idem`/`Id.`** (same
  author), **`opus citatum`/`op. cit.`** (work cited, not immediately preceding),
  **`passim`** (here and there — for indirect citations), **`loco citato`/`loc.
  cit.`** (place cited), **`Conferre`/`Cf.`** (compare), **`sequentia`/`et seq.`**
  (following). `op. cit.`, `ibidem`, `idem` may only be used on the same page/folio
  as the citation they refer to.

#### 1.4.3 Explanatory notes (§4.1.2.3)
Comments/clarifications that cannot go in the text. Arabic, single consecutive
numbering per chapter/part/document; do not restart per page; not used
simultaneously with reference notes.

`[sic]` — used in a direct quote to flag an easily identifiable error in the
original (transcribe exactly, then add `[sic]` in brackets).

---

## 2. Reference types — §4.2

### 2.0 General reference-list formatting (§4.2 preamble)
- References aligned to the **left margin only** (no justification), single
  spacing, each separated from the next by **one blank line** (single spacing).
- In footnotes: aligned left, from the 2nd line under the first letter, no space
  between references.
- Punctuation follows international standards, uniform across all references.
  Abbreviations per NBR 10522.
- The typographic resource used to highlight the **title** element (bold / italic /
  underline) must be **uniform** across the whole document. **Decision: use bold
  (negrito) for titles** (matches the manual's examples).
- **Entry by title** (no author): no typographic highlight; the first significant
  word of the title is in **CAPS** (e.g. `O PERFIL administrativo brasileiro.`).
  Articles / monosyllables are ignored for alphabetization.
- Complementary elements, once adopted, must appear in **all** references.
- Elements not present in the work → square brackets `[ ]`; suppressions → `[...]`.
- Surname is **ALL CAPS**, prename in normal case (`SOBRENOME, Prenome`).

### 2.1 Monografias (§4.2.1) → `@book` + academic works (`@thesis`/`@mastersthesis`/`@phdthesis`)
Includes books/booklets (guide, catalog, encyclopedia, dictionary, …) **and**
academic works (theses, dissertations, TCC, …).

**§4.2.1.1 Monografia no todo — whole monograph (`@book`):**
> `SOBRENOME, Prenome.` **`Título`**`: subtítulo. Edição. Local: editora, ano.`
- Essential: author; title; edition; place (city); publisher; year.
- Complementary: **page count** (`156 p.` / `iii, 156 p.` / `xiv, 43 p.`; folhas
  `f.` if single-side academic work, páginas `p.` if double-side; volumes `5 v.` /
  `5 v. em 3.`; `Paginação irregular.`; `Não paginado.`); **illustrations** (`il.`,
  `il. color.`, `principalmente il. color.`, `somente il.`, `Ilustrações de
  Ziraldo.`); **dimensions** (height ×, in cm); **series/collections** (in
  parentheses at end: `(Coleção Saber, 13)`); **notes** (no highlight: `no prelo`,
  `Tradução de: …`, ISBN, `Inclui bibliografia`, document type, etc.).
- Example: `CASTRO, C. M.` **`A prática da pesquisa`**`. São Paulo: Mc Graw-Hill do
  Brasil, 1978. 156 p.`

**Academic works (thesis / dissertation / TCC) — a monograph with a defense note:**
> `AUTOR.` **`Título`**`. Ano. Nº f. TipoDeTrabalho (Grau em Área) — Unidade,
> Instituição, Cidade, Ano.` [`Disponível em: URL. Acesso em: data.`]
- The work type, degree+area `(Mestrado em …)`, affiliation (after an **em dash
  `—`**), city and defense date go as a **note**.
- Examples: `LEITE, Sonia.` **`Memória da comunidade da Serrinha`**`. 1997. 203 f.
  Dissertação (Mestrado em Memória Social e Documento) — Centro de Ciências
  Humanas, Universidade do Rio de Janeiro, Rio de Janeiro, 1997.` /
  `REGO, S. M. B.` **`Planejamento da função de sistemas de informação`**`: um
  estudo de caso. 1992. 275 f. Dissertação (Mestrado em Administração) - Instituto
  Coppead …, 1992.`

**Thesis family — one `thesis` formatter, two ways in (CoppeTeX 4.0):**
- **Generic, you set `type`** (for any variation): `@thesis`/`@tese` and
  `@dissertation`/`@dissertacao`. `type` is a localized key (below) or literal text
  (`type = {Exame de Qualificação}`). Both require `type`.
- **Specific, `type` preset** (write no `type`): a biber source map retypes these to
  `@thesis` and presets a babel-aware `type` — `@masterdissertation`/
  `@dissertacaomestrado` (syn. `@mscdissertation`) → `mscdiss`;
  `@dscthesis`/`@tesedoutorado` → `dscthesis`; `@phdthesis`/`@tesephd` →
  `phdthesis`; `@tcc` → `tcc`.
- Localized `type` words (`.lbx`): pt `Dissertação de Mestrado` / `Tese de Doutorado`
  / `Trabalho de Conclusão de Curso`; en `M.Sc. Dissertation` / `D.Sc. Thesis` /
  `Ph.D. Thesis` / `Undergraduate Thesis`. The degree+course `(Mestrado em Curso)`,
  affiliation and defense date render from `type`/`institution`/`date` (§4.3.8.3).
  An explicit `type` on a specific entry overrides the preset.

**§4.2.1.2 Monografia no todo em meio eletrônico — electronic/online book:**
Same elements as print **plus** support type as a note (CD, DVD, *pen drive*,
*link*, …). For **online**: electronic address preceded by **`Disponível em:`** and
access date preceded by **`Acesso em:`**. `[S. l.]` = *sine loco* (no place).
- Examples: `FERREIRA, Aurélio Buarque de Holanda.` **`Novo dicionário da língua
  portuguesa`**`. 2. ed. Rio de Janeiro: Nova Fronteira, 2002. CD-ROM` /
  `DEVOS, Ryka; OETENBERG, Alexander.` **`Architecture of Great Expositions
  1937-1959`**`: messages of peace, images of war. London: Routledge, 2016. E-book.
  Disponível em: URL. Acesso em: 05 abr. 2019.`

**§4.2.1.3 Parte de monografia — chapter/part (`@incollection` / `@inbook`):**
> `SOBRENOME (autor da parte), Prenome. Título da parte: subtítulo.` *`In`*`:
> SOBRENOME (autor do livro), Prenome.` **`Título do livro`**`: subtítulo. Edição.
> Local: editora, ano. Página inicial-final.`
- Essential: author(s); part title; the expression **`In:`** in *italic*; full
  reference of the containing monograph; pagination of the part (`p. 7-16`).
- Part title is **not** bold; book title **is** bold. If the part author = book
  author, repeat the name after `In:`.
- **Encyclopedia/dictionary entries (verbetes):** with authorship (`FREIRE, J. G.
  Pater famílias.` *`In`*`: ENCICLOPÉDIA Luso-brasileira …`) or without authorship
  (enters by entry word in CAPS: `ESQUIZOFRENIA.` *`In`*`: FERREIRA, … `).
- **Separatas:** referenced as parts but replacing `In` with **`Separata de`**.

### 2.2 Correspondência (§4.2.2) → `@letter`
Includes note, letter, card. Essential: sender (author); title/denomination (assign
one in `[ ]` if none); recipient (preceded by `Destinatário:`); place; date;
physical description.
- `PILLA, Luiz. [`**`Correspondência`**`]. Destinatário: Moysés Valinho. Porto
  Alegre, 6 jun. 1979. 1 cartão pessoal.`
- **§4.2.2.1 electronic:** add medium info (DVD, CD-ROM, *pen drive*, *online*,
  *e-mail*). `LISPECTOR, Clarice. [`**`Carta enviada para sua irmã`**`].
  Destinatário: Tânia Lispector. Belém, 8 jul. 1944. 1 carta. Disponível em: URL.
  Acesso em: 4. ago. 2023.`

### 2.3 Publicações periódicas (§4.2.3) → `@periodical` and `@article`
Serials in any medium, successive physical units with numeric/chronological
designations, intended to continue indefinitely: whole collection, fascicles,
journal/newspaper issues, and material within an issue (scientific articles,
editorials, news, sections, reports). Electronic/online: same rules + support type,
`Disponível em:` / `Acesso em:`.

**§4.2.3.1 Periódico no todo — whole journal (`@periodical`):** enters by title in
CAPS. `TÍTULO DO PERIÓDICO. Local: Editora, ano- (primeiro/encerramento fascículo).
ISSN. Periodicidade. Notas.` e.g. `REVISTA BRASILEIRA DE GEOGRAFIA. Rio de Janeiro:
IBGE, 1939- . ISSN 0034-723X. Trimestral.`

**§4.2.3.2 / §4.2.3.3 — collection part / issue with no own title:** title, place,
publisher, year/volume, fascicle number, dates. e.g. `REVISTA BRASILEIRA DE
NEUROLOGIA. Rio de Janeiro: …, v. 39, n. 2, abr./jun. 2003.`

**§4.2.3.4 Artigo / matéria de revista, boletim (`@article`) — CORE:**
> `SOBRENOME, Prenome. Título do artigo: subtítulo.` **`Nome do periódico`**`,
> Local, volume, número, página inicial-final, mês abreviado. Ano.`
- Highlighted (bold) element = the **journal name** (`journaltitle`), NOT the
  article title.
- Month abbreviated **only if ≥ 5 letters** in Portuguese (so `maio` stays full);
  ranges use `/` (`jan./jun.`, `out./dez.`).
- e.g. `ARAÚJO, Vânia Maria Rodrigues Hermes de. Informação: instrumento de
  dominação e de submissão.` **`Ciência da Informação`**`, Brasília, DF, v. 20,
  n. 1, p. 37-44, jan./jun. 1991.`
- Multiple authors separated by `; `. `et al.` for many.
- **§4.2.3.5 electronic:** same + `DOI:` (if any) + medium + `Disponível em:` /
  `Acesso em:`. e.g. `YANG, Li et al. COVID-19: …` **`Signal Transduction and
  Targeted Therapy`**`, [London], v. 5, n. 128, p. 1-8, 2020. DOI: … Disponível em:
  … Acesso em: …`

**§4.2.3.6 Artigo / matéria de jornal (`@article`, newspaper) — CORE:**
> `SOBRENOME, Prenome. Título do artigo: subtítulo.` **`Nome do jornal`**`: subtítulo
> (se houver), local, ano/volume, número, data de publicação, seção/caderno,
> paginação.`
- Newspaper name bold. When there is no section/caderno, pagination precedes the
  date. e.g. `BYRNE, J. A explosão de cursos para executivos nos EUA.` **`Gazeta
  Mercantil`**`, São Paulo, 4 fev. 1992. Administração e Serviços, p. 28.` /
  `LEAL, L. N. P. MP fiscaliza com autonomia total.` **`Jornal do Brasil`**`, Rio de
  Janeiro, p. 3, 25 abr. 1999.`
- Interviews (entrevistas): enter by interviewee or interviewer name; note "Entrevista
  concedida a …".
- **§4.2.3.7/8 electronic (signed / unsigned):** + medium + `Disponível em:` /
  `Acesso em:`. Unsigned enters by first title word in CAPS.

### 2.4 Eventos (§4.2.4) → `@proceedings` and `@inproceedings`
An organized happening (conference, meeting, seminar, symposium, congress).

**§4.2.4.1 Evento no todo em monografia — proceedings as a whole (`@proceedings`):**
> `NOME DO EVENTO EM MAIÚSCULAS, Numeração., ano, local.` **`Título do documento`**`.
> Local da publicação: editor, data.`
- Event name CAPS; document title (e.g. `Anais`) bold; if the document title
  contains the event name, replace it with `[...]`.
- e.g. `ENCONTRO ANUAL DA ANPAD, 14., 1982, Florianópolis.` **`Anais`** `[...]. Belo
  Horizonte: ANPAD, 1990. 9 v.`
- **§4.2.4.2 in a periodical / §4.2.4.3 electronic** variants exist (+ journal data
  / + medium + DOI + `Disponível em:` / `Acesso em:`).

**§4.2.4.5 Trabalho apresentado em evento em monografia (`@inproceedings`) — CORE:**
> `SOBRENOME, Prenome. Título do trabalho.` *`In`*`: NOME DO EVENTO, Numeração.,
> ano, local.` **`Título do documento`** `[...]. Local: editora, data. Página
> inicial-final.`
- e.g. `CORDEIRO, Rosa Inês de N. Descrição e representação de fotografias de cenas
  e fotogramas de filmes: um esquema de indexação.` *`In`*`: CONGRESSO BRASILEIRO DE
  BIBLIOTECONOMIA E DOCUMENTAÇÃO, 16., 1991, Salvador.` **`Anais`** `[...]. Salvador:
  APBEB, 1991. v. 2, p. 1008-1022.`
- **§4.2.4.4** work only presented (not in proceedings): author, title, date of
  presentation. **§4.2.4.6/7/8** electronic / in-periodical variants (+ medium / DOI
  / journal data / `Disponível em:` / `Acesso em:`).

### 2.5 Patentes (§4.2.5) → `@patent` (beyond the core set; capture for later)
> `SOBRENOME DO INVENTOR, Prenome.` **`Título`**`: subtítulo. Depositante:
> nome/titular. Procurador: nome. Número da patente. Data de depósito. Data de
> concessão.`
- e.g. `BERTAZZOLI, Rodnei et al.` **`Eletrodos de difusão gasosa modificados …`**`.
  Depositante: Universidade Estadual de Campinas. Procurador: Maria Cristina Valim
  Lourenço Gomes. BR n. PI0600460-1A. Depósito: 27 jan. 2006. Concessão: 25 mar.
  2008.`

### 2.6 Deferred (exotic) types — §4.2.6 – §4.2.14
Listed in `desiredreferences.md`; implemented after the core set: documentos
jurídicos (legislação, jurisprudência, atos administrativos) and their electronic
variants, documentos civis e de cartórios, documento audiovisual, partituras,
documentos iconográficos, documentos cartográficos, documentos tridimensionais,
documentos de acesso exclusivo em meio eletrônico.

### 2.7 `@misc` and entry-by-title fallback
- **`@misc` (`@diverso`):** all fields optional, **no required fields**, no
  constraints — the catch-all type.
- **No `author` and no `editor` → enter by `title`** (§4.3.2.14), for **all** types:
  biber uses `labeltitle` (so author-date cites render `(Inglês, 2012)`), and the
  bibliography driver prints the title in **entry-by-title format** — first
  significant word in **CAPS**, **no bold** — instead of the author slot + bold
  title.

## 3. Reference elements (fields) — §4.3
A reference begins with the author(s) (personal or entity) **or** the title.

### 3.1 Personal authors (§4.3.1) → `author` (+ `editor`/`translator`/…)
Last surname in **CAPS**, then prename(s)/other surnames, abbreviated or not, as in
the work; use a uniform abbreviation pattern across the list.
- **One author (§4.3.1.1):** `CASTRO, C. M.`
- **Up to three (§4.3.1.2):** each `SOBRENOME, Prenome`, separated by `; `:
  `DAVIS, G. B.; PARKER, C. A.`
- **More than three (§4.3.1.3):** either list **all** (recommended for research
  output) **or** give the first + `et al.` Both are valid — so the style needs a
  configurable `maxbibnames`/`minbibnames` (default: list all, with an option to
  truncate to first `et al.`). `et al.` is a latin expression → italic.

### 3.2 How to reference a personal author (§4.3.2) — name-parsing rules for biber
Mostly handled by biber name parsing + `.bib` `{}` bracketing; record as `lbx`/data
concerns:
- Use names as they appear; initials allowed for uniformity.
- **Spanish (§4.3.2.1):** enter by middle+last surname: `ASTI VERA, A.`
- **Oriental (§4.3.2.2):** not inverted: `CHIU-PING, Liu`, `LOH, Philip Fook Seng`.
- **Antiquity/Middle Ages (§4.3.2.3):** direct order: `PLATÃO.`, `HERÁCLITO, de
  Éfeso.`, `DANTE ALIGHIERI.`
- **Pseudonym (§4.3.2.4):** author's preferred form. Religious/professional/role
  titles are **not** part of the name.
- **Kinship (§4.3.2.5):** surname + kinship word, both CAPS: `ASSAF NETO`,
  `CÂMARA JUNIOR`, `PINTO FILHO` (in `.bib`: `{Assaf Neto}, Alexandre`).
- **Noun+adjective (§4.3.2.6):** `CASTELO BRANCO, Renato`, `VILLAS BOAS, Newton`.
- **Hyphenated (§4.3.2.7):** `SCHIMIDT-NIELSEN, Knut`.
- **Prefixes (§4.3.2.8):** `DE LUCA`, `DI FIORE`, `D'AMBROISIO`, `McDONALD`,
  `O'CONNOR`.
- **Artistic names (§4.3.2.9):** single → `JAMELÃO`; with identifier →
  `ZECA PAGODINHO`, `PAULINHO DA VIOLA`; name+surname → general rule
  (`HOLANDA, Chico Buarque de`); groups direct → `THE BEATLES`, `CORAL DA UFRJ`.
- **Responsibility type (§4.3.2.10):** collection editor → name + singular abbrev in
  parentheses: `HOLANDA, Sérgio Buarque de (org.).` (org./comp./ed./coord.). Other
  roles (tradutor, revisor, ilustrador) come **after the title**:
  `… Tradução de Hernâni Donato.`
- **Psychographed (§4.3.2.11):** `EMMANUEL (Espírito).` **`Alma e coração`**`.
  Psicografado por Francisco Cândido Xavier.`
- **Adapted (§4.3.2.12):** adapter is the author.
- **Entity author (§4.3.2.13):** known form, CAPS, full or abbreviated
  (`ASSOCIAÇÃO BRASILEIRA DE NORMAS TÉCNICAS.`, `PETROBRAS.`); generic name
  prefixed by superior body/jurisdiction (`RIO DE JANEIRO (Estado). Secretaria do
  Meio Ambiente.`); specific name → direct (`COMISSÃO NACIONAL DE ENERGIA
  NUCLEAR`); homonyms → add jurisdiction in parens (`BIBLIOTECA NACIONAL (Brasil)`).
  Events as authors → event name CAPS + `Nº.` (arabic + period) + year + place;
  simultaneous events separated by `;`.
- **Unknown authorship (§4.3.2.14):** enter by **title**; only the first significant
  word in CAPS; never use "anônimo": `GUIA da Ernst & Young: …`.

### 3.3 Title and subtitle (§4.3.3) → `title` / `subtitle`
Reproduce as in the work (page de rosto for monographs). **Title : subtitle**
(colon). The **title is highlighted in bold (negrito)** — italic is **not**
recommended (italic is reserved for foreign words). The highlight goes to the
*document* where the info sits (for a part, the *whole* document is highlighted, not
the part). **Entry by title** → CAPS, no other highlight. Long titles may be
truncated with `[...]`. Parallel titles in other languages → register the first;
optionally a second separated by ` = `. No title → assign a word/phrase in `[ ]`;
artwork → `[Sem título]`.

### 3.4 Edition (§4.3.4) → `edition`
Transcribe with the abbreviation of "edition" in the work's language; Portuguese:
arabic number + `ed.` (`3. ed.`). **Do not state the 1st edition.** Electronic
"version" is treated as edition. Amendments abbreviated: `2. ed. rev.`,
`2. ed. rev. ampl.`, `1. ed. 2. tiragem`, `2nd ed., 3rd impr.`.

### 3.5 Imprenta (§4.3.5) = location + publisher + date
**§4.3.5.1 Location (`location`, ABNT *local*):** city as in the work; add
state/country to disambiguate (`Petrópolis, RJ`). Multiple places, same publisher →
most prominent or first. Place identifiable but not printed → `[São Paulo]`.
Unidentifiable → **`[S. l.]`** (*sine loco*).

**§4.3.5.2 Publisher (`publisher`, ABNT *editora*):** as in the work, abbreviating
prenames and dropping words denoting juridical/commercial nature (`Zahar`, not
`Zahar Editores`; `J. Olympio`). Homonym with an institution → keep `Editora`/`Ed.`
(`Editora UFRJ`). Two publishers → both with their places, separated by `;`
(different cities) or `:` (same city). Three+ → first/prominent. Identifiable but not
printed → `[Ardel]`. Unidentifiable → **`[s. n.]`** (*sine nomine*). Neither place
nor publisher → **`[S. l.: s. n.]`**.

**§4.3.5.3–4 Date / Year (`date`/`year`):** publication (or manufacture,
distribution, recording, access…) date; year in arabic, no spacing/punctuation.

**§4.3.5.5 Dates — general:** multi-volume across years → extreme years with hyphen
(`1926-1940`). Copyright-only → lowercase `c` (`c1993`). Printing/serigraphy only →
state before year. **No date at all → estimate in brackets:** `[1981?]` probable,
`[ca. 1977]` approximate, `[197-]` certain decade, `[197-?]` probable decade,
`[19--]` certain century, `[19--?]` probable century, `[1071 ou 1072]`, `[1987]`
certain but unprinted. Non-Gregorian calendar → Gregorian equivalent after ` = `.
- **§4.3.5.5.1 periodicals:** ended → extreme years (`1969-1973`); current → start
  year + `- ` + period (`1935- .`). **Months abbreviated** in the original language
  per NBR 6023 Annex A; **months with ≤ 4 letters are NOT abbreviated** (so `maio`
  stays full; `jan.`, `fev.`, `abr.`, `ago.`, `set.`, `out.`, `nov.`, `dez.`).
  Ranges separated by `/` (`maio/dez.`). Seasons/divisions as in work, abbreviated.
- **§4.3.5.5.2 day & time:** day in arabic before the month, space-separated
  (`19 jun. 2013`); time after the date when relevant (`23:09`; access `10:05`).

### 3.6 Descrição física (§4.3.6) — complementary
- **§4.3.6.1 pages/volumes (`pagetotal`/`volumes`):** single volume → total `p.`
  (both sides) or `f.` (front only — academic works); multi → `2 v.`; `ca. 860 p`;
  roman pre/post-text → lowercase (`viii, 236 p.`); biblio ≠ physical volumes →
  `5 v. em 3.`; parts/articles → `p. 7-16` (`pages`); `[46] p.`, `Não paginado.`,
  `Paginação irregular.`
- **§4.3.6.2 electronic medium:** state support type; social networks → network
  name `:` profile/page (`Twitter: @redescielo`). → drives medium note.
- **§4.3.6.3 illustrations:** `il.`, `il. color.`, `principalmente il.`,
  `somente il.`, specific (`6 mapas`). → a note, not a core field.
- **§4.3.6.4 dimensions:** height in cm (`21 cm`); exceptional also width
  (`20 cm x 60 cm`).

### 3.7 Série e coleções (§4.3.7) → `series` / `number`
After the physical description, in parentheses; series/collection title separated
from its numbering by a comma: `(Comunicação & Informática)`, `(Princípios, 243)`,
`(Visão do futuro, v. 1)`, `(Biblioteca luso-brasileira, Série brasileira)`.

### 3.8 Notas (§4.3.8) → `note` + specific fields (`url`/`urldate`/`doi`/`type`/…)
At the end of the reference, **no graphic highlight**; wording varies by info.
- **§4.3.8.1 translated docs:** `Tradução de: <original title/language>.`
  (`origtitle`/`origlanguage` + note).
- **§4.3.8.2 multilingual:** note `Texto em espanhol com tradução paralela em
  português.`
- **§4.3.8.3 academic works (`@thesis`):** essential = author, title, subtitle,
  **deposit year**, **work type** (tese/dissertação/TCC), **degree+course** in
  parentheses `(Mestrado em …)`, **academic affiliation**, place, **defense date**.
  Maps to `type` (+ a degree macro), `institution`/`school`, `date`. e.g.
  `LEITE, J. A. A.` **`Manual de preparação …`**`. João Pessoa, 1977. 109 f.
  Dissertação (Mestrado em Administração) - Curso de Administração, Universidade
  Federal da Paraíba, 1977.`
- **§4.3.8.4 unpublished works:** `Palestra`, `Trabalho inédito`, `Mimeografado`,
  `Notas de aula`, `Apostilas`, `Pré-print`, `No prelo` (note + origin/date).
- **§4.3.8.5 abstracts/reviews/offprints/interviews:** referenced as the original
  publication + the source preceded by `Resumo em:`, `Resenha de:`, `Recensão de:`,
  `Separata de:`; interviews `Entrevista concedida a … em <date>.`
- **§4.3.8.6 other notes:** `Bibliografia: p. …`, `ISSN`, `ISBN`, `Anexos: p. …`,
  `Inclui bibliografias e índice`, event-presented note, `Bula de remédio`,
  `Peça em 3 atos`, `Continuação de:`, `Acompanha disquete`, `Projeto em andamento`,
  `Edição fac-similar`, etc.
- **Electronic (used across all types):** `Disponível em: <url>. Acesso em:
  <urldate>.` and `DOI: <doi>.` → fields `url`, `urldate`, `doi`.

## 4. Ordering of references — §4.4
Ordered per the citation system used (NBR 10520): **(a) alphabetic** (alphabetical
order of entry) or **(b) numeric** (citation order in text). Lists generally use a
single alphabetical order of surname/author/title.

- **§4.4.1 Alphabetic system:** all references united at the end in one alphabetical
  order; in-text calls follow the chosen entry (author-data).
  **POST-2020 DELTA:** when the entry (author, or author+title) repeats, the
  subsequent entries are **repeated in full** — the old `______` (6-space dash)
  substitution for a repeated author is **gone**. biblatex: `dashed=false`.
- **§4.4.2 Numeric system:** references in ascending numeric order of citation in the
  text. **Must not** be combined with explanatory footnotes.
