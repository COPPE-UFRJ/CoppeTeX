#
# This is file `Makefile'.
#
# It should be used to strip the CoppeTeX class and its documentation.
#
# Copyright (C) 2011 CoppeTeX Project and any individual authors listed
# elsewhere in this file.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License version 3 for more details.
#
# You should have received a copy of the GNU General Public License
# version 3 along with this package (see COPYING file).
# If not, see <http://www.gnu.org/licenses/>.
#
# $URL$
# $Id$
#
# Author(s): Vicente H. F. Batista
#

PROGRAM_NAME=CoppeTeX Makefile
PACKAGE_NAME=coppe
DOC_SOURCE=coppe.dtx
VERSION="2.2"
AUTHORS=Vicente H. F. Batista and George O. Ainsworth Jr.
COPYRIGHT_YEAR=2011
PACKAGE_BUGREPORT="helano@users.sourceforge.net"

TEX = pdflatex
BIBTEX = bibtex
MAKEIDX = makeindex
_printf=printf
_rm=rm
_tar=tar

CLSDIR=$(DESTDIR)/tex/latex/coppe
BSTDIR=$(DESTDIR)/bibtex/bst/coppe
ISTDIR=$(DESTDIR)/makeindex/coppe
DOCDIR=$(DESTDIR)/doc/latex/coppe

TEXFLAGS  = 
BIBTEXFLAGS = -terse
IDXFLAGS = -q -s gind.ist
GLOFLAGS = -q -s gglo.ist
LSTFLAGS = -q -s coppe.ist

DIST_CONTENT=coppe.cls coppe.ist coppe.pdf coppe-plain.bst coppe-unsrt.bst COPYING example.bib example.tex coppe-logo.eps coppe-logo.pdf README
DISTSRC_CONTENT=coppe.bib coppe.dtx coppe.ins coppe-plain.bst coppe-unsrt.bst COPYING example.bib Makefile coppe-logo.eps coppe-logo.pdf README

.SUFFIXES: .tex .dtx

all:
	@${_printf} "make: unknown target\n"
	@${_printf} "Try \`make help' for more information.\n" >&2

doc: $(PACKAGE_NAME).dtx
	@$(TEX) $(TEXFLAGS) $<
	@if grep -s "There were undefined references" $(basename $<).log; then \
	  $(BIBTEX) $(BIBTEXFLAGS) $(basename $<).aux; \
	fi
	@if grep -s '$(basename $<).idx' $(basename $<).log; then \
	  $(MAKEIDX) $(IDXFLAGS) $(basename $<).idx -o $(basename $<).ind;\
	fi
	@if grep -s '$(basename $<).glo' $(basename $<).log; then \
	  $(MAKEIDX) $(GLOFLAGS) $(basename $<).glo -o $(basename $<).gls;\
	fi
	@i=6 ; \
	while grep "Rerun to get cross-references right" $(basename $<).log && \
	  [ $$i -gt 0 ] ; do \
	  $(TEX) $(TEXFLAGS) $< ; \
		let "i--"; \
	done

class: $(PACKAGE_NAME).cls

install: doc class example.pdf
	@if [ "$(DESTDIR)" == "" ]; then \
	  $(_printf) "error: empty detination directory.\n"; \
	  make help; \
	  exit 1; \
	fi
	if [ -d "$(CLSDIR)" ]; then \
	  rm -rf $(CLSDIR); \
	fi
	mkdir -vp $(CLSDIR)
	cp -vp $(PACKAGE_NAME).cls coppe-logo.eps coppe-logo.pdf $(CLSDIR)/
	if [ -d "$(BSTDIR)" ]; then \
	  rm -rf $(BSTDIR); \
	fi
	mkdir -vp $(BSTDIR)
	cp -vp $(PACKAGE_NAME)-*.bst $(BSTDIR)/
	if [ -d "$(ISTDIR)" ]; then \
	  rm -rf $(ISTDIR); \
	fi
	mkdir -vp $(ISTDIR)
	cp -vp $(PACKAGE_NAME).ist $(ISTDIR)/
	if [ -d "$(DOCDIR)" ]; then \
	  rm -rf $(DOCDIR); \
	fi
	mkdir -vp $(DOCDIR)
	cp -vp README COPYING $(PACKAGE_NAME).pdf \
		example.tex example.pdf $(DOCDIR)

help:
	@${_printf} "Usage: make [TARGET]\n" "${PROGRAM_NAME}"
	@${_printf} "CoppeTeX development Makefile.\n"
	@${_printf} "\n"
	@${_printf} "  doc          generate the \`%s' documentation\n" \
	            ${PACKAGE_NAME}
	@${_printf} "  class        strip the \`%s' class and \`example.tex' " \
		          ${PACKAGE_NAME} 
	@${_printf} "from \`%s'\n" ${DOC_SOURCE}
	@${_printf} "%s\n" \
           "  example.pdf  generate a PDF file from \`example.tex'" \
           "  clean        remove auxiliary archives" \
	         "  install      install class in DESTDIR" \
           "  help         display this message and exit" \
           "  version      print version information and exit"
	@${_printf} "\n"
	@${_printf} "Report bugs to <%s>.\n" "${PACKAGE_BUGREPORT}"

version:
	@${_printf} "%s %s\n\n" "${PROGRAM_NAME}" "${VERSION}"
	@${_printf} "Copyright (C) %d %s\n" "${COPYRIGHT_YEAR}" "${AUTHORS}"
	@${_printf} "This program is a free software and you can redistribute %s\n" \
		"it and/or"
	@${_printf} "modify it under the terms of the GNU General Public License as\n"
	@${_printf} "published by the Free Software Foundation.\n"
	@${_printf} "See COPYING for more details.\n"

$(PACKAGE_NAME).cls: $(PACKAGE_NAME).ins
	@$(TEX) $(TEXFLAGS) $<

example.tex: $(PACKAGE_NAME).ins
	@$(TEX) $(TEXFLAGS) $<

%.ist: $(PACKAGE_NAME).ins
	@$(TEX) $(TEXFLAGS) $<

%.pdf: %.tex
	@$(TEX) $(TEXFLAGS) $<
	@if grep -s "There were undefined references" $(basename $<).log; then \
	  $(BIBTEX) $(BIBTEXFLAGS) $(basename $<).aux; \
	fi
	@if grep -s '$(basename $<).idx' $(basename $<).log; then \
	  $(MAKEIDX) $(IDXFLAGS) $(basename $<).idx -o $(basename $<).ind;\
	fi
	@if grep -s '$(basename $<).syx' $(basename $<).log; then \
	  $(MAKEIDX) $(LSTFLAGS) $(basename $<).syx -o $(basename $<).los;\
	fi
	@if grep -s '$(basename $<).abx' $(basename $<).log; then \
	  $(MAKEIDX) $(LSTFLAGS) $(basename $<).abx -o $(basename $<).lab;\
	fi
	@$(TEX) $(TEXFLAGS) $<
	@i=6 ; \
	while grep "Rerun to get cross-references right" $(basename $<).log && \
	  [ $$i -gt 0 ] ; do \
	  $(TEX) $(TEXFLAGS) $< ; \
		let "i--"; \
	done

.PHONY: clean

clean:
	@$(_rm) -f *.log *.aux *.ist *.idx *.blg *.bbl *.glo *.bz2 \
		         *.toc *.lof *.lot *.syx *.abx *.lab *.ilg *.los *.ind \
						 *.gls *.out *~ coppe.pdf coppe.cls example.pdf example.tex
