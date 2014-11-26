# coding=utf-8
from simplefw import Controller 
import cgi
import os
import re
import json
from election_db import ElectionDb
from rdp import rdp
import math

class SearchElectionArea(Controller):
  def index(self):
    print "Content-type: text/html\n"
    dbname = './election.sqlite'
    db = ElectionDb(dbname)
    prefectures = db.GetPrefecture()

    tmpl = self.template_loader.load('template/SearchElectionArea.tmpl')
    stream = tmpl.generate(data = prefectures)
    html = stream.render('html')
    print html

