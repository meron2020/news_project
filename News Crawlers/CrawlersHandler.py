from ynet_crawler import YnetCrawler
from maariv_crawler import MaarivCrawler
from N12_crawler import N12Crawler
from israel_hayom_crawler import IsraelHayomCrawler
import pika


class CrawlersHandler:
    def __init__(self):
        connection_parameter = 'localhost'
        self.ynet_crawler = YnetCrawler(connection_parameter)
        self.maariv_crawler = MaarivCrawler(connection_parameter)
        self.n12_crawler = N12Crawler(connection_parameter)
        self.israelhayom_crawler = IsraelHayomCrawler(connection_parameter)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=connection_parameter)
        )
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='urls', exchange_type='fanout')
        self.news_links = []
        self.find_all_news_links()
        self.send_links_to_queue()

    def send_links_to_queue(self):
        for link in self.news_links:
            self.channel.basic_publish(
                exchange='urls',
                routing_key='',
                body=link,
                properties=pika.BasicProperties(delivery_mode=2)
            )
            print(" [x] Sent {} to queue".format(link))

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


handler = CrawlersHandler()
