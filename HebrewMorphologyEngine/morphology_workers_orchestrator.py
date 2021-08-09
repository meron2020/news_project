import threading
from HebrewMorphologyEngine.morphology_engine_worker import MorphologyEngineWorker


class MorphologyWorkersOrchestrator:
    @classmethod
    def worker_func(cls, worker):
        worker.start_consumption()

    def run_orchestrator(self):
        worker_list = []

        for i in range(10):
            worker_list.append(MorphologyEngineWorker())

        worker_threads = list()
        for worker in worker_list:
            x = threading.Thread(target=self.worker_func, args=(worker,))
            worker_threads.append(x)
            x.start()
