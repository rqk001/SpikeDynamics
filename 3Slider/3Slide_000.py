from time import sleep
from machine import Pin

p1 = Pin(12, Pin.OUT)
p2 = Pin(13, Pin.OUT)
p3 = Pin(14, Pin.OUT)

delay=.25

while (True):
    p1.on()
    sleep(delay)
    p3.off()
    sleep(delay)
    p2.on()
    sleep(delay)
    p3.on()
    sleep(delay)
    p1.off()
    sleep(delay)
    p2.off()
    sleep(delay)


