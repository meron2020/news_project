from bs4 import BeautifulSoup
from basic_crawler import BasicCrawler


class IsraelHayomCrawler(BasicCrawler):
    def __init__(self):
        super(IsraelHayomCrawler, self).__init__("https://www.israelhayom.co.il/news/")
        self.soup = BeautifulSoup(self.page_html, "html.parser")

    def parse_and_download(self):
        articles_div = self.soup.find_all("h2", {"class": "post-title"})
        article_links = []
        for article in articles_div:
            article_link = "https://www.israelhayom.co.il/" + article.a['href']
            article_links.append(article_link)

        print(article_links)


crawler = IsraelHayomCrawler()
crawler.parse_and_download()
