#!/usr/bin/env python
# vim: set tabstop=4 shiftwidth=4 autoindent smartindent:
import logging, os, sys, unittest

## parent directory
sys.path.insert(0, os.path.join( os.path.dirname(__file__), '..' ))
import NovelNum


class test_NovelNum(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass
	
	def test_alpha16(self):
		self.assertEqual( len(NovelNum.top16pos), 16 )



if __name__ == '__main__':
	unittest.main()
