# src/ — a fonte, e como mexer nela

## Leia isto antes de editar qualquer coisa

**Os três `.dtx` são a fonte única.** Tudo o que a CoppeTeX distribui sai
deles. Do `ufrj.dtx`, por `pdflatex ufrj.ins`: a classe, os estilos de
bibliografia, os pacotes de idioma, as bases `.bib`, o estilo do glossário, o
guia rápido e a receita de compilação. Do `ufrj-coppe.dtx`, por
`pdflatex ufrj-coppe.ins`: o estilo da COPPE, a classe `coppe` de
compatibilidade, os exemplos e a montagem das capas. Do `ufrj-poli.dtx`, por
`pdflatex ufrj-poli.ins`: o estilo da Escola Politécnica, a classe `poli` de
compatibilidade e o exemplo dela. Nenhum desses arquivos é escrito à mão, e
**toda edição feita neles se perde na próxima geração, sem aviso**.

Se você quer mudar o comportamento da classe, mude o `ufrj.dtx`. Se quer mudar
o que é da COPPE — um Programa, o logotipo, uma frase —, mude o
`ufrj-coppe.dtx`. **A classe não nomeia unidade nenhuma**, e isso também é
cobrado: `tests/regressivo/rtu04` lê o código que o `ufrj.ins` gera e reprova
qualquer menção à COPPE.

**Nada do que é gerado mora aqui.** Desde outubro de 2026, `src/` só tem fonte:
o `tools/distribuicoes.py` copia as fontes para `../build/`, roda os três `.ins`
lá, e é de `build/` que saem as distribuições (`../dist-coppe`, `../dist-poli`,
`../dist-biblatex`) e as normas (`../normas`). `build/` fica fora do git. O
teste `tests/regressivo/rtu14` reprova qualquer arquivo gerado que volte a ser
versionado em `src/`.

## O que é fonte e o que é gerado

Gerado em `../build/` — **não edite, e não traga para cá**:

| Arquivo | O que é |
|---|---|
| `ufrj.cls` | A classe. |
| `ufrj-coppe.sty` | O estilo da COPPE: o Instituto, os Programas, o logotipo da direita, as frases e a norma do colofão. Sai do `ufrj-coppe.dtx`. |
| `coppe.cls` | A classe de compatibilidade, para trabalho começado com `\documentclass{coppe}`. Sai do `ufrj-coppe.dtx`. |
| `ufrj.dbx`, `ufrj.bbx`, `ufrj.cbx` | Tipos de entrada e estilo de bibliografia e citação, em autor-data. |
| `ufrj-numeric.bbx`, `ufrj-numeric.cbx` | O mesmo, no sistema numérico (opção `numbers`). |
| `brazilian-`, `english-`, `spanish-`, `french-`, `italian-ufrj.lbx` | Termos de bibliografia por idioma. |
| `ufrj-lang-spanish.def`, `-french.def`, `-italian.def` | Textos fixos da classe nesses idiomas. Português e inglês vivem dentro da classe. |
| `ufrj.ist` | Estilo de ordenação do glossário e das listas de siglas e símbolos. |
| `ufrj.bib`, `exemplo.bib` | Bases de referências: a do manual da classe e a dos exemplos. |
| `coppe-min-exemplo.tex`, `coppe-max-exemplo.tex` | Os exemplos em português: só o obrigatório, e tudo. Saem do `ufrj-coppe.dtx`. |
| `example_pt`, `_en`, `_es`, `_fr`, `_it` `.tex` | Os demos de idioma. Saem do `ufrj-coppe.dtx`. |
| `covers_5languages.tex` | A montagem das capas lado a lado. Sai do `ufrj-coppe.dtx`. |
| `ufrj-quickref.tex` | O guia rápido da CLASSE, em inglês. |
| `coppe-quickref.tex` | O guia rápido da COPPE, em inglês (gerado do `ufrj-coppe.dtx`). |
| `poli-quickref.tex` | O guia rápido da Escola Politécnica, em inglês (gerado do `ufrj-poli.dtx`). |
| `latexmkrc.tex` | A receita de compilação (veja a nota sobre o nome, abaixo). |
| `ufrj.pdf`, `ufrj-coppe.pdf`, `ufrj-poli.pdf` | Os manuais da classe e de cada estilo, compostos dos próprios `.dtx`. |
| `poli.cls`, `ufrj-poli.sty`, `poli-*-exemplo.tex` | O estilo da Escola Politécnica, a classe de compatibilidade e os exemplos. Saem do `ufrj-poli.dtx`. |
| `manual.pdf`, os PDFs dos exemplos e das folhas de consulta | Compilados pelo `tools/build-check.ps1`. |

