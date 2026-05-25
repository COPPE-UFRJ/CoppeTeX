# Rules — `manual2024.pdf` chapters 1–3

Source: **UFRJ/SiBI, *Manual para Elaboração e Normalização de Trabalhos Acadêmicos*, 9. ed., 2025** (file `specs/manual2024.pdf`), chapters 1–3. Chapter 4 (citations & references) is covered separately by the bibliography work / `howto.md` / `explaindiff.md`.

This is TODO2 step 1. Each rule is **unique** and tagged:
- **[G]** general rule (e.g. "paper is A4");
- **[IF]** if-then rule (condition → requirement).

`§` = section in `manual2024.pdf`. **⚠ coppe** marks a likely `coppe.cls` relevance or delta to confirm in the step-2 implementation audit. The manual states its recommendations are *flexible per knowledge area / congregation decision* (§1), so some items are recommendations ("recomenda-se"), flagged **(rec.)**.

---

## Chapter 1 — Introdução (§1)

- **R1** [G] The final version of theses/dissertations/TCC is delivered **digitally only**; physical copies were discontinued (Resolução CEPG 246/2023). *(context, not a layout rule)*
- **R2** [G] Recommendations are **flexible** per knowledge area and academic-congregation decisions. *(meta-rule: COPPE-specific deviations are allowed)*

## Chapter 2 — Apresentação (§2)

### 2.1 Texto (§2.1)
- **R3** [G] The textual part is composed of **introduction, development and conclusion**.
- **R4** [G] The work may be written in **Portuguese, English or Spanish** (Art. 57, Res. CEPG 302/2024). **⚠ coppe** (babel language options).

### 2.2 Formato (§2.2)
- **R5** [G] Paper: white or recycled, **A4 (21 cm × 29,7 cm)**, **portrait** (vertical). **⚠ coppe** (`a4paper`).
- **R6** [G] Body text printed in **black** (illustrations excepted).
- **R7** [G] Main **font size = 12**. **⚠ coppe** (`12pt`).
- **R8** [IF] IF citation > 3 lines, footnote, pagination, or illustration/table caption → use a **smaller, uniform font**.
- **R9** [IF] IF citation > 3 lines → apply a standardized **left-margin indent; recommended 4 cm** (rec.). **⚠ coppe** (`longquote` env). *NB: NBR 10520:2023 makes the 4 cm indent recommended, not mandatory (`explaindiff.md`).*
- **R10** [G] Pre-textual elements go on the **front (anverso)** of the leaf, **except the folha de rosto**, whose **verso** carries the ficha catalográfica.
- **R11** [G] (rec.) Textual and post-textual elements may be printed on **both sides** (anverso e verso). **⚠ coppe** (class is currently `oneside`).
- **R12** [G] The graphic project is the **author's responsibility**.

### 2.3 Margem (§2.3)
- **R13** [IF] IF anverso (front) → margins **left 3 cm, top 3 cm, right 2 cm, bottom 2 cm**. **⚠ coppe** (geometry).
- **R14** [IF] IF verso (back) → margins **left 2 cm, top 3 cm, right 3 cm, bottom 2 cm** (mirror of anverso). **⚠ coppe** (mirrored margins ⇒ two-sided + **binding offset**; user note in `manual2024.txt`:479).

### 2.4 Espaçamento (§2.4)
- **R15** [G] Textual part: **1,5 line spacing**. **⚠ coppe** (`onehalfspacing`).
- **R16** [IF] IF citation > 3 lines, footnote, or reference note → **single spacing**.
- **R17** [IF] IF references list, illustration/table titles, sources & captions, ficha catalográfica, or the nature/objective/institution/area block of the folha de rosto → **single spacing**. (References: also single-space the blank line that separates entries.)
- **R18** [G] Section titles are separated from the preceding/following text by a **1,5 space**.
- **R19** [IF] IF a section title spans more than one line → from the 2nd line, align it **below the first letter of the first word**.
- **R20** [IF] IF on the folha de rosto / folha de aprovação → the nature/objective/institution/area block is aligned from the **middle of the text block to the right margin**. **⚠ coppe**.

### 2.5 Notas de rodapé (§2.5)
- **R21** [G] Footnotes stay **within the margins**, separated from the text by a single space and a **5 cm rule (filete)** from the left margin, in a **smaller font**, with no blank line between notes; from the 2nd line aligned below the first letter.

