#!/usr/bin/env python
# vim: set fileencoding=utf-8 tabstop=4 shiftwidth=4 autoindent smartindent:
import logging, os, sys, unittest

## parent directory
sys.path.insert(0, os.path.join( os.path.dirname(__file__), '..' ))
import NovelNum


class test_NovelNum(unittest.TestCase):

    def setUp(self):
        self.nn = NovelNum.NovelNum()

    def tearDown(self):
        pass
    
    def test_top16len(self):
        self.assertEqual( len(self.nn.C_SETS['top16']), 16 )

    def test_encode(self):
        res = self.nn.encode(2468480)
        self.assertEqual( res['top16'], 'fhnnlm' )
        self.assertEqual( res['base62'], '-cama' )
        self.assertEqual( res['anglosaxon'], u'ᚠᚳᚷᛉᚩ' )
        self.assertEqual( res['greek'], u'δγωΛ' )
        self.assertEqual( res['CJK'], u'袎乵' )
        self.assertEqual( res['hangul'], u'홬곜' )
        self.assertEqual( res['yijing'], u'䷎䷻䷶䷉' )
        self.assertEqual( res['dingbats'], u'➻❾❃' )
        self.assertEqual( res['braile'], u'⣻⢾⢃' )
        self.assertEqual( res['alchemical'], u'🜅🝋🝇🜁' )

    def test_decodeAlphas(self):
        self.assertEqual( self.nn.decode('cama'), 53972)
        self.assertEqual( self.nn.decode('cam'), 724)
        self.assertEqual( self.nn.decode('ca'), 212)
        self.assertEqual( self.nn.decode('c'), 4)
        self.assertEqual( self.nn.decode('-c'), 12)
        self.assertEqual( self.nn.decode('Cama'), 2468506)
        self.assertEqual( self.nn.decode('Cam'), 85226)
        self.assertEqual( self.nn.decode('Ca'), 658)
        self.assertEqual( self.nn.decode('C'), 38)

    def test_decodeSmall(self):
        self.assertEqual( self.nn.decode(u'w'), 1)
        self.assertEqual( self.nn.decode(u'1'), 1)
        self.assertEqual( self.nn.decode(u'丁'), 1)
        self.assertEqual( self.nn.decode(u'각'), 1)
        self.assertEqual( self.nn.decode(u'䷁'), 1)
        self.assertEqual( self.nn.decode(u'ᚢ'), 1)
        self.assertEqual( self.nn.decode(u'✁'), 1)
        self.assertEqual( self.nn.decode(u'α'), 1)
        self.assertEqual( self.nn.decode(u'⡁'), 1)
        self.assertEqual( self.nn.decode(u'🜁'), 1)

    def test_decodeHuge(self):
        self.assertEqual( self.nn.decode(u'frflhllhuutrucul'), 5999777888333222000)
        self.assertEqual( self.nn.decode(u'WfJg2iS2d97'), 5999777888333222000)
        self.assertEqual( self.nn.decode(u'琌螈蘡倸丟'), 5999777888333222000)
        self.assertEqual( self.nn.decode(u'욓퇋챈럙궁'), 5999777888333222000)
        self.assertEqual( self.nn.decode(u'䷸䷟䷁䷓䷭䷭䷕䷝䷰䷅䷆'), 5999777888333222000)
        self.assertEqual( self.nn.decode(u'ΑΖξΜΩΥΙΔλεΞα'), 5999777888333222000)
        self.assertEqual( self.nn.decode(u'ᚷᚢᛏᛏᚾᚣᚣᛠᛡᚱᛟᛡᛏ'), 5999777888333222000)
        self.assertEqual( self.nn.decode(u'➷➭➸➰❓✭➾❉✃'), 5999777888333222000)
        self.assertEqual( self.nn.decode(u'⣷⣭⣸⣰⢓⡭⣾⢉⡃'), 5999777888333222000)
        self.assertEqual( self.nn.decode(u'🜣🜐🝆🝩🜢🜿🜬🜏🝑🜁'), 5999777888333222000)

    def test_inout(self):
        self.assertEqual(123, self.nn.decode(self.nn.encode(123)['CJK']) )
        self.assertEqual(567123, self.nn.decode(self.nn.encode(567123)['anglosaxon']) )
        self.assertEqual(99123, self.nn.decode(self.nn.encode(99123)['top16']) )
        # check invalid numbers
        with self.assertRaises(TypeError):
            self.nn.encode('2')
        with self.assertRaises(TypeError):
            self.nn.encode(2.0)
        with self.assertRaises(ValueError):
            self.nn.encode(0)
        with self.assertRaises(ValueError):
            self.nn.encode(-1)

    def test_invalidunicode(self):
        with self.assertRaises(TypeError):
            self.nn.decode(2)
        with self.assertRaises(ValueError):
            self.nn.decode(u'#')
        with self.assertRaises(ValueError):
            self.nn.decode(u'丟!')

    def test_morebadunicode(self):
        with self.assertRaises(ValueError):
            self.nn.decode(u'x!x龍a')


if __name__ == '__main__':
    unittest.main()
