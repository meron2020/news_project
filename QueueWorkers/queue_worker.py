from Parsers.ynet_parser import YnetWorker
from Parsers.maariv_parser import MaarivWorker
from Parsers.N12_parser import N12Worker
from Parsers.israel_hayom_parser import IsraelHayomWorker
import pika
from DatabaseHandlers.database_publisher import DatabasePublisher
import json


class QueueWorker:
    def __init__(self):
        self.DB_queue_handler = DatabasePublisher()

        self.news_links = []
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()
        self.result = self.channel.queue_declare(queue='url_queue', durable=True)

    def callback(self, ch, method, properties, body):
        body = body.decode("utf-8")
        body = json.loads(body)
        if type(body) == int:
            self.DB_queue_handler.send_article_amount(body)
            return

        url, topic = body[0], body[1]
        try:
            if "ynet" in url:
                worker = YnetWorker(url)
                newspaper = "ynet"
            elif "maariv" in url:
                worker = MaarivWorker(url)
                newspaper = "maariv"
            elif "mako" in url:
                worker = N12Worker(url)
                newspaper = "mako"
            else:
                worker = IsraelHayomWorker(url)
                newspaper = "israel hayom"

            full_text = worker.parse()
            full_text = full_text.replace("'", "")
            self.DB_queue_handler.insert_data_to_DB_queue(newspaper, url, full_text, topic)
        #       worker.print_acknowledgement(newspaper)

        except Exception as e:
            self.DB_queue_handler.notify_handler_of_error()
            # print(" [-] Error in parsing - {}".format(e))

    def start_consumption(self):
        self.channel.basic_consume(
            queue='url_queue', on_message_callback=self.callback, auto_ack=True
        )

        self.channel.start_consuming()

# worker = QueueWorker()
# worker.start_consumption()
