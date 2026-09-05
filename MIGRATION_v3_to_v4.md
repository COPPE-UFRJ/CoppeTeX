# Migration guide — CoppeTeX v3.x → v4.0

Short guide for thesis authors currently using CoppeTeX v3.x who want to
move to v4.0. Read once, do at most one of the three sections below
depending on your situation, and you are done.

---

## TL;DR

| Your situation                                                          | Action required                          |
| ----------------------------------------------------------------------- | ---------------------------------------- |
| Portuguese-main thesis (`\documentclass[dsc]{coppe}`)                   | **None.** Just replace `coppe.cls`.       |
| English-main thesis (`\documentclass[english,dsc]{coppe}`)              | **None.** Just replace `coppe.cls`.       |
| You want to write the thesis in Spanish, French or Italian              | See Section 3 below.                     |

---

## 1. Portuguese-main thesis: nothing to do

If your `\documentclass` line is one of:

```latex
\documentclass[dsc]{coppe}
\documentclass[msc]{coppe}
\documentclass[brazilian,dsc]{coppe}
\documentclass[dscexam]{coppe}
\documentclass[mscexam]{coppe}
```

— or any combination of these with `numbers`, `doublespacing`,
`numeraisromanos`, etc. — **your document compiles bit-for-bit
identically under v4.0**. We have verified this with a
page-by-page rendered-image diff against a v3.8 build.

What to do:

1. Replace `coppe.cls`, `coppe.bbx`, `coppe.cbx`, `coppe.dbx`,
   `brazilian-coppe.lbx`, `english-coppe.lbx`, `coppe-numeric.bbx`,
   `coppe-numeric.cbx` and `coppe.ist` in your project (or local TEXMF)
   with the v4.0 versions from
   <https://github.com/COPPE-UFRJ/CoppeTeX/tree/master/dist>.
2. Recompile. Output should be visually identical.

Nothing in your `.tex` source changes.

---

## 2. English-main thesis: nothing to do

If your `\documentclass` line includes `english`:

```latex
\documentclass[english,dsc]{coppe}
```

— same story as Section 1. The `english` option keeps the exact same
semantics, the cover keeps the same institutional Portuguese template
with your English title on it, `\title{...}` and `\foreigntitle{...}`
keep their historical meaning (`\title` = Portuguese version of the
title, `\foreigntitle` = English version), and `\begin{foreignabstract}`
still produces the Brazilian-Portuguese abstract page. We have verified
byte-identical output.

What to do: same as Section 1 — replace the class files, recompile.

---

## 3. Writing in Spanish, French or Italian: three small additions

This is the new capability in v4.0. Suppose you want to write your
thesis in Spanish. Then:

### 3.1 Change the class option

```latex
\documentclass[spanish,dsc]{coppe}
```

Replace `spanish` with `french` or `italian` as appropriate.

### 3.2 Install the language pack files

Two files must sit next to `coppe.cls` (in your project directory, or in
a `TEXMF` location), both shipped in `dist/`:

- `coppe-lang-spanish.def` (class-level strings)
- `spanish-coppe.lbx` (bibliography strings)

(Use `french` or `italian` in the file names accordingly.)

If you forget either, the class will tell you so with a clear error.

### 3.3 Add a Spanish title via `\titlein`

The historical `\title{...}` still expects the Portuguese title and
`\foreigntitle{...}` still expects the English title. For a Spanish-main
thesis, the title shown on the cover is read from a new slot — set with:

```latex
\title{Título em portugu\^es}                % traditional
\foreigntitle{English title}                  % traditional
\titlein{spanish}{T\'itulo en espa\~nol}      % NEW -- the cover prints this
```

For French use `\titlein{french}{...}`; for Italian, `\titlein{italian}{...}`.

### 3.4 (Optional) Add a Portuguese abstract for the banca

When your main language is not Portuguese and you want a Portuguese
resumo for the Brazilian examiners (in addition to the abstract in the
main language and the foreign English abstract), use the new
`brazilianabstract` environment:

