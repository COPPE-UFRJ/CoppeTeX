# TODO — o que ainda falta fazer

Só o que está **em aberto**. O que já foi feito está no
[`CHANGELOG.md`](./CHANGELOG.md), no histórico do git e nos *issues* fechados
do GitHub; não se repete aqui. Cada item que tem *issue* aponta para ele, e é
lá que se discute e se fecha.

A norma de referência está em [`specs/`](./specs/): o Manual UFRJ/SiBI (9.ª ed.
rev., 2026 — o nome do arquivo diz 2024, ver `specs/README.md`) e o modelo
oficial da folha adicional da Coleta CAPES. Esses arquivos bastam para conferir
a classe; não falta documento normativo.

---

## 1. Trabalho humano

- **Revisão do pacote de espanhol por falante nativo.** Três escolhas a
  confirmar: `frame` como `Cuadro` (ou `Recuadro`), `depositor` como
  `Solicitante` (terminologia de patentes), `mscdiss` como `Tesis de Maestría`
  (ou `Tesina`). Gerar `example_es.pdf` e pedir a alguém do PESC ou de outro
  Programa que marque o que mudaria.

## 2. Distribuição

- **CTAN** — pacote a partir de `dist/` mais `src/coppe.dtx` e `src/coppe.ins`,
  que bastam para reconstruir a distribuição. Issue #14.
- **Overleaf** — modelo público com o conteúdo de `dist/` e botão "Open in
  Overleaf" no `README.md`. O `latexmkrc` já configura biber e makeindex.
- **Versão 4.1.1** — marcar e publicar o *release* com o que entrou depois da
  tag `v4.1`: `morewrites` com fluxos reais, fontes matemáticas fora da classe,
  UTF-8, exemplo em PDF/A, log do `example.tex` sem aviso.

## 3. Classe e documentação

- **Tempo de compilação do `example.tex` no Overleaf gratuito.** A primeira
  correção (fluxos reais para o `morewrites`) já entrou; a análise do restante
  e as propostas estão no issue #95.
- **Tornar `pdfa` o padrão da classe?** O `example.tex` já compila com ela, é
  PDF/A-2b conforme pelo veraPDF e o custo de tempo é desprezível. Falta decidir
  se a classe liga por padrão, com uma opção `sempdfa` para desligar.
- **`example_pdfa.tex` ficou redundante.** Ele é o `example.tex` com `pdfa`, e o
  `example.tex` agora já tem `pdfa`. Decidir se sai da geração, do
  `build-check.ps1`, da prova e da lista do `dist/`.
- **Palavras-chave no dicionário de informação do PDF sob `pdfa`.** Com a opção,
  `pdfinfo` mostra título, autor e assunto, mas não *Keywords* (sem a opção,
  mostra). Conferir se elas estão no XMP e, se não estiverem, fazê-las chegar.
- **Lista de símbolos: ordem.** A 3.1.2.2.7 do Manual pede a lista "de acordo
  com a ordem que aparece no texto"; a classe ordena alfabeticamente (com chave
  de ordenação opcional). Decidir se muda o padrão ou se oferece as duas.
- **Abreviaturas e siglas em listas separadas.** A 3.1.2.2.6 recomenda listas
  separadas; a classe as reúne numa só. Avaliar uma opção que as separe.

## 4. Higiene do repositório

- **`REVISAO_SIBI.md` desatualizado.** A lista de tarefas da seção final ainda
  tem todas as caixas `[ ]` abertas, mas quase tudo foi feito na série de
  setembro. Marcar o que foi feito, com o commit, ou declarar o documento
  histórico no topo.
- **Metadados do GitHub** — acrescentar os tópicos `latex-class`, `abnt` e
  `biblatex` aos que já existem (`coppe`, `latex`, `ufrj`, `thesis`).
- **`SECURITY.md` e `CODE_OF_CONDUCT.md`** mínimos.

---

## Para retomar em outra máquina

```bash
git clone https://github.com/COPPE-UFRJ/CoppeTeX.git
cd CoppeTeX
coppetex.bat --regerar --testes
```

O trabalho acontece no `master`. O manual do painel é o
[`PAINEL.md`](./PAINEL.md): antes de marcar uma versão,
`coppetex.bat --tudo --regressivo --conferir --dist` tem de sair com
`RESULTADO: tudo passou`. Não vêm pelo git as pastas locais `ABNT/`, `LIXO/`,
`LaTeXManuals/` e `_scratch/`.

*Última atualização: 14 de setembro de 2026.*
