import random

from .ialucy import IALucy


class IAFactory:
    disponiveis = {
        'Atena': IALucy,
        'Cindy': IALucy,
        'Joana': IALucy,
        'Lucy': IALucy,
        'Mavis': IALucy,
        'Minerva': IALucy,
    }

    def build(self, target):
        return self.disponiveis[target]

    def random(self):
        cpus = list(self.disponiveis.keys())
        random.shuffle(cpus)
        return self.build(cpus[0])
