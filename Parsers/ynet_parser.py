from bs4 import BeautifulSoup
from .basic_worker import BasicParser


class YnetParser(BasicParser):
    def __init__(self, url):
        super().__init__(url)

    def parse(self):
        soup = BeautifulSoup(self.page_html, "html.parser")
        texts = []
        texts_span = soup.find_all("span", {"data-text": "true"})
        for span in texts_span:
            texts.append(span.getText())
        full_text = ''.join(texts)
        full_text = self.remove_punctuation(full_text)
        return full_text
