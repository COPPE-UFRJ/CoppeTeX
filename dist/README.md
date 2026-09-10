<!-- AVISO-CPGP:INICIO — apagar deste comentário até AVISO-CPGP:FIM depois da aprovação -->
> ## ⚠️ Versão nova, ainda não aprovada
>
> **Esta é a CoppeTeX 4.1, e ela ainda não foi aprovada.** Vai à próxima reunião
> da Comissão de Programas de Pós-Graduação (CPGP) da COPPE/UFRJ. Use-a para
> escrever e para experimentar, mas confirme com a secretaria do seu Programa
> antes de depositar um trabalho com ela.
<!-- AVISO-CPGP:FIM -->

# CoppeTeX — o que você precisa para escrever

Esta pasta é a **entrega**: o mínimo para instalar a classe e começar a
escrever. Nada aqui é material de desenvolvimento. Quem quiser o código
comentado, os testes, os documentos de prova ou os cinco exemplos de idioma
encontra tudo na raiz do repositório.

## O que tem aqui

| Arquivo | Para que serve |
|---|---|
| `coppe.cls` | A classe. É o arquivo que o seu documento carrega. |
| `coppe.dbx`, `coppe.bbx`, `coppe.cbx` | O estilo de bibliografia e de citação, em autor-data. |
| `coppe-numeric.bbx`, `coppe-numeric.cbx` | O mesmo, no sistema numérico, usado pela opção `numbers`. |
| `brazilian-coppe.lbx`, `english-coppe.lbx`, `spanish-coppe.lbx`, `french-coppe.lbx`, `italian-coppe.lbx` | Os termos de bibliografia em cada idioma. |
| `coppe-lang-spanish.def`, `coppe-lang-french.def`, `coppe-lang-italian.def` | Os textos fixos da classe (rótulos, meses, capa) nesses três idiomas. Português e inglês vêm dentro da classe. |
| `coppe.ist` | O estilo de ordenação do glossário e da lista de símbolos. |
| `coppe-logo.pdf`, `coppe-logo.eps`, `ufrj-logo.pdf` | Os logotipos da capa. |
| `latexmkrc` | A receita de compilação, para quem usa `latexmk`. |
| `coppe.pdf` | **O manual de uso.** Comece por ele. |
| `example.tex`, `example.bib`, `example.pdf` | Um trabalho completo, para copiar e ir trocando. O PDF é o que ele produz. |
| `COPYING` | A licença, GNU GPL versão 3. |

## Instalação

O caminho mais curto é não instalar nada: copie todos estes arquivos para a
pasta do seu trabalho e compile ali. Funciona no Overleaf do mesmo jeito —
suba os arquivos junto com o seu `.tex`.

Para instalar de vez, ponha os arquivos na árvore local do seu TeX, em
`tex/latex/coppe`, e mande o sistema reindexar (`texhash` no TeX Live,
`initexmf --update-fndb` no MiKTeX).

## Como compilar

São três passadas mais o `biber`, porque as referências cruzadas e a
bibliografia só se acomodam na terceira:

```
pdflatex example
biber example
pdflatex example
pdflatex example
```

Com `latexmk` e o `latexmkrc` desta pasta, uma linha basta:

```
latexmk -pdf example
```

Um trabalho que pede todas as listas ao mesmo tempo pode esbarrar no limite de
16 fluxos de escrita do pdfTeX. A classe resolve isso sozinha quando o pacote
`morewrites` está instalado; se não estiver, instale-o ou compile com
`lualatex`, que não tem esse limite.

## O primeiro documento

Abra `example.tex`. Ele traz, comentado linha a linha, tudo o que a classe
oferece: capa, folha de rosto com linha de pesquisa, folha da Coleta CAPES,
ficha catalográfica, folha de aprovação, os três resumos, todas as listas
pré-textuais, os cinco níveis de seção, os flutuantes com legenda acima e fonte
abaixo, as citações, os apêndices e os anexos.

Troque o conteúdo e apague o que não usar. Se algo não estiver claro,
`coppe.pdf` explica.

## Licença

GNU General Public License, versão 3. O texto está em `COPYING`.