```latex
\begin{abstract}        ... main-language abstract ...    \end{abstract}
\begin{foreignabstract} ... English abstract ...          \end{foreignabstract}
\begin{brazilianabstract} ... Resumo em portugu\^es ...   \end{brazilianabstract}
```

This is the only place where the abstract layout is genuinely new.

### 3.5 Done.

The full layout, the cover, the folha de rosto, the ficha catalográfica,
the running heads, the references list — everything else is automatic
and respects the main language.

---

## 4. v4.1: alinhamento com o Manual UFRJ/SiBI 2026

A 9.ª edição revista do manual do SiBI (2026) mudou exigências que a
classe implementa. **Nenhum documento existente precisa ser alterado para
continuar compilando** — as mudanças abaixo são de comportamento e de
API compatível.

### 4.1 O que muda sozinho, sem você tocar em nada

| Antes | Agora |
|---|---|
| Margens espelhadas (`twoside` + `bindingoffset`) | Uma face: esquerda 3 cm, direita 2 cm em toda folha (2.3) |
| Versos em branco do `\cleardoublepage` | Somem — o `example.pdf` caiu de 76 para 53 páginas |
| Numeração reiniciando em 1 na Introdução | Contagem contínua desde a folha de rosto (2.7) |
| Ficha catalográfica no verso da folha de rosto | Folha adicional própria, logo após a folha de rosto (3.1.2.1.2) |
| Título antes do autor na folha de aprovação | Autor antes do título, sem caixa alta (3.1.2.1.3) |
| Cidade e data no rodapé da folha de aprovação | Removidos; entra "Aprovada em:" |
| `"Aprovada por:"` sempre em português | Acompanha o idioma principal |
| Titulação passada a `\examiner` e nunca impressa | Impressa |

Quem for **imprimir** e quiser as margens espelhadas de volta usa a opção
de classe `twoside`.

### 4.2 A ficha catalográfica saiu da sua responsabilidade

