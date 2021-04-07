import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont

from time import strftime, sleep
import random

import busio
import adafruit_mpr121

from adafruit_rgb_display.rgb import color565
import adafruit_rgb_display.st7789 as st7789
import webcolors

i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)

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

while True:
    for i in range(12):
        if not mpr121[i].value:
            p_img = Image.open("perfume.jpg")
            p_img = p_img.resize((240, 135), Image.BICUBIC)
            disp.image(p_img, rotation)             
        else:
            print(f"Banana {i} touched!")
            if i == 6:
                for j in range(865):
                    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
                    draw.text((10, 10), 'Sprays Remaining', font=font_s, fill='white')
                    draw.text((10, 30), str(865-j), font=font_l, fill='purple')
                    draw.text((130, 50), 'sprays', font=font_s, fill='white')
                    draw.text((10, 80), str(50-j/10), font=font_l, fill='skyblue')
                    draw.text((133, 110), 'ml', font=font_s, fill='white')
                    disp.image(image, rotation)
                    time.sleep(2)
            else:
                    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
                    draw.text((10, 0), 'Perfume Box', font=font_m, fill='Pink')
                    draw.text((10, 40), 'Power and Sensors', font=font_s, fill='white')
                    draw.text((10, 65), 'On', font=font_l, fill='orange')
                    disp.image(image, rotation)
                    time.sleep(5)





