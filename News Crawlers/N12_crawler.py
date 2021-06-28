from bs4 import BeautifulSoup
import requests
from basic_crawler import BasicCrawler


class N12Crawler(BasicCrawler):
    def __init__(self, connection_parameter):
        super(N12Crawler, self).__init__("https://www.n12.co.il/?partner=Newsheaderlogo")
        self.root_links = ["https://www.mako.co.il/news-military?partner=NewsNavBar",
                           "https://www.mako.co.il/news-politics?partner=NewsNavBar",
                           "https://www.mako.co.il/news-law?partner=NewsNavBar",
                           "https://www.mako.co.il/news-israel?partner=NewsNavBar"]
        self.news_links = []
        self.soup = BeautifulSoup(self.page_html, "html.parser")

    def find_news_links(self):
        for link in self.root_links:
            html = requests.get(link).text
            soup = BeautifulSoup(html, 'html.parser')
            figure_tags = soup.find_all("figure")
            for tag in figure_tags:
                try:
                    link = tag.a['href']
                    news_link = "https://www.mako.co.il" + link
                    self.news_links.append(news_link)
                except Exception:
                    pass

        return self.news_links