Fonte — **é aqui que se mexe**:

| Arquivo | O que é |
|---|---|
| `ufrj.dtx` | A classe inteira. Código e documentação no mesmo arquivo. |
| `ufrj.ins` | A lista do que gerar do `ufrj.dtx`. Só muda quando nasce um arquivo novo. |
| `ufrj-coppe.dtx` | O estilo da COPPE, a classe `coppe` de compatibilidade e os exemplos. É também o modelo do estilo de outra unidade. |
| `ufrj-coppe.ins` | A lista do que gerar do `ufrj-coppe.dtx`. |
| `ufrj-poli.dtx`, `ufrj-poli.ins` | O estilo da Escola Politécnica, a classe `poli` de compatibilidade e os exemplos dela. |
| `logos/` | Logotipos da capa: o da UFRJ é da classe; o da COPPE e o da Poli, dos estilos. Binários, não saem de `.dtx` nenhum. |
| `manual.tex` | O manual da NORMA: como o trabalho tem de sair. Não confundir com `ufrj.pdf`, que é o manual da classe. |
| `normas/` | As normas de cada unidade, **em Word** (`norma-coppe/NORMA_COPPE_2026.docx`, `norma-poli/NORMA_POLI_2026.docx`) — o `.docx` é a fonte; o gerador faz o PDF. Em `norma-coppe/cpgp/`, os documentos do processo na CPGP. |
| `distribuicao/` | O que cada distribuição leva além do gerado: o `README.md` de cada uma, os guias de migração (`coppe/`) e o documento de exemplo do biblatex avulso (`biblatex/`). |
| `gerador/` | O gerador de trabalho novo, `coppetex-novo.bat` + `geradocvazio.py`. É ferramenta do ALUNO e vai na `dist-coppe`. |

## Como os `.dtx` são organizados

São arquivos `.dtx`, o formato padrão de LaTeX para código documentado. Duas
regras bastam para ler e escrever neles:

1. **Linha que começa com `%` é documentação**, e vira o manual (`ufrj.pdf` ou
   `ufrj-coppe.pdf`). Linha que não começa com `%` é código, e vai para o
   arquivo gerado.
2. **`%<*nome>` e `%</nome>` delimitam um módulo.** O `.ins` diz qual módulo
   vai para qual arquivo. No `ufrj.ins`, o módulo `class` vira `ufrj.cls` e o
   `bbx` vira `ufrj.bbx`; no `ufrj-coppe.ins`, o `package` vira
   `ufrj-coppe.sty`, o `compat` vira `coppe.cls` e o `maxexemplo` vira
   `coppe-max-exemplo.tex`; e assim por diante.

Um trecho típico, dentro do módulo `class`:

```
% \begin{macro}{\linhapesquisa}
% A linha de pesquisa, impressa na folha de rosto.   <- vai para o manual
%    \begin{macrocode}
\newcommand\ufrj@linhapesq{}                        <- vai para ufrj.cls
\newcommand\linhapesquisa[1]{\gdef\ufrj@linhapesq{#1}}
%    \end{macrocode}
% \end{macro}
```

