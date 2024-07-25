import datetime
from dotenv import load_dotenv
import feedparser
from flask import Flask, render_template, request, make_response
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
CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=OPENEXCHANGE_API"

DEFAULTS = {'publication': 'bbc', 'city': 'London,UK', 'currency_from':'GBP', 'currency_to':'USD'}

def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)

    if request.cookies.get(key):
        return request.cookies.get(key)

    return DEFAULTS[key]

@app.route("/")
def home():
    publication = get_value_with_fallback("publication")
    articles = get_news(publication)

    city = get_value_with_fallback("city")
    weather = get_weather (city)

    currency_from = get_value_with_fallback("currency_from")
    currency_to = get_value_with_fallback("currency_to")
    rate, currencies = get_rate(currency_from, currency_to)

    response = make_response(render_template("home.html", articles=articles, weather=weather, currency_from=currency_from, currency_to=currency_to, rate=rate, currencies=sorted(currencies)))

    expires = datetime.datetime.now() + datetime.timedelta(days=365)

    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)

    return response


def get_news(publication):
    
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
            weather = {'description': data['weather'][0]['description'], 'temperature': data['main']['temp'], 'city': data['name'], 'country': data['sys']['country']}
            return weather
    return None 

def get_rate(frm, to):
    all_currency = urllib2.urlopen(CURRENCY_URL).read() #need to fix this urllib2 to urllib3 issue here

    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return (to_rate / frm_rate, parsed.keys())



if __name__ == "__main__":
    app.run(debug=True)


