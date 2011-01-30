from __future__ import division

import pygame
import sys, time
import playback
from multiprocessing import Process, Pipe


recv, send = Pipe()
p = Process(target=playback.playback, args=(recv,))
p.start()


pygame.init()
num = 8
factor = num*40
sec = 5
size = width, height = factor, factor
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

i = 0
j = 120

mass = {}
for x in range(num):
    for y in range(num):
        mass[x,y] = 0

data = {}
for x in range(num):
    for y in range(num):
        data[x,y] = False


while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            p.terminate()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x,y = event.pos
            x //= 40
            y //= 40
            data[x,y] = not data[x,y]
        

    i = (i+sec)%(factor*2)
    j = (j+sec)%(factor*2)

    if i < factor:
        x = i//40
        for y in range(num):
            if data[x,y]:
                mass[x,y] = 60
    if j < factor:
        y = j//40
        for x in range(num):
            if data[x,y]:
                mass[x,y] = 60


    sounds = []
    if i < factor and i%40 == 0:
        x = i//40
        for y in range(num):
            if data[x,y]:
                sounds += [num-y]
    
        if sounds:
            raw = playback.mixer(sounds, 1/60*(factor//num/sec))
            send.send(raw)

    
    sounds = []
    if j < factor and j%40 == 0:
        y = j//40
        for x in range(num):
            if data[x,y]:
                sounds += [x]
    
        if sounds:
            raw = playback.mixer(sounds, 1/60*(factor//num/sec))
            send.send(raw)
        

    screen.fill((0,0,0))

    for x in range(num):
        for y in range(num):
            if mass[x,y] > 0:
                pygame.draw.rect(screen,
                                 (0,0,255*mass[x,y]/60),
                                 (x*40,y*40,40,40))
                mass[x,y] -= 1
            if data[x,y]:
                pygame.draw.rect(screen,
                                 (0,0,255),
                                 (x*40,y*40,40,40),
                                 1)

    pygame.draw.line(screen, (128,128,128), (i,0), (i,factor))
    pygame.draw.line(screen, (128,128,128), (0,j), (factor,j))

    pygame.display.flip()
