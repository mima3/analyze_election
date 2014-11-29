# coding: utf-8
import sys
import cookielib
import cgi
import urllib
import urllib2
from lxml import etree
import socket
import datetime
import time
import json

class NicoCtrl():
    def __init__(self, nicovideo_id, nicovideo_pw):
        self.nicovideo_id = nicovideo_id
        self.nicovideo_pw = nicovideo_pw
        # ログイン
        cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        req = urllib2.Request("https://secure.nicovideo.jp/secure/login")
        req.add_data( urllib.urlencode( {"mail": self.nicovideo_id, "password":self.nicovideo_pw} ))
        res = self.opener.open(req).read()
        if not 'user_session' in cj._cookies['.nicovideo.jp']['/']:
            raise Exception('PermissionError')

    def _getjson(self, url, errorcnt):
        # 途中でJSONが切れて帰ってくる場合があるので、リトライ処理
        try:
            res = self.opener.open(url, timeout=100).read()
            return json.loads(res)
        except ValueError:
            if errorcnt < 3:
                errorcnt = errorcnt + 1
                return self._getjson(url, errorcnt)
            else:
               raise

    def get_live_comment(self, movie_id):
        self.movie_id = movie_id


        # 動画配信場所取得(getflv)
        res = self.opener.open("http://watch.live.nicovideo.jp/api/getplayerstatus?v="+self.movie_id).read()
        root = etree.fromstring(res)
        messageServers = root.xpath('//ms')
        if len(messageServers) == 0:
            raise Exception('UnexpectedXML')

        user_ids = root.xpath('//user_id')
        if len(user_ids) == 0:
            raise Exception('NotfoundUserId')
        user_id = user_ids[0].text

        thread_id = messageServers[0].find('thread').text
        addr = messageServers[0].find('addr').text
        port = int(messageServers[0].find('port').text) - 2725
        
        # waybackkey の取得
        waybackkeyUrl = ('http://watch.live.nicovideo.jp/api/getwaybackkey?thread=%s' % thread_id)
        req = urllib2.Request(waybackkeyUrl)
        res = self.opener.open(waybackkeyUrl).read()
        waybackkey = cgi.parse_qs(res)['waybackkey'][0]

        msUrl = 'http://%s:%d/api.json/thread?' % (addr, port)
        chats = []
        req = urllib2.Request(msUrl)
        when = '4294967295'
        while True:
            data = {
                'thread' : thread_id, 
                'version' : "20061206",
                'res_from' : '-1000',
                'waybackkey' : waybackkey,
                'user_id' : user_id,
                'when': when,
                'scores' : '1'
            }
            list = self._getjson(msUrl+urllib.urlencode(data), 0)
            chatcnt = 0
            insertdata = []
            for l in list:
                if 'chat' in l:
                    if chatcnt == 0:
                        when = int(l['chat']['date']) - 1
                    if l['chat']['content'] != '/disconnect':
                        insertdata.append(l['chat'])
                    chatcnt += 1
            chats = insertdata + chats
            if chatcnt == 0:
                break
        return chats