### 2.6 Indicativos de seções (§2.6)
- **R22** [IF] IF primary section → it **starts on a new (distinct) leaf**.
- **R23** [IF] IF printing on anverso & verso → primary-section titles **start on an odd (anverso) page**.
- **R24** [G] (rec.) Limit section depth to **quinary** (5 levels).
- **R25** [G] A section's **numeric indicative precedes its title**, left-aligned, separated by one space.
- **R26** [IF] IF a heading has **no numeric indicative** (errata, agradecimentos, listas, resumo, sumário, referências, glossário, apêndice, anexo, índice) → **center** it.
- **R27** [G] **Not numbered**: folha de aprovação, dedicatória, epígrafe.
- **R28** [G] Primary sections use **sequential integers from 1**; each lower level appends `.N` to its parent's number.
- **R29** [G] **No point, hyphen, dash or any sign** between the last digit and the title/text.
- **R30** [G] Distinguish heading levels progressively using **negrito / itálico / grifo / redondo / caixa-alta / versal**.
- **R31** [G] The title comes **after its number** (one space); body text starts on a **new line**.
- **R32** [G] In the **sumário**, sections are written exactly as in the body.
- **R33** [IF] IF a section has no title and enumerates items → use **alíneas**: lowercase letters followed by `)`.
- **R34** [G] Alínea formatting: introducing phrase ends with `:`; alíneas ordered alphabetically; letters indented from the left margin; alínea text starts lowercase and ends with `;` (last ends with `.`); continuation lines align under the alínea text; doubled letters when the alphabet is exhausted.
- **R35** [IF] IF cumulative/alternative alíneas → add **"e"/"ou"** before the last one.
- **R36** [IF] IF subdividing an alínea → use a **hyphen** subalínea, placed under the first letter of the alínea text, ending with `,`.
- **R37** [G] Section indicatives are cited along the text (e.g. "... na seção 4", "... ver 2.2").

### 2.7 Paginação (§2.7)
- **R38** [G] All leaves are **counted sequentially from the folha de rosto but not numbered** up to the textual part.
- **R39** [G] The **verso of the folha de rosto** (ficha catalográfica) is **neither counted nor numbered**.
- **R40** [G] **Numbering starts on the first leaf of the textual part**, in **arabic numerals**, in the **top-right corner, 2 cm from the top edge**, last digit **2 cm from the right edge**. **⚠ coppe** (page style / lastpage).
- **R41** [IF] IF printing anverso/verso → page number in the **top OUTER corner** (anverso top-right, verso top-left).
- **R42** [G] Multi-volume: a **single continuous numbering**; apêndice/anexo numbered continuously with the main text.

### 2.8 Siglas (§2.8)
- **R43** [IF] IF an acronym appears for the first time → precede it with the **full form** and put the acronym in **parentheses** (e.g. "Universidade Federal do Rio de Janeiro (UFRJ)").

### 2.9 Equações e fórmulas (§2.9)
- **R44** [IF] IF an equation is displayed (separated from the paragraph) → highlight it (e.g. centered); if needed, **number it in parentheses, right-aligned**.
- **R45** [IF] IF a displayed equation breaks across lines → break **before `=`** or **after `+`, `−`, `×`, `÷`**.

