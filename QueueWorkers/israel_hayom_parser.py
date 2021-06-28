from bs4 import BeautifulSoup
from basic_worker import BasicWorker


class IsraelHayomWorker(BasicWorker):
    def __init__(self, url):
        super(IsraelHayomWorker, self).__init__(url)

    def parse(self):
        soup = BeautifulSoup(self.page_html, "html.parser")
        text_div = soup.find("div", {"class": "text-content"})
        return text_div.text


worker = IsraelHayomWorker("https://www.israelhayom.co.il/news/geopolitics/article/2564010/")
print(worker.parse())