import socket
from rpi_ws281x import *
import time
from math import sin, pi
from threading import Thread


# LED strip configuration
LED_COUNT = 16      # Number of LED pixels.
LED_PIN = 12        # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10       # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False   # True to invert the signal (when using NPN transistor level shift)

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
strip.begin()


current_color = (0, 0, 0)  # Starting color, e.g., red

def pulsate():
    """ Gradually change the LED brightness in a yo-yo motion continuously """
    steps = 100  # Higher number of steps for smoother transition
    pulse_duration = 0.25  # Duration of one pulse
    interval = pulse_duration / steps  # Interval for each step

    while True:  # Continuous loop
        for step in range(steps):
            # Calculate brightness using a sine wave pattern for smooth transition
            brightness = (sin(pi * step / steps) ** 2)  # Square of sine for smoother transition
            adjusted_brightness = int(brightness * 64)

            for i in range(strip.numPixels()):
                # Use global variable current_color
                adjusted_color = Color(int(current_color[0] * adjusted_brightness / 255),
                                       int(current_color[1] * adjusted_brightness / 255),
                                       int(current_color[2] * adjusted_brightness / 255))
                strip.setPixelColor(i, adjusted_color)
            strip.show()
            time.sleep(interval)

def change_color(new_color):
    """ Change the color for the pulsating effect """
    global current_color
    current_color = new_color


def light_control(message):
    """ Change the LED light based on the message """
    color_map = {
        'sht': (255, 165, 0),  # Orange
        'ask': (0, 133, 235),  # Cyan
        'spk': (102, 255, 102),  # Mint
        'done': (0, 0, 0)    # Off
    }
    print(message)
    color = color_map.get(message, (0, 0, 0))
    change_color(color)

def start_client():
    host = 'localhost'
    port = 12345
    print("connecting")
    client_socket = socket.socket()
    client_socket.connect((host, port))
    # Start the pulsating effect in a separate thread
    pulsating_thread = Thread(target=pulsate)
    pulsating_thread.start()
    print("connected")
    try:
        while True:
            data = client_socket.recv(1024).decode()
            
            if len(data) == 3:
                light_control(data)
    except KeyboardInterrupt:
        client_socket.close()

if __name__ == '__main__':
    start_client()
