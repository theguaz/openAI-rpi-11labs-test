from RPi import GPIO
from time import sleep

clk = 17
dt = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

counter = 0
clkLastState = GPIO.input(clk)

def callback(channel):
    global counter, clkLastState
    clkState = GPIO.input(clk)
    dtState = GPIO.input(dt)
    if clkState != clkLastState:
        if dtState != clkState:
            counter += 1
        else:
            counter -= 1
        print(counter)
    clkLastState = clkState

GPIO.add_event_detect(clk, GPIO.BOTH, callback=callback, bouncetime=20)

try:
    while True:
        sleep(1)  # Sleep to reduce CPU usage, main loop does nothing.
finally:
    GPIO.cleanup()
