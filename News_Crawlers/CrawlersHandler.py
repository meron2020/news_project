from .ynet_crawler import YnetCrawler
from .maariv_crawler import MaarivCrawler
from .N12_crawler import N12Crawler
from .israel_hayom_crawler import IsraelHayomCrawler
import pika
import json


class CrawlersHandler:
    def __init__(self):
        connection_parameter = 'localhost'
        self.ynet_crawler = YnetCrawler()
        self.maariv_crawler = MaarivCrawler()
        self.n12_crawler = N12Crawler()
        self.israelhayom_crawler = IsraelHayomCrawler()
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=connection_parameter)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue="url_queue", durable=True)
        self.news_links = []
        self.crawlLinks()

    def crawlLinks(self):
        self.find_all_news_links()
        self.send_links_to_queue()

        self.connection.close()
        # self.send_one_link_to_queue()
        print("We have " + str(len(self.news_links)) + " articles")

    def send_links_to_queue(self):
        for link in self.news_links:
            link = json.dumps(link)
            self.channel.basic_publish(
                exchange='',
                routing_key='url_queue',
                body=link
            )
            print(" [x] Sent {} to queue".format(link))

    def send_one_link_to_queue(self):
        for i in range(10):
            routing_key = "routing_" + str(i % 4)
            link = json.dumps(self.news_links[i])
            self.channel.basic_publish(
                exchange='',
                routing_key='url_queue',
                body=link
            )
            print(" [x] Sent {} to queue".format(self.news_links[i]))

        self.connection.close()

    def find_all_news_links(self):
        ynet_links = self.ynet_crawler.find_all_news_links()
        self.news_links.extend(ynet_links)
        maariv_links = self.maariv_crawler.return_news_links()
        self.news_links.extend(maariv_links)
        n12_links = self.n12_crawler.find_news_links()
        self.news_links.extend(n12_links)
        israel_hayom_links = self.israelhayom_crawler.parse_and_download()
        self.news_links.extend(israel_hayom_links)


# handler = CrawlersHandler()
# handler.crawlLinks()
