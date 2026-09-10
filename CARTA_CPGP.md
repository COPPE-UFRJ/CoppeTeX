# Ofício de encaminhamento à CPGP/COPPE/UFRJ

*Rascunho — sujeito à revisão pela equipe mantenedora antes do envio.*

---

**Para:** Comissão de Programas de Pós-Graduação (CPGP) da COPPE/UFRJ
**Assunto:** Encaminhamento de proposta de deliberação — Norma para a
Elaboração Gráfica de Teses e Dissertações da COPPE/UFRJ, edição 2026, e
implementação de referência CoppeTeX 4.1
**Data:** setembro de 2026

---

Prezada Comissão,

Encaminhamos para apreciação e deliberação a proposta constante de
[`PROPOSTA_CPGP.md`](./PROPOSTA_CPGP.md), que submete a esta Comissão a
**Norma para a Elaboração Gráfica de Teses e Dissertações da COPPE/UFRJ,
edição 2026**, e o reconhecimento da classe LaTeX `coppe` versão **4.1** como
sua implementação de referência.

A proposta é curta de propósito, e o que ela pede é uma decisão de método: que
a COPPE **pare de manter uma descrição própria do formato** e passe a adotar
integralmente o *Manual para Elaboração e Normalização de Trabalhos
Acadêmicos* da UFRJ/SiBI, registrando apenas — em catorze seções — onde a COPPE
o especializa: as logomarcas, o nome da instituição em três linhas, a lista de
Programas, a identidade institucional em português, a posição da orientação,
os orientadores nas páginas de resumo, o terceiro resumo, o idioma principal,
as listas de Quadros, Programas e Algoritmos, a fonte das ilustrações, o
formato de Apêndices e Anexos, a numeração das folhas, o layout do sumário
e as edições ABNT adotadas.

Nenhum desses catorze pontos é novo. Todos já são praticados. O que a proposta
muda é que passam a estar escritos num só lugar, com a indicação de qual item
do Manual cada um especializa, e passam a ser **verificáveis por medição** —
não por leitura.

Três observações que talvez ajudem a apreciação:

- **Compatibilidade.** Para trabalhos em português ou inglês, a classe
  continua bastando sozinha, sem arquivo de configuração adicional. As
  mudanças de forma que a edição 2026 do Manual trouxe estão listadas em
  [`MIGRATION_v3_to_v4.md`](./MIGRATION_v3_to_v4.md) e nenhuma exige reescrever
  texto.

- **Identidade institucional.** Capa, folha de rosto e ficha catalográfica
  permanecem em português em qualquer idioma de redação. As cinco capas lado a
  lado, em `dist/covers_5languages.pdf`, mostram isso em uma página.

- **Evidência.** A conformidade não é afirmada, é medida: doze documentos
  completos nos quatro tipos de trabalho e nos três idiomas admitidos,
  compilados nos dois motores, com o PDF pronto conferido contra a norma em
  centímetros e em ordem, e o PDF/A validado pelo veraPDF. A Seção 3.4 da
  proposta traz os números, e um único comando os reproduz.

A Seção 4 da proposta reúne três questões que são de mérito e não de
implementação — PDF/A por padrão, coorientador nas páginas de resumo e a
revisão terminológica do espanhol —, sobre as quais a equipe mantenedora
gostaria de ouvir a Comissão.

Permanecemos à disposição para apresentar a proposta presencialmente ou
acolher quaisquer sugestões de ajuste.

Atenciosamente,

*[Nome do mantenedor responsável]*
Equipe CoppeTeX
COPPE/UFRJ

---

*Esta carta encontra-se sob versionamento no repositório
<https://github.com/COPPE-UFRJ/CoppeTeX>, no branch `nlinguas`, e acompanha a
Pull Request a ser aberta para o branch `master`.*
