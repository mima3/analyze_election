# coding=utf-8
from bottle import get, post, template, request, Bottle, response
from json import dumps
from election_db import ElectionDb

app = Bottle()
dbpath = './election.sqlite'
db = ElectionDb(dbpath)

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

#if __name__ == '__main__':
#    run(host='localhost', port=8080)
