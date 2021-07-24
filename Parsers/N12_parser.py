from bs4 import BeautifulSoup
from .basic_worker import BasicParser


class N12Parser(BasicParser):
    def __init__(self, url):
        super(N12Parser, self).__init__(url)

    def parse(self):
        soup = BeautifulSoup(self.page_html, "html.parser")
        full_text = ""
        text_divs = soup.find_all("p")
        text_divs.pop()
        for text_div in text_divs:
            full_text += text_div.get_text()
        return full_text


