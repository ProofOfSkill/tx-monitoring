import time


class TaskManager:
    def __init__(self, delay, task):
        self.delay = delay
        self.isOn = False
        self.task = task

    def start(self):
        if self.isOn:
            return False
        self.isOn = True
        self.do()

    def stop(self):
        if not self.isOn:
            return False
        self.isOn = False

    def do(self):
        while self.isOn:
            self.task()
            time.sleep(self.delay)

