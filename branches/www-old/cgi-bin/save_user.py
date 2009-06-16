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

print "Content-type: text/html; charset=iso-8859-1\n"
print """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"
"http://www.w3.org/TR/html4/strict.dtd">
<html lang="en">

<head>
  <title>CoppeTeX</title>
  <meta http-equiv="Content-Language" content='en'>
  <meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
  <meta name="keywords" content="coppetex,coppe,ufrj,latex,document class,latex package, thesis,dissertation,">
  <meta name="description" content="A LaTeX tool kit useful for writing dissertations and thesis at COPPE/UFRJ.">

  <link rel="shortcut icon" href="/images/favicon.ico" >
  <link href="/style/main.css" rel="stylesheet" type="text/css" media="all">
  <link href="/style/header.css" rel="stylesheet" type="text/css" media="all">
  <link href="/style/navbar.css" rel="stylesheet" type="text/css" media="all">
  <link href="/style/content.css" rel="stylesheet" type="text/css" media="all">
  <link href="/style/footer.css" rel="stylesheet" type="text/css" media="all">
  <link href="/style/downloads.css" rel="stylesheet" type="text/css" media="all">
  <script type="text/javascript" src="/scripts/lastmod.js"></script>
</head>

<body>
<div id="header">
  <!-- Google CSE Search Box Begins  -->
  <form id="searchbox_014050451544240989057:qn0p_qkdkmy" action="http://coppetex.sourceforge.net/results.html">
  <div>
  <label for="q" title="Search CoppeTeX's site">search coppetex:</label> 
  <input type="hidden" name="cx" value="014050451544240989057:qn0p_qkdkmy">
  <input type="hidden" name="cof" value="FORID:10">
  <input type="text" id="q" name="q" size="25">
  <input type="submit" name="sa" value="Go">
  </div>
  </form>
  <script type="text/javascript"
src="http://www.google.com/coop/cse/brand?form=searchbox_014050451544240989057%3Aqn0p_qkdkmy">
  </script>
  <!-- Google CSE Search Box Ends -->
  <p>
  A LaTeX tool kit useful for<br>
  writing dissertations and<br>
  thesis at COPPE/UFRJ.
  </p>
</div>

<div id="navbar">
  <div id="menu">
    <ul>
    <li><a href="/index.html">Home</a></li>
    <li><a href="/download.html" id="current-page">Downloads</a></li>
    <li><a href="/install.html">Install</a></li>
    <li><a href="/doc.html">Documentation</a></li>
    <li><a href="/mailing-list.html">Mailing List</a></li>
    <li><a href="/team.html">Team</a></li>
    <li class="lastli"><a href="/contact.html">Contact</a></li>
    </ul>
  </div>
  <div id="banners">
  <p>Friend Projects:</p>
    <a href="http://www.ctan.org">
<img src="/images/banner_ctan.png" alt="CTAN banner."></a><br>
    <a href="http://www.latex-project.org">
<img src="/images/banner_latex.png" alt="LaTeX Project banner."></a><br>
    <a href="http://www.tex-br.org">
<img src="/images/banner_tex-br.png" alt="TeX-BR Wiki banner."></a><br>
  <p>Hosted by:</p>
    <a href="http://sourceforge.net">
    <img
      src="http://sflogo.sourceforge.net/sflogo.php?group_id=199659&amp;type=4"
      alt="SourceForge.net Logo"></a>
  </div>
</div>

<div id="content">
  <h1>Download CoppeTeX</h1>
"""

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

