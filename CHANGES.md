# CoppeTeX 4.0 — Registro de mudanças

Versão da classe: **3.8** (`coppe.cls`, 2026).

Este documento resume **todas** as mudanças do CoppeTeX 4.0 em relação à versão
anterior (3.4). O 4.0 tem dois eixos:

1. **Bibliografia e citações** — migração de BibTeX/natbib para **BibLaTeX + biber**,
   em conformidade com a ABNT **NBR 6023** (pós-2020) e **NBR 10520:2023**.
2. **Formatação gráfica** — conformidade com o *Manual para Elaboração e
   Normalização de Trabalhos Acadêmicos* da UFRJ/COPPE (`manual2024`), capítulos
   1 a 3.

> **Processo:** o trabalho 4.0 vive no ramo `futuro2026`. O ramo `master`
> permanece na linha-base aprovada pela CPGP — mudanças de estilo só entram em
> `master` após aprovação da CPGP.

---

## ⚠️ Mudança importante na compilação: BibTeX → biber

A bibliografia agora é processada por **biber**, não mais por bibtex. Quem usa
`doall.bat` / `Makefile` / `latexmk` não precisa fazer nada (já foram
atualizados). Em compilação manual:

```
pdflatex example
biber example          # <- era "bibtex example"
makeindex ...          # listas de símbolos/abreviaturas (inalterado)
pdflatex example
pdflatex example
```

No documento, a base passou a ser declarada no preâmbulo e impressa no ponto
desejado:

```latex
\addbibresource{minhabase.bib}   % no preâmbulo (era \bibliography na hora de imprimir)
...
\printbibliography               % onde a lista deve aparecer (era \bibliography{...})
```

Não há mais `\bibliographystyle` nem arquivos `.bst`.

---

## Fase 1 — Bibliografia e citações (ABNT NBR 6023 / NBR 10520:2023)

- **Motor próprio em BibLaTeX/biber.** Estilo `coppe` (`coppe.bbx`, `coppe.cbx`,
  `coppe.dbx` e os `*-coppe.lbx`) construído sobre o *core* do biblatex —
  **não** depende do pacote `biblatex-abnt` (que implementa a edição de 2018).
- **Estilos:** autor-data por padrão; **numérico** opcional pela opção de classe
  `numbers`; o numérico lista as referências na **ordem de citação** (sem
  ordenação alfabética), atendendo ao requisito "unsorted".
- **Compatível com natbib** (`\citet`, `\citep`) — via a opção `natbib=true` do
  próprio biblatex.
- **Tipos de entrada em inglês com sinônimos em português** (sem acento):
  `@livro` = `@book`, `titulo` = `title`, `autor` = `author`, etc. Tipos afins são
  agrupados sob o nome em inglês (todas as "obras de N autores" → `book`).
- **Cobertura ampla de tipos** (datamodel padrão do biblatex + extras): inclui
  `@report` (relatório técnico), `@online`, `@manual`, e tipos personalizados
  como `@game`/`@videogame`/`@boardgame`, `@software`, `@movie`/`@tvshow`
  (jogos/softwares citam como (EDITORA, ANO) quando não há autor pessoal).
- **Família de teses:** `@thesis`/`@dissertation` genéricos exigem o campo `type`;
  os específicos `@masterdissertation` (sin. `@mscdissertation`), `@dscthesis`,
  `@phdthesis` e `@tcc` predefinem o tipo localizado.
- **Entrada pelo título** quando não há autor nem editor (primeira palavra em
  caixa alta), conforme §4.3.2.14.
- **Citações conforme a NBR 10520:2023** (implementadas em `coppe.cbx`):
  - nomes em **caixa normal** no texto (ex.: "Chartier (2002)"), e **CAIXA ALTA**
    apenas nos sobrenomes da lista de referências;
  - ponto final **fora** da citação;
  - separador **ponto e vírgula** em citações *parentéticas* vs. vírgula + "e"
    nas *narrativas* (`\textcite`/`\citet`);
  - `apud` em **itálico**, com `\citetapud` / `\citepapud` (citação de citação,
    §4.1.2.2.1).
- **Cabeçalho da lista:** a lista pós-textual chama-se **"Referências"** (não
  "Bibliografia"), conforme NBR 6023 / `manual2024` 3.1.4.1.
- **Lista de referências:** espaço simples dentro de cada entrada e **uma linha
  em branco** entre entradas.

---

## Fase 2 — Formatação gráfica (manual2024, cap. 1–3 + NBR 10520:2023)

### Página e espaçamento
- **A4**, fonte base **12 pt**.
- Margens **espelhadas** (documento `twoside`): topo **3 cm**, base **2 cm**,
  interna **3 cm** e externa **2 cm** (via `bindingoffset=1cm`). A parte
  pré-textual sai apenas no anverso (versos em branco).
