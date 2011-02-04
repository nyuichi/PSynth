from __future__ import division

from math import sin, floor, pi
from struct import pack
import pyaudio
from constants import *

singles = {}
sampling = int(44100*sec)
for i in range(41):
    hz = 2*pi*440*(2**(i/12))/44100
    raws = []
    for x in range(sampling):
        raws += [floor(32767/40*sin(hz*x))]
    singles[i] = raws


def mixer(levels):

    raw = ''

    for x in xrange(sampling):
        r = l = 0
        for level in levels:
            r += singles[level][x]
            l += singles[level*2][x]
        raw += pack('h', r) + pack('h', l)

    return raw

def playback(receiver):
    audio  = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, rate=44100, channels=2, output=True)

    while True:
        raw = receiver.recv()
        stream.write(raw)

if __name__ == '__main__':
    import time
    last = time.time()
    raw = mixer([0], 0.1)
    #stream.write(raw)
    print time.time()-last
