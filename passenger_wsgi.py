# -*- coding: UTF-8 -*-
import sys, os
INTERP = os.path.join(os.environ['HOME'], 'xn--1nr.cc', 'bin', 'python')
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)
sys.path.append(os.getcwd())



from flask import Flask
application = Flask(__name__)

from x404 import NovelNum



@application.route('/')
def index():
	helloWorld = u'Hello 去 %s' % (NovelNum.anglosaxon)
	return helloWorld
