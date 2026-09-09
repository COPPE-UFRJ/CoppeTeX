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

## O que cada um exercita além do comum

As opções e os tamanhos de banca variam de propósito, de modo que a matriz
cubra o espaço todo — inclusive os três degraus do espaçamento das
assinaturas (até 5 membros, 6, e 7 ou mais).

| Documento | Tipo | Idioma | Programa | Banca | Opções extras |
|---|---|---|---|---|---|
| `adv_mscexam_pt` | mscexam | português | PESC | 4 | twoside, doublespacing, rascunhoficha |
| `adv_mscexam_en` | mscexam | inglês | PEB | 6 | numbers, ficha real |
| `adv_mscexam_es` | mscexam | espanhol | PEC | 7 | rascunhoficha |
| `adv_dscexam_pt` | dscexam | português | PEE | 7 | numbers, twoside, ficha real |
| `adv_dscexam_en` | dscexam | inglês | PEM | 5 | doublespacing, rascunhoficha |
| `adv_dscexam_es` | dscexam | espanhol | PEMM | 6 | numbers, ficha real |
| `adv_msc_pt` | msc | português | PEN | 6 | twoside, rascunhoficha |
| `adv_msc_en` | msc | inglês | PENO | 8 | numbers, listasnosumario, ficha real |
| `adv_msc_es` | msc | espanhol | PEP | 5 | doublespacing, rascunhoficha |
| `adv_dsc_pt` | dsc | português | PEQ | 5 | numbers, twoside, ficha real |
| `adv_dsc_en` | dsc | inglês | PET | 7 | rascunhoficha |
| `adv_dsc_es` | dsc | espanhol | PPE | 8 | numbers, ficha real |

Os doze levam `pdfa`, `assinaturas` e `coorientador`. Os doze programas são
diferentes, para que a tabela de departamentos em UTF-8 saia inteira pelo
menos uma vez. Os documentos em espanhol carregam os três resumos, com o
`brazilianabstract` que só existe para esse caso.

## Como rodar

```powershell
.\tools\build-check.ps1 -Scope adversativa
```

O ciclo é completo, e é o único do harness que roda o **makeindex** das
listas de abreviaturas e de símbolos e do índice remissivo — sem isso essas
listas saem vazias ou desatualizadas, que é justamente o erro que os alunos
cometem. Depois, `-Scope pdfa` (ou `all`) passa cada um dos doze PDFs pelo
veraPDF, já que todos são compilados com a opção `pdfa`.

## O que não está aqui

Não há teste de `numeraisromanos`: a opção contraria a 2.7 do manual e existe
só para que documentos escritos sob a norma antiga continuem compilando.
Exercitá-la num documento adversativo produziria um PDF que a norma vigente
rejeita, o que confundiria a leitura dos resultados.
