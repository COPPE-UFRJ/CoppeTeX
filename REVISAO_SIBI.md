# CoppeTeX × Nova Norma (Manual UFRJ/SiBI, 9.ª ed. rev., 2026)

Verificação item a item da CoppeTeX 4.x (branch `nlinguas`) contra os
documentos da pasta `Nova Norma/`, com comparação ao manual anterior
(`specs/manual2024.pdf`) e lista consolidada de tarefas.

*Substitui integralmente a versão anterior deste arquivo, que era baseada
apenas no parecer recebido e no manual de 2025.*
*Última atualização: 2026-09-04.*

---

## 0. O que é a "Nova Norma", e o que ela invalida

A pasta `Nova Norma/` contém dois documentos:

| Arquivo | O que é |
|---|---|
| `Manual para elaboração e normalização de trabalhos acadêmicos 2024.pdf` | Manual UFRJ/SiBI, **9.ª ed. rev., 2026** |
| `Folha adicional T&D Coleta+ CAPES.pdf` | Modelo oficial da **folha de rosto + folha adicional de Coleta CAPES** |

**Atenção aos nomes de arquivo, que enganam nos dois lados.** O arquivo da
pasta `Nova Norma/` diz "2024" mas é a edição **revista de 2026**. E o
`specs/manual2024.pdf` do repositório também diz "2024", mas é a **9.ª ed.,
2025**. Os dois nunca foram o manual de 2024. Vale renomear ambos.

Descoberta lateral relevante: **`specs/manual2024.pdf` contém as suas
anotações**, que não estão em nenhum outro lugar do repositório e que se
perdem se o arquivo for simplesmente substituído. São elas:

- nas margens: *"Aqui precisa usar um binding offset novo"*;
- no sumário: *"Importante: formatação do sumário deve ser assim! Não tem
  ponto final!"*;
- nos títulos de seção: *"chapter: todas maiúsculas, bold / section: todas
  maiúsculas em normal / subsection: as primeiras letras de cada palavra em
  maiúscula, em bold / subsubsection: … em bold e itálico / subsubsubsection:
  itálico, só a primeira palavra inicia em maiúscula"*;
- *"Limite da numeração 1.1.1.1.1"*.

A anotação sobre o *binding offset* está **superada** pela edição 2026 (ver
V02). As demais continuam válidas e viraram tarefas.

### Por que houve uma edição revista

O próprio manual explica (§1): a revisão responde a três fatos novos —
**Resolução CEPG n. 246/2023** (entrega apenas digital, fim da via impressa),
**Resolução CEPG n. 302/2024** (art. 57: idiomas admitidos) e o **novo modelo
de coleta de informações acadêmicas da CAPES**. As três mudanças atingem a
CoppeTeX diretamente.

### As quatro mudanças estruturais de 2025 → 2026

1. **Nasce a "folha adicional com ficha catalográfica"** (novo item 3.1.2.1.2),
   obrigatória **a partir de agosto de 2026**, logo após a folha de rosto. A
   ficha catalográfica deixa de ficar no verso da folha de rosto e passa a
   viver dentro dessa folha, junto com os campos de Coleta CAPES.
2. **Some o conceito de verso.** A edição 2025 especificava margens de verso
   (dir. 3 cm / esq. 2 cm) e recomendava imprimir o miolo em anverso e verso.
   A edição 2026 **eliminou as margens de verso** e trocou "anverso/verso"
   por "folhas" em todo o texto.
3. **PDF/A passa a ser obrigatório** (§2.2(d) e Anexo I) — formato de
   arquivamento de longo prazo.
4. **A errata perde a seção própria** e sai da lista de elementos opcionais e
   da lista de títulos centralizados.

---

## 1. Verificações, uma a uma

Legenda do veredicto: **OK** = a CoppeTeX já atende · **AJUSTAR** = atende
parcialmente · **FALTA** = não implementado · **QUEBRADO** = a nova edição
tornou incorreto o que hoje existe.

### A. Formato, margens, espaçamento e paginação

