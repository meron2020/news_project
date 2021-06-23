from bs4 import BeautifulSoup
from basic_worker import BasicWorker


class MaarivWorker(BasicWorker):
    def __init__(self, url):
        super(MaarivWorker, self).__init__(url)
        self.page_html = self.download_link()

    def parse(self):
        soup = BeautifulSoup(self.page_html, "html.parser")
        texts = []
        full_text = ""
        texts_div = soup.find_all("div", {"class": "article-body"})
        for text_p in texts_div:
            texts.append(text_p.find_all('p'))

        for text in texts[0]:
            full_text += text.get_text()


        print(full_text)



worker = MaarivWorker("https://www.maariv.co.il/news/politics/Article-848853")
worker.parse()

