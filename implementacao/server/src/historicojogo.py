# -*- coding: utf-8 -*-
import logging
import sqlite3
import sys

from src.jsonserializer import *


class HistoricoJogo(JSONSerializer):
    def __init__(self, baseDeDados='war.db'):
        self.baseDeDados = baseDeDados

    def new(self, infos):
        try:
            conn = sqlite3.connect(self.baseDeDados)
            c = conn.cursor()

            c.execute("INSERT INTO HistoricoJogos(nome, iniciou_em, infos) VALUES (?, ?, ?);",
                      [infos.nome, infos.iniciou_em, infos.toJson()])
            conn.commit()
            conn.close()
        except:
            logging.error("HistoricoJogo erro {} ao salvar o jogo {}".format(sys.exc_info()[0], infos))
