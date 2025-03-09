import sys
import select
from machine import Pin, UART

# This script must be executed from the REPL
# ie with mpremote, `mpremote mount .` then `import uart_tgt`

uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

while True:
    while uart.any():
        c = uart.read(1)
        sys.stdout.buffer.write(c)

    if select.select([sys.stdin], [], [], 0.0)[0]:
        data = sys.stdin.buffer.read(1)
        uart.write(data)
