# Norma para a Elaboração Gráfica de Teses e Dissertações da COPPE/UFRJ

**Edição 2026 — Proposta para apreciação da CPGP**

Esta Norma, quando aprovada, substitui a *Norma para a Elaboração Gráfica de
Teses/Dissertações* da COPPE/UFRJ aprovada pela CPGP em 15 de julho de 2008
e suas revisões subsequentes (01/10/2009, 10/09/2010 e 26/11/2019).

---

## 1. Documento base e implementação de referência

### 1.1 Documento base

A apresentação gráfica de teses e dissertações da COPPE/UFRJ segue o
**Manual para Elaboração e Normalização de Trabalhos Acadêmicos** da
UFRJ/SiBI, 9.ª edição revista (Rio de Janeiro, 2026) — doravante referido
como *Manual UFRJ 2026* — em conjunto com as adaptações estabelecidas pela
presente Norma.

A edição revista de 2026 incorpora três decisões institucionais que
condicionam diretamente a presente Norma:

- A **Resolução CEPG n. 246/2023**, de 10 de novembro de 2023, que extingue
  a entrega da via impressa à Central de Memória Acadêmica e institui a
  entrega exclusivamente digital do documento final;
- A **Resolução CEPG n. 302/2024**, de 19 de julho de 2024, cujo art. 57
  fixa os idiomas em que teses e dissertações podem ser redigidas
  (ver Seção 4);
- O **novo modelo de coleta de informações acadêmicas da CAPES**, que dá
  origem à folha adicional descrita na Seção 2.3.

A presente Norma estabelece **apenas os elementos próprios da COPPE/UFRJ**.
Todos os aspectos não tratados explicitamente aqui — formato do papel,
margens, espaçamento, fonte, paginação geral, equações, tabelas,
indicativos de seção, ortografia, siglas, ilustrações no caso geral,
estrutura textual no caso geral, etc. — devem seguir o *Manual UFRJ 2026*.

### 1.2 Implementação de referência

A **implementação de referência** desta Norma é a classe LaTeX `coppe`,
versão 4.0 e posteriores (**CoppeTeX 4.x**), distribuída em
<https://github.com/COPPE-UFRJ/CoppeTeX>. A classe produz, sem
configuração adicional por parte do autor, um documento aderente
simultaneamente ao *Manual UFRJ 2026* e à presente Norma. Seu uso é o
caminho recomendado pela COPPE/UFRJ para a confecção do documento final.

---

## 2. Identificação institucional

### 2.1 Capa

A capa exibe, na ordem:

- **Universidade Federal do Rio de Janeiro**;
- **Instituto Alberto Luiz Coimbra de Pós-Graduação e Pesquisa de
  Engenharia (COPPE)**;
- O nome do **Programa de Pós-graduação** em que o trabalho foi defendido;
- O nome completo do autor;
- O título do trabalho, no idioma principal (ver Seção 4), seguido do
  subtítulo, se houver, precedido de dois pontos;
- O **número de volumes**, se houver mais de um, com a especificação do
  respectivo volume em cada capa;
- A cidade (Rio de Janeiro) e o **ano de depósito** — o da entrega da
  versão final revista ao Programa, que não coincide necessariamente com
  o ano da defesa.

Os logotipos da UFRJ e da COPPE são opcionais, conforme o Anexo A do
*Manual UFRJ 2026*. A COPPE adota o seu uso.

### 2.2 Folha de rosto

A folha de rosto exibe, na ordem:

- O nome completo do autor;
- O título do trabalho, no idioma principal, seguido do subtítulo, se
  houver, precedido de dois pontos;
- O **número de volumes**, se houver mais de um;
- A **natureza do trabalho** (tese ou dissertação), o **objetivo** (grau
  pretendido), o nome da instituição a que é submetido e a **área de
  concentração** — em espaço simples, alinhados do meio da mancha
  gráfica até a margem direita;
- A **linha de pesquisa**, conforme o modelo de coleta CAPES;
- O nome do **orientador** e, se houver, do **coorientador**, alinhados a
  partir da margem esquerda;
- A cidade (Rio de Janeiro) e o **ano de depósito**.

O nome do autor precede o título, e a data indica apenas o ano.

### 2.3 Caráter da identidade institucional

