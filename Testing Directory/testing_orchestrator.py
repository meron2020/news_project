import threading

from HebrewMorphologyEngine.morphology_workers_orchestrator import MorphologyWorkersOrchestrator
from QueueWorkers.workers_orchestrator import WorkersOrchestrator
from DatabaseHandlers.database_handler_orchestrator import DatabaseHandlerOrchestrator
from testing_urls_file import TestingUrlsSender


class TestingOrchestrator:
    def run_orchestrator(self):
        handler = DatabaseHandlerOrchestrator()
        handler_thread = threading.Thread(target=handler.run_orchestrator)
        word_dict = handler.get_all_rows_from_cache()
        handler_thread.start()
        cache_thread = threading.Thread(target=handler.create_cache_db)
        cache_thread.start()
        morphology_workers = MorphologyWorkersOrchestrator()
        morphology_workers.run_orchestrator(3, word_dict)
        workers = WorkersOrchestrator()
        workers.run_orchestrator(3)
        TestingUrlsSender.send_urls()


orchestrator = TestingOrchestrator()
orchestrator.run_orchestrator()
