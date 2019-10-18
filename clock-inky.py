from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne
from datetime import datetime, timedelta
from time import sleep

# Set up the display

inky_display = InkyPHAT("black")
inky_display.set_border(inky_display.BLACK)
refresh_time = 5

# Display a startup splash screen

img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)

message = "PiClock"
font = ImageFont.truetype(FredokaOne, 48)
w, h = font.getsize(message)
x = (inky_display.WIDTH / 2) - (w / 2)
y = (inky_display.HEIGHT / 2) - (h / 2)
draw.text((x, y), message, inky_display.BLACK, font)
inky_display.set_image(img.rotate(180))
inky_display.show()

# This next part we want to essentially loop over every min on the min.
# Actually refresh just before we need to so that the refresh happens over
# the minute and not completely after it.

# for y in range(5):
while True:
	delay = (60 - datetime.now().second) - int(refresh_time / 2)
	# print ('[{}] Time: {}, waiting for {} secs'.format(y, datetime.now().strftime("%H:%M:%S"), delay));
	sleep(delay)

	# Get the current time

	now = datetime.now() + timedelta(seconds=refresh_time)
	time = now.strftime("%H:%M")
	date = now.strftime("%a %-d %b")

	# Create the image that we will send to the pHat

	clock_img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
	clock_draw = ImageDraw.Draw(clock_img)

	# Output time to the image

	timefont = ImageFont.truetype(FredokaOne, 64)
	tw, th = timefont.getsize(time)
	tx = (inky_display.WIDTH / 2) - (tw / 2)
	ty = (inky_display.HEIGHT / 2) - (th / 2)

	clock_draw.text((tx, ty), time, inky_display.BLACK, timefont)

	# Output date to the image

	padding = 2
	datefont = ImageFont.truetype(FredokaOne, 18)
	dw, dh = datefont.getsize(date)
	dx = (inky_display.WIDTH - dw - padding)
	dy = 0

	clock_draw.text((dx, dy), date, inky_display.BLACK, datefont)

	# Rotate and then send constructed image to phat

	rotated = clock_img.rotate(180)
	inky_display.set_image(rotated)
	# print ('Time: {}'.format(datetime.now().strftime("%H:%M:%S")));
	inky_display.show()
	# print ('Time: {}'.format(datetime.now().strftime("%H:%M:%S")));
