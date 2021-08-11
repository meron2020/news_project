from News_Crawlers.CrawlersHandler import CrawlersHandler


class TestingUrlsSender:
    @classmethod
    def send_urls(cls):
        urls = [
            "https://www.ynet.co.il/news/article/byeya7xxy#autoplay",
            "https://www.ynet.co.il/news/article/r1dfhexlf#autoplay",
            "https://www.ynet.co.il/news/article/bkjuhtjgk#autoplay",
            "https://www.ynet.co.il/news/article/hyp006ojly",
            "https://www.ynet.co.il/news/article/s1yxnocjf#autoplay",
            "https://www.ynet.co.il/news/article/h1ji87lgf#autoplay",
            "https://www.ynet.co.il/news/article/s1zojl1xy",
            "https://news.walla.co.il/item/3453301",
            "https://news.walla.co.il/item/3453248",
            "https://news.walla.co.il/break/3453484",
            "https://www.maariv.co.il/news/military/Article-858557",
            "https://www.maariv.co.il/news/military/Article-858551",
            "https://www.maariv.co.il/news/world/Article-858553",
            "https://www.mako.co.il/news-military/2021_q3/Article-d8b08da5d8e2b71026.htm?partner=lobby",
            "https://www.mako.co.il/news-military/2021_q3/Article-68a72e5a92b1b71027.htm",
            "https://www.n12.co.il/news-lifestyle/2021_q3/Article-3fece949d703b71026.htm?sCh=31750a2610f26110&pId=173113802",
            "https://www.mako.co.il/news-politics/2021_q3/Article-a3a1416948c2b71027.htm?partner=lobby"
        ]

        handler = CrawlersHandler()
        handler.send_test_urls_to_queue(urls)
