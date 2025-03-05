from machine import Pin
import rp2

"""
For input() to be handled correctly when ran with mpremote, this file must be called from repl ie
mpremote repl
> import chall_crackme
"""


@rp2.asm_pio(out_shiftdir=rp2.PIO.SHIFT_RIGHT)
def beepbop():
    pull()
    out(y, 3)
    in_(y, 3)
    out(x, 5)

    pull()
    in_(osr, 2)

    in_(x, 5)

    out(null, 2)
    in_(osr, 6)

    push()


sm = rp2.StateMachine(0, beepbop)
sm.active(1)

flag = input("Enter flag: ")

if len(flag) % 2 == 1:
    flag += chr(0xA5)

out = []
for c in flag:
    sm.put(ord(c))
    if sm.rx_fifo():
        out.append(sm.get())

if out == [
    49947,
    15129,
    31708,
    51800,
    31564,
    31639,
    4507,
    58077,
    6732,
    58076,
    35416,
    51801,
    44009,
]:
    print("Correct!")
else:
    print(":(")