### 2.10 Ilustrações (§2.10)
- **R46** [G] Illustration identification appears on **top**: designative word + **order number (arabic)** + **travessão (–)** + brief title/caption. Applies to gráfico, desenho, esquema, diagrama, fluxograma, fotograma, quadro, mapa, planta, retrato, etc.
- **R47** [G] Place the illustration **as close as possible** to the text that refers to it.
- **R48** [G] The **source on the bottom is MANDATORY** (even for the author's own production), per ABNT NBR 10520. **⚠ coppe** (TODO2 `\source`/`\fonte` feature).
- **R49** [G] Type, order number, title, source, legend and notes must **respect the illustration's margins**.

### 2.11 Tabelas, quadros e figuras (§2.11)
- **R50** [G] Tables present statistically-treated data, with an objective title and **sequential arabic numbering**.
- **R51** [G] Identification appears on **top**: designative word + order number (arabic), per IBGE.
- **R52** [G] The **source on the bottom** follows ABNT NBR 10520; for the author's own work use "elaborada pelo próprio autor" / "elaboração própria" / "o próprio autor". **⚠ coppe** (TODO2 `\source`/`\fonte`).
- **R53** [IF] IF **quadro** → data delimited by lines on **all** margins. IF **tabela** → delimiting lines **only top and bottom** (IBGE distinction). **⚠ coppe** (TODO2 quadro vs table).

## Chapter 3 — Estrutura do trabalho acadêmico (§3)

### 3.1.1 Capa (§3.1.1)
- **R54** [G] The **capa is mandatory**, with these items in order: institution name; author's full name; title; subtitle (if any); number of volumes (if > 1); place (city) of the institution; year of deposit.

### 3.1.2 Elementos pré-textuais (§3.1.2)
- **R55** [G] Pre-textual order: folha de rosto (ficha catalográfica on verso) → errata → folha de aprovação → dedicatória → agradecimentos → epígrafe → resumo (vernáculo) → resumo (estrangeiro) → lista de ilustrações → lista de tabelas → lista de abreviaturas e siglas → lista de símbolos → sumário. **⚠ coppe** (front-matter order).

#### Essenciais (§3.1.2.1)
- **R56** [G] **Folha de rosto** (mandatory) — anverso: author; main title (clear, precise); subtitle (preceded by `:`); number of volumes; nature + objective + institution + area of concentration; advisor (and co-advisor if any); place; year of deposit. **⚠ coppe**.
- **R57** [G] Folha de rosto — verso: the **ficha catalográfica** per AACR2 (use the SiBI generator), placed immediately after the folha de rosto. **⚠ coppe** (ficha catalográfica page).
- **R58** [G] **Folha de aprovação** must contain: author; full title + subtitle; nature/objective/institution/area; approval date; name, titulação and institution of each examining-board member, with the **advisor first** (board president). **⚠ coppe**.
- **R59** [G] **Resumo (vernáculo)**: 1,5 spacing, a **single paragraph**, preferably 3rd-person singular + active voice, **150–500 words**.
- **R60** [G] **Keywords** follow the abstract: preceded by "palavras-chave:", separated by `;`, lowercase initial (except proper nouns / scientific names).
- **R61** [G] **Resumo (estrangeiro)**: a version of the vernacular abstract in an international language.
- **R62** [G] **Sumário** is the **last** pre-textual element, starts on an anverso; titles follow the section indicatives, left-aligned (aligned by the longest indicative's margin); written exactly as in the body. The sumário is **not** the índice.

#### Opcionais (§3.1.2.2)
- **R63** [IF] IF an errata is needed → place it **after the folha de rosto** (a list of leaf/line + correction, preceded by the work's reference). *(rarely needed now)*
- **R64** [G] **Dedicatória**: after the folha de aprovação; (rec.) aligned from the middle of the page to the right margin, at the bottom.
- **R65** [G] **Agradecimentos**: after the dedicatória; the word **"AGRADECIMENTOS" in caixa-alta + negrito**.
- **R66** [IF] IF a pre-textual **epígrafe** → it need **not** follow NBR 10520; IF an epígrafe opens a primary section → it **must** follow NBR 10520. (rec.) aligned middle-to-right, bottom.
- **R67** [G] **Lista de ilustrações**: in text order, each item = specific name + travessão + title + leaf/page; a separate list per type when needed.
- **R68** [G] **Lista de tabelas**: in text order, specific name + page.
- **R69** [G] **Lista de abreviaturas e siglas**: alphabetical, with the full expressions; (rec.) separate lists. **⚠ coppe** (`\makeloabbreviations`).
- **R70** [G] **Lista de símbolos**: in order of appearance, with meanings. **⚠ coppe** (`\makelosymbols`).

### 3.1.3 Parte textual (§3.1.3)
- **R71** [G] The textual part contains: introdução; desenvolvimento; conclusão (considerações finais); recomendações (optional).

### 3.1.4 Parte pós-textual (§3.1.4)
- **R72** [G] Post-textual items: **referências (mandatory)**, glossário, apêndice, anexos, índice.
- **R73** [G] The reference list must be a **separate chapter named "Referências"** — explicitly **not "Bibliografia"** (§3.1.4.1, footnote 5), per NBR 6023; detailed rules in §4.2. **⚠ coppe — DELTA: the coppe build currently titles it "Bibliografia".**
- **R74** [G] **Glossário** (optional): technical terms with definitions, in alphabetical order.
- **R75** [G] **Apêndice** (optional, author-made): identified by **consecutive UPPERCASE letters + travessão + title**.
- **R76** [G] **Anexo** (optional, not author-made): consecutive UPPERCASE letters + travessão + title; doubled letters when the alphabet is exhausted; same typographic emphasis as a primary section. **⚠ coppe** (`\annex`).
- **R77** [IF] IF an anexo contains references → they go in a footnote within the element or as a specific list.
- **R78** [G] **Índice** (optional): a list of words/phrases that locate information, placed at the **end** of the publication.
