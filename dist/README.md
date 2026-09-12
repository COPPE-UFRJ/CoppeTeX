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

Se você é aluno da COPPE e veio escrever um trabalho, **baixe só esta pasta** —
ou o `.zip` do *release*, que é a mesma coisa — e pode ignorar o resto do
repositório. O que está fora daqui é fonte comentada, testes, documentos de
prova e ferramentas de quem mantém a classe.

> Este README é **diferente** do da raiz e do de `src/`. O da raiz apresenta o
> projeto e a proposta levada à CPGP; o de `src/` é o guia de programação. Este
> aqui é o **guia de instalação e uso**, e é o único que interessa a quem só
> quer escrever.

## A regra da arrumação, em uma frase

**O que está na raiz funciona sem você mexer em nada. O que está numa subpasta
de idioma só funciona depois de você trazer o conteúdo dela para a raiz.**

Isso não é capricho: o LaTeX procura a classe, os estilos e as bases de
referências **ao lado do documento que está compilando**, e não dentro de
subpastas. Um arquivo que fique em `es/` é um arquivo que o LaTeX não vê.

| Pasta | O que é | O que fazer |
|---|---|---|
| **raiz** | A classe, os estilos de bibliografia e o **exemplo em português** | Nada. Já funciona. |
| `logos/` | Os três logotipos da capa | Nada. A classe procura aqui. |
| `manuais/` | Os PDFs para ler | Nada. São leitura. |
| `en/` | O exemplo em **inglês** | **Copie o conteúdo para a raiz** antes de usar |
| `es/` | O exemplo em **espanhol** e os arquivos que só ele precisa | **Copie o conteúdo para a raiz** antes de usar |
| `outraslinguas/` | Francês e italiano | **Copie para a raiz**, ciente de que não são idiomas admitidos para redigir tese |

## Vou escrever em português

É o caso de quase todo trabalho da COPPE, e não há nada a fazer. Copie **todos
os arquivos da raiz, mais a pasta `logos/`**, para a pasta do seu trabalho, abra
o `example.tex` e comece a trocar o conteúdo.

## Vou escrever em inglês

Copie o conteúdo de `en/` para a raiz, e depois a raiz inteira mais `logos/`
para a pasta do seu trabalho. O seu documento passa a ser o `example_en.tex`.

O `english-coppe.lbx` **já está na raiz**, e não em `en/`: toda tese da COPPE
tem um resumo em idioma estrangeiro, que por convenção é o inglês, e por isso
ele é necessário mesmo num trabalho escrito em português.

## Vou escrever em espanhol

Copie o conteúdo de `es/` para a raiz, e depois a raiz inteira mais `logos/`
para a pasta do seu trabalho. O seu documento passa a ser o `example_es.tex`.
São dois arquivos além do exemplo: o `spanish-coppe.lbx`, com os termos de
bibliografia, e o `coppe-lang-spanish.def`, com os textos fixos da classe.

Um trabalho em espanhol tem **três** resumos: espanhol, inglês e português. O
exemplo já vem com os três.

## E francês ou italiano?

Dá para compor, e a pasta `outraslinguas/` traz o que é preciso — mas **não há
respaldo normativo para redigir uma tese da COPPE nesses idiomas**. O art. 57 da
Resolução CEPG n. 302/2024 admite português, inglês e espanhol. Os dois pacotes
existem como demonstração do mecanismo de extensão a outros idiomas, e é por
isso que não há exemplo pronto para eles.

## Os arquivos, um a um

### Na raiz — a classe, os estilos e o exemplo em português

| Arquivo | Para que serve |
|---|---|
| `coppe.cls` | A classe. É o arquivo que o seu documento carrega. |
| `coppe.dbx`, `coppe.bbx`, `coppe.cbx` | O estilo de bibliografia e de citação, em autor-data. |
| `coppe-numeric.bbx`, `coppe-numeric.cbx` | O mesmo, no sistema numérico, usado pela opção `numbers`. |
| `brazilian-coppe.lbx`, `english-coppe.lbx` | Os termos de bibliografia em português e em inglês. **Os dois são necessários em qualquer trabalho**, por causa do resumo em idioma estrangeiro. |
| `coppe.ist` | O estilo de ordenação da lista de abreviaturas, da lista de símbolos e do índice. |
| `latexmkrc` | A receita de compilação, para quem usa `latexmk` ou o Overleaf. |
| `example.tex`, `example.bib`, `tipos.bib` | **O exemplo completo, em português**, comentado linha a linha, e as duas bases que ele cita. A `tipos.bib` traz uma entrada de **cada tipo** de referência da seção 4.2 do Manual. |
| `coppe.bib` | A base com as referências da própria classe e da norma. |
| `coppe.dtx`, `coppe.ins`, `manual.tex` | As **fontes** dos manuais. Não são necessárias para escrever; estão aqui para que a entrega baste também para refazer o manual e a classe. Não existe `coppe.tex`: o manual da classe é o próprio `coppe.dtx`, e quem o compõe é o `coppe.ins`. |
| `COPYING` | A licença, GNU GPL versão 3. |

