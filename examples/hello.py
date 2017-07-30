#!/usr/bin/env python

import time
import signal

import scrollphathd
from scrollphathd.fonts import font5x7

scrollphathd.rotate(180)

print("""
Scroll pHAT HD: Hello World

Scrolls "Hello World" across the screen
in a 5x7 pixel large font.

Press Ctrl+C to exit!

""")

#Uncomment to rotate the text
#scrollphathd.rotate(180)

#Set a more eye-friendly default brightness
scrollphathd.set_brightness(0.5)

scrollphathd.write_string("     Hi Bia!   I'm looking forward to meeting you.   I can already tell that my creator (andresnds) loves you! <3     ", x=0, y=0, font=font5x7, brightness=0.5)

while True:
    scrollphathd.show()
    scrollphathd.scroll()
    time.sleep(0.05)

