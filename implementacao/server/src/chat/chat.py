# -*- coding: utf-8 -*-
import json
import re


class Chat(object):
    KICK_COMMAND = 'kick'

    def interpreta_comandos(self, texto):
        comando = None
        with open('src/chat/comandos_adms.json') as json_file:
            comandos = json.load(json_file)
            for cmd in comandos:
                match = re.match(cmd['regex'], texto)
                if match:
                    comando = cmd['comando']
                    argumento = match.group().replace('!' + comando, '')
                    break

        if comando:
            if comando == Chat.KICK_COMMAND:
                return argumento, Chat.KICK_COMMAND

        with open('src/chat/comandos_gerais.json') as json_file:
            comandos = json.load(json_file)

            lista_comandos = []
            for cmd in comandos:
                lista_comandos.append(cmd['comando'])
            if '!help' in texto or '!comandos' in texto or '!sons' in texto or '!memes' in texto:
                texto = 'Comandos --> !' + ', !'.join(lista_comandos)
                return texto, None

            for cmd in comandos:
                texto = re.sub(cmd['regex'], cmd['html'], texto)
        return texto, None