Os elementos de identidade institucional — o nome da Universidade, o
nome do Instituto (COPPE), o nome do Programa de Pós-graduação, a cidade
sede (Rio de Janeiro), o estado (RJ) e o país (Brasil) — **são sempre
exibidos em português**, independentemente do idioma principal do
trabalho. Somente o título do trabalho, na capa e na folha de rosto,
acompanha o idioma principal.

### 2.4 Folha adicional com ficha catalográfica

A partir de agosto de 2026, conforme o §3.1.2.1.2 do *Manual UFRJ 2026*,
o trabalho apresenta uma **folha adicional imediatamente após a folha de
rosto**, preenchida pelo Programa de Pós-graduação, contendo os campos da
Coleta CAPES e a ficha catalográfica.

A ficha é obtida no **Gerador de Fichas Catalográficas** do SiBI
(<http://fichacatalografica.sibi.ufrj.br/>) ou solicitada à biblioteca do
Programa. **A ficha não é composta pelo autor nem pela classe LaTeX.**

A folha adicional **não é contada nem numerada** (ver Seção 7).

### 2.5 Folha de aprovação

A folha de aprovação apresenta, na ordem do §3.1.2.1.3 do *Manual UFRJ
2026*: o nome do autor; o título por extenso e o subtítulo, se houver; a
natureza, o objetivo, o nome da instituição e a área de concentração; a
**data de aprovação**; e o nome, a **titulação** e a **instituição** de
cada membro da Banca Examinadora.

O **orientador figura em primeiro lugar**, por presidir a banca, seguido
do coorientador, se houver, e dos demais examinadores. Não há bloco
separado de orientadores, nem local e data ao pé da página.

A folha de aprovação **não é numerada**.

---

## 3. Resumos: estrutura de três idiomas

Em complemento ao previsto no *Manual UFRJ 2026*, a presente Norma
reconhece três posições distintas para o resumo:

1. **Resumo em idioma principal**, obrigatório, no idioma em que o
   trabalho foi redigido (ver Seção 4);
2. **Resumo em idioma estrangeiro** (*foreign abstract*), obrigatório,
   por convenção em inglês; quando o idioma principal é o inglês, este
   resumo é redigido em português;
3. **Resumo em português**, opcional e adicional, requerido apenas
   quando nenhum dos dois resumos anteriores seja em português — caso
   típico de trabalhos com idioma principal espanhol. Destina-se à
   leitura pela banca e pelos examinadores brasileiros.

O §3.1.2.1.5 do *Manual UFRJ 2026* prevê dois resumos: o da língua
vernácula e o da língua de divulgação internacional. Num trabalho
redigido em espanhol — idioma admitido pelo art. 57 da Resolução CEPG n.
302/2024 — esse par é espanhol e inglês, e o português, língua da
Universidade e da banca, ficaria de fora. A terceira posição existe para
cobrir exatamente esse caso, e é acréscimo da COPPE, não exigência do
manual.

Cada resumo encerra com as palavras-chave no seu próprio idioma,
precedidas do termo correspondente e separadas por ponto e vírgula, como
determina o §3.1.2.1.4.

Cada resumo ocupa uma página própria, na ordem acima, dentro da seção
pré-textual.

---

## 4. Idioma principal do trabalho

O trabalho pode ser redigido em qualquer um dos seguintes idiomas
principais:

- **Português**;
- **Inglês**;
- **Espanhol**.

Esses são os idiomas admitidos pelo **art. 57 da Resolução CEPG n.
302/2024**, e não há na UFRJ respaldo normativo para outros. A
implementação de referência distribui ainda pacotes de francês e
italiano, que servem de demonstração do mecanismo de extensão a novos
idiomas e **não** habilitam esses idiomas para a redação de teses e
dissertações.

A escolha do idioma principal afeta:

- A língua do corpo textual;
- A língua das legendas de figuras, tabelas, quadros, programas e
  algoritmos;
- A língua dos títulos das seções pré-textuais (Sumário, Lista de
  Figuras, Lista de Tabelas, Lista de Quadros, Lista de Programas,
  Lista de Algoritmos, Lista de Abreviaturas e Siglas, Lista de
  Símbolos, Glossário, Referências, etc.);
- A língua do título do trabalho exibido na capa e na folha de rosto;
- A língua do título e do texto de abertura do resumo em idioma
  principal (ver Seção 3).

A identidade institucional permanece em português em qualquer idioma
principal (ver Seção 2.3).

---

## 5. Ilustrações próprias da COPPE/UFRJ

Em complemento às listas previstas no *Manual UFRJ 2026* (Lista de
Figuras, Lista de Tabelas, Lista de Abreviaturas e Siglas, Lista de
Símbolos), a presente Norma reconhece:

- **Lista de Quadros** — para o tipo de ilustração "quadro", bordado em
  todos os lados, distinto de tabela (a qual é delimitada apenas no topo
  e na base);
- **Lista de Programas** — para listagens de código-fonte;
- **Lista de Algoritmos** — para a apresentação de pseudo-código.

Cada uma destas listas figura entre a Lista de Tabelas e a Lista de
Abreviaturas, na seção pré-textual, sempre que houver ao menos uma
ocorrência no corpo do trabalho.

Para todas as ilustrações (figuras, tabelas, quadros, programas,
algoritmos) a legenda figura **acima** da ilustração, e a fonte é
obrigatória e figura **abaixo**, em corpo menor, espaçamento simples,
centralizada, antecedida da palavra "Fonte:" (ou seu equivalente no
idioma principal).

---

## 6. Apêndices e Anexos

Os capítulos de Apêndice e de Anexo são apresentados, tanto no início do
capítulo quanto no Sumário, no formato:

> **APÊNDICE A — *Título do apêndice***
>
> **ANEXO A — *Título do anexo***

A palavra "APÊNDICE" ou "ANEXO" figura em caixa alta, seguida da letra
identificadora (A, B, C, …), de travessão e do título do capítulo,
respeitando o idioma principal do trabalho.

---

## 7. Numeração das páginas pré-textuais

Esta Seção apenas reafirma o §2.7 do *Manual UFRJ 2026*, por ser o ponto
em que se observaram mais divergências de implementação.

A capa não é contada nem numerada. **A contagem começa na folha de
rosto** e prossegue sequencialmente por todas as folhas, que **não são
numeradas** enquanto pré-textuais. A **folha adicional** que contém a
ficha catalográfica **não é contada nem numerada**.

A numeração em algarismos arábicos é impressa **a partir da primeira
folha da parte textual, dando sequência à contagem já iniciada** — e
portanto a Introdução **não** é a folha 1. Figura no canto superior
direito, a 2 cm da borda superior, com o último algarismo a 2 cm da
borda direita.

Não se empregam algarismos romanos nas folhas pré-textuais.

---

## 8. Citações e Referências Bibliográficas

A presente Norma adota integralmente as edições mais recentes das
normas ABNT pertinentes:

- **NBR 6023** (Referências) em sua revisão a partir de 2018;
- **NBR 10520** (Citações) em sua revisão de 2023.

Os elementos da referência, os formatos das citações e as regras gerais
de apresentação são os definidos pela ABNT vigente.

A implementação de referência (CoppeTeX 4.x) fornece automaticamente a
formatação correta para todos os tipos de documento previstos na NBR
6023 vigente, em qualquer dos sistemas de chamada (autor-data ou
numérico) à escolha do autor.

---

## 9. Implementação de referência

A classe LaTeX `coppe` em suas versões 4.0 e posteriores
(**CoppeTeX 4.x**), distribuída em
<https://github.com/COPPE-UFRJ/CoppeTeX>, é a implementação de
referência desta Norma. Sua adoção é o caminho recomendado pela
COPPE/UFRJ para garantir aderência automática a todos os requisitos
acima e ao *Manual UFRJ 2026*.

Em caso de divergência entre a presente Norma escrita e a saída gerada
pela versão estável corrente do CoppeTeX 4.x, prevalece a presente Norma
e o *Manual UFRJ 2026*, e a divergência deve ser comunicada à equipe
mantenedora do CoppeTeX para correção na próxima revisão da
implementação.

---

*Versão da proposta: setembro de 2026, revista para a 9.ª edição revista
(2026) do Manual UFRJ/SiBI. Branch `nlinguas` em
<https://github.com/COPPE-UFRJ/CoppeTeX>.*
