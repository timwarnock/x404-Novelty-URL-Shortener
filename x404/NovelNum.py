#!/usr/bin/env python
# vim: set fileencoding=utf-8 tabstop=4 shiftwidth=4 autoindent smartindent:
''' NovelNum module

    maps positive integers to encoded unicode character sets, e.g.,

    >>> nn = NovelNum()
    >>> bases = nn.encode(420)
    >>> print bases['top16']
    cnw
    >>> print bases['CJK']
    侤
    >>> print bases['anglosaxon']
    ᛉᛉ
    >>> 

    Can also decode a previously encoded result, e.g.,

    >>> nn = NovelNum()
    >>> nn.decode('cnw')
    420
    >>> nn.decode(u'侤')
    420
    >>> nn.decode(u'ᛉᛉ')
    420
    >>> 

    The above functionality is used for the x404 Novelty URL Shortener

'''


#
# define static numeric character sets, from left-to-right
# e.g., base8 = '0123456789abcdef'
top16 = 'fwmucldrhsnioate'
base62 = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
greek = u'ΑαΒβΓγΔδΕεΖζΗηΘθΙιΚκΛλΜμΝνΞξΟοΠπΡρΣσςΤτΥυΦφΧχΨψΩω'
greekU = u'ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ'
greekL = u'αβγδεζηθικλμνξοπρστυφχψω'
anglosaxon = u'ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛄᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ'

C_SETS = {
    "top16": top16,
    "base62": base62,
    "greek": greek,
    "anglosaxon": anglosaxon,
}

#
# define named unicode ranges of printable characters
# use the followign format:
#       "name" : (unicode_start, unicode_end)
#       where unicode_start and unicode_end are int
# e.g., "lowercase" : (97, 122)
U_SETS = {
    "CJK"       : (int('4e00',16),int('9fea',16)),
    "hangul"    : (int('ac00',16),int('d7a3',16)),
    "yijing"    : (int('4dc0',16),int('4dff',16)),
    #"runic"     : (int('16a0',16),int('16ea',16)),
    "dingbats"  : (int('2700',16),int('27bf',16)),
    "braile"    : (int('2840',16),int('28ff',16)),
    "alchemical": (int('1f700',16),int('1f773',16)),
}


class NovelNum:
    '''

    '''

    def __init__(self):
        self.C_SETS = C_SETS
        self.U_SETS = U_SETS

    def encode(self, n):
        '''
            returns a dict with encoded values for the number n
        '''
        encodings = {}
        for type, cset in self.C_SETS.iteritems():
            encodings[type] = self.encodeByType(n, type)
        for type, (ustart,uend) in self.U_SETS.iteritems():
            encodings[type] = self.encodeByType(n, type)
        return encodings

    def encodeByType(self, n, type):
        ''' returns the encoded number (by type)
            e.g., 
            >>> nn.encodeByType(123,'base62')
            u'Z1'
            >>> 
        ''' 
        if not isinstance(n, int):
            raise TypeError("You can only encode integers")
        if n <= 0:
            raise ValueError("You can only encode positive integers")
        if type in self.C_SETS:
            nstr = self._encode_cset(n, self.C_SETS[type])
            ## differentiate top16 and base62 if they collide
            if type == 'base62' and all(c in self.C_SETS['top16'] for c in nstr):
                nstr = u'-' + nstr
            return nstr
        if type in self.U_SETS:
            return self._encode_uset(n, self.U_SETS[type][0], self.U_SETS[type][1])
        raise ValueError("Unknown encoding type {!r}".format(type))

    def decode(self, nstr):
        ctype = self._get_type(nstr)
        if len(ctype) == 2:
            ## strip the '-' from a base62
            if ctype[0] == "base62" and self._unicode_this(nstr)[0] == u'-':
                nstr = nstr[1:]
            ## make sure top16 is not actually base62
            if ctype[0] == "top16" and not all(c in top16 for c in self._unicode_this(nstr)):
                ctype = ('base62',base62)
            return self._decode_cset(nstr,ctype[1])
        elif len(ctype) == 3:
            return self._decode_uset(nstr,ctype[1],ctype[2])
        raise ValueError("Canot decode {!r} unknown numeric mapping".format(nstr))

    def decodeByType(self, nstr, type):
        if type == "base62" and self._unicode_this(nstr)[0] == u'-':
            nstr = nstr[1:]
        if type in self.C_SETS:
            return self._decode_cset(nstr, self.C_SETS[type])
        if type in self.U_SETS:
            return self._decode_uset(nstr, self.U_SETS[type][0], self.U_SETS[type][1])
        raise ValueError("Unknown encoding type {!r}".format(type))

    def _encode_cset(self, n, cset):
        chars = []
        while n > 0:
            n, d = divmod(n, len(cset))
            chars.append(cset[d])
        return ''.join(chars)

    def _encode_uset(self, n, ustart, uend):
        chars = []
        while n > 0:
            n, d = divmod(n, uend-ustart)
            chars.append(unichr(ustart+d))
        return ''.join(chars)

    def _decode_cset(self, nstr, cset):
        base = len(cset)
        basem = 1
        n = 0
        for c in self._unicode_this(nstr):
            n += (cset.index(c)) * basem
            basem = basem*base
        return n

    def _decode_uset(self, nstr, ustart, uend):
        base = uend-ustart
        basem = 1
        n = 0
        for c in self._unicode_this(nstr):
            if uend > ord(c) < ustart:
                raise ValueError("Canot decode a character within {!r}, {!r} out of bounds".format(nstr, c))
            n += (ord(c)-ustart) * basem
            basem = basem*base
        return n

    def _unicode_this(self, s):
        if isinstance(s, str):
            return unicode(s,"utf8")
        elif isinstance(s, unicode):
            return s
        raise TypeError("Invalid unicode")

    def _get_type(self, ctest):
        '''
        returns ('type', cset) or ('type', ustart, uend)
        '''
        firstC = self._unicode_this(ctest)[0]
        if firstC == u'-':
            return ('base62', base62)
        else:
            for type, cset in self.C_SETS.iteritems():
                if firstC in cset:
                    return (type, cset)
            n = ord(firstC)
            for type, (ustart,uend) in self.U_SETS.iteritems():
                if ustart <= n <= uend:
                    return (type, ustart, uend)
        raise ValueError("Canot get type for {!r}, unknown numeric mapping".format(ctest))




if __name__ == '__main__':
    ''' optparse? '''
    print ""  




