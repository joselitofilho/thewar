import time
import threading

class Timeout(threading.Thread):
    def __init__(self, tempoMaximo=60, func=None):
        threading.Thread.__init__(self)
        self.tempo = 0
        self.tempoMaximo = tempoMaximo
        self.func = func
        self.loop = True
    
    def run(self):
        self.tempo = 0
        self.loop = True
        while (self.tempo < self.tempoMaximo and self.loop):
            time.sleep(1)
            self.tempo += 1
        
        if self.tempo == self.tempoMaximo and self.func != None and self.loop:
            self.func()

    def para(self):
        self.loop = False
        raise Exception("ThreadTimeout: Forcando a parada da thread...")

    def __del__(self):
        self.para()