print """
  <p>

  The CoppeTeX project was conceived in the hope that it will be useful for
  you.  We will be grateful if you acknowledge the CoppeTeX project in your
  publications. To do so, you should use the <code style="display:
  inline;">\CoppeTeX</code> macro, which is already defined in the file
  coppe.cls.

  </p>

  <p>

  Don't forget that you must read and comply with the
  <a href="http://www.gnu.org/licenses/gpl-3.0.txt">
  license terms</a>.

  </p>

  <h2>Latest stable release</h2>

  <p>The latest stable release can be downloaded from below. For a ready-to-use
  template, go to the <a href="doc.html">Documentation page</a>.</p>

  <table class="downloads-list">
    <thead>
    <tr class="downloads-header">
      <th>filename</th>
      <th>size (bytes)</th>
      <th>date</th>
    </tr>
    </thead>
    <tbody>
    <tr class="downloads-item">
      <td class="downloads-filename"><a href="http://downloads.sourceforge.net/coppetex/coppetex-2.0.2.tar.gz?use_mirror=">coppetex-2.0.2.tar.gz</a></td>
      <td class="downloads-size">330782</td>
      <td class="downloads-date">06/15/2009</td>
    </tr>
    <tr class="downloads-item">
      <td class="downloads-filename"><a href="http://downloads.sourceforge.net/coppetex/coppetex-2.0.2.zip?use_mirror=">coppetex-2.0.2.zip</a></td>
      <td class="downloads-size">331024</td>
      <td class="downloads-date">06/15/2009</td>
    </tr>
    </tbody>
  </table>

  <p>After downloading, decompress and install it into a TEXMF tree of your
  preference. More details about installation can be found at the
  <a href="/install.html">install page</a>.</p>

  <p>If you are interested in older versions of CoppeTeX, please
  visit the <a href="http://sourceforge.net/project/showfiles.php?group_id=199659">releases archive</a> at Sourceforge.net. </p>

  <h2>Sources</h2>
  <p>
  The most up-to-date source files can be checked out from our
  SVN repository with the following command:
  </p>
  <code>
    svn co https://coppetex.svn.sourceforge.net/svnroot/coppetex/trunk coppetex
  </code>

  <p>The sources of a specific branch can be retrieved by typing:</p>
  <code>
    svn co https://coppetex.svn.sourceforge.net/svnroot/coppetex/branches/coppetex-M.N
    coppetex-M.N
  </code>
  <p>

  where M.N is any valid version number, for example 1.0.

  </p>

  <p>

  If you don't have any SVN client available, you can get one <a
  href="http://subversion.tigris.org/getting.html">here</a>.  If you
  still don't know what SVN is, you can download the sources snapshot of the
  current release from below:

  </p>

  <table class="downloads-list">
    <thead>
    <tr class="downloads-header">
      <th>filename</th>
      <th>size (bytes)</th>
      <th>date</th>
    </tr>
    </thead>
    <tbody>
    <tr class="downloads-item">
      <td class="downloads-filename"><a href="http://downloads.sourceforge.net/coppetex/coppetex-2.0.2-src.tar.gz?use_mirror=">coppetex-2.0.2-src.tar.gz</a></td>
      <td class="downloads-size">101583</td>
      <td class="downloads-date">06/15/2009</td>
    </tr>
    <tr class="downloads-item">
      <td class="downloads-filename"><a href="http://downloads.sourceforge.net/coppetex/coppetex-2.0.2-src.zip?use_mirror=">coppetex-2.0.2-src.zip</a></td>
      <td class="downloads-size">103726</td>
      <td class="downloads-date">06/15/2009</td>
    </tr>
    </tbody>
  </table>

  <p>
  
  We would like to emphasize that these files may not contain the most
  up-to-date code. The only guaranteed way of getting the latest sources is by
  checking out the trunk directory of the SVN repository as explained above.
  For older snapshots, go to the <a
  href="http://sourceforge.net/project/showfiles.php?group_id=199659">download
  archives</a>.
  
  </p>

  <p>
  
  Instructions on how to install CoppeTeX from sources are given at the <a
  href="/install.html">install page</a>. See the <a
  href="/doc.html">documentation page</a> for details about the implementation.
  
  </p>

</div>

<div id="footer">
<!-- SVN control tags -->
<p>
<script type="text/javascript">
  last_modified(String("$LastChangedDate: 2009-03-05 23:01:35 -0300 (Thu, 05 Mar 2009) $"),
                String("$LastChangedBy: helano $"));
  copyright_info();
</script>
</p>
<!-- Validators -->
<a href="http://validator.w3.org/check?uri=referer">
<img src="/images/valid-html401-blue.png" alt="Valid HTML 4.01 Strict"></a>

<a href="http://jigsaw.w3.org/css-validator/validator?uri=http://coppetex.sourceforge.net"><img src="/images/valid-css-blue.png" alt="Valid CSS"></a>
</div>

<script type="text/javascript">
var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
</script>
<script type="text/javascript">
try {
var pageTracker = _gat._getTracker("UA-7087383-1");
pageTracker._trackPageview();
} catch(err) {}</script>

</body>
</html>
"""
