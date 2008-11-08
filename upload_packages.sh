#!/bin/sh
#
# This is file `upload_packages.sh'
#
# Uploads CoppeTeX packages for a specific release.
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

PACKAGES='coppetex-1.0.tar.gz coppetex-1.0.zip coppetex-1.0-src.tar.gz coppetex-1.0-src.zip'
for i in ${PACKAGES}; do
  scp $i helano@frs.sourceforge.net:uploads/${i}
done
