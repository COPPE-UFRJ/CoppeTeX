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
implementadas em `ufrj.bbx`.

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

## `specs/ABNT/` — as normas da ABNT, fora do git

As normas da ABNT que o Manual cita, **nas edições que ele cita** na sua lista
de referências. Ficam nesta pasta para consulta e **não são versionadas**: são
publicações da ABNT, com todos os direitos reservados, e o repositório é
público. O `.gitignore` ignora tudo em `specs/` que não seja `.md` ou `.pdf` da
raiz, e por isso a subpasta fica de fora. Quem precisar delas pede ao
mantenedor, ou consulta pela biblioteca (a UFRJ assina o acesso às normas).

| Norma | Arquivo | Uso |
|---|---|---|
| NBR 6023:2025 (3.ª ed., 21/05/2025) | `Referencias-NBR-6023-2025.pdf` | Referências. O Anexo A (meses) conferido contra a classe (#146). O texto extraído perde letras de algumas fontes: leia como imagem. |
| NBR 10520:2023 | `ABNT NBR 10520 2023.pdf` | Citações. Digitalizada, sem camada de texto: leia como imagem. A 6.1.1.4 (chamada pelo título) decidiu a #138; a 6.1.1.2 e a 6.1.1.3 (entidade), a #144. |
| NBR 14724:2024 | `ABNT_NBR_14724_2024-1.pdf` | Trabalhos acadêmicos. |
| NBR 10520:2023, resumo | `NBR-10520-de-2023.pptx.pdf` | Apresentação de uma biblioteca (UFMS) sobre a norma; material secundário. |
| NBR 6023:2018 | `2020ABNT60232018VersoCorrigida - Unknown.pdf` | **Superada**: o Manual cita a de 2025. Fica só para comparar. |

**A regra (18/09/2026).** Vale sempre a norma da UFRJ. As normas da ABNT valem
nas edições que o Manual cita e por meio dele; onde uma delas diverge do Manual,
vale o Manual, e a divergência é registrada como aviso — a lista das conhecidas
está no manual da classe, na seção "Quem manda, quando as fontes divergem".

## A norma da Escola Politécnica

`Anexo_Resolucao_n_05_de_2012-Estabelece_Normas_Elaboracao_Grafica_Projeto_de_Graduacao-1.pdf`
— a norma gráfica do Projeto de Graduação da Escola Politécnica, de 2012. É
**anterior ao Manual vigente** e o contraria em treze pontos, entre eles a
numeração das folhas pré-textuais, a ordem dos elementos, a posição da legenda
das figuras e o formato das referências, que ela baseia na NB-66 — norma da
ABNT substituída em 1989. A conferência item a item está no
[`NAO-CONFORMIDADES-POLI.md`](../NAO-CONFORMIDADES-POLI.md), e o que continua
valendo dela está na proposta de norma nova,
[`src/PROPOSTA-DE-RESOLUCAO.tex`](../src/PROPOSTA-DE-RESOLUCAO.tex).

## Também nesta pasta

- `ANOTACOES.md` — anotações de Geraldo Xexéo feitas na 9.ª ed. (2025) do
  manual, transcritas do PDF anterior, com o estado de cada uma frente à edição
  revista de 2026. **A edição de 2025 não está mais nesta pasta**, e é por isso
  que as anotações foram transcritas: elas existiam só como comentários dentro
  daquele PDF e teriam desaparecido com ele.

Não há mais nenhum outro arquivo aqui. As extrações de texto que já ocuparam a
pasta eram material de trabalho, continuam ignoradas pelo `.gitignore` e podem
ser refeitas a qualquer momento com `pdftotext -layout`.

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
