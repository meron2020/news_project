import requests
from bs4 import BeautifulSoup
from basic_crawler import BasicCrawler


class YnetCrawler(BasicCrawler):
    def __init__(self):
        super(YnetCrawler, self).__init__("https://www.ynet.co.il/news")
        self.root_links = ['https://www.ynet.co.il/news/category/344',
                           'https://www.ynet.co.il/news/category/315',
                           'https://www.ynet.co.il/news/category/317',
                           'https://www.ynet.co.il/news/category/4172',
                           'https://www.ynet.co.il/news/category/4686',
                           'https://www.ynet.co.il/news/category/188',
                           'https://www.ynet.co.il/news/category/190',
                           'https://www.ynet.co.il/news/category/191',
                           'https://www.ynet.co.il/home/0,7340,L-35312,00.html',
                           'https://www.ynet.co.il/home/0,7340,L-11289,00.html',
                           'https://www.ynet.co.il/news/category/4502',
                           'https://www.ynet.co.il/news/category/13547',
                           'https://www.ynet.co.il/news/category/9500']
        self.news_links = []
        self.check_if_links_change(self.find_news_category)
        self.find_all_news_links()
        self.send_links_to_queue(self.news_links)

    @classmethod
    def find_navigation_div(cls, page_html):
        parser = BeautifulSoup(page_html, "html.parser")
        return parser.find_all("div", {"class": "categorySubNavigation"})

    def find_news_category(self):
        links = []
        div_tag = self.find_navigation_div(self.page_html)
        if len(div_tag) > 0:
            url_list = div_tag[0].ul
            for url in url_list.find_all('li'):
                page = self.get_link(url.a['href'])
                links_in_url = self.find_navigation_div(page)
                try:
                    links_in_url = links_in_url[0].ul
                    for link in links_in_url.find_all('li'):
                        links.append(link.a['href'])
                except Exception:
                    pass
        return links

    def find_all_news_links(self):
        for link in self.root_links:
            html = requests.get(link).text
            soup = BeautifulSoup(html, 'html.parser')
            slot_title_divs = soup.find_all("div", {"class": "slotView"})
            for news_link_div in slot_title_divs:
                news_span = news_link_div.span
                try:
                    news_link = news_span.a['href']
                    self.news_links.append(news_link)
                except Exception:
                    pass




crawler = YnetCrawler()
crawler.find_all_news_links()
