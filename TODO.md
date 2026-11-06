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

## 0.0. Regressão sob Git Bash (pdftotext) — quase resolvido

> ✅ **O conserto do pdftotext entrou** (2026-11-06): o `medidas.py` acha o
> `pdftotext` do poppler sozinho, e a suíte passa pelo PowerShell **e** pelo Git
> Bash nos 15 testes de medição. **Resta** só o resíduo de `r09`/`r18` sob Bash
> (marcados `(cache)`; passam no PowerShell) — nuance do cache de compilação
> compartilhada do harness, **não** da classe. Histórico abaixo, como referência.

**Não é bug da classe.** Rodada pelo **PowerShell** (pdftotext do poppler, que o
MiKTeX instala), a suíte sai `115 testes, 0 falhas, tudo passou`. Rodada pelo
**Git Bash**, o `pdftotext` que vem primeiro no PATH é o **Xpdf** (de
`C:\Program Files\Git\mingw64\bin`), que **não tem a opção `-bbox`** que o
`tests/regressivo/medidas.py` usa para extrair cada palavra com a caixa (posição)
e para pegar o texto das folhas. Sem `-bbox`, o `medidas` não devolve palavra
nenhuma, e **todo teste que inspeciona o PDF falha por falta de dado** — não por
desconformidade. Verificado em 2026-11-06 (apareceram 19 falhas no Bash e 0 no
PowerShell; as duas reais daquela rodada — `r92` e `rt68` — já foram corrigidas).

**O que fazer (melhoria do harness, não da classe):** o `medidas.py` já avisa por
teste, mas o conserto é não depender da ordem do PATH. Opções, da melhor para a
pior: (a) o `medidas` localizar o `pdftotext` do poppler explicitamente — por
exemplo o do MiKTeX (`...\MiKTeX\miktex\bin\x64\pdftotext.exe`), ou o primeiro
`pdftotext` cujo `-v` diga "poppler" —, e usá-lo sempre; (b) checar `-bbox` UMA vez
no início e **abortar a suíte com uma mensagem só**, em vez de 17 falhas iguais;
(c) deixar documentado que a suíte roda pelo PowerShell/`coppetex.bat`, nunca pelo
Git Bash. Enquanto não houver (a)/(b), **rodar a regressão sempre pelo PowerShell**.

Os 17 testes que deram falso-negativo sob Bash (todos passam no PowerShell), um a
um — o que cada um confere:

- `r09-listas-sem-folio` — as listas de abreviaturas e de símbolos não podem
  levar número de folha.
- `r18-legenda-em-cima-fonte-embaixo` — legenda da ilustração acima, fonte abaixo.
- `rt35-sumario-pos-textuais-na-coluna` — no sumário, Referências/Apêndices/Anexos/
  Índice começam na coluna dos títulos numerados, não na margem.
- `rt37-notas-de-rodape` — 2.ª linha da nota alinhada sob a 1.ª letra; número sem recuo.
- `rt38-referencias-alinhadas-a-esquerda` — lista de referências à esquerda (não justificada).
- `rt39-referencia-do-resumo` — a referência no alto do resumo igual à da lista.
- `rt40-listagem-dentro-da-margem` — números de linha das listagens dentro da margem.
- `rt41-subalineas-com-hifen` — marcador de subalínea certo (sem meia-risca).
- `rt42-espaco-depois-do-titulo` — uma linha em branco entre título e texto.
- `rt43-dedicatoria-e-epigrafe-do-meio` — dedicatória/epígrafe no meio da mancha.
- `rt45-legenda-na-largura-da-ilustracao` — legenda/fonte limitadas à largura da ilustração.
- `rt56-tese-e-dissertacao` — `@mastersthesis`/`@phdthesis` com grau e travessão.
- `rt62-audiovisual-e-versao` — direção não invertida; versão antes da imprenta.
- `rt64-intervalo-de-paginas-com-hifen` — intervalo de páginas com hífen, não meia-risca.
- `rt65-mes-no-idioma-da-publicacao` — mês abreviado no idioma da publicação.
- `rt74-legenda-e-fonte-a-esquerda` — legenda/fonte alinhadas à esquerda (margem da ilustração).
- `rtu16-capa-espaco-entre-blocos` — espaçamento do bloco institucional da capa.

## 0. Levar o `V05-unificada` ao `master`