O `ufrj.dtx` tem, na ordem: o cabeçalho com a versão e o histórico de mudanças;
o manual de uso, que é a parte que o autor de uma tese lê; e depois os módulos
de código, cada um com sua documentação intercalada. O `ufrj-coppe.dtx` segue o
mesmo desenho, em miniatura: o que é da COPPE, os exemplos, e a implementação
do estilo, que é uma lista de declarações.

## O ciclo de trabalho

```powershell
# 1. edite src\ufrj.dtx (a classe), src\ufrj-coppe.dtx ou src\ufrj-poli.dtx
# 2. gere os derivados em build\ e compile o que interessa
.\tools\build-check.ps1 -Scope example
# 3. quando estiver pronto, refaça as distribuições
.\coppetex.bat --distribuir
```

Fora do Windows, `python3 tools/distribuicoes.py --regerar` faz o passo do
docstrip, e `python3 tools/distribuicoes.py` faz docstrip, normas e montagem.

Os escopos do `build-check.ps1` vão do mais rápido ao mais completo: `class` só
regenera; `example` compila os dois exemplos; `langs`, os cinco idiomas; `tests`, a
suíte de regressão; `docs`, o manual e a norma; `pdfa`, o que passa pelo
veraPDF; `adversativa`, os seis documentos de prova nos dois motores; `all`,
tudo; `prova`, tudo mais a verificação de fonte única e um veredito.

Enquanto se trabalha, `tools\watch-build.ps1` fica observando e compila sozinho
a cada pedido. Nada disso escreve fora de `build\`, que o git ignora.

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
9.ª ed. rev. (2026), que está em `specs/`, mais a norma própria de cada
unidade, em `src/normas/`. Onde a norma não manda nada, a escolha é do autor da tese
e deve virar opção de classe, não decisão embutida.

**Quebrou compatibilidade? Escreva onde se lê.** Vai no histórico do `.dtx`, no
`CHANGELOG.md` e no guia de migração da versão (`distribuicao/coppe/MIGRATION_v4_to_v5.md` é o
mais recente), com a regra de conversão. Quem está
escrevendo uma tese há dois anos não lê commit.

**Toda mudança de comportamento ganha um teste.** Em `tests/`, se for um ponto
isolado; no gerador de `../tests/adversativa/`, se for uma opção que interage
com outras; em `../tests/regressivo/`, se for a correção de um defeito.
O teste tem de falhar antes da correção e passar depois.

## Duas armadilhas conhecidas

**O `latexmkrc` sai com o nome errado, de propósito.** O `\openout` do TeX
acrescenta `.tex` a todo nome sem extensão e recusa nome começado por ponto, de
modo que não há como pedir a ele um arquivo chamado exatamente `latexmkrc`. O
módulo gera `latexmkrc.tex`, e o `tools/distribuicoes.py` copia por cima do
`latexmkrc`. Quem roda o `ufrj.ins` à mão copia também.

**`\newfloat` define o ambiente localmente.** Se você envolver a criação de um
flutuante num grupo, ele desaparece quando o grupo fecha, e o documento falha com
"ambiente indefinido" longe dali. Isso já aconteceu uma vez, com
`\newufrjfloat`; o comentário no `.dtx` guarda a história.

## Onde fica o resto

- `../build/` — onde tudo é gerado e compilado (fora do git).
- `../dist-coppe/`, `../dist-poli/`, `../dist-biblatex/` — as distribuições, geradas.
- `../normas/` — as normas em Word e PDF, geradas de `normas/`.
- `../tools/` — o harness e o gerador das distribuições (`distribuicoes.py`). Tem README próprio.
- `../tests/` — a suíte de regressão; `../tests/adversativa/`, os seis documentos que acionam tudo.
- `../specs/` — as especificações que tudo isto implementa.
- `../CONTRIBUTING.md` — como acrescentar um pacote de idioma ou uma unidade.
