import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Define GPIO pins
clk = 17
dt = 27
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initial state
clkLastState = GPIO.input(clk)

def rotary_callback(channel):
    global clkLastState
    clkState = GPIO.input(clk)
    dtState = GPIO.input(dt)
    if clkState != clkLastState:
        if dtState != clkState:
            print("Rotated Clockwise")
        else:
            print("Rotated Counterclockwise")
    clkLastState = clkState

# Attach event to pin
GPIO.add_event_detect(clk, GPIO.BOTH, callback=rotary_callback, bouncetime=300)

try:
    while True:
        time.sleep(0.1)  # Lower sleep time here for responsiveness
except KeyboardInterrupt:
    GPIO.cleanup()
