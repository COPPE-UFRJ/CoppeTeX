# Todo for CoppeTex 4.0 - Phase 1 - Bibliography

This project aims to upgrade CoppeTeX LaTeX style for thesis and dissertations (and other documents) at COPPE/UFRJ to 

1. Use BibLaTeX instead of BibTeX
2. Conform its citations with new rules
3. Conform its references with new rules
4. All needed changes that allow for language problems, such as "and" or "e" in an author list, must be completely compatible and solved with babel, either selection brazilian or english
5. brazilian and english are the standard packages used with CoppeLaTeX
6. Since this a long work, you must garantee that no work is lost if Claude or the computer stops


## Extract all types of references from manual2024

0. Create a file howto.md from manual2024.pdf that specify, in the best style that you can use, all the types of references, it is fields, how they are formated, and blocks.
1. List all types of references from 4.2 REFERÊNCIAS in desiredreferences.md; those will be our biblatex entries
2. List all types of elements of referes from 4.3 ELEMENTOS DE REFERECIAS in desiredelements.md; those will be our biblatex fields
4. You should prepare for creating a biblatex package supporting manual2024 as much as possible
5. Beware of formatting, not only text



## Convert from BibTeX to BibLaTex

0. Must program everything in the files coppe.dtx and coppe.ins
1. Must generate all needed files from .dtx and .ins
2. From desideredreferences.md and desiredelement.md you shold ask me in which entry and field to map, providing a .csv file for me to check before continuing.
3. Must remove all references do bibtex
4. Must provide BibLaTeX with natbib option
5. Keep numeric and author-year styles
6. Must follow manual2024.pdf that superseded oldmanual.pdf, however, if manual2024 does not say something, oldmanual.pdf can still be used.
7. Must support EVERY TYPE OF REFERENCE described on file manual2024.pdf
8. Every type of reference should be a entry type in english. For example: @book, @article, ...
9. There should be a synonim in portuguese, for example, @livro should be the same as @book
10. Every necessary or optional field should be in english. For exemple: title, author, url
11. There should be a synonim in portuguese, with no accentuation, for example, titulo should be the same as title 
12. Should support babel, as in coppe.sty (that is generated from coppe.dtx) 
13. Provide english and brazilian options, following the option in the coppe.sty
14. All necessary .bbx should be generated from coppe.dtx
15. All necessary .cbx should be generated from coppe.dtx
16. All necessary .lbx should be generated from coppe.dtx
17. All necessary .dbx should be generated from coppe.dtx
18. Generate a .tex and a .bib file that should compile, later, in the end of the project, exactly as manual2024.pdf. This is the text that everything is ok
19. Do not change anything not related to bibliography in coppe.tex and coppe.dtx
20. The document example.pdf should compile without any new errors, and must reflect that ONLY the handling of bibligraphy was changed
21. You must support the numeric style and the author-date style
22. You must support unsorted
23. All formatting should be deferred for output. For example, a title that should be bold, as in "obras de um só autor", should only be converted to bold in the output 
24. It should be never necessary for format an entry, we should never do something as title="\textbf{Title}" in the .bib file
25 When possible, join types in the english name. For example, "Obras de um só autor", "Obras com até três autores". "Obras com mais de 3 autores", "Obras com um autor pessoal", should be all refered to "book", through synonims, since they are mostly a book. 

## Provide hard evidence that all work as done

You must provide a .tex file with all kind of citations and references to prove that the change work

# Todo for CoppeTex 4.0 - Phase 2 - Caption

In the new format, every float with caption, like ilustration, figure, or table, should have the caption over it, and the source (as Fonte:) under it. Therefore, there must be a command almost like \caption and provide the source, as in \source{}, but does not advance caption numbering.

The following floats: figure, table, frame (for "quadro" in brazilian). 

There should be a command to configure a new float, such as "picture", allways following the \caption, \source rule, and also to provide a command to put a list in the front part of the text (such as \listofpictures)

If any new command, such as \source, can cause an error or clash with other package, the rule is to rename \commmand as \cpcommand;

