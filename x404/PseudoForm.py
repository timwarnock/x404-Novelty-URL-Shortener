#!/usr/bin/env python
# vim: set fileencoding=utf-8 tabstop=4 shiftwidth=4 autoindent smartindent:
''' PseudoForm

    Manages the PseudoForm backend for the x404 Novel URL Shortener
    The PseudoForm is a bot-resistent alternative to a standard web form

    >>> pf = PseudoForm(ShortURLDB('x404.db'))
    >>> key = pf.getFormKey
    >>> len(key)
    38
    >>> pf.isValidFormKey(key)
    True
    >>> handshake = pf.addRequest('192.168.1.1', 'https://example.com', key)
    >>> len(handshake)
    64

    The client must compute the "return_handshake" via sha256(ip+handshake)

    >>> pf.commitRequest('192.168.1.1', return_handshake)
    123
    
    The URL is now saved to ShortURLDB and available for redirect

'''
import time
import hashlib
#TODO ConfigParser (for secretkey)
SECRET = u'secret龍key'


class PseudoForm:
    '''

    '''

    def __init__(self, surl):
        self.surl = surl
        self._initdb()

    def _initdb(self):
        curs = self.surl.db.cursor()
        curs.execute('CREATE TABLE IF NOT EXISTS url_requests(ip INT UNIQUE PRIMARY KEY, url TEXT, hs TEXT, ts REAL)')
        curs.execute('CREATE INDEX IF NOt EXISTS idx_url_requests_ts ON url_requests(ts)')
        self.surl.db.commit()
        curs.close()

    def getFormKey(self, ts=int(time.time()), divsec=300):
        ''' return a time-sensitive hash that can be 
            calculated at a later date to dermine if it matches

            can return previous hashes based on divsec increments
            the hash will change every divsec seconds (on the clock)
            e.g., divsec=300, every 5-minutes the hash will change
        '''
        return hashlib.sha1((self._unicode(ts/divsec)+SECRET).encode('utf-8')).hexdigest()[2:]

    def isValidFormKey(self, testkey, lookback=2, divsec=300):
        ''' return True IFF
            the testkey matches a hash for this or previous {lookback} iterations
            e.g., divsec=300, a formkey will be valid for at least 5 minutes (no less than 10)
            e.g., lookback=6, a formkey will valid for at least 25 minutes (no less than 30)
        '''
        for i in range(lookback):
            if testkey == self.getFormKey(int(time.time())-divsec*i):
                return True
        return False

    def addRequest(self, ip, url, formkey):
        ''' persist the request
            IFF ip is valid
                url is valid
                formkey is valid
            return handshake
        '''
        ipnum = self._is_good_ip(ip)
        handshake = None
        if (
            ipnum is not None
            and self.isValidFormKey(formkey)
            and self._is_good_url(url)
        ):
            (handshake, rhs) = self._get_handshakes(ip)
            curs = self.surl.db.cursor()
            curs.execute('DELETE FROM url_requests WHERE ip=?',(ipnum,))
            curs.execute('INSERT INTO url_requests(ip,url,hs,ts) VALUES(?,?,?,?)',(ipnum,url,rhs,time.time()))
            self.surl.db.commit()
            curs.close()
        return handshake

    def _is_good_url(self, url):
        ''' same as ShortURLDB except swallow the error '''
        try:
            return self.surl._is_good_url(url)
        except:
            return False

    def getRequest(self, ip, delete=False, maxtime=10):
        ''' retrieve the previous request (by ip) or None
            delete old requests, and optionally delete the current request
        '''
        ipnum = self._is_good_ip(ip)
        res = None
        if ipnum is not None:
            curs = self.surl.db.cursor()
            curs.execute('DELETE FROM url_requests WHERE ts < ?',(time.time()-maxtime,))
            rows = self.surl.db.execute('SELECT url,hs,ts FROM url_requests WHERE ip=?',(ipnum,))
            row = rows.fetchone()
            if row is not None:
                res = { 'url': row[0],
                        'return_handshake': row[1],
                        'ts_delta': time.time()-row[2] }
                if delete:
                    curs.execute('DELETE FROM url_requests WHERE ip=?',(self._ip2int(ip),))
                    self.surl.db.commit()
            rows.close()
            curs.close()
        return res

    def commitRequest(self, ip, rhs, mintime=1, maxtime=10):
        ''' commit the request IFF
            the time difference tdelta is mintime > tdelta < maxtime

            return rowid within the ShortURLDB
        '''
        req = self.getRequest(ip, True, maxtime)
        rowid = None
        if (
            req is not None 
            and req['return_handshake'] == rhs
            and req['ts_delta'] < maxtime
            and req['ts_delta'] > mintime
        ):
            rowid = self.surl._insert(req['url'])
        return rowid

    def _get_handshakes(self, ip):
        handshake = hashlib.sha256(str(time.time())+ip).hexdigest()
        r_handshake = self._expected_return_handshake(ip, handshake)
        return (handshake, r_handshake)

    def _expected_return_handshake(self, ip, handshake):
        return hashlib.sha256(ip+handshake).hexdigest()

    def _is_good_ip(self, ip):
        try:
            return self._ip2int(ip)
        except:
            return None

    def _ip2int(self, s_ip):
        lst = [int(item) for item in s_ip.split('.')]
        int_ip = lst[3] | lst[2] << 8 | lst[1] << 16 | lst[0] << 24
        return int_ip

    def _int2ip(self, int_ip):
        lst = []
        for i in xrange(4):
            shift_n = 8 * i
            lst.insert(0, str((int_ip >> shift_n) & 0xff))
        return ".".join(lst)

    def _unicode(self, s):
        if isinstance(s, str):
            return unicode(s,"utf8")
        elif isinstance(s, unicode):
            return s
        elif isinstance(s, int):
            return unicode(str(s),"utf8")
        raise TypeError("Invalid unicode")
