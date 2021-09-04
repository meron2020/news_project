import json
import sqlite3
from flask_app.Backend.Models.morphed import Morphed
import pika


class CacheDatabaseHandler:
    def __init__(self):

        self.queue_connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        self.channel = self.queue_connection.channel()
        self.result = self.channel.queue_declare(queue='morphology_cache', durable=True)

    def insert_morphology_words(self, word, morphed_word):
        try:
            morphed = Morphed(word, morphed_word)
            morphed.save_to_db()
        except sqlite3.Error as error:
            print("Failed to insert data into sqlite table", error)

    def return_word_to_morph_dict(self):
        morphed_words = Morphed.query.all()
        morphology_cache = {}
        for morphed in morphed_words:
            morphology_cache[morphed.word] = morphed.morphed_word
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
