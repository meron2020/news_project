import json

import networkx as nx
import networkx.algorithms.components as nac
from flask_app.Backend.NLP.nlp_algorithms import NLPProcessor
from flask_app.Backend.DatabaseHandlers.database_handler_orchestrator import DatabaseHandlerOrchestrator
import pika


class GraphConnections:
    def __init__(self):
        self.handler = DatabaseHandlerOrchestrator()
        self.queue_connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.queue_connection.channel()
        self.result = self.channel.queue_declare(queue="event_notifications", durable=True)
        self.processor = ""
        self.id_to_text_dict = ""
        self.id_to_tuple_dict = ""

    def create_NLP(self):
        self.processor = NLPProcessor()
        self.id_to_text_dict, self.id_to_tuple_dict = self.processor.get_id_to_text_dict()
        self.processor.get_id_to_title_dict()

    def find_top_similarities(self):
        texts_dense_list = self.processor.sklearn_vectorize_texts()
        texts_similarity_dict = NLPProcessor.turn_vectors_to_dict(texts_dense_list)
        texts_top_similarities = NLPProcessor.find_top_similarities(texts_similarity_dict, 0.175)
        title_dense_list = self.processor.sklearn_vectorize_title()
        title_similarity_dict = NLPProcessor.turn_vectors_to_dict(title_dense_list)
        title_top_similarities = NLPProcessor.find_top_similarities(title_similarity_dict, 0.125)
        return texts_top_similarities, title_top_similarities

    def callback(self, ch, method, properties, body):
        body = body.decode("utf-8")
        body = json.loads(body)
        if body == "Finished Webscraping":
            self.create_NLP()
            nx_graph = self.create_graph()
            self.update_cluster_ids(nx_graph)

        exit(0)

    def create_graph(self):
        G = nx.Graph()
        texts_top_similarities, title_top_similarities = self.find_top_similarities()
        graph = self.processor.get_average_similarity(title_top_similarities, texts_top_similarities, G)
        return graph

    def update_cluster_ids(self, nx_graph):
        cluster_id_dict = {}
        cluster_number = 0
        for cluster_set in (nac.connected_components(nx_graph)):
            cluster_id_dict[cluster_number] = cluster_set
            cluster_number += 1
        self.handler.update_cluster_ids(cluster_id_dict)
        for row in self.handler.get_all_rows():
            print(str(row[0]) + " >> " + str(row[-1]))

        exit(code=0)

    def start_consumption(self):
        self.channel.basic_consume(
            queue="event_notifications", on_message_callback=self.callback, auto_ack=True
        )

        self.channel.start_consuming()
