import threading
from webscrapers_orchestrator import WebscrapersOrchestrator
from flask_app.Backend.Clustering.Graphs.networkx_graph import GraphConnections


class BackendOrchestrator:
    def __init__(self):
        self.webscrapers = WebscrapersOrchestrator()
        self.graph_connections = GraphConnections()

    def run_orchestrator(self):
        graph_thread = threading.Thread(target=self.graph_connections.start_consumption, args=())
        graph_thread.start()

        self.webscrapers.run_orchestrator()


orchestrator = BackendOrchestrator()
orchestrator.run_orchestrator()
