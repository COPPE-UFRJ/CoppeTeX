# TODO — itens em aberto rumo ao release do CoppeTeX v4.1

Estado em setembro de 2026, branch `nlinguas`.

A série de trabalho de setembro alinhou a classe ao **Manual UFRJ/SiBI,
9.ª ed. revista (2026)**. A verificação item a item que originou esse
trabalho está em [`REVISAO_SIBI.md`](./REVISAO_SIBI.md); o que mudou para
quem escreve tese está em
[`MIGRATION_v3_to_v4.md`](./MIGRATION_v3_to_v4.md), seção 4.

---

## Já feito nesta série

Registrado aqui para que ninguém refaça:

- Layout de uma face, margem esquerda 3 cm (2.3) — o espelhamento perdeu
  base normativa quando a edição 2026 eliminou as margens de verso.
- Paginação contínua desde a folha de rosto; a Introdução deixou de ser a
  folha 1 (2.7).
- **Folha adicional com ficha catalográfica** e campos da Coleta CAPES
  (3.1.2.1.2), obrigatória desde agosto de 2026.
- Folha de rosto: área de concentração, linha de pesquisa, coorientador,
  subtítulo, número de volumes, ano de depósito, orientadores à esquerda.
- Folha de aprovação na ordem de 3.1.2.1.3, com data de aprovação, banca
  com titulação e instituição e o orientador como presidente.
- Palavras-chave ao final dos três resumos (3.1.2.1.4).
- **Latin Modern** no lugar das fontes bitmap — o documento inteiro saía
  em Type3, o que inviabilizava o PDF/A.
- **PDF/A-2b** sob a opção de classe `pdfa`, com metadados XMP (2.2d).
- Tipografia: recuo do primeiro parágrafo, `section` sem negrito,
  numeração até a quinária, sumário grafado como o corpo, legendas de
  algoritmo com travessão, alinhamento único de legendas, e fim dos 17
  estouros de margem do exemplo.
- Norma COPPE 2026 (`.md` e `.tex`) reconciliada com o manual.

---

## 1. Abrir o Pull Request

**Status:** pendente.

PR de `nlinguas` para `master` em
<https://github.com/COPPE-UFRJ/CoppeTeX>, com
[`CARTA_CPGP.md`](./CARTA_CPGP.md) como texto de abertura e links para os
PDFs de `dist/`.

**O `master` não deve ser avançado antes da aprovação da CPGP.** Ele
guarda o estado aprovado; o v4.x é proposta.

## 2. Validar o PDF/A com um validador de verdade

**Status: FEITO.** Os dois documentos que a classe produz com a opção
`pdfa` são **PDF/A-2b conformes** pelo veraPDF 1.30.2: 144 regras, 0
falhas.

E não é mais um ritual manual. `tools/build-check.ps1 -Scope pdfa`
compila os dois e passa os dois pelo veraPDF; o escopo `all` faz o mesmo.
São dois de propósito: `src/tests/test_pdfa.tex`, curto, cobre as páginas
pré-textuais, e `src/example_pdfa.tex` é o example.tex inteiro, com
bibliografia, listas, figuras, algoritmos e as caixas do tcolorbox — ou
seja, transparência, que é o que o a-1b proibiria e o a-2b admite.

Para chegar lá, três defeitos tiveram de ser consertados. A opção `pdfa`
**nunca tinha sido compilada num documento de verdade** e não funcionava
em nenhum: escrevia o `.xmpdata` antes de `\title` e `\author`
existirem (que é o estilo que a documentação ensina), estourava os
dezesseis fluxos de saída do TeX no `example.tex`, e uma passada ruim
gravava no `.xmpdata` o nome de uma sequência de controle, o que
inutilizava o arquivo até alguém apagá-lo à mão. Além disso, toda
listagem de código morria sob `pdfa`, porque o pdfx põe o xcolor em modo
de conversão e o `\textcolor` do `postbreak` falhava na primeira linha
quebrada.

**Avaliar tornar `pdfa` o padrão** em vez de opção — agora que se sabe que
funciona e que o resultado é conforme.

## 3. Revisão do pacote de espanhol por falante nativo

**Status:** pendente. É o que resta de trabalho humano.

Os pacotes de francês e italiano deixaram de ser idiomas de redação
autorizados (art. 57 da Res. CEPG 302/2024) e passaram a demonstração do
mecanismo de extensão, então a revisão urgente reduz-se ao **espanhol**:

- `frame` como `Cuadro` — algumas tradições preferem `Recuadro`;
- `depositor` como `Solicitante` — conferir com a terminologia de patentes;
- `mscdiss` como `Tesis de Maestría` — algumas instituições usam `Tesina`.

Gerar `dist/example_es.pdf` e pedir a um falante nativo do PESC ou de
outro Programa que marque o que mudaria.

## 4. Pendências técnicas menores

**Status: FEITAS, as quatro.**

