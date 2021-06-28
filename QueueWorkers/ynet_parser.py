from bs4 import BeautifulSoup
from basic_worker import BasicWorker


class YnetWorker(BasicWorker):
    def __init__(self, url):
        super().__init__(url)

    def parse(self):
        soup = BeautifulSoup(self.page_html, "html.parser")
        texts = []
        texts_span = soup.find_all("span", {"data-text": "true"})
        for span in texts_span:
            texts.append(span.getText())
        texts.pop(-1)
        full_text = ''.join(texts)
        return full_text


worker = YnetWorker("https://www.ynet.co.il/news/article/HJ9PLxXnu#autoplay")
print(worker.parse())
