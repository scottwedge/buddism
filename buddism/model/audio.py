#!/usr/bin/env python
#coding = utf-8

import config
import time
import json

from tornado.util import ObjectDict
from redis import Redis

_client = Redis(config.REDIS_HOST, config.REDIS_PORT, config.REDIS_DB)
_KEY = 'audio'

class AudioDAO(object):
    @classmethod
    def get_audios(cls, since=float('-INF'), before=float('INF'), offset=0, limit=10):
        ret = []
        for item in _client.zrangebyscore(_KEY, since, before, offset, limit, withscores = True):
            data = json.loads(item[0])
            data['created'] = int(item[1])
        cls.set_header('Content-Type', 'application/json')
        cls.write(json.dumps(ret))

    @classmethod
    def add_audio(cls, audio):
        audio = ObjectDict(audio)
        _client.zadd(_KEY, json.dumps(audio), int(time.time()))
        pass


