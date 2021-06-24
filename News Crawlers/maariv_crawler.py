from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from basic_crawler import BasicCrawler


class MaarivCrawler(BasicCrawler):
    def __init__(self):
        super(MaarivCrawler, self).__init__("https://www.maariv.co.il/news")
        self.news_links = []
        self.soup = BeautifulSoup(self.page_html, "html.parser")
        self.set_news_links()
        self.send_links_to_queue(self.news_links)

    def find_big_item_links(self):
        news_links = []
        big_items_list = self.soup.find_all("div", {"class": "category-five-articles-big-item"})
        for big_item in big_items_list:
            news_link = big_item.a['href']
            news_links.append(news_link)
        return news_links

    def find_small_item_links(self):
        news_links = []
        small_items_list = self.soup.find_all("div", {"class": "category-five-articles-small-item"})
        for small_item in small_items_list:
            news_link = small_item.a['href']
            news_links.append(news_link)
        return news_links

    def set_news_links(self):
        big_links = self.find_big_item_links()
        small_links = self.find_small_item_links()
        self.news_links.append(big_links)
        self.news_links.append(small_links)

        print(self.news_links)

crawler = MaarivCrawler()
crawler.set_news_links()
