import os
import random
import requests

from lxml import html

GET_CNN_NEWS_XPATH = "//p[contains(@class, 'zn-body__paragraph')]//text() | //div[contains(@class, 'zn-body__paragraph')]//text()"

USER_AGENTS_FILE = os.path.join(os.path.dirname(__file__), 'user_agents.txt')
USER_AGENTS = []

with open(USER_AGENTS_FILE, 'r') as uaf:
    for ua in uaf.readlines():
        if ua:
            USER_AGENTS.append(ua.strip()[1:-1])# [1:-1] means get the string from second to last one (not include)
random.shuffle(USER_AGENTS)#shuffle function reorder the array in random order

def getHeader():
    ua = random.choice(USER_AGENTS)
    headers = {
        "Connection" : "close",
        "User-Agent" : ua
    }
    return headers

def extract_news(news_url):
    session_requests = requests.session()
    response = session_requests.get(news_url, headers=getHeader())
    news = {}

    try:
        tree = html.fromstring(response.content) #parsing html , take string return document_fromstring
        news = tree.xpath(GET_CNN_NEWS_XPATH)#XPath to query parts of an HTML structure. XPath is a way of identifying nodes and content in an XML document structure (including HTML). ...
        news = ''.join(news)
    except Exception:
        return {}

    return news
