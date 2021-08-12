import pika
import json
from DatabaseHandlers.queue_publisher import QueuePublisher
from HebrewMorphologyEngine.morphology_engine import HebrewMorphologyEngine
from DatabaseHandlers.cache_queue_publisher import CacheQueuePublisher


class MorphologyEngineWorker:
    def __init__(self):
        connection_parameter = "localhost"
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=connection_parameter)
        )
        self.channel = self.connection.channel()
        self.result = self.channel.queue_declare(queue="morphology_engine_queue", durable=True)
        self.publisher = QueuePublisher("database")
        self.cache_publisher = CacheQueuePublisher()

    def callback(self, ch, method, properties, body):
        body = body.decode("utf-8")
        body = json.loads(body)
        if type(body) == int:
            self.publisher.send_article_amount(body)
            return

        try:
            full_text = ""
            engine = HebrewMorphologyEngine()
            base_words = engine.return_hebrew_morph_dict(body[2])
            full_text.join(base_words.values())
            self.publisher.insert_data_to_queue(body[0], body[1], full_text, body[3])
            for key, value in base_words.items():
                self.cache_publisher.insert_data_to_queue(key, value)
            print("[+] Morphed text")

        except Exception as e:
            print(e)
            self.publisher.notify_handler_of_error()

    def start_consumption(self):
        self.channel.basic_consume(
            queue='morphology_engine_queue', on_message_callback=self.callback, auto_ack=True
        )

        self.channel.start_consuming()
