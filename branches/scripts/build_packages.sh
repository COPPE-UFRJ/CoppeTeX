#!/bin/sh
#
# This is file `build_packages.sh'
#
# Automatically generates CoppeTeX packages for a specific release.
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
# $URL$
# $Id$
#
# Author(s): Vicente Helano <helano@inbox.com>
#
# TODO
#   - automatic update downloads page
#

TEX=latex
#TMPDIR=`mktemp -d coppetex.XXXXXXXXXX`
TMPDIR=coppetex-release
PROJECT=coppetex
SVNROOT=https://coppetex.svn.sourceforge.net/svnroot/coppetex
VERSION=$1

if [ "$1" == "" ]; then
  printf "%s: missing version number\n" "$0"
  exit 1
fi

svn --force export ${SVNROOT}/tags/coppetex-${VERSION} $TMPDIR > /dev/null
if [ "$?" != "0" ]; then
  printf "%s: invalid version number\n" "$0"
  exit 1
fi

cd $TMPDIR
svn --force export ${SVNROOT}/branches/template ${PROJECT}-${VERSION}-template > /dev/null

mkdir ${PROJECT}-${VERSION}{,-src}
DISTFILES='coppe.bib coppe.cls coppe.ist coppe.pdf coppe-unsrt.bst COPYING minerva.pdf minerva.eps example.tex example.pdf README'
SRCFILES='coppe.bib coppe.ins COPYING minerva.eps README coppe.dtx coppe-unsrt.bst Makefile minerva.pdf'
TEMPLATEFILES='coppe.cls coppe.ist coppe-unsrt.bst COPYING README minerva.pdf minerva.eps coppe.pdf'

make example doc
pdflatex coppe.dtx
pdflatex coppe.dtx

cp ${DISTFILES} ${PROJECT}-${VERSION} && \
cp ${SRCFILES} ${PROJECT}-${VERSION}-src && \
cp ${TEMPLATEFILES} ${PROJECT}-${VERSION}-template

tar -zcvf coppetex-${VERSION}-src.tar.gz coppetex-${VERSION}-src/*
zip coppetex-${VERSION}-src.zip coppetex-${VERSION}-src/*
tar -zcvf coppetex-${VERSION}.tar.gz coppetex-${VERSION}/*
zip coppetex-${VERSION}.zip coppetex-${VERSION}/*
tar -zcvf coppetex-${VERSION}-template.tar.gz coppetex-${VERSION}-template/*
zip coppetex-${VERSION}-template.zip coppetex-${VERSION}-template/*

cd ..

# send files
#PACKAGES='coppetex-1.0.tar.gz coppetex-1.0.zip coppetex-1.0-src.tar.gz coppetex-1.0-src.zip'
#for i in ${PACKAGES}; do
#  scp $i helano@frs.sourceforge.net:uploads/${i}
#done

exit 0
