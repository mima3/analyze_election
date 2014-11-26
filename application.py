# coding=utf-8
from bottle import get, post, template, request, Bottle, response, redirect
from json import dumps
from election_db import ElectionDb
from twitter_utility import TwitterUtility
import os

app = Bottle()
db = None


twitter_util = None

def setup(conf):
    global app
    global db
    global twitter_util

    dbpath = conf.get('database', 'election_db')
    db = ElectionDb(dbpath)

    consumer_key = conf.get('Twitter', 'consumer_key')
    consumer_secret =  conf.get('Twitter', 'consumer_secret')
    twitter_util = TwitterUtility(consumer_key, consumer_secret, 'https://api.twitter.com/oauth/request_token', 'https://api.twitter.com/oauth/authenticate' , 'https://api.twitter.com/oauth/access_token')

def convertGeoResult(ret):
    dict = {}
    for r in ret:
        key = r[5]
        if dict.get(key) is None:
            dict[key] = []
        dict[key].append([r[6], r[7]])
    res = {}
    for key in dict:
       if len(dict[key]) > 3:
         res[key] = dict[key]
    return res

@app.get('/json/GetCityGeo')
def getCityGeo():
    """
    行政機関の座標情報を取得する
    """
    prefectureName = request.query.prefectureName
    subPrefectureName = request.query.subPrefectureName
    countyName = request.query.countyName
    cityName = request.query.cityName
    ret = db.GetCityGeo(prefectureName, subPrefectureName, countyName, cityName)
    res = convertGeoResult(ret)
    response.content_type = 'application/json;charset=utf-8'
    return dumps(res)

@app.get('/json/GetGeoToCity')
def getGeoToCity():
    lat = float(request.query.lat)
    lng = float(request.query.lng)
    ret = db.GetPos(lat, lng)
    response.content_type = 'application/json;charset=utf-8'
    return dumps(ret)

@app.get('/json/GetElectionArea')
def getElectionArea():
    prefectureName = request.query.prefectureName
    subPrefectureName = request.query.subPrefectureName
    countyName = request.query.countyName
    cityName = request.query.cityName
    ret = db.GetElectionArea(prefectureName, subPrefectureName, countyName, cityName)
    res = []
    for r in ret:
        res.append({'key': r[0], 'notes':r[1]})
    response.content_type = 'application/json;charset=utf-8'
    return dumps(res)

@app.get('/json/get_prefecture_election_area')
def getPrefectureElectionArea():
    prefectureName = request.query.prefectureName
    ret = db.GetPrefectureElectionArea(prefectureName)
    res = []
    for r in ret:
        res.append(r[0])
    response.content_type = 'application/json;charset=utf-8'
    return dumps(res)

@app.get('/json/get_election_area_information')
def getElectionAreaInformation():
    electionArea = request.query.electionArea
    ret = db.GetElectionAreaInformation(electionArea)
    res = []
    for r in ret:
      prefectureName = r[2]
      subPrefectureName = r[3]
      countyName = r[4]
      cityName = r[5]
      retGeo = db.GetCityGeo(prefectureName, subPrefectureName, countyName, cityName)
      resGeo = convertGeoResult(retGeo)
      res.append({
          'key':r[0],
          'notes':r[1],
          'prefectureName':prefectureName,
          'subPrefectureName':subPrefectureName,
          'countyName':countyName,
          'cityName':cityName,
          'geo': resGeo
      })

    response.content_type = 'application/json;charset=utf-8'
    return dumps(res)


@app.get('/page/ElectionArea')
def electionAreaPage():
    prefectures = db.GetPrefecture()
    return template('electionArea', prefectures=prefectures).replace('\n', '');

###########################################
# Twitter関連
###########################################
@app.get('/login')
def login():
    callback_url = "https://" + os.environ['HTTP_HOST']  + os.path.dirname(os.environ['REQUEST_URI']) + '/auth'
    url,request_token = twitter_util.get_request_token(callback_url)

    session = request.environ.get('beaker.session')
    session['request_token'] = request_token
    session.save()

    redirect(url)

@app.get('/auth')
def auth():
    session = request.environ.get('beaker.session')
    if not session.has_key('request_token'):
      url = 'https://' + os.environ['HTTP_HOST'] + '/' + os.path.dirname(os.environ['REQUEST_URI']) + '/login'
      redirect(url)
      return
    request_token = session['request_token']
    try:
        access_token = twitter_util.get_access_token(request.query.oauth_token, request.query.oauth_verifier)
        session['access_token'] = access_token
        session.save()
        return session['access_token']
    except Exception, e:
        return e

@app.get('/logout')
def logout():
    session = request.environ.get('beaker.session')
    session.delete()
    return 'logout...'

