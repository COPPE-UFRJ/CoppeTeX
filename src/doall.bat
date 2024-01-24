pdflatex coppe.ins
pdflatex coppe.dtx
makeindex -s gglo.ist -o coppe.gls coppe.glo
makeindex -s gind.ist -o coppe.ind coppe.idx
pdflatex coppe.dtx
pdflatex example.tex
makeindex -s gglo.ist -o coppe.gls coppe.glo
makeindex -s gind.ist -o coppe.ind coppe.idx
makeindex -s coppe.ist -o example.lab example.abx
makeindex -s coppe.ist -o example.los example.syx
pdflatex coppe.dtx
pdflatex coppe.dtx
pdflatex example.tex
bibtex coppe
bibtex example
pdflatex coppe.dtx
pdflatex example.tex

