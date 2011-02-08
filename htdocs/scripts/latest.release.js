google.load("feeds", "1");
var version = "2.2";

function showReleases(url) {
  $("#loadingpackages").show()
  $("#loadingsources").show()
  var feed = new google.feeds.Feed(url);
  feed.setResultFormat(google.feeds.Feed.XML_FORMAT);
  feed.setNumEntries(-1);
  feed.load(function(result) {
    renderReleases(result);
  });
}

function renderReleases(result) {
  if (!result) return;

  var radical = new String("coppetex-");
  var items = $(result.xmlDocument).find("item");
  var i = items.length - 8;
  // render links at the corresponding table
  $(items).slice(i).each(function() {
    var title = new String($(this).find("title").text());

    // get archive name
    var start = title.indexOf(radical + version);
    var archive = title.substring(start);

    // determine the type of data, dist, sources, or template
    start = title.indexOf(radical + version) + radical.length + version.length;
    var end = title.indexOf(".", start);
    var opt = title.substring(start, end);

    // determine table name
    var table;
    if (opt == '') {
      table = "packages";
      if ( $("#loadingpackages").is(":visible") ) {
        $("#loadingpackages").hide();
      }
    } else if (opt == '-src') {
      table = "sources";
      if ( $("#loadingsources").is(":visible") ) {
        $("#loadingsources").hide();
      }
    } else {
      return;
    }

    // get details about the file
    var url = $(this).find("link").text();
    var size = $(this).find("media\\:content").attr("filesize");
    var pubdate = new Date( $(this).find("pubDate").text() );

    // append row to 'table'
    $("table[id='" + table + "']").append('<tr class="downloads-item">' +
        "<td class='downloads-filename'><a href='" + url + "'>" + archive + "</a></td>" +
        "<td class='downloads-size'>" + size + "</td>" +
        "<td class='downloads-date'>" + pubdate.getMonth() + "/" + pubdate.getDate() + "/" + pubdate.getFullYear() + "</td></tr>");
  });
}

function initRelease() {
  var url = "https://sourceforge.net/api/file/index/project-id/199659/rss";
  showReleases(url);
}

google.setOnLoadCallback(initRelease);
