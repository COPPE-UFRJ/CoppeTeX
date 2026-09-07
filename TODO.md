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

**Status:** pendente. Continua sendo o item mais importante que resta, mas
o terreno foi preparado.

Uma auditoria estrutural de `tests/test_pdfa.pdf` conferiu, item a item,
o que um validador cobraria e não achou nada errado: sem `/Encrypt`, XMP
no catálogo sem filtro declarando `pdfaid:part=2`/`conformance=B`,
OutputIntent `GTS_PDFA1` com perfil sRGB embutido, as sete fontes todas
embutidas e nenhuma Type3, as cinco anotações com o flag Print, sem
JavaScript, sem LZW, `/ID` no trailer, e DocInfo e XMP batendo em título,
autor e assunto.

Ela achou **uma** coisa e ela foi corrigida: o pdfTeX carimbava
`/PTEX.Fullbanner` no dicionário de informações. Não é uma das chaves que
a 6.6.2.3.2 mapeia para uma propriedade XMP e nenhum extension schema a
declarava, ou seja, era entrada de DocInfo sem contrapartida no XMP — a
queixa clássica de quem passa um PDF do pdfTeX por um validador. A classe
agora faz `\pdfsuppressptexinfo=-1`.

Sobram duas entradas na mesma situação, e **ambas são postas ali pelo
próprio pdfx**, não pela classe: `/Trapped` (que o pdfx grava fixo como
`/False` e não espelha em `pdf:Trapped`) e `/GTS_PDFA1Version`. Mexer
nelas é brigar com o pacote, e não vale fazer isso às cegas: são
exatamente o tipo de coisa que só se decide com o relatório do validador
na mão.

Falta, então, o que sempre faltou — **rodar o veraPDF**. Não dá para fazer
isso daqui: `software.verapdf.org`, o Maven Central e o CTAN estão fora da
política de saída tanto do ambiente da nuvem quanto da VM local. Na sua
máquina:

```powershell
# baixe o instalador em https://verapdf.org/software/
verapdf --flavour 2b tests\test_pdfa.pdf
```

Se passar, avaliar tornar `pdfa` o padrão em vez de opção. Se acusar
`/Trapped` ou `/GTS_PDFA1Version`, aí sim vale investigar como contornar
o pdfx.

## 3. Revisão do pacote de espanhol por falante nativo

**Status:** pendente.

Os pacotes de francês e italiano deixaram de ser idiomas de redação
autorizados (art. 57 da Res. CEPG 302/2024) e passaram a demonstração do
mecanismo de extensão, então a revisão urgente reduz-se ao **espanhol**:

- `frame` como `Cuadro` — algumas tradições preferem `Recuadro`;
- `depositor` como `Solicitante` — conferir com a terminologia de patentes;
- `mscdiss` como `Tesis de Maestría` — algumas instituições usam `Tesina`.

Gerar `dist/example_es.pdf` e pedir a um falante nativo do PESC ou de
outro Programa que marque o que mudaria.

## 4. Pendências técnicas menores

- **Coorientador nas páginas de resumo.** Hoje só os orientadores são
  listados ali. O formato daquela página é tradição da COPPE, não
  exigência do manual — decidir antes de mexer. **Único item ainda em
  aberto desta seção**, e é decisão, não conserto.

Os outros três saíram:

- ~~Tabela de departamentos em UTF-8.~~ Cada programa agora é declarado
  duas vezes: `\local@deptname` mantém os escapes com chaves que a capa e
  a folha de rosto compõem, e `\meta@deptname` traz o mesmo nome em UTF-8
  literal, que é o que vai para o XMP. O assunto dos metadados deixou de
  ser o código e passou a ser "Programa de Engenharia de Sistemas e
  Computação (PESC), COPPE/UFRJ", com os acentos inteiros no DocInfo e no
  `dc:description`.
- ~~Fólio a 2 cm da borda superior.~~ A medida de 2,15 cm era da linha de
  base; a 2.7 mede o fólio como mede a margem direita, pelo algarismo
  ("a 2cm da borda superior, ficando o último algarismo a 2cm da borda
  direita"). Medido na página renderizada, o topo dos algarismos estava a
  1,87 cm — alto demais, e não baixo. `headsep` foi calibrado em 15,49 pt
  a partir de dois pontos medidos; o topo dos algarismos e a borda direita
  agora caem os dois em 2,019 cm, e a margem direita é 2 cm por
  construção, então esses 0,019 cm são viés da régua e não erro residual.
  O topo do corpo continua exatamente em 3 cm.
- ~~Banca grande com a opção `assinaturas`.~~ Estourava mesmo:
  `tests/test_assinaturas_7.tex` (dois orientadores e cinco examinadores,
  um deles com nome e instituição longos) empurrava três membros para uma
  segunda folha — que ainda por cima imprimia fólio na parte pré-textual,
  onde a 2.7 proíbe. O espaço acima de cada linha de assinatura passou a
  sair de `\coppe@membrogap`, ajustado ao tamanho da banca (9 mm até
  cinco membros, 7 mm com seis, 5 mm de sete em diante) e com 2 mm de
  encolhimento para absorver um título que quebre uma linha a mais. Cinco
  membros ou menos compõem exatamente como antes.

## 5. CTAN e Overleaf

**Status:** pendentes de aprovação da CPGP.

- Tag `v4.1`, pacote CTAN a partir de `dist/` mais `src/coppe.dtx` e
  `src/coppe.ins`.
- Template no Overleaf com o conteúdo de `dist/`, e botão "Open in
  Overleaf" no README. O `latexmkrc` já configura biber e os makeindex.

## 6. Higiene do repositório

- Metadados do GitHub: descrição, tópicos (`latex`, `latex-class`,
  `thesis`, `abnt`, `coppe`, `ufrj`, `biblatex`).
- `SECURITY.md` e `CODE_OF_CONDUCT.md` mínimos.
- Release no GitHub com os artefatos de `dist/`.

**Sem CI no GitHub Actions.** A verificação roda localmente por
[`tools/build-check.ps1`](./tools/build-check.ps1), que regenera a classe,
compila o exemplo, os cinco idiomas, os manuais e a suíte de testes, e
deixa os logs em `_scratch/`. `tools/watch-build.ps1` dispara o mesmo
quando aparece um arquivo `_scratch/BUILD_REQUEST`.

---

## Como retomar em outra máquina

```bash
git clone https://github.com/COPPE-UFRJ/CoppeTeX.git
cd CoppeTeX
git checkout nlinguas          # NÃO trabalhe no master
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
.\tools\build-check.ps1 -Scope all      # class | example | langs | tests | docs | all
```

Requisitos: TeX Live ou MiKTeX com `biber`, `biblatex`, `lmodern`,
`algorithm2e`, `tcolorbox`, `pdfx` e os pacotes de idioma do Babel.
`pdftoppm` (poppler) é opcional — sem ele, apenas a montagem de capas é
pulada.

### Política de branch

O **`master` guarda o estado aprovado pela COPPE** e só se move quando a
CPGP aprovar o v4.x. Todo o trabalho vive em `nlinguas`.

Cuidado com um detalhe que já causou problema: **renomear um branch não
reaponta o upstream**. Um `git branch -m` deixou a configuração apontando
para `master` e o push seguinte publicou trabalho não aprovado dentro
dele. Depois de renomear qualquer branch, confira `git branch -vv` antes
de dar push.

---

*Última atualização: 6 de setembro de 2026, branch `nlinguas`.*
