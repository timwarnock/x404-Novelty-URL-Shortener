#!/usr/bin/env python
# vim: set fileencoding=utf-8 tabstop=4 shiftwidth=4 autoindent smartindent:
''' Usage: x404.py command [options]

    Where command includes:
    add [url] * e.g., add http://www.anattatechnologies.com/
    get [key] * e.g., get esza (returns the matching url)
    del [key] * e.g., del esza (removes the matching entry)
    list      * lists all entries

'''
import os
import sys
import math
import sqlite3


def add_url(url):
  conn = sqlite3.connect("URLs.db")
  curs = conn.cursor()
  curs.execute("select count(rowid) from URLS")
  numrows = curs.fetchall()[0][0]
  short_url = getalpha(numrows)
  curs.execute("insert into URLS(short_url, long_url) values(?,?)",(short_url,url))
  conn.commit()
  conn.close()
  return short_url


'''
>>> urllib.quote(u'笫'.encode('utf8'))
'%E7%AC%AB'
>>> print urllib.unquote('%E7%AC%AB').decode('utf8')
笫
'''



def revb(n):
  min_digits = 1 + int(math.log(n,16))
  bit_size = 4 * min_digits
  bin_number = bin(n)
  reverse_number = bin_number[-1:1:-1]
  reverse_number = reverse_number + (bit_size - len(reverse_number))*'0'
  return int(reverse_number,2)


def mixb(n):
   min_digits = 1 + int(math.log(n,16))
   bit_size = 4 * min_digits
   bin_number = bin(n)
   reverse_number = bin_number[-1:1:-1]
   reverse_number = reverse_number + (bit_size - len(reverse_number))*'0'
   if reverse_number[0:2] == '00':
     reverse_number = '1' + reverse_number + '0'
   return int(reverse_number,2)


top16pos = 'fwmucldrhsnioate'
def num16alpha(num):
    chars = []
    while num > 0:
        num, d = divmod(num, 16)
        chars.append(top16pos[d])
    return ''.join(reversed(chars))


def getalpha(n):
  return num16alpha(mixb(n))






base62 = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
top16pos = 'etaoinshrdlcumwf'
hexc = '0123456789abcdef'
greek = u'ΑαΒβΓγΔδΕεΖζΗηΘθΙιΚκΛλΜμΝνΞξΟοΠπΡρΣσςΤτΥυΦφΧχΨψΩω'
greekU = u'ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ'
greekL = u'αβγδεζηθικλμνξοπρστυφχψω'
anglos = u'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'
base10 = '3147592068'



def numc(num,cset):
    chars = []
    while num > 0:
        num, d = divmod(num, len(cset))
        chars.append(cset[d])
    #return ''.join(reversed(chars))
    return ''.join(chars)

def numuc(num,ustart,uend):
    chars = []
    while num > 0:
        num, d = divmod(num, uend-ustart)
        chars.append(unichr(ustart+d))
    #return ''.join(reversed(chars))
    return ''.join(chars)

def revuc(ucnum,ustart,uend):
  base = uend-ustart
  basem = 1
  n = 0
  #for c in unicode(ucnum,"utf8")[::-1]:
  for c in unicode(ucnum,"utf8"):
    n += (ord(c)-ustart) * basem
    basem = basem*base
  return n

def revc(ucnum,cset):
  base = len(cset)
  basem = 1
  n = 0
  #for c in unicode(ucnum,"utf8")[::-1]:
  for c in unicode(ucnum,"utf8"):
    n += (cset.index(c)) * basem
    basem = basem*base
  return n


def is_top16pos(ctest):
  for c in ctest:
    if c not in top16pos:
      return False
  return True

def num2alphanum(num):
  res = numc(num,base62)
  if is_top16pos(res):
    res = '_' + res
  return res


def alphacollisions(nmax,nmin=1):
  c = {}
  for i in range(nmin,nmax):
    a = num2alphanum(i)
    print i, "=", a
    if '_' in a:
      c[i] = a
  for i,a in c.iteritems():
    print i, a, numc(i,top16pos)
  print "there were %s collisions out of %d" % (len(c), nmax-nmin)


