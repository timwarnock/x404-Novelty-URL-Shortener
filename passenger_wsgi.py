# -*- coding: UTF-8 -*-
import sys, os
INTERP = os.path.join(os.environ['HOME'], 'xn--1nr.cc', 'bin', 'python')
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)
sys.path.append(os.getcwd())



from flask import Flask
from flask import request
application = Flask(__name__)

from x404 import NovelNum


# main page
@application.route('/')
def index():
	helloWorld = u'Hello 去 %s' % (NovelNum.anglosaxon)
	return helloWorld

# x404
@application.errorhandler(404)
def not_found(e):
    res = u' 去 %s' % (request.path,)
    return res

