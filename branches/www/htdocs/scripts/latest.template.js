google.load("feeds", "1");
var version = "2.2.1";

function showTemplate(url) {
  $("#loadingtemplates").show()
  var feed = new google.feeds.Feed(url);
  feed.setResultFormat(google.feeds.Feed.XML_FORMAT);
  feed.setNumEntries(-1);
  feed.load(function(result) {
    renderTemplate(result);
  });
}

function renderTemplate(result) {
  if (!result) return;

  var radical = new String("coppetex-");
  var items = $(result.xmlDocument).find("item:lt(6)"); // get the first 6 items
  // render links at the corresponding table
  $(items).slice(0).each(function() {
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
    if (opt == '-template') {
      table = "templates";
      if ( $("#loadingtemplates").is(":visible") ) {
        $("#loadingtemplates").hide();
      }
    } else {
      return;
    }

    // get details about the file
    var url = $(this).find("link").text();
    var size = $(this).find("media\\:content").attr("filesize");
    var pubdate = new String( $(this).find("pubDate").text() );

    // append row to 'table'
    $("table[id='" + table + "']").append('<tr class="downloads-item">' +
        "<td class='downloads-filename'><a href='" + url + "'>" + archive + "</a></td>" +
        "<td class='downloads-size'>" + size + "</td>" +
        "<td class='downloads-date'>" + pubdate + "</td></tr>");
  });
}

function initTemplate() {
  var url = "https://sourceforge.net/api/file/index/project-id/199659/rss";
  showTemplate(url);
}

google.setOnLoadCallback(initTemplate);
