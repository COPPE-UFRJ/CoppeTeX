#
# This is file `Makefile'.
#
# Here's a description...
#
# Copyright (C) 2007 Vicente Helano, George Ainsworth Jr. and Alvaro Cuno
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this package; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor,
# Boston, MA  02110-1301, USA.
#
# $URL$
# $Id$
#
# Author(s): Vicente Helano,
#            George Ainsworth,
#            Alvaro Cuno
#

PROGRAM_NAME=CoppeTeX Makefile
PACKAGE_NAME=coppe
DOC_SOURCE=coppe.dtx
VERSION="1.0"
AUTHORS=Vicente Helano, George Ainsworth Jr. and Alvaro Cuno
COPYRIGHT_YEAR=2007
PACKAGE_BUGREPORT="helano@inbox"

TEX = latex
BIBTEX = bibtex
DVIPS = dvips
DVIPDF = dvipdfm
MAKEIDX = makeindex
_printf=printf
_rm=rm
_tar=tar

TEXFLAGS  = -interaction=batchmode
BIBTEXFLAGS = -terse
DVIPSFLAGS = -Ppdf -G0 -q -t A4 
DVIPDFMFLAGS = -c -r 300 -p a4
IDXFLAGS = -q -s gind.ist
SYXFLAGS = -q -s coppe-symbl.ist
ABXFLAGS = -q -s coppe-abbrev.ist

.SUFFIXES: .tex .dvi .dtx

all:
	@${_printf} "make: unknown target\n"
	@${_printf} "Try \`make help\' for more information.\n" >&2

doc: $(PACKAGE_NAME).dvi

class: $(PACKAGE_NAME).cls

example: example.tex example.dvi

dist: distclean
	@${_tar} -jcvf $(PACKAGE_NAME).tar.bz2 ./*

distclean: clean
	@$(_rm) -f $(PACKAGE_NAME).cls example.tex *~ 

clean:
	@$(_rm) -f *.log *.aux *.dvi *.ist *.idx *.blg *.bbl *.glo *.bz2 \
		         *.toc *.lof *.lot *.syx *.abx *.lab *.ilg *.los *~ 

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

$(PACKAGE_NAME).cls example.tex: $(PACKAGE_NAME).ins
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
	  $(MAKEIDX) $(SYXFLAGS) $(basename $<).syx -o $(basename $<).los;\
	fi
	@if grep -s '$(basename $<).abx' $(basename $<).log; then \
	  $(MAKEIDX) $(ABXFLAGS) $(basename $<).abx -o $(basename $<).lab;\
	fi
	@i=6 ; \
	while grep "Rerun to get cross-references right" $(basename $<).log && \
	  [ $$i -gt 0 ] ; do \
	  $(TEX) $(TEXFLAGS) $< ; \
		let "i--"; \
	done

.PHONY: all doc class example dist help version clean distclean