def samples(num=1, ninc=1, hostname="avant.net"):
 for n in range(num,ninc+num):
  print "http://%s/%s" % (hostname, n) # base-10
  print "http://%s/%s" % (hostname, numc(n,top16pos)) # top16
  print "http://%s/%s" % (hostname, numc(n,base62)) # alphanum
  print "http://%s/%s" % (hostname, numuc(n,int('4e00',16),int('9fea',16))) # Chinese
  print "http://%s/%s" % (hostname, numuc(n,int('ac00',16),int('d7a3',16))) # Hangul
  #print "http://%s/%s" % (hostname, numuc(n,int('4dc0',16),int('4dff',16))) # yijing
  print "http://%s/%s" % (hostname, numc(n,greek)) # greek
  print "http://%s/%s" % (hostname, numc(n,anglos)) # anglo-saxon
  #print "http://%s/%s" % (hostname, numuc(n,int('16a0',16),int('16ea',16))) # runic
  print "http://%s/%s" % (hostname, numuc(n,int('2700',16),int('27bf',16))) # dingbats
  print "http://%s/%s" % (hostname, numuc(n,int('2840',16),int('28ff',16))) # 8-dot braile
  print "http://%s/%s" % (hostname, numuc(n,int('1f700',16),int('1f773',16))) # alchemical
  print "-"
  time.sleep(0.5)


'''
is there a collision? where is first collision?
Let's find out :)
'''

top64pos = 'etaoinshrdlcumwfgypbvkjxqz0123456789-_ETAOINSHRDLCUMWFGYPBVKJXQZ'
def num64alpha(num):
    chars = []
    while num > 0:
        num, d = divmod(num, 64)
        chars.append(top64pos[d])
    return ''.join(reversed(chars))


def geta64(rmax,rmin=1):
  c = {}
  for i in range(rmin,rmax):
    min_digits = 1 + int(math.log(i,64))
    bit_size = 6 * min_digits
    def geta(n):
      return num64alpha(mixb(n))
    ''' ok '''
    print i, geta(i), "min_digits", min_digits, "bit_size", bit_size
    if geta(i) in c:
      print "COLLISION AT", geta(i), i, "=",c[geta(i)]
      break
    else:
      c[geta(i)] = i


def geta16(rmax,rmin=1):
  c = {}
  for i in range(rmin,rmax):
    min_digits = 1 + int(math.log(i,16))
    bit_size = 4 * min_digits
    def geta(n):
      return num16alpha(mixb(n))
    ''' ok '''
    print i, geta(i), "min_digits", min_digits, "bit_size", bit_size
    if geta(i) in c:
      print "COLLISION AT", geta(i), i, "=",c[geta(i)]
      break
    else:
      c[geta(i)] = i


def getan(rmax,rmin=1):
  c = {}
  def mixb(num):
    base10 = '0314759268'
    chars = []
    while num > 0:
      num, d = divmod(num, 10)
      chars.append(base10[d])
    alphs = ''.join(reversed(chars))
    # return alphs
    lena = len(alphs)
    return alphs[lena/2:] + alphs[:lena/2]
  for i in range(rmin,rmax):
    enc_i = i # int(mixb(i))
    test = mixb(i) # ''.join(reversed(mixb(i))) # numc(enc_i,top16pos)
    print i, test, numc(i,top16pos), numuc(i,int('4e00',16),int('9fea',16)), numc(i,anglos)
    if test in c:
      print "COLLISION AT", test, i, "=",c[test]
      break
    else:
      c[test] = i




if __name__ == '__main__':
  ''' optparse? '''
  if len(sys.argv) > 2 and sys.argv[1] == "add":
    short_url = add_url(sys.argv[2])
    while os.path.exists("../%s" % (short_url)):
      print >> sys.stderr, "%s already exists and won't cause a 404" % (short_url)
      short_url = add_url(sys.argv[2])
    print "SUCCESS\nhttp://avant.net/%s" % (short_url)
      




