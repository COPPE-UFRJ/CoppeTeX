# Roteiro de correção — conformidade com o Manual UFRJ/SiBI 2026

Documento de trabalho **para o Claude** (ou quem retomar), escrito ao fim da
conferência completa de 16/09/2026. Diz como achar e como corrigir cada defeito
aberto, em que ordem, e o que não pode ser esquecido. Não é documentação do
usuário: quando tudo estiver fechado, este arquivo sai do repositório (ou vira
histórico, como o `REVISAO_SIBI.md`).

- **Base:** `master` em `b8103c7` (v4.1). O trabalho vai num **ramo novo**.
- **Norma:** `specs/Manual para elaboração e normalização de trabalhos acadêmicos 2024.pdf`
  (é a 9.ª ed. rev., 2026 — ver `specs/README.md`) e o modelo da folha adicional.
- **Issues:** guarda-chuva **#112**; uma por problema, **#113 a #151**, e
  **#152** (LuaLaTeX, achada ao corrigir #151; teste `r70`).
- **Testes:** `tests/regressivo/r33` a `r69` e `r89` — **todos falham hoje**
  (`38 teste(s), 38 falha(s)`); o apoio `tests/regressivo/medidas.py`; a tabela
  está no `tests/regressivo/README.md`. Cada um traz a marca `ABERTO: #<issue>`,
  e a rodada sem filtro **não** os roda.

---

## 0. Antes de mexer em qualquer coisa

1. **Fonte única.** Classe, estilos BibLaTeX, pacotes de idioma, `max-exemplo.tex`,
   `min-exemplo.tex`, `example_*.tex`, `exemplo.bib`, `manual.bib` e `coppe.bib` saem
   do `src/coppe.dtx` (`coppe.ins`). **Nunca** editar os gerados. Ficam fora do
   `.dtx` e se editam direto: `src/manual.tex`, `src/NORMA_COPPE_2026.tex`,
   `NORMA_COPPE_2026.md`, `tools/*`, `tests/*` (inclusive
   `tests/adversativa/referencias-manual.bib`).
2. **Script de edição com barra invertida vai para arquivo** (`_scratch/*.py` com
   a ferramenta Write). Heredoc do Git Bash e substituição de regex do Python
   comem `\\`. Nesta conferência um `re.sub` transformou `\n` num fim de linha
   dentro de uma string — conferir `python -c "import ast; ..."` depois.
3. **UTF-8** em tudo (nada de `\'a`), sem `\CharacterTable`/`\CheckSum`, sem
   `\paragraph` nos manuais (o max-exemplo tem exatamente um).
4. **Uma issue por problema**, fechada no commit que corrige, com o hash num
   comentário. Problema novo achado no caminho → issue nova.
4a. **A suíte nova roda aos poucos, nunca inteira** (pedido do usuário). Cada
   correção roda **só os testes dela**, pelo nome, e tira a linha
   `ABERTO: #<issue>` do teste **no mesmo commit** do `Fixes #<issue>` — a partir
   daí o teste entra na rodada normal. Rodar a lista inteira dos abertos de uma
   vez não diz nada (falham de propósito) e custa muitos minutos.
5. **Prova em etapas**, com relato entre elas (nunca um bloco de 20 min):
   `tools\build-check.ps1 -Scope class` → `example` → `langs` → `tests` → `docs` →
   `pdfa` → `adversativa`; depois `python tests/regressivo/run-regressivo.py`
   (em lotes), `coppetex.bat --conferir`, `--dist`, `--pacote`.
6. **Versão.** Várias correções mudam a aparência (corpo dos títulos, listas,
   notas). Perguntar ao usuário se sai 4.1 regerada ou 4.2 antes de tocar em
   `tools/versao.py`. Registrar no `CHANGELOG.md` e, onde a API muda, no
   `MIGRATION_v3_to_v4.md`.
7. **PDFs versionados** (`src/*.pdf`, `dist/**/*.pdf`) só se regeram nos marcos,
   pelo painel.

## 1. Como achar cada erro

```powershell
python tests/regressivo/run-regressivo.py r38          # um
python tests/regressivo/run-regressivo.py r33 r34 r35  # alguns
python tests/regressivo/r38-referencias-alinhadas-a-esquerda.py  # direto, com a saída completa
```

Cada teste diz, na falha, o que mediu e onde. Para ver o PDF que ele compilou:
`$env:MANTER_PROVA=1` mantém a pasta temporária e imprime o caminho.

**Provar a correção antes de levá-la ao `.dtx`** (foi assim que as receitas
marcadas "validada" abaixo foram conferidas):

```powershell
# 1. cópia da classe gerada
Copy-Item src\coppe.cls,src\*.bbx,src\*.cbx,src\*.dbx,src\*.lbx,src\coppe.ist,src\*.def _scratch\proto\
Copy-Item -Recurse src\logos _scratch\proto\logos
# 2. acrescentar a correção NO FIM do arquivo gerado da cópia (sobrepõe a definição)
# 3. rodar o teste contra a cópia
$env:COPPE_SRC = "D:\GitHub\CoppeTeX\_scratch\proto"; python tests\regressivo\r38-...py
$env:COPPE_SRC = ""
```

No `.dtx` a correção entra **no lugar** da definição antiga, com o comentário de
documentação no estilo do arquivo (português, explicando o porquê e citando o
item do Manual), e não como remendo no fim.

### Onde fica cada coisa no `coppe.dtx` (linhas em `b8103c7`; procurar pelo texto, que as linhas andam)

