#-----------------------------------------------------------------------------
# qwiic_joystick_ex1.py
#
# Simple Example for the Qwiic Joystick Device
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, May 2019
# 
# This python library supports the SparkFun Electroncis qwiic 
# qwiic sensor/board ecosystem on a Raspberry Pi (and compatable) single
# board computers. 
#
# More information on qwiic is at https://www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
#==================================================================================
# Copyright (c) 2019 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy 
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights 
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
#==================================================================================

from __future__ import print_function
import time
import sys
import pygame
from time import strftime, sleep
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import qwiic_joystick


# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape! 135
width = disp.height #240
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 44)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

# Define default coordination
x, y = 3, 5

# Enable the joystick
joystick = qwiic_joystick.QwiicJoystick()

if joystick.is_connected() == False:
    print("The Qwiic Joystick device isn't connected to the system. Please check your connection", \
        file=sys.stderr)

joystick.begin()

print("Initialized. Firmware Version: %s" % joystick.get_version())

pygame.init()
screen = pygame.display.set_mode((400,400))
cool = False
init_state = True

while True:
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            init_state = False

            if event.key == pygame.K_y:
                cool = True

            if event.key == pygame.K_n:
                cool = False
                
    if cool and not init_state:
        ma_img = Image.open("1.png")
        ma_img = ma_img.resize((240, 135), Image.BICUBIC)

        disp.image(ma_img, rotation)


    elif not cool and not init_state:
        ma_img = Image.open("404.png")
        ma_img = ma_img.resize((240, 135), Image.BICUBIC)

        disp.image(ma_img, rotation)


    # Button Push
    while cool and joystick.get_button() == 0:
        ma_img = Image.open("noah.jpeg")
        ma_img = ma_img.resize((240, 135), Image.BICUBIC)

        disp.image(ma_img, rotation)
        time.sleep(0.1)
    # Left
    while cool and 500 < joystick.get_horizontal() <= 600 and joystick.get_vertical() == 0:
        ma_img = Image.open("2.png")
        ma_img = ma_img.resize((240, 135), Image.BICUBIC)
    
        disp.image(ma_img, rotation)
        time.sleep(0.1)

    # Up
    while cool and joystick.get_horizontal() == 1023 and 500 <= joystick.get_vertical() < 600:
        ma_img = Image.open("3.png")
        ma_img = ma_img.resize((240, 135), Image.BICUBIC)
    
        disp.image(ma_img, rotation)
        time.sleep(0.1)

    # Right
    while cool and 500 <= joystick.get_horizontal() < 600 and 0 <= joystick.get_vertical() == 1023:
        ma_img = Image.open("4.png")
        ma_img = ma_img.resize((240, 135), Image.BICUBIC)
    
        disp.image(ma_img, rotation)
        time.sleep(0.1)

    # Down
    while cool and joystick.get_horizontal() == 0 and 500 <= joystick.get_vertical() < 600:
        ma_img = Image.open("5.png")
        ma_img = ma_img.resize((240, 135), Image.BICUBIC)
    
        disp.image(ma_img, rotation)
        time.sleep(0.1)

    # Display image.
