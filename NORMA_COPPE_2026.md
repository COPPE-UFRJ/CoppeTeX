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
UFRJ/SiBI, 9.ª edição (Rio de Janeiro, 2025) — doravante referido como
*Manual UFRJ 2025* — em conjunto com as adaptações estabelecidas pela
presente Norma.

A presente Norma estabelece **apenas os elementos próprios da COPPE/UFRJ**.
Todos os aspectos não tratados explicitamente aqui — formato do papel,
margens, espaçamento, fonte, paginação geral, equações, tabelas,
indicativos de seção, ortografia, siglas, ilustrações no caso geral,
estrutura textual no caso geral, etc. — devem seguir o *Manual UFRJ 2025*.

### 1.2 Implementação de referência

A **implementação de referência** desta Norma é a classe LaTeX `coppe`,
versão 4.0 e posteriores (**CoppeTeX 4.x**), distribuída em
<https://github.com/COPPE-UFRJ/CoppeTeX>. A classe produz, sem
configuração adicional por parte do autor, um documento aderente
simultaneamente ao *Manual UFRJ 2025* e à presente Norma. Seu uso é o
caminho recomendado pela COPPE/UFRJ para a confecção do documento final.

Quando houver dúvida quanto à apresentação correta de algum elemento
gráfico previsto pela presente Norma, a saída gerada pela versão mais
recente do CoppeTeX 4.x prevalece como referência.

---

## 2. Identificação institucional

### 2.1 Capa e folha de rosto

A capa e a folha de rosto do trabalho exibem, na ordem:

- **Universidade Federal do Rio de Janeiro**;
- **Instituto Alberto Luiz Coimbra de Pós-Graduação e Pesquisa de
  Engenharia (COPPE)**;
- O nome do **Programa de Pós-graduação** em que o trabalho foi defendido;
- O nome completo do autor;
- O título do trabalho, no idioma principal (ver Seção 4);
- A cidade (Rio de Janeiro) e o ano da defesa.

### 2.2 Caráter da identidade institucional

Os elementos de identidade institucional — o nome da Universidade, o
nome do Instituto (COPPE), o nome do Programa de Pós-graduação, a cidade
sede (Rio de Janeiro), o estado (RJ) e o país (Brasil) — **são sempre
exibidos em português**, independentemente do idioma principal do
trabalho. Somente o título do trabalho, na capa e na folha de rosto,
acompanha o idioma principal.

### 2.3 Ficha catalográfica

A ficha catalográfica é gerada conforme as regras AACR2 e o *Manual UFRJ
2025*, e figura no **verso da folha de rosto**. Acrescenta-se à ficha:

- A indicação da instituição como **UFRJ/COPPE**;
- O nome do **Programa de Pós-graduação** em que o trabalho foi defendido;
- A indicação das páginas iniciais e finais da lista de Referências.

### 2.4 Folha de aprovação

A folha de aprovação contém o título do trabalho, o nome do candidato,
os nomes do(s) orientador(es) e dos membros da Banca Examinadora — na
ordem em que aprovaram o trabalho —, com espaço para assinatura, e a
data da defesa. A folha de aprovação **não é numerada**.

---

## 3. Resumos: estrutura de três idiomas

Em complemento ao previsto no *Manual UFRJ 2025*, a presente Norma
reconhece três posições distintas para o resumo:

1. **Resumo em idioma principal**, obrigatório, no idioma em que o
   trabalho foi redigido (ver Seção 4);
2. **Resumo em idioma estrangeiro** (*foreign abstract*), obrigatório,
   por convenção em inglês; quando o idioma principal é o inglês, este
   resumo é redigido em português;
3. **Resumo em português**, opcional e adicional, requerido apenas
   quando nenhum dos dois resumos anteriores seja em português — caso
   típico de trabalhos com idioma principal espanhol, francês ou
   italiano. Destina-se à leitura pela banca e pelos examinadores
   brasileiros.

Cada resumo ocupa uma página própria, na ordem acima, dentro da seção
pré-textual.

---

## 4. Idioma principal do trabalho

O trabalho pode ser redigido em qualquer um dos seguintes idiomas
principais:

- **Português**;
- **Inglês**;
- **Espanhol**;
- **Francês**;
- **Italiano**;
- Qualquer outro idioma reconhecido pela implementação de referência
  (CoppeTeX 4.x), mediante o pacote de localização correspondente.

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
principal (ver Seção 2.2).

---

## 5. Ilustrações próprias da COPPE/UFRJ

Em complemento às listas previstas no *Manual UFRJ 2025* (Lista de
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

A capa não é contada nem numerada. A folha de rosto inicia a contagem
das páginas pré-textuais.

Por **regra padrão**, **os números das páginas pré-textuais não são
impressos**, embora sejam contados. À critério do autor, e de forma
opcional, os números das páginas pré-textuais podem ser impressos em
algarismos romanos minúsculos (iii, iv, v, …) a partir da terceira
página contada.

A numeração arábica, no canto superior externo da página, inicia em 1
na primeira página da parte textual.

---

## 8. Citações e Referências Bibliográficas

A presente Norma adota integralmente as edições mais recentes das
normas ABNT pertinentes:

- **NBR 6023** (Referências) em sua revisão a partir de 2018;
- **NBR 10520** (Citações) em sua revisão de 2023.

Os elementos da referência, os formatos das citações e as regras gerais
de apresentação são os definidos pela ABNT vigente.

Esta adoção constitui a única divergência da presente Norma em relação
ao previsto no *Manual UFRJ 2025* — que reflete edições anteriores das
mesmas normas ABNT — e ocorre na medida estrita das atualizações
posteriores a 2020 introduzidas pela própria ABNT.

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
acima e ao *Manual UFRJ 2025*.

Em caso de divergência entre a presente Norma escrita e a saída gerada
pela versão estável corrente do CoppeTeX 4.x, prevalece a presente Norma
e o *Manual UFRJ 2025*, e a divergência deve ser comunicada à equipe
mantenedora do CoppeTeX para correção na próxima revisão da
implementação.

---

*Versão da proposta: maio de 2026. Branch `nlinguas` em
<https://github.com/COPPE-UFRJ/CoppeTeX>.*
