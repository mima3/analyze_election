# coding=utf-8
from bottle import get, post, template, request, Bottle, response, redirect
from json import dumps
from election_db import ElectionDb
from twitter_utility import TwitterUtility
import os
import json
import math

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
    electionId = request.query.electionId
    ret = db.GetElectionAreaInformation(electionArea)
    area_res = []
    for r in ret:
      prefectureName = r[2]
      subPrefectureName = r[3]
      countyName = r[4]
      cityName = r[5]
      retGeo = db.GetCityGeo(prefectureName, subPrefectureName, countyName, cityName)
      resGeo = convertGeoResult(retGeo)
      area_res.append({
          'key':r[0],
          'notes':r[1],
          'prefectureName':prefectureName,
          'subPrefectureName':subPrefectureName,
          'countyName':countyName,
          'cityName':cityName,
          'geo': resGeo
      })
    candidate = []
    ret = db.GetCandidate(electionId, electionArea)
    for r in ret:
        candidate.append({
            'name': r[0],
            'age': r[1],
            'party': r[2],
            'status': r[3],
            'twitter': r[4],
            'facebook': r[5],
            'homepage': r[6],
        })

    res = {
        'area' : area_res,
        'candidate' : candidate
    }
    response.content_type = 'application/json;charset=utf-8'
    return dumps(res)


@app.get('/')
def homePage():
    return template('home').replace('\n', '');


@app.get('/page/ElectionArea/<electionId>')
def electionAreaPage(electionId):
    prefectures = db.GetPrefecture()
    return template('electionArea', prefectures=prefectures, electionId=electionId).replace('\n', '');


@app.get('/page/dondt')
def electionAreaPage():
    prefectures = db.GetPrefecture()
    return template('dondt', prefectures=prefectures).replace('\n', '');


@app.get('/page/nicolive/<nicoliveId>')
def nicoLivePage(nicoliveId):
    return template('nicolive', nicoliveId=nicoliveId).replace('\n', '');


def representsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

@app.get('/json/get_nicolive_comment/<nicoliveId>')
def getNicoLiveComment(nicoliveId):
    limit = 20
    page = int(request.query.page)
    offset = limit * (page-1)
    filters = []
    filter_user_id = ''
    filter_premium = ''
    filter_content = ''
    filter_mail = ''
    filter_score_lt = ''
    if (request.query.filters):
        filters = json.loads(request.query.filters)
        for rule in filters['rules']:
            if (rule['field'] == 'user_id'):
                filter_user_id = rule['data']
            if (rule['field'] == 'premium'):
                filter_premium = rule['data']
            if (rule['field'] == 'content'):
                filter_content = rule['data']
            if (rule['field'] == 'mail'):
                filter_mail = rule['data']
            if (rule['field'] == 'score' and representsInt(rule['data'])):
                filter_score_lt = rule['data']
    path = os.path.dirname(__file__) + '/niconico/' + nicoliveId + '.json'
    f = open(path, 'r')
    json_data = json.load(f)
    f.close()
    rows = []
    i = 0
    rowcnt = 0
    for data in json_data:
        premium = ''
        score = ''
        mail = ''
        if 'premium' in data:
            premium = data['premium']
        if 'score' in data:
            score = data['score']
        if 'mail' in data:
            mail = data['mail']

        if filter_user_id:
            if filter_user_id != data['user_id']:
                continue
        if filter_mail:
            if str(filter_mail) != str(mail):
                continue

        if filter_premium:
            if str(filter_premium) != str(premium):
                continue
        if filter_content:
            if data['content'].find(filter_content) == -1:
                continue

        if filter_score_lt:
            if not representsInt(score):
                continue
            if int(filter_score_lt) <= int(score):
                continue

        if rowcnt < limit and offset <= i:
            cells = [
                data['user_id'], 
                premium,
                data['content'],
                data['vpos'],
                score, 
                mail
            ]
            row = {'id':i, 'cell': cells}
            rowcnt += 1
            rows.append(row)
        i += 1
    res = {'page' : page, 'total': math.ceil(float(i)/limit), 'records' : i, 'rows' : rows}
    response.content_type = 'application/json;charset=utf-8'
    return dumps(res)


@app.get('/page/analyzehp/<year>')
def analyzeHpPage(year):
    path = ('%s/script_comp_manifesto/party_hp_json_%s.json' % (os.path.dirname(__file__), year))

    f = open(path, 'r')
    party_data = json.load(f)
    f.close()

    path = ('%s/script_comp_manifesto/party_hp_result_%s.json' % (os.path.dirname(__file__), year))
    f = open(path, 'r')
    party_result_data = json.load(f)
    f.close()

    return template('analyzehp', year=year, party_data=party_data, party_result_data=party_result_data).replace('\n', '');


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

