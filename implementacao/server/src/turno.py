from timeout import *
from tipoAcaoTurno import *


class Turno(object):
    TIMEOUT = (2 * 60) + 4

    def __init__(self):
        self.numero = 1
        self.tipoAcao = TipoAcaoTurno.distribuir_tropas_globais

        # Atributo utilizado para o turno: distribuir tropas para os grupos de territorios.
        self.gruposTerritorio = []

        self.reiniciaVariaveisExtras()

        self.trocouCartas = False

        self.loopTimeout = None

    def reiniciaVariaveisExtras(self):
        self.reiniciaVariaveisExtrasGruposTerritorios()
        self.reiniciaVariaveisExtrasMoverAposConquistar()

    def reiniciaVariaveisExtrasGruposTerritorios(self):
        self.quantidadeDeTropas = 0

        # Atributo utilizado para o turno: distribuir tropas para os grupos de territorios.
        self.grupoTerritorioAtual = None

    def reiniciaVariaveisExtrasMoverAposConquistar(self):
        # Atributos utilizado para o turno: mover tropas apos conquistar territorio.
        self.tropasParaMoverAposAtaque = 0
        self.territoriosDoAtaqueDaConquista = []
        self.territorioConquistado = None

    def iniciaTimeout(self, funcTimeout):
        if self.loopTimeout != None:
            self.paraTimeout()

        self.loopTimeout = Timeout(self.TIMEOUT, funcTimeout)
        self.loopTimeout.start()

    def paraTimeout(self):
        try:
            self.loopTimeout.para()
        except:
            print
            "Thread foi morta com excecao!"

        del self.loopTimeout
        self.loopTimeout = None

    @property
    def tempoRestante(self):
        if self.loopTimeout != None:
            return self.TIMEOUT - self.loopTimeout.tempo - 4
        return self.TIMEOUT - 4

    def __del__(self):
        self.paraTimeout()
