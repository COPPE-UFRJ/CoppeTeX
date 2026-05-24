# desiredreferences.md — reference types from manual2024 §4.2

Every reference type defined in `specs/manual2024.pdf` §4.2 (ABNT NBR 6023,
post-2020). These become the **biblatex entry types** of the new CoppeTeX style.
Each will get an **English** primary name and an **unaccented Portuguese synonym**
(todo Convert §8–9). The English/PT mapping below is a *proposal* — it is finalized
for your approval in `mapping.csv` (Stage 2 gate).

**Type collapsing (todo §25).** Author-count presentations from §4.3.1 — "obra de um
só autor", "obra com até três autores", "obra com mais de três autores", "obra de
autor pessoal" — are **not** separate types; they are the same type (usually
`book`) with different author rendering, handled by the style. So the inventory
below is by *document category* (§4.2), not by author count.

**Print vs electronic.** ABNT lists "… em meio eletrônico" as separate sub-sections,
but they take the *same* entry type plus the online fields (`url`/`urldate`, `doi`,
medium). We will **not** create separate entry types for electronic variants — a
single type carries both, and the presence of `url`/`doi` triggers the
`Disponível em:` / `Acesso em:` / `DOI:` output.

Legend — **Scope:** `CORE` = Phase-1 core academic set (implement + test first);
`DEFER` = implement after the core set.

## Core academic types

| § | ABNT type | Proposed entry (EN) | PT synonym | Scope | Notes |
|---|-----------|---------------------|-----------|-------|-------|
| 4.2.1.1 | Monografia no todo (livro/folheto) | `@book` | `@livro` | CORE | guide, catalog, encyclopedia, dictionary as whole. Collapses "obras de 1 / até 3 / +3 autores". |
| 4.2.1.1 | Trabalho acadêmico — genérico | `@thesis` / `@dissertation` | `@tese` / `@dissertacao` | CORE | generic; **requires `type`** (localized key or literal) for variation. |
| 4.2.1.1 | Dissertação de mestrado (M.Sc.) | `@masterdissertation` | `@dissertacaomestrado` | CORE | →`thesis`, `type`=`mscdiss`; syn. `@mscdissertation`. |
| 4.2.1.1 | Tese de doutorado (D.Sc.) | `@dscthesis` | `@tesedoutorado` | CORE | →`thesis`, `type`=`dscthesis`. |
| 4.2.1.1 | Tese de doutorado (Ph.D.) | `@phdthesis` | `@tesephd` | CORE | →`thesis`, `type`=`phdthesis`. |
| 4.2.1.1 | Trabalho de Conclusão de Curso | `@tcc` | `@tcc` | CORE | →`thesis`, `type`=`tcc`. |
| — | Diversos / catch-all | `@misc` | `@diverso` | CORE | **all fields optional**; no required fields; no-author/editor → entry by title. |
| 4.2.1.2 | Monografia no todo em meio eletrônico | `@book` (+online) | `@livro` | CORE | same entry + `url`/`doi`/medium. |
| 4.2.1.3 | Parte de monografia (capítulo) | `@incollection` | `@partedelivro` | CORE | chapter with its own author. `In:` (italic). |
| 4.2.1.3 | Parte de monografia (mesmo autor do todo) | `@inbook` | `@emlivro` | CORE | part by the book's author. |
| 4.2.1.3 | Verbete de enciclopédia/dicionário | `@inreference` | `@verbete` | CORE | with or without authorship. |
| 4.2.3.4 | Artigo/matéria de revista, boletim | `@article` | `@artigo` | CORE | journal name is the bold element. |
| 4.2.3.5 | Artigo de revista em meio eletrônico | `@article` (+online) | `@artigo` | CORE | + `doi`/`url`. |
| 4.2.3.6 | Artigo/matéria de jornal | `@article` (newspaper) | `@artigodejornal` | CORE | `journaltitle` = newspaper; section/caderno; page-before-date when no section. |
| 4.2.3.7/8 | Matéria de jornal em meio eletrônico (assinada/não) | `@article` (+online) | `@artigodejornal` | CORE | unsigned → entry by title. |
| 4.2.4.1 | Evento no todo em monografia (anais) | `@proceedings` | `@anais` | CORE | event name CAPS; `Anais`/`Proceedings` bold. |
| 4.2.4.5 | Trabalho apresentado em evento (em monografia) | `@inproceedings` | `@trabalhodeevento` | CORE | the standard conference paper. |

