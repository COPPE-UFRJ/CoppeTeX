#
# This is file `Makefile'.
#
# It should be used to strip the CoppeTeX class and its documentation.
#
# Copyright (C) 2008 CoppeTeX Project and any individual authors listed
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
# $URL: https://coppetex.svn.sourceforge.net/svnroot/coppetex/branches/coppetex-2.0/Makefile $
# $Id: Makefile 122 2008-10-21 00:21:50Z helano $
#
# Author(s): Vicente Helano,
#            George Ainsworth
#

PROGRAM_NAME=CoppeTeX Makefile
PACKAGE_NAME=coppe
DOC_SOURCE=coppe.dtx
VERSION="1.0"
AUTHORS=Vicente Helano and George Ainsworth Jr.
COPYRIGHT_YEAR=2007
PACKAGE_BUGREPORT="helano@users.sourceforge.net"

TEX = latex
BIBTEX = bibtex
DVIPS = dvips
DVIPDF = dvipdfm
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
DVIPSFLAGS = -Ppdf -G0 -q -t A4 
DVIPDFMFLAGS = -c -r 300 -p a4
IDXFLAGS = -q -s gind.ist
GLOFLAGS = -q -s gglo.ist
LSTFLAGS = -q -s coppe.ist

.SUFFIXES: .tex .dvi .dtx

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

example: example.tex example.dvi

install: doc class example
	@if [ "$(DESTDIR)" == "" ]; then \
	  $(_printf) "error: empty detination directory.\n"; \
	  make help; \
	  exit 1; \
	fi
	if [ -d "$(CLSDIR)" ]; then \
	  rm -rf $(CLSDIR); \
	fi
	mkdir -vp $(CLSDIR)
	cp -vp $(PACKAGE_NAME).cls minerva.eps minerva.pdf $(CLSDIR)/
	if [ -d "$(BSTDIR)" ]; then \
	  rm -rf $(BSTDIR); \
	fi
	mkdir -vp $(BSTDIR)
	cp -vp $(PACKAGE_NAME)-unsrt.bst $(BSTDIR)/
	if [ -d "$(ISTDIR)" ]; then \
	  rm -rf $(ISTDIR); \
	fi
	mkdir -vp $(ISTDIR)
	cp -vp $(PACKAGE_NAME).ist $(ISTDIR)/
	if [ -d "$(DOCDIR)" ]; then \
	  rm -rf $(DOCDIR); \
	fi
	mkdir -vp $(DOCDIR)
	cp -vp README COPYING $(PACKAGE_NAME).dvi \
		example.tex example.dvi $(DOCDIR)/

dist: distclean
	@${_tar} -jcvf $(PACKAGE_NAME).tar.bz2 ./*

distclean: clean
	@$(_rm) -f $(PACKAGE_NAME).cls example.* *~ coppe.pdf coppe.ps coppe.dvi

clean:
	@$(_rm) -f *.log *.aux *.dvi *.ist *.idx *.blg *.bbl *.glo *.bz2 \
		         *.toc *.lof *.lot *.syx *.abx *.lab *.ilg *.los *.ind \
						 *.gls *.out

help:
	@${_printf} "Usage: make [TARGET]\n" "${PROGRAM_NAME}"
	@${_printf} "Generate various output formats from LaTeX sources.\n"
	@${_printf} "\n"
	@${_printf} "  doc          generate the \`%s' documentation\n" \
	            ${PACKAGE_NAME}
	@${_printf} "  class        strip the \`%s' class and \`example.tex' " \
		          ${PACKAGE_NAME} 
	@${_printf} "from \`%s'\n" ${DOC_SOURCE}
	@${_printf} "%s\n" \
           "  example      generate a DVI file from \`example.tex'" \
           "  dist         create a compressed archive from sources" \
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

$(PACKAGE_NAME).cls example.tex %.ist: $(PACKAGE_NAME).ins
	@$(TEX) $(TEXFLAGS) $<

$(PACKAGE_NAME).dvi: $(PACKAGE_NAME).dtx
	@$(TEX) $(TEXFLAGS) $<
	@$(BIBTEX) $(BIBTEXFLAGS) $(PACKAGE_NAME).aux
	@$(TEX) $(TEXFLAGS) $<
	@$(TEX) $(TEXFLAGS) $<

%.dvi: %.tex
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

.PHONY: all doc class example dist help version clean distclean
