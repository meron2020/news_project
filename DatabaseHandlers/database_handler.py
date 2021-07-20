import sqlite3
import pika
import json


class DatabaseHandler:
    def __init__(self, routing_key_num, connection, cursor):
        self.queue_connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        self.channel = self.queue_connection.channel()
        self.channel.exchange_declare(exchange='database', exchange_type="direct", durable=True)
        self.result = self.channel.queue_declare(queue='', exclusive=True)
        self.queue_name = self.result.method.queue

        routing_key = "routing_" + routing_key_num
        self.channel.queue_bind(exchange='database', queue=self.queue_name, routing_key=routing_key)

        self.connection = connection
        self.cursor = cursor

        self.articles_inserted_num = 0
        self.articles_not_inserted_num = 0

    def insert_article(self, newspaper, url, full_text, topic):
        try:
            sqlite_insert_query = """INSERT INTO articles
            (newspaper, url, full_text, topic, cluster_id)
            VALUES
            ('{}', '{}', '{}', '{}', NULL);""".format(newspaper, url, full_text, topic)
            count = self.cursor.execute(sqlite_insert_query)
            self.connection.commit()
            self.articles_inserted_num += 1
            if self.articles_inserted_num % 50 == 0:
                print(" [+] {} articles inserted successfully.".format(self.articles_inserted_num))
                print(" [-] {} articles failed to insert.".format(self.articles_not_inserted_num))
        except sqlite3.Error as error:
            self.articles_not_inserted_num += 1
            # print("Failed to insert data into sqlite table", error)

    def callback(self, ch, method, properties, body):
        body = body.decode("utf-8")
        body = json.loads(body)
        if body == "Error in Parsing.":
            self.articles_not_inserted_num += 1
        else:
            self.insert_article(body[0], body[1], body[2], body[3])

    def start_consumption(self):
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=self.callback, auto_ack=True
        )

        self.channel.start_consuming()

    def update_cluster_id(self, cluster_id_dict):
        for i in range(cluster_id_dict.keys()):
            cluster_id = cluster_id_dict[cluster_id_dict.keys()[i]]
            try:
                sqlite_insert_query = """UPDATE articles
                SET cluster_id = {},
                WHERE id = {};""".format(cluster_id, i + 1)
                count = self.cursor.execute(sqlite_insert_query)
                self.connection.commit()
                print(" [+] Inserted cluster id successfully.")
            except sqlite3.Error as error:
                print(" [-] Failed to insert cluster id.", error)
