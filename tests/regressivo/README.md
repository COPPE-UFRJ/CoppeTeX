# `tests/regressivo/` — um teste para cada defeito que já aconteceu

Esta pasta **não roda na suíte normal**. Ela existe para responder a uma
pergunta diferente.

A primeira camada, em [`tests/`](../README.md), pergunta *a classe compila?* —
o veredito é o código de saída do `pdflatex`. Esta camada pergunta *aquele
defeito voltou?*, e para isso o código de saída não basta: quase todos os
defeitos desta lista **compilavam com zero**. Saíam errado e ninguém via.

Cada arquivo aqui é a **menor reprodução possível de um defeito real**, com o
defeito descrito no cabeçalho e a cobrança declarada em seguida. Um teste que
compila e sai errado **falha**.

## Como rodar

```bash
python tests/regressivo/run-regressivo.py
```

```bash
python tests/regressivo/run-regressivo.py r05 r09
```

O filtro é qualquer pedaço do nome. `--manter` deixa os arquivos intermediários
para você olhar; sem ele fica só o PDF, que é o que se abre quando um teste
falha. Pelo painel: `coppetex.bat --regressivo`.

Precisa do `pdflatex`, do `lualatex` (um teste), do `biber`, do `makeindex` e do
`pdftotext`. Sem o `pdftotext` as cobranças de texto são **puladas com aviso** —
nunca aprovadas em silêncio.

## Como escrever um teste novo

Quando um defeito for corrigido, o teste entra aqui **no mesmo commit da
correção**. Copie o menor arquivo que reproduza o problema, escreva o cabeçalho
e pronto:

```latex
%% BUG: uma linha dizendo o que acontecia antes, e por quê.
%% ESPERA-TEXTO: o que tem de sair
%% NAO-ESPERA-TEXTO: o que não pode sair
\documentclass[dsc]{coppe}
...
```

As diretivas aceitas estão no cabeçalho do
[`run-regressivo.py`](./run-regressivo.py). Em resumo:

| Diretiva | Cobra |
|---|---|
| `MOTOR:` | `pdflatex` (padrão) ou `lualatex` |
| `PASSADAS:` | quantas vezes compilar (padrão 2) |
| `BIBER:` / `MAKEINDEX:` | rodar o passo entre as passadas |
| `ESPERA-FALHA:` | a compilação **tem** de falhar |
| `ESPERA-TEXTO:` / `NAO-ESPERA-TEXTO:` | o texto do PDF inteiro |
| `ESPERA-TEXTO-PAGINA:` / `NAO-...` | `<folha>::<texto>` |
| `ESPERA-LOG:` / `NAO-ESPERA-LOG:` | o `.log` |
| `ESPERA-PAGINAS:` | o número exato de folhas |
| `ESPERA-ARQUIVO:` / `NAO-...` | `<ext>::<texto>` num auxiliar (`.aux`, `.toc`, `.xmpdata`…) |
| `ESPERA-BYTES:` | os bytes crus do PDF (`/ID`, `pdfaid`…) |

As cobranças de texto comparam **sem acento, sem caixa alta e com o espaço
reduzido a um espaço só**. Não é desleixo: a mesma frase sai com quebra de linha
num PDF e com espaço em outro, o travessão vira `-` ou `--` conforme a fonte, e
o `pdftotext` do Xpdf e o do poppler discordam nos dois. Quem precisar cobrar a
caixa alta cobra pelo `.log` ou por um auxiliar, onde o texto está como o LaTeX
o escreveu.

**Cuidado com uma armadilha**, que pegou três destes testes enquanto eram
escritos: se o título do documento de teste repetir as palavras que a cobrança
procura, a cobrança acha o título e não o que se queria provar. Dê ao teste um
título que não tenha nada a ver com o que ele cobra, e cobre **por folha**
sempre que o defeito for de uma folha só.

## O que cada arquivo guarda

### A classe