### `logos/`

`coppe-logo.pdf`, `coppe-logo.eps` e `ufrj-logo.pdf`, os logotipos da capa e da
folha de rosto. A classe procura primeiro em `logos/` e depois ao lado do
documento, então funciona com a pasta ou sem ela.

### `manuais/`

| Arquivo | O que é |
|---|---|
| `coppe.pdf` | **O manual da classe.** Todos os comandos, todas as opções, com exemplos. Comece por ele. |
| `manual.pdf` | **O manual da norma.** O que o trabalho tem de ser — margens, estrutura, ilustrações, citações, referências. Ele é, ele mesmo, a demonstração: foi composto com a classe e obedece a tudo o que enuncia. |
| `coppe-quickref.pdf` | Uma referência rápida de uma tabela só, em inglês: comando, exemplo, onde se usa. |
| `example.pdf` | O exemplo em português, já compilado, para você ver o resultado antes de compilar. |

## Menos arquivos na sua raiz: os `.bib` podem ir para uma subpasta

A classe, os estilos e os logotipos têm de ficar onde estão — essa é a regra da
arrumação acima. Os **`.bib`, não**: eles podem morar numa subpasta, e é o que
recomendamos. Escreva o caminho, com barra para frente mesmo no Windows:

```latex
\addbibresource{referencias/minha-tese.bib}
```

Funciona no seu computador e funciona no Overleaf, e o nome da pasta é o que
você quiser. Quem lê o `.bib` é o **biber**, e ele abre o caminho relativo à
pasta do documento.

E é **mais** seguro que o nome sozinho, não menos. Um nome pelado passa pela
busca do LaTeX, que olha a sua pasta e também as pastas da instalação do TeX:
se o arquivo não estiver na sua pasta, o biber acha, **em silêncio**, o arquivo
de mesmo nome que veio na distribuição — e a sua tese sai com a bibliografia de
outra pessoa. Com a subpasta no caminho não há busca nenhuma: ou o arquivo está
ali, ou o biber para com `Cannot find`. Erro na cara é melhor que referência
errada na tese.

Só evite acento e espaço no nome da pasta.

## Instalação

O caminho mais curto é **não instalar nada**: copie os arquivos da raiz e a
pasta `logos/` para a pasta do seu trabalho e compile ali. No Overleaf é igual —
suba os arquivos junto com o seu `.tex`.

Para instalar de vez, ponha os arquivos na árvore local do seu TeX, em
`tex/latex/coppe`, e mande o sistema reindexar (`texhash` no TeX Live,
`initexmf --update-fndb` no MiKTeX). Nesse caso os logotipos ficam ao lado do
`coppe.cls`, e a classe os encontra do mesmo jeito.

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

Abra o exemplo do idioma em que vai escrever. Ele traz, comentado linha a linha,
tudo o que a classe oferece: capa, folha de rosto com linha de pesquisa, folha
da Coleta CAPES, ficha catalográfica, folha de aprovação, os resumos, todas as
listas pré-textuais, os cinco níveis de seção, os flutuantes com legenda acima e
fonte abaixo, as citações, os apêndices e os anexos.

Troque o conteúdo e apague o que não usar. Se algo não estiver claro,
`manuais/coppe.pdf` explica o comando e `manuais/manual.pdf` explica a regra.

Se preferir começar de uma folha em branco em vez de apagar o exemplo, o
repositório traz um gerador: **`coppetex-novo.bat`** abre uma janela que pergunta
os dados do trabalho e escreve o `.tex` e o `.bib` prontos, com os cinco
capítulos de sempre.

Ele tem uma opção que evita todo o trabalho desta seção: **Baixar a classe do
GitHub**. Marcada, ela traz para a mesma pasta a classe, os estilos, os pacotes
de idioma e os logotipos, e — se o trabalho não for em português — já poe na
raiz o conteúdo da pasta daquele idioma. A pasta fica pronta para compilar.

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

A lista de verificação completa está no fim do `manuais/manual.pdf`.

## Se der problema

Pegue a última versão em <https://github.com/COPPE-UFRJ/CoppeTeX>, atualize a
sua instalação do LaTeX, e, se ainda assim não funcionar, abra uma *issue* lá.
O capítulo de solução de problemas do `manuais/coppe.pdf` cobre os casos comuns.

**O erro mais comum desta versão** é compilar um exemplo sem ter trazido a pasta
do idioma para a raiz. O sintoma é `File 'coppe-lang-spanish.def' not found` ou
`Cannot find 'example.bib'`. Volte à regra da arrumação, no começo deste
arquivo.

## Licença

GNU General Public License, versão 3. O texto está em `COPYING`.
