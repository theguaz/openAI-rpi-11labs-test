import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Set up pins
clk = 17  # Change as necessary
dt = 27   # Change as necessary
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize counter
counter = 0
clkLastState = GPIO.input(clk)

def rotary_callback(clk):
    global counter, clkLastState
    clkState = GPIO.input(clk)
    dtState = GPIO.input(dt)
    if clkState != clkLastState:
        if dtState != clkState:
            counter += 1
        else:
            counter -= 1
        print("Counter: ", counter)
    clkLastState = clkState
    time.sleep(0.01)  # debounce time

# Add event detection to the CLK pin
GPIO.add_event_detect(clk, GPIO.BOTH, callback=rotary_callback, bouncetime=300)

try:
    while True:
        time.sleep(0.01)
except KeyboardInterrupt:
    GPIO.cleanup()
