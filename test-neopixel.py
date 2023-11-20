import time
import threading
from rpi_ws281x import PixelStrip, Color

# LED strip configuration:
LED_COUNT = 7        # Number of LED pixels
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM)
LED_FREQ_HZ = 800000  # LED signal frequency in hertz
LED_DMA = 10          # DMA channel to use for generating signal
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal



def pulsate_color(strip, color, stop_event):
    """Pulsate a given color on the strip."""
    while not stop_event.is_set():
        for brightness in range(0, 255, 5) + list(range(255, 0, -5)):
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, color)
            strip.setBrightness(brightness)
            strip.show()
            time.sleep(0.02)
        if stop_event.is_set():
            break


def yellow_pulsate(strip, stop_event):
    pulsate_color(strip, Color(255, 255, 0), stop_event)

def green_pulsate(strip, stop_event):
    pulsate_color(strip, Color(0, 255, 0), stop_event)

def red_pulsate(strip, stop_event):
    pulsate_color(strip, Color(255, 0, 0), stop_event)



strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
strip.begin()

# Create stop events for each thread
yellow_stop = threading.Event()
green_stop = threading.Event()
red_stop = threading.Event()

# Start threads
yellow_thread = threading.Thread(target=yellow_pulsate, args=(strip, yellow_stop))
green_thread = threading.Thread(target=green_pulsate, args=(strip, green_stop))
red_thread = threading.Thread(target=red_pulsate, args=(strip, red_stop))

yellow_thread.start()
green_thread.start()
red_thread.start()

# Example usage: Run yellow animation for 10 seconds then stop
time.sleep(10)
yellow_stop.set()
yellow_thread.join()

# Cleanup when all animations are done
strip.setBrightness(0)
for i in range(strip.numPixels()):
    strip.setPixelColor(i, Color(0, 0, 0))
strip.show()
