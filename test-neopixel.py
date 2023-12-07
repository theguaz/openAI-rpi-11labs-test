import time
from rpi_ws281x import PixelStrip, Color

# LED strip configuration:
LED_COUNT = 7        # Number of LED pixels
LED_PIN = 12          # GPIO pin connected to the pixels (18 uses PWM)
LED_FREQ_HZ = 800000  # LED signal frequency in hertz
LED_DMA = 10          # DMA channel to use for generating signal
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal

# Create NeoPixel object
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
strip.begin()

try:
    while True:
        # Example: cycle colors
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(255, 0, 0))  # Red color
            strip.show()
            time.sleep(0.1)
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0, 255, 0))  # Green color
            strip.show()
            time.sleep(0.1)
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(0, 0, 255))  # Blue color
            strip.show()
            time.sleep(0.1)
except KeyboardInterrupt:
    # Clear the color of all pixels to turn them off
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
