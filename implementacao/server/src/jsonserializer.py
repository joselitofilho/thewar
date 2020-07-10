#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from json import JSONEncoder


class SerializerEncoder(JSONEncoder):
    def default(self, object):
        if type(object) == {}.values().__class__:
            return list(object)
        else:
            return object.__dict__


class JSONSerializer(object):
    def fromJson(self, jsonMsg):
        self.__dict__ = json.loads(jsonMsg)

    def toJson(self):
        return SerializerEncoder().encode(self).encode('utf-8')
