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
# $URL: https://coppetex.svn.sourceforge.net/svnroot/coppetex/branches/scripts/build_packages.sh $
# $Id: build_packages.sh 138 2008-11-08 18:24:02Z helano $
# $Author$
#
# Author(s): Vicente Helano <helano@inbox.com>
#
# TODO
#   - automatic update downloads page
#

TEX=latex
TMPDIR=`mktemp -d coppetex.XXXXXXXXXX`

echo -n "updating working copy... "
svn update

# get URL
URL=`svn info | grep URL | cut -d " " -f 2`
VERSION=`svn info | grep URL | cut -d "-" -f 2`
SVNROOT=`svn info | grep "Repository Root" | cut -d " " -f 3`
BRANCH=${SVNROOT}/branches/coppetex-${VERSION}
TAG=${SVNROOT}/tags/coppetex-${VERSION}

echo "removing old tag."
svn rm -m "Removing old tag." ${TAG}
echo "tagging Coppetex" ${VERSION}
svn cp -m "Release tag for version ${VERSION}" ${BRANCH} ${TAG}

# make packages: sources and minimum toolkit
svn --force export ${TAG} ${TMPDIR}
cd ${TMPDIR}
SOURCES=`ls`
DISTFILES='coppe.bib coppe.cls coppe.ist coppe.pdf coppe-unsrt.bst COPYING example.pdf example.tex README'

make class doc example
dvipdfm example.dvi
dvipdfm coppe.dvi

mkdir -p coppetex-${VERSION}{,-src}
cp ${SOURCES} coppetex-${VERSION}-src
cp ${DISTFILES} coppetex-${VERSION}

tar -zcvf coppetex-${VERSION}-src.tar.gz coppetex-${VERSION}-src/*
zip coppetex-${VERSION}-src.zip coppetex-${VERSION}-src/*
tar -zcvf coppetex-${VERSION}.tar.gz coppetex-${VERSION}/*
zip coppetex-${VERSION}.zip coppetex-${VERSION}/*

mv *.tar.gz *.zip ../

cd -
rm -rf ${TMPDIR}

# send files
PACKAGES='coppetex-1.0.tar.gz coppetex-1.0.zip coppetex-1.0-src.tar.gz coppetex-1.0-src.zip'
for i in ${PACKAGES}; do
  scp $i helano@frs.sourceforge.net:uploads/${i}
done

exit 0
