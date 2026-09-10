# Revisão adversativa

Doze documentos que existem para quebrar a classe. Quatro tipos — exame de
qualificação de mestrado, exame de qualificação de doutorado, dissertação e
tese — em três idiomas de redação — português, inglês e espanhol.

Cada um aciona **ao mesmo tempo** o máximo que a classe oferece: os cinco
níveis de seção, os cinco tipos de ilustração com legenda acima e fonte
abaixo, as três listas próprias da COPPE, a citação longa, as siglas, os
símbolos, as abreviaturas, o índice remissivo, a bibliografia, os apêndices e
os anexos, o colofão. Um documento real raramente usa metade disso; a ideia
aqui é que qualquer interação entre duas partes da classe apareça.

Nada aqui é escrito à mão: `tools/mk-adversativa.py` gera os doze. Para mudar
o que eles exercitam, mude o gerador e rode-o de novo a partir da raiz do
repositório.

**Nada aqui é distribuído, e nada aqui sai do `coppe.dtx`.** Esta pasta prova
que a classe funciona; não faz parte dela. Só os `.tex` e este README entram no
git — os 24 PDFs e os auxiliares são produto de build.

## Por que doze, e não um

Um documento só não serviria. A classe tem opções que se excluem entre si — não
dá para ser `twoside` e `oneside` ao mesmo tempo, nem pedir a ficha de rascunho
e a ficha real no mesmo arquivo — e tem quatro tipos de trabalho que produzem
folhas de rosto e de aprovação diferentes, e três idiomas que trocam todos os
textos fixos e o pacote de hifenização.

Doze é o menor número que cobre isso: quatro tipos vezes três idiomas. Cada uma
das doze casas dessa matriz recebe, além do seu tipo e do seu idioma, uma
combinação diferente de opções e um tamanho diferente de banca, de modo que
nenhuma opção fique sem prova e nenhuma combinação se repita.

## Cada arquivo, e o que ele está provando

A coluna "Banca" conta orientadores mais coorientador mais examinadores, que é
o que aparece na folha de aprovação. Os três degraus do espaçamento dessa folha
— até cinco membros, seis, e sete ou mais — estão todos representados, porque
sete era o tamanho em que a folha transbordava para uma segunda página.

### Exames de qualificação de mestrado

| Arquivo | O que só ele prova |
|---|---|
| `adv_mscexam_pt` | O tipo `mscexam` em português, que é o caso mais comum do repositório. Leva `twoside` e `doublespacing` juntos: é a única combinação em que a margem espelhada e o espaço duplo disputam a mesma página. Banca de 4, o degrau curto do espaçamento. Ficha de rascunho. Traz a prova de referências do Manual. |
| `adv_mscexam_en` | O mesmo tipo em inglês, com o sistema de chamada numérico (`numbers`) e a ficha catalográfica **real**, incluída de um PDF externo. Banca de 6, o degrau do meio. |
| `adv_mscexam_es` | O mesmo tipo em espanhol, que é o idioma que obriga a classe a compor **três** resumos: espanhol, inglês e português. Banca de 7, o degrau alto, na página mais curta de todas — a do exame de qualificação, que não tem folha adicional. |

### Exames de qualificação de doutorado

| Arquivo | O que só ele prova |
|---|---|
| `adv_dscexam_pt` | O tipo `dscexam` em português, com `numbers` e `twoside` juntos e a ficha real. Banca de 7 no degrau alto. Traz a prova de referências do Manual, agora no sistema numérico sobre a mesma bibliografia que o documento em autor-data usa: é o par que mostra que os dois sistemas leem a mesma base. |
| `adv_dscexam_en` | O mesmo tipo em inglês, com `doublespacing` e ficha de rascunho. Banca de 5. |
| `adv_dscexam_es` | O mesmo tipo em espanhol, e o **único** dos doze que pede `comserifa`. Desde a v4.1 a classe compõe sem serifa por padrão, e o caminho da serifa precisa de prova num documento grande, não só no teste de regressão. Banca de 6, com `numbers` e ficha real. |

### Dissertações

| Arquivo | O que só ele prova |
|---|---|
| `adv_msc_pt` | O tipo `msc` em português, com `twoside` e ficha de rascunho. Banca de 6. Traz a prova de referências do Manual. |
| `adv_msc_en` | O único que pede `listasnosumario`, que põe as listas pré-textuais dentro do sumário. E o de **banca maior**, com 8 membros, que é o teto que a folha de aprovação tem de aguentar. Ficha real e `numbers`. |
| `adv_msc_es` | O mesmo tipo em espanhol, com `doublespacing` e ficha de rascunho, e banca de 5. É o espanhol com espaço duplo, combinação que ninguém escreveria por acaso. |

### Teses

| Arquivo | O que só ele prova |
|---|---|
| `adv_dsc_pt` | **O documento extremo da suíte.** Além de tudo o que os outros fazem, ele leva mais de um exemplo em cada lista, índice remissivo com subentradas e remissivas, glossário pós-textual, um apêndice com tabela longa que atravessa folhas e um anexo com PDF externo incluído por `pdfpages`. Os outros onze ficam enxutos de propósito: eles cobrem a matriz, e um documento gigante em cada um deles só faria a prova demorar. Banca de 5, `numbers`, `twoside` e ficha real. |
| `adv_dsc_en` | A tese em inglês, com ficha de rascunho e banca de 7, o degrau alto na página mais longa. |
| `adv_dsc_es` | A tese em espanhol, com `numbers`, ficha real e **banca de 8**, o outro caso de teto. É o mais pesado dos doze depois do `adv_dsc_pt`. |

## O que todos os doze têm em comum, e por quê

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

Os doze programas são diferentes, para que a tabela de departamentos em UTF-8
saia inteira pelo menos uma vez. Os quatro documentos em português carregam a
prova de referências, com as 34 categorias da seção 4.2 do Manual, porque os
dados são os exemplos do próprio Manual e são em português.

## `_writes_probe.tex`

Não é um dos doze: é uma sonda. Compila com `semmorewrites` só para registrar,
no `RESULTADO.txt`, quantos dos 16 fluxos de escrita do pdfTeX cada parte
consome — a classe, cada pacote do autor, cada lista. Serve para que a conta
volte a ser mensurável quando alguém acrescentar um pacote e o teto voltar a
apertar. Não gera PDF que interesse a ninguém.

## Como rodar

Junto com o resto da prova de funcionamento, que é como isto deve ser rodado
antes de marcar uma versão:

```powershell
.\tools\prova.ps1
```

Ou sozinho:

```powershell
.\tools\build-check.ps1 -Scope adversativa
```

O ciclo é completo, e é o único do harness que roda o **makeindex** das listas
de abreviaturas e de símbolos e do índice remissivo — sem isso essas listas
saem vazias ou desatualizadas, que é justamente o erro que os alunos cometem.
Cada documento é compilado **duas vezes, nos dois motores**: pdfLaTeX e
LuaLaTeX, este último com `-jobname` próprio, de modo que os 24 PDFs convivem e
o veraPDF julga os 24.

## O que não está aqui

Não há teste de `numeraisromanos`: a opção contraria a 2.7 do manual e existe
só para que documentos escritos sob a norma antiga continuem compilando.
Exercitá-la num documento adversativo produziria um PDF que a norma vigente
rejeita, o que confundiria a leitura dos resultados.

Não há mais teste de `assinaturas`. A opção deixou de fazer efeito na v4.1: com
a entrega só digital, a folha de aprovação não tem mais linhas de assinatura.
