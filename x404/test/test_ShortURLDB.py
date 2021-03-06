#!/usr/bin/env python
# vim: set fileencoding=utf-8 tabstop=4 shiftwidth=4 autoindent smartindent:
import logging, os, sys, unittest

## parent directory
sys.path.insert(0, os.path.join( os.path.dirname(__file__), '..' ))
import ShortURLDB


class test_ShortURLDB(unittest.TestCase):

    def setUp(self):
        self.surl = ShortURLDB.ShortURLDB()

    def tearDown(self):
        pass
    
    def test_cr(self):
        self.surl._newdb()
        rowid = self.surl._insert('https://foobar.baz/random')
        self.assertEquals( self.surl._get(rowid), 'https://foobar.baz/random')
    
    def test_c(self):
        self.surl._newdb()
        self.assertEquals( self.surl._get(1), None )

    def test_crud(self):
        self.surl._newdb()
        rowid = self.surl._insert('https://foobar.baz/random')
        self.assertEquals( self.surl._get(rowid), 'https://foobar.baz/random')
        self.assertEquals( self.surl._edit(rowid,'https://foobar.baz/edited'), rowid)
        self.assertEquals( self.surl._get(rowid), 'https://foobar.baz/edited')
        self.assertTrue( self.surl._del(rowid) )
        self.assertEquals( self.surl._get(rowid), None )

    def test_crudl(self):
        self.surl._newdb()
        rows = self.surl._list()
        self.assertEquals( len(rows), 0)
        rowid1 = self.surl._insert('https://foobar.baz/1')
        rowid2 = self.surl._insert('https://foobar.baz/2')
        rows = self.surl._list()
        self.assertEquals( len(rows), 2)
        self.assertEquals( rows[0][1], 'https://foobar.baz/1')
        self.assertEquals( rows[1][1], 'https://foobar.baz/2')

    def test_loadURLs(self):
        self.surl._newdb()
        self.surl._loadURLs('urltest1good.txt')
        rows = self.surl._list()
        self.assertEquals( len(rows), 5)
        self.assertEquals( self.surl._get(3), 'https://avant.net/three')

    def test_loadURLsBAD(self):
        self.surl._newdb()
        self.surl._loadURLs('urltest2bad.txt')
        rows = self.surl._list()
        self.assertEquals( len(rows), 5)
        self.assertEquals( self.surl._get(3), 'https://avant.net/three')

    def test_badURLs(self):
        self.surl._newdb()
        ## check invalid URLs
        with self.assertRaises(TypeError):
            self.surl._insert(15)
        with self.assertRaises(ValueError):
            self.surl._insert('https:/what.com/missingslash')
        with self.assertRaises(ValueError):
            self.surl._insert('https://okaysofar.com/' + 'x'*4000)

    def test_badURLedits(self):
        self.surl._newdb()
        rowid = self.surl._insert('https://what.com/old')
        with self.assertRaises(TypeError):
            self.surl._edit(rowid, 15)
        with self.assertRaises(ValueError):
            self.surl._edit(rowid, 'https:/what.com/missingslash')
        with self.assertRaises(ValueError):
            self.surl._edit(rowid, 'https://okaysofar.com/' + 'x'*4000)
        self.assertEquals( self.surl._get(rowid), 'https://what.com/old')

    def test_resolve(self):
        self.surl._newdb()
        for i in range(1000):
            self.surl._insert('https://filler.com/nonsense/'+str(i))
        encodings = self.surl.add('https://what.com/test')
        self.assertEquals( self.surl.resolve(encodings['top16']), 'https://what.com/test')
        self.assertEquals( self.surl.resolve(encodings['base62']), 'https://what.com/test')
        self.assertEquals( self.surl.resolve(encodings['greek']), 'https://what.com/test')
        self.assertEquals( self.surl.resolve(encodings['hangul']), 'https://what.com/test')
        self.assertEquals( self.surl.resolve(encodings['CJK']), 'https://what.com/test')

    def test_list(self):
        self.surl._newdb()
        for i in range(1000):
            self.surl._insert('https://filler.com/nonsense/'+str(i))
        top16 = self.surl.list()
        self.assertEquals('w' , top16[0][1] )
        self.assertEquals('htu' , top16[999][1] )

    def test_listCJK(self):
        self.surl._newdb()
        for i in range(25000):
            self.surl._insert('https://filler.com/nonsense/'+str(i))
        CJK = self.surl.list('CJK')
        self.assertEquals(u'丁' , CJK[0][1] )
        self.assertEquals(u'凨' , CJK[999][1] )
        self.assertEquals(u'嶾丁' , CJK[24999][1] )

    def test_resolveNone(self):
        self.surl._newdb()
        self.assertEquals( self.surl.resolve('any'), None)

    def test_duckNone(self):
        self.surl._newdb()
        for i in range(55):
            self.surl.add('https://duckduckgo.com/')
        self.assertEquals( self.surl.resolve('du'), 'https://duckduckgo.com/')

    def test_info(self):
        self.surl._newdb()
        for i in range(16):
            self.surl.add('https://nonsense.org/')
        inf = self.surl.info('l')
        self.assertEquals( 'https://nonsense.org/', inf['url'] )
        self.assertEquals( 5, inf['rowid'] )
        self.assertEquals( u'l', inf['encodings']['top16'] )
        self.assertEquals( u'5', inf['encodings']['base62'] )
        self.assertEquals( u'丅', inf['encodings']['CJK'] )
        self.assertEquals( u'⡅', inf['encodings']['braile'] )
        self.assertEquals( u'γ', inf['encodings']['greek'] )


if __name__ == '__main__':
    unittest.main()
