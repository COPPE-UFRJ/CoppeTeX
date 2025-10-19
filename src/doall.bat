# Generate files from the .ins
pdflatex coppe.ins

# Build the manual (from .dtx)
pdflatex coppe.dtx        # writes coppe.bcf
makeindex -s gglo.ist -o coppe.gls coppe.glo
makeindex -s gind.ist -o coppe.ind coppe.idx
biber coppe               # reads coppe.bcf, writes coppe.bbl
pdflatex coppe.dtx
pdflatex coppe.dtx        # ensure all refs settle

# Build the example using your styles
pdflatex example.tex      # writes example.bcf
makeindex -s coppe.ist -o example.lab example.abx   # (only if you use makeidx w/ custom styles)
makeindex -s coppe.ist -o example.los example.syx   # (idem)
biber example             # reads example.bcf
pdflatex example.tex
pdflatex example.tex
