import socket
from rpi_ws281x import *

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

def light_control(message):
    """ Change the LED light based on the message """
    if message == 'sht':
        # Example: Turn on the LED in red
        color = Color(255, 0, 0)  # Red
    elif message == 'ask':
        # Example: Turn on the LED in green
        color = Color(0, 255, 0)  # Green
    elif message == 'spk':
        # Example: Turn on the LED in blue
        color = Color(0, 0, 255)  # Blue
    elif message == 'done':
        # Example: Turn off the LED
        color = Color(0, 0, 0)  # Off
    else:
        return

    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()

def start_client():
    host = 'localhost'
    port = 12345

    client_socket = socket.socket()
    client_socket.connect((host, port))

    try:
        while True:
            data = client_socket.recv(1024).decode()
            
            print("Received from server: " + data)
            light_control(data)
    except KeyboardInterrupt:
        client_socket.close()

if __name__ == '__main__':
    start_client()
