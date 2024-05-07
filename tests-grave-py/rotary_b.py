import RPi.GPIO as GPIO
import time

# Define GPIO pins
CLK = 17
DT = 27

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initial state of the encoder and time tracking
last_clk_state = GPIO.input(CLK)
last_dt_state = GPIO.input(DT)
last_time = time.time()
debounce_interval = 0.02  # 20 milliseconds
counter = 0
first_change = True  # Flag to detect the first change

def critical_function():
    # Placeholder for a critical function that must complete before updating the counter
    print("Executing critical function...")
    time.sleep(1)  # Simulate a delay to represent the function's execution time

def get_encoder_turn():
    global last_clk_state, last_dt_state, last_time, counter, first_change

    clk_state = GPIO.input(CLK)
    dt_state = GPIO.input(DT)
    current_time = time.time()

    # Check if the new state has persisted over the debounce interval
    if clk_state == last_clk_state and dt_state == last_dt_state:
        if (current_time - last_time) > debounce_interval:
            # Confirm the change if the time is greater than the debounce interval
            if clk_state != last_clk_state:
                # Determine direction
                if clk_state != dt_state:  # Clockwise
                    direction = 1
                else:  # Counterclockwise
                    direction = -1

                # If this is the first change, execute the critical function
                if first_change:
                    critical_function()
                    first_change = False  # Reset the flag

                # Update the counter after the critical function has completed
                counter += direction
                print("Counter:", counter)

            # Update the last known states and time
            last_clk_state = clk_state
            last_dt_state = dt_state
            last_time = current_time

# Poll the encoder state at a regular interval
try:
    while True:
        get_encoder_turn()
        time.sleep(0.001)  # Poll at 1 ms intervals
finally:
    GPIO.cleanup()  # Clean up GPIO on exit
