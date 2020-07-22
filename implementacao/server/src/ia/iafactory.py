import random

from .iadummy import IADummy
from .ialucy import IALucy
from .iaathena import IAAthena


class IAFactory:
    disponiveis = {
        'Atena': IAAthena,
        'Cindy': IALucy,
        'Joana': IALucy,
        'Lucy': IALucy,
        'Mavis': IALucy,
        'Minerva': IALucy,
        # 'Atena': IADummy,
        # 'Cindy': IADummy,
        # 'Joana': IADummy,
        # 'Lucy': IADummy,
        # 'Mavis': IADummy,
        # 'Minerva': IADummy,
    }

    def build(self, target):
        return self.disponiveis[target]

    def random(self):
        cpus = list(self.disponiveis.keys())
        random.shuffle(cpus)
        return self.build(cpus[0])
