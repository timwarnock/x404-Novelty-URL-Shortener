# -*- coding: UTF-8 -*-
import sys, os
INTERP = os.path.join(os.environ['HOME'], 'xn--1nr.cc', 'bin', 'python')
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)
sys.path.append(os.getcwd())

from flask import Flask, redirect
application = Flask(__name__)

from urllib import unquote
import traceback
import x404


##
## gx404 globals
DEBUG = True
DBFILE = 'x404.db'



# main page
@application.route('/')
def index():
    helloWorld = u'Hello 去 %s' % (x404.NovelNum.anglosaxon)
    return helloWorld


# x404
@application.route('/<path:key>')
def shorturl(key):
    try:
        ## fuck urllib.unquote for not handling a unicode string as ascii
        ## unicode is supposed to be backwards compatible with ascii
        key = unquote(str(key)).decode('utf8')
        surl = x404.ShortURLDB.ShortURLDB(DBFILE)
        url = surl.resolve(key)
        if url is not None:
            return redirect(url)
        nn = x404.NovelNum.NovelNum()
        rowid = nn.decode(key)
        res = u' 去 %s is %d, no url found' % (key,rowid)
        return res
    except Exception as e:
        if DEBUG:
            return '<pre>' + traceback.format_exc() + '</pre>'
        return redirect(u"https://去.cc", code=302)

