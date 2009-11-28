google.load("feeds", "1");

function NewsPreview(container) {
  this.container_ = container;
}

NewsPreview.prototype.show = function(url, opt_noTitle) {
  $("#loadingnews").show();
  var feed = new google.feeds.Feed(url);
  var preview = this;
  feed.load(function(result) {
    preview.render_(result, opt_noTitle);
  });
}

NewsPreview.prototype.render_ = function(result, opt_noTitle) {
  if (!result.feed || !result.feed.entries) return;
  while (this.container_.firstChild) {
    this.container_.removeChild(this.container_.firstChild);
  }

  var news = this.createDiv_(this.container_, "news");

  if ( $("#loadingnews").is(":visible") ) {
    $("#loadingnews").hide();
  }

  for (var i = 0; i < 3; i++) {
    var entry = result.feed.entries[i];
    var div = this.createDiv_(news, "news-entry");
    var linkDiv = this.createDiv_(div, "news-title");
    this.createLink_(linkDiv, entry.link, entry.title);
    if (entry.author) {
      var author = new String(entry.author);
      var start = author.indexOf("(") + 1;
      var end = author.indexOf(")");
      var when = new Date(result.feed.entries[i].publishedDate);
      this.createDiv_(div, "news-author", "Posted by " + author.substring(start, end) + " in " + 
      when.getMonth() + "/" + when.getDate() + "/" + when.getFullYear());
    }

    this.createDiv_(div, "news-body", entry.contentSnippet);
  }
}

NewsPreview.prototype.createDiv_ = function(parent, className, opt_text) {
  return this.createElement_("div", parent, className, opt_text);
}

NewsPreview.prototype.createLink_ = function(parent, href, text) {
  var link = this.createElement_("a", parent, "", text);
  link.href = href;
  return link;
}

NewsPreview.prototype.createElement_ = function(tagName, parent, className,
                                                opt_text) {
  var div = document.createElement(tagName);
  div.className = className;
  parent.appendChild(div);
  if (opt_text) {
    div.appendChild(document.createTextNode(opt_text));
  }
  return div;
}

function initNews() {
//  var url = "https://sourceforge.net/api/news/index/project-id/199659/rss";
  var url = "https://sourceforge.net/export/rss2_projnews.php?group_id=199659";
  var news = new NewsPreview(document.getElementById("news"));
  news.show(url);
}

google.setOnLoadCallback(initNews);
