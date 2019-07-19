import datetime
import hashlib
import redis
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__),'..','common'))

import news_api_client
from cloudAMQP_client import CloudAMQPClient 

SLEEP_TIME_IN_SECONDS = 10
NEWS_TIME_OUT_IN_SECONDS = 3600 * 24 * 3

REDIS_HOST = 'localhost'
REDIS_PORT = 6379


SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://ujwutzyt:3eZ-8aWIL_jV_C-pNmFAC_FQ4NALTi1S@lion.rmq.cloudamqp.com/ujwutzyt"
SCRAPE_NEWS_TASK_QUEUE_NAME = "tap-news-scrape-news-task-queue"

NEWS_SOURCES = [
    'bbc-news',
    'bbc-sport',
    'bloomberg',
    'cnn',
    'entertainment-weekly',
    'espn',
    'ign',
    'techcrunch',
    'the-new-york-times',
    'the-wall-street-journal',
    'the-washington-post'
]

redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PORT)
cloudAMQP_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)
# this file is to monitor the news. using news api to get updated news title. if there is a new news, increment the num in redis message queue. the redis expired if 3 days passed. because u cannot get all the information at one time because it is too much ,so only get the title, and trying get rid off the repetitive news by matching the title
while True:
    news_list = news_api_client.get_news_from_source(NEWS_SOURCES)
    num_of_news_news = 0
    print(news_list)

    for news in news_list:
        #hashlib.md5 is to convert the string to byte sequence, in order to prevent the repetitio
        news_digest = hashlib.md5(news['title'].encode('utf-8')).digest().encode('base64')
        #reconstruct the encoding from utf-8 to base64

        if redis_client.get(news_digest) is None:
            num_of_news_news = num_of_news_news + 1
            news['digest'] = news_digest

            if news['publishedAt'] is None:
                news['publishedAt'] = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

            redis_client.set(news_digest, "True")
            redis_client.expire(news_digest, NEWS_TIME_OUT_IN_SECONDS)

            cloudAMQP_client.sendMessage(news)

    print "Fetched %d news." % num_of_news_news

    cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)
