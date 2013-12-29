from tipoAcaoTurno import *
from timeout import *

class Turno(object):

    def __init__(self):
        self.numero = 1
        self.tipoAcao = TipoAcaoTurno.distribuir_tropas_globais

        # Atributo utilizado para o turno: distribuir tropas para os grupos de territorios.
        self.gruposTerritorio = []

        self.reiniciaVariaveisExtras()
   
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
        self.loopTimeout = Timeout(60, funcTimeout)
        self.loopTimeout.start()
    
    def paraTimeout(self):
        self.loopTimeout.stop()
        del self.loopTimeout

    def __del__(self):
        self.paraTimeout()
