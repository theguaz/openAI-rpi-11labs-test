import pigpio

ROTARY_CLK = 17
ROTARY_DT = 27
ROTARY_BUTTON = 22

pi = pigpio.pi()

def callback(way):
    print("Turned", "Right" if way > 0 else "Left")

decoder = pigpio.decoder(pi, ROTARY_CLK, ROTARY_DT, callback)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    decoder.cancel()
    pi.stop()