- ~~Tabela de departamentos em UTF-8.~~ Cada programa é declarado duas
  vezes: `\local@deptname` mantém os escapes com chaves que a capa
  compõe, `\meta@deptname` traz o nome em UTF-8 literal para o XMP.
- ~~Fólio a 2 cm da borda superior.~~ A 2.7 mede pelo algarismo, como
  mede a margem direita. O topo estava a 1,87 cm — alto demais, e não
  baixo: os 2,15 cm da medição antiga eram da linha de base. `headsep`
  calibrado; os dois eixos caem em 2,019 cm, que é o viés da régua.
- ~~Banca grande com `assinaturas`.~~ Sete membros empurravam três para
  uma segunda folha, que ainda imprimia fólio na parte pré-textual. O
  espaço acompanha o tamanho da banca.
- ~~Coorientador nas páginas de resumo.~~ Virou a opção `coorientador`,
  desligada por padrão, com teste próprio.

## 4b. Conformidade: o que a revisão contra o manual 2026 encontrou

Varredura da saída medida contra `specs/manual-sibi-9ed-rev-2026.txt`.
Três não conformidades, todas corrigidas:

- **Fólio em corpo 12.** A 2.2(b) põe a paginação na lista do que sai em
  "fonte menor e uniforme", junto das citações longas, das notas de
  rodapé e das legendas — os outros três já saíam em 10 pt.
- **Listas pré-textuais no sumário.** O sumário abria com seis entradas
  (Figuras, Tabelas, Quadros, Programas, Abreviaturas, Símbolos) que são
  elementos pré-textuais e vêm antes dele. A 3.1.2.1.6 manda usar como
  exemplo o sumário do próprio manual, que abre em "1 INTRODUÇÃO". A
  opção `listasnosumario` devolve o comportamento antigo.
- **Apêndice e Anexo à esquerda.** A 2.6 lista "apêndice(s)" e "anexo(s)"
  entre os títulos sem indicativo numérico, que são centralizados —
  letra não é indicativo numérico, e o manual centraliza o seu Anexo A.

Conferidos e **conformes**: A4; margens 3/3/2/2; recuo de 4 cm da citação
longa (7 cm da borda, medido); corpo 12 no texto e 10 nas legendas,
citações e notas; filete de 5 cm nas notas; travessão nas legendas;
legenda acima e fonte abaixo; ordem dos pré-textuais com o sumário por
último; contagem começando na folha de rosto com a folha adicional fora;
títulos sem indicativo centralizados na mancha; pós-textuais no sumário.

Também saiu da documentação um erro por fator de quatro: o parágrafo da
citação longa dizia que a margem esquerda passa a 4 cm, quando o que a
norma pede — e o que o código sempre fez — é recuo de 4 cm ALÉM da
margem. E metade das opções de classe não estava documentada, inclusive
`pdfa` e `assinaturas`.

## 4c. Fonte única, e onde ela termina

`pdflatex coppe.ins` gera **tudo o que é distribuído**: a classe, os estilos
biblatex, os pacotes de idioma, as bases `.bib`, o `.ist`, os cinco exemplos
por idioma, o `example_pdfa`, a montagem das capas e o `latexmkrc`. Nenhum
arquivo derivado é mantido à mão.

A linha para aí. O que existe só para **provar** que a classe funciona não sai
do `.dtx` e não é distribuído:

- `tests/` — a suíte de regressão, sete arquivos escritos à mão;
- `adversativa/` — doze documentos, quatro tipos de trabalho por três idiomas,
  cada um acionando ao mesmo tempo tudo o que a classe oferece;
- `tools/*.ps1` — o harness;
- `NORMA_COPPE_2026.tex` e `futuremanual2026.tex` — documentos sobre a norma,
  com ciclo de vida próprio.

## 4d. A prova de funcionamento

```powershell
.\tools\prova.ps1
```

É o que tem de sair limpo antes de marcar uma versão. Não é atalho para o
build-check: cobre as três coisas que podem estar erradas sem ninguém notar.

1. **Fonte única.** Regera tudo do `.dtx` e confere pelo git se algum arquivo
   distribuído mudou. Se mudou, alguém editou um derivado à mão — e a edição
   acabou de ser perdida. Melhor descobrir antes de publicar.
2. **O que é distribuído compila.**
3. **A prova passa**: a suíte de regressão e os doze adversativos, nos **dois
   motores**, com o veraPDF em cima de todo PDF/A.

Estado atual: **243 passos, 0 falhas, 26 PDFs conformes com PDF/A-2b**.

## 4e. Os dezesseis fluxos de escrita

Um trabalho que usa todas as listas estoura os 16 `\write` do pdfTeX. Medido
pela sonda `adversativa/_writes_probe.tex`, num documento que aciona tudo:

