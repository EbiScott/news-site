import feedparser
from flask import Flask, render_template, request


app = Flask(__name__)

RSS_FEEDS = {
             'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition_world.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640',
             'nbc': 'https://www.nbcnews.com/id/3032091/device/rss/rss.xml',
             'cnbc': 'https://www.cnbc.com/id/100727362/device/rss/rss.html',
             'abc': 'http://abcnews.go.com/abcnews/internationalheadlines',
             'aljazeera': 'http://www.aljazeera.com/xml/rss/all.xml',
             'cbs': 'https://www.cbsnews.com/latest/rss/world'
            }

@app.route("/")
def get_news():
    query = request.args.get(publication)
    if not query or query.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:
        publication = query.lower()    
    feed = feedparser.parse(RSS_FEEDS[publication])

    return render_template('home.html', articles=feed['entries'])

if __name__ == "__main__":
    app.run(debug=True)


