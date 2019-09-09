#!/usr/bin/env python
# vim: set fileencoding=utf-8 tabstop=4 shiftwidth=4 autoindent smartindent:
import logging, os, sys, unittest
import time

## parent directory
sys.path.insert(0, os.path.join( os.path.dirname(__file__), '..' ))
import PseudoForm
import ShortURLDB


class test_PseudoForm(unittest.TestCase):

    def setUp(self):
        self.pf = PseudoForm.PseudoForm(ShortURLDB.ShortURLDB())

    def tearDown(self):
        pass

    def test_secret(self):
        self.assertEqual( len(self.pf.secret), 36 )

    def test_secretfile(self):
        pf = PseudoForm.PseudoForm(ShortURLDB.ShortURLDB(), "test.config")
        self.assertEqual( pf.secret, 'secret秘密龍key')

    def test_secretnofile(self):
        pf = PseudoForm.PseudoForm(ShortURLDB.ShortURLDB(), "nosuch.config")
        self.assertNotEqual( pf.secret, 'secret秘密龍key')
        self.assertEqual( len(self.pf.secret), 36 )
    
    def test_getFormKey(self):
        self.assertEqual( len(self.pf.getFormKey()), 38 )

    def test_isValidFormKey(self):
        fkey = self.pf.getFormKey()
        self.assertTrue( self.pf.isValidFormKey(fkey) )

    def test_badFormKey(self):
        fkey = self.pf.getFormKey()
        self.assertFalse( self.pf.isValidFormKey('x' + fkey[1:]))

    def test_oldFormKey(self):
        fkey = self.pf.getFormKey(int(time.time()-258))
        self.assertTrue( self.pf.isValidFormKey(fkey) )
        fkey = self.pf.getFormKey(int(time.time()-600))
        self.assertFalse( self.pf.isValidFormKey(fkey) )

    def test_addRequest(self):
        handshake = self.pf.addRequest('192.168.1.1', 'https://nonsense.com/', self.pf.getFormKey())
        self.assertEqual( len(handshake), 64 )

    def test_BADaddRequest(self):
        handshake = self.pf.addRequest('192.168.1', 'https://nonsense.com/', self.pf.getFormKey())
        self.assertEqual( handshake, None )
        handshake = self.pf.addRequest('192.168.1.1', 'https:/nonsense.com/', self.pf.getFormKey())
        self.assertEqual( handshake, None )
        handshake = self.pf.addRequest('192.168.1.1', 'https://good', self.pf.getFormKey(int(time.time()-600)))
        self.assertEqual( handshake, None )

    def test_getRequest(self):
        self.pf.addRequest('192.168.1.1', 'https://nonsense.com/', self.pf.getFormKey())
        res = self.pf.getRequest('192.168.1.1')
        self.assertEqual(res['url'], 'https://nonsense.com/')
        self.assertTrue(res['ts_delta'] < 0.1)
        self.assertEqual(len(res['return_handshake']), 64)

    def test_commitRequest(self):
        handshake = self.pf.addRequest('192.168.1.1', 'https://nonsense.com/', self.pf.getFormKey())
        return_handshake = self.pf._expected_return_handshake(handshake)
        enc = self.pf.commitRequest('192.168.1.1', return_handshake, 0)
        req = self.pf.getRequest('192.168.1.1')
        self.assertEqual(req, None)
        self.assertEqual(self.pf.surl.resolve(enc['CJK']), 'https://nonsense.com/')

    def test_BADcommitRequest(self):
        handshake = self.pf.addRequest('192.168.1.1', 'https://nonsense.com/', self.pf.getFormKey())
        enc = self.pf.commitRequest('192.168.1.1', 'bad return handshake')
        req = self.pf.getRequest('192.168.1.1')
        self.assertEqual(req, None)
        self.assertEqual(enc, None)

    def test_LATEcommitRequest(self):
        handshake = self.pf.addRequest('192.168.1.1', 'https://nonsense.com/', self.pf.getFormKey())
        return_handshake = self.pf._expected_return_handshake(handshake)
        enc = self.pf.commitRequest('192.168.1.1', return_handshake)
        req = self.pf.getRequest('192.168.1.1')
        self.assertEqual(req, None)
        self.assertEqual(enc, None)

    def test_cleanup(self):
        db = self.pf.surl.db
        curs = db.execute('INSERT INTO url_requests(IP, URL, ts) VALUES (?, ?, ?)', (
                    self.pf._ip2int('192.168.1.1'),'https://nonsense.com', time.time() - 10))
        db.commit()
        self.assertEqual(self.pf.getRequest('192.168.1.1'), None)

    def test__ip2int(self):
        self.assertEqual(self.pf._ip2int('255.255.255.255'), 4294967295)
        self.assertEqual(self.pf._ip2int('0.0.0.5'), 5)

    def test__int2ip(self):
        self.assertEqual(self.pf._int2ip(4294967295), '255.255.255.255')
        self.assertEqual(self.pf._int2ip(5), '0.0.0.5')


if __name__ == '__main__':
    unittest.main()

