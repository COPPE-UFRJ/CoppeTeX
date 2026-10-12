# Como juntar o `master` ao `goufrj` e chegar à 5.0

> **Histórico.** Este guia foi seguido em 17/09/2026, com a estratégia **B**: o
> ramo novo `V05-unificada`, saído do `goufrj`, recebeu o
> `conformidade-manual-2026` (que era onde a conferência estava, e não o
> `master`) pelo `tools/juntar-master.py`. O merge é o commit `233b2b6`. Dos
> seis conflitos, o `resolver` fechou quatro, e dois ficaram à mão, como o
> guia previa; o `sobras` achou três nomes da 4.1 que entraram sem conflito. As
> issues da seção 4 foram corrigidas em seguida no mesmo ramo — o estado de
> cada uma está no topo do `CORRECOES_MANUAL_2026.md`.


*Escrito em 17/09/2026, para ser seguido em casa. Tudo o que está citado aqui
foi conferido no `goufrj` publicado nesse dia.*

## 1. A situação

| Onde | O que tem |
|---|---|
| `goufrj` (GitHub) | A CoppeTeX 5.0: classe `ufrj`, estilo `ufrj-coppe`, classe `coppe` de compatibilidade, 46 testes regressivos passando. Os testes da 5.0 se chamam `rtu01`–`rtu04`. |
| `master` (GitHub) | Parado em `b8103c7` (4.1), o ponto de onde o `goufrj` saiu. |
| `master` (a outra máquina) | A conferência contra o Manual UFRJ/SiBI 2026 (issue #112): os testes `r33`–`r70` e `r89`, o `tests/regressivo/medidas.py`, o `CORRECOES_MANUAL_2026.md` e **correções já começadas no `coppe.dtx`**. |

Há indício forte de que as correções já tinham começado. A issue #153 cita linhas
do `coppe.dtx` (~1618, ~1678, ~5997, ~8022) que no `b8103c7` estão em 1607, 1665,
5875 e 7891. Algo acrescentou linhas antes delas. Além disso, a #152 e a #153 dizem
ter sido achadas "durante a correção" da #151 e da #114.

**Os nomes dos testes.** Cada prefixo diz de onde o teste veio. O rodador já
aceita os três.

| Prefixo | Origem |
|---|---|
| `r` | defeitos até a 4.1 (`r01`–`r32`) e ferramentas (`r90`–`r99`) |
| `rt` | a conferência de 16/09, feita no `master`: `r33`–`r70` e `r89` passam a `rt33`–`rt70` e `rt89` quando entram no ramo da 5.0 |
| `rtu` | a classe da UFRJ e o estilo de unidade (5.0) |

## 2. A estratégia

### As opções

| | Como | Custo | Risco |
|---|---|---|---|
| **A** | Juntar o `master` **no próprio `goufrj`**, corrigir as issues no `goufrj` e abrir um PR `goufrj` → `master` | um merge, feito uma vez | baixo, com a marca do passo 1 e publicando só depois de conferir |
| **B** | Criar um ramo novo (por exemplo `v5`) a partir do `goufrj`, juntar o `master` nele, corrigir lá e abrir PR `v5` → `master` | o mesmo da A, mais um nome | igual ao da A |
| **C** | Corrigir as issues primeiro no `master`, com os nomes da 4.1, e juntar depois | cada correção é feita, testada e depois traduzida; o merge final tem muito mais conflito | alto: toda correção toca código que o `goufrj` renomeou |
| **D** | Refazer a separação da 5.0 em cima do `master` novo | refazer as cinco etapas e a conferência página a página | alto e longo |

### A recomendação: **A**, com duas regras

1. **Congelar o `master` para correções.** A conferência entra no `master` do
   jeito que está, e daí em diante toda correção é feita na 5.0, com os nomes da
   5.0. Corrigir no `master` e juntar de novo multiplica os conflitos. O
   `juntar-master.py` aguenta um segundo merge, mas cada rodada custa.
2. **Marcar o ponto de partida e publicar só o que foi conferido.** Uma etiqueta
   no `goufrj` antes do merge, e nenhum `git push` antes de a compilação e a
   suíte terem rodado. Se o merge sair errado, volta-se à etiqueta sem ter
   publicado nada.

**Ramo novo (B) vale a pena?** Para o git, A e B produzem os mesmos commits: um
ramo é só um nome que aponta para eles. O que B dá a mais é deixar o `goufrj`
parado na separação pura, e a etiqueta da regra 2 dá isso sem criar outro nome.
O que B tira: os comentários nas issues, o `README` e este guia apontam para o
`goufrj`, e um segundo ramo obriga a dizer em cada lugar qual dos dois vale.

B só compensa num caso: se alguém precisar revisar a separação sozinha,
enquanto as correções andam em outro lugar — por exemplo, se a CPGP for olhar a
5.0 antes das correções. Aí o caminho é B, com o `goufrj` como está.

Um PR só, no fim, e não dois. Um PR só da separação, `goufrj` → `master`,
conflitaria com a conferência que já estará no `master`. Seria preciso juntar
os dois de qualquer jeito.

## 3. Passo a passo

### 3.1 Na máquina da conferência

1. Termine ou guarde o que está no meio. Correção pela metade vai para um
   `git stash`, e será refeita na 5.0. Correção terminada, com o teste dela
   passando, pode ir junto.
2. Faça commit do resto: testes, `medidas.py`, `CORRECOES_MANUAL_2026.md`,
   correções terminadas, arquivos gerados e PDFs, se foram refeitos.
3. Rode a suíte na 4.1 e anote quais `r33`–`r89` passam, que são as correções já
   feitas.

   ```bash
   python tests/regressivo/run-regressivo.py
   ```

4. Publique o `master`.

   ```bash
   git push origin master
   ```

### 3.2 Em casa: o merge

```bash
git fetch origin
git switch goufrj
git pull --ff-only
git tag -a 5.0-antes-da-conferencia -m "goufrj antes de juntar a conferencia de 16/09"
python tools/juntar-master.py juntar origin/master
```

O `juntar` faz duas coisas.

- **Tira as cópias da `dist/`.** Faz um commit que remove de `dist/` as cópias
  de `ufrj.dtx`, `ufrj.ins`, `ufrj-coppe.dtx` e `ufrj-coppe.ins`. Sem isso, o git
  pareia o `src/coppe.dtx` do master com o `dist/ufrj.dtx`, porque na base as
  duas cópias eram idênticas, e as correções vão parar **em silêncio** na cópia
  da `dist/`. A simulação do merge mostrou exatamente isso. O `painel --dist`
  põe as cópias de volta no fim.
- **Faz o merge.** Usa `--no-commit` e o estilo de conflito `diff3`, que mostra
  a versão da base e é o que permite resolver pela tradução dos nomes.

### 3.3 Resolver

```bash
python tools/juntar-master.py resolver
```

| Conflito | O que o `resolver` faz |
|---|---|
| Arquivo gerado (`.cls`, `.sty`, `.bbx`, `.cbx`, `.dbx`, `.lbx`, `.def`, `.ist`, `.bib` e `.tex` que o docstrip escreve) e qualquer coisa em `dist/` | fica o do `goufrj`: tudo sai de novo do `.dtx` |
| Gerado da 4.1 que a 5.0 não tem (`coppe-lang-*.def`, `brazilian-coppe.lbx`…) | removido |
| PDF | fica o do `goufrj`: será recompilado |
| Trecho do `ufrj.dtx` que só conflita por causa do nome (`\coppe@x` × `\ufrj@x`) | traduz a base e o lado do master e refaz a comparação de três vias: fica a mudança do master, com os nomes da 5.0 |
| Trecho que o master mudou e o `goufrj` levou para o `ufrj-coppe.dtx` (os exemplos) | aplica a mudança, traduzida e em pedaços pequenos, no `ufrj-coppe.dtx` |

O que ele não resolver aparece como **PENDENTE** ou **NAO ACHEI**. As regras
para fazer à mão:

- Conflito no `ufrj.dtx` em código que a 5.0 **mudou de verdade**, e não só
  renomeou: a abertura do resumo, a natureza, a capa, os logotipos, os textos
  de unidade. Fica a intenção do master, reescrita com a interface da 5.0:
  `\ufrj@unitstr`, `\ufrj@unitcover`, `\ufrj@logoline`, `\ufrj@unitsep`, as chaves
  `tounit`, `sciencename` e `natureza`. Dado da COPPE vai para o `ufrj-coppe.dtx`
  (módulo `package`), nunca para a classe: o `rtu04` reprova.
- **NAO ACHEI** no `ufrj-coppe.dtx`: aplique à mão no módulo certo
  (`maxexemplo`, `minexemplo`, `examplept`…). O relatório mostra o antes e o depois.
- Arquivo apagado de um lado e mudado do outro: veja se é gerado. Se for, apague.

### 3.4 Regerar, testes, sobras, commit

```bash
cd src
pdflatex ufrj.ins
pdflatex ufrj-coppe.ins
cd ..
python tools/juntar-master.py testes
python tools/juntar-master.py sobras
```

O `testes` faz três coisas:

- **Renomeia:** os testes que o master criou desde `b8103c7` passam a `rt`.
- **Traduz:** dentro deles, no `medidas.py` e no `CORRECOES_MANUAL_2026.md`,
  troca os nomes da 4.1. Todo `\documentclass{coppe}` vira
  `\documentclass{ufrj}` com `\usepackage{ufrj-coppe}` na linha seguinte.
- **Arruma o README:** as linhas dos testes novos vão para uma seção própria do
  README do regressivo.

O que ele marca como **CONFERIR** pede olho humano: strings de Python, listas de
arquivos da classe que o `medidas.py` copia (a 5.0 precisa de `ufrj.cls`,
`ufrj-coppe.sty` e, para a forma antiga, `coppe.cls`), e a variável `COPPE_SRC`.

O `sobras` tem de sair limpo: sem marca de conflito e sem nome da 4.1 no código
do `ufrj.dtx` nem nos testes `rt`. Depois:

```bash
git add -A
git commit
```

A mensagem sugerida: `merge: a conferencia de 16/09 (#112) entra na 5.0`.

### 3.5 Compilar, conferir, publicar

```bash
coppetex.bat --tudo --regressivo --conferir --dist
```

O que esperar:

- **Compilação:** 153 passos sem falha, ou mais, se a conferência acrescentou
  documentos.
- **Suíte:** todo `r` e todo `rtu` passam. Os `rt` falham, menos os das
  correções terminadas no passo 3.1, que agora têm de passar também na 5.0.
- **`dist/`:** volta a ter as cópias das fontes.

Um `rt` pode falhar por um motivo da 5.0, e não da issue: por exemplo, por
cobrar a frase "à COPPE/UFRJ" num documento sem `\usepackage{ufrj-coppe}`. Nesse
caso corrija o **teste**, no mesmo commit, dizendo por quê.

Só então:

```bash
git push origin goufrj --follow-tags
```

### 3.6 Corrigir as issues

Uma issue por commit, com a linha `Fecha #NNN` na mensagem e o `rtNN` dela
passando. A ordem abaixo segue o tipo de erro, e o `CORRECOES_MANUAL_2026.md`
da conferência tem a ordem fina e as armadilhas.

1. **Decisões primeiro**, porque mudam o que se corrige: #128, #129, #130, #150,
   #153, #124 e o caminho da chamada da #144.
2. **Classe (`ufrj.dtx`, módulo `class`)**: #113, #114, #115, #116, #117, #119,
   #120, #121, #122, #123, #125, #127 e #152. A #126 fica por último, pela
   prioridade baixa.
3. **Bibliografia (`ufrj.dtx`, módulos `bbx`, `cbx`, `dbx`, `lbx*`, `num*`)**:
   #118, #131, #132, #133, #134, #135, #136, #137, #138, #139, #140, #141, #142,
   #143, #144, #145 e #146.
4. **Dados**: #147, #148 e #149.
5. **Ferramentas**: #151. Documentação: #153.

No fim, o PR `goufrj` → `master`, com a suíte inteira passando.

## 4. As issues contra o `goufrj`

Conferidas uma a uma no código do `goufrj`. **Todas as 41 continuam valendo na
5.0**: a separação não corrigiu nem piorou nenhuma. O que muda é **onde** se
corrige.

O **tipo** diz se o erro está num **programa**, numa **ferramenta**, nos
**dados** ou na **documentação**:

- **Programa:** a classe (`.cls`) ou os estilos (`.sty`, e os do biblatex:
  `.bbx`, `.cbx`, `.dbx`, `.lbx`).
- **Ferramenta:** um script do projeto.
- **Dados:** os exemplos e as bases (`.tex`, `.bib`).
- **Documentação:** manuais e Norma.

As linhas são do `goufrj` em 17/09/2026; os programas e os exemplos saem de um
`.dtx`, e o módulo vai entre colchetes.

### Nomes e arquivos que mudaram

| Na 4.1 (como as issues citam) | Na 5.0 |
|---|---|
| `coppe.dtx` | `ufrj.dtx` (classe, biblatex, bases, pacotes de idioma) e `ufrj-coppe.dtx` (estilo da COPPE, classe `coppe` de compatibilidade, **todos os exemplos**) |
| `coppe.cls`, `coppe.bbx`, `coppe.cbx`, `coppe.dbx` | `ufrj.cls`, `ufrj.bbx`, `ufrj.cbx`, `ufrj.dbx` |
| `coppe-numeric.bbx`/`.cbx`, `brazilian-coppe.lbx` | `ufrj-numeric.bbx`/`.cbx`, `brazilian-ufrj.lbx` |
| `\coppe@…`, `coppe:partdriver`, `coppe:mediadriver` | `\ufrj@…`, `ufrj:partdriver`, `ufrj:mediadriver` |
| `\newcoppefloat`, `\coppemainstring` | `\newufrjfloat`, `\ufrjmainstring`; os nomes velhos valem como apelidos no `ufrj-coppe.sty` |
| teste `r33`…`r70`, `r89` | `rt33`…`rt70`, `rt89` |

### Leiaute e elementos pré e pós-textuais

| Issue | Tipo | Onde, no `goufrj` | O que a 5.0 muda |
|---|---|---|---|
| #113 títulos maiores que 12 | programa | `ufrj.dtx` 3685–3757 [class]: `\titleformat` de capítulo, apêndice, sem número e seção, com `\Large`/`\large`; 6214 e 6246, títulos da folha adicional | nomes (`\ufrj@appendixheadings`, 3697) |
| #114 resumo sem título | programa | `ufrj.dtx` 6459 `\ufrj@resumocabeca` [class] | a frase de abertura já é texto de unidade (`\ufrj@toptext` com a chave `tounit`, que o `ufrj-coppe.sty` define como "à COPPE/UFRJ"). O título RESUMO é regra da UFRJ: vai na classe, para toda unidade |
| #115 pós-textuais fora da coluna | programa | `ufrj.dtx` 7457 `\defbibheading`, 7095 `theglossary`, 7119 `theindex`, 3724 e 3726 (anexo e apêndice no sumário), 4062 `\ufrj@listtoc` [class] | nomes |
| #116 listas sem nome e traço | programa | `ufrj.dtx` 4024 `\ufrj@wrapstarttoc`, 3938 `\l@quadro` [class] | `\newufrjfloat`; o traço depende da #150 |
| #117 notas de rodapé | programa | `ufrj.dtx` 3977–3978 (`\@footnotetext` com `\singlespacing`) [class]; a classe não redefine `\@makefntext` nem muda `\interfootnotelinepenalty` | nada |
| #118 referências justificadas | programa (biblatex) | `ufrj.dtx` 7734 `\AtBeginBibliography` [bbx] → `ufrj.bbx`, que o `ufrj-numeric.bbx` carrega | nada |
| #119 referência do resumo | programa | `ufrj.dtx` 6370 `\ufrj@refresumo` [class]; o `--` está em 6380 | a vinculação já pula a unidade quando não há uma |
| #120 números de linha na margem | programa | `ufrj.dtx` 4871–4912: `\pythonstyle`, `\xmlstyle`, `\htmlstyle`, `\prologstyle`, `\javastyle` com `numbers=left`, `numbersep=0.5em` e sem `xleftmargin` [class] | nada |
| #121 subalínea | programa | `ufrj.dtx` 3985 `\setlist[alineas,2]{label=--,leftmargin=1.8em,itemsep=0pt}` [class] | a receita da issue usa `\coppe@hifen`: escrever `\ufrj@hifen` |
| #122 espaço depois do título | programa | `ufrj.dtx`: há `\titlespacing` só para `\chapter` (3689, 3702, 3750) e `\paragraph` (3773); nenhum para seção, subseção e terciária [class] | nada |
| #123 dedicatória e epígrafe | programa | `ufrj.dtx` 6267–6275 `\dedication` (minipage de 60 mm, `\raggedleft`), 6286–6294 `\epigrafe` (meia mancha, mas `\raggedleft`) [class] | nada |
| #124 PDF/A desligado | programa + ferramenta | `ufrj.dtx` 4273 `\DeclareOption{pdfa}`, sem `sempdfa` [class]; `tools/geradocvazio.py` 165–166: campo desligado e a dica "Ligue ao depositar" | é o item "Tornar pdfa o padrão" do `TODO.md` |
| #125 legenda mais larga que a ilustração | programa | `ufrj.dtx` 3948–3954 `\cpsource`/`\source`, sem comando de largura [class] | nada |
| #126 volumes | programa | `ufrj.dtx` 5240–5241: `\volumes` e `\volume` só guardam o número [class] | nada |
| #127 letras depois do Z | programa | o `\appendix` da classe (3703–3705) chama o do `book`, que numera com `\@Alph`; o `\annex` (7553–7562) segue a mesma numeração e põe `\Alph` no `\theHchapter`; alíneas com `\alph*`, 3984 [class] | `\ufrj@tocapp`/`\ufrj@tocanx` (3711/3714); os apelidos `\coppe@tocapp`/`\coppe@tocanx` do estilo seguem a classe sozinhos |
| #128 folhas de identidade com dois idiomas | programa (textos da classe) | rótulos em `ufrj.dtx` 4707–4739 [class] e nos pacotes de idioma (8494… [langes]); natureza em 5118, lida em 7185 por `\ufrj@unitstrmain` | na 5.0 a natureza já é uma chave por idioma, com recaída no português. Foi a decisão adiada da 5.0 (item do `TODO.md`). Com (A), os rótulos ficam fixos em português. Com (B), basta escrever a chave `natureza` em inglês e em espanhol |
| #129 "(COPPE)" na capa | dado de identidade no estilo, ou Norma | `ufrj-coppe.dtx` 1876–1880 `\ufrjdeclareunit` [package]: o 2.º argumento é a forma da capa; Norma §2 em `NORMA_COPPE_2026.md` 87 e `src/NORMA_COPPE_2026.tex` 139 | **a classe não muda**: é uma linha do `ufrj-coppe.sty`, ou a Norma |
| #130 logotipos na folha de rosto | programa | `ufrj.dtx` 5741 (capa) e 5784 (folha de rosto) chamam `\ufrj@logoline` [class]; `ufrj-coppe.dtx` 1883 `\ufrjdeclarelogos` | tirar da folha de rosto é regra da UFRJ, para toda unidade. Manter só na COPPE seria escolha de comportamento por unidade, que a 5.0 ainda não tem (item do `TODO.md`) |

### Referências e citações

| Issue | Tipo | Onde, no `goufrj` | O que a 5.0 muda |
|---|---|---|---|
| #131 subtítulo | programa (biblatex) | `ufrj.dtx` [bbx]: nenhum `\subtitlepunct` nem macro `title` própria → `ufrj.bbx` | nada |
| #132 In:, et al., [S. l.] | programa (biblatex) + dados | `ufrj.dtx` 7802 `\renewbibmacro*{in:}` sem ênfase [bbx]; `andothers` não redefinido nos `.lbx` [lbx*]; `[S. l.]` e `[s. n.]` são digitados no `.bib` | nada |
| #133 edição, volumes, série | programa (biblatex) | `ufrj.dtx` [bbx]: sem formato de `edition` e sem drivers `book` e `report` → padrão do biblatex; a bibstring `volumes` não está no `brazilian-ufrj.lbx` (8320–8346 [lbxbr]) e vem do biblatex | nada |
| #134 parte de monografia | programa (biblatex) | `ufrj.dtx` 7870–7892 `ufrj:partdriver` [bbx]: `booktitle` sem `bookauthor` e sem `booksubtitle`; `pages` antes de `chapter` | nome do driver |
| #135 tradutor | programa (biblatex) | `ufrj.dtx` 7651 `\DeclareNameAlias{translator}{family-given}` [bbx] | nada |
| #136 DOI | programa (biblatex) | `ufrj.dtx` [bbx]: sem `\DeclareFieldFormat{doi}` → padrão do biblatex, com `\mkbibacro` | nada |
| #137 teses dos tipos padrão | programa (biblatex) | `ufrj.dtx` 7906 `\ufrj@degword`, 7913 formato `course` (monta "( em …)" com o grau vazio), 7919 driver `thesis` (`\setunit*` antes da instituição) [bbx] | nada |
| #138 citação pela entrada de título | programa (biblatex) | `ufrj.dtx` 8285 [cbx]: `authoryear-comp`, sem `citetitle` nem `nonameyeardelim` próprios → `ufrj.cbx` | nada |
| #139 mesmo sobrenome | programa (biblatex) | `ufrj.dtx` 7638 `uniquename=false` [bbx] **não vale**: o `authoryear-comp.cbx`, carregado pelo `ufrj.cbx` (8289), executa `uniquename` depois do `.bbx` e o liga de novo | a correção tem de ir no `.cbx` |
| #140 sistema numérico | programa (biblatex + classe) | `ufrj.dtx` 8693–8694 `labelnumberwidth` entre colchetes [numbbx]; 8721 `numeric-comp` [numcbx]; o aviso da nota de rodapé iria na classe | nada |
| #141 artigo na ordem alfabética | programa (biblatex) | `ufrj.dtx` 7641 `sorting=nyt`, 8188 `\DeclareSourcemap` [bbx] | **responde à dúvida da issue**: `\DeclareSourcemap` acumula. O `ufrj-coppe.sty` declara um segundo, e o `.bcf` de uma adversativa da 5.0 guarda os dois blocos de mapa do usuário: o da classe (`livro` → `book`) e o do estilo (`coppedegree`). Um mapa no preâmbulo do aluno não apaga o da classe |
| #142 periódico corrente | programa (biblatex) + gabarito | `ufrj.dtx` 7729 `\renewcommand*{\bibdaterangesep}{/}` [bbx]; a entrada m-4231 de `tests/adversativa/referencias-manual.bib` | nada |
| #143 filme e jogo | programa (biblatex) | `ufrj.dtx` 7608–7609 `director`/`producer` como lista literal [dbx]; 7947–7950 `\printlist`; 7961 `version` depois da imprenta em `ufrj:mediadriver` [bbx] | nada |
| #144 entidade com órgão subordinado | programa (biblatex) + documentação + dados | `ufrj.dtx` 7717 `\ufrj@ucfamily` [bbx]; a chamada no `ufrj.cbx`; exemplo em `exemplo.bib` (ver #149) | decisão de 16/09 no comentário da issue |
| #145 intervalo de páginas | programa (biblatex) | `ufrj.dtx` [bbx]: `\bibrangedash` nunca redefinido | nada |
| #146 mês no idioma da publicação | programa (biblatex) | `ufrj.dtx` 7730–7733 `\ufrj@abntdate` usa o `\mkbibmonth` do idioma do documento [bbx] | nada |

### Exemplos, Norma COPPE e ferramentas

| Issue | Tipo | Onde, no `goufrj` | O que a 5.0 muda |
|---|---|---|---|
| #147 m-diss | **dados** | `ufrj.dtx` 9453–9464 [tiposbib] → `exemplo.bib`: `type = "Memória Social e Documento"`, sem `mscdiss` e sem `course`; a mesma chave em `tests/adversativa/referencias-manual.bib` 415 | nada |
| #148 ordem das listas | **dados** + ferramenta + documentação | `ufrj-coppe.dtx` 442–451 [maxexemplo] → `max-exemplo.tex`; `src/manual.tex` 133–140; `tools/geradocvazio.py` 238–242; Norma §10: `NORMA_COPPE_2026.md` 219 e `.tex` 292 | o `max-exemplo` sai do **`ufrj-coppe.dtx`**, e não mais do `.dtx` da classe |
| #149 conteúdo dos exemplos | **dados**, com uma exceção de programa | `ufrj-coppe.dtx` [maxexemplo]: algoritmos sem `\source` em 1301–1326 (no `max-exemplo.tex`, fecham em 1107 e 1122, as linhas 1104 e 1119 da 4.1); "Cientifico", "Fundacao", "Amparo a Pesquisa" em 363–366; capítulo "Using BibLaTeX" em 1033; "Alguns outros exemplo úteis" em 1209; abreviaturas de teste em 1630–1633; "Truques de `\LaTeX`" em 1567; palavras-chave em 348, 1765 [minexemplo] e 2034–2035 [examplept]; `tools/geradocvazio.py` 356–364. `ufrj.dtx` [examplebib/tiposbib]: `norma-example` 8875 × `m-norma` 9466; `jornalcaderno-example` 8910 × `m-4236` 9163; `{Brasil. Supremo Tribunal Federal}` 8935; `manualbib` 8951 | 1) **"como no algoritmo 6.1" não é texto do exemplo**: sai de `\autoref`, com o `\algorithmautorefname` minúsculo que o `algorithm2e` define, e a legenda diz "Algoritmo". A correção é de programa, na classe. 2) O `manualbib` com "9.ª ed., 2025" **também está no `ufrj.bib`**, a base do manual da classe (`ufrj.dtx` 9021 [ufrjbib]), e a issue não cita. 3) `\LaTeX` num título em caixa alta é dado do exemplo, mas todo aluno vai escrever: vale a classe proteger |
| #150 travessão × meia-risca | programa + documentação | `ufrj.dtx` 3916 `labelsep=endash`, 4954 `\SetAlgoCaptionSeparator`, 3687 e 3700 `\textendash` nos títulos de apêndice, 3711/3714 `\ufrj@tocapp`/`\ufrj@tocanx`, 6380 `--` na referência do resumo [class]; Norma §12 em `NORMA_COPPE_2026.md` 238 | nomes; os apelidos do estilo acompanham |
| #151 a prova não roda os verificadores | ferramenta | `tools/painel.py` 239–240 (`acao_conferir`); `tools/build-check.ps1` 345 (só `conferir-manual`) | o `r89` vira `rt89` |
| #152 LuaLaTeX com T1 | programa | `ufrj.dtx` 3546 `\RequirePackage[T1]{fontenc}` **fora** do `\ifPDFTeX` de 3528 [class] | o colofão informa `lmss/T1`, e o `r30` cobra |
| #153 folha única | documentação | `ufrj.dtx` 1651 e 1709–1710 [doc], 4331 e 6457 (comentários do código); `src/manual.tex` 464 (e 1125, "cada um em uma folha", que vale conferir); `tests/regressivo/r16-resumo-sem-referencia.tex` 3; Norma §8 em `NORMA_COPPE_2026.md` 202 e `.tex` 274 | as linhas da issue (~1618…) são de um `coppe.dtx` já corrigido em parte; no `b8103c7` são 1607, 1665, 5875 e 7891 |

## 5. Decisões que continuam abertas

| Decisão | Issue | Nota |
|---|---|---|
| Folhas de identidade num idioma só: (A) português ou (B) idioma principal | #128 | na 5.0, (B) é escrever a chave `natureza` por idioma |
| "(COPPE)" na capa, ou tirar da Norma | #129 | uma linha do estilo |
| Logotipos na folha de rosto | #130 | regra da UFRJ (classe) × escolha da unidade (mecanismo que não existe) |
| Travessão ou meia-risca | #150 | vale para legenda, listas, apêndice, sumário e resumo |
| Folha única do resumo | #153 | (A) corrigir a documentação |
| `pdfa` por padrão | #124 | já no `TODO.md` |
| Chamada de entidade: converter ou `shortauthor` | #144 | |
| Rótulo da lista numérica | #140 | |
| A 5.0 vai à CPGP no lugar da 4.1? | — | `PROPOSTA_CPGP.md` e `CARTA_CPGP.md` falam da classe `coppe` 4.1 |

## 6. O que a ferramenta não faz

- Não decide conflito em código que a 5.0 reescreveu: a abertura do resumo, a
  capa, a natureza e os logotipos. Esses trechos são poucos e aparecem como
  PENDENTE.
- Não reescreve teste que cobra texto da COPPE num documento sem o estilo.
- Não corrige issue: só traz a conferência para a 5.0 com os nomes certos.
- Foi testada numa simulação, e não no commit real da conferência, que ainda
  não existe no GitHub. A simulação teve testes novos em `.tex` e em `.py`,
  correção na classe, na documentação, no `max-exemplo` e no `tiposbib`, mudança
  no `painel.py` e no README do regressivo, gerados e PDF refeitos. O resultado:
  - **Conflitos:** os quatro foram resolvidos sozinhos.
  - **Regeração:** os `.ins` rodaram sem erro.
  - **Testes:** viraram `rt`, e os `.py` compilam.
  - **Sobras:** nenhuma.
