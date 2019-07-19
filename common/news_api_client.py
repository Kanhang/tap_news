import requests

from json import loads

NEWS_API_KEY = "be8f09c8fcb74f74a1d84ac73075f8ec"
NEWS_API_ENDPOINT = "https://newsapi.org/v1/"
ARTICALES_API = "articles"

BBC = 'bbc'
CNN = 'cnn'
DEFAULT_SOURCES = [CNN]

SORT_BY_TOP = 'top'
# url = https://newsapi.org/v1/articles
def build_url(end_point=NEWS_API_ENDPOINT, api_name=ARTICALES_API):
    '''build url to scrape news '''
    return end_point + api_name

def get_news_from_source(sources = [DEFAULT_SOURCES], sortBy = SORT_BY_TOP):
    ''' scrape news using news-api '''
    articles = []
    for source in sources:
    #request has apikey,source, sortby
        payload = {
            'apiKey': NEWS_API_KEY,
            'source': source,
            'sortBy': sortBy}
            
        response = requests.get(build_url(), params=payload)
        res_json = loads(response.content)

        # 
        if (res_json is not None and 
            res_json['status'] == 'ok' and 
            res_json['source'] is not None):
            #
            for news in res_json['articles']:
                news['source'] = res_json['source']

            articles.extend(res_json['articles'])
    return articles
#this is to get news from news api