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

## 3. Classe e documentação

- **Tempo de compilação no Overleaf gratuito.** Os dois defeitos que pesavam
  entraram (`morewrites` sem fluxos reais; `.aux` que nunca estabilizava, #98):
  o `latexmk` do exemplo completo foi de 75 s com erro para 58 s limpo. Faltam as
  decisões das propostas do issue #95 — sobretudo documentar para o aluno
  `\includeonly` e o modo *draft* do Overleaf.
- **Tornar `pdfa` o padrão da classe?** Os dois exemplos já compilam com ela, é
  PDF/A-2b conforme pelo veraPDF e o custo de tempo é desprezível. Falta decidir
  se a classe liga por padrão, com uma opção `sempdfa` para desligar.
- **Palavras-chave no dicionário de informação do PDF sob `pdfa`.** Com a opção,
  `pdfinfo` mostra título, autor e assunto, mas não *Keywords* (sem a opção,
  mostra). Conferir se elas estão no XMP e, se não estiverem, fazê-las chegar.

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
