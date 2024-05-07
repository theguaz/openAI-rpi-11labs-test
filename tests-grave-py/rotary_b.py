from RPi_GPIO_Rotary import rotary
import time

import json


from playsound import playsound

# Array of items to select from
current_item = 0  # Start with the first item
projectFolder = '/home/pi/openAI-rpi-11labs-test/'
promptsFile = 'prompts.json'
items = []


with open(projectFolder + promptsFile, 'r') as file:
    items = json.load(file)['prompts']


def tellpos():
    global current_item, currentFile, canread



    current_item %= len(items)  # Ensure the current_item index wraps around
    currentFile = projectFolder + "init_audios/" + items[current_item]['id'] + "_select.wav"
    print("Selected:", currentFile)
    print("current_item:", current_item)
    playsound(currentFile)

def cwTurn():
    global current_item
    current_item += 1
    print("CW Turn")
    tellpos()

def ccwTurn():
    global current_item
    current_item -= 1
    print("CCW Turn")
    tellpos()

def buttonPushed():
    print("Button Pushed")

def valueChanged(count):
    #print(count)






## Initialise (clk, dt, sw, ticks)
obj = rotary.Rotary(17,27,22,2)

obj.register(increment=cwTurn, decrement=ccwTurn)
obj.register(pressed=buttonPushed, onchange=valueChanged)
obj.start()

try:
    # Keep your main program running
    while True:
        time.sleep(0.1)  # Reduces CPU load
finally:
    GPIO.cleanup()  # Clean up GPIO on exit