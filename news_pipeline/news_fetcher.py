import os
import sys

from newspaper import Article

# import common package in parent directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers'))

import cnn_news_scraper
from cloudAMQP_client import CloudAMQPClient

DEDUPE_NEWS_TASK_QUEUE_URL = "amqp://odznjasr:Umk_yuHytcjpLELx5v9wSN2JOf_Z9f3Q@lion.rmq.cloudamqp.com/odznjasr"
DEDUPE_NEWS_TASK_QUEUE_NAME = "tap-news-dedupe-news-task-queue"

SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://ujwutzyt:3eZ-8aWIL_jV_C-pNmFAC_FQ4NALTi1S@lion.rmq.cloudamqp.com/ujwutzyt"
SCRAPE_NEWS_TASK_QUEUE_NAME = "tap-news-scrape-news-task-queue"

SLEEP_TIME_IN_SECONDS = 5

dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)
#this q is to scape the news from web pages.
# task is the response from news api it has url, publishat, author, title,descrption , url ,url to image,
# so as long as we get the news response, we can get a url.

def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        print 'message is broken'
        return

    task = msg
    text = None

    article = Article(task['url'])
    article.download()
    article.parse()

    task['text'] = article.text.encode('utf-8')

    dedupe_news_queue_client.sendMessage(task)

while True:
    if scrape_news_queue_client is not None:
        msg = scrape_news_queue_client.getMessage()
        if msg is not None:
            try:
                handle_message(msg)
            except Exception as e:
                print # coding=utf-8
                pass
        scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)
