# desiredelements.md — reference elements from manual2024 §4.3

Every reference **element** defined in `specs/manual2024.pdf` §4.3 (and the
data-bearing elements used in §4.2 templates). These become the **biblatex fields**
of the new CoppeTeX style. Each gets an **English** primary name (biblatex-standard
where one exists) and an **unaccented Portuguese synonym** (todo Convert §10–11).

Mappings are a *proposal*, finalized for your approval in `mapping.csv` (Stage 2).
`std` = biblatex provides this field natively; `new` = must be declared in our
custom datamodel (`.dbx`). **Scope:** `CORE` = needed by the Phase-1 core types;
`DEFER` = only needed by deferred (exotic) types.

> Reminder (todo §23–24): fields carry **plain data only**. All highlighting
> (bold title, italic `In:`/`et al.`, CAPS surnames, `Disponível em:` / `Acesso
> em:` wording, `[S. l.]` etc.) is applied by the **style at output**, never written
> into the `.bib`.

## Authorship & responsibility (§4.3.1 – §4.3.2)

| § | ABNT element | Field (EN) | PT synonym | Kind | Scope | Notes |
|---|--------------|-----------|-----------|------|-------|-------|
| 4.3.1 | Autor pessoal / entidade | `author` | `autor` | std | CORE | surname CAPS at output; corporate as `{Name}`. |
| 4.3.2.10 | Organizador/compilador/coordenador | `editor` + `editortype` | `organizador` | std | CORE | `(org.)`/`(comp.)`/`(coord.)` rendered from `editortype`. |
| 4.3.2.10 | Tradutor | `translator` | `tradutor` | std | CORE | rendered after title (`Tradução de …`). |
| 4.3.2.10 | Ilustrador / outros | `namea`+`nameatype` | `ilustrador` | new | DEFER | other responsibility roles. |
| 4.3.2.13 | Autor entidade (jurisdição) | `author` | `autor` | std | CORE | hierarchy via `{Sup. Sub}`; homonym jurisdiction in note. |

## Title (§4.3.3)

| § | ABNT element | Field (EN) | PT synonym | Kind | Scope | Notes |
|---|--------------|-----------|-----------|------|-------|-------|
| 4.3.3 | Título | `title` | `titulo` | std | CORE | **bold** at output (entry-by-title → CAPS, no bold). |
| 4.3.3 | Subtítulo | `subtitle` | `subtitulo` | std | CORE | separated by `:` at output. |
| 4.2.3.4 | Título do periódico/jornal | `journaltitle` | `periodico` | std | CORE | the bold element of `@article`. |
| 4.2.1.3 | Título do livro (da parte) | `booktitle` | `titulodolivro` | std | CORE | for `@incollection`/`@inproceedings`. |
| 4.2.4 | Nome do evento | `eventtitle` | `evento` | std | CORE | event name (CAPS) for proceedings/inproceedings. |
| 4.3.3 | Título paralelo (outro idioma) | `titleaddon` | `tituloparalelo` | std | DEFER | ` = ` separated. |

## Imprenta (§4.3.5) — place, publisher, date

| § | ABNT element | Field (EN) | PT synonym | Kind | Scope | Notes |
|---|--------------|-----------|-----------|------|-------|-------|
| 4.3.5.1 | Local de publicação | `location` | `local` | std | CORE | `[S. l.]` when absent (style-supplied). |
| 4.3.5.2 | Editora | `publisher` | `editora` | std | CORE | `[s. n.]` when absent (style-supplied). |
| 4.3.5.3/4 | Data / Ano | `date` (`year`) | `data` (`ano`) | std | CORE | ISO `date` preferred; `year` synonym. No-date forms from `date` granularity. |
| 4.3.5.5.1 | Mês / período | (part of `date`) | — | std | CORE | abbreviated per Annex A; ≤4-letter months not abbreviated (lbx). |
| 4.3.5.5 | Copyright / impressão only | `date` (+ flag) | `data` | std | DEFER | `c1993`, printing-only. |

## Physical description (§4.3.6) & series (§4.3.7)

| § | ABNT element | Field (EN) | PT synonym | Kind | Scope | Notes |
|---|--------------|-----------|-----------|------|-------|-------|
| 4.3.6.1 | Total de páginas/folhas | `pagetotal` | `totaldepaginas` | std | CORE | `p.` vs `f.` distinction → see `pagination` below. |
| 4.3.6.1 | Páginas inicial-final | `pages` | `paginas` | std | CORE | parts/articles (`p. 7-16`). |
| 4.3.6.1 | Folhas vs páginas | `pagination`/`bookpagination` | `paginacao` | std | CORE | value `leaf` → renders `f.`. |
| 4.3.6.1 | Volume (da parte) | `volume` | `volume` | std | CORE | article/collection volume. |
| 4.3.6.1 | Total de volumes | `volumes` | `volumes` | std | DEFER | `2 v.`, `5 v. em 3.` |
| 4.2.3 | Número / fascículo | `number` | `numero` | std | CORE | issue number `n.` |
| 4.3.6.3 | Ilustrações | `note`/`addendum` | `ilustracoes` | std | DEFER | `il.`, `il. color.` |
| 4.3.6.4 | Dimensões | `addendum` | `dimensoes` | std | DEFER | `21 cm`. |
| 4.3.7 | Série / coleção | `series` | `serie` | std | DEFER | `(Série, n)`. |
| 4.3.7 | Número na série | `number` | `numerodaserie` | std | DEFER | within `series`. |

