#!/usr/bin/env python

import math
import time
import signal

import scrollphathd
from scrollphathd.fonts import font5x7

scrollphathd.rotate(180)

print("""
Press Ctrl+C to exit!
""")

#Uncomment to rotate the text
# scrollphathd.rotate(180)

BRIGHTNESS = 0.4
TIME_SWIRL_SEC = 5
DT_SWRIL = 0.001
TIME_MESSAGE = 40
DT_MESSAGE = 0.05

# Set a more eye-friendly default brightness
scrollphathd.set_brightness(BRIGHTNESS)

def swirl(x, y, step):
    x -= (scrollphathd.DISPLAY_WIDTH/2.0)
    y -= (scrollphathd.DISPLAY_HEIGHT/2.0)

    dist = math.sqrt(pow(x, 2) + pow(y, 2))

    angle = (step / 10.0) + dist / 1.5

    s = math.sin(angle)
    c = math.cos(angle)

    xs = x * c - y * s
    ys = x * s + y * c

    r = abs(xs + ys)

    return max(0.0, 0.7 - min(1.0, r/8.0))


while True:
    for i in xrange(int(TIME_SWIRL_SEC/DT_SWRIL)):
        timestep = math.sin(time.time() / 18) * 1500

        for x in range(0, scrollphathd.DISPLAY_WIDTH):
            for y in range(0, scrollphathd.DISPLAY_HEIGHT):
                v = swirl(x, y, timestep)
                scrollphathd.pixel(x, y, v)

        time.sleep(DT_SWRIL)
        scrollphathd.show()


    scrollphathd.write_string("    Pombinhaaa! Pq faz isso comigo?  :((    Pls don't kill me!   ", x=0, y=0, font=font5x7, brightness=BRIGHTNESS)

    for i in xrange(int(TIME_MESSAGE/DT_MESSAGE)):
        scrollphathd.show()
        scrollphathd.scroll()
        time.sleep(DT_MESSAGE)

