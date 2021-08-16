import networkx as nx
import networkx.algorithms.components as nac
from NLP.nlp_algorithms import NLPProcessor
from DatabaseHandlers.database_handler_orchestrator import DatabaseHandlerOrchestrator
import matplotlib.pyplot as plt


class GraphConnections:
    def __init__(self):
        self.handler = DatabaseHandlerOrchestrator()
        self.processor = ""
        self.id_to_text_dict = ""
        self.id_to_tuple_dict = ""
        self.create_NLP()

    def create_NLP(self):
        self.processor = NLPProcessor()
        self.id_to_text_dict, self.id_to_tuple_dict = self.processor.get_id_to_text_dict()

    def find_top_similarities(self):
        dense_list = self.processor.sklearn_vectorize()
        similarity_dict = NLPProcessor.turn_vectors_to_dict(dense_list)
        return similarity_dict

    def create_graph(self):
        G = nx.Graph()
        similarity_dict = self.find_top_similarities()
        for text_id in self.id_to_text_dict:
            G.add_node(text_id)
        for key, value in similarity_dict.items():
            for other_id, similarity in value.items():
                if similarity > 0.175:
                    G.add_edge(key, other_id)
        return G

    def update_cluster_ids(self, nx_graph):
        cluster_id_dict = {}
        cluster_number = 0
        for cluster_set in (nac.connected_components(nx_graph)):
            cluster_id_dict[cluster_number] = cluster_set
            cluster_number += 1
        self.handler.update_cluster_ids(cluster_id_dict)
        for row in self.handler.get_all_rows():
            print(str(row[0]) + " >> " + str(row[-1]))


graph = GraphConnections()
nx_graph = graph.create_graph()
graph.update_cluster_ids(nx_graph)
# connected_list = [len(c) for c in sorted(nx.conneגcted_components(nx_graph), key=len, reverse=True)]
# for c in nac.connected_components(nx_graph):
#     print(c)
#     print(type(c))

# nx.draw_networkx(connected_list)
# plt.show()
