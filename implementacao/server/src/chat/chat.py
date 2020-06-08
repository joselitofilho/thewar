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

            mapa_comandos = {}
            lista_comandos = []
            for cmd in comandos:
                mapa_comandos[cmd['comando']] = cmd
                lista_comandos.append(cmd['comando'])
            if '!help' in texto or '!comandos' in texto or '!memes' in texto:
                texto = 'Comandos --> !' + ', !'.join(lista_comandos)
                return texto, None

            cmd_pergunta = mapa_comandos['pergunta']
            match = re.match(cmd_pergunta['regex'], texto)
            if match:
                texto = match.group()
                texto_split = texto.split('?')
                pergunta = texto_split[0].replace('!' + cmd_pergunta['comando'], '').strip() + '?'
                opcoes = texto_split[1].split(',')
                texto = cmd_pergunta['html'].replace('pergunta', pergunta).replace(
                    'respostapositiva', opcoes[0].strip()).replace(
                    'respostanegativa', opcoes[1].strip())
            else:
                for cmd in comandos:
                    texto = re.sub(cmd['regex'], cmd['html'], texto)
        return texto, None
