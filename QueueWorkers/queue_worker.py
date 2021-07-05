from israel_hayom_parser import IsraelHayomWorker
from ynet_parser import YnetWorker
from maariv_parser import MaarivWorker
from N12_parser import N12Worker
import pika
from database_handler import DatabaseHandler

handler = DatabaseHandler()

news_links = []
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

channel = connection.channel()
channel.exchange_declare(exchange='news_urls', exchange_type="direct", durable=True)
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

counter = 0

routing_keys = []
for i in range(4):
    routing_keys.append("routing_" + str(i))

for routing_key in routing_keys:
    channel.queue_bind(exchange='news_urls', queue=queue_name, routing_key=routing_key)


def callback(ch, method, properties, body):
    body = body.decode("utf-8")
    try:
        if "ynet" in body:
            worker = YnetWorker(body)
            newspaper = "ynet"
        elif "maariv" in body:
            worker = MaarivWorker(body)
            newspaper = "maariv"
        elif "mako" in body:
            worker = N12Worker(body)
            newspaper = "mako"
        else:
            worker = IsraelHayomWorker(body)
            newspaper = "israel hayom"

        full_text = worker.parse()
        full_text = full_text.replace("'", "")
        handler.insert_article(newspaper, body, full_text)
#        worker.print_acknowledgement(newspaper)

    except Exception:
        print(" [-] Error in parsing")


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True
)

channel.start_consuming()
