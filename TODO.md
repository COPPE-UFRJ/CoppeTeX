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

- **CTAN** — pacote a partir de `dist/` mais os dois `.dtx` e os dois `.ins`
  (`src/ufrj.*` e `src/ufrj-coppe.*`), que bastam para reconstruir a
  distribuição. Os nomes da 5.0 já têm o prefixo `ufrj`, que evita colisão com
  outro pacote da TeX Live. Issue #14.
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
- **A natureza da folha de rosto no idioma principal?** A seção 4 da Norma COPPE
  diz que a natureza acompanha o idioma principal; a classe a escreve em
  português em qualquer idioma (conferido no `example_en.pdf`). Decidido na 5.0
  deixar para depois. O texto já está pronto para isso: a natureza é a chave
  `natureza`, lida no idioma principal e, na falta, em português. Seguir a
  Norma é escrever a chave em inglês e em espanhol, com teste regressivo;
  manter é corrigir a seção 4.
- **Escolhas de comportamento por unidade.** Na 5.0 o estilo de unidade traz só
  identidade — nomes, Programas, logotipos, frases. As escolhas da Norma COPPE
  que são comportamento (orientador e Programa no resumo, referência no alto do
  resumo, orientador na banca) continuam padrão da classe. Uma unidade que
  precise de outro padrão pede um mecanismo novo: o `\usepackage` do estilo roda
  depois das opções da classe, e a classe teria de distinguir o que o autor
  pediu explicitamente para o estilo não passar por cima.
- **O gerador de documento só conhece a COPPE.** `tools/geradocvazio.py`
  escreve `\usepackage{ufrj-coppe}` e tem a própria lista dos treze Programas,
  cópia da que está no `ufrj-coppe.dtx`. Com uma segunda unidade, ele tem de
  perguntar a unidade e ler os Programas do estilo.
- **Autoria do `manual.pdf`.** O manual da norma passou a tratar da UFRJ, com a
  COPPE como exemplo, mas continua assinado pela CPGP da COPPE, que o
  encomendou. Decidir se muda.
- **A 5.0 e a proposta à CPGP.** `PROPOSTA_CPGP.md`, `CARTA_CPGP.md` e a seção
  *The proposal for CPGP* do `README.md` foram escritos para a 4.1 e falam da
  classe `coppe`; o aviso do topo do `README.md` diz isso. Decidir se a 5.0 vai
  à votação no lugar da 4.1 — e então reescrever os três — ou se a 4.1 é votada
  e a 5.0 vem depois.

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

*Última atualização: 15 de setembro de 2026.*
