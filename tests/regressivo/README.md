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

O nome de cada teste começa por um prefixo que diz de onde ele veio:

| Prefixo | Origem |
|---|---|
| `r` | um defeito da classe até a 4.1, ou das ferramentas (`r90` em diante) |
| `rt` | a conferência contra o Manual UFRJ/SiBI 2026, feita no `master` (issue #112) — cada um falha até a issue dele ser corrigida |
| `rtu` | a classe `ufrj` e o estilo de unidade, da 5.0 |

O filtro por pedaço do nome continua valendo: `rtu` roda só os da 5.0, e `rt3`
roda os da conferência que começam por 3.

Precisa do `pdflatex`, do `lualatex` (um teste), do `biber`, do `makeindex` e do
`pdftotext`. Sem o `pdftotext` as cobranças de texto são **puladas com aviso** —
nunca aprovadas em silêncio.

**O `pdftotext` e o `pdftohtml` têm de ser os do poppler.** Os testes de medida
usam `pdftotext -bbox`, que é opção do poppler; o `pdftotext` do Xpdf — o que o
Git for Windows instala em `mingw64\bin` — não a tem, e devolve uma saída sem
palavra nenhuma. Antes da guarda da #156 isso não dava erro: o teste passava
**sem medir nada**. No Windows com o Git instalado, o Git Bash acha o do Xpdf e
o PowerShell acha o do MiKTeX (poppler), então **rode a suíte pelo PowerShell**.
O rodador imprime as versões que achou antes do primeiro teste, e avisa quando
não são as do poppler.

## Como escrever um teste novo

Quando um defeito for corrigido, o teste entra aqui **no mesmo commit da
correção**. Copie o menor arquivo que reproduza o problema, escreva o cabeçalho
e pronto:

```latex
%% BUG: uma linha dizendo o que acontecia antes, e por quê.
%% ESPERA-TEXTO: o que tem de sair
%% NAO-ESPERA-TEXTO: o que não pode sair
\documentclass[dsc]{ufrj}
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
| `r01-flutuante-do-autor` | `\newufrjfloat` (antes `\newcoppefloat`) embrulhava o `\newfloat` num grupo; como o `\newfloat` define o ambiente localmente, o flutuante do autor sumia ao fechar o grupo. A lista também saía sem número e sem pontilhado. |
| `r02-capa-espaco-duplo` | Com `doublespacing` a capa transbordava para uma segunda folha, e a folha de sobra saía **numerada** na parte pré-textual, o que a 2.7 proíbe. |
| `r03-folha-aprovacao-oito` | A folha de aprovação com sete ou mais membros transbordava, e o `\thispagestyle` valia só para uma folha: a de sobra vinha numerada. Oito é o teto. |
| `r04-sumario-dois-digitos` | O `\@dottedtocline` dá ao número uma caixa de largura fixa; indicativos como `10.10.10.10` estouravam a caixa em até 4,6 mm e passavam **por cima** do título. A coluna passou a ser medida e viaja no `.aux`. |
| `r05-ponto-sumario-espanhol` | Com o espanhol como idioma principal, o babel punha um ponto no indicativo do sumário: `1.1. SECCIÓN` no sumário e `1.1 SECCIÓN` no título. |
| `r06-escrita-espanhol` | Documento em espanhol morria com `Unbalanced write command`: os rótulos da ficha passavam pelo `\@roman`, que o babel-espanhol redefine para versalete. |
| `r07-glossario-depois-dos-simbolos` | O `\renewcommand\glossaryname` do `\printlosymbols` ficava fora do grupo, e o Glossário pós-textual saía intitulado "Lista de Símbolos". |
| `r08-todas-as-listas` | O TeX tem dezesseis fluxos de escrita; um trabalho que pede **todas** as listas precisa de dezessete. Morria com `No room for a new \write`. |
| `r09-listas-sem-folio` | As listas de abreviaturas e de símbolos saíam com número de folha e pontilhado. A 4.1.1 pede o termo e o significado, e não pede localização nenhuma. |
| `r10-data-a-ser-determinada` | Sem `\dataaprovacao` a folha desenhava uma régua para preencher à mão. Ninguém escreve num PDF. |
| `r11-orientador-fora-da-banca` | A folha de aprovação listava sempre os orientadores, sem como tirar. Desde a #165 é o padrão: a banca é o que o autor declara com `\examiner`, e o orientador, que a preside, é o primeiro (3.1.2.1.3e). |
| `r12-orientador-examina` | O outro lado: a opção `orientadorexamina` põe o orientador de volta, à frente dos examinadores. |
| `r13-xmp-do-documento` | A opção `pdfa` nunca tinha sido compilada num documento de verdade: o `.xmpdata` era escrito antes de `\title` existir. |
| `r14-id-no-lualatex` | O LuaTeX renomeou `\pdfsuppressptexinfo` e ampliou o alcance dele: `-1` suprimiria também o `/ID` do trailer, que o PDF/A **exige**. |
| `r15-referencia-no-resumo` | A 3.1.2.1.4 sugere, e os Anexos E e F mostram, o resumo antecedido pela referência do trabalho. A classe não imprimia nenhuma. |
| `r16-resumo-sem-referencia` | O outro lado: `resumosemreferencia`, para o resumo que já está no limite das 500 palavras. |
| `r17-folio-so-na-parte-textual` | A contagem começava na Introdução, que saía como folha 1. A 2.7 manda contar da folha de rosto e **não** contar a folha adicional. |
| `r18-legenda-em-cima-fonte-embaixo` | A legenda ficava embaixo, como no `\caption` padrão. A norma põe a legenda em cima e a fonte, obrigatória, embaixo. |
| `r19-folha-de-rosto-em-portugues` | A folha de rosto de um trabalho em inglês ou espanhol saía com metade dos rótulos em cada idioma: "Research line" e "Co-advisor" sobre uma natureza e um "Orientador:" em português. Ela é identidade institucional e fica inteira em português (#128). O teste nasceu ao contrário — cobrava o rótulo no idioma do trabalho, defeito corrigido na v4.1 —, e a decisão da #128 desfez a regra, não a correção. |
| `r20-folha-adicional-capes` | A folha adicional do Anexo H não existia; depois existiu com parágrafos soltos e pontilhado, em vez da moldura fechada do modelo. |
| `r21-tratamento-e-instituicao` | `\advisor` e `\examiner` pediam o tratamento como obrigatório e a instituição como opcional. A 3.1.2.1.3(e) pede o contrário. |
| `r22-nivel-quinario` | A 2.6 admite até a seção quinária, e a classe parava na quaternária. |
| `r26-gerador-de-documento` | Não guarda defeito antigo: nasceu com o gerador de documento vazio. Um gerador erra de um jeito particular — produz um arquivo que **parece** certo e só quebra quando alguém compila, e quem compila é o aluno, na véspera. O teste gera dois documentos, o padrão e um com tudo ligado ao mesmo tempo, e **compila os dois** só com o que há na entrega, cobrando biber limpo, nenhuma citação sem resolver e nenhum aviso além do que a classe emite de propósito. |
| `r25-resumo-no-idioma-da-folha` | O texto que a **classe** escreve na folha de resumo — frase de abertura, título, mês, rótulos de orientação e de Programa — estava preso ao português na folha do `abstract` e ao inglês na do `foreignabstract`. Numa tese em inglês, cada folha saía com metade de cada idioma; numa tese em espanhol, duas folhas saíam com o mesmo cabeçalho em português e não havia cabeçalho em espanhol em lugar nenhum. O teste compila um trabalho com cada idioma principal e confere, folha por folha, que cada peça saiu no idioma certo e que nenhuma peça do idioma errado apareceu ali. |
| `r24-seminario-de-mestrado` | Não havia como compor um **Seminário de Mestrado**, que é requisito obrigatório de alguns Programas e não é um exame de qualificação. Quem precisava dele compunha com `mscexam` e trocava o título à mão, o que sai errado em quatro folhas de uma vez. O teste cobre a opção `mscsem` nos **cinco idiomas**, e cobra as duas metades: que o trabalho apareça como seminário, e que não venha com folha da Coleta CAPES, ficha catalográfica nem referência no alto do resumo — as três só cabem a trabalho depositado. |
| `r27-resumo-cinco-elementos` | Guarda, e não repara: a folha de resumo tem cinco elementos, e o teste liga os quatro opcionais — desde a #157 só a referência vem ligada por padrão, a folha do Anexo E, que o `rt76` cobra. Os três ambientes de resumo traziam o bloco inteiro copiado byte a byte, e foi essa cópia que produziu o `r23` e o `r25` — uma correção entrava em dois lugares e faltava no terceiro. Desde a v4.1 os três chamam o mesmo macro, e o teste cobra os cinco elementos na folha do resumo **e** na do *abstract*. |
| `r28-resumo-so-o-texto` | `\configuraresumos{false}{false}{false}{false}`: só o resumo propriamente dito é obrigatório. Cobra os **dois** idiomas, porque um comando que desligasse apenas o resumo do idioma principal passaria por uma cobrança de uma folha só. |
| `r29-configuraresumos-invalido` | Os quatro argumentos são lógicos, e um valor que não seja `true` nem `false` tem de **parar** a compilação. Um comando que engolisse `sim` em silêncio deixaria o elemento no estado anterior, e o autor descobriria a folha errada no depósito. |
| `r30-colofao-na-compilacao` | O colofão anunciava "Latin Modern" mesmo depois de o autor trocar de fonte, e dizia só o nome do motor — sem versão, sem sistema TeX, sem formato, sem data e sem hora. Colofão é registro de como **aquele** exemplar foi produzido. O teste troca `\familydefault` para uma família que a classe não conhece e cobra que o colofão diga a família nova. |
| `r31-bib-em-subpasta` | Não repara defeito antigo: prova uma recomendação. Os `.bib` passaram a morar numa subpasta, e o teste cobra as duas metades da resposta — que o caminho relativo **funciona** sem o `src/` para socorrer, e que ele **protege**, porque um nome pelado passa pela busca do kpathsea e acha, em silêncio, o `.bib` de mesmo nome que vem na distribuição do TeX. |
| `r32-tipo-do-trabalho-obrigatorio` | A única opção sem padrão é o tipo do trabalho, e nada cobrava que ela viesse. Sem ela a classe carregava em silêncio e morria mais tarde, dentro do `\maketitle`, com `Undefined control sequence \local@doctype` apontando para uma linha da própria classe. Agora para com uma mensagem que nomeia as cinco opções, e o teste cobra também que a cascata de quarenta erros **não** volte. |
| `r23-terceiro-resumo-com-titulo` | O terceiro resumo saía **sem título**. Ao fechar, o `foreignabstract` apagava `\local@title` — faxina de quando ele era a última folha pré-textual. Desde a v4.0 não é: o `brazilianabstract` vem depois e compõe o título com o que acabara de ser apagado. Só aparece em trabalho escrito em espanhol, e ia para o depósito assim. |

### Conformidade com o Manual 2026 (conferência de 16/09/2026)

Saíram da conferência completa da 4.1 contra o Manual UFRJ/SiBI, 9.ª ed. rev.
(2026) — issue guarda-chuva #112, uma issue por teste. Nasceram **mostrando**
defeito aberto, falhando até a correção; todos foram corrigidos no ramo
`V05-unificada` (17 e 18/09/2026), e hoje guardam a correção como os de cima.
O roteiro, com o commit de cada issue, está em
[`CORRECOES_MANUAL_2026.md`](../../CORRECOES_MANUAL_2026.md). Os que vieram
depois, da mesma família — a ordem dos pré-textuais, as normas da ABNT —,
entram nesta tabela com o prefixo `rt`.

**A marca `ABERTO`**, para a próxima conferência — hoje nenhum teste a traz.
Um teste de defeito aberto traz, logo depois da linha `BUG:`, uma linha
`ABERTO: #<issue>` (nos `.tex`, `%% ABERTO: #<issue>`). A rodada **sem filtro**
não roda teste marcado — só lista quais ficaram de fora —, porque trinta e
tantos testes que falham de propósito, e compilam cada um várias vezes, não
dizem nada a cada rodada e custam minutos. Enquanto a correção é feita, roda-se
**pelo nome, aos poucos**: `python tests/regressivo/run-regressivo.py rt38 rt50`.
A correção tira a linha `ABERTO` no mesmo commit do `Fixes #<issue>`, e dali em
diante o teste entra na rodada normal, como os de cima.

Quase todos cobram TIPOGRAFIA — itálico, negrito, corpo, posição na folha —, que
as diretivas de texto deste rodador não veem de propósito (tiram acento, caixa e
largura de traço). Por isso são `.py`, e usam o apoio [`medidas.py`](./medidas.py):
`pdftohtml -xml` dá a fonte e o corpo de cada pedaço de texto, `pdftotext -bbox`
dá a caixa exata de cada palavra, em pontos. O `medidas.py` não é teste — o
nome não casa com `r<número>-` — e compila numa pasta temporária. O
`Documento.ok` dele exige o PDF **e** nenhuma linha `!` no `.log`: em
`nonstopmode` o TeX produz o PDF mesmo depois de um erro, e um teste de medida
reprovava (ou aprovava) um documento quebrado sem dizer que ele tinha erro.

**Provar uma correção antes de levá-la ao `.dtx`.** `COPPE_SRC=<pasta>` faz os
testes usarem a classe de outra pasta: copie `src/` para um rascunho, mexa nos
arquivos gerados, e rode o teste contra a cópia. Os testes marcados com ✓ na
tabela passaram assim, contra um protótipo da correção proposta na issue — ou
seja, não são testes impossíveis de satisfazer.

```powershell
$env:COPPE_SRC = "C:\rascunho\src"; python tests/regressivo/rt38-referencias-alinhadas-a-esquerda.py
```

| Arquivo | Issue | O defeito | Prot. |
|---|---|---|---|
| `rt33-titulos-em-corpo-12` | #113 | Títulos de capítulo, seção e sem indicativo em `\Large`/`\large`; a 2.2(b) fixa corpo 12. | ✓ |
| `rt34-resumo-com-titulo` | #114 | Folhas de resumo sem o título centralizado RESUMO/ABSTRACT (2.6). | ✓ |
| `rt35-sumario-pos-textuais-na-coluna` | #115 | Referências, apêndices, anexos e índice na margem do sumário, e não na coluna dos títulos (3.1.2.1.6). | ✓ |
| `rt36-listas-com-nome-e-travessao` | #116 | Listas de ilustrações e de tabelas sem o nome específico e o traço (3.1.2.2.4). | ✓ |
| `rt37-notas-de-rodape` | #117 | Nota com a segunda linha na margem, número recuado, nota partida entre folhas (2.5, 4.1.2). | ✓ |
| `rt38-referencias-alinhadas-a-esquerda` | #118 | Lista de referências justificada e hifenizada (4.2). | ✓ |
| `rt39-referencia-do-resumo` | #119 | Referência do resumo justificada, título sem negrito, meia-risca (4.2, Anexo E). | ✓ |
| `rt40-listagem-dentro-da-margem` | #120 | Números de linha das listagens dentro da margem esquerda (2.3). | ✓ |
| `rt41-subalineas-com-hifen` | #121 | Subalínea com meia-risca e fora de posição (2.6). | ✓ |
| `rt42-espaco-depois-do-titulo` | #122 | Menos de uma linha em branco depois do título de seção (2.4). | ✓ |
| `rt43-dedicatoria-e-epigrafe-do-meio` | #123 | Dedicatória e epígrafe não começam no meio da mancha (3.1.2.2.1). | ✓ |
| `rt44-pdfa-por-padrao` | #124 | PDF/A desligado por padrão, e o gerador também (2.2d). | |
| `rt45-legenda-na-largura-da-ilustracao` | #125 | Legenda e fonte mais largas que a ilustração (2.10). API proposta: `\illustrationwidth`. | |
| `rt46-volumes-numeracao-e-sumario` | #126 | Volumes sem numeração contínua nem sumário completo (2.7). API proposta: `\volumefiles`. | |
| `rt47-letras-dobradas` | #127 | "Counter too large" depois do Z em apêndice, anexo e alínea (3.1.4.4). A letra dobrada é a mesma letra repetida — AA, BB, CC —, e não a contagem do Excel (AA, AB); o 27.º sai igual nas duas leituras, e por isso o teste cobra também o 28.º. | |
| `rt48-folhas-de-identidade-num-idioma` | #128 | Folha de rosto e aprovação com dois idiomas; cobra só um idioma por folha, qualquer que seja a decisão. | |
| `rt49-capa-nome-do-instituto` | #129 | Capa diferente da §2 da Norma COPPE; lê a Norma e confere. | |
| `rt50-subtitulo-nas-referencias` | #131 | Subtítulo depois de ponto, em negrito, e em caixa alta na entrada pelo título (4.3.3). | ✓ |
| `rt51-expressoes-latinas-em-italico` | #132 | "In:", "et al.", "[S. l.]", "[s. n.]" em redondo (4.2.1.3c, 4.1.2.2). | ✓ |
| `rt52-livro-edicao-volumes-serie` | #133 | "3ª ed.", "2 vol." antes da imprenta, série sem parênteses (4.3.4, 4.3.7). | |
| `rt53-parte-de-monografia` | #134 | Parte de monografia sem `bookauthor` e `booksubtitle`; capítulo depois das páginas (4.2.1.3). | |
| `rt54-tradutor-e-titulo-original` | #135 | Tradutor como autor ("Trad. por SOBRENOME, Nome"); sem título original (4.3.2.10). | |
| `rt55-doi` | #136 | DOI em versalete, sem https://doi.org, e aviso de fonte (4.2.3.5). | |
| `rt56-tese-e-dissertacao` | #137 | `@mastersthesis`/`@phdthesis` sem grau e sem travessão; "( em" com tipo digitado (4.3.8.3). | |
| `rt57-citacao-pela-entrada-de-titulo` | #138 | Chamada pelo título em itálico e sem vírgula (4.1.1.1.2), e com o título inteiro: a NBR 10520:2023 (6.1.1.4) o corta — "(Anteprojeto [...], 1987)", "(A flor [...], 1995)". Cobra também a caixa alta da entrada na lista, com o artigo ou o monossílabo inicial. | |
| `rt58-mesmo-sobrenome-mesmo-ano` | #139 | "(Orlando Braga, 1987)" no lugar de "(Braga, Orlando, 1987)" (4.1.1.2b). | ✓ |
| `rt59-sistema-numerico` | #140 | Chamada numérica entre colchetes; nenhum aviso com nota de rodapé (4.1.1.1.1). | ✓ |
| `rt60-ordem-alfabetica-sem-artigo` | #141 | O artigo e o monossílabo iniciais contam na alfabetação (4.2). Cobra também que as duas listas de palavras do `ufrj.bbx` — a do TeX e a do mapa do biber — sejam iguais. | ✓ |
| `rt61-periodico-em-curso` | #142 | Periódico corrente "1950/." no lugar de "1950- ." (4.3.5.5.1). | ✓ |
| `rt62-audiovisual-e-versao` | #143 | "Direção de Sobrenome, Nome"; versão depois da imprenta (4.2.9, 4.3.4). | |
| `rt63-entidade-hierarquica` | #144 | Chamada de entidade com órgão subordinado repete a hierarquia em caixa alta (4.1.1.2). O autor digita o nome como se escreve, e a classe põe a entrada em caixa alta na lista, sem o qualificador entre parênteses: "BRASIL. Ministério da Educação", "RIO DE JANEIRO (Estado). Secretaria…", "(IBGE, 2011)". | |
| `rt64-intervalo-de-paginas-com-hifen` | #145 | Intervalo de páginas com meia-risca (4.2.3.4). | ✓ |
| `rt65-mes-no-idioma-da-publicacao` | #146 | Mês no idioma do trabalho, e não no da publicação (4.3.5.5.1). Cobra inglês, espanhol, francês e alemão, pelas tabelas do Anexo A da NBR 6023:2025. | |
| `rt66-dissertacao-do-exemplo` (`.tex`) | #147 | A m-diss do `exemplo.bib` sem "Dissertação (Mestrado em …)" desde b14a5d6. Corrigida; a correção separou também as chaves das duas bases do gabarito (`m-` e `pt-`), porque com chaves iguais a forma em português nunca era composta. | |
| `rt67-ordem-das-listas` | #148 | Listas de ilustração depois da lista de tabelas nos modelos e na Norma COPPE §10 (3.1.2). Sem compilar. | |
| `rt68-conteudo-dos-exemplos` | #149 | Conteúdo dos exemplos contra o Manual: algoritmo sem fonte, acentos, palavras-chave, repetidas… Sem compilar. | |
| `rt69-mesmo-traco` | #150 | Traço diferente na legenda, no apêndice, no sumário e na Norma COPPE §12; cobra só que seja o mesmo. | |
| `rt70-lualatex-caracteres` | #152 | Achado ao ligar os verificadores à prova (#151): no LuaLaTeX, com `fontenc` T1, `º` saía `ž`, `§` saía `ğ`, e travessão, aspas curvas e reticências sumiam. Compila a mesma amostra nos dois motores. Corrigido: nos motores Unicode a classe fica em TU, com a Latin Modern em OpenType. | |
| `rt71-logotipos-so-na-capa` | #130 | A folha de rosto repetia a linha de logotipos da capa; o Anexo A põe os dois na **capa** e o Anexo B, modelo da folha de rosto, não traz imagem nenhuma. Mede **tinta** na faixa de cima de cada folha, porque os logotipos são vetoriais e o `pdfimages` não os vê. | |
| `rt72-ordem-dos-pre-textuais` | #148 | A classe não conferia a ordem dos pré-textuais da 3.1.2: um sumário antes das listas, uma lista de tabelas antes da de figuras ou uma dedicatória antes da folha de aprovação saíam como o autor escrevesse. Cobra o erro que nomeia os dois comandos, a epígrafe aceita depois do `\mainmatter` e o aviso de falta do sumário. Pela classe `coppe` de compatibilidade é aviso, e o `rtu03` cobra isso. | |
| `rt73-bib-sem-comentario-de-percentual` | #164 | Os `.bib` gerados do `ufrj.dtx`, a base das adversativas e o `.bib` do gerador tinham linhas de comentário com `%` — o preâmbulo do docstrip, o gabarito dentro das entradas e as divergências aceitas —, e o JabRef não as entende. Cobra, sem compilar, nenhuma linha começada por `%`, os 34 gabaritos de cada base lidos pelo `conferir-referencias.py` no formato `@comment{Manual: …}`, e os acentos do `.bib` do gerador em UTF-8. | |
| `rt74-legenda-e-fonte-a-esquerda` | #160 | A legenda e a fonte das ilustrações saíam centralizadas; o único exemplo do Manual, a Figura 1, as alinha à esquerda, na margem da ilustração, e a Norma COPPE §11 mandava centralizar a fonte. Mede, na folha, onde começa a linha da legenda e a da fonte, sem `\illustrationwidth` (na margem da mancha) e com ele (na margem da ilustração). | |
| `rt75-ordem-dos-resumos` | #158 | O resumo em português (língua vernácula) vinha depois do estrangeiro num trabalho em inglês ou espanhol: a Norma COPPE §7 ordenava pelo idioma principal. Cobra, em português, inglês e espanhol, a ordem certa sem erro e o erro que nomeia os dois ambientes fora dela. | |
| `rt76-folha-de-resumo-do-anexo-e` (`.tex`) | #157 | A folha de resumo vinha, por padrão, com quatro elementos acima do texto — a frase "Resumo da Tese apresentada à COPPE/UFRJ…", o título com o autor e o mês, a orientação com o Programa e a referência —, e o manual da classe dizia que era a folha dos Anexos E e F. Os Anexos mostram só a referência, o texto e as palavras-chave. Cobra o padrão, sem comando nenhum, nas folhas do resumo e do abstract. | |
| `rt77-conferir-referencias-confere` | #167 | O `conferir-referencias.py` separava as referências pela marca `[n]`, e desde a #140 a lista numérica sai sem colchetes: achava zero referências, dava o documento como "pulado" e passava — de 17 a 21/09/2026 nada foi conferido. E o gabarito não era o Manual: 12 das 34 referências tinham sido ajustadas à classe, e a divergência aceita de uma entrada escondia qualquer outra dela (a vírgula de "1996, p. 7-16"). Cobra, sem compilar: a separação com e sem colchetes, pelo número seguinte da sequência; a divergência aceita que só passa com a forma exata do `@comment{Classe: …}`, e a que falta, a velha e a de outra saída como divergência; os 34 gabaritos de cada base iguais ao texto do PDF do Manual em `specs/`. | |
| `rt78-jurisprudencia-julgado-em` (`.tex`) | #169 | A jurisprudência saía sem a data do julgamento, que a 4.2.6.2(i) pede "precedido da expressão 'julgado em' e da data abreviada", e com o rótulo `Relator` escrito no código, em qualquer idioma e gênero. Cobra os dois exemplos da seção: "Relator: Ministro Rafael Mayer, julgado em 26 fev. 1986" e "Relatora: Min. Ellen Gracie, julgado em 29 nov. 2005", e que a data não volte na imprenta. | |
| `rt80-cache-do-regressivo` | #154 | Uma rodada completa chama o motor perto de cem vezes, quase sempre com a mesma classe; desde a #154 o resultado de cada compilação fica em `_scratch/cache-regressivo`. Um cache mal feito é pior do que nenhum — faz o teste passar com um PDF velho. Cobra que o mesmo documento venha do cache na segunda vez com o PDF idêntico, que **outra classe mude a chave** (é a razão de ser do teste), que outro documento mude a chave, que a falha seja lembrada como falha, e que `COPPE_SEM_CACHE` desligue tudo. Cada rodada usa um documento com marca própria, para não depender do cache estar vazio. |  |
| `rt79-datas-incertas` | #168 | A classe não compunha data incerta (4.3.5): `[1981?]`, `[ca. 1977]`, `[197-]`, `[19--?]`, `[1071 ou 1072]`. Escrever o literal no `year` errava em três coisas — o `--` virava meia-risca, o ponto depois de `?]` sumia, e o `biber` avisava que o ano não é inteiro e ordenava pelo texto. Compila um documento com as oito formas e duas datas normais, e cobra cada forma na referência **e** na chamada, a data normal e a de acesso intactas, o `biber` sem aviso, e a lista ordenada pelo ano derivado. | |
| `rt89-prova-roda-as-conferencias` | #151 | A prova não rodava `conferir-referencias.py` nem `conferir-norma.py`; a m-diss do `exemplo.bib` saiu errada na 4.1 com o verificador acusando a divergência, mas ninguém o chamava. Sem compilar: cobra que o painel ou o `build-check` chamem os dois. No primeiro dia ligados, os dois acharam o `nž` do LuaLaTeX (#152). | |

### A classe da UFRJ e o estilo da unidade (`rtu`)

Os testes da 5.0. Nenhum repara defeito antigo: guardam a separação entre a
classe `ufrj` e o estilo da unidade.

| Arquivo | O que guarda |
|---|---|
| `rtu01-classe-sem-unidade` | Não repara defeito antigo: guarda a separação em camadas da v5.0. A classe `ufrj`, **sem estilo de unidade nenhum**, compõe o trabalho inteiro com os textos da UFRJ — "Programa de Pós-Graduação em", "apresentada à UFRJ", "em conformidade com o Manual" — e não escreve o Instituto, a sigla, o grau "em Ciências" nem a norma da COPPE. |
| `rtu02-unidade-ficticia` | Não repara defeito antigo: prova o objetivo da v5.0. Uma unidade inventada, no `ufrj-ficticia.sty` desta pasta, escrita **só com a interface pública** da classe, troca a capa, a natureza, a abertura do resumo, a referência e o colofão — com outra sigla, outro artigo e outro nome de grau — sem que a classe mude. |
| `rtu03-classe-coppe-antiga` | Não repara defeito antigo: guarda a compatibilidade com o que foi escrito até a v4.1. `\documentclass{coppe}`, `\newcoppefloat`, `\coppetexfinalpage`, um `\renewcommand\coppefinalmanual` e um `.toc` escrito pela classe antiga compilam sem erro, só com avisos. O `.toc` velho é o caso que a própria troca de nome encontrou: sem o apelido de `\coppe@tocapp`, a primeira compilação parava. O documento tem o sumário antes da lista de mapas, como os modelos da 4.x ensinavam: pela classe `coppe` a ordem errada é **aviso**, e não o erro da classe `ufrj` (#148). |
| `rtu04-classe-nao-nomeia-unidade` | Não repara defeito antigo: a mesma separação do rtu01, cobrada no **código**. Nada do que o `ufrj.ins` gera — classe, estilos de bibliografia, pacotes de idioma — pode nomear a COPPE, o Instituto, o logotipo, o grau "em Ciências" ou a sigla de um Programa. Pega o dado que voltasse para um ramo que o documento do rtu01 não percorre. Rodado contra a classe da v4.1, falha. |
| `rtu05-area-na-folha-de-rosto` | Não repara defeito antigo: guarda o modelo do SiBI. A área de concentração sai na **folha adicional**, entre os campos da Coleta CAPES, e não no bloco da natureza da folha de rosto nem no da folha de aprovação — o Anexo B e o Anexo D terminam o bloco no grau. Cobra as duas metades: sem a opção não sai nas folhas de identidade e sai na adicional; com `areanafolhaderosto` volta às duas (#155). |
| `rtu07-graduacao-na-poli` | Não repara defeito antigo: a classe só compunha trabalho de pós-graduação, e este teste guarda o de graduação (opção `grad`, #170) com o estilo `ufrj-poli`. Um departamento da Engenharia Civil (DES) prova o curso certo — Engenharia Civil, e não "Estruturas", como a antiga `poli.cls` — e o título, Engenheiro Civil. Cobra a natureza "apresentado ao Curso de…", a folha adicional só com a ficha, sem a Coleta CAPES, e a referência "Projeto de Graduação (Graduação em…)". |
| `rtu15-apelidos-em-portugues` | A regra dos dois nomes da 5.0: o nome em inglês tem o código, o português é apelido, e os apelidos ficam num bloco só no fim da classe. Compila o **mesmo trabalho** escrito todo em português e todo em inglês — folha de rosto, listas, siglas, símbolos, glossário, ilustração com fonte e anexo — e cobra que o texto saia igual folha por folha; confere que os dois nomes existem no `.cls` gerado; e chama o `tools/conferir-manual.py`, que reprova um comando público com um nome só ou um par declarado fora do bloco. |
| `rtu14-gerados-versionados` | O `src/ufrj.ist` estava no `.gitignore`, sozinho entre os gerados: numa cópia limpa do repositório ele não existia, e o `painel.py --dist`, o `rtu04` e as listas da classe quebravam. Achado do Codex na revisão do PR #171. Em vez de só consertar o caso, lê a lista do `painel.py` e cobra que **todo** arquivo de texto que vai de `src/` para `dist/` esteja versionado no git. |
| `rtu13-fontes-da-poli` | A Resolução 05/2012 da Escola pede "letra de tamanho equivalente a Times New Roman 12 ou Arial 11", e o estilo não oferecia nenhuma das duas famílias (#170). Compila um Projeto de Graduação sem opção, com `times` e com `arial`, e cobra a família que sai no PDF em cada um, e que toda fonte esteja embutida — que é o que o PDF/A exige. |
| `rtu10-cursos-da-poli` | Todos os cursos de graduação da Escola Politécnica estão declarados no estilo (#170): os treze de Engenharia e o de Nanotecnologia, pela lista da própria Escola. Sem compilar, lê o `ufrj-poli.sty` gerado e cobra o nome de cada curso, o título conferido de cada Engenharia, as siglas de departamento da antiga `poli.cls` e nenhuma sigla declarada duas vezes no mesmo ramo da opção. Falha quando a Escola cria um curso e ninguém o declara. |
| `rtu11-classe-poli-antiga` | A classe `poli` de compatibilidade (#170): um trabalho escrito com a classe antiga da Escola — `\documentclass[grad,pdftex]{poli}`, `\advisor` com quatro argumentos, `\examiner` com três, `\place` e `\university` — compila, com o aviso da classe e o aviso de que a banca sai sem instituição, e sem erro nenhum. |
| `rtu12-campus-fora-do-rio` | A UFRJ tem campus em Macaé e em Duque de Caxias, e a cidade estava escrita na classe. `\city` (e `\place`) trocam a cidade, que sai na capa, na folha de rosto e na referência do alto do resumo; o estilo da unidade declara o padrão dela com `\ufrjdeclareplace`, e o que o autor escreve prevalece. |
| `rtu09-civil-por-departamento` | A segunda forma da Engenharia Civil no estilo da Poli (#170): cinco siglas (DCC, DES, DEG, DET, DHIMA) são departamentos que conferem o mesmo título e que a `poli.cls` nomeava como curso. Por padrão o estilo dá o curso, Engenharia Civil (`rtu07`); com a opção `civilpordepartamento` dá o nome do departamento. Cobra a capa, a natureza e a referência na segunda forma. |
| `rtu08-graduacao-sem-unidade` | O mesmo tipo `grad` sem estilo de unidade: a classe sozinha compõe um Trabalho de Conclusão de Curso da UFRJ, e um curso declarado sem título confere "Bacharel em" o nome do curso. |
| `rtu06-logotipo-da-ufrj-fixo` | Não repara defeito antigo: guarda a divisão dos logotipos da capa (#162). O da UFRJ, à esquerda, é da classe, e a unidade não o troca nem o tira; o da direita é da unidade, declarado com `\ufrjdeclarelogo`. Cobra a classe sem unidade, a COPPE com o logotipo unificado, e a forma antiga `\ufrjdeclarelogos`, que continua aceita com aviso e ignora o logotipo da esquerda. |

### As ferramentas

Defeito de ferramenta merece teste igual. Um verificador que aprova tudo é pior
que verificador nenhum, porque parece que alguém conferiu.

| Arquivo | O defeito |
|---|---|
| `r90-log-de-uma-passada` | Os verificadores liam só o trecho do `.log` depois do **último** `LaTeX2e <`, achando que o arquivo guardasse várias passadas. Não guarda: o que aparece duas vezes é o banner, que o LaTeX repete no fim. O corte jogava fora o corpo da passada — onde estão os avisos — e o verificador passou a aprovar qualquer coisa. |
| `r91-logotipo-ausente` | Quem copiava só o `coppe.cls` (hoje `ufrj.cls`) recebia `File 'coppe-logo' not found`, sem pista de que o arquivo vem com a classe. |
| `r93-dist-basta-sozinha` | A pasta `dist/` é a única coisa que o aluno baixa, e nada garantia que ela bastasse — já saiu incompleta mais de uma vez, e o defeito só aparecia do outro lado, na máquina de quem foi escrever a tese. Aqui tudo compila porque `src/` está no caminho de busca do TeX e supre o que faltar. O teste tira essa muleta: copia `dist/` para uma pasta temporária, aponta o `TEXINPUTS` só para ela e compila os três exemplos. É o mais demorado da suíte. |
| `r92-lista-do-dist` | A cópia para `dist/` levava junto o `README.md` da raiz — que é a proposta para a CPGP, não o guia de instalação — e os cinco exemplos por idioma, que tinham sido tirados de propósito. A lista estava escrita em dois lugares e os dois divergiram. Este teste lê a lista; não compila nada. Cobra também que o rodador da primeira camada não volte a morrer no banner do `makeindex`. |

Um defeito do próprio rodador ficou de fora da tabela porque está corrigido no
código e comentado lá: ele descobria os testes por "nome que começa com `r`", e
`run-regressivo.py` começa com `r`. Rodava a si mesmo, e cada cópia rodava a si
mesma de novo. Agora o nome de um teste é `r<número>-<apelido>`, e o número não
é enfeite.
