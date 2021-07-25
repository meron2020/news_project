import requests
from bs4 import BeautifulSoup
from .basic_crawler import BasicCrawler


class WallaCrawler(BasicCrawler):
    def __init__(self):
        super(WallaCrawler, self).__init__("https://news.walla.co.il/")
        self.root_links = ["https://news.walla.co.il/category/12837",
                           "https://news.walla.co.il/category/2689",
                           "https://news.walla.co.il/category/1",
                           "https://news.walla.co.il/category/2686",
                           "https://news.walla.co.il/category/2"]

        self.news_links = []

    def find_all_links(self):
        # for link in self.root_links:
        html = requests.get("https://news.walla.co.il/").text
        soup = BeautifulSoup(html, 'html.parser')
        events_divs = soup.body.find_all("div", {"class": 'events'})
        all_links = []
        events_divs.pop(2)
        events_divs.pop(-1)
        events_divs.pop(-2)
        for div in events_divs:
            for link in div.find_all("a"):
                all_links.append([link['href']])

        return all_links
