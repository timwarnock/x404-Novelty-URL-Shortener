# -*- coding: UTF-8 -*-
import sys, os
INTERP = os.path.join(os.environ['HOME'], 'xn--1nr.cc', 'bin', 'python')
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)
sys.path.append(os.getcwd())

from flask import Flask, jsonify, redirect, request, render_template
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
        data = {'anglos':u'ᚢᚱᛚ ᛋᚻᚩᚱᛏᛖᚾᛖᚱ', 'CJK':u'網址縮短'}
        return render_template('index.html', title=title, data=data)
    except Exception as e:
        if DEBUG:
            return '<pre>' + traceback.format_exc() + '</pre>'
        return redirect(u"https://avant.net", code=302)



# x404 get info on key
@application.route('/<string:key>/info')
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


# x404 get formkey json
@application.route('/__formkey__/')
def getFormKey():
    try:
        formkey = _PF.getFormKey()
        return jsonify({'formkey':formkey})
    except Exception as e:
        if DEBUG:
            return '<pre>' + traceback.format_exc() + '</pre>'
        return u'{}'


# x404 get psuedoform html|json object
@application.route('/__new__/', methods=['GET', 'POST', 'PUT'])
def handlePseudoForm():
    try:
        if request.method == 'POST':
            data = request.get_json()
            hs = _PF.addRequest(request.remote_addr, data.get('url'), data.get('formkey'))
            res = jsonify({'handshake':hs})
            if hs is None:
                res.status_code = 400
            return res
        elif request.method == 'PUT':
            data = request.get_json()
            encodings = _PF.commitRequest(request.remote_addr, data.get('return_handshake'), 1)
            if encodings is None:
                res.status_code = 412
            return jsonify({'encodings':encodings})
        formkey = _PF.getFormKey()
        data = {'anglos':u'ᚢᚱᛚ ᛋᚻᚩᚱᛏᛖᚾᛖᚱ', 'CJK':u'網址縮短'}
        return render_template('new.html', formkey=formkey, data=data)
    except Exception as e:
        if DEBUG:
            return '<pre>' + traceback.format_exc() + '</pre>'
        return u'{}'


# x404 redirector
# TODO template? or redirect somewhere else?
@application.route('/<key>')
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

