from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pika


class BasicWorker:
    def __init__(self, url):
        self.url = url

    def download_link(self):
        base_url = Request(self.url)
        page = urlopen(base_url)
        page_html = page.read().decode('utf-8')
        return page_html
