class IAInterface:

    def usuario(self):
        raise NotImplementedError()

    def jogador_ref(self, value):
        raise NotImplementedError()

    def processa_msg(self, jogo, msg):
        raise NotImplementedError()

    def turno_distribuir_tropas_globais(self, jogo, params):
        raise NotImplementedError()

    def turno_distribuir_tropas_grupo_territorio(self, jogo, params):
        raise NotImplementedError()

    def turno_distribuir_topas_troca_de_cartas(self, jogo, params):
        raise NotImplementedError()

    def turno_troca_de_cartas(self, jogo, params):
        raise NotImplementedError()

    def turno_atacar(self, jogo, params):
        raise NotImplementedError()

    def turno_mover(self, jogo, params):
        raise NotImplementedError()