## Electronic & identifiers (§4.3.6.2, §4.3.8)

| § | ABNT element | Field (EN) | PT synonym | Kind | Scope | Notes |
|---|--------------|-----------|-----------|------|-------|-------|
| 4.2.x | Endereço eletrônico | `url` | `url` | std | CORE | rendered `Disponível em: <url>.` |
| 4.1/4.2 | Data de acesso | `urldate` | `dataacesso` | std | CORE | rendered `Acesso em: <date>.` |
| 4.2.3.5 | DOI | `doi` | `doi` | std | CORE | rendered `DOI: <doi>.` |
| 4.3.6.2 | Tipo de suporte/meio | `howpublished` | `meio` | std | DEFER | CD/DVD/pen drive/online/social. |
| 4.3.8.6 | ISSN | `issn` | `issn` | std | DEFER | periodicals. |
| 4.3.8.6 | ISBN | `isbn` | `isbn` | std | DEFER | monographs. |

## Edition & academic works (§4.3.4, §4.3.8.3)

| § | ABNT element | Field (EN) | PT synonym | Kind | Scope | Notes |
|---|--------------|-----------|-----------|------|-------|-------|
| 4.3.4 | Edição | `edition` | `edicao` | std | CORE | `3. ed.`; never "1. ed.". |
| 4.3.8.3 | Tipo de trabalho | `type` | `tipo` | std | CORE | Dissertação / Tese / TCC. |
| 4.3.8.3 | Grau + curso | `type`/macro | `grau` | new | CORE | `(Mestrado em …)`. |
| 4.3.8.3 | Vinculação acadêmica | `institution`/`school` | `instituicao` | std | CORE | unit + university. |
| 4.3.8.1 | Tradução de (orig.) | `origtitle`/`origlanguage` | `traducaode` | std | DEFER | `Tradução de: …`. |
| 4.3.8 | Nota livre | `note`/`addendum` | `nota` | std | CORE | free note at end, no highlight. |

## Custom fields for deferred (exotic) types

| § | ABNT element | Field (EN) | PT synonym | Kind | Scope | Notes |
|---|--------------|-----------|-----------|------|-------|-------|
| 4.2.2 | Destinatário (carta) | `recipient` | `destinatario` | new | DEFER | rendered `Destinatário: …`. |
| 4.2.5 | Depositante (patente) | `holder` | `depositante` | std | DEFER | patent applicant/holder. |
| 4.2.5 | Procurador (patente) | `agent` | `procurador` | new | DEFER | patent agent. |
| 4.2.5 | Nº / data depósito / concessão | `number`/`date`/`...` | `numero`/`datadeposito` | new | DEFER | patent-specific dates. |
| 4.2.3.1 | Periodicidade | `note` | `periodicidade` | std | DEFER | `Mensal`, `Trimestral`. |

## Citation-only locators (§4.1) — not `.bib` fields
Page/locator passed as the biblatex post-note: `p.` (page), `par.` (paragraph),
`min.`, `slide`, `local.`, plus volume/section ordering (author, date, volume/
section, page). Handled by `\cite[…]{…}`, not stored in the entry.

## Open questions for the mapping (to resolve in mapping.csv review)
1. PT synonyms: confirm unaccented spellings (e.g. `edicao`, `traducaode`,
   `datadeposito`). Any you want pluralized or hyphenated differently?
2. `pagetotal` (`p.` total) vs `pages` (range): keep both with the `pagination=leaf`
   trick to switch `p.`→`f.`? (Proposal: yes.)
3. Academic degree+course: a single `type` string vs a structured `degree` + `field`
   custom pair? (Proposal: `type` for the work kind + a free note for `(Grau em
   Curso)`, simplest and ABNT-faithful.)
4. Confirm which deferred custom fields (`recipient`, `agent`, patent dates) to
   declare now in the datamodel vs add when their types are implemented.

## Custom fields for games / software / audiovisual (added 2026-05-23)

For the custom `game`/`videogame`/`boardgame`/`tvshow` types and the native
`software`/`movie`/`video` types. Declared in `coppe.dbx`.

| ABNT/role | Field (EN) | PT synonym | Kind | Scope | Notes |
|---|---|---|---|---|---|
| Designer/criador | `author` | `autor` | std | CORE | personal (`Meier, Sid`) or corporate (`{Firaxis Games}`). |
| Artista (arte) | `artist` | `artista` | new | CORE | game/illustration art credit. |
| Versão | `version` | `versao` | std | CORE | software/game version (native biblatex field). |
| Plataforma | `platform` | `plataforma` | new | CORE | videogame platform (PC, PS5, …). |
| Diretor | `director` | `diretor` | new | CORE | movie/tvshow/video director. |
| Produtor(a) | `producer` | `produtor` | new | DEFER | movie/tvshow producer or studio. |
| Editora/distribuidora | `publisher`/`organization` | `editora` | std | CORE | doubles as label when no personal author (PUBLISHER, YEAR rule). |

**Label fallback (PUBLISHER, YEAR).** For these types, define `labelname` to fall
back author → editor → `publisher`/`organization`, so a game/software with no
personal author cites as `(Firaxis Games, 2016)`.
