<?php
$author = $_GET['author'];
$title = $_GET['title'];
$school = $_GET['school'];
$dept = $_GET['dept'];
$year = date("Y");
$degree = $_GET['degree'];

$label = str_replace(" ", "", $author) . "_" . $degree . $year;

if (strcasecmp($degree,"msc"))
  $doctype = "mastersthesis";
if (strcasecmp($degree,"dsc"))
  $doctype = "phdthesis";

if (!defined('PHP_EOL')) {
  switch (strtoupper(substr(PHP_OS, 0, 3))) {
    // Windows
    case 'WIN':
      define('PHP_EOL', "\r\n");
      break;
    // Mac
    case 'DAR':
      define('PHP_EOL', "\r");
      break;
    // Unix
    default:
      define('PHP_EOL', "\n");
  }
}

$Handle = fopen("../persistent/data/coppetex.bib", 'a') or die("can't open file");
fwrite($Handle, "@" . $doctype . "{ ". $label . "," . PHP_EOL);
fwrite($Handle, "  author = {" . $author . "}," . PHP_EOL);
fwrite($Handle, "  title = {" . $title . "}," . PHP_EOL);
fwrite($Handle, "  school = {" . $school . "}," . PHP_EOL);
fwrite($Handle, "  department = {" . $dept . "}," . PHP_EOL);
fwrite($Handle, "  year = {" . $year . "}," . PHP_EOL);
fwrite($Handle, "}" . PHP_EOL);
fclose($Handle);
?>