- **A conferência de 16/09 (#112) está junta com a 5.0 e corrigida**, no ramo
  `V05-unificada`: o `goufrj` mais o `conformidade-manual-2026`, com as issues
  #113 a #153 fechadas uma por commit, e as achadas no caminho (#155, #156).
  Nenhum teste `rt` está marcado `ABERTO`. Falta publicar o ramo, abrir o PR
  para o `master` e decidir se a 5.0 vai à CPGP (item do fim da seção 3).
- **Testes: uma compilação para muitos testes** (#154) — o principal que
  descobre os testes, agrupa os documentos compatíveis e injeta o documento já
  compilado, para a suíte rodar inteira em uma fração do tempo.

## 1. Trabalho humano

- **Revisão do pacote de espanhol por falante nativo.** Três escolhas a
  confirmar: `frame` como `Cuadro` (ou `Recuadro`), `depositor` como
  `Solicitante` (terminologia de patentes), `mscdiss` como `Tesis de Maestría`
  (ou `Tesina`). Gerar `example_es.pdf` e pedir a alguém do PESC ou de outro
  Programa que marque o que mudaria.

## 2. Distribuição

Os dois pacotes já se **geram**, pelo `coppetex.bat --envio`, em `build/` e
fora do git: `build/pacotes/ufrj-<versão>.zip` e
`build/pacotes/CoppeTeX-overleaf-coppe-<versão>.zip`. O que falta nos dois é o
**envio**, que é trabalho humano e feito uma vez.

- **CTAN** — subir o `ufrj-<versão>.zip` em <https://ctan.org/upload>. Ele leva
  a fonte (os `.dtx` e `.ins` da classe e do estilo da COPPE), os manuais, os
  exemplos, os logotipos e a árvore TDS pronta no `ufrj.tds.zip`. O nome do
  pacote é **`ufrj`**, o da classe: é o que se procura no CTAN e o que vai no
  `\documentclass` e no `texmf` de quem instala; CoppeTeX continua sendo o nome
  do projeto. **Confira antes de subir se `ufrj` já não está tomado no CTAN** —
  o formulário recusa nome repetido, e aí o caminho é `coppetex` ou
  `ufrj-thesis`. Faltam duas decisões: a **licença** declarada no formulário (o
  projeto é GPL v3, que o CTAN aceita, embora a LPPL seja a usual em classe
  LaTeX) e **quem assina** o envio. Issue #14.
- **Overleaf** — criar o projeto público a partir do
  `CoppeTeX-overleaf-coppe-<versão>.zip` (New Project → Upload Project →
  Publish as Template) e pôr o botão "Open in Overleaf" no `README.md`. O zip
  já é plano, com todos os idiomas na raiz e um documento principal só, e o
  `latexmkrc` já configura o biber e o makeindex.

## 3. Classe e documentação

- **Tempo de compilação no Overleaf gratuito.** Os dois defeitos que pesavam
  entraram (`morewrites` sem fluxos reais; `.aux` que nunca estabilizava, #98):
  o `latexmk` do exemplo completo foi de 75 s com erro para 58 s limpo. Faltam as
  decisões das propostas do issue #95 — sobretudo documentar para o aluno
  `\includeonly` e o modo *draft* do Overleaf.
- **Palavras-chave no dicionário de informação do PDF sob `pdfa`.** Com a opção,
  `pdfinfo` mostra título, autor e assunto, mas não *Keywords* (sem a opção,
  mostra). Conferir se elas estão no XMP e, se não estiverem, fazê-las chegar.
- **Escolhas de comportamento por unidade.** Na 5.0 o estilo de unidade traz só
  identidade — nomes, Programas, logotipos, frases. As escolhas da Norma COPPE
  que são comportamento (orientador e Programa no resumo, referência no alto do
  resumo, orientador na banca) continuam padrão da classe. Uma unidade que
  precise de outro padrão pede um mecanismo novo: o `\usepackage` do estilo roda
  depois das opções da classe, e a classe teria de distinguir o que o autor
  pediu explicitamente para o estilo não passar por cima. A área de concentração
  na folha de rosto (#155) é hoje uma opção de classe, `areanafolhaderosto`, e
  viraria uma chave da unidade quando o mecanismo existir.
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
[`tools/PAINEL.md`](tools/PAINEL.md): antes de marcar uma versão,
`coppetex.bat --tudo --regressivo --conferir --dist` tem de sair com
`RESULTADO: tudo passou`. Não vêm pelo git as pastas locais `ABNT/`, `LIXO/`,
`LaTeXManuals/` e `_scratch/`.

*Última atualização: 6 de novembro de 2026.*
