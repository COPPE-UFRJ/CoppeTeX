#!/bin/sh
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
