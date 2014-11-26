#!C:\Python27\python.exe
# coding: utf-8
# #!/usr/bin/env -S LD_LIBRARY_PATH=/home/needtec/usr/local/lib:/home/needtec/local/lib /usr/local/bin/python
#import site
#site.addsitedir('C:\\Python27\\Lib\\site-packages')
from bottle import run
import ConfigParser
import sys
conf = ConfigParser.SafeConfigParser()
conf.read("serif.ini")
try:
  i = 0
  path = conf.get('system', 'path' + str(i))
  while path != "":
    i = i + 1
    sys.path.append(path)
    path = conf.get('system', 'path' + str(i))
except ConfigParser.NoOptionError as e:
  pass

from application import app

run(app, server='cgi')
