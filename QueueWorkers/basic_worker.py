import requests
from bs4 import BeautifulSoup
import pika


class BasicWorker:
    def __init__(self, url):
        self.url = url
        self.page_html = self.download_link()

    def download_link(self):
        r = requests.get(self.url)
        return r.text

    @classmethod
    def print_acknowledgement(cls, newspapaer):
        print("{} url received.".format(newspapaer))
