# Painel do desenvolvedor

Manual do `coppetex.bat` — o ponto de entrada único para gerar, compilar,
testar, conferir, distribuir e versionar a CoppeTeX.

> Este documento é para quem **mexe na classe**. Quem só quer escrever uma tese
> não precisa de nada disto: leia o [`README.md`](./README.md) e o manual da
> classe, `src/coppe.pdf`.

---

## O caminho mais curto

Abra um terminal na raiz do repositório e rode:

```bat
coppetex.bat
```

Abre uma janela, pergunta o que você quer fazer, faz, e mostra a saída enquanto
acontece. Não precisa decorar nada.

Se preferir a linha de comando, **tudo o que a janela faz tem uma opção
equivalente** — e não por educação: a janela não tem nenhum caminho próprio.
Cada botão chama a mesma função que a opção de linha de comando chama, de modo
que não existam duas implementações da mesma coisa, uma delas sempre um pouco
atrasada em relação à outra.

```bat
coppetex.bat --regerar
coppetex.bat --tudo --dist
coppetex.bat --ajuda
```

---

## As ações

| Opção | O que faz |
|---|---|
| `--regerar` | Roda o `coppe.ins`: a classe, os estilos BibLaTeX, os pacotes de idioma, as bases `.bib`, os cinco exemplos por idioma, o `example_pdfa`, a montagem das capas e o `latexmkrc` saem todos do `src/coppe.dtx`. É rápido, e é o primeiro passo de qualquer coisa. |
| `--docs` | Compila os PDFs da entrega: o manual da classe (`coppe.pdf`), o guia rápido em inglês, o exemplo completo, os cinco exemplos por idioma, o manual da norma (`manual.pdf`), a Norma COPPE e a folha de capas. |
| `--testes` | A **primeira camada**: a suíte de `tests/`. Pergunta *a classe compila?* |
| `--adversativo` | A **segunda camada**: os seis documentos de `tests/adversativa/`, que acionam tudo ao mesmo tempo, nos dois motores, validados pelo veraPDF. |
| `--regressivo` | A **terceira camada**: `tests/regressivo/`, um teste mínimo para cada defeito já corrigido. Não roda junto com as outras, de propósito. |
| `--pdfa` | Passa os PDF/A pelo veraPDF no perfil 2b. Sem o veraPDF instalado o passo é **pulado**, não falha. |
| `--conferir` | Os verificadores que não compilam nada: referências cruzadas em todos os `.log`, cobertura do manual (todo comando, ambiente e opção documentado) e versão sincronizada. |
| `--tudo` | A prova completa, com veredito no fim. É o que tem de sair limpo antes de marcar uma versão. |
| `--dist` | Copia para `dist/` os 31 arquivos que o aluno precisa: a classe, os estilos, os logotipos, os dois manuais, o guia rápido, um exemplo por idioma admitido e a licença. **Só copia; nunca compila.** A lista está em `PARA_DIST`, em `tools/painel.py`, e existe só lá. |
| `--pacote` | Fecha `dist/` num `.zip` com o número da versão, em `_scratch/`, pronto para anexar ao *release*. O zip leva uma pasta dentro, `CoppeTeX-<versão>/`, e não os arquivos soltos. |
| `--gerador` | Abre o **gerador de documento vazio**, que escreve o `.tex` e o `.bib` de um trabalho novo. Tem porta própria, o `coppetex-novo.bat`, porque o público é outro: esta ação existe para quem já está com o painel aberto. |
| `--limpar` | Tira `.aux`, `.log` e companhia de `src/` e de `tests/`. Não toca em nenhum PDF. |

Pode combinar quantas quiser. **A ordem em que você escreve não importa**: o
painel roda na ordem que faz sentido — regerar antes de compilar, compilar antes
de copiar, e conferir por último. A cópia para `dist/` vem depois de tudo o que
compila, porque `dist/` não pode receber o que ainda não foi provado, e **antes**
de `--conferir`, porque um dos verificadores compara `dist/` com `src/` byte a
byte — na ordem contrária ele reprovava uma cópia que o passo seguinte ia
fazer.

---

## Versão

```bat
coppetex.bat --versao 2      REM  4.1  ->  4.2
coppetex.bat --versao 3      REM  4.1  ->  4.1.1
```

