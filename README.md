# x404-Novelty-URL-Shortener
Working example on https://去.cc

## What
This project is a proof-of-concept to make a better and more interesting URL shortening service. It leverages the entire Unicode character set to offer unique characters (in Chinese, Korean, anglosaxon runes, braile, and even emojis).

Most URL shortening services use a base-62 alphanumeric key to map to a long-url. Typically, the base-62 characters include 26-uppercase letters (ABCD...), 26 lowercase letters (abcd...), and 10 digits (0123...), for a total of 62 characters. Occasionally they will include an underscore or dash, bringing you to base-64.

This is all well and fine, and perfectly reasonable in an ASCII character set where you're trying to avoid non-printable characters. However, nowadays with modern browsers supporting UTF-8, and offering at least one font capable of rendering most of the popular Unicode character sets (中文, 한글, etc), then why limit ourselves to ASCII? We have the entire global set of symbols at our disposal!

## Why
Why not! There are numerous problems with URL shortening services, from scammers to all kinds of ugliness, but most people use a URL shortening service as a kind of novelty. For me, this is a personal project and I don't expect to offer it in any serious production capacity, other than for my own amusement, and as a proof-of-concept of what a URL Shortening Service **could** do.

## How
In short, Punycode with Unicode numeric bases.

### Punycode
Punycode is a transcoding of ASCII-safe characters to represent Unicode characters. Punycode is used for internationalized domain names. For examples the domain **去.cc** in punycode is **xn--1nr.cc**. All punycode domain names begin with the prefix "xn--". Older browsers that don't support internationalized domain names, will simply gracefully degrade to the punycode representation. Modern browsers will display the internationalized domain names perfectly fine.

For referemce, 去 (pinyin: qù) means "to go", as in 去商店 (go to the store) or 去學校 (go to school).

### Unicode and UTF-8
Unicode is the industry standard for character coding, covering over a hundred thousand characters across modern as well as ancient writing scripts (with over a million possible characters). UTF-8 is the encoding standard. It is variable width (1 to 4 bytes per character), and is completely backwards compatible with ASCII. This means ASCII strings will perfectly match their corresponding UTF-8 strings. However, UTF-8 also supports multi-byte Unicode encodings (including the [CJK blocks](https://en.wikipedia.org/wiki/CJK_characters)).

Unfortunately, browser support on these extended Unicode sets varies wildly, although increasingly most browsers offer at least one font capable of rendering most of the common Unicode ranges. And this seems to improve every year.

### Unicode as a Numeric Base
One of the larger contiguous unicode ranges that seems to have decent support on modern browsers is the initial CJK block as well as Korean Hangul syllables. Why are these interesting? Well, rather than a base-62 or base-64, what if we can offer a base-20000?

#### Extremely Large Numeric Bases
The CJK range of *4e00* to *9fea* seems to be adequately supported, as well as the Hangul range of *ac00* to *d7a3*, this would give us a base-20970 and a base-11171 respectively.

For example, in a base-62 scheme, you may have a typical short URL that looks like this:

    http://shorturl/xp5

However, the CJK and Hangul would look something like:

    http://去.cc/齁
    http://去.cc/톞각
    
Taken to extremes, what if we're loading in 9,223,372,036,854,775,807 (that's nine quintillion two hundred twenty-three quadrillion three hundred seventy-two trillion thirty-six billion eight hundred fifty-four million seven hundred seventy-five thousand eight hundred seven). This is the largest signed-64-bit integer on most systems. We'd end up with something like this:

    http://shorturl/7M85y0N8lZa
    http://去.cc/瑙稃瑰蜣丯
    http://去.cc/셁뻾뮋럣깐
    
In practice, I'm not sure anyone will ever need to map nine quitillion URLs. There aren't that many URLs, although there are billions of URLs. Let's say we're dealing with 88-billion URLs. In that case it would look like this:

    http://shorturl/3CG2Fy1
    http://去.cc/執洪仉
    http://去.cc/닁읛껅
    
NOTE: while the character-length of the Chinese string is less than the alphanumeric string, each of the Chinese characters reprsents 3-bytes in UTF-8. So this is not in any way saving you space in binary, although technically neither is ASCII, but it's worth mentioning.

#### Other Novelty Bases
Unicode is full of fun and interesting character sets, here are some examples that I have built into x404:

    # base-10   922111
    base62:     LSR3
    top16:      eewwt
    CJK:        鶱丫
    hangul:     쏉걒
    dingbats:   ➚✴✙
    braille:    ⣚⡴⡙
    alchemical: 🜩🝓🝅
    anglosaxon: ᛡᛇᛞᚻᚢ
    greek:      οΒΦδ
    yijing:     ䷫䷔䷫䷃
    
* **top16**: The top-16 most common letters in English (where f maps to 0). This is a subset of base62, and I find it often produces sequences that are easier to remember, albeit longer than base-62.
* **CJK**: The base-20970 Chinese characters. This potentially can grow to over 80,000 -- depending on future browser support of the CJK block extensions. Also, these are really beautiful.
* **hangul**: The base-11171 Hangul syllables. Note: Hangul is a phonetic alphabet with only 28 characters, however, for readability, Unicode includes 11,171 combinations of those 28 Hangul characters. This makes it useful an extremely large numeric base.
* **dingbats**: Precursor to emojis, dingbats provide a base-192.
* **braille**: 8-dot Braille patterns provide a base-192.
* **alchemical**: alchemical symbols provide a base-116.
* **anglosaxon**: Anglo-Saxon Runes provide a mere base-29.
* **greek**: Greek provides a base-49.
* **yijing**: The I Ching (易經, yijing) hexagrams provide a base-64.
    
