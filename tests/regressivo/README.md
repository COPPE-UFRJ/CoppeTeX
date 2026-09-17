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
| `r26-gerador-de-documento` | Não guarda defeito antigo: nasceu com o gerador de documento vazio. Um gerador erra de um jeito particular — produz um arquivo que **parece** certo e só quebra quando alguém compila, e quem compila é o aluno, na véspera. O teste gera dois documentos, o padrão e um com tudo ligado ao mesmo tempo, e **compila os dois** só com o que há na entrega, cobrando biber limpo, nenhuma citação sem resolver e nenhum aviso além do que a classe emite de propósito. |
| `r25-resumo-no-idioma-da-folha` | O texto que a **classe** escreve na folha de resumo — frase de abertura, título, mês, rótulos de orientação e de Programa — estava preso ao português na folha do `abstract` e ao inglês na do `foreignabstract`. Numa tese em inglês, cada folha saía com metade de cada idioma; numa tese em espanhol, duas folhas saíam com o mesmo cabeçalho em português e não havia cabeçalho em espanhol em lugar nenhum. O teste compila um trabalho com cada idioma principal e confere, folha por folha, que cada peça saiu no idioma certo e que nenhuma peça do idioma errado apareceu ali. |
| `r24-seminario-de-mestrado` | Não havia como compor um **Seminário de Mestrado**, que é requisito obrigatório de alguns Programas e não é um exame de qualificação. Quem precisava dele compunha com `mscexam` e trocava o título à mão, o que sai errado em quatro folhas de uma vez. O teste cobre a opção `mscsem` nos **cinco idiomas**, e cobra as duas metades: que o trabalho apareça como seminário, e que não venha com folha da Coleta CAPES, ficha catalográfica nem referência no alto do resumo — as três só cabem a trabalho depositado. |
| `r27-resumo-cinco-elementos` | Guarda, e não repara: a folha de resumo tem cinco elementos e os quatro opcionais vêm **ligados**. Os três ambientes de resumo traziam o bloco inteiro copiado byte a byte, e foi essa cópia que produziu o `r23` e o `r25` — uma correção entrava em dois lugares e faltava no terceiro. Desde a v4.1 os três chamam o mesmo macro, e o teste cobra os cinco elementos na folha do resumo **e** na do *abstract*. |
| `r28-resumo-so-o-texto` | `\configuraresumos{false}{false}{false}{false}`: só o resumo propriamente dito é obrigatório. Cobra os **dois** idiomas, porque um comando que desligasse apenas o resumo do idioma principal passaria por uma cobrança de uma folha só. |
| `r29-configuraresumos-invalido` | Os quatro argumentos são lógicos, e um valor que não seja `true` nem `false` tem de **parar** a compilação. Um comando que engolisse `sim` em silêncio deixaria o elemento no estado anterior, e o autor descobriria a folha errada no depósito. |
| `r30-colofao-na-compilacao` | O colofão anunciava "Latin Modern" mesmo depois de o autor trocar de fonte, e dizia só o nome do motor — sem versão, sem sistema TeX, sem formato, sem data e sem hora. Colofão é registro de como **aquele** exemplar foi produzido. O teste troca `\familydefault` para uma família que a classe não conhece e cobra que o colofão diga a família nova. |
| `r31-bib-em-subpasta` | Não repara defeito antigo: prova uma recomendação. Os `.bib` passaram a morar numa subpasta, e o teste cobra as duas metades da resposta — que o caminho relativo **funciona** sem o `src/` para socorrer, e que ele **protege**, porque um nome pelado passa pela busca do kpathsea e acha, em silêncio, o `.bib` de mesmo nome que vem na distribuição do TeX. |
| `r32-tipo-do-trabalho-obrigatorio` | A única opção sem padrão é o tipo do trabalho, e nada cobrava que ela viesse. Sem ela a classe carregava em silêncio e morria mais tarde, dentro do `\maketitle`, com `Undefined control sequence \local@doctype` apontando para uma linha da própria classe. Agora para com uma mensagem que nomeia as cinco opções, e o teste cobra também que a cascata de quarenta erros **não** volte. |
| `r23-terceiro-resumo-com-titulo` | O terceiro resumo saía **sem título**. Ao fechar, o `foreignabstract` apagava `\local@title` — faxina de quando ele era a última folha pré-textual. Desde a v4.0 não é: o `brazilianabstract` vem depois e compõe o título com o que acabara de ser apagado. Só aparece em trabalho escrito em espanhol, e ia para o depósito assim. |

### Conformidade com o Manual 2026 (conferência de 16/09/2026)

Estes não guardam defeito já corrigido: **mostram** defeito aberto. Saíram da
conferência completa da 4.1 contra o Manual UFRJ/SiBI, 9.ª ed. rev. (2026) —
issue guarda-chuva #112, uma issue por teste —, e **falham até a correção**.
O roteiro de correção está em [`CORRECOES_MANUAL_2026.md`](../../CORRECOES_MANUAL_2026.md).

