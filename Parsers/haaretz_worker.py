from bs4 import BeautifulSoup
from basic_worker import BasicWorker


class HaaretzWorker(BasicWorker):
    def __init__(self, url):
        super(HaaretzWorker, self).__init__(url)

    def parse(self):
        soup = BeautifulSoup(self.page_html, 'html.parser')
        full_text = ""
        texts_div = soup.find(attrs={"data-test": "articleBody"}).findChildren("p")
        for text_div in texts_div:
            full_text += text_div.get_text()
        print(full_text)
        return full_text


worker = HaaretzWorker('https://www.haaretz.co.il//news/law/netanyahutrial/.premium-1.9936262')
worker.parse()
