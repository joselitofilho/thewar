import threading
import time


class Timeout(threading.Thread):
    def __init__(self, tempoMaximo=60, func=None, func_args=None):
        threading.Thread.__init__(self)
        self.tempo = 0
        self.tempoMaximo = tempoMaximo
        self.func = func
        self.func_args = func_args
        self.loop = True

    def run(self):
        self.tempo = 0.0
        self.loop = True
        while self.tempo < self.tempoMaximo and self.loop:
            time.sleep(0.5)
            self.tempo += 0.5

        if self.loop and self.tempo == self.tempoMaximo and self.func is not None:
            if self.func_args:
                self.func(**self.func_args)
            else:
                self.func()

    def para(self):
        self.loop = False
        # raise Exception("ThreadTimeout: Forcando a parada da thread...")

    def __del__(self):
        self.para()
