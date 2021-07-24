import requests
from bs4 import BeautifulSoup
from basic_crawler import BasicCrawler


class YnetCrawler(BasicCrawler):
    def __init__(self):
        super(YnetCrawler, self).__init__("https://www.ynet.co.il/news")
        self.root_links_dict = {'https://www.ynet.co.il/news/category/344': 'צבא וביטחון',
                                'https://www.ynet.co.il/news/category/315': 'מדיני',
                                'https://www.ynet.co.il/news/category/317': 'המערכת הפוליטית',
                                'https://www.ynet.co.il/news/category/4172': 'פלסטינים',
                                'https://www.ynet.co.il/news/category/188': 'כללי',
                                'https://www.ynet.co.il/news/category/190': 'משפט ופלילים',
                                'https://www.ynet.co.il/news/category/191': 'חינוך ובריאות',
                                'https://www.ynet.co.il/news/category/192': 'חדשות בעולם'}
        self.news_links = []
        self.check_if_links_change(self.find_news_category)
        self.find_links_in_category_pages()

    def find_links_in_category_pages(self):
        category_lists = ["https://www.ynet.co.il/news/category/185",
                          "https://www.ynet.co.il/news/category/187"]
        for link in category_lists:
            html = self.get_link(link)
            soup = BeautifulSoup(html, "html.parser")
            article_tabs_div = soup.find_all("div", {"class": "MultiArticleComponenta ArticleHeadlinesAuto"})
            all_page_links = []
            for div in article_tabs_div:
                slots = div.find("div", {"class": "slotsContent"})
                div_links = slots.find_all("a")
                for link in div_links:
                    if "article" in link['href']:
                        all_page_links.append(link['href'])

            all_page_links = list(dict.fromkeys(all_page_links))
            for link in all_page_links:
                print(link)

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
        for link in self.root_links_dict.keys():
            html = requests.get(link).text
            soup = BeautifulSoup(html, 'html.parser')
            slot_title_divs = soup.find_all("div", {"class": "slotView"})
            for news_link_div in slot_title_divs:
                news_span = news_link_div.span
                try:
                    news_link = [news_span.a['href'], self.root_links_dict[link]]
                    self.news_links.append(news_link)
                except Exception:
                    pass

        # print(self.news_links)
        # print(len(self.news_links))
        return self.news_links


YnetCrawler()
