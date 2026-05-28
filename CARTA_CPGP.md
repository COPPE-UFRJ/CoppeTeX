# Carta de submissão à CPGP/COPPE/UFRJ

*Rascunho — sujeito à revisão pela equipe mantenedora antes do envio.*

---

**Para:** Comissão de Programas de Pós-Graduação (CPGP) da COPPE/UFRJ
**Assunto:** Proposta de atualização da norma para apresentação gráfica de teses e dissertações e da implementação de referência CoppeTeX (v4.0)
**Data:** maio de 2026

---

Prezada Comissão,

Submetemos à apreciação desta CPGP a versão **4.0** do pacote **CoppeTeX**
— a implementação de referência LaTeX para teses e dissertações da
COPPE/UFRJ — acompanhada de uma proposta de **atualização mínima da
norma** atualmente vigente, aprovada por esta CPGP em 15 de julho de 2008
e revisada pela última vez em 26 de novembro de 2019.

A presente proposta é apresentada no *branch* `nlinguas` do repositório
oficial em <https://github.com/COPPE-UFRJ/CoppeTeX>, e contempla duas
contribuições articuladas:

1. **Modelo multilíngue na implementação de referência.** A classe
   `coppe` ganha um modelo de três posições fixas de idioma — *principal*,
   *estrangeiro* e *terceiro opcional* —, com cinco opções de idioma
   principal já embutidas (português, inglês, espanhol, francês e
   italiano) e um mecanismo extensível para qualquer idioma adicional
   suportado pelo Babel.

2. **Norma atualizada e enxuta.** Propomos substituir a norma atual,
   relativamente extensa, por uma versão **mínima** (cerca de duas páginas)
   que delega à *Manual para Elaboração e Normalização de Trabalhos
   Acadêmicos* da UFRJ/SiBI (9ª edição, 2025) tudo aquilo que esta já
   cobre, e estabelece apenas o conjunto de regras específicas da
   COPPE/UFRJ — identidade institucional, estrutura de três resumos,
   listas próprias, paginação pré-textual, e a adoção das edições
   ABNT pós-2020 (NBR 6023 a partir de 2018 e NBR 10520:2023).

A norma proposta — **NORMA_COPPE_2026.md** — cita a classe `coppe` v4.0+
explicitamente como sua **implementação de referência**, no espírito do
que ocorre com normas técnicas de outras áreas: a definição formal está
no texto, e a verificação automática de conformidade fica a cargo do
artefato computacional.

### Pontos relevantes para a apreciação

- **Compatibilidade total para alunos em curso.** A versão 4.0 preserva
  integralmente o comportamento da v3.x para os dois idiomas
  historicamente suportados (português e inglês). Documentos de alunos
  em fase final compilam **bit a bit** com o mesmo resultado, sem
  qualquer modificação no texto-fonte.

- **Sem dependência adicional para os casos mais comuns.** Para os
  trabalhos em português ou inglês — a grande maioria do programa — não
  é necessário arquivo de configuração adicional algum; basta a classe
  `coppe.cls`, como antes.

- **Identidade institucional preservada.** Em qualquer idioma principal,
  os elementos institucionais (capa, folha de rosto, ficha catalográfica)
  permanecem em português, sendo apenas o título do trabalho exibido
  no idioma principal escolhido.

- **Atualização ABNT.** A versão 4.0 já incorpora as revisões pós-2020
  das normas NBR 6023 e NBR 10520; nenhum novo trabalho do ponto de
  vista de adequação às normas vigentes é necessário.

### Material em anexo

O *branch* `nlinguas` contém, no diretório-raiz, os artefatos a seguir
para apreciação:

- **NORMA_COPPE_2026.md** — proposta de norma (texto mínimo).
- **CHANGELOG.md** — histórico de mudanças da v4.0.
- **dist/coppe.pdf** — manual completo da classe atualizado.
- **dist/example_pt.pdf**, **example_en.pdf**, **example_es.pdf**,
  **example_fr.pdf**, **example_it.pdf** — documentos demonstrativos,
  um por idioma principal embutido.
- **dist/covers_5languages.pdf** — visão panorâmica em uma única página
  das cinco capas, mostrando a uniformidade da identidade institucional.
- **MIGRATION_v3_to_v4.md** — guia curto para alunos que desejarem
  migrar voluntariamente para a v4.0 antes da defesa.
- **CONTRIBUTING.md** — instruções para colaboradores que quiserem
  contribuir com novos pacotes de idioma no futuro.
- **TODO.md** — itens em aberto para a versão final, em particular a
  revisão dos pacotes de espanhol, francês e italiano por falantes
  nativos antes da liberação oficial.

Permanecemos à disposição para apresentar a proposta presencialmente ou
acolher quaisquer sugestões de ajuste por parte desta Comissão.

Atenciosamente,

*[Nome do mantenedor responsável]*
Equipe CoppeTeX
COPPE/UFRJ

---

*Esta carta encontra-se sob versionamento no repositório
<https://github.com/COPPE-UFRJ/CoppeTeX>, no branch `nlinguas`, e
acompanha a Pull Request a ser aberta para o branch `master`.*