| | fluxos |
|---|---|
| núcleo (`.aux`, `\@partaux`, `\@unused`) | 3 |
| a classe e os pacotes que ela carrega | 3 |
| `tcolorbox` do autor | 1 |
| `makeidx` | 1 |
| listas de abreviaturas e de símbolos | 2 |
| `.out` do hyperref, no `\begin{document}` | 1 |
| as seis listas (`.toc`, `.lof`, `.lot`, `.loq`, `.lol`, `.loa`) | 6 |

Dezessete para dezesseis lugares. A classe responde por dois, e os dois só
existem se o autor pedir as listas; seis listas custam seis fluxos porque é
assim que o `\@starttoc` do LaTeX funciona. Não há o que enxugar.

Por isso, sob pdfTeX a classe **carrega o `morewrites` sozinha**, se estiver
instalado — mensagem de erro mandando ligar opção é conselho para quem já
sabe. `semmorewrites` desliga, para quem topar com um conflito;
`morewrites` passa a significar "eu insisto" (falta do pacote vira erro). Sob
LuaTeX, que tem 128 fluxos, nada é carregado.

E quando o teto for atingido mesmo assim, o erro é da classe, em português, e
nomeia as três saídas.

## 5. CTAN e Overleaf

**Status:** pendentes de aprovação da CPGP.

- Tag `v4.1`, pacote CTAN a partir de `dist/` mais `src/coppe.dtx` e
  `src/coppe.ins` — que agora bastam sozinhos para reconstruir a
  distribuição inteira.
- Template no Overleaf com o conteúdo de `dist/`, e botão "Open in
  Overleaf" no README. O `latexmkrc` já configura biber e os makeindex.

## 6. Higiene do repositório

- Metadados do GitHub: descrição, tópicos (`latex`, `latex-class`,
  `thesis`, `abnt`, `coppe`, `ufrj`, `biblatex`).
- `SECURITY.md` e `CODE_OF_CONDUCT.md` mínimos.
- Release no GitHub com os artefatos de `dist/`.

**Sem CI no GitHub Actions.** A verificação roda localmente por
[`tools/build-check.ps1`](./tools/build-check.ps1), que regenera tudo a
partir do `.dtx`, compila o exemplo, os cinco idiomas, os manuais e a
suíte de testes, passa os dois documentos PDF/A pelo veraPDF, e deixa os
logs em `_scratch/`. `tools/watch-build.ps1` dispara o mesmo
quando aparece um arquivo `_scratch/BUILD_REQUEST`.

---

## Como retomar em outra máquina

```bash
git clone https://github.com/COPPE-UFRJ/CoppeTeX.git
cd CoppeTeX
git checkout nlinguas          # NÃO trabalhe no master
cd src && pdflatex coppe.ins   # gera TODOS os arquivos derivados
```

### O que não vem pelo git

- **Os manuais em `specs/`.** São publicações do SiBI e do próprio COPPE; o
  repositório não os redistribui (ver `.gitignore`). Só os `.md` daquela
  pasta são versionados. Copie os PDFs da máquina antiga —
  [`specs/README.md`](./specs/README.md) diz o que é cada um e onde
  obtê-los. Sem eles dá para compilar tudo, mas não para conferir a
  classe contra a norma.
- As pastas locais `ABNT/`, `LIXO/`, `LaTeXManuals/` e `_scratch/`.

### Para compilar e verificar

Numa janela do PowerShell, deixe rodando:

```powershell
.\tools\watch-build.ps1
```

Ele observa `_scratch\BUILD_REQUEST` e escreve `_scratch\RESULTADO.txt`.
Ou rode direto:

```powershell
.\tools\build-check.ps1 -Scope all   # class|example|langs|tests|docs|pdfa|all
```

O escopo `pdfa` compila os dois documentos PDF/A e passa os dois pelo
veraPDF, que o script procura em `%USERPROFILE%\verapdf` e no PATH; sem
ele o passo é pulado, não falha. O relatório XML fica em
`_scratch/build-logs/` e o resumo, com a cláusula de cada regra
reprovada, vai para o `RESULTADO.txt`.

Requisitos: TeX Live ou MiKTeX com `biber`, `biblatex`, `lmodern`,
`algorithm2e`, `tcolorbox`, `pdfx` e os pacotes de idioma do Babel.
`pdftoppm` (poppler) é opcional — sem ele, apenas a montagem de capas é
pulada. O [veraPDF](https://verapdf.org/) é necessário só para o escopo
`pdfa`.

### Política de branch

O **`master` guarda o estado aprovado pela COPPE** e só se move quando a
CPGP aprovar o v4.x. Todo o trabalho vive em `nlinguas`.

Cuidado com um detalhe que já causou problema: **renomear um branch não
reaponta o upstream**. Um `git branch -m` deixou a configuração apontando
para `master` e o push seguinte publicou trabalho não aprovado dentro
dele. Depois de renomear qualquer branch, confira `git branch -vv` antes
de dar push.

---

*Última atualização: 9 de setembro de 2026, branch `nlinguas`.*