## Periodicals & sub-parts (supporting the article core)

| § | ABNT type | Proposed entry (EN) | PT synonym | Scope | Notes |
|---|-----------|---------------------|-----------|-------|-------|
| 4.2.3.1 | Periódico no todo | `@periodical` | `@periodico` | CORE | enters by title (CAPS); ISSN, periodicity. |
| 4.2.3.2 | Parte da coleção de periódico | `@periodical` | `@periodico` | DEFER | subset of periodical. |
| 4.2.3.3 | Partes de revista/boletim (fascículo sem título) | `@suppperiodical` | `@fasciculo` | DEFER | issue/fascicle without own title. |
| 4.2.2 | Correspondência (carta, bilhete, cartão) | `@letter` | `@correspondencia` | DEFER | sender/recipient/place/date. |
| 4.2.4.2 | Evento no todo em publicação periódica | `@proceedings` | `@anais` | DEFER | + journal data. |
| 4.2.4.4 | Trabalho apenas apresentado (não nos anais) | `@unpublished` | `@trabalhoapresentado` | DEFER | presented, not published. |
| 4.2.4.7 | Trabalho em evento em publicação periódica | `@inproceedings` | `@trabalhodeevento` | DEFER | event note + journal data. |

## Deferred (exotic) types — §4.2.5 – §4.2.14

| § | ABNT type | Proposed entry (EN) | PT synonym | Scope | Notes |
|---|-----------|---------------------|-----------|-------|-------|
| 4.2.5 | Patente | `@patent` | `@patente` | DEFER | inventor, depositante, procurador, nº, depósito/concessão. |
| 4.2.6.1 | Legislação | `@legislation` | `@legislacao` | DEFER | jurisdiction entry by entity (CAPS). |
| 4.2.6.2 | Jurisprudência (decisão judicial) | `@jurisdiction` | `@jurisprudencia` | DEFER | court decisions. |
| 4.2.6.3 | Atos administrativos normativos | `@legislation` | `@atonormativo` | DEFER | portarias, resoluções, etc. |
| 4.2.7 | Documentos jurídicos em meio eletrônico | (above) (+online) | — | DEFER | + `url`/`doi`. |
| 4.2.8 | Documentos civis e de cartórios | `@legal` | `@documentocivil` | DEFER | certidões, escrituras. |
| 4.2.9 | Documento audiovisual | `@video` | `@audiovisual` | DEFER | film, TV, video. |
| 4.2.10 | Partitura | `@music` | `@partitura` | DEFER | musical score; 4.2.10.1 electronic. |
| 4.2.11 | Documento iconográfico | `@image` | `@iconografico` | DEFER | photo, drawing, print; 4.2.11.1 electronic. |
| 4.2.12 | Documento cartográfico | `@map` | `@cartografico` | DEFER | maps, atlases; 4.2.12.1 electronic. |
| 4.2.13 | Documento tridimensional | `@artwork` | `@tridimensional` | DEFER | sculpture, object, model. |
| 4.2.14 | Documento de acesso exclusivo em meio eletrônico | `@online` | `@online` | DEFER | website, post, social media, e-mail. |

## Open questions for the mapping (to resolve in mapping.csv review)
1. Newspaper article: keep under `@article` (distinguished by fields) or a dedicated
   `@artigodejornal` entry type? (Proposal: one `@article`, behavior driven by
   `journaltitle`/`section`/`entrysubtype`.)
2. Academic works: one `@thesis` with a `type` field, with `@mastersthesis` /
   `@phdthesis` / `@monografia` / `@tcc` as synonyms presetting `type`? (Proposal:
   yes.)
