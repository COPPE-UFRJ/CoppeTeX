#!/bin/sh
# send files
PACKAGES='coppetex-1.0.tar.gz coppetex-1.0.zip coppetex-1.0-src.tar.gz coppetex-1.0-src.zip'
for i in ${PACKAGES}; do
  scp $i helano@frs.sourceforge.net:uploads/${i}
done
