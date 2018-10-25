import time

class Periodic:

    def __init__(self, period, task):
        self.period = period
        self.isOn = False
        self.task = task

    def start(self):
        if self.isOn:
            return False
        self.isOn = True
        self._doit()

    def stop(self):
        if not self.isOn:
            return False
        self.isOn = False

    def _doit(self):
        while self.isOn:
            self.task()
            time.sleep(self.period)