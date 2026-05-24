:: Generate the class and example sources from the .dtx/.ins
pdflatex coppe.ins

:: --- Documentation (coppe.pdf) ---
pdflatex coppe.dtx
makeindex -s gglo.ist -o coppe.gls coppe.glo
makeindex -s gind.ist -o coppe.ind coppe.idx
pdflatex coppe.dtx
pdflatex coppe.dtx

:: --- Example (example.pdf): biblatex/biber bibliography + coppe lists ---
:: First pass writes example.bcf (for biber) and example.abx/.syx (for the
:: lists of abbreviations and symbols); biber resolves the bibliography;
:: makeindex builds the lists; two final passes settle citations and refs.
pdflatex example.tex
biber example
makeindex -s coppe.ist -o example.lab example.abx
makeindex -s coppe.ist -o example.los example.syx
pdflatex example.tex
pdflatex example.tex
