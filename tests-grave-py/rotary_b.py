import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
clk = 17  # Adjust pin numbers accordingly
dt = 27
GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_UP)




def my_callback(channel):
    state_clk = GPIO.input(clk)
    state_dt = GPIO.input(dt)
    if state_clk == 0 and state_dt == 1:
        print("Rotated Clockwise")
    elif state_clk == 0 and state_dt == 0:
        print("Rotated Counterclockwise")

# Use the built-in bouncetime parameter to debounce
GPIO.add_event_detect(clk, GPIO.FALLING, callback=my_callback, bouncetime=200)

