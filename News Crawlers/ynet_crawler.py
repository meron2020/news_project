from urllib.request import urlopen, Request
from bs4 import BeautifulSoup


class YnetCrawler:
    def __init__(self):
        self.page_html = self.get_link("https://www.ynet.co.il/news")
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
        self.check_if_links_change()


    @classmethod
    def get_link(cls, url):
        base_url = Request(url)
        page = urlopen(base_url)
        page_html = page.read().decode('utf-8')
        return page_html

    @classmethod
    def find_navigation_div(cls, page_html):
        parser = BeautifulSoup(page_html, "html.parser")
        return parser.find_all("div", {"class": "categorySubNavigation"})

    def check_if_links_change(self):
        news_links = self.find_news_links()
        if not news_links == self.root_links:
            self.root_links = news_links

        else:
            pass

    def find_news_links(self):
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


crawler = YnetCrawler()
print(crawler.find_news_links())
