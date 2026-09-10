# src/ — a fonte, e como mexer nela

## Leia isto antes de editar qualquer coisa

**`coppe.dtx` é a fonte única.** Tudo o que a CoppeTeX distribui sai dele, por
`pdflatex coppe.ins`. A classe, os estilos de bibliografia, os pacotes de
idioma, as bases `.bib`, o estilo do glossário, os seis exemplos e a receita de
compilação: nenhum desses arquivos é escrito à mão, e **toda edição feita neles
se perde na próxima geração, sem aviso**.

Se você quer mudar o comportamento da classe, mude o `coppe.dtx`.

Isso é verificado, e não é honra. `tools\prova.ps1` roda `coppe.ins` e pergunta
ao git se algum arquivo que estava limpo mudou. Se mudou, alguém editou um
derivado à mão, a edição acaba de ser perdida, e a prova falha antes de deixar
marcar uma versão.

## O que é gerado e o que é fonte

Gerado — **não edite**:

| Arquivo | O que é |
|---|---|
| `coppe.cls` | A classe. |
| `coppe.dbx`, `coppe.bbx`, `coppe.cbx` | Tipos de entrada e estilo de bibliografia e citação, em autor-data. |
| `coppe-numeric.bbx`, `coppe-numeric.cbx` | O mesmo, no sistema numérico (opção `numbers`). |
| `brazilian-`, `english-`, `spanish-`, `french-`, `italian-coppe.lbx` | Termos de bibliografia por idioma. |
| `coppe-lang-spanish.def`, `-french.def`, `-italian.def` | Textos fixos da classe nesses idiomas. Português e inglês vivem dentro da classe. |
| `coppe.ist` | Estilo de ordenação do glossário e das listas de siglas e símbolos. |
| `coppe.bib`, `example.bib` | Bases de referências. |
| `example.tex` | O exemplo completo, em português. |
| `example_pt`, `_en`, `_es`, `_fr`, `_it`, `_pdfa` `.tex` | Os demos de idioma e a versão PDF/A. |
| `covers_5languages.tex` | A montagem das capas lado a lado. |
| `latexmkrc.tex` | A receita de compilação (veja a nota sobre o nome, abaixo). |
| `coppe.pdf` | O manual de uso, composto do próprio `coppe.dtx`. |

Fonte — **é aqui que se mexe**:

| Arquivo | O que é |
|---|---|
| `coppe.dtx` | Tudo. Código e documentação no mesmo arquivo. |
| `coppe.ins` | A lista do que gerar e de onde. Só muda quando nasce um arquivo novo. |
| `coppe-logo.pdf`, `coppe-logo.eps`, `ufrj-logo.pdf` | Logotipos da capa. Binários, não saem do `.dtx`. |
| `NORMA_COPPE_2026.tex` | A norma da COPPE, documento próprio. |
| `futuremanual2026.tex` | Documento de trabalho sobre a edição de 2026 do manual do SiBI. |

## Como o `coppe.dtx` é organizado

É um arquivo `.dtx`, o formato padrão de LaTeX para código documentado. Duas
regras bastam para ler e escrever nele:

1. **Linha que começa com `%` é documentação**, e vira o manual `coppe.pdf`.
   Linha que não começa com `%` é código, e vai para o arquivo gerado.
2. **`%<*nome>` e `%</nome>` delimitam um módulo.** O `coppe.ins` diz qual
   módulo vai para qual arquivo. O módulo `class` vira `coppe.cls`, o módulo
   `bbx` vira `coppe.bbx`, o módulo `example` vira `example.tex`, e assim por
   diante.

Um trecho típico, dentro do módulo `class`:

```
% \begin{macro}{\linhapesquisa}
% A linha de pesquisa, impressa na folha de rosto.   <- vai para o manual
%    \begin{macrocode}
\newcommand\coppe@linhapesq{}                        <- vai para coppe.cls
\newcommand\linhapesquisa[1]{\gdef\coppe@linhapesq{#1}}
%    \end{macrocode}
% \end{macro}
```

O arquivo tem, na ordem: o cabeçalho com a versão e o histórico de mudanças; o
manual de uso, em inglês, que é a parte que o autor de uma tese lê; e depois os
módulos de código, cada um com sua documentação intercalada.

## O ciclo de trabalho

```powershell
# 1. edite src\coppe.dtx
# 2. gere os derivados e compile o que interessa
.\tools\build-check.ps1 -Scope example
```

