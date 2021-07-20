import requests
from bs4 import BeautifulSoup
from basic_crawler import BasicCrawler
from datetime import datetime


class WallaCrawler(BasicCrawler):
    def __init__(self):
        super(WallaCrawler, self).__init__("https://news.walla.co.il/")
        self.root_links = ["https://news.walla.co.il/category/12837",
                           "https://news.walla.co.il/category/2689",
                           "https://news.walla.co.il/category/1",
                           "https://news.walla.co.il/category/2686",
                           "https://news.walla.co.il/category/2"]

        self.news_links = []
        # self.find_current_news_links()
        # self.send_links_to_queue(self.news_links)

    # def find_current_news_links(self):
    #     for link in self.root_links:
    #         html = requests.get(link).text
    #         soup = BeautifulSoup(html, 'html.parser')
    #         current_news_links = soup.find("section", {"class": "category-content"}).ul
    #         for current_link in current_news_links:
    #             pub_date = current_link.div[{'class': 'pub-date'}]
    #             date_today = datetime.today().strftime('%Y-%m-%d')
    #             if date_today[-2:] == pub_date[:2]:
    #                 try:
    #                     news_link = current_link.a['href']
    #                     self.news_links.append(news_link)
    #                 except Exception:
    #                     pass

    def new_finding_method(self):
        # for link in self.root_links:
        html = requests.get("https://news.walla.co.il/category/2689").text
        soup = BeautifulSoup(html, 'html.parser')
        all_links = soup.body.find_all("a")
        for link in all_links:
            try:
                if 'item' in link['href']:
                    print(link['href'])
            except Exception:
                pass


crawler = WallaCrawler()
crawler.new_finding_method()