everything must be babel compatible

# VERIFY THAT THESE CHANGES ARE WORKING AS THEY SHOULD WORK NOW

A NBR 10520 é uma norma que engloba todas as regras para que você faça citações no seu trabalho da forma certa e sem cometer plágio. No mês de julho de 2023 essa diretriz passou por algumas alterações e agora você vai conferir as principais.

Pontuação
Você deve usar o ponto final para terminar a frase, e não a citação.

Antes:  “A autenticidade e a conexão emocional são elementos-chave para construir uma marca sólida no cenário atual.” (SANTOS, 2022, p. 78).

Depois: “A autenticidade e a conexão emocional são elementos-chave para construir uma marca sólida no cenário atual” (Santos, 2022, p. 78).

Sistema autor-data (pessoa física)
Não se deve usar mais a caixa alta no final da citação. Agora, é necessário que você coloque letras maiúsculas e minúsculas dentro do parênteses.

Antes: Atender o cliente com qualidade é importante para toda empresa que deseja encantar os consumidores e ter sucesso. (SOUZA, 2015).

Depois: Atender o cliente com qualidade é importante para toda empresa que deseja encantar os consumidores e ter sucesso (Souza, 2015).

Sistema autor-data (pessoa jurídica)
Utilize o nome completo da organização em letras maiúsculas e minúsculas. 

Antes: (SERVIÇO BRASILEIRO DE APOIO ÀS MICRO E PEQUENAS EMPRESAS, 2022, p.15).

Depois: (Serviço Brasileiro de Apoio às Micros e Pequenas Empresas, 2022, p.15).

As siglas devem continuar em caixa alta. Ex.: (SEBRAE, 2022).

Citação direta longa
O recuo de 4 cm para a esquerda em citações com mais de 3 linhas deixa de ser obrigatório e passa a ser recomendado. Assim, os pesquisadores podem escolher usá-lo ou não.

Uso do Et al. 

Utilizar o et al. para citar obras com mais de 3 autores passou a ser opcional. Você pode mencionar todos os autores na citação ou continuar usando o et.al.

Exemplo:

“O papel da inteligência emocional no ambiente de trabalho é crucial para promover um clima organizacional saudável” (Garcia; Torres; Araújo; Souza, 2019, p. 56).

“O papel da inteligência emocional no ambiente de trabalho é crucial para promover um clima organizacional saudável” (Garcia et al., 2019, p. 56).

Citação de citação
As expressões latinas, como o apud, devem ser grafadas em itálico.

Antes:  “A inovação é um catalisador para o crescimento organizacional, sendo imperativo adotar práticas que estimulem a criatividade e a implementação de novas ideias.” (OLIVEIRA, 1995 apud SANTOS, 2015, p. 56).

Depois: “A inovação é um catalisador para o crescimento organizacional, sendo imperativo adotar práticas que estimulem a criatividade e a implementação de novas ideias” (Oliveira 1995 apud Santos, 2015, p. 56).

Paginação na citação direta
Você precisa mencionar a página ou a localização, apenas se houver.

Exemplo:

De acordo com Ferreira (2019, p. 49), “a globalização impacta diretamente as estratégias de mercado das organizações”.

“A criatividade desempenha um papel fundamental na concepção de soluções inovadoras para os desafios contemporâneos” (Carvalho, 2000, local. 288).

Como fazer citação direta?
Citação direta é quando você “copia e cola” as palavras exatas de outra pessoa no seu trabalho, indicando a fonte. A citação direta pode ser curta ou longa.

Citação direta curta
A citação direta curta tem até 3 linhas. Para fazê-la corretamente, coloque:

o sobrenome do autor;
o ano da publicação;
a página ou local (se houver);
aspas na citação.
Exemplos: 

Segundo Silva (2019, p. 35 ) “a educação é a chave para que a sociedade progrida e tenha melhores condições de sobrevivência”.

“A educação é a chave para que a sociedade progrida e tenha melhores condições de sobrevivência” (Silva, 2019, p. 35).

Citação direta longa
Quando a citação direta for longa (com mais de 3 linhas), você precisa indicar:

