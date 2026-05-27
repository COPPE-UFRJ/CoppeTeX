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
- [x] #13 doc de bibliografia — cap. 5 "Using BibLaTeX": biber, normas ABNT, natbib opção, comandos de citação (args opcionais/"tradução nossa"/apud/múltiplas bibs) e catálogo de todos os tipos de entrada `.bib` com sinônimos PT — `4e9009b`, `1fe1927`. (Resíduo opcional: seção equivalente de tipos no próprio `coppe.pdf`.)
- [x] #14 capítulo "Escrevendo matemática" — align, matrix, subequations, array, `\DeclareMathOperator` (\RMSE/\diag) e nota unicode-math/LuaLaTeX
- [x] #15 `latexmkrc` (biber + makeindex `coppe.ist` p/ listas .lab/.los; engine configurável) — funciona local e no Overleaf; verificado com `latexmk` (biber + listas automáticos); adicionado ao `doall.bat`→`dist/`. Doc detalhada fica no #19.

- [x] #16 capítulo de floats — `\source`/`\fonte` em TODOS os floats (incl. longtable e sidewaystable) + seções 4.4 Subfiguras (subcaption), 4.5 Imagens (graphicx/eps/svg), 4.6 Introdução ao tikz, 4.7 Float vs. inline.
- [x] #17 capítulo "Referências cruzadas, notas e índices" — \label/\ref/\autoref/\pageref, notas de rodapé, hyperref/bookmarks, \url/\href, índice (makeindex + latexmk/Perl/Strawberry), traduções "tradução nossa" (NBR 10520).

- [x] #18 listings & algoritmos — seção 6.1: float Programa, `\pythoninline` inline, bloco `gxoutput` de saída, linguagens (java/xml/html/prolog) e algoritmo em PT (\Para/\Ate/\Enquanto).

- [x] #19 capítulo "Truques de LaTeX" — comentários mágicos (% !TeX), espaço engolido, escopo, \clearpage vs \newpage, latexmkrc/perl. (Inserir magic comments nos arquivos *gerados* é barrado pelo docstrip; `example1.tex` já os tem e o capítulo ensina o padrão.)

- [x] #20 removidos os 4 `.bst` retirados (coppe-plain/coppe-unsrt/en-coppe-plain/en-coppe-unsrt); projeto 100% biblatex+biber.

- [x] #21 formato de data ABNT — datas da bibliografia agora "dia mês. ano" sem "de" (ex.: "4 fev. 1992", "25 abr. 1999", "fev. 1996"); override de \mkbibdatelong/\mkbibdateshort via \AtBeginBibliography (escopo só na bibliografia).

- [x] #22 jurisprudência + partitura — driver de jurisprudência com jurisdição/órgão (CAIXA ALTA), título da decisão, "Relator:" (campo `relator` novo) e data ABNT; partitura ganha a nota de meio "1 partitura" (`addendum`). Exemplo de jurisprudência adicionado.

- [x] #23 títulos iniciados por artigo (B3) — artigo + 1ª palavra significativa em CAIXA ALTA ("AS NORMAS de…"); `\coppeUCtitle` estendido com teste de artigo (`\coppeUCifart`).

## Em andamento
- (nenhuma)

## Pendente (ordem da fila)
- **Fila concluída — #1 a #23 todos feitos.**

## Pós-fila
- [ ] Sincronizar `dist/` e regenerar `coppe.pdf`/`example.pdf` via `doall.bat`.
