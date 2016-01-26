#!/bin/sh
#
# This is file `mkrelease.sh'
#
# Automatically generates sourceforge project releases from Subversion
# repositories.
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

if [ "${BRANCH}" == "${VERSION}" ]; then
  printf "%s: creating branch number %s.\n" $0 ${VERSION}
  svn copy ${SVNROOT}/trunk \
      ${SVNROOT}/branches/${PROJECT}-${VERSION} \
      -m "Branching CoppeTeX ${VERSION}."
fi

printf "%s: creating tag number %s.\n" $0 ${VERSION}
svn copy ${SVNROOT}/branches/${PROJECT}-${BRANCH} \
    ${SVNROOT}/tags/${PROJECT}-${VERSION} \
    -m "Tagging CoppeTeX ${VERSION}."

cd ..

exit 0
