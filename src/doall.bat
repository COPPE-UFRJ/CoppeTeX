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

:: --- Sync the minimal distributable set from src to ..\dist ---
:: Only the files an end user needs: the class, the biblatex style files, the
:: makeindex style, the logos, the manual, the example, and the docs. Build
:: intermediates (.aux/.log/.bcf/...) are never copied, to keep dist minimal.
copy /Y coppe.cls ..\dist\ >nul
copy /Y coppe.dbx ..\dist\ >nul
copy /Y coppe.bbx ..\dist\ >nul
copy /Y coppe.cbx ..\dist\ >nul
copy /Y coppe-numeric.bbx ..\dist\ >nul
copy /Y coppe-numeric.cbx ..\dist\ >nul
copy /Y brazilian-coppe.lbx ..\dist\ >nul
copy /Y english-coppe.lbx ..\dist\ >nul
copy /Y coppe.ist ..\dist\ >nul
copy /Y coppe.pdf ..\dist\ >nul
copy /Y coppe-logo.eps ..\dist\ >nul
copy /Y coppe-logo.pdf ..\dist\ >nul
copy /Y example.tex ..\dist\ >nul
copy /Y example.bib ..\dist\ >nul
copy /Y example.pdf ..\dist\ >nul
copy /Y ..\README.md ..\dist\ >nul
copy /Y ..\COPYING ..\dist\ >nul
:: Remove the retired bibtex styles (replaced by the biblatex style files).
del /Q ..\dist\coppe-plain.bst ..\dist\coppe-unsrt.bst ..\dist\en-coppe-plain.bst ..\dist\en-coppe-unsrt.bst 2>nul
