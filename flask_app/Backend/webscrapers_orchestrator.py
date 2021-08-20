from flask_app.Backend.QueueWorkers.workers_orchestrator import WorkersOrchestrator
from flask_app.Backend.News_Crawlers.CrawlersHandler import CrawlersHandler
import threading
from flask_app.Backend.DatabaseHandlers.database_handler_orchestrator import DatabaseHandlerOrchestrator
from flask_app.Backend.HebrewMorphologyEngine.morphology_workers_orchestrator import MorphologyWorkersOrchestrator


class WebscrapersOrchestrator:
    def run_orchestrator(self):
        handler = DatabaseHandlerOrchestrator()
        cache_thread = threading.Thread(target=handler.create_cache_db)
        cache_thread.start()
        word_dict = handler.get_all_rows_from_cache()
        handler_thread = threading.Thread(target=handler.run_orchestrator, args=())
        handler_thread.start()
        morphology_workers = MorphologyWorkersOrchestrator()
        morphology_workers.run_orchestrator(3, word_dict)
        workers = WorkersOrchestrator()
        workers.run_orchestrator(3)

        crawler_handler = CrawlersHandler()
        crawler_thread = threading.Thread(target=crawler_handler.crawl_links, args=())
        crawler_thread.start()
