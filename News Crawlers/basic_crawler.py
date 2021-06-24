from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import requests
import pika


class BasicCrawler:
    def __init__(self, url):
        self.root_links = []
        self.page_html = self.get_link(url)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost')
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='news urls', durable=True)

    @classmethod
    def get_link(cls, url):
        r = requests.get(url)
        return r.text

    def send_links_to_queue(self, url_links):
        for link in url_links:
            self.channel.basic_publish(
                exchange='',
                routing_key='news urls',
                body=link,
                properties=pika.BasicProperties(delivery_mode=2)
            )

    def check_if_links_change(self, find_news_links):
        news_links = find_news_links()
        if not news_links == self.root_links:
            self.root_links = news_links

        else:
            pass
