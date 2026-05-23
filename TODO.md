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