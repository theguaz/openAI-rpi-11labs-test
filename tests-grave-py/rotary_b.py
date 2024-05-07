from RPi_GPIO_Rotary import rotary
import time


def cwTurn():
    print("CW Turn")

def ccwTurn():
    print("CCW Turn")

def buttonPushed():
    print("Button Pushed")

def valueChanged(count):
    print(count)


## Initialise (clk, dt, sw, ticks)
obj = rotary.Rotary(17,27,22,5)

obj.register(increment=cwTurn, decrement=ccwTurn)
obj.register(pressed=buttonPushed, onchange=valueChanged)
obj.start()

try:
    # Keep your main program running
    while True:
        time.sleep(0.1)  # Reduces CPU load
finally:
    GPIO.cleanup()  # Clean up GPIO on exit