| # | Especificação (Nova Norma 2026) | Mudou em relação a 2025? | CoppeTeX hoje | Veredicto |
|---|---|---|---|---|
| **V01** | A4 retrato; texto em preto; fonte 12; fonte menor em citações longas, notas, **paginação** e legendas (§2.2) | Redação nova ("configuração de página" no lugar de "papel branco ou reciclado"); some "datilografadas" | `a4paper`; legendas em `\footnotesize`; notas em `\singlespacing`; **paginação em corpo normal** | AJUSTAR (só a paginação) |
| **V02** | Margens: **esquerda 3, superior 3, direita 2, inferior 2** (§2.3) | **SIM — as margens de verso foram eliminadas** | `twoside, bindingoffset=1cm, top=3, bottom=2, inner=2, outer=2` | **QUEBRADO** |
| **V03** | Elementos pré-textuais escritos **na frente da folha** (§2.2c) | Redação nova; antes "no anverso (frente)" | `twoside` + `\cleardoublepage` geram versos em branco | QUEBRADO (resolve com V02) |
| **V04** | Entrega em **PDF/A** (§2.2d, Anexo I) | **SIM — exigência nova** | Não produz PDF/A | **FALTA** |
| **V05** | Texto em 1,5; espaço simples em citações >3 linhas, notas de rodapé, notas de referência, referências (inclusive a linha em branco entre elas), títulos e fontes/legendas de ilustrações e tabelas, ficha catalográfica, e na folha de rosto a natureza/objetivo/instituição (§2.4) | Saiu "a área de concentração"; "ficha catalográfica (no verso da folha de rosto)" virou só "ficha catalográfica" | `\onehalfspacing` padrão; notas, fontes e legendas em `\singlespacing` | OK (conferir referências e folha de rosto) |
| **V06** | Recuo de citação longa: 4 cm da margem esquerda (§2.2b) | Não | `\recuolongquote = 4cm` | **OK** |
| **V07** | Contagem sequencial **a partir da folha de rosto**, sem numerar; **a folha adicional não é contada nem numerada**; numeração arábica **a partir da primeira folha textual, continuando a contagem**, no **canto superior direito**, a 2 cm das bordas superior e direita (§2.7) | **SIM** — antes o não-contado era o verso da folha de rosto; antes a posição alternava anverso/verso | `\frontmatter` → romanos reiniciando em 1; `\mainmatter` → arábicos **reiniciando em 1**; `\fancyhead[RO,LE]` (canto externo) | **QUEBRADO em três pontos** |
| **V08** | Títulos sem indicativo numérico são centralizados: agradecimentos, listas, resumo, sumário, referências, glossário, apêndice, anexo, índice (§2.6) | **SIM — "errata" saiu da lista** | `\titleformat{name=\chapter,numberless}` com `\filcenter` | **OK** |
| **V09** | Destaque **gradativo** dos títulos: negrito, itálico, grifo, redondo, caixa-alta ou versal (§2.6) | Não | `\section` = `\bfseries` + caixa alta; `\subsection` = `\bfseries`; `\subsubsection` = `\bfseries\itshape` | AJUSTAR — a sua própria anotação diz **section em caixa alta e normal, sem negrito** |
| **V10** | Sem ponto, hífen ou travessão entre o indicativo numérico e o título (§2.6) | Não | `\titleformat` com separação de `1ex`, sem sinal | **OK** |
| **V11** | Seções primárias em folha distinta; só há exigência de página ímpar quando o trabalho é diagramado em páginas (§2.6) | **SIM** — antes era "anverso" | `openright` (herdado de `twoside`) | Resolve com V02 |
| **V12** | Numeração até a quinária, recomendada (§2.6) | Não | Sem limite explícito | Menor |

### B. Capa e elementos pré-textuais

