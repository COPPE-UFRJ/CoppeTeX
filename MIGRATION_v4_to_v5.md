# Guia de migração — CoppeTeX 4.x → 5.0

Para quem escreve um trabalho com a CoppeTeX 4.0 ou 4.1 e vai atualizar os
arquivos da classe. Leia a tabela, faça o que ela mandar para o seu caso, e é
só isso.

A 5.0 não muda a forma do trabalho: **as folhas saem iguais**, exceto a frase do
colofão que diz com que classe o trabalho foi composto — agora "a classe ufrj,
do projeto CoppeTeX, versão v5.0". O que muda é a organização. A classe passa a se chamar `ufrj` e a implementar só o Manual da
UFRJ/SiBI, e tudo o que era da COPPE — o nome do Instituto, os treze
Programas, o logotipo, as frases que a Norma COPPE fixa — sai da classe e vai
para um **estilo de unidade**, o `ufrj-coppe`. É o que permite que outra
unidade da UFRJ use a classe escrevendo só o estilo dela.

*In English: CoppeTeX 5.0 renames the class to `ufrj` and moves everything that
belongs to COPPE into the unit style `ufrj-coppe`. A thesis started with
`\documentclass{coppe}` keeps compiling unchanged; the recommended form is
`\documentclass{ufrj}` followed by `\usepackage{ufrj-coppe}`.*

---

## Em uma tabela

| A sua situação | O que fazer |
|---|---|
| Trabalho da COPPE com `\documentclass[...]{coppe}` | **Nada no `.tex`.** Troque os arquivos da classe pelos da 5.0 — inclusive o `coppe.cls`, que agora é outro — e compile. O `.log` vai sugerir, uma vez, trocar duas linhas (seção 2). |
| Quer a forma nova, sem o aviso | Troque `\documentclass[...]{coppe}` por `\documentclass[...]{ufrj}` e acrescente `\usepackage{ufrj-coppe}` logo abaixo. Mais nada. |
| Trabalho de outra unidade da UFRJ | Use a classe sem estilo e declare o seu Programa no preâmbulo (seção 6), até a sua unidade ter um estilo. |
| Você escreveu um pacote de idioma | Renomeie os dois arquivos e o comando, e tire deles o que é institucional (seção 7). |

---

## 1. O que mudou de nome

Os arquivos que o seu trabalho usa:

| Até a 4.1 | Na 5.0 |
|---|---|
| `coppe.cls` | `ufrj.cls`, **mais** `ufrj-coppe.sty` |
| `coppe.bbx`, `coppe.cbx`, `coppe.dbx` | `ufrj.bbx`, `ufrj.cbx`, `ufrj.dbx` |
| `coppe-numeric.bbx`, `coppe-numeric.cbx` | `ufrj-numeric.bbx`, `ufrj-numeric.cbx` |
| `brazilian-coppe.lbx`, `english-coppe.lbx` e os demais | `brazilian-ufrj.lbx`, `english-ufrj.lbx` e os demais |
| `coppe-lang-spanish.def` e os demais | `ufrj-lang-spanish.def` e os demais |
| `coppe.ist` | `ufrj.ist` |
| `coppe.bib` | `ufrj.bib` |
| `manuais/coppe.pdf` | `manuais/ufrj.pdf` (a classe) e `manuais/ufrj-coppe.pdf` (o estilo da COPPE) |
| `manuais/coppe-quickref.pdf` | `manuais/ufrj-quickref.pdf` |

Os logotipos não mudam: `logos/ufrj-logo.pdf` e `logos/coppe-logo.pdf`.

Os arquivos antigos que ficarem na pasta do trabalho não atrapalham, com uma
exceção: o **`coppe.cls`**. O da 4.1 era a classe inteira; o da 5.0 é uma classe
de compatibilidade de poucas linhas. Se o antigo ficar, `\documentclass{coppe}`
continua carregando a 4.1. Substitua-o.

O mesmo vale para um **`latexmkrc`** antigo, que chama o `makeindex` com
`coppe.ist`: troque-o pelo da 5.0.

## 2. As duas linhas

Um trabalho escrito até a 4.1 começa assim:

```latex
\documentclass[dsc]{coppe}
```

Na 5.0 ele compila como está: o `coppe.cls` carrega a `ufrj` com as mesmas
opções, carrega o `ufrj-coppe`, e deixa no `.log` o aviso

```
Class coppe Warning: A classe coppe agora e a classe ufrj com o estilo
(coppe)              ufrj-coppe. Este documento compila como esta, ...
```

Para tirar o aviso, a forma recomendada é:

```latex
\documentclass[dsc]{ufrj}
\usepackage{ufrj-coppe}
```

As opções de classe são as mesmas, e todos os comandos do documento também. As
folhas saem idênticas nas duas formas.

## 3. Os nomes antigos continuam valendo

Os comandos que levavam o nome da classe ganharam o nome novo, e o antigo
continua funcionando sempre que o estilo `ufrj-coppe` está carregado — direto,
ou pelo `coppe.cls`:

