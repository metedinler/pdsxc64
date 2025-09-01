import threading
import multiprocessing

class AsyncManager:
    def __init__(self):
        self.threads = []
        self.processes = []

    def create_thread(self, target):
        thread = threading.Thread(target=target)
        self.threads.append(thread)
        thread.start()
        return thread

    def create_process(self, target):
        process = multiprocessing.Process(target=target)
        self.processes.append(process)
        process.start()
        return process

    def join_all(self):
        for thread in self.threads:
            thread.join()
        for process in self.processes:
            process.join()