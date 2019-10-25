from blinkt import set_pixel, set_brightness, show, clear
import time

set_brightness(0.1)

while True:
    for i in range(8):
        clear()
        set_pixel(i, 255, 0, 0)
        show()
        time.sleep(0.05)
        