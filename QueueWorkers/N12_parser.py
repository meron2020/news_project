from bs4 import BeautifulSoup
from basic_worker import BasicWorker


class N12Worker(BasicWorker):
    def __init__(self, url):
        super(N12Worker, self).__init__(url)

    def parse(self):
        soup = BeautifulSoup(self.page_html, "html.parser")
        full_text = ""
        text_divs = soup.find_all("p")
        text_divs.pop()
        for text_div in text_divs:
            full_text += text_div.get_text()
        return full_text


worker = N12Worker(
    "https://www.mako.co.il/news-politics/2021_q2/Article-7eeef050d1d3a71026.htm?partner=lobby")
print(worker.parse())
