# Normas

As normas de elaboração gráfica de cada unidade, na versão mais recente
disponível. **A fonte de cada uma é o `.docx`**: edite o Word e regere.

| Pasta | Norma | Situação |
|---|---|---|
| `norma-coppe/` | Norma para a Elaboração Gráfica de Teses e Dissertações da COPPE/UFRJ — Edição 2026 | Aprovada pela CPGP. Substitui a norma de 2008, revista em 2019. |
| `norma-poli/` | Norma para a Elaboração Gráfica do Projeto de Graduação da Escola Politécnica/UFRJ — Edição 2026 | Proposta à Congregação. Em vigor: Anexo da Resolução n.º 05/2012 (em `specs/`). |

As duas especializam o *Manual para Elaboração e Normalização de Trabalhos
Acadêmicos* da UFRJ/SiBI (9.ª ed. rev., 2026), que está em `specs/`.

Em `src/normas/norma-coppe/cpgp/` estão os documentos do processo de aprovação
na CPGP (minuta de resolução, explicação das escolhas, ofício); eles não vão
para `normas/`.

A pasta `normas/` da raiz é gerada por `python tools/distribuicoes.py --normas`
(ou `coppetex.bat --distribuir`), que copia o `.docx` e o converte em PDF pelo
LibreOffice ou pelo Word.