Desde agosto de 2026 a ficha vem do gerador do SiBI
(<http://fichacatalografica.sibi.ufrj.br/>) ou da biblioteca do seu
Programa, dentro de uma folha adicional que o **Programa** preenche.

```latex
\fichacatalografica{ficha.pdf}   % o PDF gerado pelo SiBI
```

Sem esse comando, a folha sai com uma moldura vazia indicando onde obter
a ficha. Durante a redação, a opção de classe `rascunhoficha` põe no lugar
a ficha composta pela própria classe — **nunca válida para depósito**.

### 4.3 Campos novos do preâmbulo

Nenhum é obrigatório; o que faltar sai como linha para preencher à mão.

```latex
\areaconcentracao{Engenharia de Sistemas e Computação}
\linhapesquisa{Engenharia de Dados e Conhecimento}
\dataaprovacao{15 de setembro de 2026}

% folha adicional (Coleta CAPES)
\tipoproducao{bibliografica}   % bibliografica | artistica | tecnologica | tecnica
\projetovinculado{sim}         % sim | nao
\nomeprojeto{Nome do projeto de pesquisa}
\agenciafomento{Conselho Nacional de Desenvolvimento Científico e Tecnológico}{CNPq}
```

`\areaconcentracao` não serve só à folha adicional: 3.1.2.1.1(e) e
3.1.2.1.3(c) exigem a área de concentração também no bloco de natureza da
folha de rosto e da folha de aprovação.

### 4.4 `\advisor` e `\examiner` ganharam a instituição

**Mudança de API, compatível para trás.** A instituição entra como
argumento **opcional**, antes dos demais:

```latex
% antes -- continua funcionando, apenas sem instituição
\advisor{Prof.}{Nome}{Sobrenome}{D.Sc.}
\examiner{Prof.}{Nome Sobrenome}{D.Sc.}

% agora
\advisor[UFRJ]{Prof.}{Nome}{Sobrenome}{D.Sc.}
\examiner[UFF]{Prof.}{Nome Sobrenome}{D.Sc.}
```

Duas consequências para quem já usava `\examiner`:

1. O terceiro argumento (a titulação) **era descartado silenciosamente** e
   agora é impresso. Se você vinha passando algo que não é titulação
   naquele lugar, isso agora aparece na folha de aprovação — confira.
2. Orientadores e examinadores viraram **uma lista só**, com os
   orientadores em primeiro lugar, por presidirem a banca
   (3.1.2.1.3(e)). O bloco "Orientadores:" separado deixou de existir
   nessa página. Se você listava o orientador também como `\examiner`,
   ele agora aparece duas vezes — remova a duplicata.

A opção de classe `assinaturas` troca a lista compacta por uma régua de
assinatura por membro, como no Anexo D do manual.

### 4.5 PDF/A no depósito

2.2(d) exige a entrega em PDF/A, e o Anexo I do manual só ensina a
conversão por Word, LibreOffice, Acrobat ou sites — nada que sirva a quem
escreve em LaTeX. A classe passa a produzir o arquivo diretamente:

```latex
\documentclass[dsc,pdfa]{coppe}
```

A opção é **opcional por ora**, não o padrão: as restrições do PDF/A podem
esbarrar em imagens ou pacotes que o seu texto use. Ligue-a ao preparar a
versão de depósito e confira que o documento ainda compila.

O nível é o **PDF/A-2b**. O Anexo I fala em "ISO 19005-1", que é o a-1b,
mas esse nível proíbe transparência — que o `tcolorbox` e vários pacotes
gráficos produzem — e reprovaria documentos sem defeito algum. O a-2b é a
ISO 19005-2, também listada no Anexo I entre as opções do LibreOffice.

Os metadados XMP (título, autor, palavras-chave, programa) são gerados a
partir do que você já declarou no preâmbulo, num arquivo
`<nome>.xmpdata`. Ele é lido na compilação **seguinte** à que o escreveu;
como o build roda `pdflatex` três vezes, isso é transparente. O arquivo é
gerado, não deve ser versionado nem editado à mão.

Duas observações:

- Se você já convertia o PDF por fora, pode parar. A conversão externa
  costuma rasterizar ou reamostrar, e agora é desnecessária.
- Nenhum validador PDF/A foi executado sobre a saída até aqui. O arquivo
  declara conformidade e satisfaz as verificações estruturais feitas,
  mas vale passá-lo por um validador (veraPDF, ou o pré-voo do Acrobat)
  antes do depósito.

### 4.6 Francês e italiano

O art. 57 da Resolução CEPG n. 302/2024 admite teses e dissertações em
**português, inglês ou espanhol**. Os pacotes de francês e italiano
continuam distribuídos como demonstração do mecanismo de extensão, mas
não têm respaldo normativo como idioma de redação de tese na UFRJ.

---

## Frequently asked

> **Will my v3.x tese-em-andamento break if I switch now?**
>
> No, as long as you are not using Spanish/French/Italian. pt/en
> documents are byte-identical.

> **Can I keep v3.x files in some directories and v4.0 in others?**
>
> Yes — each project picks up the `coppe.cls` (and friends) it finds
> first on its TEXMF path. Most students will simply put the v4.0 files
> in their project directory and forget about the global tree.

> **What if I want to use a language not in the built-in five?**
>
> Write a `coppe-lang-<lang>.def` and a `<lang>-coppe.lbx` (use any of
> the shipped Spanish/French/Italian as a template). See
> [`CONTRIBUTING.md`](./CONTRIBUTING.md) for the step-by-step.

> **Do I need to update my `latexmkrc` / Overleaf setup?**
>
> No. The build chain (pdflatex / biber / makeindex) is unchanged.

> **Where is the full reference?**
>
> Section 5.2 "Multilingual support" of the manual
> (`dist/coppe.pdf`).
