function last_modified(lastchanged, lastauthor)
{
  lastchanged = lastchanged.replace(/.*\(/, "").replace(/\).*/, "");
  lastauthor = lastauthor.replace(/.*:\s/g, "").replace(/\s*.\$/, "");
  lastauthor = lastauthor[0].toUpperCase() + lastauthor.substr(1);
  document.write("Last modified on " + lastchanged + " by " + lastauthor);
}

function copyright_info()
{
  var copyright = new Date();
  document.write("<br>&copy; " + copyright.getFullYear() + " CoppeTeX Project");
}
