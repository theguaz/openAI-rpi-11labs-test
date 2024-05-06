import RPi.GPIO as GPIO
import time

# Define GPIO pins
CLK = 17
DT = 27

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(CLK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initial state of the encoder
last_clk_state = GPIO.input(CLK)
last_dt_state = GPIO.input(DT)
last_time = time.time()
debounce_interval = 0.02  # 20 milliseconds

counter = 0

def get_encoder_turn():
    global last_clk_state, last_dt_state, last_time, counter

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
                    counter += 1
                else:  # Counterclockwise
                    counter -= 1
                print("Counter:", counter)

            # Update the last known states and time
            last_clk_state = clk_state
            last_dt_state = dt_state
            last_time = current_time

# Poll the encoder state at a regular interval
try:
    while True:
        get_encoder_turn()
        time.sleep(0.5)  # Poll at 1 ms intervals
finally:
    GPIO.cleanup()  # Clean up GPIO on exit
