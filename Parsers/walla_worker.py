from bs4 import BeautifulSoup
from basic_worker import BasicParser


class WallaParser(BasicParser):
    def __init__(self, url):
        super(WallaParser, self).__init__(url)

    def parse(self):
        soup = BeautifulSoup(self.page_html, "html.parser")
        nav_ul = soup.find("article", {"class": "common-item"}).find("nav").find("ul")
        topic = nav_ul.find_all("li")[-1].a['title']
        text_div = soup.find("section", {"class": "article-content"})
        return [text_div.get_text, topic]