| # | Especificação (Nova Norma 2026) | Mudou? | CoppeTeX hoje | Veredicto |
|---|---|---|---|---|
| **V13** | **Capa** (§3.1.1, Anexo A): nome da instituição, autor, título, **subtítulo**, **número de volumes**, local, **ano de depósito**. Logos opcionais | Não | UFRJ + COPPE + Programa, autor, título, cidade, ano; logos presentes | AJUSTAR — faltam subtítulo e volumes. **O parecer errou aqui: a instituição já está lá** |
| **V14** | **Folha de rosto** (§3.1.2.1.1, Anexo B): (a) autor, (b) título, (c) subtítulo precedido de dois pontos, (d) número de volumes, (e) natureza + objetivo + instituição + **área de concentração**, (f) **orientador e coorientador** + local, (g) **ano de depósito**. Modelo **sem logos**, com o bloco (e) alinhado do meio da mancha à margem direita e em espaço simples | Não, salvo pela saída da ficha do verso | Título **antes** do autor; logos no topo; mês + ano; bloco recuado de 8,45 cm; sem subtítulo, volumes, área de concentração, coorientador | AJUSTAR — **6 divergências** |
| **V15** | Modelo CAPES acrescenta à folha de rosto uma linha de **Linha de Pesquisa**, e coloca orientador e coorientador **na margem esquerda** | **SIM — novo** | Não existe | **FALTA** |
| **V16** | **Folha adicional com ficha catalográfica** (§3.1.2.1.2, Anexo H): obrigatória **a partir de agosto de 2026**, **imediatamente após a folha de rosto**, **preenchida pelo programa de pós-graduação**. Contém os campos de Coleta CAPES — tipo de produção intelectual (bibliográfica / artística / tecnológica / técnica), projeto de pesquisa vinculado (sim/não), nome do projeto, área de concentração, agências de fomento (nome por extenso + sigla) — **e** a ficha catalográfica gerada em <http://fichacatalografica.sibi.ufrj.br/>. **Não é contada nem numerada** | **SIM — elemento inteiramente novo** | `\makecatalog` compõe a ficha em LaTeX e a imprime no **verso da folha de rosto** | **QUEBRADO — a mudança mais importante de todas** |
| **V17** | **Folha de aprovação** (§3.1.2.1.3, Anexo D): (a) autor, (b) título por extenso + subtítulo, (c) natureza/objetivo/instituição/**área de concentração** (do meio da mancha à direita), (d) **data de aprovação** ("Aprovada em: ___"), (e) **nome, titulação e instituição** de cada membro da banca, **com o orientador em primeiro lugar por ser o presidente**. Sem bloco separado de orientadores; sem local/data no rodapé | Não | Título antes do autor e em caixa alta; bloco "Orientadores:" separado; **`"Aprovada por:"` fixo em português**; `\examiner{titulação}{nome}{grau}` **descarta o 3.º argumento** e não tem campo de instituição; sem data de aprovação; rodapé com local e data | AJUSTAR — **7 divergências**. **Correção ao parecer: o orientador deve sim aparecer, como primeiro membro da banca** |
| **V18** | **Resumo em língua vernácula** (§3.1.2.1.4, Anexo E): espaço **1,5**; parágrafo único; 3.ª pessoa do singular, voz ativa; 150 a 500 palavras; **sugere-se** que venha antecedido da referência bibliográfica completa; **palavras-chave ao final**, precedidas de "Palavras-chave:", separadas por ponto e vírgula | Não | Página no formato COPPE (título, autor, mês/ano, orientadores, programa); **não imprime palavras-chave**, embora `\keyword` exista e alimente só o `hyperref` | AJUSTAR — palavras-chave é **defeito**; a referência é **sugestão**, não obrigação |
| **V19** | **Resumo em língua estrangeira** (§3.1.2.1.5): a versão do resumo vernáculo no idioma de divulgação internacional — portanto **dois** resumos | Não | Dois resumos + terceiro opcional (`brazilianabstract`), por decisão da Norma COPPE 2026 §3 | Compatível como **acréscimo** da COPPE; documentar |
| **V20** | **Sumário** é o último elemento pré-textual; títulos alinhados à esquerda; sem ponto final (sua anotação) | **SIM** — saiu "iniciar no anverso, usando o verso se necessário" | Verificar o ponto final e o alinhamento | AJUSTAR |
| **V21** | Dedicatória e epígrafe: do meio da mancha à margem direita, parte inferior; não numeradas (§2.6, §3.1.2.2) | Não | Verificar | AJUSTAR |
| **V22** | **Errata**: perdeu a seção própria e saiu dos elementos opcionais | **SIM** | Não implementa | **OK — nada a fazer** |
| **V23** | Agradecimentos: palavra **AGRADECIMENTOS em caixa-alta e negrito** (§3.1.2.2.2) | Não | Capítulo sem numeração, centralizado, `\Large\bfseries` | OK |

### C. Parte textual e pós-textual

| # | Especificação (Nova Norma 2026) | Mudou? | CoppeTeX hoje | Veredicto |
|---|---|---|---|---|
| **V24** | **Apêndice e Anexo**: letras maiúsculas consecutivas, **travessão** e respectivos títulos; letras dobradas quando esgotado o alfabeto; destaque tipográfico igual ao da seção primária (§3.1.4.3–4) | Não | `\if@coppeappendix` monta `APÊNDICE A – Título` com `\textendash` | **OK** — e a Norma COPPE 2026 §6 está correta |
| **V25** | **Referências**: essa é a nomenclatura, não "Bibliografia"; NBR 6023 (§3.1.4.1) | Não | biblatex com estilos `coppe` | **OK** |
| **V26** | Havendo apêndice e anexo, suas folhas seguem a numeração contínua do texto (§2.7) | Não | Segue | OK |
| **V27** | Mais de um volume: sequência única de numeração do primeiro ao último volume; sumário completo em cada volume (§2.7, §3.1.2.1.6) | Não | Sem suporte a volumes | FALTA (ver V13/V14) |

### D. Ilustrações, tabelas e quadros

| # | Especificação (Nova Norma 2026) | Mudou? | CoppeTeX hoje | Veredicto |
|---|---|---|---|---|
| **V28** | Identificação **na parte superior**: palavra designativa + número arábico + **travessão** + título; **fonte obrigatória na parte inferior**, mesmo quando é produção do próprio autor (§2.10, §2.11) | Não | `\captionsetup{labelsep=endash}` e `\cpsource` para a fonte | **OK, exceto algoritmos** |
| **V29** | Idem para algoritmos, como qualquer ilustração | Não | `algorithm2e` carregado com a opção **`ruled`**, que ignora o `caption` da classe: legenda em negrito, com filetes acima e abaixo, e **sem travessão** | AJUSTAR — confirma o parecer |
| **V30** | Quadro × tabela (nota de rodapé 3, critério IBGE): quadro delimitado nos quatro lados, tabela só no topo e na base | Não | Norma COPPE 2026 §5 e a classe seguem esse critério | **OK** |
| **V31** | Listas de ilustrações: nome específico + **travessão** + título + número da folha (§3.1.2.2.4) | Não | Verificar o travessão nas listas geradas | AJUSTAR |
| **V32** | Tipo, número, título, fonte, legenda e notas devem respeitar as margens da ilustração (§2.10) | Não | Estouro de margem em listagem de código na seção 7.6 do manual | AJUSTAR (defeito do manual, não da classe) |

### E. Idiomas

| # | Especificação (Nova Norma 2026) | Mudou? | CoppeTeX hoje | Veredicto |
|---|---|---|---|---|
| **V33** | **Resolução CEPG n. 302/2024, art. 57**: teses e dissertações podem ser redigidas em **português, inglês ou espanhol** (§2.1, Anexo G) | **SIM — a citação normativa é nova** | v4.0 oferece cinco idiomas principais, incluindo francês e italiano | **QUEBRADO** — francês e italiano não têm respaldo normativo. A Norma COPPE 2026 §4 já lista só pt/en/es; a classe, o `README`, o `CHANGELOG` e a `CARTA_CPGP` contradizem a própria Norma |
| **V34** | Resumo estrangeiro "no idioma de divulgação internacional" — para trabalho em espanhol, o par natural é es + en, deixando o português de fora | Não | O terceiro resumo (`brazilianabstract`) da Norma COPPE cobre exatamente esse caso | **OK** — é uma boa razão para defender o acréscimo da COPPE |

---

## 2. O que foi apagado da lista anterior, e por quê

| Tarefa anterior | Destino |
|---|---|
| **F-3/F-4/F-5/F-6** — corrigir `p.`→`f.`, remover `29,7cm`, espaçamento e ordem dentro da ficha gerada pela classe | **APAGADAS.** A ficha não é mais composta pela classe: vem pronta do gerador do SiBI, dentro da folha adicional (V16). Corrigir a `\makecatalog` seria polir algo que sai do documento |
| **D-2**, parte "ficha com UFRJ/COPPE e Programa" e "páginas das Referências na ficha" | **APAGADAS.** Deixam de ser conflito com o SiBI: nenhum dos dois campos é mais da classe. A Norma COPPE 2026 §2.3 precisa ser reescrita, não negociada |
| **D-2**, parte "orientadores na folha de aprovação" | **APAGADA — o parecer estava errado.** O §3.1.2.1.3 manda o orientador aparecer, em primeiro lugar, como presidente da banca. O que muda é a forma: um único bloco de banca, não um bloco "Orientadores:" separado |
| **D-3** — esclarecer a paginação com o SiBI | **APAGADA.** O §2.7 responde sem ambiguidade (V07). A Introdução **não** é a página 1 |
| **D-5** — decidir se a classe continua gerando a ficha | **APAGADA.** A Nova Norma decidiu |
| **S-3** — reescrever a página de resumo começando pela referência | **REBAIXADA a P2.** O §3.1.2.1.4 diz "**sugere-se**". A página no formato COPPE é defensável |
| **T-7** — verificar o esquema de títulos contra o manual | **CONVERTIDA em ação concreta** (V09), com base na sua anotação: `\section` em caixa alta **sem negrito** |
| **T-2** — avaliar `oneside` | **PROMOVIDA a P0.** Deixou de ser questão de gosto: a edição 2026 eliminou as margens de verso e a entrega é digital (V02, V03) |
| **D-1** — decidir entre convergir para o SiBI ou manter a identidade COPPE | **REDUZIDA.** Com a ficha fora da classe e a paginação resolvida, sobra praticamente só a página de resumo. Não é mais uma decisão de política, é um item |
| Item 1 do parecer — "capa sem o nome da instituição" | **IMPROCEDENTE**, confirmado pelo Anexo A |
| Item 31 do parecer — "as margens mudam ao longo do documento" | **PROCEDENTE AGORA.** Era o espelhamento de `twoside`, defensável em 2025; a edição 2026 tirou a base normativa dele |

---

## 3. TODO consolidado — rumo à CoppeTeX conforme à Nova Norma

Prioridade: **P0** = bloqueia o PR / a conformidade a partir de agosto de 2026 ·
**P1** = antes do release v4.0 · **P2** = depois.

### N — Norma COPPE 2026 (o documento precisa ser revisto antes do código)

- [ ] **N-1 (P0)** Reescrever `NORMA_COPPE_2026.md` §2.3: a ficha
      catalográfica deixa de ser composta pela COPPE. Substituir pela
      remissão à **folha adicional** do SiBI e ao gerador de fichas.
- [ ] **N-2 (P0)** Corrigir `NORMA_COPPE_2026.md` §7: a numeração arábica
      **continua a contagem iniciada na folha de rosto** e não reinicia em 1
      na parte textual; os pré-textuais são contados e não numerados; a
      folha adicional não é contada. O texto atual contraria a NBR 14724 e
      o §2.7 do manual.
- [ ] **N-3 (P0)** Acrescentar à Norma a **folha adicional de Coleta CAPES**
      como elemento essencial a partir de agosto de 2026, com a ressalva de
      que é preenchida pelo programa.
- [ ] **N-4 (P0)** Ajustar §1.1 e a bibliografia: o documento base passa a
      ser a **9.ª ed. rev., 2026**, e não a 9.ª ed., 2025. Citar as
      Resoluções CEPG 246/2023 e 302/2024.
- [ ] **N-5 (P0)** §4: manter pt/en/es e dizer explicitamente que o
      fundamento é o **art. 57 da Res. CEPG 302/2024**.
- [ ] **N-6 (P1)** §3: justificar o terceiro resumo pelo caso do trabalho em
      espanhol (V34) — é o argumento mais forte a favor dele.
- [ ] **N-7 (P1)** Regerar `NORMA_COPPE_2026.pdf` e `futuremanual2026.pdf`.

### C — Folha adicional e Coleta CAPES (o bloco novo)

- [ ] **C-1 (P0)** Implementar `\folhaadicional{<arquivo.pdf>}`: inclui o PDF
      da folha adicional (gerada pelo programa) **imediatamente após a folha
      de rosto**, **fora da contagem de páginas** e sem numeração.
- [ ] **C-2 (P0)** Alternativa nativa `\makefolhaadicional`, compondo em
      LaTeX os campos do Anexo H — tipo de produção intelectual
      (bibliográfica / artística / tecnológica / técnica), projeto de
      pesquisa vinculado (sim/não), nome do projeto, área de concentração,
      agências de fomento (por extenso + sigla) — com espaço reservado para
      a ficha catalográfica do gerador do SiBI.
- [ ] **C-3 (P0)** Novos comandos de preâmbulo para alimentar C-2:
      `\tipoproducao{}`, `\projetopesquisa{}`, `\nomeprojeto{}`,
      `\areaconcentracao{}`, `\agenciafomento{}{}` (repetível).
- [ ] **C-4 (P0)** Retirar `\makecatalog` do verso da folha de rosto.
      Mantê-la apenas como pré-visualização durante a redação, sob opção de
      classe `rascunhoficha`, com aviso no log de que não é a ficha oficial.
- [ ] **C-5 (P1)** Gerar no site do SiBI uma ficha real para o `example.tex`
      e guardá-la em `tests/` como baseline visual.
- [ ] **C-6 (P1)** Documentar no manual e no `MIGRATION_v3_to_v4.md` que a
      ficha passou a ser responsabilidade do programa, com o passo a passo.

### G — Geometria, paginação e PDF/A (o bloco que a edição 2026 quebrou)

- [ ] **G-1 (P0)** Trocar a geometria para **`oneside`**, `left=3cm`,
      `right=2cm`, `top=3cm`, `bottom=2cm`, **sem `bindingoffset`**.
      Manter `twoside` apenas como opção de classe explícita, para quem
      ainda quiser imprimir.
- [ ] **G-2 (P0)** Paginação: **não reiniciar em 1 na parte textual**.
      Contar a partir da folha de rosto, imprimir arábicos a partir da
      primeira folha textual dando sequência à contagem.
- [ ] **G-3 (P0)** Tirar a folha adicional da contagem (`\stepcounter`
      suprimido / página não contada).
- [ ] **G-4 (P0)** Número de página no **canto superior direito** em todas
      as folhas (`\fancyhead[R]`), a 2 cm das bordas superior e direita —
      no lugar do atual `[RO,LE]`.
- [ ] **G-5 (P1)** Pré-textuais sem numeração impressa por padrão
      (contados, não numerados), coerente com N-2.
- [ ] **G-6 (P0)** **PDF/A**: gerar saída conforme, via `pdfx` ou
      `hyperref`/`hyperxmp` com perfil de cor embutido, fontes embutidas e
      metadados XMP. Documentar no manual e conferir com `veraPDF`.
- [ ] **G-7 (P1)** Paginação em corpo menor (V01).

### R — Folha de rosto e capa

- [ ] **R-1 (P0)** Inverter a ordem na folha de rosto: **autor antes do
      título**.
- [ ] **R-2 (P1)** Novo `\subtitle{}`, impresso após o título, precedido de
      dois pontos, na capa e na folha de rosto.
- [ ] **R-3 (P1)** Novo `\volumes{<n>}` / `\volume{<i>}`, com impressão
      condicional na capa e na folha de rosto.
- [ ] **R-4 (P1)** Novo `\areaconcentracao{}`, incluído no bloco de natureza
      da folha de rosto e da folha de aprovação (reaproveita C-3).
- [ ] **R-5 (P1)** Novo `\coadvisor{}` (coorientador), distinto de
      `\advisor`.
- [ ] **R-6 (P1)** Novo `\linhapesquisa{}` — exigido pelo modelo CAPES.
- [ ] **R-7 (P1)** Orientadores e coorientadores alinhados **à margem
      esquerda**, fora do bloco recuado.
- [ ] **R-8 (P1)** Bloco de natureza alinhado **do meio da mancha à margem
      direita** e em **espaço simples**.
- [ ] **R-9 (P1)** Data: **apenas o ano de depósito** (hoje sai mês + ano).
      Manter `\date{mês}{ano}` por compatibilidade, mas usar só o ano.
- [ ] **R-10 (P2)** Avaliar remover os logos da folha de rosto — o Anexo B
      não os traz (na capa, o Anexo A os declara opcionais).

### A — Folha de aprovação

- [ ] **A-1 (P0)** *Bug de i18n:* `"Aprovada por:"` está **fixo em
      português** em `\makefrontpage` (`coppe.cls`, l. 742), enquanto o
      dispatcher já tem `approvedmale`/`approvedfemale` (l. 331–334). Uma
      tese em inglês ou espanhol sai com essa linha em português.
- [ ] **A-2 (P1)** Inverter a ordem: autor antes do título; remover o
      `\MakeUppercase` do título.
- [ ] **A-3 (P1)** Substituir o bloco separado de orientadores por **uma
      única lista de banca, com o orientador em primeiro lugar** como
      presidente (§3.1.2.1.3(e)).
- [ ] **A-4 (P1)** Acrescentar **"Aprovada em: ______"** (data de
      aprovação).
- [ ] **A-5 (P1)** Estender `\examiner` para **nome, titulação e
      instituição** — hoje o 3.º argumento (grau) é **silenciosamente
      descartado** e não existe campo de instituição. **Mudança de API**:
      exige entrada em `MIGRATION_v3_to_v4.md`.
- [ ] **A-6 (P1)** Incluir o bloco de natureza/objetivo/instituição/área de
      concentração, do meio da mancha à direita.
- [ ] **A-7 (P1)** Remover o local e a data do rodapé
      (`\frontpage@bottomtext`).

### S — Resumos

- [ ] **S-1 (P1)** Imprimir as **palavras-chave** ao final de cada resumo,
      precedidas de "Palavras-chave:" (e equivalentes por idioma),
      separadas por ponto e vírgula. Hoje `\keyword` só alimenta o
      `hyperref`.
- [ ] **S-2 (P2)** Oferecer, como **opção**, a referência bibliográfica
      completa no topo da página de resumo (Anexo E) — "sugere-se", não
      obrigatório.
- [ ] **S-3 (P2)** Avisar no log quando o resumo ficar fora da faixa de
      150–500 palavras.

### I — Idiomas

- [ ] **I-1 (P0)** Rebaixar **francês e italiano** de "idioma principal
      autorizado" para "exemplo de *language pack*", sem respaldo na Res.
      CEPG 302/2024. Ajustar `README.md`, `CHANGELOG.md`, `CARTA_CPGP.md` e
      o manual **antes** de a CPGP avaliar o PR — hoje a classe contradiz a
      própria Norma COPPE §4.
- [ ] **I-2 (P1)** Emitir aviso no log quando `french` ou `italian` for
      usado como idioma principal.

### T — Tipografia e corpo do texto

- [ ] **T-1 (P0)** Carregar `indentfirst` (ou aplicar o recuo via
      `titlesec`): hoje o primeiro parágrafo de cada seção sai sem recuo, e
      o pacote só aparece **comentado** no preâmbulo do exemplo
      (`coppe.dtx`, l. 965).
- [ ] **T-2 (P1)** `\section`: **caixa alta sem negrito**, conforme a sua
      anotação e o destaque gradativo do §2.6. Revisar em cascata
      `\subsection` (versalete/título em bold) e `\subsubsection`.
- [ ] **T-3 (P1)** `algorithm2e`: substituir a opção `ruled` ou redefinir o
      estilo de legenda, para que os algoritmos usem **travessão**, sem
      negrito e sem filetes, como as demais ilustrações.
- [ ] **T-4 (P1)** Sumário: conferir a ausência de ponto final e o
      alinhamento à esquerda pela margem do indicativo mais extenso.
- [ ] **T-5 (P1)** Listas de ilustrações: garantir o **travessão** entre o
      nome específico e o título.
- [ ] **T-6 (P1)** Uniformizar o alinhamento das legendas de tabela
      (5.1 e 5.2 destoam no manual).
- [ ] **T-7 (P1)** Corrigir o estouro de margem na listagem da seção 7.6 do
      manual.
- [ ] **T-8 (P1)** Manual: "algoritmo 6.1" → "Algoritmo 6.1".
- [ ] **T-9 (P2)** Dedicatória e epígrafe: alinhamento do meio da mancha à
      margem direita, na parte inferior da folha.

### H — Higiene do repositório

- [ ] **H-1 (P0)** Descartar o ruído de CRLF da árvore de trabalho
      (`git diff --ignore-cr-at-eol` volta vazio) e criar `.gitattributes`
      com `* text=auto eol=lf`. Adicionar `.claude/` ao `.gitignore`.
- [ ] **H-2 (P0)** **Preservar as suas anotações** de
      `specs/manual2024.pdf` antes de substituí-lo — elas não existem em
      nenhum outro lugar. Transcrevê-las para um `specs/ANOTACOES.md`.
- [ ] **H-3 (P1)** Renomear os manuais para o que de fato são:
      `specs/manual-sibi-9ed-2025.pdf` e
      `specs/manual-sibi-9ed-rev-2026.pdf`; mover a pasta `Nova Norma/`
      para dentro de `specs/`.
- [ ] **H-4 (P1)** Guardar em `specs/` o modelo oficial da folha
      adicional/CAPES e o link do gerador de fichas.
- [ ] **H-5 (P1)** Atualizar o `TODO.md` existente: o item 2 (revisão por
      nativos de espanhol/francês/italiano) reduz-se ao **espanhol**, se
      I-1 for aceito.

### V — Verificação

- [ ] **V-1 (P0)** Confirmar qual PDF o autor do parecer examinou: vários
      itens (sobretudo o da capa sem instituição) sugerem versão anterior
      ao commit `940f104`.
- [ ] **V-2 (P1)** Tabela de rastreabilidade *item do manual → macro da
      classe → página do `example.pdf`*, para responder à próxima revisão
      ponto a ponto.
- [ ] **V-3 (P1)** Ampliar `tests/` com um caso por página pré-textual,
      incluindo a folha adicional, e validar o PDF/A com `veraPDF` no CI.
- [ ] **V-4 (P1)** Regerar os exemplos e submeter de volta ao autor do
      parecer, com o que foi aceito, o que foi recusado e por quê —
      registrando as duas correções ao parecer (capa e orientador na folha
      de aprovação).

---

## 4. Sequência sugerida

1. **H-1, H-2, V-1** — barato e evita perder trabalho.
2. **N-1 a N-5** — a Norma COPPE precisa parar de contradizer o manual e a
   si mesma antes de qualquer linha de código.
3. **I-1** e **A-1** — bloqueiam a avaliação do PR e são baratos.
4. **G-1 a G-6** — geometria, paginação e PDF/A: o bloco que a edição 2026
   quebrou.
5. **C-1 a C-4** — a folha adicional. É o que torna a classe utilizável a
   partir de agosto de 2026.
6. **R**, **A**, **S**, **T** — o acabamento das páginas pré-textuais e da
   tipografia.
7. **V-2 a V-4** — resposta formal ao parecer e ao SiBI.

O prazo de **agosto de 2026 já passou**: a folha adicional (bloco **C**) é
hoje uma exigência vigente, e não uma antecipação.
