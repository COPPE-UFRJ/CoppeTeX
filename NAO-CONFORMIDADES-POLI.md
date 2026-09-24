# Não conformidades da Resolução 05/2012 da Escola Politécnica

Este documento confere, ponto a ponto, o **Anexo da Resolução n.º 05, de 2012 —
Estabelece Normas de Elaboração Gráfica do Projeto de Graduação** da Escola
Politécnica (em `specs/`) contra o **Manual para elaboração e normalização de
trabalhos acadêmicos** da UFRJ/SiBI, 9.ª ed. rev. (2026), daqui em diante
*Manual UFRJ 2026*.

**A regra de desempate é a do projeto**, e ela é simples: a norma da UFRJ é mais
nova e vale sobre a da unidade. Onde a Resolução da Poli **contraria** o Manual,
a Resolução está superada, e a implementação segue o Manual. Onde ela apenas
**escolhe** entre alternativas que o Manual deixa em aberto, ou acrescenta um
dado que só a Escola tem, a escolha vale e está implementada no `ufrj-poli.sty`.

Cada item abaixo diz o que a Resolução manda, o que o Manual manda, o veredito e
o que a classe faz hoje.

---

## 1. Conflitos: a Resolução está superada

### 1.1 Corpo da letra — Arial 11

- **Resolução:** "letra de tamanho equivalente a Times New Roman 12 ou Arial 11";
  títulos até "Times New Roman 24 ou Arial 22".
- **Manual (2.2b):** "utilizando **fonte tamanho 12**", com fonte menor e
  uniforme para citações longas, notas, paginação e legendas.
- **Veredito:** o corpo do texto é **12**. O "Arial 11" está superado. A
  *família* não é fixada pelo Manual, e a escolha da Escola vale — veja 2.1.

### 1.2 Espaçamento de 2 (duplo)

- **Resolução:** "em espaço 1,5 ou 2 (duplo)".
- **Manual (2.4):** a parte textual é digitada em **espaço 1,5**, com espaço
  simples nos casos que ele lista (citações longas, notas, referências, títulos
  e fontes de ilustrações, ficha, natureza na folha de rosto).
- **Veredito:** espaço 1,5. O duplo está superado. (A classe tem a opção
  `doublespacing`, que existe para revisão, e não para o depósito.)

### 1.3 Margens de 30 mm à direita

- **Resolução (Anexo VII):** superior 25 mm, esquerda e direita 30 mm, inferior
  25 mm.
- **Manual (2.3):** esquerda 3 cm, superior 3 cm, **direita 2 cm**, inferior
  2 cm.
- **Veredito:** as margens são as do Manual. A classe já as compõe, e o
  `tools/conferir-norma.py` as mede no PDF pronto.

### 1.4 Numeração das folhas pré-textuais em romanos

- **Resolução:** "a numeração destas páginas deve ser feita por letras romanas
  minúsculas: i, ii, iii…".
- **Manual (2.7):** as folhas pré-textuais são **contadas e não numeradas**; o
  fólio em arábico aparece a partir da parte textual, no canto superior direito.
- **Veredito:** sem romanos. A classe tem a opção `numeraisromanos` para quem
  precisar do comportamento antigo, e ela **não** é o padrão.

### 1.5 Capítulos numerados em algarismos romanos

- **Resolução:** "Os capítulos existentes devem ser numerados em algarismos
  romanos ou arábicos".
- **Manual (NBR 6024, 2.6):** numeração progressiva em **arábicos**.
- **Veredito:** arábicos.

### 1.6 Ordem dos pré-textuais: sumário antes das listas

- **Resolução:** capa, folha de rosto, folha de aprovação, ficha, dedicatória,
  agradecimentos, resumos, **sumário**, listas de figuras, tabelas e símbolos.
