from __future__ import division

from math import sin, floor, pi
from struct import pack
import pyaudio

def mixer(levels, seconds):

    sampling = int(44100*seconds)

    rs = [2*pi*440*(2**(i/12))/44100 for i in levels]
    ls = [2*pi*440*(2**((i+1)/12))/44100 for i in levels]

    raw = ''

    for x in xrange(sampling):
        r = l = 0
        for step in rs:
            r += floor(30000/12*sin(step*x))
        for step in ls:
            l += floor(30000/12*sin(step*x))
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
