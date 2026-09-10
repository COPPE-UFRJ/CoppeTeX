# specs/ — documentos normativos de referência

Esta pasta guarda os documentos normativos que a CoppeTeX implementa. Os dois
PDFs abaixo **são versionados** junto com o código: quem clona o repositório já
recebe a norma exatamente na versão contra a qual a classe foi conferida, sem
depender de o SiBI manter os arquivos no ar.

## Os documentos

### `Manual para elaboração e normalização de trabalhos acadêmicos 2024.pdf`

A norma vigente. Universidade Federal do Rio de Janeiro, Sistema de Bibliotecas
e Informação, *Manual para elaboração e normalização de trabalhos acadêmicos*,
9.ª ed. rev., Rio de Janeiro, UFRJ/SiBI, 2026, 121 p. (Série Manuais de
Procedimento, 5).

**O nome do arquivo diz 2024 e está errado.** A folha de rosto e a ficha
catalográfica dizem 9.ª ed. rev., 2026. O nome é o que veio da distribuição do
SiBI e foi mantido para que o arquivo continue localizável por ele; o que vale é
a edição impressa na capa. Nunca existiu um manual de 2024.

É o documento de referência para margens, sumário, destaque gradativo dos
títulos de seção, elementos pré-textuais e as 34 categorias de referência
implementadas em `coppe.bbx`.

### `Folha adicional T&D Coleta+ CAPES.pdf`

Duas páginas, modelo oficial do SiBI: a folha de rosto de tese ou dissertação e
a folha adicional com as informações de Coleta CAPES (tipo de produção
intelectual, projeto de pesquisa vinculado, área de concentração, agências de
fomento) mais a ficha catalográfica. A folha adicional passou a ser obrigatória
em agosto de 2026.

É o documento de referência para a folha de rosto e para a página adicional
geradas pela classe.

## Sobre redistribuição

Os dois PDFs são publicações do SiBI/UFRJ, distribuídas por ele para uso da
comunidade da universidade. Não trazem declaração de licença. O repositório os
inclui como documentação de referência da norma implementada; se o SiBI pedir a
retirada, basta apagar os arquivos e voltar a ignorá-los no `.gitignore`.

## Também nesta pasta

- `ANOTACOES.md` — anotações de Geraldo Xexéo feitas na 9.ª ed. (2025) do
  manual, transcritas do PDF anterior, com o estado de cada uma frente à edição
  revista de 2026.

## Documentos relacionados, fora desta pasta

- `../NORMA_COPPE_2026.md` — a norma própria da COPPE, que complementa o manual
  do SiBI. É o documento que a CoppeTeX implementa em conjunto com ele.
- `../REVISAO_SIBI.md` — verificação item a item da classe contra a edição 2026,
  e o plano de trabalho decorrente.

## Resoluções citadas pelo manual

- **CEPG n. 302/2024**, art. 57 — teses e dissertações podem ser redigidas em
  português, inglês ou espanhol.
- **CEPG n. 246/2023** — entrega apenas em versão digital; fim da via impressa.
- **CEPG n. 128/2022** — defesas de trabalhos de conclusão na pós-graduação.

Os links estão no Anexo G do manual vigente.