| Nome antigo | Nome novo |
|---|---|
| `\coppetexfinalpage` | `\ufrjfinalpage` |
| `\newcoppefloat` | `\newufrjfloat` |
| `\usecoppelanguage` | `\useufrjlanguage` |
| `\copperdefstring`, `\coppestring`, `\coppemainstring`, `\coppeforeignstring` | `\ufrjdefstring`, `\ufrjstring`, `\ufrjmainstring`, `\ufrjforeignstring` |
| `\coppefinalengine`, `\coppefinalfont`, `\coppefinalsystem`, `\coppefinaltexsystem`, `\coppefinaltime`, `\coppefinalmanual` | `\ufrjfinalengine`, `\ufrjfinalfont`, `\ufrjfinalsystem`, `\ufrjfinaltexsystem`, `\ufrjfinaltime`, `\ufrjfinalmanual` |
| estilo de página `coppe` | estilo de página `ufrj` |
| campo `coppedegree` no `.bib` | campo `ufrjdegree` |

Um `\renewcommand\coppefinalsystem{}` escrito para tirar o nome da máquina do
colofão continua tirando.

## 4. Auxiliares de uma compilação anterior

A classe escreve nomes internos seus no `.toc` e nas listas de siglas e de
símbolos, e na 4.1 esses nomes começavam por `coppe@`. O estilo da COPPE os
reconhece, de modo que a primeira compilação depois da atualização lê os
auxiliares antigos sem erro e os reescreve.

Se ainda assim algo sair estranho na primeira compilação, apague os `.aux`,
`.toc`, `.lof`, `.lot`, `.bbl`, `.bcf`, `.lab`, `.los`, `.lsg` e `.lgs` e
compile de novo.

## 5. Um erro novo, que diz o que falta

Na 4.1, um `\department` com uma sigla que a classe não conhecia não dava erro
nenhum: a capa saía sem o nome do Programa, ou a compilação morria longe dali. Na
5.0 a sigla tem de ter sido declarada pelo estilo da unidade, e quando não foi a
compilação para em

```
! Class ufrj Error: Programa `PESC' nao declarado.
```

Quase sempre é o `\usepackage{ufrj-coppe}` que faltou.

## 6. Um trabalho de outra unidade da UFRJ

Sem estilo nenhum, a classe compõe o trabalho com os textos da UFRJ: a capa traz
a universidade e o "Programa de Pós-Graduação em…", o resumo diz que o
trabalho foi apresentado "à UFRJ", e o colofão cita o Manual do SiBI. O
Programa é declarado no preâmbulo:

```latex
\documentclass[dsc]{ufrj}
\ufrjdeclareprogram{PPGI}{Informática}{Informatics}
```

e escolhido, como sempre, com `\department{PPGI}`. Quando a sua unidade tiver o
seu estilo, a declaração sai e o `\usepackage` entra. Como escrever um estilo de
unidade está no [`CONTRIBUTING.md`](./CONTRIBUTING.md), e o modelo é o
`ufrj-coppe.dtx`.

## 7. Um pacote de idioma escrito por você

Se você escreveu um pacote para outro idioma, ele precisa de quatro ajustes:

1. `coppe-lang-<idioma>.def` passa a se chamar `ufrj-lang-<idioma>.def`, e
   `<idioma>-coppe.lbx`, `<idioma>-ufrj.lbx` — inclusive dentro do
   `\ProvidesFile` e do `\DeclareLanguageMapping`.
2. `\copperdefstring` passa a ser `\ufrjdefstring`.
3. As chaves `universityname`, `cityname`, `statename` e `countryname` saem:
   nenhum código as lia.
4. A chave `abstracttail` perde o começo. O "à COPPE/UFRJ" vai para a nova
   chave `tounit`, que no pacote é o valor sem unidade — "à UFRJ" no seu
   idioma —, e a `sciencename` ("em Ciências") sai do pacote, porque é do
   estilo da unidade. Os pacotes de espanhol, francês e italiano da 5.0 são o
   modelo.

## 8. Para quem mexe na classe

- A fonte são dois arquivos: `src/ufrj.dtx`, a classe, e `src/ufrj-coppe.dtx`,
  o estilo da COPPE, a classe `coppe` de compatibilidade e os exemplos. Cada um
  tem o seu `.ins` e o seu manual. O harness, o painel e os verificadores já
  conhecem os dois.
- **A classe não nomeia unidade nenhuma.** `tests/regressivo/rtu04` reprova
  qualquer menção à COPPE no código que o `ufrj.ins` gera, e `rtu01` compõe um
  trabalho sem estilo e cobra que nada da COPPE apareça no PDF.
- A interface entre a classe e o estilo é pública e está documentada no
  `ufrj.pdf`, na seção *A instituição e a unidade*: `\ufrjdeclareunit`,
  `\ufrjdeclareprogram`, `\ufrjdeclarelogos`, `\ufrjdeclarenorm` e
  `\ufrjdefunitstring`. `rtu02` prova que uma unidade inventada se escreve só com
  ela, e `rtu03` que um documento da 4.1 continua compilando.
- Os textos de uma unidade ficam numa tabela própria, que tem precedência sobre a
  dos pacotes de idioma, carregados antes ou depois.
- Três passos, cada um conferido contra imagens das páginas do estado anterior:
  o isolamento da COPPE dentro do `.dtx` (`22e7dc9`), a troca de nome
  (`fc0eb20`) e a separação em dois `.dtx` (`547bf45`).
