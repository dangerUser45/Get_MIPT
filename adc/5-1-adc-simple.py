import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

troyka_pin     = 13
comparator_pin = 14
dac_pins       = [8, 11, 7, 1, 0, 5, 12, 6]

GPIO.setup(dac_pins, GPIO.OUT)
GPIO.setup(comparator_pin, GPIO.IN)
GPIO.setup(troyka_pin, GPIO.OUT, initial = 1)


def number_to_bin(num):
    return [int(bit) for bit in bin(num)[2:].zfill(8)]

BASE_VOLTAGE = 3.3
SLEEP_TIME   = 0.001

def adc():
    for i in range(0, 256):
        GPIO.output(dac_pins, number_to_bin(i) )
        time.sleep(SLEEP_TIME)
        if (GPIO.input(comparator_pin) == 1):
            return i

    return 256

try:
    while(1):
        voltage = adc() / 256 * BASE_VOLTAGE
        print(f'Voltage = {voltage:.2f} V')

finally:
    GPIO.output(dac_pins, 0)
    GPIO.output(troyka_pin, 0)
    GPIO.cleanup()