| O que | Procurar | Linha | Módulo |
|---|---|---|---|
| título de capítulo | `\titleformat{\chapter}[hang]` | 5229 | class |
| `\appendix` e títulos de apêndice | `\renewcommand\appendix`, `\newcommand\coppe@appendixheadings` | 5248, 5241 | class |
| `\@chapter` (entradas do sumário) | `\def\@chapter[#1]#2` | 5261 | class |
| títulos sem indicativo | `\titleformat{name=\chapter,numberless}` | 5292 | class |
| seção e demais níveis, `\titlespacing` | `\titleformat{\section}`, `\titlespacing*{\paragraph}` | 5300, 5317 | class |
| linha do sumário | `\newcommand\coppe@tocline` | 5401 | class |
| legendas | `\captionsetup{font=footnotesize` | 5460, 6484 | class |
| `\cpsource` | `\newcommand{\cpsource}` | 5493 | class |
| `\newcoppefloat` | `\newcommand{\newcoppefloat}` | 5510 | class |
| nota de rodapé | `\long\def\@footnotetext`, `\renewcommand\footnoterule` | 5522 | class |
| alíneas | `\setlist[alineas,2]` | 5529 | class |
| envoltório de `\@starttoc` | `\newcommand\coppe@wrapstarttoc` | 5568 | class |
| listas pré-textuais no sumário | `\newcommand\coppe@listtoc` | 5606 | class |
| opção `pdfa` | `\DeclareOption{pdfa}` | 5817 | class |
| `listings` e estilos de código | `\lstset{captionpos=t`, `\newcommand\pythonstyle` | 6370, 6410 | class |
| `algorithm2e` | `\SetAlgoCaptionSeparator` | 6493 | class |
| capa | `\newcommand\makecover` | 7165 | class |
| folha de rosto | `\renewcommand\maketitle` | 7199 | class |
| folha de aprovação | `\newcommand\makefrontpage` | 7373 | class |
| folha adicional | `\newcommand\makefolhaadicional` | 7644 | class |
| dedicatória, epígrafe | `\newcommand\dedication`, `\newcommand\epigrafe` | 7703, 7722 | class |
| referência do resumo | `\newcommand\coppe@refresumo` | 7805 | class |
| cabeça das folhas de resumo | `\newcommand\coppe@resumocabeca` | 7893 | class |
| glossário, índice | `\newenvironment{theglossary}`, `\renewenvironment{theindex}` | 8529, 8553 | class |
| cabeçalho da bibliografia | `\defbibheading{bibliography}` | 8908 | class |
| `\annex` | `\newcommand{\annex}` | 9004 | class |
| campos próprios (director…) | `\DeclareDatamodelFields[type=list,datatype=literal]{director}` | 9058 | dbx |
| opções do estilo | `\ExecuteBibliographyOptions{%` | 9085 | bbx |
| caixa alta do sobrenome | `\protected\def\coppe@ucfamily` | 9167 | bbx |
| separador de intervalo de data | `\renewcommand*{\bibdaterangesep}` | 9179 | bbx |
| formato do título | `\DeclareFieldFormat{title}` | 9216 | bbx |
| `In:` | `\renewbibmacro*{in:}` | 9252 | bbx |
| parte de monografia | `\newbibmacro*{coppe:partdriver}` | 9320 | bbx |
| curso e tese | `\DeclareFieldFormat{course}`, `\DeclareBibliographyDriver{thesis}` | 9363, 9369 | bbx |
| mídia | `\newbibmacro*{coppe:media}`, `\newbibmacro*{coppe:mediadriver}` | 9392, 9401 | bbx |
| mapas de fonte (sinônimos) | `\DeclareSourcemap{` | 9638 | bbx |
| citações autor-data | `\RequireCitationStyle{authoryear-comp}` | 9739 | cbx |
| strings pt/en/es/fr/it | `\DeclareBibliographyStrings{%` | 9773, 9802, 9828, 9854 | lbxbr, lbxen, lbxes, lbxfr |
| estilo numérico | `\RequireBibliographyStyle{coppe}`, `\RequireCitationStyle{numeric-comp}` | 10147, 10183 | numbbx, numcbx |
| `m-diss` | `@thesis{m-diss,` | 10915 | tiposbib |
| `manualbib` | `@manual{manualbib,` | 10413 | examplebib |
| listas do max-exemplo | `\listoftables` | 3551 | maxexemplo |
| palavras-chave do max-exemplo / min-exemplo | `\keyword{Primeira palavra-chave}` | 3456, 4870 | maxexemplo, minexemplo |
| algoritmos do max-exemplo | `\begin{algorithm}[H]` | 4408, 4422 | maxexemplo |
| agências do max-exemplo | `\fundingagency{Conselho Nacional` | 3471 | maxexemplo |
| capítulo em inglês | `\chapter{Using BibLaTeX}` | 4140 | maxexemplo |