Os escopos do `build-check.ps1` vão do mais rápido ao mais completo: `class` só
regenera; `example` compila o exemplo; `langs`, os cinco idiomas; `tests`, a
suíte de regressão; `docs`, o manual e a norma; `pdfa`, o que passa pelo
veraPDF; `adversativa`, os doze documentos de prova nos dois motores; `all`,
tudo; `prova`, tudo mais a verificação de fonte única e um veredito.

Enquanto se trabalha, `tools\watch-build.ps1` fica observando e compila sozinho
a cada pedido. Nada disso escreve fora de `_scratch\`, que o git ignora.

Antes de marcar uma versão, uma vez só:

```powershell
.\tools\prova.ps1
```

## Regras de convivência

**Documente junto com o código, no mesmo lugar.** O `.dtx` existe para isso. Uma
mudança de comportamento que não aparece no manual é uma mudança que ninguém vai
usar, e um comentário solto num arquivo gerado é um comentário que morre na
próxima geração.

**Escreva no histórico.** Toda mudança de comportamento ganha uma linha
`\changes{versão}{data}{o que mudou e por quê}` no cabeçalho do `.dtx`. É de lá
que sai a lista de mudanças do manual.

**Diga por que, não o que.** O código diz o que faz. O comentário existe para
registrar a decisão: qual item da norma exige aquilo, qual alternativa foi
tentada e falhou, qual efeito colateral está sendo evitado. O `.dtx` está cheio
desses, e é o que torna possível mexer nele anos depois.

**Nada de mudar aparência sem norma que sustente.** A classe implementa o
*Manual para elaboração e normalização de trabalhos acadêmicos* da UFRJ/SiBI,
9.ª ed. rev. (2026), que está em `specs/`, mais a norma própria da COPPE, em
`NORMA_COPPE_2026.md`. Onde a norma não manda nada, a escolha é do autor da tese
e deve virar opção de classe, não decisão embutida.

**Quebrou compatibilidade? Escreva onde se lê.** Vai no histórico do `.dtx`, no
`CHANGELOG.md` e no `MIGRATION_v3_to_v4.md`, com a regra de conversão. Quem está
escrevendo uma tese há dois anos não lê commit.

**Toda mudança de comportamento ganha um teste.** Em `tests/`, se for um ponto
isolado; no gerador de `adversativa/`, se for uma opção que interage com outras.
O teste tem de falhar antes da correção e passar depois.

## Duas armadilhas conhecidas

**O `latexmkrc` sai com o nome errado, de propósito.** O `\openout` do TeX
acrescenta `.tex` a todo nome sem extensão e recusa nome começado por ponto, de
modo que não há como pedir a ele um arquivo chamado exatamente `latexmkrc`. O
módulo gera `latexmkrc.tex`, e o `build-check.ps1` copia por cima do
`latexmkrc`. Quem roda o `coppe.ins` à mão copia também.

**`\newfloat` define o ambiente localmente.** Se você envolver a criação de um
flutuante num grupo, ele desaparece quando o grupo fecha, e o documento falha com
"ambiente indefinido" longe dali. Isso já aconteceu uma vez, com
`\newcoppefloat`; o comentário no `.dtx` guarda a história.

## O que está aqui e não deveria

`baseline.pdf`, `example0.pdf`, `example1.*`, `example2.*`,
`documento da COPPE com o formato válido nessa classe e estilo.pdf` e o
`examples.md` que os descreve são material de trabalho da migração para o
`biblatex`, em 2026. Não saem do `.dtx`, não são distribuídos e nenhuma
ferramenta os cita. Estão registrados no
[issue #79](https://github.com/COPPE-UFRJ/CoppeTeX/issues/79), à espera de quem
decida se saem ou mudam de pasta.

O `Makefile` e o `doall.bat` são de antes do harness em PowerShell. O `Makefile`
ainda declara a versão 3.2. Quem trabalha no Windows usa `tools\build-check.ps1`;
quem trabalha no Unix usa o `coppe.ins` direto.

## Onde fica o resto

- `../tests/` — a suíte de regressão.
- `../adversativa/` — doze documentos que acionam tudo ao mesmo tempo.
- `../tools/` — o harness. Tem README próprio.
- `../dist/` — a entrega.
- `../specs/` — a norma que tudo isto implementa.
- `../CONTRIBUTING.md` — como acrescentar um pacote de idioma, e como contribuir
  vindo de fora.