- **Manual (3.1.2):** folha de rosto, folha adicional (com a ficha), errata,
  folha de aprovação, dedicatória, agradecimentos, epígrafe, resumo em língua
  vernácula, resumo em língua estrangeira, **listas**, e o **sumário por
  último**.
- **Veredito:** a ordem é a do Manual, e a classe a confere: fora dela, é erro
  de compilação, em qualquer classe do projeto.

### 1.7 Ficha catalográfica desenhada à mão

- **Resolução:** ficha de 60 caracteres de largura num quadro de 120 mm, com
  margens de 10 mm/5 mm e parágrafos descritos um a um; "Projeto de Graduação —
  UFRJ/ POLI/ Curso de Engenharia do Petróleo, 2008".
- **Manual (3.1.2.1.2):** a ficha vem na **folha adicional**, gerada pelo
  Gerador de Fichas Catalográficas do SiBI (`fichacatalografica.sibi.ufrj.br`),
  segundo as regras AACR2.
- **Veredito:** a ficha é a do gerador do SiBI. A classe reserva o espaço e
  inclui o PDF que o gerador devolve (`\fichacatalografica`).

### 1.8 Folha de aprovação em caixa alta, com linhas de assinatura

- **Resolução (Anexo III):** bloco inteiro em maiúsculas ("PROJETO DE GRADUAÇÃO
  SUBMETIDO AO CORPO DOCENTE…"), "Examinada por:", linhas de assinatura, cidade,
  estado e país em maiúsculas, mês e ano em maiúsculas.
- **Manual (3.1.2.1.3 e Anexo D):** autor, título, natureza alinhada do meio da
  mancha para a direita, data de aprovação e a banca com nome, titulação e
  instituição.
- **Veredito:** a folha é a do Manual.

### 1.9 Legenda das figuras abaixo da ilustração

- **Resolução:** "As legendas das tabelas devem ser posicionadas imediatamente
  acima das mesmas, e as das figuras, imediatamente abaixo delas".
- **Manual (2.10):** para **toda** ilustração, a identificação vem **acima** e a
  **fonte é obrigatória**, abaixo.
- **Veredito:** legenda em cima, fonte embaixo, para figuras e tabelas.

### 1.10 Referências e citações pela NB-66

Este é o conflito mais extenso, e a decisão é a mais firme: **a bibliografia
segue estritamente a norma da UFRJ; toda diferença apresentada na Resolução é
tida como errada.**

- **Resolução (3.1):** duas formas baseadas na **NB-66** (norma da ABNT
  substituída em 1989), com: número da referência entre colchetes precedido do
  sobrenome ("IESAN [2] determinou"); título do livro grifado; "pp." antes das
  páginas; título de artigo entre aspas; até três autores citados e "et al." em
  itálico a partir do quarto; ano logo depois do autor; URL entre `<` e `>`.
- **Manual (4.1 e 4.2):** **NBR 10520:2023** para as citações e **NBR
  6023:2025** para as referências, nas edições que o próprio Manual cita.
- **Veredito:** vale o Manual, item por item. Continua valendo da Resolução
  apenas a **escolha entre os dois sistemas de chamada** — numérico ou
  autor-data —, que o Manual também admite (4.1.1.1) e a classe oferece na
  opção `numbers`.

### 1.11 Resumo com o cabeçalho da Escola

- **Resolução (Anexos V e VI):** "Resumo do Projeto de Graduação apresentado à
  Escola Politécnica/UFRJ como parte dos requisitos…", título, autor, mês/ano,
  "Orientador:" e "Curso:".
- **Manual (3.1.2.1.4 e Anexo E):** o título da folha, a referência do trabalho,
  o texto e as palavras-chave.
- **Veredito:** a folha é a do Anexo E. Os elementos da Resolução continuam
  disponíveis na classe, desligados por padrão (`\configuraresumos`), para o
  caso de a Escola os exigir.

### 1.12 Capa azul-rei com letras douradas

- **Resolução (Anexo I):** "Cor da Capa: Azul Rei. Cor da Letra: Dourada", com
  lombada.
- **Manual (Anexo A):** modelo de capa branca, com os dois logotipos, o nome da
  instituição, autor, título, cidade e ano.
- **Veredito:** a capa é a do Manual. A capa dura colorida era da via impressa
  encadernada; o depósito hoje é digital, em PDF/A. A lombada (NBR 12225) não é
  composta pela classe.

### 1.13 Lista de símbolos por capítulo

- **Resolução:** admite, como alternativa, uma lista de símbolos no início de
  cada capítulo.
- **Manual (3.1.2.1.6 e 4.1.1):** a lista de símbolos é elemento pré-textual,
  única.
- **Veredito:** lista única, pré-textual.

---

## 2. Escolhas da Escola que continuam valendo

### 2.1 Família da letra: Times New Roman ou Arial

O Manual fixa o **tamanho** (12) e não nomeia família; a Resolução nomeia duas.
A escolha vale, e o estilo a oferece:

```latex
\usepackage[times]{ufrj-poli}   % família com serifa, no desenho do Times
\usepackage[arial]{ufrj-poli}   % família sem serifa, no desenho do Arial
```

O corpo continua 12, como o Manual manda — a Resolução fala em "tamanho
equivalente", e é o tamanho que o Manual fixa. Sem opção nenhuma, vale a fonte
da classe (Latin Modern), que é a testada com o PDF/A e com a matemática.

### 2.2 Sistema de chamada: numérico ou autor-data, a critério do autor

A Resolução deixa a escolha ao autor, e o Manual também (4.1.1.1). Na classe,
`numbers` escolhe o numérico; sem ela, autor-data. O que **não** vale é o
formato das referências da Resolução (1.10).

### 2.3 Resumo com até 250 palavras

O Manual admite até 500 (3.1.2.1.4); a Escola é mais restritiva, e uma
restrição dentro do limite é escolha legítima. A classe não conta palavras: a
regra fica com o autor e com o orientador.

### 2.4 Nome do curso: "Curso de Engenharia X"

A Resolução nomeia o curso em toda folha em que ele aparece — folha de rosto,
ficha ("UFRJ/ Escola Politécnica/ Curso de Engenharia do Petróleo"), folha de
aprovação ("CURSO DE ENGENHARIA DE PETRÓLEO") e resumo ("Curso: Engenharia do
Petróleo"). É dado da unidade, e está implementado: a capa traz "CURSO DE
ENGENHARIA X", a natureza diz "apresentado ao Curso de Engenharia X" e a
referência do resumo, "(Graduação em Engenharia X)".

### 2.5 Logotipos

A Resolução é de 2012 e não trata deles; o Manual (Anexo A) põe o logotipo da
UFRJ à esquerda e o da unidade à direita. É o que a classe faz, com a **marca
principal colorida** da Escola à direita. O preto e branco que circula em
documentos da Escola é limitação de impressão, e não a marca.

### 2.6 Parte textual em português

A Resolução manda a parte textual em português, admitindo inglês ou espanhol
com justificativa; o Manual admite os três idiomas (art. 57 da Resolução CEPG
302/2024). A exigência de justificativa é da Escola, e não afeta a formatação.

---

## 3. O que a Resolução pede e a classe não faz

- **Lombada** (NBR 12225): a classe não a compõe.
- **Papel, gramatura e encadernação**: são da via impressa; o depósito é
  digital.
- **Contagem de palavras do resumo**: não é conferida pela classe.
- **Impressão em preto**: a classe compõe em preto, e a cor fica por conta das
  ilustrações do autor.

---

## 4. Como este documento é usado

Ele é a base da **proposta de resolução nova** da Escola
(`src/PROPOSTA-DE-RESOLUCAO.tex`), que assume o Manual UFRJ 2026 por inteiro e
guarda da Resolução 05/2012 apenas o que está na seção 2 acima.
