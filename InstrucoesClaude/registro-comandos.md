# Registro de comandos — CoppeTeX 4.0

Log cronológico dos comandos/decisões do usuário para o trabalho do CoppeTeX 4.0
(ramo `futuro2026`). O histórico anterior a este registro está no `git log`.

---

## 2026-05-25 — Pendências: tratamento e ordem de execução

Após o levantamento das pendências (formatação, bibliografia, higiene e
processo), o usuário comandou:

- **Registrar** todos os comandos seguintes neste arquivo `.md`.
- **C2** (`.gitignore` `/LaTeXManuals`, `specs/manual2024.pdf` modificados): **esquecer** — foi o usuário que fez.
- **C3** (`specs/ufrj-logo.pdf` não rastreado): **não se preocupar** — foi o usuário que fez.
- **C1** (referências de caminho desatualizadas em `rules.md`/`formatting-tasks.md`): **fazer a correção trivial**.
- **C4** (`master` / aprovação CPGP): **não pode ser feito agora**.
- Executar, **uma de cada vez, nesta ordem**: **B1, B3, B4, B2, A1, A2**
  - B1 — papel do organizador "(Org.)/(Comp.)/(Coord.)" nas referências.
  - B3 — entrada por título com a 1ª palavra significativa em CAIXA ALTA (ABNT 4.2).
  - B4 — artigo de jornal (caderno/seção, `entrysubtype=newspaper`).
  - B2 — formatação ABNT exata dos tipos exóticos (patente, legislação, jurisprudência, norma, etc.).
  - A1 — entrada de apêndice/anexo no Sumário ("APÊNDICE A – …").
  - A2 — ficha catalográfica no verso da folha de rosto (NBR 14724, R57).
- **Depois** de tudo pronto: **analisar todos os documentos e fazer um plano de correção**.

---

## 2026-05-26 — Nova tarefa: capa (Anexo A)

O usuário comandou **continuar** a execução pendente e **incluir nas tarefas**:

- **Capa** no estilo da **página 115 do manual2024 (Anexo A — Sugestão de capa)**,
  com o **nome completo da COPPE** ("Instituto Alberto Luiz Coimbra de
  Pós-Graduação e Pesquisa de Engenharia") e o **nome do programa**, obtido da
  configuração `\department`.
  - Implementada como `\makecover` em `coppe.dtx`, chamada por `\maketitle`
    antes da folha de rosto. Bloco institucional centralizado em caixa alta
    (universidade / nome completo da COPPE / "Programa de <depto>"), autor em
    negrito, título, cidade e ano; logos UFRJ+COPPE no topo. Capa não contada.
