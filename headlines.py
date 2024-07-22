from dotenv import load_dotenv
import feedparser
from flask import Flask, render_template, request
import json
import random
import urllib
import urllib3


load_dotenv()

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


WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}"

# def get_weather(query):
#     API_KEY = 'OPENWEATHER_API'
#     query = urllib.quote(query)
#     url = api_url.format(query)
#     data = urllib2.urlopen(url).read()
#     parsed = json.loads(data)
#     weather = None
#     if parsed.get("weather"):
#         weather = {"description":parsed["weather"][0]["description"], "temperature":parsed["main"]["temp"], "city":parsed["name"]}

DEFAULTS = {'publication': 'bbc', 'city': 'Lagos,NG'}


@app.route("/")
def home():
    publication = request.args.get('publication')
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)

    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
    return render_template("home.html", articles=articles, weather=weather)

def get_news(publication):
    # query = request.args.get(publication)
    # if not query or query.lower() not in RSS_FEEDS:
    #     publication = DEFAULTS["publication"]
    # else:
    #     publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']

def get_weather(query):
    API_KEY = "OPENWEATHER_API"
    query = urllib.parse.quote(query)
    url = WEATHER_URL.format(query, API_KEY)
    http = urllib3.PoolManager()
    
    response = http.request('GET', url)
    if response.status == 200:
        data = json.loads(response.data)
        if data.get('weather'):
            weather = {'description': data['weather'][0]['description'], 'temperature': data['main']['temp'], 'city': data['name']}
            return weather
    return None 

if __name__ == "__main__":
    app.run(debug=True)


