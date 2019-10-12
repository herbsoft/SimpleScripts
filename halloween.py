# Simple script to move servos via a piconzero for a halloween decoration
# Press Ctrl-C to stop
#

from time import sleep
import piconzero as pz, time

print ("Halloween animation using servos")
print ("Press Ctrl-C to end")
print

pz.init()

number_servos = 5
start_angle = 45
stop_angle = 135
delay_time = 0.3

# Define which pins are the servos and set their output and centre them
for s in range(number_servos):
    pz.setOutputConfig(s, 2)
    pz.setOutput(s, start_angle)
    sleep(delay_time)

# main loop
try:
    # while True:
    for i in range(5):
        for servo in range(number_servos):
             pz.setOutput(servo, stop_angle)
             sleep(delay_time)
             pz.setOutput(servo, start_angle)
             sleep(delay_time)
        
except KeyboardInterrupt:
    print

finally:
    pz.cleanup()
