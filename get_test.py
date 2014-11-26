#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
from election_db import ElectionDb
from rdp import rdp
import math
import numpy as np
import time


def main(argvs, argc):
    dbname = './election.sqlite'
    db = ElectionDb(dbname)
    start = time.time()
    ret = db.GetPos(35.65858,139.445433)
    elapsed_time = time.time() - start
    print("elapsed_time:{0}".format(elapsed_time))
    print (ret)
    ret2 = db.GetElectionArea(ret['prefectureName'], ret['subPrefectureName'], ret['countyName'], ret['cityName'])
    print (ret2)
    for r in ret2:
      print r
    return 0

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    sys.exit(main(argvs, argc))
