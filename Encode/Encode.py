# coding: utf8
import binascii
import urllib.parse


def DoubleUrlencode(text):  # double encode
    text = SingleUrlencode(text)
    text = SingleUrlencode(text)
    return text


def SingleUrlencode(text):  # singl encode
    lengthText = urllib.parse.urlencode({'blahblahblah': text})
    lengthText = lengthText[13:]
    return lengthText


def HexEncode(text):
    text = bytes(text, 'utf-8')
    hexcode = binascii.hexlify(text)
    return str(hexcode)


def EnkodeHexOne(text):  # with parametr %
    text = HexEncode(text)
    text = text[2:-1]
    out = '%'
    i = -1
    for t in text:
        if i % 2 == 0:
            out = out + t + "%"
            i += 1
        else:
            out = out + t
            i += 1
    return out[0:len(out) - 1]


def EnkodeHexTwo(text):  # with parametr &#x
    text = HexEncode(text)
    text = text[2:-1]
    out = '&#x'
    i = -1
    for t in text:
        if i % 2 == 0:
            out = out + t + "&#x"
            i += 1
        else:
            out = out + t
            i += 1

    return out[0:len(out) - 3]


def UnicodeOverlong(text):  # unicode overlong , replace dot with slash and backslash
    str = text.replace('.', '%c0%2e')
    str1 = str.replace('/', '%c0%af')
    str2 = str1.replace('\\', '%c0%5c')
    return str2


def UnicodeBit16(text): # 16-Bit unicode Encoding
    str = text.replace('.', '%u002e')
    str1 = str.replace('/', '%u2215')
    str2 = str1.replace('\\', '%u2216')
    return str2



# utf 7 text.encode('utf-7')