o sobrenome do autor;
o ano da publicação;
a página (se houver);
aplicar recuo de 4cm à esquerda (Recomenda-se o recuo de 4cm);
usar espaçamento simples.
Exemplos:

O desenvolvimento sustentável é um conceito amplo que envolve a integração entre aspectos ambientais, sociais e econômicos. Nesse contexto, Silva (2018, p. 78) destaca:

A importância da sustentabilidade tornou-se evidente nas últimas décadas, com a necessidade premente de preservar os recursos naturais para as gerações futuras. Esse paradigma exige uma abordagem holística, considerando não apenas as questões ambientais, mas também os impactos sociais e econômicos das ações humanas.

A importância da sustentabilidade tornou-se evidente nas últimas décadas, com a necessidade premente de preservar os recursos naturais para as gerações futuras. Esse paradigma exige uma abordagem holística, considerando não apenas as questões ambientais, mas também os impactos sociais e econômicos das ações humanas (Silva, 2018, p. 78).

Como fazer citação indireta?
Citação indireta é quando você expressa com as suas próprias palavras as ideias de outro autor. É como contar para alguém o que você entendeu de um texto, mas dando crédito à fonte da informação. Essa prática ajuda a aumentar a credibilidade da sua pesquisa, pois ela será fundamentada pelas opiniões de especialistas.

Citação indireta curta
A citação indireta curta é composta de até 3 linhas. Para fazê-la da forma certa no seu trabalho, coloque:

o sobrenome do autor;
o ano da publicação;
Exemplo: 

Segundo Oliveira (2016), a gestão eficaz de projetos é crucial para o sucesso organizacional, pois permite o alinhamento estratégico de recursos e metas. Assim, a eficiência na condução de projetos contribui significativamente para a obtenção de resultados positivos.

A gestão eficaz de projetos é crucial para o sucesso organizacional, pois permite o alinhamento estratégico de recursos e metas. Nesse contexto, a eficiência na condução de projetos contribui significativamente para a obtenção de resultados positivos (Oliveira, 2016).

Citação indireta longa
Esse tipo de citação tem mais de 3 linhas e deve ser feita mencionando:

o sobrenome do autor;
o ano da publicação;
aplicar recuo de 4cm à esquerda (recomendado o recuo de 4 cm );
usar espaçamento simples.
Exemplos:

Segundo Oliveira (2018):

A gestão estratégica envolve a formulação e implementação de estratégias organizacionais, sendo essencial para o alcance dos objetivos a longo prazo. Assim, o autor destaca a necessidade de alinhar as ações da empresa com sua visão e missão, garantindo uma direção consistente para todas as atividades. 

A gestão estratégica envolve a formulação e implementação de estratégias organizacionais, sendo essencial para o alcance dos objetivos a longo prazo. Assim, o autor destaca a necessidade de alinhar as ações da empresa com sua visão e missão, garantindo uma direção consistente para todas as atividades (Oliveira, 2018).

Como fazer citação da citação?
A citação de citação ocorre quando você cita um autor mencionado por outro autor. Em outras palavras, você não teve acesso direto à obra original, mas sim a um trecho dela em outro trabalho. 

Esse tipo de citação deve ser utilizado com moderação, pois é preferível indicar diretamente a fonte original sempre que possível. Quando necessário, você deve citar o autor que encontrou a informação, seguido pela expressão “apud” (citado por) e o autor da obra original.

Exemplos:

Segundo Martins (2020 apud Santos, 1990, p. 75), “a tecnologia desempenha um papel crucial na transformação dos processos de negócios, proporcionando eficiência e inovação.”

“A tecnologia desempenha um papel crucial na transformação dos processos de negócios, proporcionando eficiência e inovação”  (Martins, 2020 apud Santos, 1990, p. 75).

Fazer citação corretamente em trabalhos acadêmicos é fundamental para reforçar os argumentos da sua pesquisa e dar crédito às fontes para evitar plágio. Seguir as normas da ABNT é essencial para manter a consistência e qualidade do document

