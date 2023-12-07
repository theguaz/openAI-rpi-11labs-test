import socket
from rpi_ws281x import *
import time


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

def pulsate(color, total_duration=0.5):
    """ Gradually change the LED brightness to create a pulsating effect over a total duration """
    steps = 10  # Number of brightness levels
    num_cycles = 2  # Brighten and dim count as 2 cycles
    interval = total_duration / (steps * num_cycles)

    for brightness in list(range(0, 256, int(256/steps))) + list(range(255, -1, -int(256/steps))):
        for i in range(strip.numPixels()):
            adjusted_color = Color(int(color[0] * brightness/255),
                                   int(color[1] * brightness/255),
                                   int(color[2] * brightness/255))
            strip.setPixelColor(i, adjusted_color)
        strip.show()
        time.sleep(interval)


def light_control(message):
    """ Change the LED light based on the message """
    color_map = {
        'sht': (255, 0, 0),  # Red
        'ask': (0, 255, 0),  # Green
        'spk': (0, 0, 255),  # Blue
        'done': (0, 0, 0)    # Off
    }
    
    color = color_map.get(message, (0, 0, 0))
    pulsate(color)

def start_client():
    host = 'localhost'
    port = 12345

    client_socket = socket.socket()
    client_socket.connect((host, port))

    try:
        while True:
            data = client_socket.recv(1024).decode()
            
            
            light_control(data)
    except KeyboardInterrupt:
        client_socket.close()

if __name__ == '__main__':
    start_client()
