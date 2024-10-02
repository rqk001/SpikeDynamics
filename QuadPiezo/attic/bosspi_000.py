
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

def tonewave(snd, size):
    import math
    for i in range(0, size//2):
        snd[i*2:i*2+2]=struct.pack('>h',int(2000 * math.sin(math.pi * i / (size//4))) & 0x0fff)

def sndsend(h, cs, size, snd, ind, bout, bin):
    cs.off()
    h.write_readinto(bout, bin)
    while (( bin[0] & 0xf0 ) != 0xc0 or (bin[1] & 0xc0) == 0x80):
        h.write_readinto(bout, bin)
    len = (bin[1] & 0x7f) * 2
    trim = len if (len + ind) <= size else size - ind
    h.write(snd[ind:ind+trim])
    cs.on()
    ind += trim
    if (ind >= size):
        ind -= size
    return ind

def sndplay(h, cs, snd, bufsize):
    ind = 0
    b5616=struct.pack('>h', 0x5616)
    bin=bytearray(2)
    while(True):
        ind = sndsend(h, cs, bufsize, snd, ind, b5616, bin)

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
    

        



