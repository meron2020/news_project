from QueueWorkers.workers_orchestrator import WorkersOrchestrator
from News_Crawlers.CrawlersHandler import CrawlersHandler
import threading
from DatabaseHandlers.database_handler_orchestrator import DatabaseHandlerOrchestrator
from HebrewMorphologyEngine.morphology_workers_orchestrator import MorphologyWorkersOrchestrator


class WebscrapersOrchestrator:
    def run_orchestrator(self):
        handler = DatabaseHandlerOrchestrator()
        handler_thread = threading.Thread(target=handler.run_orchestrator, args=())
        handler_thread.start()
        morphology_workers = MorphologyWorkersOrchestrator()
        morphology_workers.run_orchestrator(10)
        workers = WorkersOrchestrator()
        workers.run_orchestrator(10)

        crawler_handler = CrawlersHandler()
        crawler_thread = threading.Thread(target=crawler_handler.crawl_links, args=())
        crawler_thread.start()


orchestrator = WebscrapersOrchestrator()
orchestrator.run_orchestrator()
