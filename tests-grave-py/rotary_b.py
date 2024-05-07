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
obj = rotary.Rotary(17,27,22,2)

obj.register(increment=cwTurn, decrement=ccwTurn)
obj.register(pressed=buttonPushed, onchange=valueChanged)
obj.start()
time.sleep(5)
obj.stop()