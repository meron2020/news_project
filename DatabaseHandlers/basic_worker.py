import requests
from bs4 import BeautifulSoup
import pika


class BasicWorker:
    def __init__(self, url):
        self.url = url

    def download_link(self):
        r = requests.get(self.url)
        return r.text