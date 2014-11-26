# coding=utf-8
from simplefw import Controller 
import cgi
import os
import re
import json
from election_db import ElectionDb
from rdp import rdp
import math

class GetGeoToCity(Controller):
  def index(self):
    form = cgi.FieldStorage()
    print ("Content-Type: application/json;charset=utf-8\n")
    dbname = './election.sqlite'
    db = ElectionDb(dbname)

    lat = float(form['lat'].value)
    lng = float(form['lng'].value)

    ret = db.GetPos(lat, lng)
    print (json.dumps(ret))

