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

**Status:** pendente, e é o item mais importante que resta.

O arquivo produzido com a opção `pdfa` **declara** conformidade a-2b,
traz OutputIntent com perfil sRGB embutido, todas as fontes embutidas e
XMP completo — mas **nenhum validador rodou sobre ele**. Não há veraPDF
disponível no ambiente em que a classe foi desenvolvida.

Antes do release: passar `dist/example.pdf` pelo
[veraPDF](https://verapdf.org/) ou pelo pré-voo do Acrobat, e só então
considerar 2.2(d) atendido. Se passar, avaliar tornar `pdfa` o padrão em
vez de opção.

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

- **Tabela de departamentos em UTF-8.** Os nomes em `\department` trazem
  escapes com chaves (`Computa{\c c}{\~ a}o`), que o pdfx copia literais
  para o XMP. Por isso o `\Subject` dos metadados usa o código do
  programa. Gêmeos em UTF-8 resolveriam de vez.
- **Coorientador nas páginas de resumo.** Hoje só os orientadores são
  listados ali. O formato daquela página é tradição da COPPE, não
  exigência do manual — decidir antes de mexer.
- **Fólio a 2 cm da borda superior.** Está a ~2,15 cm; 2.7 diz 2 cm.
- **Banca grande com a opção `assinaturas`.** Com 7 membros pode estourar
  a folha; testado até 5.

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

*Última atualização: setembro de 2026, branch `nlinguas`.*
