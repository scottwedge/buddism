#-*- coding:utf-8 -*-
#!/usr/bin/env python
import json
import config
import time
import tornado
import os

import buddism.network
from buddism.mail import send_mail

from model.audio import AudioDAO
from redis import Redis

_client = Redis(config.REDIS_HOST, config.REDIS_PORT)
_KEY = "FEED"
_SKEY = "SERIAL"
_FKEY = 'FABAO'
_AKEY = 'ACTIVITY'

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

class SerialHandler(tornado.web.RequestHandler):
    def get(self):
        data = []
        offset = int(self.get_argument('offset', 0))
        limit = int(self.get_argument('limit', 20))
        for item in _client.zrange(_SKEY, offset, limit + offset - 1, withscores = True):
            j_obj = json.loads(item[0])
            j_obj['created'] = int(item[1])
            j_obj['coverUrl']='http://huaxingtan.cn/cover/grid_big.png'
            data.append(j_obj)
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(data))

class FabaoHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('''
            <head>
                <meta http-equiv="refresh" content="5; url=http://huaxingtan.cn"/>
            </head>
            <body>
            您的请求已经记录，我们会很快跟您联系
            <br>
            5秒后跳转到<a href="http://huaxingtan.cn">化性谈首页</a>
            </body>
        ''')

    def post(self):
        name = self.get_argument('name','')
        qq   = self.get_argument('qq', '')
        phone = self.get_argument('phone','')
        fabao = self.get_argument('fabao', '')
        _key = int(time.time()*100)
        print name
        print qq
        _client.lpush(_FKEY, json.dumps({'id':_key, 'name':name, 'qq':qq, 'phone':phone, 'fabao':fabao}))
        print _key
        send_mail(u'姓名:%s<br> QQ:%s<br> 电话:%s<br> 法宝内容:%s<br>'%(name,qq,phone,fabao))
        self.write(str(_key))

class ActivityHandler(tornado.web.RequestHandler):
    def post(self):
        phone = self.get_argument('phone', '')
        date = time.time()
        ret = u'手机号格式错误' 
        if valid_phone(phone):
            _client.lpush(_AKEY, json.dumps({'phone':phone, 'date':time.time()}))
            ret = u'提交成功' 
        self.write(ret)

    def get(self):
        self.set_header('Content-type', 'text/csv') 
        self.set_header('Content-dispostion', 'attachment;filename=activity.csv')
        ret = 'phone\n'
        lst = _client.lrange(_AKEY, 0, -1)
        for item in lst:
            data = json.loads(item)
            ret = ret + data['phone'] + '\n'
        self.write(ret)


def valid_phone(phone):
    return len(phone) == 11 and phone.isdigit()