- Entrelinhas **1,5** no texto; **espaço simples** em citações longas, notas de
  rodapé, referências, legendas, fontes, ficha catalográfica e dados da folha de
  rosto.

### Títulos e numeração
- Formatação por nível (via `titlesec`): **capítulo** em CAIXA ALTA e negrito;
  **seção** em CAIXA ALTA; **subseção** em negrito; **subsubseção** em negrito
  itálico; e uma **subsubsubseção**. Títulos **sem indicativo numérico** (errata,
  agradecimentos, listas, resumo, sumário, referências, glossário, apêndice,
  anexo, índice) ficam **centralizados**.
- **Paginação:** algarismos arábicos a partir da primeira folha textual, no
  **canto superior externo** (direita no anverso, esquerda no verso). A opção de
  classe **`numeraisromanos`** numera a parte pré-textual em romanos.

### Capa e elementos pré-textuais
- **Dois logotipos** na folha de rosto (UFRJ + COPPE).

### Ilustrações, tabelas e quadros
- **Legenda no topo** de figuras, tabelas e quadros (`Figura N – título`, com
  travessão), em corpo menor.
- **Fonte obrigatória embaixo** com `\source{...}` (ou `\fonte{...}`): linha
  "Fonte: …" em corpo menor, espaço simples, sem numeração e sem avançar
  contadores. Em caso de conflito de nome, use `\cpsource` / `\cpfonte`.
- Novo float **`quadro`** (sinônimo em inglês: `frame`), numerado por capítulo,
  com **`\listofquadros`**.
- **`\newcoppefloat{amb}{Nome}{Título da Lista}`** declara outros floats com a
  mesma regra (legenda no topo, `\source` embaixo, `\listof…`).

### Citações e aspas
- `csquotes` carregado; `\enquote{…}` para aspas conforme o idioma, e o sinônimo
  **`\citacao{…}`**.
- Recuo de 4 cm para citações longas (recomendado pela NBR 10520:2023).

### Listas e elementos especiais
- Ambiente **`alineas`** (a) b) c) com subitens em travessão).
- **Siglas:** `\newsigla{chave}{SIGLA}{forma extensa}` e **`\sigla{chave}`** —
  imprime "forma extensa (SIGLA)" na primeira ocorrência (registrando-a
  automaticamente na lista) e só "SIGLA" depois; `\sigla*` força a forma extensa.
  A lista passou a se chamar **"Lista de Abreviaturas e Siglas"**.
- Notas de rodapé em **espaço simples**, **footnotesize**, com **filete de 5 cm**.

### Listagens de código e algoritmos
- Pacote `listings` embutido: ambiente/legenda **"Programa N"** (legenda no topo),
  com acentuação UTF-8 e **`\listofprogramas`**.
- Estilos prontos: `python`, `java`, `xml`, `html`, `prolog`; código em linha
  (`\pythoninline`, `\javainline`), de arquivo externo (`\pythonexternal`,
  `\javaexternal`) e saída de programa (`gxoutput`, `gxoutputs`).
- Algoritmos via `algorithm2e` (idioma seguindo a opção `english`; português por
  padrão), com as palavras-chave `\Para`/`\Enquanto` e **`\listofalgorithms`**.

### Pós-textuais
- **Apêndice / Anexo** identificados como **"APÊNDICE A – Título"** /
  **"ANEXO A – Título"** (letras maiúsculas consecutivas + travessão + título),
  com `\appendix` e `\annex`.

---

## Resumo de novos comandos e opções

| Recurso | Comando / opção |
|---|---|
| Estilo numérico (ordem de citação) | opção de classe `numbers` |
| Frente em romanos | opção de classe `numeraisromanos` |
| Espaço duplo | opção de classe `doublespacing` |
| Citação de citação | `\citetapud`, `\citepapud` |
| Aspas | `\enquote`, `\citacao` |
| Fonte de ilustração | `\source`, `\fonte` (ou `\cpsource`, `\cpfonte`) |
| Quadro | ambiente `quadro` / `frame`, `\listofquadros` |
| Float personalizado | `\newcoppefloat{amb}{Nome}{Título}` |
| Alíneas | ambiente `alineas` |
| Siglas | `\newsigla`, `\sigla`, `\sigla*` |
| Programas | ambientes `python`/`java`/`xml`/`html`/`prolog`, `\listofprogramas` |
| Saída de programa | `gxoutput`, `gxoutputs` |
| Algoritmos | ambiente `algorithm`, `\Para`, `\Enquanto`, `\listofalgorithms` |
| Anexo | `\annex` |

Compatível com **babel** (português e inglês). Veja `example.tex` para um
documento de demonstração que exercita todos os recursos acima.
