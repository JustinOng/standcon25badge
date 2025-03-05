import time

from badge import Badge

badge = Badge()

while True:
    pads = badge.read_touch_pads()
    for i in range(len(pads)):
        badge.set_led(i, pads[i])
    time.sleep(0.1)