3. `@inbook` vs `@incollection` split — keep both (ABNT distinguishes "same author"
   vs "different author" only by repeating the name after `In:`), or collapse to one?
   (Proposal: keep biblatex's standard split.)
4. Entry types not native to biblatex will be declared in our custom datamodel
   (`.dbx`). Confirm naming at mapping time. (NB: most are native — see next section.)

## Full standard biblatex entry types (adopt ALL, per cross-check rule)

Rule (added 2026-05-23): derive the type set from biblatex's standard datamodel
(`blx-dm.def`), not only from the ABNT manual — this caught a missing `@report`.
**All** of these standard types are supported (drivers ABNT-tweaked as needed); each
gets an unaccented PT synonym. Scope = which get a dedicated ABNT driver first.

| biblatex type | PT synonym | Scope | Notes |
|---|---|---|---|
| `report` | `relatorio` | **CORE** | technical report; `techreport`/`relatoriotecnico` synonyms (biblatex maps `techreport`→`report`). **Was missing — now core.** |
| `manual` | `manual` | CORE | technical manual/standard docs. |
| `online` | `online` | CORE | website/page (ABNT 4.2.14). |
| `book`,`inbook`,`incollection`,`inreference`,`article`,`proceedings`,`inproceedings`,`thesis`,`periodical`,`misc` | (see core tables) | CORE | already specified above. |
| `software` | `software` | CORE | see custom-fields note + (PUBLISHER, YEAR) rule below. |
| `movie` | `filme` | CORE | audiovisual (ABNT 4.2.9); native type. |
| `video` | `video` | DEFER | online/recorded video. |
| `dataset` | `conjuntodedados` | DEFER | research data. |
| `letter` | `correspondencia` | DEFER | already in core tables. |
| `patent` | `patente` | DEFER | already listed. |
| `music`,`audio` | `partitura`,`audio` | DEFER | scores/recordings. |
| `image`,`artwork` | `iconografico`,`obradearte` | DEFER | iconographic/3D. |
| `legislation`,`jurisdiction`,`legal` | `legislacao`,`jurisprudencia`,`documentojuridico` | DEFER | native; legal docs. |
| `standard` | `norma` | DEFER | technical standards. |
| `performance` | `performance` | DEFER | live performance. |
| `booklet`,`collection`,`mvbook`,`mvcollection`,`mvproceedings`,`mvreference`,`reference`,`bookinbook`,`suppbook`,`suppcollection`,`suppperiodical`,`set`,`unpublished`,`review`,`commentary`,`bibnote`,`customa`–`f` | (as needed) | DEFER | inherit standard behavior + ABNT tweaks. |

## Custom CoppeTeX entry types (not in biblatex)

For games and TV — declared in `coppe.dbx`. Many cite as **(PUBLISHER, YEAR)** unless
there is an explicit personal author (e.g. Sid Meier); see the label rule below.

| Custom type | PT synonym | Scope | Key fields |
|---|---|---|---|
| `game` | `jogo` | CORE | `author` (designer, personal or corporate), `artist`, `publisher`, `date`, `version`, `note`. |
| `boardgame` | `jogodetabuleiro` | CORE | as `game`. |
| `videogame` | `videogame` (syn `jogoeletronico`) | CORE | as `game` + `platform` (PC/console). |
| `tvshow` | `programadetv` (syn `serietv`) | CORE | `title`, `director`, `producer`, `publisher`/network, `date`; entry by title. |
| (`movie`,`software` are native — see above) | | | `movie`: `director`,`producer`; `software`: `author`/`organization`,`version`. |

**(PUBLISHER, YEAR) label rule.** For `game`/`videogame`/`boardgame`/`software`
(and `movie`/`tvshow`), when there is no personal `author`, the citation label and
the reference head fall back to the **corporate author** — put the company in
`author` as `author={{Firaxis Games}}`, OR rely on a `labelname` fallback to
`publisher`/`organization`. With an explicit designer use `author={Meier, Sid}`.
