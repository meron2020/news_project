import sqlite3
import pika
import json
import random


class DatabaseHandler:
    def __init__(self, routing_key_num, connection, cursor, table_name):
        self.queue_connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        self.channel = self.queue_connection.channel()
        self.channel.exchange_declare(exchange='database', exchange_type="direct", durable=True)
        self.result = self.channel.queue_declare(queue='', exclusive=True)
        self.queue_name = self.result.method.queue
        self.table_name = table_name

        routing_key = "routing_" + routing_key_num
        self.channel.queue_bind(exchange='database', queue=self.queue_name, routing_key=routing_key)

        self.topic_dict = {}

        self.connection = connection
        self.cursor = cursor

        self.article_amount = 0
        self.articles_sent = 0

        self.articles_inserted_num = 0
        self.articles_not_inserted_num = 0

        self.create_topic_dict()

    def insert_article(self, newspaper, url, full_text, topic):
        try:
            sqlite_insert_query = """INSERT INTO {}
            (newspaper, url, full_text, topic, cluster_id)
            VALUES
            ('{}', '{}', '{}', '{}', NULL);""".format(self.table_name, newspaper, url, full_text, topic)
            count = self.cursor.execute(sqlite_insert_query)
            self.connection.commit()
            self.articles_inserted_num += 1
            if self.articles_inserted_num % 50 == 0:
                # print(" [+] {} articles inserted successfully.".format(self.find_articles_inserted_num()))
                # print(" [-] {} articles failed to insert.".format(self.articles_not_inserted_num))
                self.find_each_newspaper_num()

            if self.find_articles_inserted_num() == self.article_amount:
                self.find_articles_inserted_num()
        except sqlite3.Error as error:
            self.articles_not_inserted_num += 1
            print("Failed to insert data into sqlite table", error)
        return self.cursor.lastrowid

    def find_articles_inserted_num(self):
        sqlite_insert_query = "SELECT COUNT(*) FROM articles"
        self.cursor.execute(sqlite_insert_query)
        cur_result = self.cursor.fetchone()
        return cur_result

    def find_each_newspaper_num(self):
        newspaper_dict = {'ynet': 0, 'maariv': 0, 'walla': 0, 'mako': 0}
        query = "SELECT * FROM articles"
        self.cursor.execute(query)
        cur_result = self.cursor.fetchall()
        for result in cur_result:
            for newspaper in newspaper_dict.keys():
                if newspaper in result[1]:
                    newspaper_dict[newspaper] += 1
        print("\n")
        for newspaper in newspaper_dict:
            print("{} - {}".format(newspaper, newspaper_dict[newspaper]))

    def callback(self, ch, method, properties, body):
        body = body.decode("utf-8")
        body = json.loads(body)
        if body == "Error in Parsing.":
            self.articles_not_inserted_num += 1
            self.articles_sent += 1
        elif type(body) == int:
            self.article_amount = body
        else:
            _id = self.insert_article(body[0], body[1], body[2], body[3])
            cluster_id = self.random_clustering(body[3])
            self.update_cluster_id(_id, cluster_id)
            self.articles_sent += 1

    def start_consumption(self):
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=self.callback, auto_ack=True
        )

        self.channel.start_consuming()

    def create_topic_dict(self):
        topic_dict = {'צבא וביטחון': [],
                      'מדיני': [],
                      'המערכת הפוליטית': [],
                      'פלסטינים': [],
                      'כללי': [],
                      'משפט ופלילים': [],
                      'חינוך ובריאות': [],
                      'חדשות בעולם': []}

        for topic in topic_dict.keys():
            topic_index = list(topic_dict.keys()).index(topic) * 4
            topic_dict[topic] = list(range(topic_index, topic_index + 4))

        self.topic_dict = topic_dict

    def update_cluster_id(self, _id, cluster_id):
        try:
            sqlite_insert_query = """UPDATE {}
                SET cluster_id = {}
                WHERE id = {};""".format(self.table_name, str('"' + cluster_id + '"'), _id)
            count = self.cursor.execute(sqlite_insert_query)
            self.connection.commit()
        except sqlite3.Error as error:
            print(" [-] Failed to insert cluster id.", error)

    def random_clustering(self, topic_arg):
        cluster_list = self.topic_dict[topic_arg]
        cluster_ids = []
        for i in range(2):
            cluster_ids.append(str(random.choice(cluster_list)))

        cluster_ids_str = ",".join(cluster_ids)
        return cluster_ids_str

    def select_all_rows(self):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        self.cursor.execute("SELECT * FROM tasks")

        rows = self.cursor.fetchall()

        row_list = []
        for row in rows:
            row_list.append(row)

        return row_list

    def delete_all_rows(self):
        sqlite_insert_query = "DELETE FROM {};".format(self.table_name)
        count = self.cursor.execute(sqlite_insert_query)
        self.connection.commit()
