import RPi.GPIO as GPIO
import time
import json


from playsound import playsound

# Define GPIO pins
CLK = 17
DT = 27
SW = 22

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Variables to track the state
clkLastState = GPIO.input(CLK)
dtLastState = GPIO.input(DT)

# Array of items to select from
current_item = 0  # Start with the first item
projectFolder = '/home/pi/openAI-rpi-11labs-test/'
promptsFile = 'prompts.json'
items = []

with open(projectFolder + promptsFile, 'r') as file:
    items = json.load(file)['prompts']


def tellpos(current_i):
    global current_item, currentFile
    current_item = current_i
    current_item %= len(items)  # Ensure the current_item index wraps around
    currentFile = projectFolder + "init_audios/" + items[current_item]['id'] + "_select.wav"
    print("Selected:", currentFile)
    print("current_item:", current_item)

def update_position():
    global current_item, clkLastState, dtLastState
    clkState = GPIO.input(CLK)
    dtState = GPIO.input(DT)
    
    # Check for state change
    if clkState != clkLastState or dtState != dtLastState:
        if clkState != clkLastState:  # If the clock has changed
            if dtState != clkState:  # Clock and data states are different
                current_item += 1
                tellpos(current_item)
                break
            else:  # Clock and data states are the same
                current_item -= 1
                tellpos(current_item)
                break
        
        # Save the last states for the next comparison
        clkLastState = clkState
        dtLastState = dtState

def button_pressed_callback(channel):
    # You could add actions here for when the button is pressed
    print("Button Pressed - Current selection:", items[current_item])

# Attach the callback function to GPIO events
GPIO.add_event_detect(CLK, GPIO.BOTH, callback=lambda channel: update_position())
GPIO.add_event_detect(SW, GPIO.FALLING, callback=button_pressed_callback, bouncetime=300)

try:
    # Keep your main program running
    while True:
        time.sleep(0.1)  # Reduces CPU load
finally:
    GPIO.cleanup()  # Clean up GPIO on exit
