from .queue_worker import QueueWorker
import threading


class WorkersOrchestrator:
    @classmethod
    def worker_func(cls, worker):
        worker.start_consumption()

    def run_orchestrator(self):
        worker_list = []

        for i in range(1):
            worker_list.append(QueueWorker())

        worker_threads = list()
        for worker in worker_list:
            x = threading.Thread(target=self.worker_func, args=(worker,))
            worker_threads.append(x)
            x.start()
