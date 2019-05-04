# -*- coding: UTF-8 -*-
import sys, os
INTERP = os.path.join(os.environ['HOME'], 'xn--1nr.cc', 'bin', 'python')
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)
sys.path.append(os.getcwd())

from flask import Flask, jsonify, redirect, render_template
application = Flask(__name__)

from urllib import unquote
import traceback
import x404


##
## gx404 globals
DEBUG = True
DBFILE = 'x404.db'
_SURL = x404.ShortURLDB.ShortURLDB(DBFILE)
_PF = x404.PseudoForm.PseudoForm(_SURL)


# urllib.unquote (python2) does not handle unicode properly
def _utf8(s):
    return unquote(str(s)).decode('utf8')


# main page
@application.route('/')
def index():
    try:
        title = u'去.cc'
        data = {'username':x404.NovelNum.anglosaxon}
        return render_template('index.html', title=title, data=data)
    except Exception as e:
        if DEBUG:
            return '<pre>' + traceback.format_exc() + '</pre>'
        return redirect(u"https://avant.net", code=302)



# x404 get info on key
@application.route('/<path:key>/info')
def getURLinfo(key):
    try:
        key = _utf8(key)
        surl = _SURL
        inf = surl.info(key)
        url = inf['url']
        rowid = inf['rowid']
        if url is None:
            res = u'info: %s is %d, no url found' % (key,rowid)
        else:
            res = render_template('info.html', key=key, 
                    rowid=rowid, url=url, 
                    encodings=inf['encodings'].values() )
        return res
    except Exception as e:
        if DEBUG:
            return '<pre>' + traceback.format_exc() + '</pre>'
        return redirect(u"https://去.cc", code=302)


# x404 get psuedoform html|json object
@application.route('/new.url', methods=['GET', 'POST', 'PUT'])
def getPseudoForm():
    try:
        formkey = _PF.getFormKey()
        if request.method == 'POST':
            hs = _PF.addRequest(request.remote_addr, request.form.get('url'), formkey)
            return jsonify({'handshake':hs})
        elif request.method == 'PUT':
            rowid = _PF.commitRequest(request.remote_addr, request.form.get('return_handshake')
            return jsonify({'id':rowid})
        return render_template('new.html', formkey=formkey)
    except Exception as e:
        if DEBUG:
            return '<pre>' + traceback.format_exc() + '</pre>'
        return u'{}'


# x404 redirector
# TODO template? or redirect somewhere else?
@application.route('/<path:key>')
def URLredirector(key):
    try:
        key = _utf8(key)
        surl = _SURL
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

