# Revisão adversativa

> **`src/coppe.dtx` é a fonte única da classe.** Os documentos desta pasta não
> saem dele — saem de `tools/mk-adversativa.py` — mas a classe que eles
> exercitam sai. Uma correção descoberta aqui vai para `src/coppe.dtx`, nunca
> para `src/coppe.cls`, que é regerado por cima. Veja
> [`../../src/README.md`](../../src/README.md).

Seis documentos que existem para quebrar a classe.

Cada um aciona **ao mesmo tempo** o máximo que a classe oferece: os cinco
níveis de seção, os cinco tipos de ilustração com legenda acima e fonte
abaixo, as três listas próprias da COPPE, a citação longa, as siglas, os
símbolos, as abreviaturas, o índice remissivo, a bibliografia, os apêndices e
os anexos, o colofão. Um documento real raramente usa metade disso; a ideia
aqui é que qualquer interação entre duas partes da classe apareça.

Nada aqui é escrito à mão: `tools/mk-adversativa.py` gera os seis. Para mudar o
que eles exercitam, mude o gerador — a matriz está no topo dele — e rode-o de
novo a partir da raiz do repositório.

**Nada aqui é distribuído, e nada aqui sai do `coppe.dtx`.** Esta pasta prova
que a classe funciona; não faz parte dela. Só os `.tex`, a base de referências
do Manual e este README entram no git; os PDFs e os auxiliares são produto de
build e ficam de fora.

## Por que seis, e por que estes seis

Eram doze — quatro tipos de trabalho vezes três idiomas — e o corte para seis
foi pelo relógio. Cada documento é compilado **duas vezes**, no pdfTeX e no
LuaTeX, com `biber`, dois `makeindex`, o índice remissivo e três ou mais
passadas, e depois validado pelo veraPDF. Doze faziam a prova demorar mais do
que alguém está disposto a esperar antes de marcar uma versão — e prova que
demora demais é prova que deixa de ser rodada, que é o pior resultado possível.

O corte **não foi uniforme**, e é aí que está a amostragem:

- o **português fica com quatro**, um de cada tipo de trabalho. É o idioma de
  quase todo trabalho da COPPE e o único em que os quatro tipos aparecem de
  verdade;
- **inglês e espanhol ficam com um cada**, e de tipos **diferentes**, para que a
  amostra cruze idioma com tipo em vez de repetir o mesmo par.

O que não podia sumir junto com os seis documentos era a cobertura das
**opções**. Por isso a matriz do gerador passou a ser explícita, e não mais
calculada por resto de divisão: dá para conferir com o dedo que nenhuma opção
ficou sem prova e que os três degraus do espaçamento da folha de aprovação
continuam representados.

## Cada arquivo, e o que ele está provando

A coluna **imprime** é quantos nomes a folha de aprovação realmente imprime: só
os examinadores, ou também os orientadores e o coorientador quando há
`orientadorexamina`. É esse número, e não o total de pessoas declaradas, que
decide o espaçamento da folha — e sete era o tamanho em que ela transbordava.

| Arquivo | Tipo, idioma | Opções próprias | Imprime |
|---|---|---|---|
| `adv_mscexam_pt` | Exame de mestrado, pt | `twoside` + `doublespacing` juntos — a única combinação em que a margem espelhada e o espaço duplo disputam a mesma página. Ficha de rascunho. | 4 (degrau curto) |
| `adv_dscexam_pt` | Exame de doutorado, pt | `numbers`, `semlinks` e `orientadorexamina`. O **único sem `\dataaprovacao`**: é o caso em que a folha tem de escrever "a ser determinada". | 7 (degrau alto, na folha mais curta — exame não tem folha adicional) |
| `adv_msc_pt` | Dissertação, pt | O **único com `comserifa`**. Desde a v4.1 a classe compõe sem serifa por padrão, e o caminho da serifa precisa de prova num documento grande. Ficha real. | 5 (o degrau original) |
| `adv_dsc_pt` | Tese, pt | **O documento extremo da suíte.** Além de tudo o que os outros fazem, leva mais de um exemplo em cada lista, índice remissivo com subentradas e remissivas, glossário pós-textual, apêndice com tabela longa que atravessa folhas e anexo com PDF externo incluído por `pdfpages`. Ficha real. | 6 (degrau do meio) |
| `adv_msc_en` | Dissertação, en | O **único com `listasnosumario`**, mais `numbers` e `orientadorexamina`. Ficha real. | **8 — o teto** que a folha tem de aguentar numa folha só |
| `adv_dscexam_es` | Exame de doutorado, es | `doublespacing` e ficha de rascunho. O espanhol é o idioma que obriga a classe a compor **três** resumos: espanhol, inglês e português. | 7, de novo na folha curta do exame |

Os outros cinco ficam enxutos ao lado do `adv_dsc_pt` de propósito: eles cobrem
a matriz de opções e de idiomas, e um documento gigante em cada um só faria a
prova demorar sem provar mais nada.

## O que todos têm em comum, e por quê

Todos pedem `pdfa` e `coorientador`, e **nenhuma opção de fluxo de escrita**, de
propósito. Acionar todas as listas ao mesmo tempo é exatamente o caso em que o
pdfTeX estoura os 16 `\write` de que dispõe, e o que se quer verificar é que a
classe resolve isso sozinha, no caminho padrão, sem o autor saber que o
problema existe.

Todos declaram a banca na forma da v4.1 — nome, sobrenome, titulação e
instituição, com o tratamento no argumento opcional. O primeiro orientador leva
tratamento e o segundo não, e um dos examinadores fica com a instituição em
branco: os três caminhos precisam de prova.

Todos chamam `\agenciafomento` **duas vezes**. O Anexo H pede "Agência(s)", e é
a segunda chamada que exercita a acumulação — uma só nunca a exercitaria.

Os seis programas são diferentes, para que a tabela de departamentos em UTF-8
saia por inteiro. Os quatro documentos em português carregam a **prova de
referências**, com as 34 categorias da seção 4.2 do Manual, porque os dados são
os exemplos do próprio Manual e são em português — e os quatro cobrem os dois
sistemas de chamada, autor-data e numérico, sobre a mesma base.

## `_writes_probe.tex`

Não é um dos seis: é uma sonda. Compila com `semmorewrites` só para registrar,
no `RESULTADO.txt`, quantos dos 16 fluxos de escrita do pdfTeX cada parte
consome — a classe, cada pacote do autor, cada lista. Serve para que a conta
volte a ser mensurável quando alguém acrescentar um pacote e o teto voltar a
apertar. Não gera PDF que interesse a ninguém.

## Como rodar

Junto com o resto da prova de funcionamento, que é como isto deve ser rodado
antes de marcar uma versão:

```powershell
.\coppetex.bat --prova
```

Ou só esta camada:

```powershell
.\coppetex.bat --adversativo
```
