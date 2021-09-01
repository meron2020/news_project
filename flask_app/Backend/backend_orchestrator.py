import threading
from webscrapers_orchestrator import WebscrapersOrchestrator
from flask_app.Backend.Graphs.networkx_graph import GraphConnections
webscrapers = WebscrapersOrchestrator()
graph_connections = GraphConnections()
graph_thread = threading.Thread(target=graph_connections.start_consumption, args=())
graph_thread.start()

webscrapers.run_orchestrator()
