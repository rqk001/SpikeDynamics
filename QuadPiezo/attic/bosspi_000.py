
from machine import Pin, SPI
import binascii
import struct

def hspi(baud):
    from machine import Pin, SPI
    global cs
    a=SPI(2)
    a.init(baudrate=baud, polarity=0, phase=0, bits=16, firstbit=SPI.MSB, sck=Pin(18), miso=Pin(19), mosi=Pin(23))
    cs=Pin(5, Pin.OUT, value=1)
    return a

def wrreg(a, out):
    import array, struct, binascii
    global cs
    bout=bytearray(2)
    bin=bytearray(2)
    bout=struct.pack('>h', out)
    cs.off()
    a.write_readinto(bout, bin)
    cs.on()
    return binascii.hexlify(bin)


def iwrreg(a, out):
    import array, struct, binascii
    global cs
    bout=bytearray(2)
    bin=bytearray(2)
    bout=struct.pack('>h', out)
    cs.off()
    a.write_readinto(bout, bin)
    cs.on()
    return struct.unpack('>h', bin)

def a4wave(ba4):
    import math
    for i in range(0, 18):
        ba4[i*2:i*2+2]=struct.pack('>h',int(2000 * math.sin(math.pi * i / 9)) & 0x0fff)

def a4play(h, ba4):
    i=0
    flag = 0x10
    bufsize = 36
    ind = 0
    b5617=struct.pack('>h', 0x5617)
    bin=bytearray(2)
    while(True):
        h.write_readinto(b5617, bin)
        while (( bin[0] & 0xf0 ) != 0xc0 or (bin[1] & 0xc0) == 0x80):
            h.write_readinto(b5617, bin)
        len = (bin[1] & 0x7f) * 2
        trim = len if (len + ind) <= bufsize else bufsize - ind
        h.write(ba4[ind:ind+trim])
        ind += trim
        if (ind >= bufsize):
            ind -= bufsize

def a4playd(h, a4):
    i=0
    flag = 0x10
    while(True):
        n=iwrreg(h, 0x5607 | flag)[0]
        while (( n & 0xf000 ) != 0xc000):
            n = iwrreg(h, 0x5607 | flag)[0]
        if (( n & 0x007f) < 0x10 ):
            flag = 0x10
            print('.')
            continue
        if (( n & 0x007f) > 0x30 ):
            flag = 0
            print('x')
        n = wrreg(h, a4[i])
        i = i+1
        if (i > 16):
            i = 0
    

        



