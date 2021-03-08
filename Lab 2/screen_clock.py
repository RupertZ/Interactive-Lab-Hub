import time
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
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

# Enable the buttons for demo
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)

# Define default coordination
x, y = 3, 5

# Enable the joystick
joystick = qwiic_joystick.QwiicJoystick()

if joystick.is_connected() == False:
    print("The Qwiic Joystick device isn't connected to the system. Please check your connection", \
        file=sys.stderr)

joystick.begin()

print("Initialized. Firmware Version: %s" % joystick.get_version())

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    #TODO: fill in here. You should be able to look in cli_clock.py and stats.py 

    # Get current time hour 
    hour = int(strftime("%H"))

    print("X: %d, Y: %d, Button: %d" % ( \
            joystick.get_horizontal(), \
            joystick.get_vertical(), \
            joystick.get_button()))

    time.sleep(0.1)

    # Button Push
    while joystick.get_button() == 0:
        ma_img = Image.open("mawen.jpeg")
        ma_img = ma_img.resize((240, 135), Image.BICUBIC)

        disp.image(ma_img, rotation)
        time.sleep(0.1)
    # Left
    while 500 < joystick.get_horizontal() <= 600 and joystick.get_vertical() == 0:
        ma_img = Image.open("1.png")
        ma_img = ma_img.resize((240, 135), Image.BICUBIC)
    
        disp.image(ma_img, rotation)
        time.sleep(0.1)
    # Upper Left
    while joystick.get_horizontal() == 1023 and 0 <= joystick.get_vertical() < 100:
        ma_img = Image.open("2.png")
        ma_img = ma_img.resize((240, 135), Image.BICUBIC)
    
        disp.image(ma_img, rotation)
        time.sleep(0.1)
    # Up
    while joystick.get_horizontal() == 1023 and 500 <= joystick.get_vertical() < 600:
        ma_img = Image.open("3.png")
        ma_img = ma_img.resize((240, 135), Image.BICUBIC)
    
        disp.image(ma_img, rotation)
        time.sleep(0.1)
    # Upper Right
    while joystick.get_horizontal() == 1023 and 1000 <= joystick.get_vertical() < 1024:
        ma_img = Image.open("4.png")
        ma_img = ma_img.resize((240, 135), Image.BICUBIC)
    
        disp.image(ma_img, rotation)
        time.sleep(0.1)
    # Right
    while 500 <= joystick.get_horizontal() < 600 and 0 <= joystick.get_vertical() == 1023:
        ma_img = Image.open("5.png")
        ma_img = ma_img.resize((240, 135), Image.BICUBIC)
    
        disp.image(ma_img, rotation)
        time.sleep(0.1)
    # Lower Right
    while joystick.get_horizontal() == 0 and 1000 <= joystick.get_vertical() < 1024:
        ma_img = Image.open("6.png")
        ma_img = ma_img.resize((240, 135), Image.BICUBIC)
    
        disp.image(ma_img, rotation)
        time.sleep(0.1)
    # Down
    while joystick.get_horizontal() == 0 and 500 <= joystick.get_vertical() < 600:
        ma_img = Image.open("7.png")
        ma_img = ma_img.resize((240, 135), Image.BICUBIC)
    
        disp.image(ma_img, rotation)
        time.sleep(0.1)
    # Lower Left
    while 0 <=joystick.get_horizontal() < 100 and 0 <= joystick.get_vertical() < 100:
        ma_img = Image.open("8.png")
        ma_img = ma_img.resize((240, 135), Image.BICUBIC)
    
        disp.image(ma_img, rotation)
        time.sleep(0.1)

 

    # Wake Up: If Master Ma notices that you get up late, he will criticize you and ask you to practice Kung Fu.
    # Use bottons to show how it looks like when the current hour is not in that range.

    if (6 <= hour < 8) or (buttonA.value and not buttonB.value): 
        image = Image.open("mabaoguo3.jpeg")
        # Resize the image to miniPiTFT resolution 240 * 135
        image = image.resize((240, 135), Image.BICUBIC)

        draw = ImageDraw.Draw(image)

        draw.text((x, y), strftime("%H:%M:%S%p"), font=font, fill="#005AC8")
        draw.text((x + 135, y + 90), "Young man,", font=font, fill="#FDAF00")
        draw.text((x + 135, y + 110), "very rude!", font=font, fill="#FDAF00")
        
    # Late Hours： If Master Ma notices that you sleep late， he will kindly urge you to sleep.
    # Use bottons to show how it looks like when the current hour is not in that range.
    
    elif (23 <= hour or hour < 6) or (buttonB.value and not buttonA.value): 
        image = Image.open("mabaoguo2.jpeg")
        # Resize the image to miniPiTFT resolution 240 * 135
        image = image.resize((240, 135), Image.BICUBIC)

        draw = ImageDraw.Draw(image)

        draw.text((x, y), strftime("%H:%M:%S%p"), font=font, fill="#005AC8")
        draw.text((x + 100, y + 60), "How's weather?", font=font, fill="#FFFFFF")
        draw.text((x + 100, y + 80), "Think better!", font=font, fill="#FFFFFF")

    # Default: It is business hours and Master Ma shows his master style and manner。
    else:
        image = Image.open("mabaoguo1.jpeg")
        # Resize the image to miniPiTFT resolution 240 * 135
        image = image.resize((240, 135), Image.BICUBIC)

        draw = ImageDraw.Draw(image)
        
        draw.text((x, y), strftime("%H:%M:%S%p"), font=font, fill="#005AC8")
        draw.text((x, y + 90), "I'm Tai Chi master", font=font, fill="#960000")
        draw.text((x, y + 110), "Ma Baoguo", font=font, fill="#960000")


    # Display image.
    disp.image(image, rotation)
    time.sleep(1)