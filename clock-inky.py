from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne
from datetime import datetime, timedelta
from time import sleep
import subprocess

# ------------------------------------------------------------------------------
# Set up the display

inky_display = InkyPHAT("black")
inky_display.set_border(inky_display.BLACK)

# ------------------------------------------------------------------------------

def check_wifi():
	ps = subprocess.Popen(['iwgetid'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	try:
		subprocess.check_output(('grep', 'ESSID'), stdin=ps.stdout)
		return True
	except subprocess.CalledProcessError:
		return False

# ------------------------------------------------------------------------------

def create_mask(source, mask=(inky_display.WHITE, inky_display.BLACK)):
	mask_image = Image.new("1", source.size)
	w, h = source.size
	for x in range(w):
		for y in range(h):
			p = source.getpixel((x, y))
			if p in mask:
				mask_image.putpixel((x, y), 255)

	return mask_image

# Pre load and configure some images that we will display. These must be specifically created
# as 8-bit indexed pallette images

wifi_image = Image.open("wifi.png")
mask = create_mask(wifi_image)

# ------------------------------------------------------------------------------
# Display a startup splash screen

img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)

message = "PiClock"
font = ImageFont.truetype(FredokaOne, 48)
w, h = font.getsize(message)
x = (inky_display.WIDTH / 2) - (w / 2)
y = (inky_display.HEIGHT / 2) - (h / 2) - 10
draw.text((x, y), message, inky_display.BLACK, font)

version = "v1.1"
font = ImageFont.truetype(FredokaOne, 18)
w, h = font.getsize(version)
x = (inky_display.WIDTH - w - 15)
y = (inky_display.HEIGHT - h - 15)
draw.text((x, y), version, inky_display.BLACK, font)

if(check_wifi()):
	img.paste(wifi_image, (3, 0), mask)

inky_display.set_image(img.rotate(180))
inky_display.show()

# This next part we want to essentially loop over every min on the min.
# Actually refresh just before we need to so that the refresh happens over
# the minute and not completely after it.

refresh_time = 5

# for y in range(1):
while True:
	delay = (60 - datetime.now().second) - int(refresh_time / 2)
	# print('[{}] Time: {}, waiting for {} secs'.format(y, datetime.now().strftime("%H:%M:%S"), delay));

	if (delay > 0):
		sleep(delay)

	# Get the current time

	now = datetime.now() + timedelta(seconds=refresh_time)
	time = now.strftime("%H:%M")
	date = now.strftime("%a %-d %b")

	# Create the image that we will send to the pHat

	clock_img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))	# Create new 8bit image
	clock_draw = ImageDraw.Draw(clock_img)

	# Output time to the image

	font = ImageFont.truetype(FredokaOne, 64)
	w, h = font.getsize(time)
	x = (inky_display.WIDTH / 2) - (w / 2)
	y = (inky_display.HEIGHT / 2) - (h / 2)

	clock_draw.text((x, y), time, inky_display.BLACK, font)

	# Output date to the image

	padding = 4
	font = ImageFont.truetype(FredokaOne, 18)
	w, h = font.getsize(date)
	x = (inky_display.WIDTH - w - padding)
	y = 1

	clock_draw.text((x, y), date, inky_display.BLACK, font)

	# Output wifi symbol if connected

	if(check_wifi()):
		clock_img.paste(wifi_image, (3, 0), mask)

	# Rotate and then send constructed image to phat

	rotated = clock_img.rotate(180)
	inky_display.set_image(rotated)
	# print('Time: {}'.format(datetime.now().strftime("%H:%M:%S")));
	inky_display.show()
	# print('Time: {}'.format(datetime.now().strftime("%H:%M:%S")));
