# tools/ — o harness, e como escrever para ele

## Por que esta pasta existe

Compilar sem erro não prova nada. **Uma tese compila perfeitamente com a margem
errada.** As ferramentas daqui existem para medir o que a compilação não mede:
se a página tem as margens da norma, se as referências saem na forma que o
Manual imprime, se o PDF/A é mesmo PDF/A, e se alguém editou à mão um arquivo
que deveria ter sido gerado.

Nada aqui é distribuído. Nada aqui sai do `coppe.dtx`.

## Antes de tudo: a fonte é o `.dtx`

**`src/coppe.dtx` é a fonte única.** Toda a distribuição sai dele por
`pdflatex coppe.ins`, e editar um arquivo gerado é perder a edição na próxima
geração. O guia de programação está em [`../src/README.md`](../src/README.md);
leia-o antes de mexer na classe.

O `build-check.ps1` regenera a distribuição no começo de **todo** escopo,
inclusive o mais rápido. Isso é de propósito: garante que o que você acabou de
compilar veio do `.dtx`, e não de um arquivo que ficou para trás.

## O que cada ferramenta faz

| Arquivo | O que faz |
|---|---|
| `build-check.ps1` | O motor. Regenera a distribuição e compila o que o escopo pedir, deixando os logs em `_scratch/build-logs/` e um resumo legível em `_scratch/RESULTADO.txt`. |
| `prova.ps1` | Atalho para `build-check.ps1 -Scope prova`. É o que tem de sair limpo antes de marcar uma versão. |
| `watch-build.ps1` | Fica observando `_scratch/BUILD_REQUEST` e roda o `build-check` quando o arquivo aparece. Deixe rodando numa janela enquanto trabalha. |
| `mk-adversativa.py` | Gera os doze documentos de `adversativa/`. Eles não são escritos à mão: para mudar o que provam, mude o gerador. |
| `conferir-norma.py` | Lê um PDF pronto e mede, em centímetros, o que a norma fixa: margens, corpo, recuos, ordem das páginas pré-textuais. |
| `conferir-referencias.py` | Compõe as referências e as compara, uma a uma, com o texto que o Manual imprime. O gabarito está nos comentários `%%` de `adversativa/referencias-manual.bib`. |

## Os escopos do `build-check.ps1`

Do mais rápido ao mais completo. Todos começam regenerando a distribuição.

| Escopo | O que compila |
|---|---|
| `class` | Nada. Só regenera a partir do `.dtx`. Segundos. |
| `example` | O exemplo completo em português. |
| `langs` | Os cinco exemplos de idioma. |
| `tests` | A suíte de regressão de `tests/`. |
| `docs` | O manual de uso, a norma da COPPE, o manual futuro e a montagem de capas. |
| `pdfa` | O que tem de ser PDF/A, passado pelo veraPDF. |
| `adversativa` | Os doze documentos de prova, nos dois motores, com ciclo completo. É o escopo demorado. |
| `all` | Tudo acima. |
| `prova` | `all`, mais a verificação de fonte única antes e um veredito depois. |

```powershell
.\tools\build-check.ps1 -Scope example
.\tools\prova.ps1
```

## O que a prova verifica, e por que essas três coisas

1. **Fonte única.** Regenera tudo e pergunta ao git se algum arquivo que estava
   limpo mudou. Se mudou, alguém editou um derivado à mão e a edição acabou de
   ser perdida — que é o que se quer descobrir antes de publicar, não depois.
2. **O que é distribuído compila.** A classe, os exemplos, os manuais.
3. **O que prova que funciona.** A suíte de regressão e os doze documentos
   adversativos, nos dois motores, com todos os PDF/A pelo veraPDF.

Um escopo **pulado conta como reprovação**. Se o veraPDF não estiver instalado,
a prova não passa — e está certa: sem ele ninguém sabe se os PDF/A estão
conformes, e a 2.2(d) do Manual os exige no depósito.

## O laço de trabalho com o observador

O ambiente onde a classe é editada nem sempre tem um TeX completo. O observador
resolve isso: deixe-o rodando numa janela do PowerShell,

```powershell
.\tools\watch-build.ps1
```

e peça uma compilação escrevendo o escopo em `_scratch/BUILD_REQUEST`. Quando
terminar, ele escreve `_scratch/BUILD_DONE` e o resultado legível em
`_scratch/RESULTADO.txt`.

Tudo isso vive em `_scratch/`, que o git ignora. **Nenhuma ferramenta daqui
escreve em arquivo versionado**, com uma exceção declarada: `mk-adversativa.py`
reescreve os doze `.tex` de `adversativa/`, porque é para isso que ele existe.

## Se você for escrever uma ferramenta nova

**Ela mede, não conserta.** O harness diz o que está errado; corrigir é trabalho
de quem edita o `.dtx`. Uma ferramenta que conserta sozinha esconde o problema.

**Ela lê o PDF, não o `.tex`.** É o PDF que vai para o depósito. Medir a fonte é
medir a intenção; medir o PDF é medir o resultado. `conferir-norma.py` é o
modelo: abre o PDF pronto e mede centímetros.

**O gabarito é citável.** Quando a ferramenta compara com a norma, o valor
esperado tem de vir com a referência de onde saiu — o item do Manual, ou o texto
que ele imprime. `conferir-referencias.py` guarda o gabarito em comentários ao
lado de cada entrada, e registra as divergências **aceitas** com o motivo
escrito, em vez de escondê-las no número final. O Manual tem erratas, e há
lugares em que o certo é divergir dele; isso precisa estar escrito.

**Ela não escreve em arquivo versionado.** Saída vai para `_scratch/`.

**Ela roda sem instalação.** PowerShell e Python 3 estão pressupostos; o resto —
poppler, `pypdf`, veraPDF — é procurado, e a ausência vira um passo **pulado com
aviso**, não um erro obscuro. Só a prova é que trata pulado como reprovação.

**Ela explica no cabeçalho para que existe.** Todo arquivo desta pasta abre com
um bloco dizendo o que faz, por que existe e como se roda. Não é ornamento: é o
que permite alguém entender o harness sem ter estado aqui.

## Onde fica o resto

- [`../src/README.md`](../src/README.md) — o guia de programação da classe.
- [`../tests/README.md`](../tests/README.md) — o que cada teste guarda.
- [`../adversativa/README.md`](../adversativa/README.md) — o que cada documento
  de prova está provando.
- [`../CONTRIBUTING.md`](../CONTRIBUTING.md) — como contribuir vindo de fora.
