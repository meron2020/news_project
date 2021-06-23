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
    def urllib_get_link(cls, url):
        base_url = Request(url, headers={
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'}
                           )
        page = urlopen(base_url)
        page_html = page.read().decode('utf-8')
        return page_html

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
