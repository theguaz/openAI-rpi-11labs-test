import RPi.GPIO as GPIO
import time

# Define GPIO pins
CLK = 17
DT = 27

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# State Encoding
states = {
    '00': 0,
    '01': 1,
    '10': 2,
    '11': 3
}

# Valid transitions from current state to next state
# This table is specific to how your rotary encoder might behave. This is a common pattern but check your device specs.
transition_table = [
    [0, 1, -1, 0],
    [-1, 0, 0, -1],
    [0, -1, 0, 1],
    [1, 0, -1, 0]
]

current_state = states[f'{GPIO.input(CLK)}{GPIO.input(DT)}']
counter = 0

def read_encoder():
    global current_state, counter
    clk_state = GPIO.input(CLK)
    dt_state = GPIO.input(DT)
    next_state = states[f'{clk_state}{dt_state}']
    val = transition_table[current_state][next_state]
    if val != -1:
        counter += val
        print("Counter:", counter)
    current_state = next_state

# Attach the callback function to GPIO events
GPIO.add_event_detect(CLK, GPIO.BOTH, callback=lambda channel: read_encoder())
GPIO.add_event_detect(DT, GPIO.BOTH, callback=lambda channel: read_encoder())

try:
    while True:
        time.sleep(0.1)  # Reduce CPU usage
finally:
    GPIO.cleanup()  # Clean up GPIO on exit