**A marca `ABERTO`.** Cada um traz, logo depois da linha `BUG:`, uma linha
`ABERTO: #<issue>` (nos `.tex`, `%% ABERTO: #<issue>`). A rodada **sem filtro**
não roda teste marcado — só lista quais ficaram de fora —, porque trinta e
tantos testes que falham de propósito, e compilam cada um várias vezes, não
dizem nada a cada rodada e custam minutos. Enquanto a correção é feita, roda-se
**pelo nome, aos poucos**: `python tests/regressivo/run-regressivo.py r38 r50`.
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
$env:COPPE_SRC = "C:\rascunho\src"; python tests/regressivo/r38-referencias-alinhadas-a-esquerda.py
```

| Arquivo | Issue | O defeito | Prot. |
|---|---|---|---|
| `r33-titulos-em-corpo-12` | #113 | Títulos de capítulo, seção e sem indicativo em `\Large`/`\large`; a 2.2(b) fixa corpo 12. | ✓ |
| `r34-resumo-com-titulo` | #114 | Folhas de resumo sem o título centralizado RESUMO/ABSTRACT (2.6). | ✓ |
| `r35-sumario-pos-textuais-na-coluna` | #115 | Referências, apêndices, anexos e índice na margem do sumário, e não na coluna dos títulos (3.1.2.1.6). | ✓ |
| `r36-listas-com-nome-e-travessao` | #116 | Listas de ilustrações e de tabelas sem o nome específico e o traço (3.1.2.2.4). | ✓ |
| `r37-notas-de-rodape` | #117 | Nota com a segunda linha na margem, número recuado, nota partida entre folhas (2.5, 4.1.2). | ✓ |
| `r38-referencias-alinhadas-a-esquerda` | #118 | Lista de referências justificada e hifenizada (4.2). | ✓ |
| `r39-referencia-do-resumo` | #119 | Referência do resumo justificada, título sem negrito, meia-risca (4.2, Anexo E). | ✓ |
| `r40-listagem-dentro-da-margem` | #120 | Números de linha das listagens dentro da margem esquerda (2.3). | ✓ |
| `r41-subalineas-com-hifen` | #121 | Subalínea com meia-risca e fora de posição (2.6). | ✓ |
| `r42-espaco-depois-do-titulo` | #122 | Menos de uma linha em branco depois do título de seção (2.4). | ✓ |
| `r43-dedicatoria-e-epigrafe-do-meio` | #123 | Dedicatória e epígrafe não começam no meio da mancha (3.1.2.2.1). | ✓ |
| `r44-pdfa-por-padrao` | #124 | PDF/A desligado por padrão, e o gerador também (2.2d). | |
| `r45-legenda-na-largura-da-ilustracao` | #125 | Legenda e fonte mais largas que a ilustração (2.10). API proposta: `\illustrationwidth`. | |
| `r46-volumes-numeracao-e-sumario` | #126 | Volumes sem numeração contínua nem sumário completo (2.7). API proposta: `\volumefiles`. | |
| `r47-letras-dobradas` | #127 | "Counter too large" depois do Z em apêndice, anexo e alínea (3.1.4.4). | |
| `r48-folhas-de-identidade-num-idioma` | #128 | Folha de rosto e aprovação com dois idiomas; cobra só um idioma por folha, qualquer que seja a decisão. | |
| `r49-capa-nome-do-instituto` | #129 | Capa diferente da §2 da Norma COPPE; lê a Norma e confere. | |
| `r50-subtitulo-nas-referencias` | #131 | Subtítulo depois de ponto, em negrito, e em caixa alta na entrada pelo título (4.3.3). | ✓ |
| `r51-expressoes-latinas-em-italico` | #132 | "In:", "et al.", "[S. l.]", "[s. n.]" em redondo (4.2.1.3c, 4.1.2.2). | ✓ |
| `r52-livro-edicao-volumes-serie` | #133 | "3ª ed.", "2 vol." antes da imprenta, série sem parênteses (4.3.4, 4.3.7). | |
| `r53-parte-de-monografia` | #134 | Parte de monografia sem `bookauthor` e `booksubtitle`; capítulo depois das páginas (4.2.1.3). | |
| `r54-tradutor-e-titulo-original` | #135 | Tradutor como autor ("Trad. por SOBRENOME, Nome"); sem título original (4.3.2.10). | |
| `r55-doi` | #136 | DOI em versalete, sem https://doi.org, e aviso de fonte (4.2.3.5). | |
| `r56-tese-e-dissertacao` | #137 | `@mastersthesis`/`@phdthesis` sem grau e sem travessão; "( em" com tipo digitado (4.3.8.3). | |
| `r57-citacao-pela-entrada-de-titulo` | #138 | Chamada pelo título em itálico e sem vírgula (4.1.1.1.2). | |
| `r58-mesmo-sobrenome-mesmo-ano` | #139 | "(Orlando Braga, 1987)" no lugar de "(Braga, Orlando, 1987)" (4.1.1.2b). | ✓ |
| `r59-sistema-numerico` | #140 | Chamada numérica entre colchetes; nenhum aviso com nota de rodapé (4.1.1.1.1). | ✓ |
| `r60-ordem-alfabetica-sem-artigo` | #141 | O artigo inicial conta na alfabetação (4.2). | ✓ |
| `r61-periodico-em-curso` | #142 | Periódico corrente "1950/." no lugar de "1950- ." (4.3.5.5.1). | ✓ |
| `r62-audiovisual-e-versao` | #143 | "Direção de Sobrenome, Nome"; versão depois da imprenta (4.2.9, 4.3.4). | |
| `r63-entidade-hierarquica` | #144 | Chamada de entidade com órgão subordinado repete a hierarquia em caixa alta (4.1.1.2). | |
| `r64-intervalo-de-paginas-com-hifen` | #145 | Intervalo de páginas com meia-risca (4.2.3.4). | ✓ |
| `r65-mes-no-idioma-da-publicacao` | #146 | Mês no idioma do trabalho, e não no da publicação (4.3.5.5.1). | |
| `r66-dissertacao-do-exemplo` (`.tex`) | #147 | A m-diss do `exemplo.bib` sem "Dissertação (Mestrado em …)" desde b14a5d6. Corrigida; a correção separou também as chaves das duas bases do gabarito (`m-` e `pt-`), porque com chaves iguais a forma em português nunca era composta. | |
| `r67-ordem-das-listas` | #148 | Listas de ilustração depois da lista de tabelas nos modelos e na Norma COPPE §10 (3.1.2). Sem compilar. | |
| `r68-conteudo-dos-exemplos` | #149 | Conteúdo dos exemplos contra o Manual: algoritmo sem fonte, acentos, palavras-chave, repetidas… Sem compilar. | |
| `r69-mesmo-traco` | #150 | Traço diferente na legenda, no apêndice, no sumário e na Norma COPPE §12; cobra só que seja o mesmo. | |
| `r70-lualatex-caracteres` | #152 | Achado ao ligar os verificadores à prova (#151): no LuaLaTeX, com `fontenc` T1, `º` saía `ž`, `§` saía `ğ`, e travessão, aspas curvas e reticências sumiam. Compila a mesma amostra nos dois motores. Corrigido: nos motores Unicode a classe fica em TU, com a Latin Modern em OpenType. | |

A issue #130 (logotipos na folha de rosto) não tem teste: depende de decisão.

### As ferramentas

Defeito de ferramenta merece teste igual. Um verificador que aprova tudo é pior
que verificador nenhum, porque parece que alguém conferiu.

| Arquivo | O defeito |
|---|---|
| `r90-log-de-uma-passada` | Os verificadores liam só o trecho do `.log` depois do **último** `LaTeX2e <`, achando que o arquivo guardasse várias passadas. Não guarda: o que aparece duas vezes é o banner, que o LaTeX repete no fim. O corte jogava fora o corpo da passada — onde estão os avisos — e o verificador passou a aprovar qualquer coisa. |
| `r91-logotipo-ausente` | Quem copiava só o `coppe.cls` recebia `File 'coppe-logo' not found`, sem pista de que o arquivo vem com a classe. |
| `r93-dist-basta-sozinha` | A pasta `dist/` é a única coisa que o aluno baixa, e nada garantia que ela bastasse — já saiu incompleta mais de uma vez, e o defeito só aparecia do outro lado, na máquina de quem foi escrever a tese. Aqui tudo compila porque `src/` está no caminho de busca do TeX e supre o que faltar. O teste tira essa muleta: copia `dist/` para uma pasta temporária, aponta o `TEXINPUTS` só para ela e compila os três exemplos. É o mais demorado da suíte. |
| `r89-prova-roda-as-conferencias` | A prova não rodava `conferir-referencias.py` nem `conferir-norma.py` (#151); a m-diss do `exemplo.bib` saiu errada na 4.1 com o verificador acusando a divergência, mas ninguém o chamava. Sem compilar: cobra que o painel ou o `build-check` chamem os dois. No primeiro dia ligados, os dois acharam o `nž` do LuaLaTeX (#152). |
| `r92-lista-do-dist` | A cópia para `dist/` levava junto o `README.md` da raiz — que é a proposta para a CPGP, não o guia de instalação — e os cinco exemplos por idioma, que tinham sido tirados de propósito. A lista estava escrita em dois lugares e os dois divergiram. Este teste lê a lista; não compila nada. Cobra também que o rodador da primeira camada não volte a morrer no banner do `makeindex`. |

Um defeito do próprio rodador ficou de fora da tabela porque está corrigido no
código e comentado lá: ele descobria os testes por "nome que começa com `r`", e
`run-regressivo.py` começa com `r`. Rodava a si mesmo, e cada cópia rodava a si
mesma de novo. Agora o nome de um teste é `r<número>-<apelido>`, e o número não
é enfeite.
