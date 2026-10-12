# CoppeTeX biblatex — referências e citações ABNT conforme o Manual da UFRJ

Estilos **biblatex/biber** que compõem referências e citações como o *Manual
para Elaboração e Normalização de Trabalhos Acadêmicos* da UFRJ/SiBI (9.ª ed.
rev., 2026) as imprime, seguindo a NBR 6023:2025 e a NBR 10520:2023. São os
mesmos estilos que a classe `ufrj` usa, empacotados para **qualquer outro
documento LaTeX**: artigo, relatório, livro, apresentação.

> Quem escreve tese, dissertação ou Projeto de Graduação na UFRJ não precisa
> desta pasta: a classe `ufrj` já carrega estes estilos (veja `dist-coppe` ou
> `dist-poli`).
>
> Esta pasta é gerada. A fonte é o `src/ufrj.dtx` do repositorio
> <https://github.com/COPPE-UFRJ/CoppeTeX>.

## O que tem aqui

| Arquivo | O que é |
|---|---|
| `ufrj.dbx` | Modelo de dados: os tipos e campos do Manual (`@dscthesis`, `@mscthesis`, `@tcc`, patentes, documentos jurídicos, audiovisuais…) e os nomes em português (`@livro`, `autor`, `titulo`, `edicao`). |
| `ufrj.bbx` | Estilo da lista de referências, autor-data. |
| `ufrj.cbx` | Estilo de citação autor-data: Silva (2020), (SILVA, 2020), *apud*. |
| `ufrj-numeric.bbx`, `ufrj-numeric.cbx` | Sistema numérico, na ordem de citação. |
| `brazilian-ufrj.lbx`, `english-ufrj.lbx`, `spanish-ufrj.lbx`, `french-ufrj.lbx`, `italian-ufrj.lbx` | Termos de bibliografia de cada idioma ("Disponível em", "Acesso em", "et al."…). |
| `exemplo.bib` | Uma entrada de cada tipo do Manual, cada uma precedida da forma exata que o Manual imprime. |
| `exemplo-biblatex.tex` | Documento mínimo que usa os estilos com a classe `article`. |
| `COPYING.txt` | Licença GNU GPL v3. |

## Como usar

Copie os `.dbx`, `.bbx`, `.cbx` e os `.lbx` dos idiomas do seu documento para a
pasta dele (ou para `tex/latex/ufrj-biblatex` na sua árvore do TeX, seguido de
`texhash`). No preâmbulo:

```latex
\usepackage[english,brazilian]{babel}
\usepackage{csquotes}
\usepackage[backend=biber,datamodel=ufrj,
            bibstyle=ufrj,citestyle=ufrj,natbib=true]{biblatex}
\addbibresource{minhas-referencias.bib}
```

e, no fim do texto, `\printbibliography`.

Dois detalhes que não são opcionais:

1. **`datamodel=ufrj`** — sem ele o biber não conhece os tipos e campos do
   Manual, e as entradas em português somem com aviso.
2. **`backend=biber`** — os estilos não funcionam com o BibTeX.

O idioma das referências segue o do `babel`: o "em" de "Tese (Doutorado em
Engenharia)" sai "in" em inglês e "en" em espanhol.

Para o **sistema numérico**, use `bibstyle=ufrj-numeric,citestyle=ufrj-numeric`.
O Manual não admite o numérico em trabalho com notas de rodapé.

## Citações

| Comando | Resultado |
|---|---|
| `\citet{chave}` | Silva (2020) |
| `\citep{chave}` | (SILVA, 2020) |
| `\citep[p.~45]{chave}` | (SILVA, 2020, p. 45) |
| `\citetapud{Autor}{ano}{chave}` | citação de citação, no texto |
| `\citepapud{Autor}{ano}{chave}` | citação de citação, entre parênteses |

## Compilar

```
pdflatex exemplo-biblatex
biber exemplo-biblatex
pdflatex exemplo-biblatex
pdflatex exemplo-biblatex
```

ou `latexmk -pdf exemplo-biblatex`.

## Licença

GNU General Public License, versão 3 (`COPYING.txt`).
