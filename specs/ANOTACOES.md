# Anotações no manual UFRJ/SiBI

Anotações feitas por Geraldo Xexéo sobre a **9.ª ed. (2025)** do *Manual para
elaboração e normalização de trabalhos acadêmicos* — hoje em
`specs/manual-sibi-9ed-2025.pdf`.

Elas existiam apenas como comentários dentro daquele PDF e não estavam
registradas em nenhum outro lugar do repositório. Foram transcritas aqui para
sobreviverem à substituição do manual pela edição revista de 2026.

Cada anotação vem com o estado atual: se a edição 2026 a manteve, superou ou
respondeu.

---

## 1. Margens do verso

> **"Aqui precisa usar um binding offset novo"**

Anotada ao lado da especificação de margens de verso da edição 2025
(direita 3 cm, superior 3 cm, esquerda 2 cm, inferior 2 cm).

**Estado: SUPERADA.** A edição 2026 **eliminou as margens de verso**. Com a
Resolução CEPG n. 246/2023 a entrega passou a ser somente digital, e o manual
trocou "anverso/verso" por "folhas" em todo o texto. Não há mais base normativa
para `bindingoffset`; a classe deve usar `oneside` com margem esquerda de 3 cm.

## 2. Limite de subdivisão

> **"Limite da numeração 1.1.1.1.1"**

Anotada em §2.6, sobre a recomendação de limitar as seções até a quinária.

**Estado: MANTIDA.** A edição 2026 repete a recomendação sem alteração.

## 3. Formatação do sumário

> **"Importante: formatação do sumário deve ser assim! Não tem ponto final!"**

**Estado: MANTIDA.** O §3.1.2.1.6 de 2026 continua mandando grafar as seções no
sumário exatamente como aparecem no corpo do trabalho, e o exemplo do próprio
manual não traz ponto final.

## 4. Esquema tipográfico dos títulos de seção

Anotada sobre o exemplo de destaque gradativo em §2.6:

| Nível | Anotação |
|---|---|
| `chapter` | todas maiúsculas, **bold** |
| `section` | todas maiúsculas, **normal** (sem negrito) |
| `subsection` | as primeiras letras de cada palavra em maiúscula, **bold** |
| `subsubsection` | as primeiras letras de cada palavra em maiúscula, **bold e itálico** |
| `subsubsubsection` | itálico, só a primeira palavra inicia em maiúscula |

**Estado: MANTIDA.** O §2.6 de 2026 repete "destaca-se gradativamente os títulos
das seções, utilizando os recursos de negrito, itálico ou grifo e redondo,
caixa-alta ou versal", com o mesmo exemplo.

Esta é a leitura de referência do projeto para o destaque gradativo, e é o que
`\titleformat` deve implementar em `coppe.cls`.

## 5. Referência cruzada às seções

> **"Como se referir as seções"**

Marcador colocado sobre os exemplos "… na seção 4 / … ver 2.2 / … em 1.1.2.2,
§ 3.º".

**Estado: MANTIDA** na edição 2026, sem alteração.

---

*Transcrito em 2026-09-04, a partir da extração de texto de
`specs/manual-sibi-9ed-2025.pdf`.*
