#!/usr/bin/env python
# vim: set fileencoding=utf-8 tabstop=4 shiftwidth=4 autoindent smartindent:
''' ShortURLDB module

    Manages storage for the x404 Novelty URL Shortener

    >>> surl = ShortURLDB('x404.sqlite')
    >>> encodings = surl.add('https://www.duckduckgo.com/')
    >>> encodings['top16']
    u'dd'
    >>> encodings['base62']
    u'E1'
    >>> surl.resolve('dd')
    u'https://www.duckduckgo.com/'
    >>> surl.resolve('E1')
    u'https://www.duckduckgo.com/'
    >>> 

'''

import sqlite3
import NovelNum


class ShortURLDB:
    '''

    '''

    def __init__(self, dbfile = None):
        if dbfile is None:
            self.db = sqlite3.connect(':memory:')
        else:
            self.db = sqlite3.connect(dbfile)

    def _newdb(self):
        curs = self.db.cursor()
        curs.execute('DROP TABLE IF EXISTS urls')
        curs.execute('CREATE TABLE urls(url TEXT)')
        self.db.commit()
        curs.close()

    def _loadURLs(self, urlfile):
        with open(urlfile) as f:
            for line in f:
                try:
                    self._insert(line.strip())
                except:
                    pass

    def resolve(self, key):
        ''' resolve the NovelNum key and return the full URL
        '''
        nn = NovelNum.NovelNum()
        return self._get(nn.decode(key))

    def add(self, url):
        ''' insert a new URL and return all NovelNum encodings
            for the newly inserted URL.
        ''' 
        nn = NovelNum.NovelNum()
        rowid = self._insert(url)
        return nn.encode(rowid)

    def _is_good_url(self, url):
        if isinstance(url, int):
            raise TypeError("URL cannot be a number")
        if len(url) > 2048 or not (url.startswith('http://') or url.startswith('https://')):
            raise ValueError("{!r} is not a valid URL".format(url))
        return True

    def _get(self, rowid):
        try:
            curs = self.db.execute('SELECT url FROM urls WHERE rowid=?',(rowid,))
            url = curs.fetchall()[0][0]
            curs.close()
            return url
        except IndexError:
            return None

    def _list(self):
        reslist = []
        curs = self.db.execute('SELECT rowid,url FROM urls')
        reslist = curs.fetchall()
        curs.close()
        return reslist

    def _insert(self, url):
        self._is_good_url(url)
        curs = self.db.cursor()
        curs.execute('INSERT INTO urls(url) VALUES (?)', (url,))
        retval = curs.lastrowid
        self.db.commit()
        curs.close()
        return retval

    def _edit(self, rowid, url):
        self._is_good_url(url)
        curs = self.db.cursor()
        curs.execute('UPDATE urls SET url=? WHERE rowid=?', (url,rowid))
        retval = rowid
        self.db.commit()
        curs.close()
        return retval

    def _del(self, rowid):
        curs = self.db.cursor()
        curs.execute('DELETE FROM urls WHERE rowid=?', (rowid,))
        self.db.commit()
        curs.close()
        return True


if __name__ == '__main__':
    ''' optparse? '''
    print ""  




