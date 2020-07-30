import random

from .iaathena import IAAthena
from .iadummy import IADummy
from .ialucy import IALucy


class IAFactory:
    disponiveis = {
        'Atena': IAAthena,
        'Cindy': IALucy,
        'Joana': IALucy,
        'Lucy': IALucy,
        'Mavis': IALucy,
        'Minerva': IALucy
    }

    def build(self, target):
        return self.disponiveis[target]

    def random(self):
        cpus = list(self.disponiveis.keys())
        random.shuffle(cpus)
        return self.build(cpus[0])

    def dummy(self):
        return IADummy
