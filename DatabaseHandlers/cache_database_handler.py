import json
import sqlite3

import pika


class CacheDatabaseHandler:
    def __init__(self, connection, cursor, table_name):
        self.connection = connection
        self.cursor = cursor
        self.table_name = table_name

        self.queue_connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        self.channel = self.queue_connection.channel()
        self.result = self.channel.queue_declare(queue='morphology_cache', durable=True)
        self.table_name = table_name
        self.connection = connection
        self.cursor = cursor

    def insert_morphology_words(self, word, morphed_word):
        word = '"' + word + '"'
        morphed_word = '"' + morphed_word + '"'
        try:
            sqlite_insert_query = """INSERT INTO {} (word, morphed_word) VALUES ({}, {});""".format(self.table_name,
                                                                                                    word, morphed_word)
            count = self.cursor.execute(sqlite_insert_query)
            self.connection.commit()
        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)

    def return_word_to_morph_dict(self):
        self.cursor.execute("SELECT * FROM {}".format(self.table_name))

        rows = self.cursor.fetchall()

        morphology_cache = {}
        for row in rows:
            morphology_cache[row[0]] = row[1]
        return morphology_cache

    def callback(self, ch, method, properties, body):
        body = body.decode("utf-8")
        body = json.loads(body)
        self.insert_morphology_words(body[0], body[1])

    def start_consumption(self):
        self.channel.basic_consume(
            queue="morphology_cache", on_message_callback=self.callback, auto_ack=True
        )

        self.channel.start_consuming()
