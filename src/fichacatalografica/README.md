# Prova da ficha catalográfica

Esta pasta prova que o comando `\catalogcard{...}` coloca a ficha catalográfica
**no lugar da moldura vazia** ("Espaço reservado à ficha catalográfica"), no
**pé da folha adicional**.

- `ficha-exemplo.tex` — documento mínimo da COPPE que chama
  `\catalogcard{fichacatalografica.pdf}`.
- `fichacatalografica.pdf` — uma página A4 qualquer, que faz as vezes da ficha
  real (a de verdade vem de <http://fichacatalografica.sibi.ufrj.br/>).

## Como provar

Copie os dois arquivos para uma pasta onde a classe esteja ao alcance (por
exemplo `build/`, depois de `coppetex.bat --regerar`) e compile:

```
pdflatex ficha-exemplo
```

Na folha adicional, a `fichacatalografica.pdf` aparece no lugar da moldura.
Comente a linha `\catalogcard{...}` e, no mesmo lugar, volta a moldura vazia —
prova de que o comando é quem troca uma pela outra.

## Por que fica aqui, e não na distribuição

É **prova de funcionamento**, não material do aluno: fica versionada em `src/`
(para não envelhecer em silêncio) e **não entra nas `dist-*`**. O aluno gera a
sua ficha no SiBI e a inclui com `\catalogcard{ficha.pdf}`, como ensina o
*Guia Passo a Passo* e o manual.