A versão canônica é a do `\def\fileversion` em `src/coppe.dtx`. Subir a versão
reescreve esse número, a data, e **todo** `\ProvidesFile` e `\ProvidesClass` do
`.dtx` — e em seguida o painel acrescenta `--regerar` por conta própria, porque
o número novo precisa entrar nos arquivos gerados na mesma rodada. Uma
distribuição com metade de cada versão é pior que uma versão velha.

**O primeiro nível não é oferecido, nem na janela nem na linha de comando.** Na
CoppeTeX a troca de *major* sempre significou mudança de modelo — a 4.0 trouxe o
modelo multilíngue, a 3.0 foi a reescrita da classe. Isso é decisão de quem
mantém o projeto e da CPGP, e um clique errado num painel não pode anunciar uma
versão que não existe.

**A prosa não é reescrita sozinha**, também de propósito. O aviso do
`README.md` e o título do `CHANGELOG.md` não são só um número: são uma frase
sobre o que aquela versão é. Trocar o número deixando a frase velha é pior do
que não trocar nada. O comando diz quais arquivos ficaram faltando; o resto é
com você.

Para só conferir, sem mexer em nada:

```bash
python tools/versao.py
python tools/versao.py --detalhe
```

Ele confere a versão em 28 arquivos gerados e em 6 lugares em prosa, e ainda
compara `dist/` com `src/` byte a byte — porque o número de versão é o mesmo nos
dois mesmo quando a cópia ficou para trás, e é exatamente esse o caso que
ninguém percebe.

---

## O que rodar, e quando

**Mexi na classe e quero ver se não quebrei nada:**

```bat
coppetex.bat --regerar --testes
```

**Vou marcar uma versão:**

```bat
coppetex.bat --tudo --regressivo --conferir --dist
```

Na janela, esse conjunto está no botão **"Antes de marcar uma versão"**. Tem de
sair com `RESULTADO: tudo passou` e com zero divergências.

**Só quero atualizar `dist/` depois de compilar:**

```bat
coppetex.bat --dist
```

**Vou publicar um *release*:**

```bat
coppetex.bat --dist --pacote
```

Sai `_scratch/CoppeTeX-<versão>.zip` com a entrega inteira, que é o único anexo
que o *release* precisa ter. O resto do repositório o GitHub já publica sozinho,
como o código-fonte da tag.

---

## O outro bat: `coppetex-novo.bat`

Este manual é do `coppetex.bat`, que é o painel de quem **mexe na classe**. Há
um segundo bat na raiz, o `coppetex-novo.bat`, que é para quem vai **escrever
uma tese** — público diferente, por isso porta diferente.

```bat
coppetex-novo.bat                       abre a janela
coppetex-novo.bat --gerar               gera com os padrões da COPPE
coppetex-novo.bat --gerar --tipo=msc --programa=PEM
coppetex-novo.bat --ajuda               a lista de todos os campos
```

Ele escreve o `.tex` e o `.bib` com que um trabalho começa, já com a estrutura
que a norma pede e os cinco capítulos de sempre — Introdução, Fundamentação
Teórica, Materiais e Métodos, Resultados e Conclusões —, com texto de
preenchimento para que o documento compile e mostre cada folha.

Existe porque começar do `example.tex` significa **apagar**: aquele é um
documento de demonstração, cheio de figuras, tabelas e comentários que ensinam,
e quem vai escrever passa a primeira hora limpando o que não vai usar. Aqui é o
contrário: sai o esqueleto, e você escreve por cima.

Tudo o que é opcional tem um sim/não, e o padrão de tudo é o **padrão completo
da COPPE**, como no exemplo: quem aperta Gerar sem mexer em nada recebe um
trabalho com todas as folhas que a norma prevê. Tirar é escolha de quem gera.

Há uma exceção a esse padrão, e é deliberada: o campo **Pasta das referências**
vem preenchido com `referencias`, e o `.bib` gerado vai para lá em vez da raiz.
O exemplo tem os `.bib` na raiz por história, não por norma, e a subpasta é a
recomendação desde a 4.1 — ela tira arquivo da raiz do trabalho e, de quebra,
impede que um `.bib` da distribuição do TeX se passe pelo seu. Apague o campo
para voltar à raiz. A justificativa está no `src/coppe.pdf`, na seção *Onde por
os `.bib`*, e o teste é o `tests/regressivo/r31`.