| Arquivo | O defeito |
|---|---|
| `r01-flutuante-do-autor` | `\newcoppefloat` embrulhava o `\newfloat` num grupo; como o `\newfloat` define o ambiente localmente, o flutuante do autor sumia ao fechar o grupo. A lista também saía sem número e sem pontilhado. |
| `r02-capa-espaco-duplo` | Com `doublespacing` a capa transbordava para uma segunda folha, e a folha de sobra saía **numerada** na parte pré-textual, o que a 2.7 proíbe. |
| `r03-folha-aprovacao-oito` | A folha de aprovação com sete ou mais membros transbordava, e o `\thispagestyle` valia só para uma folha: a de sobra vinha numerada. Oito é o teto. |
| `r04-sumario-dois-digitos` | O `\@dottedtocline` dá ao número uma caixa de largura fixa; indicativos como `10.10.10.10` estouravam a caixa em até 4,6 mm e passavam **por cima** do título. A coluna passou a ser medida e viaja no `.aux`. |
| `r05-ponto-sumario-espanhol` | Com o espanhol como idioma principal, o babel punha um ponto no indicativo do sumário: `1.1. SECCIÓN` no sumário e `1.1 SECCIÓN` no título. |
| `r06-escrita-espanhol` | Documento em espanhol morria com `Unbalanced write command`: os rótulos da ficha passavam pelo `\@roman`, que o babel-espanhol redefine para versalete. |
| `r07-glossario-depois-dos-simbolos` | O `\renewcommand\glossaryname` do `\printlosymbols` ficava fora do grupo, e o Glossário pós-textual saía intitulado "Lista de Símbolos". |
| `r08-todas-as-listas` | O TeX tem dezesseis fluxos de escrita; um trabalho que pede **todas** as listas precisa de dezessete. Morria com `No room for a new \write`. |
| `r09-listas-sem-folio` | As listas de abreviaturas e de símbolos saíam com número de folha e pontilhado. A 4.1.1 pede o termo e o significado, e não pede localização nenhuma. |
| `r10-data-a-ser-determinada` | Sem `\dataaprovacao` a folha desenhava uma régua para preencher à mão. Ninguém escreve num PDF. |
| `r11-orientador-fora-da-banca` | A folha de aprovação listava sempre os orientadores, sem como tirar. Ela registra quem **examinou**. |
| `r12-orientador-examina` | O outro lado: a opção `orientadorexamina` põe o orientador de volta, à frente dos examinadores. |
| `r13-xmp-do-documento` | A opção `pdfa` nunca tinha sido compilada num documento de verdade: o `.xmpdata` era escrito antes de `\title` existir. |
| `r14-id-no-lualatex` | O LuaTeX renomeou `\pdfsuppressptexinfo` e ampliou o alcance dele: `-1` suprimiria também o `/ID` do trailer, que o PDF/A **exige**. |
| `r15-referencia-no-resumo` | A 3.1.2.1.4 sugere, e os Anexos E e F mostram, o resumo antecedido pela referência do trabalho. A classe não imprimia nenhuma. |
| `r16-resumo-sem-referencia` | O outro lado: `resumosemreferencia`, para o resumo que já está no limite das 500 palavras. |
| `r17-folio-so-na-parte-textual` | A contagem começava na Introdução, que saía como folha 1. A 2.7 manda contar da folha de rosto e **não** contar a folha adicional. |
| `r18-legenda-em-cima-fonte-embaixo` | A legenda ficava embaixo, como no `\caption` padrão. A norma põe a legenda em cima e a fonte, obrigatória, embaixo. |
| `r19-linha-de-pesquisa-no-idioma` | O rótulo da linha de pesquisa estava fixo em português num trabalho em inglês. |
| `r20-folha-adicional-capes` | A folha adicional do Anexo H não existia; depois existiu com parágrafos soltos e pontilhado, em vez da moldura fechada do modelo. |
| `r21-tratamento-e-instituicao` | `\advisor` e `\examiner` pediam o tratamento como obrigatório e a instituição como opcional. A 3.1.2.1.3(e) pede o contrário. |
| `r22-nivel-quinario` | A 2.6 admite até a seção quinária, e a classe parava na quaternária. |

### As ferramentas

Defeito de ferramenta merece teste igual. Um verificador que aprova tudo é pior
que verificador nenhum, porque parece que alguém conferiu.

| Arquivo | O defeito |
|---|---|
| `r90-log-de-uma-passada` | Os verificadores liam só o trecho do `.log` depois do **último** `LaTeX2e <`, achando que o arquivo guardasse várias passadas. Não guarda: o que aparece duas vezes é o banner, que o LaTeX repete no fim. O corte jogava fora o corpo da passada — onde estão os avisos — e o verificador passou a aprovar qualquer coisa. |
| `r91-logotipo-ausente` | Quem copiava só o `coppe.cls` recebia `File 'coppe-logo' not found`, sem pista de que o arquivo vem com a classe. |
