#!/usr/bin/env python
#coding = utf-8
import json
import config
import time
import tornado
import os

import buddism.network

from model.audio import AudioDAO
from redis import Redis

_client = Redis(config.REDIS_HOST, config.REDIS_PORT)
_KEY = "FEED"

class FeedHandler(tornado.web.RequestHandler):
    def get(self):
        data = []
        offset = int(self.get_argument('offset', 0))
        limit  = int(self.get_argument('limit', 20))
        for item in  _client.zrange(_KEY, offset, limit + offset - 1, withscores = True):
            j_obj = json.loads(item[0])
            j_obj['created'] = int(item[1])
            j_obj['fileUrl'] = config.STATIC_BASE_URL + j_obj['fileUrl'] 
            data.append(j_obj)
        self.set_header('Content-Type',"application/json" )
        self.write(json.dumps(data))

    def post(self):
        data = self.get_argument('data', 'No data received')
        lo   = self.get_argument('lo', -1)
        la   = self.get_argument('la', -1)
        _client.zadd(_KEY, json.dumps({'lo':lo, 'la':la, 'data':data}), int(time.time()))
        self.write("{}")
