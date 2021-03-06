import time
import subprocess
import digitalio
import board
import pygame
from PIL import Image, ImageDraw, ImageFont

from time import strftime, sleep
import random

import busio
import adafruit_mpr121

from adafruit_rgb_display.rgb import color565
import adafruit_rgb_display.st7789 as st7789
import webcolors

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
    board.SPI(),
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
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
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
font_s = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
font_m = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
font_l = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 50)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

pygame.init()
screen = pygame.display.set_mode((400,400))
cool = 0
init_state = True

while True:
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            init_state = False

            if event.key == pygame.K_q:
                cool = 1

            if event.key == pygame.K_w:
                cool = 2

            if event.key == pygame.K_e:
                cool = 3

            if event.key == pygame.K_r:
                cool = 4

 
        if init_state:
            p_img = Image.open("perfume.jpg")
            p_img = p_img.resize((240, 135), Image.BICUBIC)
            disp.image(p_img, rotation)             


        elif cool == 1 and not init_state:
            ma_img = Image.open("1.png")
            ma_img = ma_img.resize((240, 135), Image.BICUBIC)

            disp.image(ma_img, rotation)


        elif cool == 2 and not init_state:
            ma_img = Image.open("2.png")
            ma_img = ma_img.resize((240, 135), Image.BICUBIC)

            disp.image(ma_img, rotation)


        elif cool == 3 and not init_state:
            ma_img = Image.open("3.png")
            ma_img = ma_img.resize((240, 135), Image.BICUBIC)

            disp.image(ma_img, rotation)


        elif cool == 4 and not init_state:
            ma_img = Image.open("4.png")
            ma_img = ma_img.resize((240, 135), Image.BICUBIC)

            disp.image(ma_img, rotation)




