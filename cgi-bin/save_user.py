#!/usr/bin/python
#
# This is file `save_user.py'.
#
# It contains code to save details of publications from CoppeTeX users
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
# $URL: https://coppetex.svn.sourceforge.net/svnroot/coppetex/branches/www/cgi-bin/save_user.py $
# $Id: save_user.py 163 2009-03-05 23:21:52Z helano $
#
# Author(s): Vicente Helano,
#            George Ainsworth
#

import cgi

form = cgi.FieldStorage()

def get_bibdata(form):
  bibdata = {}
  bibdata['author'] = form['author'].value
  bibdata['title'] = form['title'].value
  if form['schoolbutton'].value == "on":
    bibdata['school'] = form['schoolname'].value     
    bibdata['dept'] = form['otherdeptname'].value
  else:
    bibdata['school'] = form['schoolbutton'].value
    bibdata['dept'] = form['dept'].value
  bibdata['year'] = form['year'].value
  bibdata['doctype'] = form['doctype'].value
  return bibdata

def get_biblabel(author, degree, year):
  label = "".join(author.split(" "))
  label += "_" + degree + year
  return label

bibtype = {"msc": "mastersthesis", "dscexam": "misc", "dsc": "phdthesis"}
data = {}
data = get_bibdata(form)

if data != {}:
  print "<p>Thank you for submitting your information to CoppeTeX!</p>"
  biblabel = ""
  biblabel = get_biblabel(data['author'], data['doctype'], data['year'])
  f = open("../persistent/data/coppetex.bib", "a")
  f.write( "@" + bibtype[data['doctype']] + "{ ")
  f.write(biblabel + ",\n")
  f.write("  author = {" + data['author'] + "},\n")
  f.write("  title = {" + data['title'] + "},\n")
  f.write("  school = {" + data['school'] + "},\n")
  f.write("  department = {" + data['dept'] + "},\n")
  f.write("  year = {" + data['year'] + "},\n")
  f.write("}\n\n")
  f.close()
