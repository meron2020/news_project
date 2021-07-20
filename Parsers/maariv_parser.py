from bs4 import BeautifulSoup
from .basic_worker import BasicWorker


class MaarivWorker(BasicWorker):
    def __init__(self, url):
        super(MaarivWorker, self).__init__(url)

    def parse(self):
        soup = BeautifulSoup(self.page_html, "html.parser")
        texts = []
        full_text = ""
        texts_div = soup.find_all("div", {"class": "article-body"})
        for text_p in texts_div:
            texts.append(text_p.find_all('p'))

        for text in texts[0]:
            full_text += text.get_text()

        full_text_list = full_text.split()
        for text in full_text_list:
            text = text[::-1]
        full_text = ' '.join(full_text_list)

        return full_text