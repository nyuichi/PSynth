from __future__ import division

import pygame
import sys, time, random, itertools
from constants import *
import playback
from multiprocessing import Process, Pipe

def round(n, bottom=0, upper=19):
    if n > upper:
        return upper
    elif n < bottom:
        return bottom
    else:
        return n

recv, send = Pipe()
p = Process(target=playback.playback, args=(recv,))
p.start()


pygame.init()

screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
clock = pygame.time.Clock()

i = 0
j = height

depth = {}
for x in xrange(w):
    for y in xrange(h):
        depth[x,y] = 0

active = {}
for x in xrange(w):
    for y in xrange(h):
        active[x,y] = False


life_playing = False
step = 0

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            p.terminate()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x,y = event.pos
            x //= mass
            y //= mass
            for k in xrange(20):
                dx = int(random.normalvariate(0, 2))
                dy = int(random.normalvariate(0, 2))
                mx = round(x+dx, 0, w)
                my = round(y+dy, 0, h)
                active[mx,my] = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                life_playing = not life_playing

    i = (i+speed)%(width*1)
    j = (j+speed)%(height*1)

    if i < width:
        x = i//mass
        for y in xrange(h):
            if active[x,y]: depth[x,y] = 60

    if j < height:
        y = j//mass
        for x in xrange(w):
            if active[x,y]: depth[x,y] = 60


    sounds = []
    if i < width and i%mass < speed:
        x = i//mass
        for y in xrange(h):
            if active[x,y]:
                sounds += [int(y/h*20)]
    
        if sounds:
            raw = playback.mixer(sounds)
            send.send(raw)

    
    sounds = []
    if j < height and j%mass < speed:
        y = j//mass
        for x in xrange(w):
            if active[x,y]:
                sounds += [int(x/w*20)]
    
        if sounds:
            raw = playback.mixer(sounds)
            send.send(raw)
        

    screen.fill((0,0,0))

    for x in xrange(w):
        for y in xrange(h):
            if depth[x,y] > 0:
                pygame.draw.rect(screen,
                                 (0,0,255*depth[x,y]/60),
                                 (x*mass,y*mass,mass,mass))
                depth[x,y] -= 1
            if active[x,y]:
                pygame.draw.rect(screen,
                                 (0,0,255),
                                 (x*mass,y*mass,mass,mass),
                                 1)

    revs = []
    for x in xrange(w):
        for y in xrange(h):
            count = 0
            for dx in -1,0,1:
                for dy in -1,0,1:
                    if dx == dy == 0: continue
                    mx = loopx[x+dx]
                    my = loopy[y+dy]
                    if active[mx,my]: count += 1
            if not active[x,y] and count == 3:
                revs += [(x,y)]
            elif active[x,y] and count <= 1:
                revs += [(x,y)]
            elif active[x,y] and count >= 4:
                revs += [(x,y)]

    if life_playing and step % 1 == 0:
        for r in revs:
            x,y = r
            active[x,y] = not active[x,y]
    step += 1

    pygame.draw.line(screen, (128,128,128), (i,0), (i,height))
    pygame.draw.line(screen, (128,128,128), (0,j), (width,j))

    pygame.display.flip()
