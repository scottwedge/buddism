#!/usr/bin/env python
#coding = utf-8
import json
import config
import time
import tornado

import buddism.network

from model.audio import AudioDAO
from redis import Redis

_client = Redis(config.REDIS_HOST, config.REDIS_PORT)
_KEY = "FEED"

class FeedHandler(tornado.web.RequestHandler):
    def get(self):
        data = []
        for item in  _client.zrange(_KEY, 0, 10, withscores = True):
            j_obj = json.loads(item[0])
            data.append((j_obj['data'], int(item[1]), float(j_obj['lo']), float(j_obj['la'])))
        self.set_header('Content-Type',"application/json" )
        self.write(json.dumps(data))

    def post(self):
        data = self.get_argument('data', 'No data received')
        lo   = self.get_argument('lo', -1)
        la   = self.get_argument('la', -1)
        _client.zadd(_KEY, json.dumps({'lo':lo, 'la':la, 'data':data}), int(time.time()))
        self.write("{}")
