#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import urllib2
import json

import scrollphathd
from scrollphathd.fonts import font5x5, font5x7

from datetime import datetime

scrollphathd.rotate(180)

print("""
Scroll pHAT HD: Clock

Displays hours and minutes in text,
plus a seconds progress bar.

Press Ctrl+C to exit!

""")

# Display a progress bar for seconds
# Displays a dot if False
DISPLAY_BAR = True

# Brightness of the seconds bar and text
BRIGHTNESS = 0.1
NIGHT_BRIGHTNESS = 0.15
DAY_BRIGHTNESS = 0.5

TIME_CLOCK = 10
TIME_WEATHER = 5
TIME = TIME_CLOCK + TIME_WEATHER

# Uncomment to rotate
#scrollphathd.rotate(180)

temp = None
weather = None
weather_time = None
def get_weather():
    global weather_time
    now = datetime.now()
    if weather_time is not None and (now - weather_time).total_seconds() < 60:
        return
    weather_time = now
    try:
        global weather
        global temp
        get = urllib2.urlopen(
            "http://api.openweathermap.org/data/2.5/weather?"
            "q=London,uk&"
            "appid=2ea853544cc14753dffb4130332237e6&"
            "units=metric")
        weather = json.loads(get.read())
        main = weather["main"]
        temp = main["temp"]
    except Exception as e:
        print "Can't get weather", e

def display_weather():
    scrollphathd.write_string(
        "%doC" % temp, x=0, y=0, font=font5x5, brightness=BRIGHTNESS)

def display_bar():
    # Grab the "seconds" component of the current time
    # and convert it to a range from 0.0 to 1.0
    float_sec = (time.time() % 60) / 59.0

    # Multiply our range by 15 to spread the current
    # number of seconds over 15 pixels.
    #
    # 60 is evenly divisible by 15, so that
    # each fully lit pixel represents 4 seconds.
    #
    # For example this is 28 seconds:
    # [x][x][x][x][x][x][x][ ][ ][ ][ ][ ][ ][ ][ ]
    #  ^ - 0 seconds                59 seconds - ^
    seconds_progress = float_sec * 15

    if DISPLAY_BAR:
        # Step through 15 pixels to draw the seconds bar
        for y in range(15):
            # For each pixel, we figure out its brightness by
            # seeing how much of "seconds_progress" is left to draw
            # If it's greater than 1 (full brightness) then we just display 1.
            current_pixel = min(seconds_progress, 1)

            # Multiply the pixel brightness (0.0 to 1.0) by our global brightness value
            scrollphathd.set_pixel(y + 1, 6, current_pixel * BRIGHTNESS)

            # Subtract 1 now we've drawn that pixel
            seconds_progress -= 1

            # If we reach or pass 0, there are no more pixels left to draw
            if seconds_progress <= 0:
                break

    else:
        # Just display a simple dot
        scrollphathd.set_pixel(int(seconds_progress), 6, BRIGHTNESS)


def display_clock():
    # Display the time (HH:MM) in a 5x5 pixel font
    scrollphathd.write_string(
        time.strftime("%H:%M"),
        x=0, # Align to the left of the buffer
        y=0, # Align to the top of the buffer
        font=font5x5, # Use the font5x5 font we imported above
        brightness=BRIGHTNESS # Use our global brightness value
    )

    # int(time.time()) % 2 will tick between 0 and 1 every second.
    # We can use this fact to clear the ":" and cause it to blink on/off
    # every other second, like a digital clock.
    # To do this we clear a rectangle 8 pixels along, 0 down,
    # that's 1 pixel wide and 5 pixels tall.
    if int(time.time()) % 2 == 0:
        scrollphathd.clear_rect(8, 0, 1, 5)

def update_brightness():
    try:
        t = time.mktime(datetime.now().timetuple())
        global weather
        if t > weather["sys"]["sunrise"] and t < weather["sys"]["sunset"]:
            global BRIGHTNESS
            BRIGHTNESS = DAY_BRIGHTNESS
        else:
            global BRIGHTNESS
            BRIGHTNESS = NIGHT_BRIGHTNESS
    except Exception as e:
        print "Can't set brightness", e


while True:
    scrollphathd.clear()

    get_weather()
    if weather is None or int(datetime.now().second)%TIME < TIME_CLOCK:
        display_clock()
    else:
        display_weather()

    display_bar()
    if weather is not None:
        update_brightness()

    # Display our time and sleep a bit. Using 1 second in time.sleep
    # is not recommended, since you might get quite far out of phase
    # with the passing of real wall-time seconds and it'll look weird!
    #
    # 1/10th of a second is accurate enough for a simple clock though :D
    scrollphathd.show()
    time.sleep(0.1)
