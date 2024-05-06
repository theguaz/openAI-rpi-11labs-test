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

# Array of items to select from
items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
current_item = 0  # Start with the first item

clkLastState = GPIO.input(CLK)
buttonPressedTime = 0
debounceTime = 0.3  # Debounce time in seconds

try:
    while True:
        clkState = GPIO.input(CLK)
        dtState = GPIO.input(DT)
        swState = GPIO.input(SW)
        
        # Handle rotation
        if clkState != clkLastState:
            if time.time() - buttonPressedTime > debounceTime:  # Debounce by time
                if dtState != clkState:
                    current_item += 1
                else:
                    current_item -= 1
                current_item = current_item % len(items)  # Wrap around
                print("Selected:", items[current_item])
                buttonPressedTime = time.time()
        clkLastState = clkState

        # Handle button press
        if not swState:  # If button pressed
            if time.time() - buttonPressedTime > debounceTime:  # Debounce by time
                print("Button Pressed - Current selection:", items[current_item])
                buttonPressedTime = time.time()  # Update the last pressed time
            while not GPIO.input(SW):
                time.sleep(0.02)  # Delay to wait for the button to be released

        time.sleep(0.01)  # Small delay to reduce CPU usage

finally:
    GPIO.cleanup()  # Clean up GPIO on exit

