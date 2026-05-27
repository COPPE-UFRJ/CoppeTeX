# Fila de tarefas — CoppeTeX (ramo `futuro2026`)

Fila mestra do que precisa ser feito. **Atualizada e commitada a cada ciclo.**
Fontes: `TODO4.md` (#8–#20), revisão/plano de correção (#21–#23),
`InstrucoesClaude/registro-comandos.md` + tarefas de formatação (#1–#7).

Legenda: `[x]` concluído · `[~]` em andamento · `[ ]` pendente.

## Concluído
- [x] #1 B3 — entrada por título: 1ª palavra em CAIXA ALTA (ABNT 4.2) — `61974c3`
- [x] #2 Capa (Anexo A), nome completo da COPPE + programa de `\department` — `9432682`
- [x] #3 B4 — artigo/matéria de jornal (caderno/seção, `entrysubtype=newspaper`) — `46a69af`
- [x] #4 B2 — tipos exóticos ABNT: patente, legislação/jurisprudência/legal, mapa — `ea40092`, `beb4449`
- [x] #5 A1 — APÊNDICE/ANEXO no Sumário (R75/R76) — `1e802ec`
- [x] #6 A2 — ficha catalográfica no verso da folha de rosto (NBR 14724 R57) — `65bc2d2`
- [x] #7 Revisão completa → plano de correção
- [x] #8 apud — só a obra consultada entra na lista de referências — `9c22c8a`
- [x] #9 `coppe.bbx` usável isolado (carrega `setspace`) — `2163017`
- [x] #10 versão 3.8 unificada + `hologo` na classe — `9ccb47c`
- [x] #11 logos `\TeX/\LaTeX/...` via `hologo` (classe + driver) — `263c614`
- [x] #12 compatível com LuaLaTeX e pdfLaTeX (`iftex`, aviso pró-LuaLaTeX) — `2a4d234`

## Em andamento
- [~] #13 doc de bibliografia — cap. 5 "Using BibLaTeX" feito (`4e9009b`).
  Falta: catálogo de **todos** os tipos de entrada `.bib` (no example e numa seção do `coppe.pdf`).

## Pendente (ordem da fila)
- [ ] #14 capítulo de matemática (align/matrix/subequations/array, `\DeclareMathOperator`, unicode-math)
- [ ] #15 Overleaf × local (`latexmkrc` + perl, instruções nos dois)
- [ ] #16 capítulo de floats (`\source` em todos incl. longtable/rotated, subcaption, imagens/graphicx/svg, tikz, tabelas)
- [ ] #17 capítulo de referências (footnotes, hyperref/bookmarks, URLs com quebra, índices/perl, traduções "tradução nossa")
- [ ] #18 capítulo de listings & algoritmos (como implementados)
- [ ] #19 capítulo de truques LaTeX (magic comments `% !TeX`, espaço engolido, scoping, `\clearpage` vs `\newpage`, latexmkrc)
- [ ] #20 remover resíduos do bibtex (`.bst` e temporários)
- [ ] #21 formato de data ABNT — remover "de…de" → "25 abr. 1999" (NBR 6023 §4.3.5.5.2; alto impacto visual)
- [ ] #22 driver de jurisprudência (decisão judicial) + nota de meio da partitura ("1 partitura")
- [ ] #23 títulos iniciados por artigo (B3): "A HISTÓRIA…" (artigo + 1ª palavra significativa)

## Pós-fila
- [ ] Sincronizar `dist/` e regenerar `coppe.pdf`/`example.pdf` via `doall.bat`.