Fora do `.dtx`: `tools/painel.py` `def acao_conferir` (l. 228); `tools/build-check.ps1`
escopo `prova` (l. 250 e 551) e `conferir-manual` (l. 333); `tools/geradocvazio.py`
campo `pdfa` (l. 165), `LISTAS` (l. 238), palavras-chave (l. 353);
`NORMA_COPPE_2026.md` §2 (l. 81), §10 (l. 215), §12 (l. 233), §14 (l. 261), e a
mesma coisa em `src/NORMA_COPPE_2026.tex`; `tests/adversativa/referencias-manual.bib`
pt-4231 e pt-diss (as chaves eram `m-` até a #147).

---

## 2. Ordem de trabalho

A ordem importa por três razões: decisões mudam o que se implementa; o
ferramental tem de pegar regressão **antes** das mudanças grandes; e algumas
correções mexem no mesmo código.

| Fase | Issues | Por quê |
|---|---|---|
| **0. Decisões** (perguntar ao usuário, registrar na issue) | #128 idioma das folhas de identidade · #129 "(COPPE)" na capa · #130 logotipos na folha de rosto · #150 travessão ou meia-risca · #124 `pdfa` por padrão · versão 4.1 ou 4.2 · confirmar #113 (muda a aparência) | O que se implementa em #116, #119, #128–#130 depende disto |
| **1. Rede de segurança** | #151 (prova roda `conferir-norma` e `conferir-referencias`) · #147 (m-diss) · #152 (LuaLaTeX com T1) | A partir daqui a prova acusa regressão de referência e de leiaute; #147 e #152 são as duas divergências que o #151 passou a acusar |
| **2. Títulos** | #113 corpo 12 · #122 espaço depois do título | Mesmo bloco de `\titleformat`/`\titlespacing`; conferir `r04`, `r95`, `r22` |
| **3. Sumário e listas** | #115 coluna dos pós-textuais · #116 nome e traço nas listas · #148 ordem das listas | Mesmo envoltório `\coppe@wrapstarttoc`; #116 usa o traço de #150 |
| **4. Pré-textuais** | #114 título do resumo · #119 referência do resumo · #123 dedicatória e epígrafe · #128 · #129 · #130 | #119 depois de #150 e de #131 (forma do título:subtítulo) |
| **5. Corpo** | #117 notas · #120 listagens · #121 subalíneas | Independentes |
| **6. Referências** | #118 alinhamento → #131 subtítulo → #134 parte de monografia → #133 livro e relatório → #137 tese → #132 itálicos → #135 tradutor → #136 DOI → #143 mídia → #141 ordenação → #142 data aberta → #145 hífen → #146 mês | #134 depende da macro de título de #131; #133 e #134 reescrevem drivers |
| **7. Citações** | #138 entrada pelo título · #139 mesmo sobrenome · #140 numérico · #144 entidade | #138 e #144 mexem no rótulo da chamada |
| **8. Exemplos** | #149 conteúdo · #147 (se não saiu na fase 1) | Depois das correções de estilo, para o max-exemplo mostrar o resultado certo |
| **9. Opções e extensões** | #124 `pdfa` padrão · #125 `\illustrationwidth` · #126 `\volumefiles` · #127 letras dobradas | API nova: manual, quickref, `conferir-manual.py` (todo comando público documentado), MIGRATION |
| **10. Fechamento** | #112 | Prova completa em etapas; conferência visual do max-exemplo; CHANGELOG, TODO, `REVISAO_SIBI.md` declarado histórico; `dist/`; fechar #112 |

---

## 3. Receita por issue

Legenda: **validada** = a receita foi acrescentada a uma cópia da classe gerada
e o teste passou (Apêndice A tem o código exato usado). **Proposta** = não foi
prototipada; conferir com cuidado.

### #113 — títulos em corpo 12 · `r33` · FEITA
- `\Large`→`\normalsize` em `\titleformat{\chapter}`, `name=\chapter,numberless`,
  `\coppe@appendixheadings`; `\large`→`\normalsize` em `\titleformat{\section}`;
  `\large\bfseries`→`\bfseries` nos dois títulos de `\makefolhaadicional`.
- Provado: `r33`; `r04`, `r05`, `r20`, `r22`, `r95`, `r99` pelo nome; o
  max-exemplo compilado num rascunho.

### #122 — uma linha em branco antes e depois dos títulos · `r42` · FEITA
- `\titlespacing*{\section}{0pt}{\baselineskip}{\baselineskip}` e o mesmo para
  `\subsection`, `\subsubsection`, `\paragraph` (este tinha `2.5ex…/1.5ex…`). O
  capítulo já tinha `1.5\baselineskip` depois.
- **Armadilha:** nada de elástico (`\baselineskip plus .2\baselineskip`). O
  titlesec passa o valor ao `\setlength` do `calc`, que não aceita `plus` depois
  de registro: "Missing number", "plus .2" impresso na folha, e o espaço depois
  do título menor que uma entrelinha. E o `r42` falhou só pela medida, porque o
  `Documento.ok` do `medidas.py` olhava só se o PDF existia — agora exige também
  nenhuma linha `!` no `.log`.

### #115 — pós-textuais na coluna do sumário · `r35` · validada
- `\protect\numberline{}` antes do título nas entradas: `\@chapter` (ramos de
  apêndice e anexo, antes de `\protect\coppe@tocapp`/`\coppe@tocanx`),
  `\defbibheading{bibliography}`, `theindex`, `theglossary` e `\coppe@listtoc`.
- O `\coppe@tocnumberline` mede a largura do número; com `{}` vazio não altera a
  coluna. Rodar `r04`, `r95` (estabilidade do `.aux`), `r98` (listasnosumario).

### #116 — nome específico e traço nas listas · `r36` · validada
- No `\coppe@wrapstarttoc`: se a extensão não é `toc` e existe
  `\coppe@listname@<ext>`, `\let\numberline\coppe@listnumberline`, que escreve
  `\coppe@listname\nobreakspace#1\nobreakspace<traço>\space`.
- Tabela de nomes: `lof`→`\figurename`, `lot`→`\tablename`, `loq`→`\quadroname`,
  `lol`→`\lstlistingname`, `loa`→`\algorithmcfname`; `\newcoppefloat{nome}{Nome}{…}`
  define `\coppe@listname@lonome` = `Nome`.
- `\l@figure`, `\l@table`, `\l@quadro`, `\l@lstlisting`, `\l@algocf` e o
  `\l@<float>` do `\newcoppefloat` → `\@dottedtocline{1}{0pt}{0pt}` (no
  `\AtBeginDocument`, porque `listings` e `algorithm2e` definem os seus depois).
- O traço é o decidido em #150 (hoje as legendas usam `\textendash`).
- Rodar `r01`, `r08`, `r09`.

### #148 — ordem das listas · `r67` · proposta
- `max-exemplo` (módulo `maxexemplo`): mover `\listoftables` para depois de
  `\listofalgorithms`; o comentário que explica as listas também.
- `src/manual.tex` l. 124–128 e `tools/geradocvazio.py` `LISTAS`: a mesma ordem.
- Norma §10 (`.md` e `.tex`): "entre a Lista de Figuras e a Lista de Tabelas" —
  ou reescrever sem posição e dizer que seguem a 3.1.2.
- Conferir a tabela de listas da documentação (`coppe.dtx` l. ~1716) e do quickref.

### #114 — título RESUMO/ABSTRACT · `r34` · validada
- No começo de `\coppe@resumocabeca`: `\begin{center}\bfseries\MakeUppercase{\@nameuse{coppe@str@\coppe@reslang @abstractname}}\end{center}` e um respiro.
- O título **não** fica sob `\configuraresumos` (é o único obrigatório).
- Conferir que `r27` e `r28` passam, e que as três folhas do espanhol (resumen,
  abstract, resumo) ganham o título no idioma de cada uma (`r25`, `r23`).
- Documentar no `.dtx` e no `manual.tex` (seção do resumo).

### #119 — referência do resumo · `r39` · validada
- `\coppe@refresumo`: `\raggedright`; `\textbf{\coppe@selecttitle}` e o subtítulo
  fora do negrito, depois de `: `; `\textemdash` (ou o traço de #150) antes de
  `\local@instname`.
- Decidir com #150. Considerar compor a referência com a mesma forma do driver
  `thesis` (discussão na issue) — se mudar, atualizar `r15` e Norma COPPE §8.

### #123 — dedicatória e epígrafe · `r43` · validada
- `\dedication` e `\epigrafe`: minipage de `0.5\textwidth` com `\raggedright`
  (texto começa no meio da mancha); autoria da epígrafe `\raggedleft\small`.

### #117 — notas de rodapé · `r37` · validada
```latex
\renewcommand\@makefntext[1]{%
  \setbox\@tempboxa\hbox{\@makefnmark}%
  \noindent\hangindent\wd\@tempboxa\hangafter\@ne
  \box\@tempboxa #1}
\interfootnotelinepenalty=\@M
```
- Nota com mais de um parágrafo: o segundo parágrafo perde o recuo; tratar no
  `\@footnotetext` da classe (`\parindent` = largura da marca, ou `\everypar`).
- Conferir `\footfullcite` (referência em nota, 4.2) e a folha 23 do max-exemplo.

### #120 — listagens dentro da margem · `r40` · validada
- `xleftmargin=2em` nos cinco estilos (`\pythonstyle`, `\javastyle`, `\xmlstyle`,
  `\htmlstyle`, `\prologstyle`) — ou uma vez no `\lstset` global, conferindo que
  `lstlisting` sem números não fica recuado demais.
- `\theFancyVerbLine` (Verbatim numerado): `xleftmargin` no `\fvset`.

### #121 — subalíneas · `r41` · validada
```latex
\newlength\coppe@hifen
\settowidth\coppe@hifen{-}
\setlist[alineas,2]{label=-,labelindent=0pt,labelwidth=\coppe@hifen,
  labelsep=0.333em,leftmargin=!,align=left,itemsep=0pt}
```
- **Armadilha já vista:** `labelwidth=*` com `labelsep=0.5em` põe o hífen no lugar
  certo mas abre um vão de 22 pt até o texto — a primeira versão do protótipo
  passava no teste por isso, e o `r41` ganhou a cobrança do vão (até 7 pt).
- No `.dtx`, medir o hífen na fonte do texto (a `\settowidth` no carregamento da
  classe mede na fonte daquele momento); `\widthof{-}` avaliado no início da
  lista é mais seguro, se o `calc` estiver carregado.
- Sugestão sem teste: letras do primeiro nível reentradas (hoje 0,18 cm).

### #118 — lista de referências à esquerda · `r38` · validada
- `\AtBeginBibliography{\raggedright \hyphenpenalty=\@M \exhyphenpenalty=\@M}` no
  `coppe.bbx` (o biblatex lê o `.bbx` com `@` como letra; no protótipo funcionou).
- Conferir URLs longas (quebram pelo `url`), e as folhas 57–61 do max-exemplo.

### #131 — subtítulo · `r50` · validada para `title`
```latex
\renewcommand*{\subtitlepunct}{\addcolon\space}
\DeclareFieldFormat{subtitlecase}{#1}
\renewbibmacro*{title}{%
  \ifboolexpr{ test {\iffieldundef{title}} and test {\iffieldundef{subtitle}} }
    {}
    {\printtext[title]{\printfield[titlecase]{title}}%
     \setunit{\subtitlepunct}%
     \printfield[subtitlecase]{subtitle}%
     \newunit}%
  \printfield{titleaddon}}
```
- Fazer o mesmo nas macros `booktitle`, `maintitle`, `journal` (padrão do
  biblatex) — copiar a definição de `standard.bbx` e separar o negrito do título.
- Conferir `conferir-referencias.py` inteiro (gabarito de 34 categorias) depois.

### #134 — parte de monografia · `r53` · proposta
- `coppe:partdriver`: depois de `in:`, `bookauthor` (`\printnames{bookauthor}` com
  o formato de autor) **ou** `coppe:bookeditor`; título do livro pela macro de
  título com `booktitle`/`booksubtitle` (de #131); imprenta; `\newunit`;
  `\printfield{chapter}` com formato `cap.~#1`; `\setunit{\addcomma\space}`;
  `\printfield{pages}`.
- `inbook` usa o mesmo driver; conferir m-4213 e o COWIN/EDWARDS do max-exemplo.

### #133 — livro e relatório · `r52` · proposta
- `\DeclareFieldFormat{edition}{\ifinteger{#1}{#1\adddot\addnbspace\bibstring{edition}}{#1}}`
  (a bibstring `edition` no pt deve ser "ed.").
- `volumes` no `brazilian-coppe.lbx`: `{v\adddot}` longo e curto.
- Drivers `book` e `report` próprios: autor. título. edição. local: editora,
  data. `pagetotal` ou `volumes`. `(série, número)` — com `\mkbibparens` e
  `\addcomma`. nota. DOI. URL.
- Conferir "BAUMAN… 2. ed. rev." (edição literal) e SOUSA/manualbib.

### #137 — tese e dissertação · `r56` · proposta
- `\DeclareFieldFormat{type}`: `mathesis`→"Dissertação", `phdthesis`→"Tese" (forma
  longa: `\biblstring`), e os tipos próprios como hoje.
- Grau: `mathesis`→"Mestrado", `phdthesis`→"Doutorado" (estender `\coppe@degword`).
- `course` + grau: "(Grau em Curso)"; sem curso: "(Grau)"; sem grau conhecido e
  com curso: "(Curso)" — nunca "( em".
- Travessão com `\setunit{…\textemdash…}` (não `\setunit*`) sempre que houver
  `type` e `institution`.
- `pages` do JabRef (`pages = {157}` em tese) → tratar como `pagetotal`? Discutir
  na issue; hoje não sai.

### #132 — expressões latinas · `r51` · validada
- `\renewbibmacro*{in:}{\printtext{\mkbibemph{\bibstring{in}}\addcolon\space}}`
- `andothers = {{\mkbibemph{et al\adddot}}{\mkbibemph{et al\adddot}}}` nos `.lbx`
  (pt, en, es; fr e it por coerência).
- `\DeclareStyleSourcemap` (não `\DeclareSourcemap`) trocando `[S. l.]`,
  `[s. n.]`, `[S. l.: s. n.]` por `[\emph{S. l.}]` etc. em `location`/`publisher`.

### #135 — tradutor · `r54` · proposta
- `\DeclareNameAlias{translator}{given-family}` e, no bloco da bibliografia, o
  tradutor fora do `\mkbibnamefamily` em caixa alta (como já se faz com
  `holder` em `coppe:depositor`).
- bibstring `bytranslator` = "Tradução de" (pt).
- `origtitle` → nota "Tradução de: …" no fim, antes de DOI/URL.

### #136 — DOI · `r55` · proposta
- `\DeclareFieldFormat{doi}{DOI\addcolon\space\url{https://doi.org/#1}}`, com teste
  para valor que já começa por `http`.
- O aviso `T1/lmss/m/sc` deve sumir do log do max-exemplo também.

### #143 — mídia · `r62` · proposta
- `coppe.dbx`: `director` e `producer` como `type=list,datatype=name`.
- `coppe:media`: `\printnames` em ordem direta, sem caixa alta, com "Direção:" e
  "Produção:" (strings nos `.lbx`).
- `coppe:mediadriver`: `version` antes da imprenta (lugar da edição).
- Conferir filme-example e videogame-example do max-exemplo.

### #141 — ordenação sem artigo · `r60` · validada
```latex
\DeclareStyleSourcemap{\maps[datatype=bibtex]{%
  \map{\step[fieldsource=title,
             match=\regexp{\A(O|A|Os|As|Um|Uma|Uns|Umas|The|An|El|La|Los|Las)\s+(.+)\Z},
             final]
       \step[fieldset=sorttitle, fieldvalue={$2}]}}}
```
- Conferir se um `\DeclareSourcemap` no preâmbulo do aluno apaga o da classe; se
  apagar, migrar os sinônimos em português para `\DeclareStyleSourcemap` também.

### #142 — periódico corrente · `r61` · validada
- `\renewcommand*{\bibdaterangesep}{\iffieldequalstr{endyear}{}{\mbox{-}\space}{/}}`
- Tirar os `%%!` de pt-4231 em `tests/adversativa/referencias-manual.bib` e de
  m-4231 no módulo `tiposbib` (a mesma nota está nos dois).
- Conferir a CHAMADA com data aberta e letra de desempate: desde que os
  adversativos em português citam `m-4231` e `pt-4231` juntos, o autor-data
  (`adv_msc_pt`) compõe "(São Paulo Medical Journal 1941a/a; ... 1941b/b)". A
  letra vai no ano inicial, e não também depois da barra.

### #145 — hífen no intervalo · `r64` · validada
- `\renewcommand*{\bibrangedash}{-}` no `\AtBeginBibliography`; nas chamadas,
  `\DeclareFieldFormat{postnote}` já usa `\mkpageprefix` — conferir "p. 10-20".

### #146 — mês no idioma da publicação · `r65` · proposta
- Em `\coppe@abntdate`, trocar `\mkbibmonth` por uma macro que olha
  `\thefield{langid}` e usa tabelas próprias (NBR 6023, Anexo A) para pt, en, es,
  fr, it. **Não** ligar `autolang` (mudaria "Disponível em"/"Acesso em").

### #138 — chamada pela entrada de título · `r57` · proposta
- `\DeclareFieldFormat{citetitle}{#1}`; `\DeclareDelimFormat{nonameyeardelim}{\addcomma\space}`.
- `\DeclareStyleSourcemap`: sem `author` e sem `editor` (`\step[notfield=author,final]`
  e o mesmo para `editor`), `shorttitle` = palavra de entrada (artigo + palavra).
- Confirmar na NBR 10520:2023 a forma de título com várias palavras antes de fixar.

### #139 — mesmo sobrenome e ano · `r58` · validada
```latex
\ExecuteBibliographyOptions{uniquename=minyearfull}
\DeclareNameFormat{labelname}{%
  \nameparts{#1}%
  \usebibmacro{name:family}{\namepartfamily}{\namepartgiven}{\namepartprefix}{\namepartsuffix}%
  \ifcase\value{uniquename}%
  \or\addcomma\space\namepartgiveni
  \or\addcomma\space\namepartgiven
  \fi
  \usebibmacro{name:andothers}}
```
- No `coppe.cbx` (o `authoryear-comp` liga `uniquename` depois do `.bbx`).

### #140 — sistema numérico · `r59` · validada
- `coppe-numeric.cbx`: `\DeclareCiteCommand{\cite}[\mkbibparens]{…}` e
  `\DeclareCiteCommand{\parencite}[\mkbibparens]{…}` copiando o `numeric-comp`
  (Apêndice A).
- `coppe-numeric.bbx`: `\DeclareFieldFormat{labelnumberwidth}{#1}` (e
  `shorthandwidth`).
- Classe, com `numbers`: aviso **uma vez** no primeiro `\footnote` citando a
  4.1.1.1.1 (o protótipo avisa a cada nota — melhorar com um `\if`).
- Documentar `\supercite` como a forma sobrescrita.

### #144 — chamada de entidade hierárquica · `r63` · proposta
- Rótulo da chamada: se o nome tem ". ", só o segmento antes do primeiro ". ",
  convertido de CAIXA ALTA para caixa de título (partículas de, da, do, das, dos,
  e em minúscula); `shortauthor` do autor vence sempre.
- **Não** mudar a regra da lista (comentário junto de `\coppe@ucfamily`: nome com
  ponto sai como foi digitado). **Decisão do usuário (16/09/2026):** BRASIL e
  nomes de país como autor saem sempre em caixa alta nas referências, e isso é
  responsabilidade de quem escreve o `.bib` — a classe não converte. Vale para
  jurisdição e entidade superior em geral ("RIO DE JANEIRO (Estado).",
  "UNIVERSIDADE FEDERAL DO RIO DE JANEIRO."). Consequências:
  - documentar isso para o aluno no manual (`coppe.dtx`, seção de referências;
    `src/manual.tex`; quickref), com exemplo de `.bib`;
  - o `exemplo.bib` tem de dar o exemplo certo (#149: `{Brasil. Supremo Tribunal
    Federal}` → `{BRASIL. Supremo Tribunal Federal}`; o `r68` cobra);
  - a chamada é outra história (esta issue): com o `.bib` digitado em caixa alta,
    ela precisa sair "(Brasil, 1995)" — ou a classe converte o primeiro segmento,
    ou a documentação ensina `shortauthor = {Brasil}`. Decidir na issue antes de
    implementar; o `r63` cobra o resultado, não o caminho.

### #147 — m-diss · `r66` · FEITA
- Módulo `tiposbib`: `type = {mscdiss}`, `course = {Memória Social e Documento}`.
  O defeito vinha de `b14a5d6`, quando a base ganhou a forma em inglês.
- A colisão de chaves era pior do que parecia: o biber achava todas as citações
  no `exemplo.bib` e **nem abria** o `referencias-manual.bib` (o `.blg` não o
  menciona), e as 34 entradas com os sinônimos em português nunca eram compostas.
  Agora são `m-<item>` no `exemplo.bib` e `pt-<item>` no `referencias-manual.bib`;
  o `mk-adversativa.py` cita as duas.
- `conferir-referencias.py` lê o gabarito das duas bases (o bloco `%%` colado à
  chave) e liga cada `[n]` à chave pelo `.bbl`, em vez de casar pelo começo do
  texto. `adv_dscexam_pt`: 68 gabaritos, 0 divergências, 6 aceitas (as mesmas
  três em cada forma).
- Os comentários do `exemplo.bib` diziam "metade das entradas em português" —
  não há nenhuma desde a conversão —, e o manual repetia isso. Corrigidos.

### #149 — conteúdo dos exemplos · `r68` · proposta
- Checklist na issue. Palavras-chave em minúscula no max-exemplo, min-exemplo,
  `example_pt` e gerador (em inglês continuam com inicial maiúscula, como no
  Anexo F). `\source` depois dos dois algoritmos. Acentos nas agências.
  Renomear "Using BibLaTeX" e "exemplo úteis". Tirar as duplicatas (ou deixar só
  uma no `\nocite`). `manualbib` → 9. ed. rev., 2026. `BRASIL.` em caixa alta na
  jurisprudência — país e jurisdição como autor são digitados em caixa alta por
  quem escreve o `.bib` (decisão de 16/09/2026, ver #144), e o exemplo tem de
  mostrar isso. "Algoritmo 6.1". Lista de abreviaturas sem as entradas de teste.
  `\LaTeX` em título: usar `\texorpdfstring` ou evitar o logotipo em caixa alta.
  Espaço engolido depois dos logotipos no texto do max-exemplo ("COPPETEXcom",
  "LATEXpor", visto na folha 22 ao conferir #113): `\CoppeTeX{}`, `\LaTeX{}`.

### #151 — a prova roda os verificadores · `r89` · FEITA
- Os dois verificadores, sem argumento, sabem o que conferir (a lista mora
  neles): `conferir-norma.py` → `src/max-exemplo.pdf`, `src/min-exemplo.pdf` e
  todo `adv_*.pdf`; `conferir-referencias.py` → os `adv_*` com `numbers` e
  `referencias-manual.bib` (hoje só o `adv_dscexam_pt`), nos dois motores.
- `painel.py --conferir` chama os dois sem argumento; `build-check.ps1` chama o
  `conferir-norma` logo depois do escopo `example` e os dois depois do
  `adversativa` (e portanto no `all` e na `prova`), com as linhas acusadas no
  `RESULTADO.txt`.
- Uma chamada do `pdftotext` por documento, e não por folha: os mesmos 7 PDFs
  levavam 174 s e levam 18 s; os 14 (dois exemplos, doze adversativos) mais o
  gabarito, 40 s.
- Ligados, acusaram duas coisas: m-diss (#147) e o `nž` do LuaLaTeX (#152). A
  prova só sai limpa depois das duas.
- Continua aberta a discussão: estender `conferir-norma.py` com as medidas de
  r33–r43, ou confiar na suíte de regressão.

### #152 — LuaLaTeX com `fontenc` T1 · `r70` · FEITA
- `fontenc` T1 só dentro de `\ifPDFTeX`; nos motores Unicode fica a TU do kernel,
  com a Latin Modern em OpenType (os `tulm*.fd` vêm no LaTeX base).
- As formas que a classe declara para calar substituição (`lmss` it/b/sbc,
  `lmtt` bx/b-it) ganharam a versão TU, com `\UnicodeFontFile`; a pré-carga dos
  `.fd` usa `\encodingdefault`.
- `\ttb`/`\ttm` (estilos de linguagem das listagens) eram `T1/txtt` fixas: no
  LuaLaTeX passaram a `TU/lmtt`, porque a txtt não existe em OpenType.
- Provado: `r70`, `r14`, `r30` pelo nome; sonda com `\emph`, negrito itálico,
  `\texttt` em negrito, semicondensado, logotipo e `\pythonstyle` nos dois
  motores, sem mensagem de forma nem "Missing character";
  `adv_dscexam_pt_lua`: 0 divergências no `conferir-referencias` (eram 5) e
  PDF/A-2b pelo veraPDF.

### #124 — `pdfa` por padrão · `r44` · proposta (decisão na fase 0)
- `\@coppepdfatrue` por padrão, `\DeclareOption{sempdfa}{\@coppepdfafalse}`, manter
  `pdfa` como sinônimo inócuo. Gerador: campo `True` e dica reescrita. Quickref,
  manual, MIGRATION. Conferir `r13`, `r14`, `r98` (casos com e sem `pdfa`).
- O `test_pdfa`/`test_comserifa` da primeira camada e o escopo `pdfa` do build-check.

### #125 — `\illustrationwidth` · `r45` · proposta
- `\newcommand\illustrationwidth[1]{\captionsetup{width=#1}\def\coppe@ilwidth{#1}}`
  e `\let\largurailustracao\illustrationwidth`; `\cpsource` compõe num
  `\parbox{\coppe@ilwidth}` centralizado quando definido (local ao flutuante).
- `conferir-manual.py` cobra documentação do comando novo.

### #126 — `\volumefiles` · `r46` · proposta
- Ler do `.aux` do volume anterior a última folha (o `lastpage` já está lá) e
  fazer `\setcounter{page}` na primeira folha contada; ler os `.toc` dos outros
  volumes dentro do `\tableofcontents`, com uma linha "Volume n" entre eles.
- Ordem de compilação e o caso de um volume ainda não compilado (aviso, não erro).

### #127 — letras dobradas · `r47` · proposta
- Contador `\coppe@Alph`: 1–26 → A–Z; 27 → AA, 28 → AB… (e `\coppe@alph`).
  `\thechapter` no `\appendix`/`\annex`; `\AddEnumerateCounter` no enumitem para o
  rótulo das alíneas. Conferir `\theHchapter` e os bookmarks.

### #128, #129, #130, #150 — decisões
- Implementar só depois da resposta registrada na issue. `r48`, `r49`, `r69` já
  são neutros quanto à decisão. `r19` muda se #128 for "tudo em português".
- #130 não tem teste: se sair o logotipo da folha de rosto, criar `r71` (o `r70`
  ficou com o #152). Os
  logotipos são PDF vetorial incluído (XObject de formulário), que o
  `pdfimages` não lista: medir tinta na faixa de 3 a 5,5 cm do topo da folha 2
  com `pdftoppm -gray` (como o `tinta_folio` do `conferir-norma.py`), ou procurar
  o XObject na folha.

---

## 4. Não são erros (não reabrir)

- Rótulo "Palavras-chave:" em negrito (o Anexo E não tem, mas a 3.1.2.1.4 não
  fixa estilo).
- Título da folha de aprovação em caixa normal (o Anexo D é modelo, não regra).
- Legenda do algoritmo dentro dos filetes do `algorithm2e` (já tem palavra,
  número, traço e título no topo — #70).
- `\cite` sem parênteses no autor-data (convenção do biblatex; documentado: usar
  `\citep`/`\parencite`).
- Numeração de ilustrações por capítulo ("Figura 4.1"): é sequencial em arábicos.
- Frase "Resumo da Tese apresentada…" (Norma COPPE §6–8) — continua, só ganha
  um título acima (#114).

## 5. O que já foi conferido e está conforme

A4; margens 3/3/2/2 (texto de 3,00 a 19,00 cm; topo 3,02 cm); espaço 1,5 (17,9 pt);
corpo 12 no texto e 10 no fólio, notas, legendas e citação longa; citação longa
com recuo de 4 cm e espaço simples; filete de 5 cm; fólio a 2,015 cm do topo e
2,024 cm da direita, contagem a partir da folha de rosto, capa e folha adicional
fora; pré-textuais sem fólio; capa (instituição em três linhas, autor, título:
subtítulo, volume, local, ano); folha de rosto (natureza em espaço simples do meio
à direita, área de concentração, linha de pesquisa, orientação à esquerda, local e
ano); folha adicional com os campos do Anexo H; folha de aprovação (natureza, data,
banca com orientador primeiro e titulação e instituição); palavras-chave nos
resumos; dedicatória e epígrafe na metade inferior; listas de símbolos na ordem
de aparição e de abreviaturas e siglas separadas e alfabéticas; sumário sem ponto
final, indicativos na margem, títulos numerados numa coluna, destaque de cada
nível igual ao do corpo; legenda em cima com número e traço, fonte embaixo; tabela
aberta nas laterais e quadro fechado; tabela longa com "continua"/"continuação";
equação numerada à direita entre parênteses; cinco níveis com destaque gradativo;
indicativo sem ponto; título de várias linhas alinhado sob a primeira letra;
apêndice e anexo centralizados com letra, traço e título; glossário alfabético;
índice; siglas por extenso na primeira ocorrência; idiomas pt/en/es; e o
gabarito de 34 categorias de referência (fora o que está nas issues). Os
exemplos em inglês e espanhol têm a mesma estrutura.

---

## Apêndice A — protótipo usado para validar

Acrescentado ao fim das cópias geradas (`coppe.cls`, `coppe.bbx`, `coppe.cbx`,
`coppe-numeric.cbx`, `coppe-numeric.bbx`) numa pasta de rascunho. **Não copiar
assim para o `.dtx`**: cada trecho vai para o lugar da definição que substitui.
Com ele, passaram r33–r43, r50, r51, r58–r61 e r64; os demais testes continuaram
falhando, como deviam.

### A.1 `coppe.cls`

```latex
%% r33: titulos em corpo 12
\titleformat{\chapter}[hang]
  {\normalfont\normalsize\bfseries}
  {\if@coppeappendix\MakeUppercase{\appendixname}\ \thechapter\ \textendash\else\thechapter\fi}
  {1ex}{\MakeUppercase}
\titleformat{name=\chapter,numberless}[hang]
  {\normalfont\normalsize\bfseries\filcenter}{}{0pt}{\MakeUppercase}
\titleformat{\section}
  {\normalfont\normalsize}{\thesection}{1ex}{\MakeUppercase}
\renewcommand\coppe@appendixheadings{%
  \titleformat{\chapter}[block]
    {\normalfont\normalsize\bfseries\filcenter}
    {\MakeUppercase{\appendixname}\ \thechapter\ \textendash}
    {1ex}{\MakeUppercase}%
  \titlespacing*{\chapter}{0pt}{10pt}{1.5\baselineskip}}
\patchcmd{\makefolhaadicional}{\large\bfseries}{\bfseries}{}{}
\patchcmd{\makefolhaadicional}{\large\bfseries}{\bfseries}{}{}

%% r42: uma linha em branco antes e depois dos titulos
\titlespacing*{\section}{0pt}{\baselineskip}{\baselineskip}
\titlespacing*{\subsection}{0pt}{\baselineskip}{\baselineskip}
\titlespacing*{\subsubsection}{0pt}{\baselineskip}{\baselineskip}
\titlespacing*{\paragraph}{0pt}{\baselineskip}{\baselineskip}

%% r34: titulo centralizado nas folhas de resumo
\pretocmd{\coppe@resumocabeca}{%
  \begin{center}\bfseries
    \MakeUppercase{\@nameuse{coppe@str@\coppe@reslang @abstractname}}%
  \end{center}\par\vspace*{6mm}}{}{}

%% r35: pos-textuais na coluna dos titulos do sumario
\def\@chapter[#1]#2{%
  \ifnum \c@secnumdepth >\m@ne
    \if@mainmatter
      \refstepcounter{chapter}%
      \typeout{\@chapapp\space\thechapter.}%
      \if@coppeappendix
        \if@coppeannex
          \addcontentsline{toc}{chapter}{\protect\numberline{}\protect\coppe@tocanx{\thechapter}#1}%
        \else
          \addcontentsline{toc}{chapter}{\protect\numberline{}\protect\coppe@tocapp{\thechapter}#1}%
        \fi
      \else
        \addcontentsline{toc}{chapter}{\protect\numberline{\thechapter}#1}%
      \fi
    \else
      \addcontentsline{toc}{chapter}{#1}%
    \fi
  \else
    \addcontentsline{toc}{chapter}{#1}%
  \fi
  \chaptermark{#1}%
  \addtocontents{lof}{\protect\addvspace{10\p@}}%
  \addtocontents{lot}{\protect\addvspace{10\p@}}%
  \if@twocolumn
    \@topnewpage[\@makechapterhead{#2}]%
  \else
    \@makechapterhead{#2}%
    \@afterheading
  \fi}
\defbibheading{bibliography}{%
  \chapter*{\coppestring{references}}%
  \addcontentsline{toc}{chapter}{\protect\numberline{}\coppestring{references}}}
\patchcmd{\theindex}{\addcontentsline{toc}{chapter}{\indexname}}
  {\addcontentsline{toc}{chapter}{\protect\numberline{}\indexname}}{}{}
\patchcmd{\theglossary}{\addcontentsline{toc}{chapter}{\glossaryname}}
  {\addcontentsline{toc}{chapter}{\protect\numberline{}\glossaryname}}{}{}

%% r36: nome especifico e traco nas listas de ilustracoes e de tabelas
\newcommand\coppe@listnumberline[1]{\coppe@listname\nobreakspace#1\nobreakspace\textendash\space}
\def\coppe@listname@lof{\figurename}
\def\coppe@listname@lot{\tablename}
\def\coppe@listname@loq{\quadroname}
\def\coppe@listname@lol{\lstlistingname}
\def\coppe@listname@loa{\algorithmcfname}
\renewcommand\coppe@wrapstarttoc{%
  \let\coppe@orig@starttoc\@starttoc
  \def\@starttoc##1{%
    \coppe@checkwrites{##1}%
    \begingroup
      \def\coppe@@ext{##1}\def\coppe@@toc{toc}%
      \ifx\coppe@@ext\coppe@@toc \let\numberline\coppe@tocnumberline
      \else
        \@ifundefined{coppe@listname@##1}{}{%
          \expandafter\let\expandafter\coppe@listname\csname coppe@listname@##1\endcsname
          \let\numberline\coppe@listnumberline}%
      \fi
      \coppe@orig@starttoc{##1}%
    \endgroup}}
\AtBeginDocument{%
  \renewcommand*\l@figure{\@dottedtocline{1}{0pt}{0pt}}%
  \let\l@table\l@figure
  \let\l@quadro\l@figure
  \let\l@lstlisting\l@figure
  \let\l@algocf\l@figure}
\let\coppe@orig@newcoppefloat\newcoppefloat
\renewcommand{\newcoppefloat}[3]{%
  \coppe@orig@newcoppefloat{#1}{#2}{#3}%
  \expandafter\def\csname coppe@listname@lo#1\endcsname{#2}%
  \AtBeginDocument{\expandafter\let\csname l@#1\endcsname\l@figure}}

%% r37: nota de rodape alinhada e sem quebrar entre folhas
\renewcommand\@makefntext[1]{%
  \setbox\@tempboxa\hbox{\@makefnmark}%
  \noindent\hangindent\wd\@tempboxa\hangafter\@ne
  \box\@tempboxa #1}
\interfootnotelinepenalty=\@M

%% r39: referencia do resumo
\renewcommand\coppe@refresumo{%
  \if@copperefresumo
    \if@coppeexame\else
      {\singlespacing\noindent\raggedright
        \nohyphens{%
          \MakeUppercase{\@authsurn}, \@authname.
          \textbf{\coppe@selecttitle}%
          \@ifundefined{coppe@subtitle@\coppe@mainlang}{}{%
            : \coppe@selectsubtitle}.
          \local@cityname, \coppe@docyear.
          \local@doctype\ (\@degreename\ em \local@deptname)\ \textemdash\
          \local@instname, \local@universityname,
          \local@cityname, \coppe@docyear.}\par}%
      \vspace*{4mm}
    \fi
  \fi}

%% r40: numero de linha das listagens dentro da mancha
\lstset{xleftmargin=2em}
\patchcmd{\pythonstyle}{numbersep=0.5em,}{numbersep=0.5em,xleftmargin=2em,}{}{}

%% r41: subalinea com hifen, sob a primeira letra do texto da alinea, e um espaco
\newlength\coppe@hifen
\settowidth\coppe@hifen{-}
\setlist[alineas,2]{label=-,labelindent=0pt,labelwidth=\coppe@hifen,
  labelsep=0.333em,leftmargin=!,align=left,itemsep=0pt}

%% r43: dedicatoria e epigrafe do meio da mancha
\renewcommand\dedication[1]{%
  \gdef\@dedic{#1}%
  \cleardoublepage
  \vspace*{\fill}%
  \begin{flushright}
    \begin{minipage}{0.5\textwidth}
      \raggedright\itshape\normalsize #1
    \end{minipage}
  \end{flushright}}
\renewcommand\epigrafe[2]{%
  \cleardoublepage
  \vspace*{\fill}%
  \begin{flushright}
    \begin{minipage}{0.5\textwidth}
      \raggedright\itshape\normalsize #1\par
      \vspace{1ex}{\raggedleft\normalfont\small #2\par}
    \end{minipage}
  \end{flushright}}

%% r59: aviso de nota de rodape com o sistema numerico
\if@coppenumeric
  \AtBeginDocument{%
    \let\coppe@orig@footnote\footnote
    \renewcommand\footnote{%
      \ClassWarningNoLine{coppe}{Sistema numerico com nota de rodape: a
        4.1.1.1.1 do Manual UFRJ/SiBI diz que o sistema numerico nao deve
        ser usado quando ha notas de rodape}%
      \coppe@orig@footnote}}
\fi
```

### A.2 `coppe.bbx`

```latex
%% r38 e r64
\AtBeginBibliography{%
  \raggedright
  \hyphenpenalty=\@M
  \exhyphenpenalty=\@M
  \renewcommand*{\bibrangedash}{-}}

%% r50
\renewcommand*{\subtitlepunct}{\addcolon\space}
\DeclareFieldFormat{subtitlecase}{#1}
\renewbibmacro*{title}{%
  \ifboolexpr{ test {\iffieldundef{title}} and test {\iffieldundef{subtitle}} }
    {}
    {\printtext[title]{\printfield[titlecase]{title}}%
     \setunit{\subtitlepunct}%
     \printfield[subtitlecase]{subtitle}%
     \newunit}%
  \printfield{titleaddon}}

%% r51
\renewbibmacro*{in:}{\printtext{\mkbibemph{\bibstring{in}}\addcolon\space}}
\DefineBibliographyStrings{brazilian}{andothers = {\mkbibemph{et al\adddot}}}
\DeclareStyleSourcemap{%
  \maps[datatype=bibtex]{%
    \map{\step[fieldsource=location, match=\regexp{\[S\.\s*l\.\]}, replace={[\\emph{S. l.}]}]}
    \map{\step[fieldsource=publisher, match=\regexp{\[s\.\s*n\.\]}, replace={[\\emph{s. n.}]}]}
    %% r60
    \map{\step[fieldsource=title, match=\regexp{\A(O|A|Os|As|Um|Uma|Uns|Umas|The|An)\s+(.+)\Z}, final]
         \step[fieldset=sorttitle, fieldvalue={$2}]}
  }%
}

%% r61
\renewcommand*{\bibdaterangesep}{\iffieldequalstr{endyear}{}{\mbox{-}\space}{/}}
```

### A.3 `coppe.cbx`

```latex
%% r58
\ExecuteBibliographyOptions{uniquename=minyearfull}
\DeclareNameFormat{labelname}{%
  \nameparts{#1}%
  \usebibmacro{name:family}{\namepartfamily}{\namepartgiven}{\namepartprefix}{\namepartsuffix}%
  \ifcase\value{uniquename}%
  \or
    \addcomma\space\namepartgiveni
  \or
    \addcomma\space\namepartgiven
  \fi
  \usebibmacro{name:andothers}}
```

### A.4 `coppe-numeric.cbx` e `coppe-numeric.bbx`

```latex
%% r59 (cbx)
\DeclareCiteCommand{\cite}[\mkbibparens]
  {\usebibmacro{cite:init}\usebibmacro{prenote}}
  {\usebibmacro{citeindex}\usebibmacro{cite:comp}}
  {}
  {\usebibmacro{cite:dump}\usebibmacro{postnote}}
\DeclareCiteCommand{\parencite}[\mkbibparens]
  {\usebibmacro{cite:init}\usebibmacro{prenote}}
  {\usebibmacro{citeindex}\usebibmacro{cite:comp}}
  {}
  {\usebibmacro{cite:dump}\usebibmacro{postnote}}

%% r59 (bbx)
\DeclareFieldFormat{labelnumberwidth}{#1}
\DeclareFieldFormat{shorthandwidth}{#1}
```

---

*Escrito em 16/09/2026, ao fim da conferência (issue #112). Atualizar a cada
issue fechada: marcar a fase, anotar o commit, e tirar daqui o que deixou de ser
verdade.*
