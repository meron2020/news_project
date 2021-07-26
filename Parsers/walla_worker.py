from bs4 import BeautifulSoup
from .basic_worker import BasicParser


class WallaParser(BasicParser):
    def __init__(self, url):
        super(WallaParser, self).__init__(url)

    def parse(self):
        soup = BeautifulSoup(self.page_html, "html.parser")
        text_div = soup.find("section", {"class": "article-content"})
        return text_div.get_text()

    def topic_parse(self):
        soup = BeautifulSoup(self.page_html, "html.parser")
        nav_ul = soup.find("article", {"class": "common-item"}).find("nav").find("ul")
        if nav_ul.find_all("li")[-2].a['title'] == "חדשות בעולם":
            topic = 'חדשות בעולם'
            return topic
        topic = nav_ul.find_all("li")[-1].a['title']
        if topic == 'קורונה':
            topic = "חינוך ובריאות"
        elif topic == 'פוליטי-מדיני':
            topic = 'מדיני'
        elif topic == 'יחסי חוץ':
            topic = 'מדיני'
        elif topic == 'חדשות פלילים ומשפט':
            topic = 'משפט ופלילים'
        elif topic == 'אירועים בארץ':
            topic = 'כללי'
        return topic



