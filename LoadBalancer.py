import os
import threading
import time

from Directory import Directory


class MyLoadBalancer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.files_queue = []
        self.thread_wait_time = 0.5
        self.PRIORITY = 0
        self.FILE = 1
        self.WAIT_TIME = 2
        self.client_list = []
        self.directories = [Directory(), Directory(), Directory(), Directory(), Directory()]

    def add_files(self, files):
        if len(self.files_queue) == 0:
            for file in files:
                self.files_queue.append([self.count_priority(0.1, file.size), file, 0.1])
        else:
            for file in files:
                self.files_queue.append([self.count_priority(0.1, file.size), file, 0.1])
        self.files_queue.sort(reverse=True, key=self.by_priority)

    def by_priority(self, queue):
        return queue[self.PRIORITY]

    def count_priority(self, wait_time, size):
        return wait_time / size * len(self.files_queue)

    def run(self):
        while True:

            if len(self.files_queue) > 0:
                file_queue = []
                for file in self.files_queue:
                    file_queue.append([self.count_priority(file[self.WAIT_TIME], file[1].size),
                                       file[self.FILE],
                                       file[self.WAIT_TIME] + self.thread_wait_time])

                file_queue.sort(reverse=True, key=self.by_priority)
                for directory in self.directories:
                    if directory.is_free() and len(self.files_queue) > 0:
                        directory.send_file(self.files_queue.pop(0)[self.FILE])

            time.sleep(self.thread_wait_time)
