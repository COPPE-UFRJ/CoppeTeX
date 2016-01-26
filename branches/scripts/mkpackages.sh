#!/bin/sh
#
# This is file `mkpackages.sh'
#
# Automatically generates compressed packages for the given release number.
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

TEX=latex
PROJECT=coppetex
SVNROOT=https://svn.code.sf.net/p/coppetex/code
VERSION=$1

if [ "$1" == "" ]; then
  printf "%s: missing version number.\n" "$0"
  exit 1
fi

TMPDIR=`mktemp -d coppetex.XXXXXXXXXX`

# Do we have a new branch or a new tag?
RELKIND=`echo ${VERSION} | tr -dc '.' | wc -c`
BRANCH=''

if [ "${RELKIND}" -eq "1" ]; then # We need to create a branch
  BRANCH=${VERSION}
elif [ "${RELKIND}" -eq "2" ]; then
  BRANCH=${VERSION%.*}
else
  printf "%s: invalid version number.\n" $0
  exit 1
fi

# Creating download packages
printf "%s: exporting tag %s to %s.\n" $0 ${VERSION} ${TMPDIR}
svn --force export ${SVNROOT}/tags/${PROJECT}-${VERSION} ${TMPDIR} > /dev/null
if [ "$?" != "0" ]; then
  printf "%s: invalid version number\n" "$0"
  exit 1
fi

cd $TMPDIR
mkdir ${PROJECT}-${VERSION}{,-src}
svn --force export ${SVNROOT}/branches/template ${PROJECT}-${VERSION}-template > /dev/null

make doc
make example.pdf

DISTFILES='coppe.cls
           coppe.ist
           coppe.pdf
           coppe-logo.eps
           coppe-logo.pdf
           coppe-plain.bst
           coppe-unsrt.bst
           COPYING
           example.bib
           example.tex
           README'

DISTSOURCEFILES='coppe.bib
                 coppe.dtx
                 coppe.ins
                 coppe-logo.eps
                 coppe-logo.pdf
                 coppe-plain.bst
                 coppe-unsrt.bst
                 COPYING
                 example.bib
                 Makefile
                 README'

DISTTEMPLATEFILES='coppe.cls
                   coppe.ist
                   coppe.pdf
                   coppe-logo.eps
                   coppe-logo.pdf
                   coppe-plain.bst
                   coppe-unsrt.bst
                   COPYING
                   README'

cp ${DISTFILES} ${PROJECT}-${VERSION} && \
cp ${DISTSOURCEFILES} ${PROJECT}-${VERSION}-src && \
cp ${DISTTEMPLATEFILES} ${PROJECT}-${VERSION}-template

tar -Jcvf ${PROJECT}-${VERSION}-src.tar.xz ${PROJECT}-${VERSION}-src/*
zip ${PROJECT}-${VERSION}-src.zip ${PROJECT}-${VERSION}-src/*
tar -Jcvf ${PROJECT}-${VERSION}.tar.xz ${PROJECT}-${VERSION}/*
zip ${PROJECT}-${VERSION}.zip ${PROJECT}-${VERSION}/*
tar -Jcvf ${PROJECT}-${VERSION}-template.tar.xz ${PROJECT}-${VERSION}-template/*
zip ${PROJECT}-${VERSION}-template.zip ${PROJECT}-${VERSION}-template/*

cd ..

exit 0
