# coding=utf-8
from simplefw import Controller 
import cgi
import os
import re
import json
from election_db import ElectionDb
from rdp import rdp
import math

class GetElectionArea(Controller):
  def index(self):
    form = cgi.FieldStorage()
    print ("Content-Type: application/json;charset=utf-8\n")
    dbname = './election.sqlite'
    db = ElectionDb(dbname)
    prefectureName = form['prefectureName'].value
    subPrefectureName = ''
    countryName = ''
    cityName = ''
    if form.has_key('subPrefectureName'):
        subPrefectureName = form['subPrefectureName'].value
    if form.has_key('countryName'):
        countryName = form['countryName'].value
    if form.has_key('cityName'):
        cityName = form['cityName'].value
    ret = db.GetElectionArea(prefectureName, subPrefectureName, countryName, cityName)
    res = []
    for r in ret:
        res.append({'key': r[0], 'notes':r[1]})
    print (json.dumps(res))