### Ele também busca a classe

A opção **Baixar a classe do GitHub** (`--baixar=sim`) traz, para a mesma pasta,
a classe, os estilos, os pacotes de idioma e os logotipos — do *release* mais
recente, ou do ramo `master` se não houver *release*. A pasta fica compilável na
hora, sem nenhuma cópia manual.

E faz de uma vez o passo que todo mundo esquece: se o trabalho não for em
português, ela **traz para a raiz** o conteúdo da pasta daquele idioma, que é
onde o LaTeX procura. Sem isso, o erro seria um arquivo que está ali do lado e
que o LaTeX diz não achar.

Não traz os exemplos nem as fontes dos manuais: você pediu um documento em
branco, e um exemplo ao lado é justamente o que se queria evitar.

Guardado por `tests/regressivo/r26`, que gera dois documentos — o padrão e um
com tudo ligado ao mesmo tempo — e **compila os dois**, só com o que há na
entrega. Um gerador erra de um jeito particular: produz um arquivo que parece
certo e só quebra quando alguém compila, e quem compila é o aluno, na véspera.
O download em si não é exercitado no teste — teste que depende da rede falha no
avião e no proxy da universidade, e teste que falha por motivo alheio deixa de
ser lido —, mas a regra do que vem e do que não vem é cobrada.

## Como as peças se encaixam

```
coppetex.bat            o lançador; só chama o painel
  └── tools/painel.py   decide o que roda, em que ordem, e mostra a saída
        ├── tools/build-check.ps1        compila tudo (é quem sabe o ciclo)
        ├── tests/regressivo/run-regressivo.py
        ├── tools/conferir-*.py          os verificadores
        └── tools/versao.py              confere e sobe a versão
```

O painel **não compila nada por conta própria**. Quem compila é o
`tools/build-check.ps1`, que já existia antes do painel, já é usado por quem
roda a prova e já sabe o ciclo completo de cada documento — quantas passadas,
quando chamar o `biber`, quando chamar o `makeindex` das listas, quando parar.
Duplicar isso no painel seria criar uma segunda verdade sobre como se compila
uma tese.

`src/doall.bat` continua funcionando: virou um atalho para
`coppetex.bat --regerar --docs --dist`. Ele tinha uma lista de cópias própria, e
essa lista divergiu da do `Makefile` — uma das duas copiava o `README.md` da raiz
por cima do guia de instalação de `dist/` a cada execução. Agora a lista existe
em um lugar só.

---

## Requisitos

| Ferramenta | Para quê | Sem ela |
|---|---|---|
| `pdflatex`, `biber`, `makeindex` | tudo | nada funciona |
| `lualatex` | um teste de regressão e metade da suíte adversativa | esses passos são pulados, com aviso |
| Python 3 | o painel, a suíte de regressão e os verificadores | o `coppetex.bat` avisa e indica o caminho do PowerShell direto |
| Tkinter (vem com o Python) | a janela | o painel cai num menu de texto no terminal |
| `pdftotext` | as cobranças de texto da suíte de regressão | as cobranças são **puladas com aviso**, nunca aprovadas em silêncio |
| veraPDF | validar PDF/A-2b | o passo é pulado, não falha |

Sobre o `pdftotext`, uma armadilha que já custou tempo: existem **dois**
programas com esse nome. O do poppler aceita `-bbox` e o do Xpdf não, e o
`tools/conferir-norma.py`, que mede margens em centímetros no PDF pronto,
precisa do primeiro. No Windows, o que vem com o MiKTeX serve; o que vem com o
Git Bash não. Se o Git Bash estiver antes no `PATH`, o verificador avisa que a
**ferramenta** é insuficiente — e não reprova o documento, que é o que ele fazia
antes.

---

## Sem Python

O harness é PowerShell puro e não depende do painel:

```powershell
powershell -File tools\build-check.ps1 -Scope prova
powershell -File tools\build-check.ps1 -Scope class
powershell -File tools\build-check.ps1 -Scope example
```

Os escopos são `class`, `example`, `langs`, `tests`, `docs`, `pdfa`,
`adversativa`, `all` e `prova`. A suíte de regressão, essa sim, precisa do
Python.
