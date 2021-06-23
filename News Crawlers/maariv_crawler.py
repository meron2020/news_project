from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from basic_crawler import BasicCrawler


class MaarivCrawler(BasicCrawler):
    def __init__(self):
        super(MaarivCrawler, self).__init__("https://www.maariv.co.il/news")
        self.root_links = ["https://www.maariv.co.il/news/politics",
                           "https://www.maariv.co.il/news/israel",
                           "https://www.maariv.co.il/news/military",
                           "https://www.maariv.co.il/news/world",
                           "https://www.maariv.co.il/news/health",
                           "https://www.maariv.co.il/news/law"]
        self.send_links_to_queue(self.root_links)


