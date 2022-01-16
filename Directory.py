import threading
import time


class Directory(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.progress = 0
        self.file_left = 0
        self.file_size = 1
        self.file_name = ""
        self.alive = False
        self.SEND_SPEED = 1000
        self.thread_wait_time = 0.5

    def send_file(self, file):
        self.file_size = file.size
        self.file_left = self.file_size
        self.file_name = file.name
        print("file:",self.file_name)
        if not self.alive:
            self.start()

    def run(self):
        self.alive = True
        while True:
            while self.file_left > 0:
                self.file_left -= self.SEND_SPEED
                self.progress = int((self.file_size - self.file_left) / self.file_size * 100)
                if self.progress > 100:
                    self.progress = 100
                time.sleep(self.thread_wait_time)
            self.file_left = 0
            self.file_name = ""
            self.progress = 0
    def is_free(self):
        if self.file_left == 0:
            return True
        return False
