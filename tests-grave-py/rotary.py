import RPi.GPIO as GPIO
import time

# Define GPIO pins
CLK = 17
DT = 27
SW = 22

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Variables to hold the state and timing for debouncing
last_rotation_time = 0
debounce_time = 0.3  # Debounce time in seconds

# Array of items to select from

current_item = 0  # Start with the first item
clkLastState = GPIO.input(CLK)

projectFolder = '/home/pi/openAI-rpi-11labs-test/'

promptsFile = 'prompts.json'

items = None

def loadPrompts(filename):
    # Load the JSON data from a file
    with open(filename, 'r') as file:
        items = json.load(file)
        

loadPrompts(projectFolder + promptsFile)




def clk_callback(channel):
    global current_item, last_rotation_time, clkLastState
    current_time = time.time()
    if (current_time - last_rotation_time) > debounce_time:
        dtState = GPIO.input(DT)
        if dtState != clkLastState:
            current_item += 1
        else:
            current_item -= 1
        current_item %= len(items)  # Wrap around
        

        currentFile = projectFolder + "init_audios/" + items[current_item]['id'] + "_selected.wav"
        print("Selected:", currentFile)
        playsound(currentFile)

        last_rotation_time = current_time
    clkLastState = GPIO.input(CLK)

def sw_callback(channel):
    global last_rotation_time
    current_time = time.time()
    if (current_time - last_rotation_time) > debounce_time:
        print("Button Pressed - Current selection:", items[current_item])
        last_rotation_time = current_time

# Attach the callback functions to GPIO events
GPIO.add_event_detect(CLK, GPIO.BOTH, callback=clk_callback, bouncetime=int(debounce_time * 1000))
GPIO.add_event_detect(SW, GPIO.FALLING, callback=sw_callback, bouncetime=int(debounce_time * 1000))

try:
    # Keep your main program running
    while True:
        time.sleep(1)  # You can change this to a very long sleep as it's just to keep the script running

finally:
    GPIO.cleanup()  # Clean up GPIO on exit
