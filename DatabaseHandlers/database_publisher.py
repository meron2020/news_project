import pika
import json


class DatabasePublisher:
    def __init__(self):
        connection_parameter = 'localhost'
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=connection_parameter)
        )
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='database', exchange_type='direct', durable=True)

    def insert_data_to_DB_queue(self, newspaper, url, full_text, topic):
        payload = json.dumps([newspaper, url, full_text, topic])

        index = 0
        routing_key = "routing_" + str(index)
        self.channel.basic_publish(
            exchange='database',
            routing_key=routing_key,
            body=payload
        )

    def notify_handler_of_error(self):
        notification = json.dumps("Error in Parsing.")
        index = 0
        routing_key = "routing_" + str(index)
        self.channel.basic_publish(
            exchange='database',
            routing_key=routing_key,
            body=notification
        )

    def send_article_amount(self, amount):
        amount_json = json.dumps(amount)
        index = 0
        routing_key = "routing_" + str(index)
        self.channel.basic_publish(
            exchange='database',
            routing_key=routing_key,
            body=amount_json
        )
        # print("\n [x] Sent {} article to queue".format(newspaper))
