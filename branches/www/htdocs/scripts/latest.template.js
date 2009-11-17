google.load("feeds", "1");

function showTemplates(url, opt_noTitle) {
  var feed = new google.feeds.Feed(url);
  feed.load(function(result) {
    renderTemplates(result, opt_noTitle);
  });
}

function renderTemplates(result, opt_noTitle) {
  if (!result.feed || !result.feed.entries) return;

  // these two correspond to the sources snapshot and pure release
  var baseurl = "https://sourceforge.net/projects/coppetex/files/CoppeTeX";
  var extensions = new Array(".tar.gz", ".zip");
  for (var i = 0; i < 2; i++) {
    var entry = result.feed.entries[i];
    var title = new String(entry.title);
    var content = new String(entry.content);
    var exp = /\d+\.\d+(\.\d+)?/g;
    var version = title.match(exp);
    exp = / Sources Snapshot/gi;
    var type = title.match(exp);
    var when = new Date(result.feed.entries[i].publishedDate);
    var archive = 'coppetex-' + version + '-template';
    var table = "templates";
    if (type != null) {
      continue;
    }
    $(extensions).each(function() {
    var start = content.indexOf(archive + this + " (") + archive.length + this.length + 2;
    var end = content.indexOf(" bytes", start);
    var size = content.substring(start,end);

    $("table[name='" + table + "']").append('<tr class="downloads-item">' +
      "<td class='downloads-filename'><a href='" + baseurl + "/" + version + "/" + archive + this + "/download'>" + archive + this + "</a></td>" +
      "<td class='downloads-size'>" + size + "</td>" +
      "<td class='downloads-date'>" + when.getMonth() + "/" + when.getDate() + "/" + when.getFullYear() + "</td></tr>");
    });
  }
}

function initRelease() {
  var url = "https://sourceforge.net/export/rss2_projfiles.php?group_id=199659&rss_fulltext=1";
  showTemplates(url);
}

google.setOnLoadCallback(initRelease);
