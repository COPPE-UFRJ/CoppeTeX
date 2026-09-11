<!-- AVISO-CPGP:INICIO — apagar deste comentário até AVISO-CPGP:FIM depois da aprovação -->
> ## ⚠️ Versão nova, ainda não aprovada
>
> **Esta é a CoppeTeX 4.1, e ela ainda não foi aprovada.** Vai à próxima reunião
> da Comissão de Programas de Pós-Graduação (CPGP) da COPPE/UFRJ. Use-a para
> escrever e para experimentar, mas confirme com a secretaria do seu Programa
> antes de depositar um trabalho com ela.
<!-- AVISO-CPGP:FIM -->

# CoppeTeX — a entrega

**Esta pasta é tudo o que você precisa para escrever uma tese, e nada além
disso.**

Se você é aluno da COPPE e veio escrever um trabalho, **baixe só esta pasta** e
pode ignorar o resto do repositório. O que está fora daqui é fonte comentada,
testes, documentos de prova e ferramentas de quem mantém a classe — útil para
quem vai mexer nela, inútil para quem vai usá-la.

> Este README é **diferente** do da raiz e do de `src/`. O da raiz apresenta o
> projeto e a proposta levada à CPGP; o de `src/` é o guia de programação. Este
> aqui é o **guia de instalação e uso**, e é o único que interessa a quem só
> quer escrever.

## Os arquivos que têm de estar aqui

São **31**, mais este README: 32 arquivos ao todo. Se faltar algum, a pasta
está incompleta — refaça a cópia com `coppetex.bat --dist` a partir da raiz do
repositório, ou baixe o pacote da entrega de novo.

### A classe e o que ela carrega — 19 arquivos

| Arquivo | Para que serve |
|---|---|
| `coppe.cls` | A classe. É o arquivo que o seu documento carrega. |
| `coppe.dbx`, `coppe.bbx`, `coppe.cbx` | O estilo de bibliografia e de citação, em autor-data. |
| `coppe-numeric.bbx`, `coppe-numeric.cbx` | O mesmo, no sistema numérico, usado pela opção `numbers`. |
| `brazilian-coppe.lbx`, `english-coppe.lbx`, `spanish-coppe.lbx`, `french-coppe.lbx`, `italian-coppe.lbx` | Os termos de bibliografia em cada idioma. |
| `coppe-lang-spanish.def`, `coppe-lang-french.def`, `coppe-lang-italian.def` | Os textos fixos da classe — rótulos, meses, capa — nesses três idiomas. Português e inglês vêm dentro da própria classe. |
| `coppe.ist` | O estilo de ordenação da lista de abreviaturas, da lista de símbolos e do índice. |
| `latexmkrc` | A receita de compilação, para quem usa `latexmk` ou o Overleaf. |
| `coppe-logo.pdf`, `coppe-logo.eps`, `ufrj-logo.pdf` | Os logotipos da capa e da folha de rosto. |

### Os manuais — 3 arquivos

| Arquivo | O que é |
|---|---|
| `coppe.pdf` | **O manual da classe.** Todos os comandos, todas as opções, com exemplos. Comece por ele. |
| `manual.pdf` | **O manual da norma.** O que o trabalho tem de ser — margens, estrutura, ilustrações, citações, referências — segundo o Manual da UFRJ/SiBI e as decisões da COPPE. Ele é, ele mesmo, a demonstração: foi composto com a classe e obedece a tudo o que enuncia. |
| `coppe-quickref.pdf` | Uma referência rápida de uma tabela só, em inglês: comando, exemplo, onde se usa. Para consultar sem abrir o manual. |

### Um exemplo por idioma — 8 arquivos

O art. 57 da Resolução CEPG n. 302/2024 admite **português, inglês ou
espanhol**. Há um exemplo para cada um.

| Arquivo | O que é |
|---|---|
| `example.tex`, `example.pdf` | **O exemplo completo, em português.** Um trabalho inteiro, comentado linha a linha. É por onde quase todo mundo começa. |
| `example_en.tex`, `example_en.pdf` | O mesmo modelo com o inglês como idioma principal. |
| `example_es.tex`, `example_es.pdf` | Com o espanhol como idioma principal — o caso em que a classe compõe **três** resumos: espanhol, inglês e português. |
| `example.bib`, `coppe.bib` | As bases de referências que os exemplos usam. `example.bib` traz um exemplo de **cada tipo** de referência da seção 4.2 do Manual. |

Francês e italiano **não** têm exemplo aqui, embora os pacotes de idioma deles
estejam na lista acima. Eles existem como demonstração do mecanismo de extensão
a outros idiomas; não há respaldo normativo para redigir uma tese neles.

### A licença — 1 arquivo

`COPYING`, a GNU General Public License versão 3.

## Instalação

O caminho mais curto é **não instalar nada**: copie estes arquivos para a pasta
do seu trabalho e compile ali. No Overleaf é igual — suba os arquivos junto com
o seu `.tex`.

Para instalar de vez, ponha os arquivos na árvore local do seu TeX, em
`tex/latex/coppe`, e mande o sistema reindexar (`texhash` no TeX Live,
`initexmf --update-fndb` no MiKTeX).

## Como compilar

São três passadas mais o `biber`, porque as referências cruzadas e a
bibliografia só se acomodam na terceira:

```
pdflatex example
biber example
pdflatex example
pdflatex example
```

Com `latexmk` e o `latexmkrc` desta pasta, uma linha basta:

```
latexmk -pdf example
```

Um trabalho que pede todas as listas ao mesmo tempo pode esbarrar no limite de
16 fluxos de escrita do pdfTeX. A classe resolve isso sozinha quando o pacote
`morewrites` está instalado; se não estiver, instale-o ou compile com
`lualatex`, que não tem esse limite.

## O primeiro documento

Abra `example.tex` — ou `example_en.tex`, ou `example_es.tex`, conforme o idioma
em que vai escrever. Ele traz, comentado linha a linha, tudo o que a classe
oferece: capa, folha de rosto com linha de pesquisa, folha da Coleta CAPES,
ficha catalográfica, folha de aprovação, os resumos, todas as listas
pré-textuais, os cinco níveis de seção, os flutuantes com legenda acima e fonte
abaixo, as citações, os apêndices e os anexos.

Troque o conteúdo e apague o que não usar. Se algo não estiver claro,
`coppe.pdf` explica o comando e `manual.pdf` explica a regra.

## Antes de depositar

Ligue a opção `pdfa`, que produz o **PDF/A-2b** exigido pelo item 2.2(d) do
Manual, e inclua a ficha catalográfica de verdade, gerada em
<http://fichacatalografica.sibi.ufrj.br/> ou pedida à biblioteca do seu
Programa:

```latex
\documentclass[dsc,pdfa]{coppe}
...
\fichacatalografica{ficha.pdf}
```

A lista de verificação completa está no fim do `manual.pdf`.

## Se der problema

Pegue a última versão em <https://github.com/COPPE-UFRJ/CoppeTeX>, atualize a
sua instalação do LaTeX, e, se ainda assim não funcionar, abra uma *issue* lá.
O capítulo de solução de problemas do `coppe.pdf` cobre os casos comuns.

## Licença

GNU General Public License, versão 3. O texto está em `COPYING`.
